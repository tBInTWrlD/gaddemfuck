import requests
import streamlit as st

from frontend.api.client import get_error_message, get_goods
from frontend.auth.state import is_admin
from frontend.components.item_card import render_good_card  # Импортируем карточку товара

st.header("Каталог доступных товаров")

# Если зашел админ, даем ему кнопку для добавления товара в каталог
if is_admin():
    if st.button("Добавить товар в каталог"):
        st.switch_page("pages/create_good.py")

try:
    response = get_goods()
except requests.RequestException:
    st.error("Backend недоступен. Проверьте запуск FastAPI.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

goods = response.json()

if not goods:
    st.info("В каталоге товаров пока пусто. Адветьте администратору, чтобы он добавил позиции.")
    st.stop()

# Выводим товары в сетку из 3 колонок
columns = st.columns(3)

for index, good in enumerate(goods):
    with columns[index % 3]:
        render_good_card(good)
