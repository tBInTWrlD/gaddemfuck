from enum import Enum
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class OfferStatus(str, Enum):
    PENDING = "pending"  # Баер предложил, покупатель думает
    ACCEPTED = "accepted"  # Покупатель принял предложение (Заказ в работе)
    SHIPPED = "shipped"  # Баер отправил товар из-за границы
    DELIVERED = "delivered"  # Товар получен покупателем, сделка закрыта
    CANCELED = "canceled"  # Отменено


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    price: Mapped[int] = mapped_column(nullable=False)
    delivery_days: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Сделка контролируется прямо здесь!
    status: Mapped[str] = mapped_column(String(50), default=OfferStatus.PENDING.value, nullable=False)

    # Отношения
    request: Mapped["Request"] = relationship(back_populates="offers")
    buyer: Mapped["User"] = relationship(back_populates="offers")
