from fastapi import HTTPException, status
from sqlalchemy.orm import Session

# ИМПОРТЫ МОДЕЛЕЙ И РЕПОЗИТОРИЕВ (Решают проблему NameError)
from app.models.offer import Offer
from app.repositories.offer_repository import OfferRepository
from app.repositories.request_repository import RequestRepository
from app.schemas.offer import OfferCreate, OfferUpdate


class OfferService:

    def __init__(self, db: Session):
        self.repository = OfferRepository(db)
        self.request_repository = RequestRepository(db)  # Для проверки существования запроса

    def create_offer(self, schema: OfferCreate, request_id: int, buyer_id: int) -> Offer:
        """Создать предложение от баера"""
        request = self.request_repository.get_by_id(request_id)
        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        offer = Offer(
            request_id=request_id,
            buyer_id=buyer_id,
            price=schema.price,
            delivery_days=schema.delivery_days,
            comment=schema.comment,
            status="pending"  # Статус по умолчанию при создании
        )

        return self.repository.create(offer)

    def get_offers_by_request(self, request_id: int) -> list[Offer]:
        """Получить все предложения к конкретному запросу"""
        return self.repository.get_by_request_id(request_id)

    def get_offer(self, offer_id: int) -> Offer:
        """Получить одно предложение по ID"""
        offer = self.repository.get_by_id(offer_id)
        if offer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer not found",
            )
        return offer

    def update_offer(self, offer_id: int, schema: OfferUpdate) -> Offer:
        """Обновить поля предложения"""
        offer = self.get_offer(offer_id)

        if schema.price is None and schema.delivery_days is None and schema.comment is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.price is not None:
            offer.price = schema.price
        if schema.delivery_days is not None:
            offer.delivery_days = schema.delivery_days
        if schema.comment is not None:
            offer.comment = schema.comment

        return self.repository.update(offer)

    def update_offer_status(self, offer_id: int, new_status: str, current_user_id: int) -> Offer:
        """Управление статусами сделки (вместо сущности Orders)"""
        offer = self.get_offer(offer_id)

        # Логика: Принять предложение (accepted) может только создатель ЗАПРОСА
        if new_status == "accepted" and offer.request.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Только автор запроса может принять оффер")

        # Логика: Изменить на "отправлено" (shipped) может только баер
        if new_status == "shipped" and offer.buyer_id != current_user_id:
            raise HTTPException(status_code=403, detail="Только баер может отметить отправку")

        # Логика: Изменить на "доставлено" (delivered) может только покупатель
        if new_status == "delivered" and offer.request.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Только покупатель подтверждает получение")

        offer.status = new_status
        return self.repository.update(offer)

    def delete_offer(self, offer_id: int) -> None:
        """Удалить предложение"""
        offer = self.get_offer(offer_id)
        self.repository.delete(offer)
