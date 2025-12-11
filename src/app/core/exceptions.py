from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.schemas.common import ErrorResponse

class BookstoreException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

async def bookstore_exception_handler(request: Request, exc: BookstoreException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            timestamp=datetime.utcnow(),
            path=str(request.url.path),
            status=exc.status_code,
            code=exc.code,
            message=exc.message,
            details=exc.details,
        ).model_dump(mode="json"),
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    code = "UNKNOWN_ERROR"
    if exc.status_code == 400:
        code = "BAD_REQUEST"
    elif exc.status_code == 401:
        code = "UNAUTHORIZED"
    elif exc.status_code == 403:
        code = "FORBIDDEN"
    elif exc.status_code == 404:
        code = "RESOURCE_NOT_FOUND"
    elif exc.status_code == 409:
        code = "STATE_CONFLICT"
    elif exc.status_code == 422:
        code = "UNPROCESSABLE_ENTITY"
    elif exc.status_code == 429:
        code = "TOO_MANY_REQUESTS"
    elif exc.status_code == 500:
        code = "INTERNAL_SERVER_ERROR"

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            timestamp=datetime.utcnow(),
            path=str(request.url.path),
            status=exc.status_code,
            code=code,
            message=str(exc.detail),
        ).model_dump(mode="json"),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = {}
    for error in exc.errors():
        # Simplified field extraction
        # loc is a tuple like ('body', 'email')
        field = ".".join(str(x) for x in error["loc"])
        details[field] = error["msg"]

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, # Changed to 400 as per requirement example (though 422 is standard FastAPI)
        content=ErrorResponse(
            timestamp=datetime.utcnow(),
            path=str(request.url.path),
            status=status.HTTP_400_BAD_REQUEST,
            code="VALIDATION_FAILED",
            message="Input validation failed",
            details=details,
        ).model_dump(mode="json"),
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    # Log the error here in a real app
    # print(f"DB Error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            timestamp=datetime.utcnow(),
            path=str(request.url.path),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="DATABASE_ERROR",
            message="An unexpected database error occurred.",
        ).model_dump(mode="json"),
    )
