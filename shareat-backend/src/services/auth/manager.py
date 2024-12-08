from typing import Optional

from fastapi import Depends, Request, HTTPException, status
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, schemas, models


from src.models import User, Employee, Client, Admin
from src.repositories.implementations.user_repository import UserRepository, get_user_db
from src.schemas.user_schema import UserDetails, ClientRead, AdminRead, EmployeeRead

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgotten their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        if not safe and "role_id" not in user_dict:
            created_user = await self.user_db.create(user_dict)
            await self.on_after_register(created_user, request)
            return created_user
        elif safe:
            user_dict["role_id"] = 1

        # created_user = await self.user_db.create(user_dict)

        role_data = {}
        if user_dict.get("role_id") == 1:  # Client
            role_data = {
                "address": getattr(user_create, "address", None),
                "phone_number": getattr(user_create, "phone_number", None),
                "hobbies": getattr(user_create, "hobbies", None),
                "money": getattr(user_create, "money", 0),
            }
        elif user_dict.get("role_id") == 0:  # Admin
            role_data = {
                "department": getattr(user_create, "department", None),
            }
        elif user_dict.get("role_id") == 2:  # Employee
            role_data = {
                "department": getattr(user_create, "department", None),
                "position": getattr(user_create, "position", None),
            }
            
        created_user = await self.user_db.create_user_with_role(user_dict, role_data, Admin if user_dict.get(
            "role_id") == 0 else Employee if user_dict.get("role_id") == 2 else Client)

        await self.on_after_register(created_user, request)

        return created_user

    async def update_password(self, user: User, old_password: str, new_password: str) -> bool:
        # Проверка старого пароля
        is_correct, updated_hash = self.password_helper.verify_and_update(old_password, user.hashed_password)

        if not is_correct:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect.")

        # Обновляем хэш, если verify_and_update вернул новый хэш
        if updated_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_hash})

        # Проверка нового пароля на соответствие требованиям
        await self.validate_password(new_password, user)

        # Хэшируем новый пароль и обновляем в базе данных
        hashed_new_password = self.password_helper.hash(new_password)
        await self.user_db.update(user, {"hashed_password": hashed_new_password})
        return True

    async def get_user_details(self, user: User) -> UserDetails:
        try:
            # Создаем словарь для хранения данных пользователя
            user_data = UserDetails.model_validate(user)

            # Обновляем данные пользователя с информацией из связанных моделей
            if user.role_id == 1:
                client_data = user.client
                if client_data is not None:
                    client_details = ClientRead.model_validate(client_data)
                    user_data = user_data.model_copy(update=client_details.model_dump())
            elif user.role_id == 0:
                admin_data = user.admin
                if admin_data is not None:
                    admin_details = AdminRead.model_validate(admin_data)
                    user_data = user_data.model_copy(update=admin_details.model_dump())
            elif user.role_id == 2:
                employee_data = user.employee
                if employee_data is not None:
                    employee_details = EmployeeRead.model_validate(employee_data)
                    user_data = user_data.model_copy(update=employee_details.model_dump())

            return user_data
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

    async def update_balance(self, user: User, amount: int) -> int:
        # Проверяем, что сумма больше нуля
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The amount must be greater than zero.",
            )

        # Проверяем, является ли пользователь клиентом
        if user.role_id != 1 or not user.client:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only clients can update their balance.",
            )

        # Рассчитываем новый баланс
        new_balance = user.client.money + amount

        # Вызываем репозиторий для обновления баланса
        await self.user_db.update_client_fields(user.client.id, {"money": new_balance})

        # Возвращаем новый баланс
        return new_balance

    async def deduct_balance(self, user_id: int, amount: int):
        """Проверяет баланс пользователя и списывает указанную сумму."""
        # Получение пользователя
        user = await self.user_db.get(user_id)
        if not user or user.role_id != 1 or not user.client:
            raise HTTPException(
                status_code=403, detail="Only clients can perform this operation."
            )

        # Проверка, хватает ли средств
        if user.client.money < amount:
            raise HTTPException(
                status_code=400, detail="Insufficient funds."
            )

        # Списание средств
        new_balance = user.client.money - amount
        await self.user_db.update_client_fields(user.client.id, {"money": new_balance})


async def get_user_manager(user_db: UserRepository = Depends(get_user_db)):
    yield UserManager(user_db)
