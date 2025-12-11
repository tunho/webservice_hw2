from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, books, orders, carts, reviews, sellers, coupons, stats, admin, discounts, favorites, settlements

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(carts.router, prefix="/carts", tags=["carts"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(sellers.router, prefix="/sellers", tags=["sellers"])
api_router.include_router(coupons.router, prefix="/coupons", tags=["coupons"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(discounts.router, prefix="/discounts", tags=["discounts"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
api_router.include_router(settlements.router, prefix="/settlements", tags=["settlements"])
