from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from sqlalchemy import select, update, delete
from sqlalchemy.orm import load_only

from src.models.photo import Photo
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType, UpdateSchemaType
from src.models import Product as ProductModel
from src.config.database.db_helper import db_helper
from src.schemas.product_schema import ProductCreate, ProductUpdate


class ProductRepository(SqlAlchemyRepository[ModelType, ProductCreate, ProductUpdate]):
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

    async def create_with_photos(self, data: dict, photo_paths: List[str]) -> ModelType:
        product = self.model(**data)
        self.session.add(product)
        await self.session.flush()

        for path in photo_paths:
            photo = Photo(product_id=product.id, path=path)
            self.session.add(photo)

        await self.session.flush()

        await self.session.commit()

        await self.session.refresh(product)

        return product

    async def update_with_photos(
            self, data: UpdateSchemaType, photos: List[str], **filters
    ) -> ModelType:
        data = {key: value for key, value in data.items() if value is not None}

        # 2. Обновление данных товара
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(**filters)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        product = res.scalar_one_or_none()

        if not product:
            raise ValueError(f"Product with id not found")

        # 3. Удаление старых фотографий
        await self.session.execute(
            delete(Photo).where(Photo.product_id == product.id)
        )

        # 4. Добавление новых фотографий (если есть)
        if photos:
            new_photos = [Photo(product_id=product.id, path=path) for path in photos]
            self.session.add_all(new_photos)

        # 5. Сохранение изменений
        await self.session.commit()

        # 6. Обновляем объект товара, включая связанные фотографии
        await self.session.refresh(product, ["photos"])

        return product


async def get_product_db(db_session: AsyncSession = Depends(db_helper.get_db_session)):
    yield ProductRepository(db_session=db_session, model=ProductModel)
