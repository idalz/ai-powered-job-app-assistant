from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.core.rag import search_resumes
from app.core.logger import logger

router = APIRouter()

# Search best matching candidates
@router.post("/search-candidates")
def search_candidates(
    job_description: str = Body(..., embed=True)
):
    logger.info("Recruiter searching for candidates based on job description.")

    # Search top 5 resumes
    search_results = search_resumes(job_description, k=5)

    return JSONResponse(content={"results": search_results})