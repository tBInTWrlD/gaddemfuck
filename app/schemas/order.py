from pydantic import BaseModel, ConfigDict, Field
from app.models.order import OrderStatus


class OrderCreate(BaseModel):
    offer_id: int = Field(gt=0, description="ID предложения баера, которое принимает покупатель")


class OrderUpdateStatus(BaseModel):
    status: OrderStatus = Field(description="Новый статус заказа")


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    offer_id: int
    request_id: int
    user_id: int
    buyer_id: int
    status: OrderStatus
