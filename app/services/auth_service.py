from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserLogin


class AuthService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def login(self, schema: UserLogin) -> Token:
        user = self._authenticate_user(schema.email, schema.password)
        access_token = create_access_token(user.id)

        return Token(access_token=access_token)

    def _authenticate_user(self, email: str, password: str) -> User:
        user = self.repository.get_by_email(email)

        if user is None:
            raise self._invalid_credentials_error()

        if not verify_password(password, user.hashed_password):
            raise self._invalid_credentials_error()

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    def _invalid_credentials_error(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )