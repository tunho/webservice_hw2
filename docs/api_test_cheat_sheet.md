# API Manual Testing Cheat Sheet

This guide provides the exact JSON bodies, headers, and parameters you need to test key endpoints manually in Postman.

## 1. Authentication (Login)
**Endpoint**: `POST /api/v1/auth/login`
**Headers**: `Content-Type: application/x-www-form-urlencoded`
**Body** (x-www-form-urlencoded):
- `username`: `admin@example.com` (or `seller@example.com`, `customer@example.com`)
- `password`: `admin123` (or `seller123`, `customer123`)

**Response**:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```
> **IMPORTANT**: Copy the `access_token` from the response. You will need it for almost all other requests.

---

## 2. Common Header for Protected Requests
For all requests below (except Public endpoints), add this header:
- **Key**: `Authorization`
- **Value**: `Bearer <YOUR_ACCESS_TOKEN>`

---

## 3. Users (Create & List)

### Create User (Public)
**Endpoint**: `POST /api/v1/users/`
**Body** (JSON):
```json
{
    "email": "newuser@example.com",
    "password": "password123",
    "name": "New User",
    "phone_number": "010-9999-8888",
    "gender": "MALE",
    "birth_date": "1995-01-01T00:00:00",
    "role": "USER"
}
```

### List Users (Admin Only)
**Endpoint**: `GET /api/v1/users/?page=0&size=10`
**Headers**: `Authorization: Bearer <ADMIN_TOKEN>`
**Params**:
- `page`: `0` (First page)
- `size`: `10` (Items per page)

---

## 4. Books (Create & List)

### Create Book (Seller Only)
**Endpoint**: `POST /api/v1/books/`
**Headers**: `Authorization: Bearer <SELLER_TOKEN>`
**Body** (JSON):
```json
{
    "title": "New Python Book",
    "authors": "[\"John Doe\"]",
    "categories": "[\"Programming\"]",
    "publisher": "Tech Books",
    "summary": "A great book about Python.",
    "isbn": "978-1234567890",
    "price": 30000,
    "stock": 50,
    "publication_date": "2023-12-01T00:00:00",
    "subcategory": "IT"
}
```

### List Books (Public)
**Endpoint**: `GET /api/v1/books/?page=0&size=5`

---

## 5. Orders (Create)

### Create Order (User Only)
**Endpoint**: `POST /api/v1/orders/`
**Headers**: `Authorization: Bearer <USER_TOKEN>`
**Body** (JSON):
```json
{
    "payment_method": "CARD",
    "receiver_name": "Receiver Name",
    "receiver_phone": "010-1234-5678",
    "shipping_address": "Seoul, Gangnam-gu",
    "items": [
        {
            "book_id": 1,
            "quantity": 1,
            "unit_price": 35000,
            "subtotal": 35000
        }
    ]
}
```

---

## 6. Settlements (Create)

### Request Settlement (Seller Only)
**Endpoint**: `POST /api/v1/settlements/`
**Headers**: `Authorization: Bearer <SELLER_TOKEN>`
**Body** (JSON):
```json
{
    "period_start": "2023-11-01T00:00:00",
    "period_end": "2023-11-30T23:59:59"
}
```
