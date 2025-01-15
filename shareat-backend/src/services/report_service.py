import io
import os
from datetime import datetime

from fastapi import Depends, UploadFile, HTTPException
from starlette.responses import StreamingResponse

from src.config.project_config import settings
from src.models import User, Report
from src.repositories.sqlalchemy_repository import ReadSchemaType
from src.schemas.report_schema import ReportRead, ReportCreate
from src.services.auth.manager import UserManager, get_user_manager
from src.services.base_service import BaseService
from src.repositories.implementations.report_repository import get_report_db
from src.services.order_service import OrderService, get_order_service
from src.services.product_service import ProductService, get_product_service
from src.report_type.report_factory import ReportFactory
from src.services.s3_service import S3Service, get_s3_service


class ReportService(BaseService):
    def __init__(self, repository, product_service: ProductService, order_service: OrderService, user_service: UserManager, s3_service: S3Service):
        super().__init__(repository)
        self.user_service = user_service
        self.product_service = product_service
        self.order_service = order_service
        self.s3_service = s3_service

    async def filter(
            self,
            fields: list[str] | None = None,
            order: list[str] | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[ReadSchemaType] | None:
        reports = await self.repository.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset
        )
        return [ReportRead.model_validate(convert_product_to_read(report)) for report in reports]

    async def exists(self, name: str) -> bool:
        return await self.repository.exists(name=name)

    async def create(self, model: ReportCreate, user: User) -> ReportRead:
        report_class = ReportFactory.get_report(model.type)
        buffer = io.BytesIO()
        generator = report_class(f"{user.firstname} {user.secondname}", buffer)
        params = {
            "product_service": self.product_service,
            "order_service" : self.order_service,
        }
        await generator.generate(params)
        buffer.seek(0)
        datet = datetime.now()
        filename = str(int(datet.timestamp()))
        file = UploadFile(file=buffer, filename=filename)
        url = await self.s3_service.upload_file(file,filename,
                                          settings.BASE_REPORT_PATH+'/'+generator.document_name)
        report_data_dict = model.model_dump()
        report_data_dict.update(
            {
                "key": url,
                "type": generator.document_name,
                "date": datet,
                "author_id": user.id,
            }
        )
        created_order = await self.repository.create(data=report_data_dict)

        return created_order

    async def get(self, pk: int) -> ReadSchemaType:
        report = await self.repository.get_single(id=pk)
        if not report:
            return ReportRead()
        resp = ReportRead(id=report.id, type=report.type, key=report.key, date=report.date, author_id=report.author_id)
        return ReportRead.model_validate(resp)

    async def get_report(self, report_key: str) -> StreamingResponse:
        """
        Получает файл из S3 через S3Service и возвращает его как поток.
        """
        try:
            file_stream, content_type = await self.s3_service.get_file(f"{report_key}")
            return StreamingResponse(
                file_stream,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"inline; filename={os.path.basename(report_key)}"
                }
            )
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Photo not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


async def get_report_service(
    report_db=Depends(get_report_db),
    product_service: ProductService = Depends(get_product_service),
    user_service: UserManager = Depends(get_user_manager),
    order_service: OrderService = Depends(get_order_service),
    s3_service: S3Service = Depends(get_s3_service),
):
    yield ReportService(repository=report_db, product_service=product_service, user_service=user_service, order_service=order_service, s3_service=s3_service)

def convert_product_to_read(report: Report) -> ReportRead | None:
    if report:
        return ReportRead(
            id = report.id,
            type = report.type,
            key = report.key,
            date = report.date,
            author_id = report.author_id
        )
    else:
        return None