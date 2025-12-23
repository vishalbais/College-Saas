from sqlalchemy import (
    Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    full_name = Column(String(256))
    role = Column(String(50), index=True)  # SuperAdmin, CollegeAdmin, Editor
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    college = relationship("College", back_populates="users")

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    slug = Column(String(256), unique=True, index=True)
    meta = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    users = relationship("User", back_populates="college")
    events = relationship("Event", back_populates="college")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    date = Column(DateTime, nullable=False)
    venue = Column(String(512))
    description = Column(Text)
    capacity = Column(Integer, default=0)
    settings = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    college = relationship("College", back_populates="events")
    students = relationship("Student", back_populates="event")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(256), nullable=False)
    year = Column(String(50))
    branch = Column(String(128))
    roll_no = Column(String(128))
    email = Column(String(256), index=True)
    mobile = Column(String(50))
    payment_status = Column(Boolean, default=False)
    uid = Column(String(128), unique=True, index=True, nullable=True)
    qr_image_path = Column(String(1024), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    event = relationship("Event", back_populates="students")

    __table_args__ = (
        UniqueConstraint('event_id', 'email', name='uq_event_email'),
        UniqueConstraint('event_id', 'roll_no', name='uq_event_roll'),
    )

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    sent_at = Column(DateTime, nullable=True)
    delivery_channel = Column(String(50), default="email")  # email / whatsapp
    status = Column(String(50), default="pending")  # pending / sent / failed
    meta = Column(JSON, default={})

class Checkin(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    device = Column(String(256))
    operator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student")
    event = relationship("Event")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String(256))
    entity = Column(String(256))
    entity_id = Column(String(128))
    meta = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
