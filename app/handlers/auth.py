from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    schema: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(schema)


@router.post(
    "/login",
    response_model=Token,
)
def login_user(
    schema: UserLogin,
    service: AuthService = Depends(get_auth_service),
):
    return service.login(schema)