from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, users, job_analysis, jobs, resumes, letters, recruiter_search

app = FastAPI(title="AI Job Assistant", version="1.0.0")

# CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1/endpoints/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/endpoints/users", tags=["Users"])
app.include_router(jobs.router, prefix="/api/v1/endpoints/jobs", tags=["Jobs"])
app.include_router(resumes.router, prefix="/api/v1/endpoints/resumes", tags=["Resumes"])
app.include_router(letters.router, prefix="/api/v1/endpoints/letters", tags=["Letters"])
app.include_router(job_analysis.router, prefix="/api/v1/endpoints/job-analysis", tags=["Job Analysis"])
app.include_router(recruiter_search.router, prefix="/api/v1/endpoints/recruiter-search", tags=["Recruiter Search"])
