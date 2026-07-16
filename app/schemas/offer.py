from pydantic import BaseModel, ConfigDict, Field

class OfferCreate(BaseModel):
    price: int = Field(gt=0)
    delivery_days: int = Field(gt=0)
    comment: str | None = Field(default=None, max_length=500)

class OfferUpdate(BaseModel):
    price: int | None = Field(default=None, gt=0)
    delivery_days: int | None = Field(default=None, gt=0)
    comment: str | None = Field(default=None, max_length=500)

class OfferUpdateStatus(BaseModel):
    status: str = Field(description="Новый статус сделки (accepted, shipped, delivered, canceled)")

class OfferResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: int
    buyer_id: int
    price: int
    delivery_days: int
    comment: str | None
    status: str
