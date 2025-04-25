from fastapi import FastAPI
from app.api.v1.endpoints import jobs, resumes, letters, assistant

app = FastAPI(title="AI Job Assistant")

app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(resumes.router, prefix="/api/v1/resumes", tags=["Resumes"])
app.include_router(letters.router, prefix="/api/v1/letters", tags=["Letters"])
app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["Assistant"])

@app.get("/")
def root():
    return {"message": "First try."}
