from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.resumes import router as resumes_router
from app.api.v1.endpoints.letters import router as letters_router
from app.api.v1.endpoints.job_analysis import router as job_analysis_router
from app.api.v1.endpoints.recruiter_search import router as recruiter_search_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(resumes_router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(letters_router, prefix="/letters", tags=["Letters"])
api_router.include_router(job_analysis_router, prefix="/job-analysis", tags=["Job Analysis"])
api_router.include_router(recruiter_search_router, prefix="/recruiter-search", tags=["Recruiter Search"])
