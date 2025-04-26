from sqlalchemy.orm import Session
from app.models.users import UserInfo

def get_resume_by_email(db: Session, email: str):
    user_info = db.query(UserInfo).filter(UserInfo.email == email).first()
    if not user_info or not user_info.resume:
        return None
    return user_info.resume

def update_resume(db: Session, email: str, resume_text: str):
    user_info = db.query(UserInfo).filter(UserInfo.email == email).first()
    if not user_info:
        return None
    
    user_info.resume = resume_text
    db.commit()
    db.refresh(user_info)
    return user_info
