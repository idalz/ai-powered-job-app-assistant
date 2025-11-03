from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.users import UserCred, UserInfo
from app.core.security import create_access_token
from app.core.logger import logger
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
limiter = Limiter(key_func=get_remote_address)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Login endpoint with rate limiting (5 attempts per minute)
@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    logger.info(f"Login attempt for {email}")

    user_cred = db.query(UserCred).filter(UserCred.email == email).first()
    user_info = db.query(UserInfo).filter(UserInfo.email == email).first()

    if not user_cred or not verify_password(password, user_cred.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Prepare data for JWT token
    token_data = {
        "email": email,
        "is_recruiter": user_info.is_recruiter if user_info else False
    }

    # Create access token
    access_token = create_access_token(token_data)

    logger.info(f"Token created for {email}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
