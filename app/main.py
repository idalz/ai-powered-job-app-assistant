from fastapi import FastAPI
from app.api.v1.endpoints import jobs, resumes, letters, assistant
from app.api.v1.endpoints import users

app = FastAPI(title="AI Job Assistant")

app.include_router(users.router, prefix="/api/v1/endpoints/jobs", tags=["Users"])
app.include_router(jobs.router, prefix="/api/v1/endpoints/jobs", tags=["Jobs"])
app.include_router(resumes.router, prefix="/api/v1/endpoints/resumes", tags=["Resumes"])
app.include_router(letters.router, prefix="/api/v1/endpoints/letters", tags=["Letters"])
app.include_router(assistant.router, prefix="/api/v1/endpoints/assistant", tags=["Assistant"])

@app.get("/")
def root():
    return {"message": "First try."}
