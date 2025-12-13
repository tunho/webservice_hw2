from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole, UserStatus
from app.schemas.token import TokenPayload

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security_scheme = HTTPBearer()

def get_current_user(
    db: Session = Depends(get_db),
    token_creds: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> User:
    token = token_creds.credentials
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.user_id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Debug
    print(f"DEBUG: user.status={user.status} type={type(user.status)}")
    print(f"DEBUG: UserStatus.ACTIVE={UserStatus.ACTIVE} type={type(UserStatus.ACTIVE)}")
    print(f"DEBUG: Comparison={user.status != UserStatus.ACTIVE}")
    
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
