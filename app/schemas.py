from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ------------------------------
# User Schemas
# ------------------------------

class UserCreate(BaseModel):
    """Schema for user signup"""
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str

class UserOut(BaseModel):
    """Schema for returning user info"""
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
        # For Pydantic v2, use:
        # from_attributes = True

# ------------------------------
# History Schemas
# ------------------------------

class HistoryCreate(BaseModel):
    """Schema for creating a history record"""
    user_id: Optional[int] = None  # optional for logged-in user
    input_text: str
    corrected_text: Optional[str] = None  # optional on input

class HistoryOut(BaseModel):
    """Schema for returning history record"""
    id: int
    user_id: Optional[int] = None
    input_text: str
    corrected_text: str
    timestamp: datetime

    class Config:
        orm_mode = True
        # For Pydantic v2, use:
        # from_attributes = True
