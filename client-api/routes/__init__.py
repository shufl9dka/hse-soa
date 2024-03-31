from fastapi import APIRouter

from .user import router as user_routes

router = APIRouter(prefix="/api")

router.include_router(user_routes)
