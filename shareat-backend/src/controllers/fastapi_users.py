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