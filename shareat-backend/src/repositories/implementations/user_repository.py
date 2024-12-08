from typing import Dict, Any, Type

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.config.database.db_helper import db_helper
from src.models import User, Base, Client
from fastapi_users.db import SQLAlchemyUserDatabase


class UserRepository(SQLAlchemyUserDatabase):
    def __init__(self, db_session: AsyncSession, model: User):
        super().__init__(db_session, model)

    async def create_user_with_role(self, user_data: Dict[str, Any], role_data: Dict[str, Any],
                                    role_model: Type[Base]) -> User:
        # Создаем пользователя без вызова create
        user = self.user_table(**user_data)
        self.session.add(user)

        # Выполняем flush, чтобы сгенерировать user.id
        await self.session.flush()

        # Добавляем ID пользователя в данные роли
        role_data["id"] = user.id
        role_instance = role_model(**role_data)
        self.session.add(role_instance)

        # Выполняем commit для сохранения обеих записей
        await self.session.commit()

        # Обновляем объект user для возвращения
        await self.session.refresh(user)
        return user

    async def update_client_fields(self, client_id: int, update_fields: dict):
        """
        Универсальный метод обновления любых полей клиента.

        :param client_id: ID клиента
        :param update_fields: Словарь с полями и значениями для обновления
        """
        if not update_fields:
            raise ValueError("Update fields must not be empty")

        statement = (
            update(Client)
            .where(Client.id == client_id)
            .values(**update_fields)
        )
        await self.session.execute(statement)
        await self.session.commit()



async def get_user_db(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    yield UserRepository(db_session=db_session, model=User)
