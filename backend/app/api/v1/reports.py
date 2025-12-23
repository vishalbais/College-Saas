from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.v1.deps import get_current_user
from sqlalchemy import select, func
from app.models.models import Student, Event, Checkin
from typing import Dict

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/event/{event_id}")
async def event_report(event_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # permission checked below
    q = await db.execute(select(Event).filter(Event.id == event_id))
    event = q.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if current_user.role != "SuperAdmin" and current_user.college_id != event.college_id:
        raise HTTPException(status_code=403, detail="Access denied")

    total_q = await db.execute(select(func.count(Student.id)).filter(Student.event_id == event_id))
    total = total_q.scalars().first() or 0
    paid_q = await db.execute(select(func.count(Student.id)).filter(Student.event_id == event_id, Student.payment_status == True))
    paid = paid_q.scalars().first() or 0
    checked_q = await db.execute(select(func.count(Checkin.id)).filter(Checkin.event_id == event_id))
    checked = checked_q.scalars().first() or 0

    return {"event_id": event_id, "total": total, "paid": paid, "checked_in": checked, "not_checked_in": total - checked}
