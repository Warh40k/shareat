import os
from typing import List
from uuid import uuid4

from fastapi import Depends, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

from src.models import Product
from src.repositories.sqlalchemy_repository import ReadSchemaType
from src.schemas.base_schema import PyModel
from src.schemas.product_schema import ProductRead
from src.services.base_service import BaseService
from src.repositories.implementations.product_repository import ProductRepository, get_product_db
from src.services.s3_service import S3Service, get_s3_service


def convert_product_to_read(product: Product) -> ProductRead | None:
    if product is not None:
        return ProductRead(
            id=product.id,
            title=product.title,
            description=product.description,
            price_per_day=product.price_per_day,
            in_rent=product.in_rent,
            is_active=product.is_active,
            photos=[photo.path for photo in product.photos] if product.photos else []
        )
    else:
        return None


class ProductService(BaseService):
    def __init__(self, repository: ProductRepository, s3_service: S3Service):
        super().__init__(repository=repository)
        self.s3_service = s3_service

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
        product = await self.repository.get_single(id=pk)
        if product and product.photos:
            for photo in product.photos:
                # Удаляем фото из S3
                await self.s3_service.delete_file(f"photos/{photo.path}")
        await self.repository.delete(id=pk)

    async def create_with_photos(self, model: PyModel, photos: List[UploadFile]) -> ReadSchemaType:
        photo_urls = []
        for photo in photos:
            file_extension = os.path.splitext(photo.filename)[-1]
            file_name = f"{uuid4()}{file_extension}"  # Генерируем уникальное имя файла
            url = await self.s3_service.upload_file(photo, file_name, folder="photos")
            photo_urls.append(url.split("/")[-1])

        product = await self.repository.create_with_photos(data=model.model_dump(), photo_paths=photo_urls)
        return convert_product_to_read(product)

    async def get(self, pk: int) -> ReadSchemaType:
        return convert_product_to_read(await self.repository.get_single(id=pk))

    async def update_with_photos(self, pk: int, model: PyModel, photos: List[UploadFile]) -> ReadSchemaType:
        product = await self.repository.get_single(id=pk)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Удаление старых фото
        if product.photos:
            for photo in product.photos:
                await self.s3_service.delete_file(f"photos/{photo.path}")

        # Загрузка новых фото
        photo_urls = []
        for photo in photos:
            file_extension = os.path.splitext(photo.filename)[-1]
            file_name = f"{uuid4()}{file_extension}"  # Генерируем уникальное имя файла
            url = await self.s3_service.upload_file(photo, file_name, folder="photos")
            photo_urls.append(url.split("/")[-1])

        return convert_product_to_read(
            await self.repository.update_with_photos(data=model.model_dump(), photos=photo_urls, id=pk)
        )

    async def get_photo(self, photo_name: str) -> StreamingResponse:
        """
        Получает файл из S3 через S3Service и возвращает его как поток.
        """
        try:
            file_stream, content_type = await self.s3_service.get_file(f"photos/{photo_name}")
            return StreamingResponse(
                file_stream,
                media_type=content_type,
                headers={
                    "Content-Disposition": f"inline; filename={photo_name}"
                }
            )
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Photo not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def get_product_service(
        product_db: ProductRepository = Depends(get_product_db),
        s3_service: S3Service = Depends(get_s3_service),
):
    yield ProductService(repository=product_db, s3_service=s3_service)
