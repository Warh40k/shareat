from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

from src.controllers.fastapi_users import current_active_manageruser, current_active_clientuser
from src.models import User
from src.schemas.order_schema import OrderRead, OrderCreate
from src.services.order_service import OrderService, get_order_service

router = APIRouter(prefix="/order", tags=["order"])


@router.get("/getOrders", response_model=List[OrderRead])
async def api_get_orders(
        fields: Annotated[list, Query()] = [],
        order: Annotated[list, Query()] = [],
        limit: int | None = None,
        offset: int | None = None,
        user: User = Depends(current_active_manageruser),
        order_service: OrderService = Depends(get_order_service),
) -> list[OrderRead] | None:
    try:
        return await order_service.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/getOrderInfo/{order_id}", response_model=OrderRead)
async def api_get_order(order_id: int,
                        user: User = Depends(current_active_manageruser),
                        order_service: OrderService = Depends(get_order_service)
                        ) -> OrderRead:
    try:
        return await order_service.get(pk=order_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.post("/createOrder", response_model=OrderRead)
async def create_order(order_data: OrderCreate,
                       user: User = Depends(current_active_clientuser),
                       service: OrderService = Depends(get_order_service)):
    """Создать заказ (Клиент)."""
    return await service.create(model=order_data, user_id=user.id)
    # try:
    #
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


@router.patch("/setOrderStatus", response_model=OrderRead)
async def set_order_status(order_id: int,
                           status: int,
                           user: User = Depends(current_active_manageruser),
                           service: OrderService = Depends(get_order_service)):
    """Изменить статус заказа (Менеджер)."""
    try:
        return await service.update_order_status(order_id, status)
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))
