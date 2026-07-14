from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.request import Request
from app.repositories.request_repository import RequestRepository
from app.repositories.good_repository import GoodRepository  # Импортируем репозиторий товаров
from app.schemas.request import RequestCreate, RequestUpdate


class RequestService:

    def __init__(self, db: Session):
        self.repository = RequestRepository(db)
        self.good_repository = GoodRepository(db)  # Инициализируем для проверки товара

    def create_request(self, schema: RequestCreate, user_id: int) -> Request:
        # Проверяем, существует ли товар в каталоге
        good = self.good_repository.get_by_id(schema.good_id)
        if good is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Good not found in catalog",
            )

        request = Request(
            user_id=user_id,
            good_id=schema.good_id,  # Передаем ID привязанного товара
            description=schema.description,
            target_price=schema.target_price,
        )

        return self.repository.create(request)

    def get_requests(self) -> list[Request]:
        return self.repository.get_all()

    def get_request(self, request_id: int) -> Request:
        request = self.repository.get_by_id(request_id)

        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        return request

    def update_request(
        self,
        request_id: int,
        schema: RequestUpdate,
    ) -> Request:

        request = self.get_request(request_id)

        if schema.good_id is None and schema.description is None and schema.target_price is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.good_id is not None:
            # Если меняют товар, проверяем что новый товар тоже существует в каталоге
            good = self.good_repository.get_by_id(schema.good_id)
            if good is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="New good not found in catalog",
                )
            request.good_id = schema.good_id

        if schema.description is not None:
            request.description = schema.description

        if schema.target_price is not None:
            request.target_price = schema.target_price

        return self.repository.update(request)

    def delete_request(self, request_id: int) -> None:
        request = self.get_request(request_id)

        self.repository.delete(request)
