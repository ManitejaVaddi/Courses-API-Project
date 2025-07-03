from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "student"

class UserLogin(BaseModel):
    username: str
    password: str

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class Course(CourseBase):
    id: int
    class Config:
        orm_mode = True

class EnrollmentBase(BaseModel):
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    completed: bool
    class Config:
        orm_mode = True
