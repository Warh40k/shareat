from fastapi import APIRouter

from .controllers import user_controller, auth_controller, catalog_controller, admin_controller, order_controller, report_controller


def get_apps_router():
    router = APIRouter()
    router.include_router(admin_controller.router)
    router.include_router(report_controller.router)
    router.include_router(user_controller.router)
    router.include_router(auth_controller.router)
    router.include_router(catalog_controller.router)
    router.include_router(order_controller.router)
    return router
