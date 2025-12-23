from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.v1.deps import get_current_user
from app.models.models import Student, Event, Checkin
from app.schemas.schemas import CheckinCreate, CheckinRead
from sqlalchemy import select
from datetime import datetime

router = APIRouter(prefix="/checkins", tags=["checkins"])

@router.post("/", response_model=CheckinRead)
async def create_checkin(payload: CheckinCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # Only admins/editors of the college or SuperAdmin
    if current_user.role not in ("CollegeAdmin", "Editor", "SuperAdmin"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # find student by uid or id
    student = None
    if payload.uid:
        q = await db.execute(select(Student).filter(Student.uid == payload.uid))
        student = q.scalars().first()
    elif payload.student_id:
        q = await db.execute(select(Student).filter(Student.id == payload.student_id))
        student = q.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # permission: same college
    if current_user.role != "SuperAdmin" and current_user.college_id != student.college_id:
        raise HTTPException(status_code=403, detail="Cross-tenant access denied")

    # ensure event exists
    q = await db.execute(select(Event).filter(Event.id == payload.event_id))
    event = q.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # already checked-in?
    q = await db.execute(select(Checkin).filter(Checkin.student_id == student.id))
    existing = q.scalars().first()
    if existing:
        # return existing (duplicate handling)
        return existing

    checkin = Checkin(
        student_id=student.id,
        event_id=payload.event_id,
        device=payload.device or "web",
        operator_id=current_user.id,
        timestamp=datetime.utcnow()
    )
    db.add(checkin)
    await db.commit()
    await db.refresh(checkin)
    return checkin
