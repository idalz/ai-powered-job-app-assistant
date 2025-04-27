
from pydantic import BaseModel, EmailStr
from typing import Optional, List

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

class UserInfoSchema(BaseModel):
    email: EmailStr
    name: str
    phone_number: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    github_url: Optional[str] = ""
    resume: Optional[str] = ""
    is_recruiter: Optional[bool] = False

    class ConfigDict:
        from_attributes = True   

class EmailsRequest(BaseModel):
    emails: List[EmailStr]

class UserUpdateSchema(BaseModel):
    name: str
    phone_number: Optional[str] = ""
    linkedin_url: Optional[str] = ""
    github_url: Optional[str] = ""

    class ConfigDict:
        from_attributes = True   