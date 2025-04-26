
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.users import UserCreate, UserLogin
from app.crud.user_crud import register_user, authenticate_user, get_user_info, update_user_info

router = APIRouter()

# Register a new user
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Login 
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful!"}

# Read user info
@router.get("/user/info")
def read_user_info(email: str, db: Session = Depends(get_db)):
    try:
        user_info = get_user_info(db, email)
        return user_info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Update user info
@router.put("/user/info")
def update_user(email: str, updated_fields: dict, db: Session = Depends(get_db)):
    try:
        return update_user_info(db, email, updated_fields)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    