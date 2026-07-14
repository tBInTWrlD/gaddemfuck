from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Good(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Связи: этот товар может фигурировать во множестве запросов от разных людей
    requests: Mapped[list["Request"]] = relationship(back_populates="good", cascade="all, delete-orphan")
