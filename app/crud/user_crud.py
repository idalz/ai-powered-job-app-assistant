from sqlalchemy.orm import Session
from app.models.users import UserCred, UserInfo
from app.schemas.users import UserCreate
from app.core.security import get_password_hash, verify_password 

def register_user(db: Session, user: UserCreate):
    # Check if user already exists
    db_user = db.query(UserCred).filter(UserCred.email == user.email).first()
    if db_user:
        raise ValueError("Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create UserCred record
    new_user_cred = UserCred(
        email=user.email,
        hashed_password=hashed_password
    )

    # Create UserInfo record
    new_user_info = UserInfo(
    email=user.email,
    name=user.name,
    phone_number=user.phone_number or "",
    linkedin_url=user.linkedin_url or "",
    github_url=user.github_url or "",
    resume=user.resume or "",
    is_recruiter=user.is_recruiter or False
)

    # Add both to the session
    db.add(new_user_cred)
    db.add(new_user_info)

    # Commit
    db.commit()
    db.refresh(new_user_cred)

    return {"message": "User registered successfully!"}

def authenticate_user(db: Session, email: str, password: str):
    # Get the user by email
    db_user = db.query(UserCred).filter(UserCred.email == email).first()
    
    if not db_user:
        return None  # user not found

    # Verify password
    if not verify_password(password, db_user.hashed_password):
        return None  # password incorrect

    return db_user  # authentication successful

def update_user_info(db: Session, email: str, updated_info: dict):
    # Find the user info by email
    user_info = db.query(UserInfo).filter(UserInfo.email == email).first()
    if not user_info:
        raise ValueError("User info not found.")

    # Define fields that are allowed to update
    allowed_fields = {"name", "phone_number", "linkedin_url", "github_url", "resume"}

    # Update only allowed fields
    for field, value in updated_info.items():
        if field in allowed_fields:
            setattr(user_info, field, value)

    db.commit()
    db.refresh(user_info)

    return {"message": "User info updated successfully!"}

def get_user_info(db: Session, email: str):
    # Find user info by email
    user_info = db.query(UserInfo).filter(UserInfo.email == email).first()
    if not user_info:
        raise ValueError("User info not found.")

    return user_info
