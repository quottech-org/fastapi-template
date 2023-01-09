from fastapi import APIRouter

from .v1.all_routes import router as v1_router

router = APIRouter(prefix="/api")


router.include_router(v1_router)