from sqlalchemy.orm import Session
from app.models.order import Order


class OrderRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, order: Order) -> Order:
        return self._save(order)

    def update(self, order: Order) -> Order:
        return self._save(order)

    def _save(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> Order | None:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_by_offer_id(self, offer_id: int) -> Order | None:
        """Проверка: нет ли уже заказа по этому офферу"""
        return self.db.query(Order).filter(Order.offer_id == offer_id).first()

    def get_user_orders(self, user_id: int) -> list[Order]:
        """Все заказы пользователя как покупателя"""
        return self.db.query(Order).filter(Order.user_id == user_id).all()

    def get_buyer_orders(self, buyer_id: int) -> list[Order]:
        """Все заказы пользователя как баера (что ему нужно привезти)"""
        return self.db.query(Order).filter(Order.buyer_id == buyer_id).all()
