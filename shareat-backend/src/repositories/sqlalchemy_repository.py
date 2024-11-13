from typing import Type, TypeVar, Optional, Generic
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base_model import Base
from .base_repository import AbstractRepository

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class SqlAlchemyRepository(AbstractRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.session = db_session
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, data: UpdateSchemaType, **filters) -> ModelType:
        data = {key: value for key, value in data.items() if value is not None}
        stmt = update(self.model).values(**data).filter_by(**filters).returning(self.model)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def delete(self, **filters) -> None:
        await self.session.execute(delete(self.model).filter_by(**filters))
        await self.session.commit()

    async def get_single(self, **filters) -> Optional[ModelType] | None:
        row = await self.session.execute(select(self.model).filter_by(**filters))
        return row.scalar_one_or_none()

    async def get_multi(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0
    ) -> list[ModelType]:
        stmt = select(self.model).order_by(*order).limit(limit).offset(offset)
        row = await self.session.execute(stmt)
        return row.scalars().all()
