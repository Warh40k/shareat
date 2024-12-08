from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.controllers.fastapi_users import fastapi_users, current_active_user, current_active_clientuser
from src.models import User
from src.schemas.user_schema import UserRead, UserUpdate, ResetPasswordRequest, UserDetails
from src.services.auth.manager import get_user_manager, UserManager

# Создаем основной роутер для пользователей
router = APIRouter(prefix="/personal", tags=["user"])


@router.get("/getUserData", response_model=UserDetails, name="users:details_user",
            response_model_exclude_none=True,
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Missing token or inactive user.",
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": "User not found.",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "Validation error.",
                },
            })
async def get_user_data(user: User = Depends(current_active_user),
                        user_manager: UserManager = Depends(get_user_manager)):
    try:
        user_details = await user_manager.get_user_details(user)
        return user_details
    except HTTPException as e:
        raise e


@router.post("/resetPassword", status_code=status.HTTP_200_OK, name="users:reset_password",
             responses={
                 status.HTTP_200_OK: {"description": "Password updated successfully."},
                 status.HTTP_400_BAD_REQUEST: {"description": "Invalid password or update failed."},
                 status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."},
             })
async def reset_password(
        reset_request: ResetPasswordRequest,
        user: User = Depends(current_active_user),
        user_manager: UserManager = Depends(get_user_manager)
):
    try:
        await user_manager.update_password(
            user=user,
            old_password=reset_request.old_password,
            new_password=reset_request.new_password
        )
        return {"detail": "Password updated successfully"}
    except HTTPException as e:
        raise e


class BalanceUpdateRequest(BaseModel):
    amount: int


@router.post("/updateBalance", status_code=status.HTTP_200_OK, name="users:update_balance")
async def update_balance(
    balance_update: BalanceUpdateRequest,
    user: User = Depends(current_active_clientuser),
    user_manager: UserManager = Depends(get_user_manager)
):
    try:
        new_balance = await user_manager.update_balance(user=user, amount=balance_update.amount)
        return {"detail": "Balance updated successfully.", "new_balance": new_balance}
    except HTTPException as e:
        raise e


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)
