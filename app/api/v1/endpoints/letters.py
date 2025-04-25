from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.core.llm import generate_cover_letter
from app.core.logger import logger

router = APIRouter()

@router.post("/generate")
async def generate_letter(
    resume_info: str = Body(..., embed=True),
    job_info: str = Body(..., embed=True),
    guidelines: str = Body(default="", embed=True)
):
    logger.info("Generating tailored cover letter with extra guidelines")
    result = generate_cover_letter(resume_info, job_info, guidelines)
    return JSONResponse(content=result)
