from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.models.user import UserRole  # Импортируем Enum ролей


class UserCreate(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=128)
    country: str = Field(default="Russia", min_length=2, max_length=100)
    # Если хочешь, чтобы при регистрации можно было сразу выбрать роль (например, "buyer"):
    role: UserRole = Field(default=UserRole.USER)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email:
            raise ValueError("Email must contain @")
        return email


class UserLogin(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email:
            raise ValueError("Email must contain @")
        return email


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    country: str
    is_active: bool
    role: UserRole  # Возвращаем роль в виде Enum
