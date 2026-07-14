import requests
from streamlit import session_state

BACKEND_URL = "http://127.0.0.1:8000"

# --- ЭНДПОИНТЫ ---
LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register"
PROFILE_ENDPOINT = f"{BACKEND_URL}/users/me"

GOODS_ENDPOINT = f"{BACKEND_URL}/goods/"
REQUESTS_ENDPOINT = f"{BACKEND_URL}/requests/"
OFFERS_ENDPOINT = f"{BACKEND_URL}/offers/"
ORDERS_ENDPOINT = f"{BACKEND_URL}/orders/"


# --- АВТОРИЗАЦИЯ И ПРОФИЛЬ ---
def register(email: str, password: str, country: str = "Russia") -> requests.Response:
    """Регистрация нового пользователя с указанием страны"""
    data = {
        "email": email,
        "password": password,
        "country": country,
    }
    return requests.post(REGISTER_ENDPOINT, json=data)


def login(email: str, password: str) -> requests.Response:
    data = {
        "email": email,
        "password": password,
    }
    return requests.post(LOGIN_ENDPOINT, json=data)


def get_profile() -> requests.Response:
    return request_with_authorization_header("GET", PROFILE_ENDPOINT)


# --- ГЛОБАЛЬНЫЙ КАТАЛОГ ТОВАРОВ (GOODS) ---
def get_goods() -> requests.Response:
    """Получить весь каталог товаров (доступно всем)"""
    return requests.get(GOODS_ENDPOINT)


def get_good(good_id: int) -> requests.Response:
    return requests.get(f"{GOODS_ENDPOINT}{good_id}")


def search_goods(query: str) -> requests.Response:
    """Поиск товаров по названию в каталоге"""
    return requests.get(f"{GOODS_ENDPOINT}search", params={"query": query})


def create_good(payload: dict) -> requests.Response:
    """Добавить товар в каталог (обычно для роли ADMIN)"""
    return request_with_authorization_header("POST", GOODS_ENDPOINT, payload=payload)


# --- ЗАПРОСЫ ПОКУПАТЕЛЕЙ (REQUESTS) ---
def get_requests() -> requests.Response:
    """Получить список всех открытых запросов, которые видят баеры"""
    return requests.get(REQUESTS_ENDPOINT)


def get_request(request_id: int) -> requests.Response:
    return requests.get(f"{REQUESTS_ENDPOINT}{request_id}")


def create_request(payload: dict) -> requests.Response:
    """Покупатель создает запрос на покупку товара из каталога (передает good_id)"""
    return request_with_authorization_header("POST", REQUESTS_ENDPOINT, payload=payload)


def update_request(request_id: int, payload: dict) -> requests.Response:
    return request_with_authorization_header("PATCH", f"{REQUESTS_ENDPOINT}{request_id}", payload=payload)


def delete_request(request_id: int) -> requests.Response:
    return request_with_authorization_header("DELETE", f"{REQUESTS_ENDPOINT}{request_id}")


# --- ПРЕДЛОЖЕНИЯ БАЕРОВ (OFFERS) ---
def create_offer(request_id: int, payload: dict) -> requests.Response:
    """Баер делает ценовое предложение к конкретному запросу покупателя"""
    endpoint = f"{BACKEND_URL}/requests/{request_id}/offers"
    return request_with_authorization_header("POST", endpoint, payload=payload)


def get_offers_by_request(request_id: int) -> requests.Response:
    """Покупатель смотрит все предложения баеров к своему запросу"""
    endpoint = f"{BACKEND_URL}/requests/{request_id}/offers"
    return requests.get(endpoint)


def get_offer(offer_id: int) -> requests.Response:
    return requests.get(f"{OFFERS_ENDPOINT}{offer_id}")


def update_offer(offer_id: int, payload: dict) -> requests.Response:
    return request_with_authorization_header("PATCH", f"{OFFERS_ENDPOINT}{offer_id}", payload=payload)


def delete_offer(offer_id: int) -> requests.Response:
    return request_with_authorization_header("DELETE", f"{OFFERS_ENDPOINT}{offer_id}")


# --- ЗАКАЗЫ / СДЕЛКИ (ORDERS) ---
def create_order(offer_id: int) -> requests.Response:
    """Покупатель принимает предложение баера и создает заказ (бронирует сделку)"""
    payload = {"offer_id": offer_id}
    return request_with_authorization_header("POST", ORDERS_ENDPOINT, payload=payload)


def get_my_purchases() -> requests.Response:
    """Список покупок текущего авторизованного пользователя"""
    return request_with_authorization_header("GET", f"{ORDERS_ENDPOINT}purchases")


def get_my_deliveries() -> requests.Response:
    """Список доставок баера (какие товары он должен привезти)"""
    return request_with_authorization_header("GET", f"{ORDERS_ENDPOINT}deliveries")


def get_order(order_id: int) -> requests.Response:
    return request_with_authorization_header("GET", f"{ORDERS_ENDPOINT}{order_id}")


def update_order_status(order_id: int, status_str: str) -> requests.Response:
    """Смена статуса заказа (paid, shipped, delivered, canceled)"""
    payload = {"status": status_str}
    return request_with_authorization_header("PATCH", f"{ORDERS_ENDPOINT}{order_id}/status", payload=payload)


def update_good(good_id: int, payload: dict) -> requests.Response:
    """Обновить данные товара в каталоге (для роли ADMIN)"""
    endpoint = f"{GOODS_ENDPOINT}{good_id}"
    return request_with_authorization_header(
        "PATCH",
        endpoint,
        payload=payload,
    )


def delete_good(good_id: int) -> requests.Response:
    """Удалить товар из каталога (для роли ADMIN)"""
    endpoint = f"{GOODS_ENDPOINT}{good_id}"
    return request_with_authorization_header("DELETE", endpoint)


# --- СИСТЕМНОЕ ЯДРО КЛИЕНТА ---
def request_with_authorization_header(
    request_type: str,
    endpoint: str,
    params: dict | None = None,
    payload: dict | None = None,
) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {session_state.get('access_token', '')}"
    }

    if request_type == "GET":
        response = requests.get(endpoint, headers=headers, params=params)
    elif request_type == "POST":
        response = requests.post(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "PATCH":
        response = requests.patch(endpoint, headers=headers, params=params, json=payload)
    elif request_type == "DELETE":
        response = requests.delete(endpoint, headers=headers, params=params)
    else:
        raise ValueError("Неизвестный тип запроса")

    if response.status_code == 401:
        session_state.pop("access_token", None)
        session_state.pop("profile", None)

    return response


def get_error_message(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка backend: HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка backend: HTTP {response.status_code}"

