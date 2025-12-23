from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.schemas import CollegeCreate, CollegeRead
from app.models.models import College
from sqlalchemy import select
from app.api.v1.deps import get_current_user, require_roles
from typing import List

router = APIRouter(prefix="/colleges", tags=["colleges"])

@router.post("/", response_model=CollegeRead, dependencies=[Depends(require_roles("SuperAdmin"))])
async def create_college(college_in: CollegeCreate, db: AsyncSession = Depends(get_db)):
    college = College(name=college_in.name, slug=college_in.slug)
    db.add(college)
    await db.commit()
    await db.refresh(college)
    return college

@router.get("/", response_model=List[CollegeRead], dependencies=[Depends(require_roles("SuperAdmin"))])
async def list_colleges(db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(College))
    return r.scalars().all()
