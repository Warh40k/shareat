from fastapi import APIRouter

from src.controllers.fastapi_users import fastapi_users
from src.schemas.user_schema import UserRead, UserCreate
from src.services.auth.auth_service import auth_backend


# Создаем основной роутер для пользователей
router = APIRouter(prefix="/auth", tags=["auth"])

# Добавляем стандартные маршруты FastAPI Users
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)
router.include_router(
    fastapi_users.get_reset_password_router(),
)
