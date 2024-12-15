from src.report_type.report_type import ReportType


class SalesReport(ReportType):
    def __init__(self, report_author, dirpath):
        self.document_name = 'sales'
        self._document_title = 'Отчет о завершенных заказах'
        super().__init__(report_author, dirpath)

    def generate(self, params: dict):
        pass