from sqlalchemy.orm import Session
from app.models.offer import Offer


class OfferRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, offer: Offer) -> Offer:
        return self._upsert(offer)

    def update(self, offer: Offer) -> Offer:
        return self._upsert(offer)

    def _upsert(self, offer: Offer) -> Offer:
        self.db.add(offer)
        self.db.commit()
        self.db.refresh(offer)
        return offer

    def get_by_id(self, offer_id: int) -> Offer | None:
        return (
            self.db.query(Offer)
            .filter(Offer.id == offer_id)
            .first()
        )

    def get_by_request_id(self, request_id: int) -> list[Offer]:
        """Получить все отклики баеров на конкретный запрос покупателя"""
        return (
            self.db.query(Offer)
            .filter(Offer.request_id == request_id)
            .all()
        )

    def get_by_buyer_id(self, buyer_id: int) -> list[Offer]:
        """Получить все предложения, которые сделал конкретный баер"""
        return (
            self.db.query(Offer)
            .filter(Offer.buyer_id == buyer_id)
            .all()
        )

    def delete(self, offer: Offer) -> None:
        self.db.delete(offer)
        self.db.commit()
