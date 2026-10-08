from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, students, applications

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Internship and Student Management API",
    description="Week 2 internship project - CRUD, relationships, authentication, authorization, search, filtering and Swagger.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(applications.router)


@app.get("/")
def root():
    return {
        "message": "Internship and Student Management API is running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
