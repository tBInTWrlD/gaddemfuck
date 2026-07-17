from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.offer import OfferCreate, OfferResponse, OfferUpdate, OfferUpdateStatus
from app.services.offer_service import OfferService

# Добавляем префикс /offers, чтобы все пути начинались с него автоматически
router = APIRouter(
    prefix="/offers",
    tags=["offers"],
)


def get_offer_service(db: Session = Depends(get_db)) -> OfferService:
    return OfferService(db)


# --- 1. СТАТИЧЕСКИЕ ПУТИ ЛИЧНЫХ КАБИНЕТОВ (СТРОГО ВВЕРХУ) ---

@router.get("/my-purchases")
def get_my_purchases(
    current_user: User = Depends(get_current_user),
    service: OfferService = Depends(get_offer_service),
):
    """
    Покупатель смотрит свои заказы.
    Нам нужно в сервисе отфильтровать все офферы,
    которые были приняты (status == 'accepted' / 'shipped' / 'delivered')
    и принадлежат запросам текущего пользователя.
    """
    # Если метод get_offers_by_user еще не написан, мы возвращаем список офферов.
    # В реальном проекте здесь будет вызов: service.get_user_purchases(current_user.id)
    return []


@router.get("/my-deliveries")
def get_my_deliveries(
    current_user: User = Depends(get_current_user),
    service: OfferService = Depends(get_offer_service),
):
    """
    Баер смотрит товары, которые взял в доставку.
    Фильтруем офферы, где buyer_id == current_user.id и status != 'pending'
    """
    # Здесь в будущем будет вызов: service.get_buyer_deliveries(current_user.id)
    return []


# --- 2. ДИНАМИЧЕСКИЕ ПУТИ (СТРОГО ВНИЗУ) ---

@router.get("/{offer_id}", response_model=OfferResponse)
def get_offer(
    offer_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.get_offer(offer_id)


@router.patch("/{offer_id}/status", response_model=OfferResponse)
def update_offer_status(
    offer_id: int,
    schema: OfferUpdateStatus,
    current_user: User = Depends(get_current_user),
    service: OfferService = Depends(get_offer_service),
):
    return service.update_offer_status(
        offer_id=offer_id,
        new_status=schema.status,
        current_user_id=current_user.id
    )


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_offer(
    offer_id: int,
    service: OfferService = Depends(get_offer_service),
) -> None:
    service.delete_offer(offer_id)


# --- 3. ИСКЛЮЧЕНИЕ: СОЗДАНИЕ ОФФЕРА ПРИВЯЗАНО К ЗАПРОСУ ---
# Этот эндпоинт идет отдельно, так как его корень начинается с /requests, а не /offers.
# Мы выносим его в отдельный роутер или прописываем полный путь, игнорируя префикс.
@router.post(
    "/requests/{request_id}/offers",
    response_model=OfferResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True
)
def create_offer(
    request_id: int,
    schema: OfferCreate,
    current_user: User = Depends(require_role(UserRole.BUYER)),
    service: OfferService = Depends(get_offer_service),
):
    return service.create_offer(schema, request_id=request_id, buyer_id=current_user.id)


@router.get(
    "/requests/{request_id}/offers",
    response_model=list[OfferResponse],
)
def get_offers_by_request(
    request_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.get_offers_by_request(request_id)
