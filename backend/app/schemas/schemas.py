from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr
import datetime

# Shared
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[int]
    exp: Optional[int]
    role: Optional[str]
    college_id: Optional[int]

# User
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str]
    role: Optional[str] = "CollegeAdmin"
    college_id: Optional[int]

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str
    college_id: Optional[int]

    class Config:
        orm_mode = True

# College & Event
class CollegeCreate(BaseModel):
    name: str
    slug: Optional[str]

class CollegeRead(BaseModel):
    id: int
    name: str
    slug: Optional[str]

    class Config:
        orm_mode = True

class EventCreate(BaseModel):
    name: str
    date: datetime.datetime
    venue: Optional[str]
    description: Optional[str]
    capacity: Optional[int] = 0
    settings: Optional[dict] = {}

class EventRead(BaseModel):
    id: int
    name: str
    date: datetime.datetime
    venue: Optional[str]
    description: Optional[str]
    capacity: Optional[int]
    settings: Optional[dict]
    college_id: int

    class Config:
        orm_mode = True

# Student
class StudentCreate(BaseModel):
    name: str
    year: Optional[str]
    branch: Optional[str]
    roll_no: Optional[str]
    email: Optional[EmailStr]
    mobile: Optional[str]
    payment_status: bool = False

class StudentRead(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr]
    roll_no: Optional[str]
    uid: Optional[str]
    qr_image_path: Optional[str]
    payment_status: bool

    class Config:
        orm_mode = True

# Check-in
class CheckinCreate(BaseModel):
    uid: Optional[str]
    student_id: Optional[int]
    event_id: int
    device: Optional[str]

class CheckinRead(BaseModel):
    id: int
    student_id: int
    event_id: int
    device: Optional[str]
    operator_id: Optional[int]
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
