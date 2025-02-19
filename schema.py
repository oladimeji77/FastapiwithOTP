from pydantic import BaseModel, EmailStr, Field, constr, conint, validator
from datetime import datetime, date
from typing import Optional
import re

class UserCreate(BaseModel):
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=100)
    email: EmailStr
    is_active: Optional[bool] = Field(default=False)
    is_verified: Optional[bool] = Field(default=False)
    phone_number: str = Field(..., description="Nigerian phone number starting with +234 or 0 followed by 10 digits.")
    account_type: Optional[str] = Field(None, description="Type of bank account (e.g., savings, checking)")

    @validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        # Regular expression for Nigerian phone number validation
        pattern = re.compile(r"^(?:\+234|0)[789]\d{9}$")
        if not pattern.match(value):
            raise ValueError("Invalid Nigerian phone number. Must start with +234 or 0 followed by 10 digits.")
        return value
    

class UserRes(BaseModel):
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    is_active: Optional[bool] = Field(default=False)
    is_verified: Optional[bool] = Field(default=False)
    phone_number: str = Field(min_length=3, max_length=100)
    account_type: Optional[str] = Field(None, description="Type of bank account (e.g., savings, checking)")

    class Config:
        orm_mode = True  # Allows Pydantic to work with ORM objects directly


class UserUpdate(BaseModel):
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    phone_number: str = Field(..., description="Nigerian phone number starting with +234 or 0 followed by 10 digits.")
    account_type: Optional[str] = Field(None, description="Type of bank account (e.g., savings, checking)")

    @validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        # Regular expression for Nigerian phone number validation
        pattern = re.compile(r"^(?:\+234|0)[789]\d{9}$")
        if not pattern.match(value):
            raise ValueError("Invalid Nigerian phone number. Must start with +234 or 0 followed by 10 digits.")
        return value
##########################################################################################
class Token(BaseModel):
    access_token: str
    token_type: str
   


class TokenData(BaseModel):
    id: Optional[int] = None


##########################################################################################
class Candidate(BaseModel):    
    name: str
    Party: str


class Vote(BaseModel):
    candidate_id : int
    candidate_name : str
    
    

class VoteRes(BaseModel):
    voter_id : int
    candidate_id : int
    candidate_name : Candidate



# Pydantic Models for OTP
class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    otp : str