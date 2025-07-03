from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, User, Course, Enrollment
from database import engine, get_db
from schemas import *
from auth import hash_password, verify_password, create_access_token
from dependencies import get_current_user, get_admin_user
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed, role=user.role)
    db.add(new_user)
    db.commit()
    return {"msg": "User registered"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/courses", response_model=Course)
def create_course(course: CourseBase, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.get("/courses", response_model=list[Course])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@app.post("/enroll", response_model=Enrollment)
def enroll(enroll_data: EnrollmentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing = db.query(Enrollment).filter_by(user_id=user.id, course_id=enroll_data.course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")
    enrollment = Enrollment(user_id=user.id, course_id=enroll_data.course_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment

@app.get("/me/enrollments", response_model=list[Enrollment])
def get_my_enrollments(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Enrollment).filter_by(user_id=user.id).all()

@app.put("/enrollments/{enroll_id}/complete")
def mark_complete(enroll_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    enrollment = db.query(Enrollment).filter_by(id=enroll_id, user_id=user.id).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not found")
    enrollment.completed = True
    db.commit()
    return {"msg": "Marked as completed"}
