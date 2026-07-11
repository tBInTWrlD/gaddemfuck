from fastapi import APIRouter
from app.config.config import get_settings
router = APIRouter(
    prefix="/health",
    tags=["health"],
    )
@router.get("")
def health_check():
    settings = get_settings()
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
    }