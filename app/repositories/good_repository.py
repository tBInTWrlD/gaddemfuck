from sqlalchemy.orm import Session
from app.models.good import Good


class GoodRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, good: Good) -> Good:
        return self._upsert(good)

    def update(self, good: Good) -> Good:
        return self._upsert(good)

    def _upsert(self, good: Good) -> Good:
        self.db.add(good)
        self.db.commit()
        self.db.refresh(good)
        return good

    def get_all(self) -> list[Good]:
        return self.db.query(Good).all()

    def get_by_id(self, good_id: int) -> Good | None:
        return (
            self.db.query(Good)
            .filter(Good.id == good_id)
            .first()
        )

    def search_by_name(self, query: str) -> list[Good]:
        """Поиск товаров по названию для каталога"""
        return (
            self.db.query(Good)
            .filter(Good.name.ilike(f"%{query}%"))
            .all()
        )

    def delete(self, good: Good) -> None:
        self.db.delete(good)
        self.db.commit()
