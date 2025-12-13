from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, books, orders, carts, reviews, favorites

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(carts.router, prefix="/carts", tags=["carts"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
