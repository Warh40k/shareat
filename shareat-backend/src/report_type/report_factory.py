from typing import Type

from src.report_type.implementations.active_orders_report import ActiveOrdersReport
from src.report_type.implementations.inventory_report import InventoryReport
from src.report_type.implementations.sales_report import SalesReport


class ReportFactory:
    _report_types = {
        "sales": SalesReport,
        "inventory" : InventoryReport,
        "active_orders": ActiveOrdersReport,
    }

    @staticmethod
    def get_report(report_type: str) -> Type[InventoryReport | ActiveOrdersReport | SalesReport]:
        report_class = ReportFactory._report_types.get(report_type)
        if not report_class:
            raise ValueError(f"Report type '{report_type}' not found")
        return report_class