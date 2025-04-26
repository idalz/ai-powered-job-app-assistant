from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.core.llm import match_resume_to_job
from app.core.logger import logger
from app.api.deps.jwt_bearer import JWTBearer

router = APIRouter()

# Resume-job match
@router.post("/match", dependencies=[Depends(JWTBearer())])
def match_resume_and_job(
    resume_info: str = Body(..., embed=True),
    job_info: str = Body(..., embed=True)
):
    logger.info("Running resume-job matching.")
    result = match_resume_to_job(resume_info, job_info)
    return JSONResponse(content=result)

