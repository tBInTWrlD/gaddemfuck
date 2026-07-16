from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.offer import OfferCreate, OfferResponse, OfferUpdate, OfferUpdateStatus
from app.services.offer_service import OfferService

router = APIRouter(
    tags=["offers"],
)


def get_offer_service(db: Session = Depends(get_db)) -> OfferService:
    return OfferService(db)


@router.post(
    "/requests/{request_id}/offers",
    response_model=OfferResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_offer(
    request_id: int,
    schema: OfferCreate,
    current_user: User = Depends(require_role(UserRole.BUYER)),
    service: OfferService = Depends(get_offer_service),
):
    return service.create_offer(schema, request_id=request_id, buyer_id=current_user.id)


@router.get(
    "/requests/{request_id}/offers",
    response_model=list[OfferResponse],
)
def get_offers_by_request(
    request_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.get_offers_by_request(request_id)


@router.get(
    "/offers/{offer_id}",
    response_model=OfferResponse,
)
def get_offer(
    offer_id: int,
    service: OfferService = Depends(get_offer_service),
):
    return service.get_offer(offer_id)


@router.patch(
    "/offers/{offer_id}/status",
    response_model=OfferResponse,
)
def update_offer_status(
    offer_id: int,
    schema: OfferUpdateStatus,
    current_user: User = Depends(get_current_user),
    service: OfferService = Depends(get_offer_service),
):
    return service.update_offer_status(
        offer_id=offer_id,
        new_status=schema.status,
        current_user_id=current_user.id
    )


@router.delete(
    "/offers/{offer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_offer(
    offer_id: int,
    service: OfferService = Depends(get_offer_service),
) -> None:
    service.delete_offer(offer_id)
