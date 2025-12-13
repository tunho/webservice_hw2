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
    swagger_ui_parameters={"persistAuthorization": True},
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "examples": {
                        "BAD_REQUEST": {
                            "summary": "Bad Request",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/users/",
                                "status": 400,
                                "code": "BAD_REQUEST",
                                "message": "Invalid input data",
                                "details": {"field": "value is invalid"}
                            }
                        },
                        "VALIDATION_FAILED": {
                            "summary": "Validation Failed",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/users/",
                                "status": 400,
                                "code": "VALIDATION_FAILED",
                                "message": "Input validation failed",
                                "details": {"email": "invalid email format"}
                            }
                        },
                        "INVALID_QUERY_PARAM": {
                            "summary": "Invalid Query Param",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/books?sort=invalid",
                                "status": 400,
                                "code": "INVALID_QUERY_PARAM",
                                "message": "Invalid query parameter",
                                "details": {"sort": "must be one of [price, created_at]"}
                            }
                        }
                    }
                }
            }
        },
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "UNAUTHORIZED": {
                            "summary": "Unauthorized",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/users/me",
                                "status": 401,
                                "code": "UNAUTHORIZED",
                                "message": "Could not validate credentials",
                                "details": None
                            }
                        },
                        "TOKEN_EXPIRED": {
                            "summary": "Token Expired",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/users/me",
                                "status": 401,
                                "code": "TOKEN_EXPIRED",
                                "message": "Token has expired",
                                "details": None
                            }
                        }
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
                    "examples": {
                        "RESOURCE_NOT_FOUND": {
                            "summary": "Resource Not Found",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/books/999",
                                "status": 404,
                                "code": "RESOURCE_NOT_FOUND",
                                "message": "Book not found",
                                "details": None
                            }
                        },
                        "USER_NOT_FOUND": {
                            "summary": "User Not Found",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/users/999",
                                "status": 404,
                                "code": "USER_NOT_FOUND",
                                "message": "User not found",
                                "details": None
                            }
                        }
                    }
                }
            }
        },
        409: {
            "model": ErrorResponse,
            "description": "Conflict",
            "content": {
                "application/json": {
                    "examples": {
                        "DUPLICATE_RESOURCE": {
                            "summary": "Duplicate Resource",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/users/",
                                "status": 409,
                                "code": "DUPLICATE_RESOURCE",
                                "message": "User with this email already exists",
                                "details": None
                            }
                        },
                        "STATE_CONFLICT": {
                            "summary": "State Conflict",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/orders/1/cancel",
                                "status": 409,
                                "code": "STATE_CONFLICT",
                                "message": "Cannot cancel completed order",
                                "details": None
                            }
                        }
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
                        "code": "UNPROCESSABLE_ENTITY",
                        "message": "Input validation failed",
                        "details": {"price": "ensure this value is greater than 0"}
                    }
                }
            }
        },
        429: {
            "model": ErrorResponse,
            "description": "Too Many Requests",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2025-03-05T12:34:56Z",
                        "path": "/api/v1/books/",
                        "status": 429,
                        "code": "TOO_MANY_REQUESTS",
                        "message": "Rate limit exceeded",
                        "details": None
                    }
                }
            }
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "examples": {
                        "INTERNAL_SERVER_ERROR": {
                            "summary": "Internal Server Error",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/orders/",
                                "status": 500,
                                "code": "INTERNAL_SERVER_ERROR",
                                "message": "An unexpected error occurred",
                                "details": None
                            }
                        },
                        "DATABASE_ERROR": {
                            "summary": "Database Error",
                            "value": {
                                "timestamp": "2025-03-05T12:34:56Z",
                                "path": "/api/v1/orders/",
                                "status": 500,
                                "code": "DATABASE_ERROR",
                                "message": "Database connection failed",
                                "details": None
                            }
                        }
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
app.add_middleware(RateLimitMiddleware, max_requests=1000, window_seconds=60)

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
