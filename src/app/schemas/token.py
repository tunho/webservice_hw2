from typing import Optional
from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjU0MzY5NTQsInN1YiI6IjEifQ.pt-I4sNWYYDDUmmjNBiPF75Qn9N8-qL2C4_XqTK3rR4",
                "token_type": "bearer"
            }
        }
    )

class TokenPayload(BaseModel):
    sub: Optional[str] = None
