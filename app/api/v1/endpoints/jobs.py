from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.core.llm import extract_job_info
from app.core.logger import logger

router = APIRouter()

@router.post("/parse")
async def parse_job_description(job_text: str = Body(..., embed=True)):
    logger.info("Received job description for parsing")
    result = extract_job_info(job_text)
    return JSONResponse(content=result)
