from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from uuid import uuid4
from app.core.logger import logger

UPLOAD_DIR = "app/uploads" # Store uploads here

os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

# File upload
@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        logger.warning(f"Rejected file upload: {file.filename}")
        raise HTTPException(status_code=400, detail="Only .pdf and .docx files are supported.")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)

    logger.info(f"Uploaded resume: {file.filename} saved as {file_path}")
    return JSONResponse(content={"message": "Resume uploaded", "file_path": file_path})


@router.post("/")
def upload_resume():
    return {"message": "Resume upload and parsing will go here."}
