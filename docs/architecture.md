# 시스템 아키텍처 (System Architecture)

## 1. 개요 (Overview)
Bookstore API는 **FastAPI**를 기반으로 한 **계층형 아키텍처(Layered Architecture)**를 따릅니다.
각 계층은 관심사의 분리(Separation of Concerns) 원칙에 따라 독립적으로 구성되어 있으며, 유지보수성과 확장성을 보장합니다.

## 2. 계층 구조 (Layered Architecture)

요청(Request)은 상위 계층에서 하위 계층으로 흐르며, 데이터(Response)는 역순으로 반환됩니다.

```mermaid
graph TD
    Client[Client (Web/Mobile)] --> API[Presentation Layer (API)]
    API --> Service[Business Logic Layer (Service/Core)]
    Service --> Data[Data Access Layer (Repository/Models)]
    Data --> DB[(Database)]
```

### 2.1. 프레젠테이션 계층 (Presentation Layer)
- **위치**: `src/app/api/api_v1/endpoints/`
- **역할**: 클라이언트의 HTTP 요청을 수신하고, 입력 데이터(Pydantic Schema)를 검증하며, 비즈니스 로직을 호출한 뒤 응답을 반환합니다.
- **주요 모듈**:
    - `auth.py`: 로그인 및 토큰 발급
    - `users.py`, `books.py`, `orders.py` 등: 도메인별 라우터

### 2.2. 비즈니스 로직 계층 (Business Logic Layer)
- **위치**: `src/app/core/`, `src/app/services/` (일부 로직은 엔드포인트에 포함)
- **역할**: 애플리케이션의 핵심 규칙을 처리합니다. (예: 비밀번호 해싱, 권한 검사, 주문 총액 계산)
- **주요 모듈**:
    - `security.py`: JWT 토큰 생성 및 검증, 비밀번호 암호화
    - `config.py`: 환경 변수 및 설정 관리
    - `deps.py`: 의존성 주입 (DB 세션, 현재 사용자 주입)

### 2.3. 데이터 접근 계층 (Data Access Layer)
- **위치**: `src/app/models/`, `src/app/db/`
- **역할**: 데이터베이스와 직접 상호작용하여 데이터를 조회(SELECT), 저장(INSERT), 수정(UPDATE), 삭제(DELETE)합니다.
- **주요 모듈**:
    - `models/`: SQLAlchemy ORM 모델 정의 (`user.py`, `book.py` 등)
    - `db/session.py`: 데이터베이스 세션 관리
    - `db/base.py`: 모델 메타데이터 관리

## 3. 모듈 구조 및 의존성 (Module Structure & Dependencies)

프로젝트의 디렉토리 구조는 기능별로 명확하게 분리되어 있습니다.

```text
src/app/
├── api/                    # API 라우터 및 엔드포인트
│   └── api_v1/
│       └── endpoints/      # (users, books, orders, auth 등)
├── core/                   # 핵심 설정 및 유틸리티
│   ├── config.py           # 환경 설정 (Env)
│   ├── security.py         # 보안 (JWT, Hash)
│   └── deps.py             # 의존성 (DB Session, User)
├── db/                     # 데이터베이스 설정
│   ├── session.py          # DB 연결 세션
│   └── base.py             # ORM Base 클래스
├── models/                 # 데이터베이스 모델 (ORM)
│   ├── user.py
│   ├── book.py
│   └── ...
├── schemas/                # 데이터 검증 스키마 (Pydantic)
│   ├── user.py
│   ├── book.py
│   └── ...
└── main.py                 # 애플리케이션 진입점 (Entry Point)
```

### 의존성 흐름 (Dependency Flow)
1.  **`main.py`**는 `api/` 라우터를 포함합니다.
2.  **`api/`** 엔드포인트는 `schemas/`를 사용하여 입력을 검증하고, `core/deps.py`를 통해 DB 세션을 주입받습니다.
3.  **`api/`**는 `models/`를 사용하여 DB 데이터를 조작하거나 조회합니다.
4.  **`models/`**는 `db/base_class.py`를 상속받아 DB 테이블과 매핑됩니다.

## 4. 기술 스택 (Tech Stack)
- **Framework**: FastAPI (Python 3.10+)
- **ORM**: SQLAlchemy (비동기 지원 준비)
- **Validation**: Pydantic v2
- **Auth**: JWT (python-jose), Passlib (bcrypt)
- **Database**: SQLite (Dev), MySQL (Prod)
- **Server**: Uvicorn (ASGI)
- **Container**: Docker, Docker Compose


