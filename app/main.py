import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from app.config.config import get_settings
from app.database import Base, engine
from app.handlers.auth import router as auth_router
from app.handlers.users import router as users_router
from app.handlers.requests import router as requests_router
from app.handlers.offers import router as offers_router
from app.handlers.goods import router as goods_router
from app.models.order import Order
from app.handlers.orders import router as orders_router
from app.models.order import Order
from app.handlers.orders import router as orders_router

# Импортируем новые модели, чтобы Base.metadata.create_all нашел их структуру
from app.models.user import User
from app.models.request import Request
from app.models.offer import Offer

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,

)

# Автоматически создаем таблицы в файле marketplace.db
Base.metadata.create_all(bind=engine)

# Подключаем роутеры
app.include_router(orders_router)
app.include_router(goods_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(requests_router)
app.include_router(offers_router)
app.include_router(orders_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
