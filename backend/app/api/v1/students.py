from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.v1.deps import get_current_user
from app.models.models import Student, Event, Ticket
from app.schemas.schemas import StudentCreate, StudentRead
from typing import List
from sqlalchemy import select
from app.storage.files import save_upload
import pandas as pd
from io import BytesIO
from app.services.qr_service import generate_uid, generate_qr
from app.tasks import send_ticket_task
import os

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/{event_id}/upload", response_model=List[StudentRead])
async def upload_students(event_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # Only CollegeAdmin / Editor of the same tenant
    if current_user.role not in ("CollegeAdmin", "Editor", "SuperAdmin"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    # ensure tenant
    q = await db.execute(select(Event).filter(Event.id == event_id))
    event = q.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if current_user.role != "SuperAdmin" and current_user.college_id != event.college_id:
        raise HTTPException(status_code=403, detail="Cross-tenant access denied")

    # Save upload to disk (optional)
    rel, path = save_upload(file, subdir=f"imports/{event_id}")
    # Read as pandas
    ext = os.path.splitext(file.filename)[1].lower()
    if ext in (".csv",):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    # expect columns: name, year, branch, roll_no, email, mobile, payment_status
    created = []
    for _, row in df.iterrows():
        email = row.get("email")
        roll_no = row.get("roll_no")
        # check duplicates per event:
        dup_q = await db.execute(select(Student).filter(Student.event_id == event_id).filter((Student.email == email) | (Student.roll_no == roll_no)))
        if dup_q.scalars().first():
            continue
        student = Student(
            event_id=event_id,
            college_id=event.college_id,
            name=row.get("name") or "Unknown",
            year=row.get("year"),
            branch=row.get("branch"),
            roll_no=roll_no,
            email=email,
            mobile=row.get("mobile"),
            payment_status=bool(row.get("payment_status"))
        )
        # Generate UID & QR if paid
        if student.payment_status:
            student.uid = generate_uid()
            rel_qr = generate_qr(student.uid, event_id)
            student.qr_image_path = rel_qr
        db.add(student)
        await db.flush()
        created.append(student)
        # create ticket record
        ticket = Ticket(student_id=student.id, delivery_channel="email")
        db.add(ticket)

        # send ticket asynchronously if paid and email exists and event setting allows
        if student.payment_status and student.email:
            # basic html
            html = f"<h3>Ticket for {event.name}</h3><p>UID: {student.uid}</p>"
            # pass absolute file path for attachment
            attachments = []
            if student.qr_image_path:
                attachments.append(os.path.join(os.getenv("MEDIA_ROOT", "/data/media"), student.qr_image_path))
            # offload to celery
            send_ticket_task.delay(student.email, f"Ticket: {event.name}", html, attachments)
    await db.commit()
    # load and return created list
    ids = [s.id for s in created]
    if not ids:
        return []
    q = await db.execute(select(Student).filter(Student.id.in_(ids)))
    return q.scalars().all()
