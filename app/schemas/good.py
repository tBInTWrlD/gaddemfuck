from pydantic import BaseModel, ConfigDict, Field

class GoodCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255, description="Название товара (например, iPhone 15 Pro)")
    brand: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=500)

class GoodUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    brand: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=500)

class GoodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    brand: str | None
    category: str | None
    image_url: str | None
