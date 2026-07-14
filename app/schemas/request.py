from pydantic import BaseModel, ConfigDict, Field

class RequestCreate(BaseModel):
    good_id: int = Field(gt=0, description="ID товара из каталога")
    description: str | None = Field(default=None, max_length=1000, description="Детали: размер, цвет, примечания")
    target_price: int = Field(gt=0, description="Желаемая цена в рублях/валюте")

class RequestUpdate(BaseModel):
    good_id: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, max_length=1000)
    target_price: int | None = Field(default=None, gt=0)

class RequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    good_id: int
    description: str | None
    target_price: int
