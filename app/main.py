from fastapi import FastAPI
from app.api.v1.endpoints import users, job_analysis, jobs, resumes, letters, recruiter_search

app = FastAPI(title="AI Job Assistant")

app.include_router(users.router, prefix="/api/v1/endpoints/jobs", tags=["Users"])
app.include_router(jobs.router, prefix="/api/v1/endpoints/jobs", tags=["Jobs"])
app.include_router(resumes.router, prefix="/api/v1/endpoints/resumes", tags=["Resumes"])
app.include_router(letters.router, prefix="/api/v1/endpoints/letters", tags=["Letters"])
app.include_router(job_analysis.router, prefix="/api/v1/endpoints/job_analysis", tags=["Job Analysis"])
app.include_router(recruiter_search.router, prefix="/api/v1/endpoints/search-candidates", tags=["Search Candidates"])

@app.get("/")
def root():
    return {"message": "First try."}
