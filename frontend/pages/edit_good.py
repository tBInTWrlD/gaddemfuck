import requests
import streamlit as st

from frontend.api.client import get_error_message, get_good, update_good, delete_good
from frontend.auth.state import require_admin

# Закрываем доступ для всех, кроме админа
require_admin()
st.header("Редактирование товара в каталоге")

good_id = st.session_state.get("edit_good_id")

if good_id is None:
    st.info("Сначала выберите товар для редактирования.")
    st.stop()

try:
    good_response = get_good(good_id)
except requests.RequestException:
    st.error("Не удалось получить данные о товаре с backend.")
    st.stop()

if not good_response.ok:
    st.error(get_error_message(good_response))
    st.stop()

good = good_response.json()

with st.form(f"edit_good_form_{good_id}"):
    name = st.text_input("Название товара", value=good["name"])
    brand = st.text_input("Бренд", value=good.get("brand") or "")
    category = st.text_input("Категория", value=good.get("category") or "")
    image_url = st.text_input("Ссылка на изображение", value=good.get("image_url") or "")
    submitted = st.form_submit_button("Сохранить изменения")

if submitted:
    if not name.strip():
        st.error("Название товара не может быть пустым.")
        st.stop()

    payload = {
        "name": name.strip(),
        "brand": brand.strip() or None,
        "category": category.strip() or None,
        "image_url": image_url.strip() or None,
    }

    try:
        response = update_good(good_id, payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.ok:
        st.success("Товар успешно обновлен!")
        st.switch_page("pages/catalog.py")
    else:
        st.error(get_error_message(response))
