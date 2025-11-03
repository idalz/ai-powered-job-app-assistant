from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.llm import match_resume_to_job, extract_job_info
from app.core.logger import logger
from app.db.deps import get_db
from app.crud.resumes import get_resume_by_email
from app.api.deps.current_user import get_current_user_payload

router = APIRouter()

# Job info
@router.post("/job-info")
async def parse_job_description(
    job_text: str = Body(..., embed=True),
    current_user: dict = Depends(get_current_user_payload)
):
    logger.info("Received job description for parsing")
    
    if not job_text.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    result = extract_job_info(job_text)
    return JSONResponse(content=result)

# Resume-job match
@router.post("/match")
def match_resume_and_job(
    job_info: str = Body(..., embed=True),
    current_user: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    logger.info("Running resume-job matching.")

    # Get email from token
    email = current_user.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid user token.")

    # Fetch resume from database
    resume_info = get_resume_by_email(db, email)
    if not resume_info:
        raise HTTPException(status_code=404, detail="User resume not found.")

    # Perform matching using LLM
    result = match_resume_to_job(resume_info, job_info)

    return JSONResponse(content=result)
