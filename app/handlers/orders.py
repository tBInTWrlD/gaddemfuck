from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdateStatus
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    schema: OrderCreate,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    """Покупатель принимает оффер баера и создает заказ"""
    return service.create_order(schema, current_user_id=current_user.id)


@router.get("/purchases", response_model=list[OrderResponse])
def get_my_purchases(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    """Список покупок текущего пользователя (он в роли покупателя)"""
    return service.get_my_purchases(user_id=current_user.id)


@router.get("/deliveries", response_model=list[OrderResponse])
def get_my_deliveries(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    """Список доставок текущего пользователя (он в роли баера)"""
    return service.get_my_deliveries(buyer_id=current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return service.get_order(order_id, current_user_id=current_user.id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    schema: OrderUpdateStatus,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    """Обновление статуса (оплата, отправка, получение)"""
    return service.update_order_status(order_id, schema, current_user_id=current_user.id)
