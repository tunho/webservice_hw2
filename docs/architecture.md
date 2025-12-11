# System Architecture

## Overview
The Bookstore API follows a layered architecture pattern using FastAPI.

## Layers

### 1. Presentation Layer (API)
- **Location**: `src/app/api/api_v1/endpoints/`
- **Responsibility**: Handles HTTP requests, validates input (Pydantic), and returns responses.
- **Components**: Routers (`users.py`, `books.py`, etc.)

### 2. Service/Business Logic Layer
- **Location**: Embedded within API endpoints and `src/app/core/`
- **Responsibility**: Implements business rules (e.g., calculating discounts, processing orders).
- **Components**: Dependency injection (`deps.py`), Security utilities (`security.py`).

### 3. Data Access Layer (Repository)
- **Location**: `src/app/crud/` (Implicit in endpoints via SQLAlchemy)
- **Responsibility**: Interacts with the database.
- **Components**: SQLAlchemy Models (`src/app/models/`), DB Session (`src/app/db/`).

### 4. Database
- **Type**: Relational (SQLite/MySQL)
- **Responsibility**: Persistent storage of application data.

## Tech Stack
- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Auth**: JWT (python-jose)
- **Server**: Uvicorn (ASGI)
- **Containerization**: Docker & Docker Compose
