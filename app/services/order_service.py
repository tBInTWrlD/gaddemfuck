from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.repositories.order_repository import OrderRepository
from app.repositories.offer_repository import OfferRepository
from app.schemas.order import OrderCreate, OrderUpdateStatus


class OrderService:

    def __init__(self, db: Session):
        self.repository = OrderRepository(db)
        self.offer_repository = OfferRepository(db)

    def create_order(self, schema: OrderCreate, current_user_id: int) -> Order:
        # 1. Проверяем, существует ли оффер
        offer = self.offer_repository.get_by_id(schema.offer_id)
        if offer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")

        # 2. Проверяем, что именно этот юзер является создателем ЗАПРОСА
        if offer.request.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only accept offers for your own requests"
            )

        # 3. Проверяем, не создан ли уже заказ по этому офферу (связь 1-к-1)
        existing_order = self.repository.get_by_offer_id(schema.offer_id)
        if existing_order is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order for this offer already exists"
            )

        # 4. Создаем заказ
        order = Order(
            offer_id=offer.id,
            request_id=offer.request_id,
            user_id=current_user_id,
            buyer_id=offer.buyer_id,
            status=OrderStatus.PENDING.value
        )
        return self.repository.create(order)

    def get_order(self, order_id: int, current_user_id: int) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Видеть заказ могут только его участники: покупатель или баер
        if order.user_id != current_user_id and order.buyer_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return order

    def update_order_status(self, order_id: int, schema: OrderUpdateStatus, current_user_id: int) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Логика изменения статусов:
        # Например, перевести в SHIPPED (отправлено) может только баер
        if schema.status == OrderStatus.SHIPPED and order.buyer_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the buyer can ship the order")

        # Перевести в DELIVERED (доставлено) может только покупатель, подтверждая получение
        if schema.status == OrderStatus.DELIVERED and order.user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the customer can confirm delivery")

        order.status = schema.status.value
        return self.repository.update(order)

    def get_my_purchases(self, user_id: int) -> list[Order]:
        return self.repository.get_user_orders(user_id)

    def get_my_deliveries(self, buyer_id: int) -> list[Order]:
        return self.repository.get_buyer_orders(buyer_id)
