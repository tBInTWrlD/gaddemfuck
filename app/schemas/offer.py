from pydantic import BaseModel, ConfigDict, Field

class OfferCreate(BaseModel):
    price: int = Field(gt=0, description="Итоговая цена от баера")
    delivery_days: int = Field(gt=0, description="Срок доставки в днях")
    comment: str | None = Field(default=None, max_length=500, description="Комментарий баера")

class OfferUpdate(BaseModel):
    price: int | None = Field(default=None, gt=0)
    delivery_days: int | None = Field(default=None, gt=0)
    comment: str | None = Field(default=None, max_length=500)

class OfferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: int
    buyer_id: int
    price: int
    delivery_days: int
    comment: str | None
