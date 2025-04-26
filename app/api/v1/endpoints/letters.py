from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.crud.resumes import get_resume_by_email
from app.core.llm import generate_cover_letter
from app.services.check_result_type import check_result_type
from app.core.logger import logger
from app.api.deps.current_user import get_current_user_payload


router = APIRouter()

# Generate cover letter
@router.post("/generate")
async def generate_letter(
    job_info: str = Body(..., embed=True),
    guidelines: str = Body(default="", embed=True),
    current_user: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    email = current_user.get("email")
    
    logger.info(f"Generating cover letter for {email}")

    # Fetch resume using CRUD function
    resume_info = get_resume_by_email(db, email)
    if not resume_info:
        raise HTTPException(status_code=404, detail="User resume not found.")

    # Generate cover letter using LLM
    raw_cover_letter = generate_cover_letter(resume_info, job_info, guidelines)
    cover_letter = check_result_type(raw_cover_letter, expected_type=str, fallback="")

    logger.info(f"Generated cover letter successfully for {email}")

    return JSONResponse(content={
        "email": email,
        "cover_letter": cover_letter
    })
