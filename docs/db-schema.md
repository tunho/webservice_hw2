# Database Schema

## Overview
The database is designed using a relational model (SQLAlchemy ORM) supporting both SQLite (Dev) and MySQL (Prod).

## ER Diagram (Conceptual)
`User` (1) -- (*) `Order`
`User` (1) -- (*) `Review`
`User` (1) -- (1) `Cart`
`Seller` (1) -- (*) `Book`
`Book` (1) -- (*) `Review`
`Order` (1) -- (*) `OrderItem`
`Cart` (1) -- (*) `CartItem`

## Key Tables

### Users (`users`)
- `user_id` (PK): Unique identifier
- `email` (Unique): Login credential
- `role`: USER, SELLER, ADMIN
- `status`: ACTIVE, BANNED, DELETED

### Books (`books`)
- `book_id` (PK)
- `seller_id` (FK): Link to Seller
- `title`, `price`, `stock`
- `status`: AVAILABLE, SOLD_OUT, DELETED

### Orders (`orders`)
- `order_id` (PK)
- `user_id` (FK): Buyer
- `total_price`, `status` (CREATED, PAID, SHIPPED, COMPLETED)

### OrderItems (`order_items`)
- `order_item_id` (PK)
- `order_id` (FK)
- `book_id` (FK)
- `quantity`, `unit_price`

### Settlements (`settlements`)
- `settlement_id` (PK)
- `seller_id` (FK)
- `total_sales`, `commission`, `final_payout`
- `period_start`, `period_end`

*(See `src/app/models/` for full schema definitions)*
