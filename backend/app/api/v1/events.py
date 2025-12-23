from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schemas import EventCreate, EventRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.models import Event
from sqlalchemy import select
from app.api.v1.deps import get_current_user, require_roles
from typing import List

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventRead)
async def create_event(event_in: EventCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # only CollegeAdmin or SuperAdmin can create
    if current_user.role not in ("CollegeAdmin", "SuperAdmin"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    college_id = current_user.college_id if current_user.role != "SuperAdmin" else event_in.settings.get("college_id")
    if not college_id:
        raise HTTPException(status_code=400, detail="college_id required for event")
    event = Event(
        name=event_in.name,
        date=event_in.date,
        venue=event_in.venue,
        description=event_in.description,
        capacity=event_in.capacity,
        settings=event_in.settings,
        college_id=college_id
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

@router.get("/", response_model=List[EventRead])
async def list_events(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # Return only events for the user's college unless SuperAdmin
    if current_user.role == "SuperAdmin":
        r = await db.execute(select(Event))
    else:
        r = await db.execute(select(Event).filter(Event.college_id == current_user.college_id))
    return r.scalars().all()
