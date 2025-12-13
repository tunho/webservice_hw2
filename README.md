# Bookstore API Project

## 1. 프로젝트 개요
**문제 정의**: 온라인 서점의 핵심 비즈니스 로직(회원, 상품, 주문, 결제)을 RESTful API로 구현하여, 확장 가능하고 유지보수가 용이한 백엔드 시스템을 구축합니다.
**주요 기능**:
- **회원 관리**: 회원가입, 로그인(JWT), 프로필 관리, 회원 탈퇴(Soft/Hard Delete).
- **상품 관리**: 도서 등록/수정/삭제(관리자 전용), 카테고리별 조회, 검색, 재고 관리.
- **주문/결제**: 장바구니, 주문 생성, 결제 처리(Mock), 주문 상태 관리(배송/취소).
- **커뮤니티**: 도서 리뷰 및 평점, 즐겨찾기(찜).
- **관리자 기능**: 전체 주문/회원 관리, 도서 관리.

## 2. 실행 방법

### 로컬 실행 (Python/FastAPI)

**1. 의존성 설치**
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

**2. 데이터베이스 초기화 (마이그레이션 & 시드)**
```bash
# 초기 데이터 생성 (Admin, User, Book, Order 등)
PYTHONPATH=src python scripts/seed.py
```
*기본적으로 SQLite (`sql_app.db`)를 사용합니다.*

**3. 서버 실행**
```bash
PYTHONPATH=src python src/run.py
# 또는
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 3. 환경변수 설명
`.env.example` 파일을 참고하여 `.env` 파일을 생성해야 합니다.

| 변수명 | 설명 | 기본값/예시 |
|---|---|---|
| `SECRET_KEY` | JWT 서명용 비밀키 | (임의의 문자열) |
| `ALGORITHM` | 암호화 알고리즘 | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 토큰 만료 시간(분) | 30 |
| `SQLALCHEMY_DATABASE_URI` | DB 접속 주소 | sqlite:///./sql_app.db |
| `DB_HOST` | (MySQL 사용 시) 호스트 | localhost |
| `DB_PORT` | (MySQL 사용 시) 포트 | 3306 |
| `DB_USER` | (MySQL 사용 시) 사용자 | user |
| `DB_PASSWORD` | (MySQL 사용 시) 비밀번호 | password |
| `DB_NAME` | (MySQL 사용 시) DB명 | bookstore |

## 4. 배포 주소
- **Base URL**: `http://113.198.66.68:13072/api/v1`
- **Swagger UI**: `http://113.198.66.68:13072/docs`
- **Health Check**: `http://113.198.66.68:13072/health`

## 5. 인증 플로우 설명
본 프로젝트는 **JWT (JSON Web Token)** 방식을 사용합니다.
1.  **로그인**: `POST /auth/login`으로 이메일/비밀번호 전송.
2.  **토큰 발급**: 유효한 경우 `access_token` 발급.
3.  **API 요청**: `Authorization: Bearer <access_token>` 헤더를 포함하여 요청.
4.  **권한 확인**: 서버는 토큰을 검증하고 User Role(USER/ADMIN)에 따라 접근 제어.

## 6. 역할/권한표

| API 그룹 | ROLE_USER | ROLE_ADMIN |
|---|:---:|:---:|
| **도서 조회** | O | O |
| **도서 관리(등록/수정/삭제)** | X | O |
| **주문/결제** | O | O |
| **장바구니** | O | O |
| **리뷰 작성** | O | O |
| **회원 관리** | O (본인만) | O (전체 수정/삭제) |

## 7. 예제 계정

| 역할 | 이메일 | 비밀번호 | 비고 |
|---|---|---|---|
| **관리자** | `admin@example.com` | `admin123` | 모든 권한 보유 |
| **사용자** | `customer@example.com` | `customer123` | 일반 구매/리뷰 가능 |

## 8. DB 연결 정보 (테스트용)
*로컬 개발 시 SQLite(`sql_app.db`)가 자동 생성되어 사용됩니다.*
만약 MySQL Docker를 사용하는 경우:
- **Host**: `localhost`
- **Port**: `3306`
- **Database**: `bookstore`
- **User**: `user`
- **Password**: `password`

## 9. 엔드포인트 요약표 (Endpoint Summary)

| Tag | Method | Endpoint | 설명 (Description) | 권한 (Role) |
| :--- | :---: | :--- | :--- | :---: |
| **Auth** | `POST` | `/auth/login` | 로그인 및 토큰 발급 | All |
| **Auth** | `POST` | `/auth/refresh` | 액세스 토큰 갱신 | All |
| **Users** | `GET` | `/users/` | 회원 목록 조회 (페이지네이션) | Admin |
| **Users** | `POST` | `/users/` | 회원가입 | All |
| **Users** | `GET` | `/users/me` | 내 프로필 조회 | User |
| **Users** | `PATCH` | `/users/me` | 내 프로필 수정 | User |
| **Users** | `DELETE` | `/users/me` | 회원 탈퇴 (Soft Delete) | User |
| **Users** | `POST` | `/users/logout` | 로그아웃 | User |
| **Users** | `DELETE` | `/users/{id}/hard` | 회원 영구 삭제 | Admin |
| **Books** | `GET` | `/books/` | 도서 목록 조회 (검색/필터) | All |
| **Books** | `GET` | `/books/{id}` | 도서 상세 조회 | All |
| **Books** | `POST` | `/books/` | 도서 등록 | Admin |
| **Books** | `PATCH` | `/books/{id}` | 도서 수정 | Admin |
| **Books** | `DELETE` | `/books/{id}` | 도서 삭제 | Admin |
| **Orders** | `POST` | `/orders/` | 주문 생성 | User |
| **Orders** | `GET` | `/orders/` | 내 주문 내역 조회 (Admin: 전체) | User/Admin |
| **Orders** | `GET` | `/orders/{id}` | 주문 상세 조회 | User/Admin |
| **Orders** | `POST` | `/orders/{id}/cancel` | 주문 취소 | User |
| **Carts** | `GET` | `/carts/` | 장바구니 조회 | User |
| **Carts** | `POST` | `/carts/items` | 장바구니 담기 | User |
| **Carts** | `GET` | `/carts/items` | 장바구니 항목 목록 조회 | User |
| **Carts** | `PATCH` | `/carts/items` | 수량 변경 (PUT) | User |
| **Carts** | `DELETE` | `/carts/items/{id}` | 항목 삭제 | User |
| **Carts** | `DELETE` | `/carts/` | 장바구니 비우기 | User |
| **Reviews** | `GET` | `/reviews/{book_id}` | 도서별 리뷰 조회 | All |
| **Reviews** | `POST` | `/reviews/` | 리뷰 작성 | User |
| **Reviews** | `GET` | `/reviews/{id}/detail` | 리뷰 상세 조회 | All |
| **Reviews** | `PATCH` | `/reviews/{id}` | 리뷰 수정 | User |
| **Reviews** | `DELETE` | `/reviews/{id}` | 리뷰 삭제 | User/Admin |
| **Favorites** | `GET` | `/favorites/` | 내 즐겨찾기 목록 | User |
| **Favorites** | `POST` | `/favorites/{book_id}` | 즐겨찾기 추가/취소 (Toggle) | User |

*(자세한 명세는 Swagger UI 참조)*

## 10. 성능/보안 및 기술적 고려사항
- **Rate Limiting**: `SlowAPI`를 적용하여 분당 요청 횟수 제한 (DDoS 방지).
- **Password Hashing**: `bcrypt`를 사용하여 비밀번호를 안전하게 단방향 암호화 저장.
- **CORS 설정**: 프론트엔드 연동 및 테스트를 위해 `CORSMiddleware` 적용 (모든 도메인 허용).
- **Health Check**: `/health` 엔드포인트를 통해 서버 상태 및 버전 정보 제공 (인증 불필요).
- **SQL Injection 방지**: SQLAlchemy ORM을 사용하여 쿼리 파라미터 바인딩 처리.
- **N+1 문제 방지**: 연관 데이터 조회 시 Eager Loading(`joinedload`) 적절히 활용.
- **DB 마이그레이션**: `scripts/seed.py` 및 SQLAlchemy `Base.metadata.create_all`을 통해 스키마 자동 생성 및 시드 데이터(200건+) 초기화.
- **Soft Delete**: 주요 데이터(회원, 상품 등)는 `deleted_at`을 사용하여 논리적 삭제 처리.

## 11. 한계와 개선 계획
- **한계**:
    - 현재 결제는 실제 PG사 연동 없이 DB 상태 변경으로만 구현됨.
    - 대용량 트래픽 처리를 위한 캐싱(Redis)이 일부 미적용됨 (현재는 세션/토큰 위주).
- **개선 계획**:
    - **Redis 도입**: 랭킹 집계 및 세션 관리에 Redis 적용하여 성능 향상.
    - **비동기 처리**: 이메일 발송, 정산 집계 등 무거운 작업을 Celery로 분리.
    - **테스트 커버리지 확대**: 현재 핵심 로직 위주의 테스트를 엣지 케이스까지 확장.

