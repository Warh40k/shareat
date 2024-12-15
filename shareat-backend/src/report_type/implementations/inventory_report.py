from abc import abstractmethod

from src.report_type.report_type import ReportType


class InventoryReport(ReportType):
    def __init__(self, report_author, dirpath):
        self._document_name = 'inventory'
        self._document_title = 'Отчет об инвентаризации'
        super().__init__(report_author, dirpath)

    def generate(self, params: dict):
        pass