# API 설계 및 변경 사항 (API Design & Changes)

## 1. 개요 (Overview)
본 프로젝트는 **과제 1(웹 서비스 설계)**에서 도출된 API 명세를 기반으로 구현되었으며, **핵심 커머스 기능에 집중**하기 위해 일부 기능을 수정하거나 제외하였습니다.
이 문서는 과제 1의 초기 설계 대비 **실제 구현된 API의 변경 사항과 그 이유**를 요약합니다.

## 2. 과제 1 대비 주요 변경 사항 (Modifications from HW1)

### 2.1. 역할 및 권한 모델 간소화 (Role Simplification)
- **변경 전**: `User`, `Seller`, `Admin` 3계층 구조. 판매자가 도서를 등록하고 정산받는 구조.
- **변경 후**: **`User`, `Admin` 2계층 구조**로 변경.
    - **이유**: 단일 벤더 쇼핑몰 모델로 전환하여 복잡한 정산(Settlement) 로직을 제거하고, 관리자(Admin)가 상품을 직접 관리하도록 단순화했습니다.
    - **영향**: `Seller` 관련 API 및 `Settlement` API 전체 제거.

### 2.2. 기능 통합 및 제외 (Feature Consolidation)
| 기능 (Feature) | 상태 (Status) | 설명 (Description) |
| :--- | :--- | :--- |
| **회원 (User)** | ✅ 구현됨 | 회원가입, 로그인(JWT), 정보 수정, 탈퇴(Soft Delete) 구현 완료. |
| **도서 (Book)** | ✅ 구현됨 | 관리자만 등록/수정/삭제 가능. 재고(Stock) 관리 포함. |
| **주문 (Order)** | ✅ 구현됨 | 주문 생성, 조회, 취소 구현. 상태(`CREATED`~`COMPLETED`) 관리. |
| **장바구니 (Cart)** | ✅ 구현됨 | 도서 담기, 수량 변경, 삭제 구현. |
| **리뷰 (Review)** | ✅ 구현됨 | 도서별 리뷰 작성, 조회, 삭제 구현. (평점 포함) |
| **즐겨찾기 (Favorite)** | ✅ 구현됨 | 찜하기(Toggle) 기능 구현. |
| **댓글 (Comment)** | ❌ 제외됨 | 리뷰에 대한 대댓글 기능은 복잡도 감소를 위해 제외. |
| **라이브러리 (Library)** | ❌ 제외됨 | '주문 내역(Order History)'으로 대체 가능하여 중복 기능 제거. |
| **쿠폰/할인 (Coupon)** | ❌ 제외됨 | 핵심 결제 로직에 집중하기 위해 부가 기능 제외. |
| **통계/랭킹 (Stats)** | ❌ 제외됨 | 실시간 랭킹 및 통계 API 제외. |

### 2.3. 기술적 개선 사항 (Technical Improvements)
- **JWT Refresh Token**: 보안 강화를 위해 Access/Refresh Token 이중화 및 갱신 로직 추가.
- **Soft Delete**: 데이터 보존을 위해 `User`, `Book`, `Order` 삭제 시 DB에서 즉시 지우지 않고 `deleted_at` 타임스탬프 처리.
- **Path Parameter 예시**: Swagger UI 사용성 개선을 위해 모든 Path Variable에 기본값(`example=1`) 적용.

## 3. 최종 구현된 API 구조 (Implemented API Structure)

### 인증 (Auth)
- `POST /api/v1/auth/login`: 로그인 (Access/Refresh Token 발급)
- `POST /api/v1/auth/refresh`: 토큰 갱신

### 사용자 (Users)
- `POST /api/v1/users`: 회원가입
- `GET /api/v1/users/me`: 내 정보 조회
- `PATCH /api/v1/users/me`: 내 정보 수정
- `DELETE /api/v1/users/me`: 회원 탈퇴 (Soft Delete)

### 도서 (Books)
- `GET /api/v1/books`: 도서 목록 조회 (검색/필터)
- `GET /api/v1/books/{book_id}`: 도서 상세 조회
- `POST /api/v1/books`: 도서 등록 (Admin)
- `PATCH /api/v1/books/{book_id}`: 도서 수정 (Admin)
- `DELETE /api/v1/books/{book_id}`: 도서 삭제 (Admin)

### 주문 (Orders)
- `POST /api/v1/orders`: 주문 생성
- `GET /api/v1/orders`: 내 주문 목록 조회
- `GET /api/v1/orders/{order_id}`: 주문 상세 조회
- `POST /api/v1/orders/{order_id}/cancel`: 주문 취소

### 장바구니 (Carts)
- `GET /api/v1/carts`: 장바구니 조회
- `POST /api/v1/carts/items`: 장바구니 담기
- `PATCH /api/v1/carts/items/{item_id}`: 수량 변경
- `DELETE /api/v1/carts/items/{item_id}`: 항목 삭제
- `DELETE /api/v1/carts`: 장바구니 비우기

### 리뷰 (Reviews)
- `GET /api/v1/reviews/{book_id}`: 도서별 리뷰 조회
- `POST /api/v1/reviews`: 리뷰 작성
- `DELETE /api/v1/reviews/{review_id}`: 리뷰 삭제

### 즐겨찾기 (Favorites)
- `GET /api/v1/favorites`: 내 즐겨찾기 목록
- `POST /api/v1/favorites/{book_id}`: 즐겨찾기 추가/취소 (Toggle)


