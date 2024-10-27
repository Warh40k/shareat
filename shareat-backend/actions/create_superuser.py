import os
import sys
import asyncio
import contextlib
from os import getenv

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.database.db_helper import db_helper
from src.models import User
from src.repositories.implementations.user_repository import get_user_db
from src.schemas.user_schema import UserCreate
from src.services.auth.manager import get_user_manager, UserManager

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

default_username = "admin"
default_firstname = "admin"
default_secondname = "admin"
default_email = getenv("DEFAULT_EMAIL", "admin@admin.com")
default_password = getenv("DEFAULT_PASSWORD", "admin")
default_role_id = 0
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(
        user_manager: UserManager,
        user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
        username: str = default_username,
        firstname: str = default_firstname,
        secondname: str = default_secondname,
        email: str = default_email,
        password: str = default_password,
        role_id: int = default_role_id,
        is_active: bool = default_is_active,
        is_superuser: bool = default_is_superuser,
        is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        username=username,
        firstname=firstname,
        secondname=secondname,
        email=email,
        password=password,
        role_id=role_id,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    async with db_helper.session_factory() as session:
        async with get_user_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )


if __name__ == "__main__":
    asyncio.run(create_superuser())
