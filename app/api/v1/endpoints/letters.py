from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def generate_letter():
    return {"message": "Cover letter generation will go here."}
