from fastapi import APIRouter

from .user.routes import router as user_router
from .auth.routes import router as auth_router
from .good.routes import router as good_router
from .order.routes import router as order_router


router = APIRouter(prefix="/v1")

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(good_router)
router.include_router(order_router)
