from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from fastapi.responses import JSONResponse
import os
from uuid import uuid4
from app.core.logger import logger
from app.core.rag import store_resume, search_resumes
from app.core.llm import extract_resume_info
from app.services.resume_parser import parse_pdf_resume, parse_docx_resume


UPLOAD_DIR = "app/uploads" # Store uploads here

os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

# File upload
@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    name: str = Body(default="", embed=True)
):
    # Read file and create path
    if not file.filename.endswith((".pdf", ".docx", ".txt")):
        logger.warning(f"Rejected file upload: {file.filename}")
        raise HTTPException(status_code=400, detail="Only .pdf and .docx files are supported.")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)

    logger.info(f"Uploaded resume: {file.filename} saved as {file_path}")
    
    # Parse file
    if file.filename.endswith(".pdf"):
        parsed_text = parse_pdf_resume(file_path)
    else:
        parsed_text = parse_docx_resume(file_path)

    # LLM info extraction
    extracted_info = extract_resume_info(parsed_text)
    
    # Store in vector
    pinecone_store_result = store_resume(parsed_text, metadata={"filename": file.filename, "name": name})

    # Return json 
    return JSONResponse(content={
        "message": "Resume uploaded and parsed successfully",
        "file_path": file_path,
        "parsed_text": parsed_text,
        "extracted_info": extracted_info,
        "pinecone_store": pinecone_store_result
    })

# Store a resume
@router.post("/store")
def store(text: str = Body(..., embed=True)):
    result = store_resume(text, metadata={"source": "user_upload"})
    return JSONResponse(content={
        "message": "Resume stored successfully.",
        "pinecone_result": result
    })

# Search for resume
@router.post("/search")
def search(query: str = Body(..., embed=True)):
    return search_resumes(query)
