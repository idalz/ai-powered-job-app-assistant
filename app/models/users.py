from sqlalchemy import Column, String, ForeignKey
from app.db.database import Base



class UserCred(Base):
    __tablename__ = "users_cred"

    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)


class UserInfo(Base):
    __tablename__ = "users_info"

    email = Column(String, ForeignKey("users_cred.email", ondelete="CASCADE"), primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, default="")
    linkedin_url = Column(String, default="")
    github_url = Column(String, default="")
    resume = Column(String, default="")
    