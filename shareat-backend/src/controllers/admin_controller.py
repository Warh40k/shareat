from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users import exceptions as fastapi_users_exceptions

from src.controllers.fastapi_users import fastapi_users, current_active_superuser
from src.models import User
from src.schemas.user_schema import UserCreate, UserRead, UserUpdate
from src.services.auth.manager import get_user_manager, UserManager

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/createUser",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_active_superuser)],  # Доступ только для суперпользователей
)
async def create_user_endpoint(
    user_create: UserCreate,
    user_manager: UserManager = Depends(get_user_manager),
):
    """
    Создание пользователя через панель администратора.
    """
    try:
        # Создаем пользователя с помощью UserManager
        user = await user_manager.create(user_create=user_create, safe=False)
        return user
    except fastapi_users_exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}",
        )
