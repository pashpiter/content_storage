from fastapi import APIRouter

from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.content import router as content_router
from api.v1.endpoints.user import router as user_router


router = APIRouter(prefix='/v1')
router.include_router(auth_router, tags=['Аутентфикация'])
router.include_router(user_router, tags=['Пользователи (только для админов)'])
router.include_router(content_router, tags=['Контент'])
