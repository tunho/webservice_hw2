from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from app.models.user import UserRole, UserStatus, Gender

class UserBase(BaseModel):
    email: EmailStr
    name: str
    nickname: Optional[str] = None # Not in schema but useful? Schema has name.
    phone_number: str
    gender: Gender
    birth_date: datetime
    address: Optional[str] = None
    profile_image: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=4)
    role: UserRole = UserRole.USER

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "demo_user@example.com",
                "name": "Demo User",
                "password": "password123",
                "phone_number": "010-1111-2222",
                "gender": "FEMALE",
                "birth_date": "1995-05-05T00:00:00",
                "address": "Busan, Korea",
                "role": "USER"
            }
        }
    )

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    profile_image: Optional[str] = None
    status: Optional[UserStatus] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Name",
                "phone_number": "010-9876-5432",
                "address": "Busan, Korea"
            }
        }
    )

class UserResponse(UserBase):
    user_id: int
    role: UserRole
    status: UserStatus
    region: Optional[str]
    last_login: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "admin@example.com",
                "name": "Super Admin",
                "nickname": "Admin",
                "phone_number": "010-0000-0000",
                "gender": "MALE",
                "birth_date": "1990-01-01T00:00:00",
                "address": "Seoul, Gangnam-gu",
                "profile_image": "https://example.com/admin_profile.jpg",
                "user_id": 1,
                "role": "ADMIN",
                "status": "ACTIVE",
                "region": "KR",
                "last_login": "2025-12-11T09:00:00",
                "created_at": "2025-01-01T00:00:00"
            }
        }
    )
