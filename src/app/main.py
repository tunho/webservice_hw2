from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.exceptions import (
    BookstoreException,
    bookstore_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
)

from app.core.middleware import StructuredLoggingMiddleware, RateLimitMiddleware

from app.schemas.common import ErrorResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2025-03-05T12:34:56Z",
                        "path": "/api/v1/users/",
                        "status": 400,
                        "code": "BAD_REQUEST",
                        "message": "Invalid input data",
                        "details": {"field": "value is invalid"}
                    }
                }
            }
        },
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2025-03-05T12:34:56Z",
                        "path": "/api/v1/users/me",
                        "status": 401,
                        "code": "UNAUTHORIZED",
                        "message": "Could not validate credentials",
                        "details": None
                    }
                }
            }
        },
        403: {
            "model": ErrorResponse,
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2025-03-05T12:34:56Z",
                        "path": "/api/v1/admin/users",
                        "status": 403,
                        "code": "FORBIDDEN",
                        "message": "Not enough privileges",
                        "details": None
                    }
                }
            }
        },
        404: {
            "model": ErrorResponse,
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2025-03-05T12:34:56Z",
                        "path": "/api/v1/books/999",
                        "status": 404,
                        "code": "RESOURCE_NOT_FOUND",
                        "message": "Book not found",
                        "details": None
                    }
                }
            }
        },
        422: {
            "model": ErrorResponse,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2025-03-05T12:34:56Z",
                        "path": "/api/v1/books/",
                        "status": 422,
                        "code": "VALIDATION_FAILED",
                        "message": "Input validation failed",
                        "details": {"price": "ensure this value is greater than 0"}
                    }
                }
            }
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2025-03-05T12:34:56Z",
                        "path": "/api/v1/orders/",
                        "status": 500,
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "An unexpected error occurred",
                        "details": None
                    }
                }
            }
        },
    }
)

# Add Middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(StructuredLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)

app.add_exception_handler(BookstoreException, bookstore_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
def root():
    return {"message": "Welcome to the Practical API Server"}
