import os
from typing import List
from uuid import uuid4

from fastapi import Depends, UploadFile, HTTPException
from fastapi.responses import FileResponse

from src.models import Product
from src.repositories.sqlalchemy_repository import ReadSchemaType
from src.schemas.base_schema import PyModel
from src.schemas.product_schema import ProductRead
from src.services.base_service import BaseService
from src.repositories.implementations.product_repository import ProductRepository, get_product_db

UPLOADS_DIR = "resources"


def convert_product_to_read(product: Product) -> ProductRead:
    return ProductRead(
        id=product.id,
        title=product.title,
        description=product.description,
        price_per_day=product.price_per_day,
        in_rent=product.in_rent,
        is_active=product.is_active,
        photos=[photo.path for photo in product.photos] if product.photos else []
    )


class ProductService(BaseService):
    
    async def filter(
            self,
            fields: list[str] | None = None,
            order: list[str] | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[ReadSchemaType] | None:
        products = await self.repository.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset
        )
        return [convert_product_to_read(product) for product in products]

    async def exists(self, name: str) -> bool:
        return await self.repository.exists(name=name)

    async def delete(self, pk: int) -> None:
        # TODO: add logic with deleting photos
        await self.repository.delete(id=pk)

    async def create_with_photos(self, model: PyModel, photos: List[UploadFile]) -> ReadSchemaType:
        photo_paths = await self._save_photos(photos)

        product = await self.repository.create_with_photos(data=model.model_dump(), photo_paths=photo_paths)

        return convert_product_to_read(product)

    async def get(self, pk: int) -> ReadSchemaType:
        return convert_product_to_read(await self.repository.get_single(id=pk))

    async def update_with_photos(self, pk: int, model: PyModel, photos: List[UploadFile]) -> ReadSchemaType:
        # TODO: add logic with updating photos
        photo_paths = await self._save_photos(photos)

        return convert_product_to_read(await self.repository.update_with_photos(data=model.model_dump(),
                                                                                photos=photo_paths, id=pk))

    async def _save_photos(self, photos: List[UploadFile]) -> List[str]:
        saved_photo_paths = []
        for photo in photos:
            file_extension = os.path.splitext(photo.filename)[-1]
            file_name = f"{uuid4()}{file_extension}"
            # TODO: add logic with adding photos
            saved_photo_paths.append(file_name)
        return saved_photo_paths


    async def get_photo(self, photo_name: str):
        photo_path = os.path.join(UPLOADS_DIR, 'product_card.jpg')

        if not os.path.isfile(photo_path):
            raise HTTPException(status_code=404, detail="Photo not found")

        return FileResponse(
            path=photo_path,
            filename=photo_name,
            media_type='image/jpeg'  # Задай правильный тип файла, если он отличается
        )


async def get_product_service(product_db: ProductRepository = Depends(get_product_db)):
    yield ProductService(repository=product_db)
