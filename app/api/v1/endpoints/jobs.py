from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_jobs():
    return {"message": "List of jobs or parsing logic will go here."}
