
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone_number: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    github_url: Optional[str] = ""
    resume: Optional[str] = ""
    is_recruiter: Optional[bool] = False 

class UserLogin(BaseModel):
    email: EmailStr
    password: str