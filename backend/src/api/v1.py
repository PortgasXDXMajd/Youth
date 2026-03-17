from fastapi import APIRouter

from src.packages.auth.controller import router as auth_router
from src.packages.users.controller import router as users_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(users_router)
