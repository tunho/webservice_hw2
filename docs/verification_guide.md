# 프로젝트 검증 가이드

이 가이드는 프로젝트가 과제의 10가지 필수 요구사항을 모두 충족하는지 확인하는 방법을 안내합니다.

## 1. 리소스 및 CRUD (요구사항 1-1)
- **요구사항**: 4개 이상의 핵심 리소스와 전체 CRUD 구현.
- **확인 방법**: `src/app/api/api_v1/endpoints/` 디렉토리 확인.
    - `users.py`: 사용자(User) CRUD
    - `books.py`: 책(Book) CRUD
    - `orders.py`: 주문(Order) CRUD
    - `reviews.py`: 리뷰(Review) CRUD
    - 추가 리소스: `coupons.py`, `discounts.py`, `favorites.py`, `settlements.py`

## 2. 엔드포인트 개수 (요구사항 1-2)
- **요구사항**: 30개 이상의 엔드포인트.
- **확인 방법**:
    - 현재 개수: **59개** (코드 스캔으로 확인됨).
    - Swagger UI 확인: `http://localhost:8000/docs` 에서 전체 목록 확인 가능.

## 3. 인증 및 인가 (요구사항 1-3)
- **요구사항**: JWT 인증, RBAC (사용자/관리자).
- **확인 방법**:
    - 로그인: `POST /api/v1/auth/login` (액세스 토큰 반환).
    - RBAC: `src/app/api/deps.py` 파일의 `get_current_active_superuser` 함수 확인.
    - 토큰 없이 `/api/v1/users/` 접근 시도 (401 에러 반환 확인).

## 4. 검증 및 에러 처리 (요구사항 1-4)
- **요구사항**: Pydantic 검증, 표준 에러 응답.
- **확인 방법**:
    - `src/app/schemas/` 에서 Pydantic 모델 확인.
    - 잘못된 데이터(예: 음수 가격)로 책 생성 시도 -> 422 에러 반환 확인.
    - `src/app/core/exceptions.py` 에서 전역 예외 처리기 확인.

## 5. 목록 조회 페이지네이션 (요구사항 1-5)
- **요구사항**: 응답에 `page`, `size`, `totalElements` 포함.
- **확인 방법**:
    - `GET /api/v1/books/?page=0&size=5` 호출.
    - 응답이 `PageResponse` 형식을 따르는지 확인:
      ```json
      {
        "content": [...],
        "page": 0,
        "size": 5,
        "totalElements": ...,
        "totalPages": ...
      }
      ```

## 6. 데이터베이스 (요구사항 1-6)
- **요구사항**: MySQL 사용, 외래키(FK)/인덱스, 시드 데이터(200건 이상).
- **확인 방법**:
    - 모델: `src/app/models/` 에서 `ForeignKey` 및 `relationship` 확인.
    - 시드 데이터: `PYTHONPATH=src python src/app/db/seed.py` 실행.
    - MySQL: `mysql_install_guide.md`를 따라 설정.

## 7. 보안 및 성능 (요구사항 1-7)
- **요구사항**: .env 사용, CORS, 레이트 리밋(Rate Limit).
- **확인 방법**:
    - `.env` 파일 확인 (비밀키 등이 하드코딩되지 않음).
    - `src/app/main.py` 에서 `CORSMiddleware` 및 `RateLimitMiddleware` 확인.
    - 헬스 체크: `GET /health` -> `{"status": "ok"}` 반환 확인.

## 8. 문서화 (요구사항 1-8)
- **요구사항**: Swagger, Postman.
- **확인 방법**:
    - Swagger: `http://localhost:8000/docs` 접속.
    - Postman: `postman_collection.json` 파일 열기 (59개 요청 + 로그인 테스트 스크립트 포함).

## 9. 로깅 (요구사항 1-9)
- **요구사항**: 요청/응답 로그 남기기.
- **확인 방법**:
    - 서버 실행 후 API 요청 보내기.
    - 터미널 출력에서 JSON 로그(타임스탬프, 경로, 상태 코드, 소요 시간) 확인.

## 10. 테스트 (요구사항 1-10)
- **요구사항**: 20개 이상의 자동화 테스트.
- **확인 방법**:
    - `PYTHONPATH=src venv/bin/pytest` 실행.
    - 결과: **21개 통과** (인증, 사용자, 책, 주문, 리뷰 등 커버).
