# API Design & Changes

## Overview
This document outlines the API design principles and key modifications made during the development of the Bookstore API.

## Key Design Principles
1.  **RESTful Architecture**: Resources are manipulated via standard HTTP methods (GET, POST, PUT, PATCH, DELETE).
2.  **Stateless Authentication**: JWT (JSON Web Tokens) are used for all authenticated requests.
3.  **Standardized Responses**: All list endpoints return a `PageResponse` structure, and errors follow a consistent `ErrorResponse` format.
4.  **Soft Deletes**: Critical resources (Users, Books, Orders) use soft deletion (`deleted_at`) to preserve data integrity.

## Modifications from Initial Requirements
1.  **Settlement Logic**: Added a dedicated `Settlement` resource to handle seller payouts separately from Orders.
2.  **Admin Features**: Enhanced Admin capabilities to view any user's cart and create settlements for testing purposes.
3.  **Book Status**: Added `DELETED` status to `BookStatus` enum to support soft deletion workflows.
4.  **Dynamic Seller Assignment**: `create_book` now dynamically assigns the correct `seller_id` based on the logged-in user's role.

## API Structure
- `/api/v1/auth`: Authentication (Login, Refresh)
- `/api/v1/users`: User management
- `/api/v1/books`: Product catalog
- `/api/v1/orders`: Order processing
- `/api/v1/carts`: Shopping cart
- `/api/v1/reviews`: User reviews
- `/api/v1/settlements`: Seller payouts
- `/api/v1/admin`: Administrative statistics
