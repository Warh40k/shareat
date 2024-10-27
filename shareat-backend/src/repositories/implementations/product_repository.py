from sqlalchemy import select, update
from sqlalchemy.orm import load_only
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.models.models import ProductModel
from src.config.database.db_helper import db_helper
from src.schemas.product_schema import Product


class ProductRepository(SqlAlchemyRepository[ModelType, Product]):
    
    async def create(self, data: Product) -> ProductModel:
        """Переопределённый метод create для работы с несовпадающими полями схемы и модели"""
        async with self._session_factory() as session:
            # Преобразуем данные ProductSchema в структуру модели базы данных
            model_data = {
                "title": data.name,
                "description": data.description,
                "price_per_day": data.price,
            }
            instance = self.model(**model_data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def update(self, data: Product, **filters) -> ProductModel:
        """Переопределённый метод update для работы с несовпадающими полями схемы и модели"""
        async with self._session_factory() as session:
            update_data = {
                "title": data.name,
                "description": data.description,
                "price_per_day": data.price,
            }
            stmt = update(self.model).values(**update_data).filter_by(**filters).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def filter(
        self,
        fields: list[str] | None = None,
        order: list[str] | None = None,
        limit: int = None,
        offset: int = 0,
    ) -> list[ModelType] | None:
        async with self._session_factory() as session:
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

            row = await session.execute(stmt)
            return row.scalars().all()

    async def all(self) -> list[ModelType] | None:
        return await self.filter()

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None


product_repository = ProductRepository(model=ProductModel, db_session=db_helper.get_db_session)
