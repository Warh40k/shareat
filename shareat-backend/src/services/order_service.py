from datetime import datetime, date
from typing import List, Optional

from fastapi import Depends, HTTPException

from src.models import Order
from src.models.order import OrderStatusEnum
from src.repositories.sqlalchemy_repository import ReadSchemaType
from src.schemas.base_schema import PyModel
from src.schemas.order_schema import OrderRead, OrderUpdate, OrderCreate
from src.services.auth.manager import UserManager, get_user_manager
from src.services.base_service import BaseService
from src.repositories.implementations.order_repository import OrderRepository, get_order_db
from src.services.product_service import ProductService, get_product_service


class OrderService(BaseService):
    def __init__(self, repository, product_service: ProductService, user_service: UserManager):
        super().__init__(repository)
        self.product_service = product_service
        self.user_service = user_service

    async def filter(
            self,
            fields: list[str] | None = None,
            order: list[str] | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[ReadSchemaType] | None:
        orders = await self.repository.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset
        )
        return [OrderRead.model_validate(order) for order in orders]

    async def exists(self, name: str) -> bool:
        return await self.repository.exists(name=name)

    async def create(self, model: OrderCreate, user_id: int) -> OrderRead:
        today = date.today()

        # Проверка даты окончания
        if model.end_date <= today:
            raise HTTPException(
                status_code=400, detail="End date must be after the current date."
            )

        # Получение информации о товаре
        product = await self.product_service.get(model.product_id)
        if not product:
            raise HTTPException(
                status_code=404, detail="Product not found"
            )

        # Вычисление общей стоимости
        days_rented = (model.end_date - today).days
        total_price = days_rented * product.price_per_day

        # Проверка и списание средств через сервис пользователя
        try:
            await self.user_service.deduct_balance(user_id=user_id, amount=total_price)
        except HTTPException as e:
            raise e

        # Создание заказа
        order_data_dict = model.model_dump()
        order_data_dict.update({
            "start_date": today,
            "status": OrderStatusEnum.new,
            "user_id": user_id,
            "total_price": total_price,
        })

        # Создаём заказ через репозиторий
        created_order = await self.repository.create(data=order_data_dict)

        # Возвращаем сериализованную модель
        return OrderRead.from_orm(created_order)

    async def update_order_status(self, order_id: int, status: int) -> Optional[OrderRead]:
        """Обновить статус заказа."""
        status_enum = OrderStatusEnum.from_int(status)
        if not status_enum:
            raise HTTPException(status_code=400, detail="Invalid order status")

        updated_order = await self.repository.update(data=OrderUpdate(status=status_enum).model_dump(), id=order_id)
        if not updated_order:
            return None
        return OrderRead.model_validate(updated_order)

    async def get(self, pk: int) -> ReadSchemaType:
        order = await self.repository.get_single(id=pk)
        if not order:
            return None
        return OrderRead.model_validate(order)


async def get_order_service(
    order_db=Depends(get_order_db),
    product_service: ProductService = Depends(get_product_service),
    user_service: UserManager = Depends(get_user_manager),
):
    yield OrderService(repository=order_db, product_service=product_service, user_service=user_service)
