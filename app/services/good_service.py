from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.good import Good
from app.repositories.good_repository import GoodRepository
from app.schemas.good import GoodCreate, GoodUpdate


class GoodService:

    def __init__(self, db: Session):
        self.repository = GoodRepository(db)

    def create_good(self, schema: GoodCreate) -> Good:
        good = Good(
            name=schema.name,
            brand=schema.brand,
            category=schema.category,
            image_url=schema.image_url,
        )
        return self.repository.create(good)

    def get_goods(self) -> list[Good]:
        return self.repository.get_all()

    def get_good(self, good_id: int) -> Good:
        good = self.repository.get_by_id(good_id)
        if good is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Good not found in catalog",
            )
        return good

    def search_goods(self, query: str) -> list[Good]:
        return self.repository.search_by_name(query)

    def update_good(self, good_id: int, schema: GoodUpdate) -> Good:
        good = self.get_good(good_id)

        if not any([schema.name, schema.brand, schema.category, schema.image_url]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.name is not None: good.name = schema.name
        if schema.brand is not None: good.brand = schema.brand
        if schema.category is not None: good.category = schema.category
        if schema.image_url is not None: good.image_url = schema.image_url

        return self.repository.update(good)

    def delete_good(self, good_id: int) -> None:
        good = self.get_good(good_id)
        self.repository.delete(good)
