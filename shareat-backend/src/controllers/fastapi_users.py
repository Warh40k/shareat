from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers

from src.models import User
from src.services.auth.auth_service import auth_backend
from src.services.auth.manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)


async def get_user_by_role(
    required_role: int,  # Указание необходимой роли
    user: User = Depends(current_active_user),
) -> User:
    """Проверить, соответствует ли пользователь необходимой роли."""
    if user.role_id != required_role:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user


async def current_active_adminuser(
    user: User = Depends(current_active_user),
) -> User:
    """Пользователь с ролью 'Admin'."""
    return await get_user_by_role(required_role=0, user=user)


async def current_active_clientuser(
    user: User = Depends(current_active_user),
) -> User:
    """Пользователь с ролью 'Client'."""
    return await get_user_by_role(required_role=1, user=user)


async def current_active_manageruser(
    user: User = Depends(current_active_user),
) -> User:
    """Пользователь с ролью 'Manager'."""
    return await get_user_by_role(required_role=2, user=user)
