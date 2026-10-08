from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Application, Student, User
from app.schemas import (
    ApplicationCreate,
    ApplicationOut,
    ApplicationUpdate,
    StatusUpdate,
)
from app.security import get_current_user, require_admin

router = APIRouter(prefix="/applications", tags=["Internship Applications"])

ALLOWED_STATUSES = {"pending", "reviewing", "shortlisted", "accepted", "rejected"}


def get_application_or_404(application_id: int, db: Session) -> Application:
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


def can_access_application(application: Application, user: User) -> bool:
    return user.role == "admin" or (
        user.student is not None and application.student_id == user.student.id
    )


@router.post("/", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def create_application(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = db.get(Student, data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if current_user.role != "admin" and student.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only create an application for your own student profile",
        )

    application = Application(**data.model_dump(mode="json"))
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/", response_model=list[ApplicationOut])
def list_applications(
    search: str | None = Query(default=None, description="Search name, university, course, company or position"),
    status_filter: str | None = Query(default=None, alias="status"),
    university: str | None = None,
    course: str | None = None,
    track: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Application)
        .join(Application.student)
        .options(joinedload(Application.student))
        .order_by(Application.id.desc())
    )

    if current_user.role != "admin":
        if not current_user.student:
            return []
        stmt = stmt.where(Application.student_id == current_user.student.id)

    if search:
        term = f"%{search}%"
        stmt = stmt.where(
            or_(
                Student.full_name.ilike(term),
                Student.university.ilike(term),
                Student.course.ilike(term),
                Application.company.ilike(term),
                Application.position.ilike(term),
            )
        )

    if status_filter:
        if status_filter not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Use one of: {', '.join(sorted(ALLOWED_STATUSES))}",
            )
        stmt = stmt.where(Application.status == status_filter)

    if university:
        stmt = stmt.where(Student.university.ilike(f"%{university}%"))

    if course:
        stmt = stmt.where(Student.course.ilike(f"%{course}%"))

    if track:
        stmt = stmt.where(Application.track.ilike(f"%{track}%"))

    return db.scalars(stmt).unique().all()


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = get_application_or_404(application_id, db)

    if not can_access_application(application, current_user):
        raise HTTPException(status_code=403, detail="You cannot access this application")

    return application


@router.put("/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int,
    data: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = get_application_or_404(application_id, db)

    if not can_access_application(application, current_user):
        raise HTTPException(status_code=403, detail="You cannot update this application")

    for key, value in data.model_dump(exclude_unset=True, mode="json").items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)
    return application


@router.patch("/{application_id}/status", response_model=ApplicationOut)
def update_status(
    application_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    application = get_application_or_404(application_id, db)
    application.status = data.status
    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = get_application_or_404(application_id, db)

    if not can_access_application(application, current_user):
        raise HTTPException(status_code=403, detail="You cannot delete this application")

    db.delete(application)
    db.commit()
    return None
