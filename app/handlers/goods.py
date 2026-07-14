from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import require_role
from app.database import get_db
from app.models.user import UserRole
from app.schemas.good import GoodCreate, GoodResponse, GoodUpdate
from app.services.good_service import GoodService

router = APIRouter(
    prefix="/goods",
    tags=["goods"],
)


def get_good_service(db: Session = Depends(get_db)) -> GoodService:
    return GoodService(db)


@router.post(
    "/",
    response_model=GoodResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_good(
    schema: GoodCreate,
    service: GoodService = Depends(get_good_service),
    current_user=Depends(require_role(UserRole.ADMIN)),  # Наполнять каталог может, например, только админ
):
    """Добавить новый товар в глобальный каталог"""
    return service.create_good(schema)


@router.get(
    "/",
    response_model=list[GoodResponse],
)
def get_goods(
    service: GoodService = Depends(get_good_service),
):
    """Получить весь каталог товаров"""
    return service.get_goods()


@router.get(
    "/search",
    response_model=list[GoodResponse],
)
def search_goods(
    query: str,
    service: GoodService = Depends(get_good_service),
):
    """Поиск по каталогу товаров"""
    return service.search_goods(query)


@router.get(
    "/{good_id}",
    response_model=GoodResponse,
)
def get_good(
    good_id: int,
    service: GoodService = Depends(get_good_service),
):
    return service.get_good(good_id)
