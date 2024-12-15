from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

from src.controllers.fastapi_users import current_active_manageruser
from src.models import User
from src.schemas.report_schema import ReportRead, ReportCreate
from src.services.report_service import get_report_service, BaseReportService

router = APIRouter(prefix="/report", tags=["report"])

@router.get("/getReports", response_model=List[ReportRead])
async def api_get_reports(
        fields: Annotated[list, Query()] = [],
        order: Annotated[list, Query()] = [],
        limit: int | None = None,
        offset: int | None = None,
        user: User = Depends(current_active_manageruser),
        report_service: BaseReportService = Depends(get_report_service),
) -> list[ReportRead] | None:
    try:
        return await report_service.filter(
            fields=fields,
            order=order,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@router.get("/getReportInfo/{report_id}", response_model=ReportRead)
async def api_get_report(report_id: int,
                        user: User = Depends(current_active_manageruser),
                        report_service: BaseReportService = Depends(get_report_service)
                        ) -> ReportRead:
    try:
        return await report_service.get(pk=report_id)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))

@router.post("/createReport", response_model=ReportRead)
async def create_report(report_data: ReportCreate,
                        user: User = Depends(current_active_manageruser),
                        service: BaseReportService = Depends(get_report_service)):
    """Создать отчет (Менеджер)."""
    return await service.create(model=report_data, user = user)
    # try:
    #
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))