from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.request import RequestCreate, RequestResponse, RequestUpdate
from app.services.request_service import RequestService

router = APIRouter(
    prefix="/requests",
    tags=["requests"],
)


def get_request_service(
    db: Session = Depends(get_db),
) -> RequestService:
    return RequestService(db)


@router.post(
    "/",
    response_model=RequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_request(
    schema: RequestCreate,
    current_user: User = Depends(get_current_user),
    service: RequestService = Depends(get_request_service),
):
    # Передаем current_user.id в сервис, чтобы зафиксировать автора запроса
    return service.create_request(schema, user_id=current_user.id)


@router.get(
    "/",
    response_model=list[RequestResponse],
)
def get_requests(
    service: RequestService = Depends(get_request_service),
):
    return service.get_requests()


@router.get(
    "/{request_id}",
    response_model=RequestResponse,
)
def get_request(
    request_id: int,
    service: RequestService = Depends(get_request_service),
):
    return service.get_request(request_id)


@router.patch(
    "/{request_id}",
    response_model=RequestResponse,
)
def update_request(
    request_id: int,
    schema: RequestUpdate,
    service: RequestService = Depends(get_request_service),
):
    return service.update_request(request_id, schema)


@router.delete(
    "/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_request(
    request_id: int,
    service: RequestService = Depends(get_request_service),
) -> None:
    service.delete_request(request_id)
