from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def upload_resume():
    return {"message": "Resume upload and parsing will go here."}
