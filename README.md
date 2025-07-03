# Courses-API-Project
We can access the Fast API network in this project 

Courses API Project (FastAPI)

This is a backend API for managing course registrations, built using **FastAPI** and **JWT authentication**.

# Features

- User registration & login with JWT
-  Course creation and listing
-  Enroll in courses
-  Mark courses as complete
-  Built-in Swagger UI for testing

# Tech Stack

- FastAPI
- SQLAlchemy
- SQLite (or your DB of choice)
- JWT (python-jose)
- Pydantic
- Uvicorn

| Method | Endpoint                     | Description                |
| ------ | ---------------------------- | -------------------------- |
| POST   | `/register`                  | Register a new user        |
| POST   | `/login`                     | Login and get JWT token    |
| GET    | `/courses`                   | List all available courses |
| POST   | `/courses`                   | Create a new course        |
| POST   | `/enroll`                    | Enroll in a course         |
| GET    | `/me/enrollments`            | View your enrollments      |
| PUT    | `/enrollments/{id}/complete` | Mark course as complete    |

#contact
To Maniteja
