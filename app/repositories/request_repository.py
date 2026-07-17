from sqlalchemy.orm import Session
from app.models.request import Request


class RequestRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, request: Request) -> Request:
        return self._upsert(request)

    def update(self, request: Request) -> Request:
        return self._upsert(request)

    def _upsert(self, request: Request) -> Request:
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    def get_all(self) -> list[Request]:
        return self.db.query(Request).all()

    def get_by_id(self, request_id: int) -> Request | None:
        return (
            self.db.query(Request)
            .filter(Request.id == request_id)
            .first()
        )

    def get_by_user_id(self, user_id: int) -> list[Request]:
        """Получить все запросы конкретного покупателя"""
        return (
            self.db.query(Request)
            .filter(Request.user_id == user_id)
            .all()
        )

    def delete(self, request: Request) -> None:
        self.db.delete(request)
        self.db.commit()
