from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base



class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Связываем запрос с конкретным товаром из каталога
    good_id: Mapped[int] = mapped_column(ForeignKey("goods.id", ondelete="CASCADE"), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_price: Mapped[int] = mapped_column(nullable=False)

    # Отношения (Relationships)
    creator: Mapped["User"] = relationship(back_populates="requests")
    good: Mapped["Good"] = relationship(back_populates="requests")  # Обратная связь с каталогом товаров
    offers: Mapped[list["Offer"]] = relationship(back_populates="request")
