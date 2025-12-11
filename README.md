# Bookstore API Project

## 1. 프로젝트 개요
**문제 정의**: 온라인 서점의 핵심 비즈니스 로직(회원, 상품, 주문, 결제, 정산, 통계)을 RESTful API로 구현하여, 확장 가능하고 유지보수가 용이한 백엔드 시스템을 구축합니다.
**주요 기능**:
- **회원 관리**: 회원가입, 로그인(JWT), 프로필 관리, 회원 탈퇴(Soft/Hard Delete).
- **상품 관리**: 도서 등록/수정/삭제, 카테고리별 조회, 검색, 재고 관리.
- **주문/결제**: 장바구니, 주문 생성, 결제 처리(Mock), 주문 상태 관리(배송/취소/반품).
- **프로모션**: 쿠폰 발급/사용, 도서별 할인 정책 적용.
- **커뮤니티**: 도서 리뷰 및 평점, 댓글, 즐겨찾기(찜).
- **관리자 기능**: 정산 관리, 통계(랭킹, 이탈률 등) 조회, 전체 주문/회원 관리.

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
- **Base URL**: `http://<SERVER_IP>:8000/api/v1`
- **Swagger UI**: `http://<SERVER_IP>:8000/docs`
- **ReDoc**: `http://<SERVER_IP>:8000/redoc`
- **Health Check**: `http://<SERVER_IP>:8000/health`

## 5. 인증 플로우 설명
본 프로젝트는 **JWT (JSON Web Token)** 방식을 사용합니다.
1.  **로그인**: `POST /auth/login`으로 이메일/비밀번호 전송.
2.  **토큰 발급**: 유효한 경우 `access_token` 발급.
3.  **API 요청**: `Authorization: Bearer <access_token>` 헤더를 포함하여 요청.
4.  **권한 확인**: 서버는 토큰을 검증하고 User Role(USER/SELLER/ADMIN)에 따라 접근 제어.

## 6. 역할/권한표

| API 그룹 | ROLE_USER | ROLE_SELLER | ROLE_ADMIN |
|---|:---:|:---:|:---:|
| **도서 조회** | O | O | O |
| **도서 관리(등록/수정/삭제)** | X | O (본인 것만) | O (전체) |
| **주문/결제** | O | O | O |
| **장바구니** | O | O | O (타인 것 조회 가능) |
| **리뷰 작성** | O | O | O |
| **정산 요청** | X | O | O (테스트용) |
| **통계/랭킹 조회** | X | X | O |
| **회원 관리** | O (본인만) | O (본인만) | O (전체 수정/삭제) |

## 7. 예제 계정

| 역할 | 이메일 | 비밀번호 | 비고 |
|---|---|---|---|
| **관리자** | `admin@example.com` | `admin123` | 모든 권한 보유 |
| **판매자** | `seller@example.com` | `seller123` | 상품/정산 관리 가능 |
| **사용자** | `customer@example.com` | `customer123` | 일반 구매/리뷰 가능 |

## 8. DB 연결 정보 (테스트용)
*로컬 개발 시 SQLite(`sql_app.db`)가 자동 생성되어 사용됩니다.*
만약 MySQL Docker를 사용하는 경우:
- **Host**: `localhost`
- **Port**: `3306`
- **Database**: `bookstore`
- **User**: `user`
- **Password**: `password`

## 9. 엔드포인트 요약표

| Method | Endpoint | 설명 |
|---|---|---|
| `POST` | `/auth/login` | 로그인 및 토큰 발급 |
| `GET` | `/users/me` | 내 프로필 조회 |
| `GET` | `/books/` | 도서 목록 조회 (검색/필터) |
| `POST` | `/orders/` | 주문 생성 |
| `GET` | `/orders/` | 주문 내역 조회 (Admin: 전체) |
| `GET` | `/carts/` | 장바구니 조회 (Admin: 타인 조회 가능) |
| `POST` | `/settlements/` | 정산 요청 (Seller/Admin) |
| `GET` | `/admin/stats/...` | 관리자 통계 (랭킹, 이탈률 등) |

*(자세한 명세는 Swagger UI 참조)*

## 10. 성능/보안 고려사항
- **Rate Limiting**: `SlowAPI`를 적용하여 분당 요청 횟수 제한 (DDoS 방지).
- **Password Hashing**: `bcrypt`를 사용하여 비밀번호를 안전하게 단방향 암호화 저장.
- **SQL Injection 방지**: SQLAlchemy ORM을 사용하여 쿼리 파라미터 바인딩 처리.
- **N+1 문제 방지**: 연관 데이터 조회 시 Eager Loading(`joinedload`) 적절히 활용 (일부 복잡한 통계 제외).
- **Soft Delete**: 주요 데이터(회원, 상품 등)는 `deleted_at`을 사용하여 논리적 삭제 처리, 데이터 복구 가능성 확보.

## 11. 한계와 개선 계획
- **한계**:
    - 현재 결제는 실제 PG사 연동 없이 DB 상태 변경으로만 구현됨.
    - 대용량 트래픽 처리를 위한 캐싱(Redis)이 일부 미적용됨 (현재는 세션/토큰 위주).
- **개선 계획**:
    - **Redis 도입**: 랭킹 집계 및 세션 관리에 Redis 적용하여 성능 향상.
    - **비동기 처리**: 이메일 발송, 정산 집계 등 무거운 작업을 Celery로 분리.
    - **테스트 커버리지 확대**: 현재 핵심 로직 위주의 테스트를 엣지 케이스까지 확장.

