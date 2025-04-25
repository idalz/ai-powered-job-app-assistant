from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.core.llm import generate_cover_letter, match_resume_to_job
from app.services.check_result_type import check_result_type

from app.core.logger import logger

router = APIRouter()

# Generate cover letter
@router.post("/generate")
async def generate_letter(
    resume_info: str = Body(..., embed=True),
    job_info: str = Body(..., embed=True),
    guidelines: str = Body(default="", embed=True)
):
    logger.info("Generating tailored cover letter with extra guidelines")
    
    raw_cover_letter = generate_cover_letter(resume_info, job_info, guidelines)
    cover_letter = check_result_type(raw_cover_letter, expected_type=str, fallback="")

    match_result = match_resume_to_job(resume_info, job_info)
    
    logger.info(f"Generated cover letter: {cover_letter}")

    return JSONResponse(content={
        "resume_info": resume_info,
        "job_info": job_info,
        "match_result": match_result,
        "cover_letter": cover_letter
    })
