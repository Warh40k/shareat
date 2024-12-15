from datetime import datetime, date
from io import BytesIO

from fastapi_users import FastAPIUsers
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from src.models import User
from src.models.order import OrderStatusEnum
from src.report_type.report_type import ReportType
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from src.schemas.order_schema import OrderRead
from src.schemas.product_schema import ProductRead
from src.schemas.user_schema import UserCreate
from src.services.order_service import OrderService
from src.services.product_service import ProductService


class ActiveOrdersReport(ReportType):
    def __init__(self, author: str, buffer : BytesIO):
        self.document_name = 'active_orders'
        self.document_title = 'Информация об активных заказах'
        super().__init__(author, buffer)

    async def generate(self, params: dict):
        table_data = await self.get_table_data(params)
        table = Table(table_data)
        # Apply a style to the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),  # Header font
            ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Body background
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines
        ])
        table.setStyle(style)

        self._elements.append(table)
        self._elements.append(Spacer(1,20))

        self._template.build(self._elements, onFirstPage=self.include_header_and_footer, onLaterPages=self.include_footer)

    async def get_table_data(self, params: dict) -> list:
        order_service : OrderService = params['order_service']
        product_service : ProductService = params['product_service']
        orders : list[OrderRead] = await order_service.filter()
        curdate : date = datetime.date(datetime.now())
        result = [['Товар', 'Клиент', 'Дата аренды', 'Дата окончания', 'Цена в день', 'Стоимость по окончанию срока']]
        for order in orders:
            if not (order.is_active and (order.status in [OrderStatusEnum.in_rent.to_int(), OrderStatusEnum.returned.to_int()]) and order.end_date > curdate):
                continue
            cur_product : ProductRead = await product_service.get(pk=order.product_id)
            row = [cur_product.title, order.user_id, order.start_date, order.end_date, cur_product.price_per_day,
                   order.total_price]
            result.append(row)

        return result
