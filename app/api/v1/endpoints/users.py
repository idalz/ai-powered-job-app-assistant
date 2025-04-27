
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.users import UserCreate
from app.crud.user_crud import register_user, authenticate_user, get_user_info, update_user_info
from app.api.deps.current_user import get_current_user_payload

router = APIRouter()

# Register a new user
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Read user info
@router.get("/info")
def read_user_info(current_user: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    email = current_user.get("email")
    try:
        user_info = get_user_info(db, email)
        return user_info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Update user info
@router.put("/info")
def update_user(updated_fields: dict, current_user: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    email = current_user.get("email")
    try:
        return update_user_info(db, email, updated_fields)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    