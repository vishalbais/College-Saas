from fastapi import FastAPI
from app.api.v1 import auth, colleges, events, students, checkins, reports
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.db import session
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="College SaaS API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(colleges.router, prefix="/api/v1")
app.include_router(events.router, prefix="/api/v1")
app.include_router(students.router, prefix="/api/v1")
app.include_router(checkins.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")

# Serve media in dev
if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")

# startup event to ensure DB connection - migrations expected via Alembic externally
@app.on_event("startup")
async def startup():
    # Optionally run simple create_all for dev (not recommended for prod)
    from app.models.models import Base
    from app.db.session import engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
