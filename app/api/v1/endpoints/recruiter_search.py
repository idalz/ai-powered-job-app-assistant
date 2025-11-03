from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.core.rag import search_resumes
from app.core.logger import logger
from app.api.deps.current_user import get_current_user_payload

router = APIRouter()

# Search best matching candidates
@router.post("/candidates")
def search_candidates(
    job_description: str = Body(..., embed=True),
    current_user: dict = Depends(get_current_user_payload)
):
    # Verify user is a recruiter
    if not current_user.get("is_recruiter"):
        raise HTTPException(status_code=403, detail="Only recruiters can search candidates")

    logger.info(f"Recruiter {current_user.get('email')} searching for candidates based on job description.")

    # Search top 5 resumes
    search_results = search_resumes(job_description, k=5)

    return JSONResponse(content={"results": search_results})
