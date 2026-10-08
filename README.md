# Internship and Student Management API

Week 2 backend internship project built with FastAPI and SQLAlchemy.

## Features

- User registration and login
- JWT authentication
- Role-based authorization
- Student CRUD
- Internship application CRUD
- Student/application relationship
- Search
- Filtering
- Application status updates
- Error handling
- Swagger documentation
- Render deployment support

## Run locally

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the API

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Authentication

Register:

`POST /auth/register`

Example:

```json
{
  "full_name": "Admin User",
  "email": "admin@example.com",
  "password": "admin123",
  "role": "admin"
}
```

Login:

`POST /auth/login`

Swagger uses OAuth2 form fields:

- username = email
- password = password

Copy the returned token and click **Authorize** in Swagger.

## Important production note

The public registration endpoint currently accepts the `role` field so the project is easy to demonstrate. In a real system, public registration should always create a student, while admin accounts should be created securely by an administrator or deployment process.

## Render

Use PostgreSQL on Render and set:

```text
DATABASE_URL=<Render PostgreSQL connection string>
SECRET_KEY=<long random secret>
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
