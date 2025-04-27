from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse

from app.db.deps import get_db
from app.schemas.users import UserCreate, UserInfoSchema, EmailsRequest, UserUpdateSchema
from app.crud.user_crud import register_user, get_user_info, update_user_info, get_users_by_emails
from app.api.deps.jwt_bearer import JWTBearer
from app.api.deps.current_user import get_current_user_payload

router = APIRouter()

# Register a new user 
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Read my own user info 
@router.get("/me", response_model=UserInfoSchema)
def read_user_info(current_user: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    try:
        email = current_user.get("email")
        user_info = get_user_info(db, email)
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found.")
        return user_info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Update my own user info 
@router.put("/me", response_model=UserUpdateSchema)
def update_user(updated_fields: UserUpdateSchema = Body(...), current_user: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    email = current_user.get("email")
    try:
        updated_user = update_user_info(db, email, updated_fields.model_dump())
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found.")
        return JSONResponse(content={
            "message": "User info updated successfully.",
            "updated_fields": updated_user
        })
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Search multiple users by emails (for recruiters)
@router.post("/search-users", response_model=List[UserInfoSchema], dependencies=[Depends(JWTBearer())])
def search_users_by_emails(
    request: EmailsRequest,
    db: Session = Depends(get_db),
):
    users = get_users_by_emails(db, request.emails)
    return users
