from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, StyleSheet1

from src.models import User


class ReportType(ABC):
    document_name = ""
    document_title = ""
    _report_author = ""
    _template: SimpleDocTemplate = None
    _elements: list = list()
    _styles: StyleSheet1 = None

    def __init__(self, author : str, buffer: BytesIO):
        top_margin = 700
        bottom_margin = 60

        self._report_author = author
        self._template = SimpleDocTemplate(buffer,
           pagesize=A4,
           topMargin=A4[1]-top_margin,
           bottomMargin=bottom_margin,
           leftMargin=50,
           rightMargin=50,
       )
        pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "DejaVuSans-Bold.ttf"))
        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        self._styles = getSampleStyleSheet()

    def include_header_and_footer(self, canvas, doc):
        self.include_header(canvas, doc)
        self.include_footer(canvas, doc)

    def include_header(self, canvas, doc):
        canvas.saveState()

        canvas.setFont("DejaVuSans-Bold", 14)
        canvas.drawString(50, 770, self.document_title)
        canvas.setFont("DejaVuSans", 12)
        canvas.drawString(50, 755, f"Автор: {self._report_author}")
        canvas.drawString(50, 740, f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%m:%S')}")

        canvas.setLineWidth(1)
        canvas.line(50, 735, 550, 735)

        canvas.restoreState()

    def include_footer(self, canvas, doc):
        canvas.saveState()

        canvas.setFont("DejaVuSans-Bold", 10)
        canvas.drawRightString(A4[0] - 50, 35, f"Страница {doc.page}")
        canvas.setFont("DejaVuSans", 12)
        canvas.drawCentredString(A4[0] / 2, 10, "Конфиденциально - Только для внутреннего использования")

        canvas.restoreState()

    @abstractmethod
    async def generate(self, params: dict):
        pass