from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    role: Literal["student", "admin"] = "student"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class StudentCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    university: str = Field(min_length=2, max_length=150)
    course: str = Field(min_length=2, max_length=150)
    level: str = Field(min_length=1, max_length=50)


class StudentUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    university: str | None = Field(default=None, min_length=2, max_length=150)
    course: str | None = Field(default=None, min_length=2, max_length=150)
    level: str | None = Field(default=None, min_length=1, max_length=50)


class StudentOut(StudentCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None


class ApplicationCreate(BaseModel):
    student_id: int
    company: str = Field(min_length=2, max_length=150)
    position: str = Field(min_length=2, max_length=150)
    track: str = Field(min_length=2, max_length=100)
    motivation: str = Field(min_length=10)
    portfolio_url: HttpUrl | None = None
    resume_url: HttpUrl | None = None
    join_innovation_club: bool = False


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=2, max_length=150)
    position: str | None = Field(default=None, min_length=2, max_length=150)
    track: str | None = Field(default=None, min_length=2, max_length=100)
    motivation: str | None = Field(default=None, min_length=10)
    portfolio_url: HttpUrl | None = None
    resume_url: HttpUrl | None = None
    join_innovation_club: bool | None = None


class StatusUpdate(BaseModel):
    status: Literal["pending", "reviewing", "shortlisted", "accepted", "rejected"]


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    company: str
    position: str
    track: str
    motivation: str
    portfolio_url: str | None
    resume_url: str | None
    status: str
    join_innovation_club: bool
    submitted_at: datetime
