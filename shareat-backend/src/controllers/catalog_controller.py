from typing import Annotated, List

from fastapi import HTTPException, Query, APIRouter, Depends, UploadFile, File, Form
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

from src.controllers.fastapi_users import current_active_superuser
from src.models import User
from src.schemas.product_schema import ProductRead, ProductCreate, ProductUpdate
from src.services.product_service import get_product_service, ProductService

UPLOADS_DIR = "resources"

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/getProducts")
async def api_get_products(
        fields: Annotated[list, Query()] = [],
        order: Annotated[list, Query()] = [],
        limit: int | None = None,
        offset: int | None = None,
        product_service: ProductService = Depends(get_product_service)
) -> list[ProductRead] | None:
    try:
        return await product_service.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/getProduct/{product_id}")
async def api_get_product(product_id: int,
                          product_service: ProductService = Depends(get_product_service)
                          ) -> ProductRead:
    try:
        return await product_service.get(pk=product_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.post("/createProduct")
async def api_create_product(
        title: str = Form(...),
        description: str = Form(...),
        price_per_day: float = Form(...),
        in_rent: bool = Form(...),
        is_active: bool = Form(...),
        photos: List[UploadFile] = File(...),
        user: User = Depends(current_active_superuser),
        product_service: ProductService = Depends(get_product_service),
):
    if not photos:
        raise HTTPException(status_code=400, detail="At least one photo is required.")

    product_data = ProductCreate(
        title=title,
        description=description,
        price_per_day=price_per_day,
        in_rent=in_rent,
        is_active=is_active
    )

    try:
        return await product_service.create_with_photos(model=product_data, photos=photos)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


# @router.patch("/updateProduct/{product_id}")
# async def api_update_product(product_id: int, product_data: ProductUpdate,
#                              product_service: ProductService = Depends(get_product_service)
#                              ) -> ProductRead:
#     try:
#         return await product_service.update(pk=product_id, model=product_data)
#     except Exception as e:
#         raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.put("/updateProduct/{product_id}")
async def api_update_product(product_id: int,
                             title: str = Form(...),
                             description: str = Form(...),
                             price_per_day: float = Form(...),
                             in_rent: bool = Form(...),
                             is_active: bool = Form(...),
                             photos: List[UploadFile] = File(...),
                             user: User = Depends(current_active_superuser),
                             product_service: ProductService = Depends(get_product_service)
                             ) -> ProductRead:
    if not photos:
        raise HTTPException(status_code=400, detail="At least one photo is required.")

    product_data = ProductCreate(
        title=title,
        description=description,
        price_per_day=price_per_day,
        in_rent=in_rent,
        is_active=is_active
    )

    try:
        return await product_service.update_with_photos(pk=product_id, model=product_data, photos=photos)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.delete("/deleteProduct/{product_id}", status_code=HTTP_204_NO_CONTENT)
async def api_delete_product(product_id: int,
                             user: User = Depends(current_active_superuser),
                             product_service: ProductService = Depends(get_product_service)
                             ):
    try:
        return await product_service.delete(pk=product_id)
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/getPhoto/{photo_name}")
async def get_photo(photo_name: str,
                    product_service: ProductService = Depends(get_product_service)
                    ):
    try:
        return await product_service.get_photo(photo_name)
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))
