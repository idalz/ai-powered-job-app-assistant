from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
from app.core.llm import extract_job_info
from app.core.logger import logger

router = APIRouter()

@router.post("/parse")
async def parse_job_description(job_text: str = Body(..., embed=True)):
    logger.info("Received job description for parsing")
    
    if not job_text.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    result = extract_job_info(job_text)
    return JSONResponse(content=result)
