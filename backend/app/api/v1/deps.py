from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.utils.security import decode_token
from app.models.models import User
from sqlalchemy.future import select
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    q = await db.execute(select(User).filter(User.id == user_id))
    user = q.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def require_roles(*roles):
    async def role_dep(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles and "SuperAdmin" not in roles and current_user.role != "SuperAdmin":
            # allow SuperAdmin to do everything
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_dep

def require_tenant(event_college_id: int, current_user: User):
    """
    Helper for endpoint implementations: ensure the current_user belongs to same college OR SuperAdmin
    """
    if current_user.role == "SuperAdmin":
        return True
    if current_user.college_id != event_college_id:
        raise HTTPException(status_code=403, detail="Cross-tenant access denied")
    return True
