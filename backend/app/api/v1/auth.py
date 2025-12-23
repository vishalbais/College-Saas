from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.schemas import UserCreate, Token
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User, College
from sqlalchemy import select
from app.utils.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Only SuperAdmin can create colleges and link users to other colleges in prod
    stmt = select(User).filter(User.email == user_in.email)
    r = await db.execute(stmt)
    exists = r.scalars().first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed,
        full_name=user_in.full_name,
        role=user_in.role,
        college_id=user_in.college_id
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    token = create_access_token(subject=user.id, role=user.role, college_id=user.college_id)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login(form_data: dict, db: AsyncSession = Depends(get_db)):
    """
    For OAuth2PasswordBearer from frontend, you can implement OAuth2PasswordRequestForm.
    Here we accept a JSON payload with email & password (for simplicity).
    """
    email = form_data.get("username") or form_data.get("email")
    password = form_data.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    stmt = select(User).filter(User.email == email)
    r = await db.execute(stmt)
    user = r.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.id, role=user.role, college_id=user.college_id)
    return {"access_token": token, "token_type": "bearer"}
