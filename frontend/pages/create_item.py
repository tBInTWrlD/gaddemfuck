import requests
import streamlit as st

from frontend.api.client import create_good, get_error_message
from frontend.auth.state import require_admin

# Ограничиваем доступ — только админ может наполнять каталог
require_admin()
st.header("Добавление товара в каталог")

with st.form("create_good_form"):
    name = st.text_input("Название товара (например, iPhone 15 Pro)")
    brand = st.text_input("Бренд (например, Apple)")
    category = st.text_input("Категория (например, Электроника)")
    image_url = st.text_input("Ссылка на изображение товара")
    submitted = st.form_submit_button("Добавить в каталог")

if submitted:
    if not name.strip():
        st.error("Укажите название товара.")
        st.stop()

    payload = {
        "name": name.strip(),
        "brand": brand.strip() or None,
        "category": category.strip() or None,
        "image_url": image_url.strip() or None,
    }

    try:
        response = create_good(payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.status_code in (200, 201):
        st.success("Товар успешно добавлен в общий каталог!")
        # Перенаправляем обратно в каталог, чтобы увидеть результат
        st.switch_page("pages/catalog.py")
    else:
        st.error(get_error_message(response))
