from fastapi import APIRouter

from .posts import router as posts_routes
from .user import router as user_routes

router = APIRouter(prefix="/api")

router.include_router(posts_routes)
router.include_router(user_routes)
