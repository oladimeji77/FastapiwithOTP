from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, func, ForeignKey
from database import Base, Base2
from typing import Optional
from pydantic import EmailStr
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


# Define a model (representing a table in MySQL)
class UserCreate(Base):
    __tablename__ = "UserCreate"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=False, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=True)
    verified_at = Column(Date, nullable=True)
    registered_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    phone_number = Column(String(100), nullable=False, unique=True)
    account_type = Column(String(15), nullable=True)
    totp_secret = Column(String)

class Candidate(Base):
    __tablename__ = "candidate"
    candidate_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), nullable=False, unique=True)
    Party = Column(String(100), nullable=False)
    

class Vote(Base):
    __tablename__ = "election"
    voter_id = Column(Integer, ForeignKey("UserCreate.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidate.candidate_id", ondelete="CASCADE"), nullable=False)
    candidate_name = Column(String(20), ForeignKey("candidate.name",  ondelete="CASCADE"), nullable=False)
    

class SMS(Base2):
    __tablename__ = "sms"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), nullable=False)
    srcAddress = Column(String(100), nullable=False, default="ZENITHBANK")
    priority = Column(Integer, nullable=False)
    text = Column(String(1000), nullable=False)