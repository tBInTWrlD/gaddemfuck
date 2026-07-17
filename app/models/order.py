from enum import Enum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class OrderStatus(str, Enum):
    PENDING = "pending"  # Ожидает оплаты / подтверждения
    PAID = "paid"  # Оплачен покупателем
    SHIPPED = "shipped"  # Баер отправил товар из другой страны
    DELIVERED = "delivered"  # Доставлен и успешно закрыт
    CANCELED = "canceled"  # Отменен


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Связь "Один к одному": ставим unique=True, чтобы на один оффер нельзя было создать два заказа
    offer_id: Mapped[int] = mapped_column(
        ForeignKey("offers.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    # Дублируем для удобства выборки (хотя можно вытащить и через offer.request_id)
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)

    # Кто покупает и кто везет (для быстрых выборок в БД)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    status: Mapped[str] = mapped_column(
        String(50),
        default=OrderStatus.PENDING.value,
        nullable=False
    )

    # Отношения (Relationships)
    offer: Mapped["Offer"] = relationship()
    request: Mapped["Request"] = relationship()
