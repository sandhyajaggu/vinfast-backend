from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.sql import func
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)   
    created_at = Column(DateTime(timezone=True), server_default=func.now())



