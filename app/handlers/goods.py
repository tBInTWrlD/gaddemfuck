from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import require_role
from app.database import get_db
from app.models.user import UserRole
from app.schemas.good import GoodCreate, GoodUpdate
from app.services.good_service import GoodService

router = APIRouter(
    prefix="/goods",
    tags=["goods"],
)


def get_good_service(db: Session = Depends(get_db)) -> GoodService:
    return GoodService(db)


@router.post(
    "",  # Благодаря префиксу путь будет просто /goods
    status_code=status.HTTP_201_CREATED,
)
def create_good(
    schema: GoodCreate,
    service: GoodService = Depends(get_good_service),
    current_user=Depends(require_role(UserRole.ADMIN)),  # Только админ может создавать товары
):
    """Добавить новый товар в глобальный каталог"""
    g = service.create_good(schema)
    return {
        "id": g.id,
        "name": g.name,
        "brand": g.brand,
        "category": g.category,
        "image_url": g.image_url
    }


@router.get("")  # Путь /goods
def get_goods(
    service: GoodService = Depends(get_good_service),
):
    """Получить весь каталог товаров (безопасный плоский JSON)"""
    goods = service.get_goods()
    return [
        {
            "id": g.id,
            "name": g.name,
            "brand": g.brand,
            "category": g.category,
            "image_url": g.image_url
        } for g in goods
    ]


@router.get("/search")  # Путь /goods/search
def search_goods(
    query: str,
    service: GoodService = Depends(get_good_service),
):
    """Поиск по каталогу товаров"""
    goods = service.search_goods(query)
    return [
        {
            "id": g.id,
            "name": g.name,
            "brand": g.brand,
            "category": g.category,
            "image_url": g.image_url
        } for g in goods
    ]


@router.get("/{good_id}")  # Путь /goods/{good_id}
def get_good(
    good_id: int,
    service: GoodService = Depends(get_good_service),
):
    """Получить конкретный товар по его ID"""
    g = service.get_good(good_id)
    return {
        "id": g.id,
        "name": g.name,
        "brand": g.brand,
        "category": g.category,
        "image_url": g.image_url
    }


@router.patch("/{good_id}")  # Путь /goods/{good_id}
def update_good(
    good_id: int,
    schema: GoodUpdate,
    service: GoodService = Depends(get_good_service),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    """Обновить товар в каталоге (только для админа)"""
    g = service.update_good(good_id, schema)
    return {
        "id": g.id,
        "name": g.name,
        "brand": g.brand,
        "category": g.category,
        "image_url": g.image_url
    }


@router.delete("/{good_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_good(
    good_id: int,
    service: GoodService = Depends(get_good_service),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    """Удалить товар из каталога (только для админа)"""
    service.delete_good(good_id)
