from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import load_only

from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.models import Order as OrderModel
from src.config.database.db_helper import db_helper
from src.schemas.order_schema import OrderCreate, OrderUpdate


class OrderRepository(SqlAlchemyRepository[ModelType, OrderCreate, OrderUpdate]):
    async def filter(
        self,
        fields: list[str] | None = None,
        order: list[str] | None = None,
        limit: int = None,
        offset: int = 0,
    ) -> list[ModelType] | None:
        stmt = select(self.model)
        if fields:
            model_fields = [getattr(self.model, field) for field in fields]
            stmt = stmt.options(load_only(*model_fields))
        if order:
            stmt = stmt.order_by(*order)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        row = await self.session.execute(stmt)
        return row.scalars().all()

    async def all(self) -> list[ModelType] | None:
        return await self.filter()

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar() is not None


async def get_order_db(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    yield OrderRepository(db_session=db_session, model=OrderModel)
