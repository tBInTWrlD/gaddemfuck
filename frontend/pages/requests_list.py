import requests
import streamlit as st

from frontend.api.client import create_request, get_error_message, get_good
from frontend.auth.state import require_login

# Страница только для авторизованных
require_login()
st.header("Создание запроса на покупку")

good_id = st.session_state.get("create_request_good_id")

if good_id is None:
    st.info("Сначала выберите товар в общем каталоге.")
    st.page_link("pages/catalog.py", label="Перейти в каталог")
    st.stop()

# Подгружаем инфо о товаре, чтобы пользователь видел, на что оставляет заявку
try:
    good_response = get_good(good_id)
except requests.RequestException:
    st.error("Не удалось связаться с бэкендом.")
    st.stop()

if good_response.ok:
    good_data = good_response.json()
    st.subheader(f"Вы заказываете: {good_data['name']}")
    if good_data.get("brand"):
        st.caption(f"Бренд: {good_data['brand']}")
else:
    st.caption(f"Вы заказываете товар с ID: {good_id}")

st.divider()

with st.form("create_request_form"):
    target_price = st.number_input("Желаемая цена (сколько вы готовы заплатить в ₽)", min_value=1, step=500)
    description = st.text_area("Опишите детали заказа (размер, цвет, ссылка на зарубежный сайт, если есть)")
    submitted = st.form_submit_button("Опубликовать запрос")

if submitted:
    if target_price <= 0:
        st.error("Укажите корректную желаемую цену.")
        st.stop()

    payload = {
        "good_id": int(good_id),
        "description": description.strip() or None,
        "target_price": int(target_price)
    }

    try:
        response = create_request(payload)
    except requests.RequestException:
        st.error("Не удалось отправить запрос на бэкенд.")
        st.stop()

    if response.status_code in (200, 201):
        st.success("Ваш запрос успешно опубликован в ленте! Ожидайте предложений от баеров.")
        # Чистим за собой сессию
        st.session_state.pop("create_request_good_id", None)
        st.page_link("pages/requests.py", label="Перейти в Ленту запросов")
    else:
        st.error(get_error_message(response))
