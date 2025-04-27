from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.core.llm import extract_resume_info
from app.core.rag import store_resume, search_resumes, delete_resume_by_email
from app.services.resume_parser import parse_pdf_resume, parse_docx_resume
from app.db.deps import get_db
from app.crud.resumes import update_resume
from app.api.deps.jwt_bearer import JWTBearer
from app.api.deps.current_user import get_current_user_payload

import os
from uuid import uuid4

UPLOAD_DIR = "app/uploads" # Store uploads here

os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

# File upload
@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    email = current_user.get("email")
    
    # Validate file type
    if not file.filename.endswith((".pdf", ".docx", ".txt")):
        logger.warning(f"Rejected file upload: {file.filename}")
        raise HTTPException(status_code=400, detail="Only .pdf, .docx, or .txt files are supported.")

    # Save uploaded file
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    logger.info(f"Uploaded resume: {file.filename} saved as {file_path}")

    # Parse resume text
    if file.filename.endswith(".pdf"):
        parsed_text = parse_pdf_resume(file_path)
    else:
        parsed_text = parse_docx_resume(file_path)

    # Update Resume in Database 
    updated_user = update_resume(db, email, parsed_text)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Manage Resume in Vectorstore
    try:
        delete_resume_by_email(email)  # Delete old vector (if exists)
    except Exception as e:
        logger.warning(f"No previous resume to delete for {email}: {str(e)}")

    pinecone_store_result = store_resume(parsed_text, metadata={"email": email})

    # Return response
    return JSONResponse(content={"message": "Resume uploaded and processed successfully."})

# Extract structured info from resume text using LLM.
@router.post("/extract-resume-info", dependencies=[Depends(JWTBearer())])
async def extract_info_from_resume(
    resume_text: str = Body(..., embed=True),
):
    extracted = extract_resume_info(resume_text)
    return JSONResponse(content=extracted)

# Store a resume
@router.post("/store", dependencies=[Depends(JWTBearer())])
def store(text: str = Body(..., embed=True)):
    result = store_resume(text, metadata={"source": "user_upload"})
    return JSONResponse(content={
        "message": "Resume stored successfully.",
        "pinecone_result": result
    })

# Search for resume
@router.post("/search", dependencies=[Depends(JWTBearer())])
def search(query: str = Body(..., embed=True)):
    return search_resumes(query)
