import requests
import streamlit as st

from api.client import (
    delete_request,
    delete_good,
    get_error_message,
)
from auth.state import is_admin, is_authenticated, is_buyer


def render_admin_good_actions(good_id: int, key_prefix: str) -> None:
    if not is_admin():
        return

    edit_column, delete_column = st.columns(2)

    if edit_column.button(
            "Редактировать",
            key=f"{key_prefix}_edit_good_{good_id}",
    ):
        st.session_state["edit_good_id"] = good_id
        st.switch_page("pages/edit_good.py")

    if delete_column.button(
            "Удалить",
            key=f"{key_prefix}_delete_good_{good_id}",
            type="primary",
    ):
        try:
            response = delete_good(good_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.success("Товар удален из каталога.")
            st.rerun()
        else:
            st.error(get_error_message(response))


def render_request_card(request_item: dict) -> None:
    request_id = request_item["id"]
    good_id = request_item["good_id"]

    with st.container(border=True):
        st.caption(f"Запрос №{request_id} • От пользователя ID: {request_item['user_id']}")
        st.markdown(f"### Ищет товар ID: {good_id}")

        if request_item.get("description"):
            st.write(f"**Примечания:** {request_item['description']}")

        st.metric(label="Желаемая цена покупателя", value=f"{request_item['target_price']} ₽")

        if st.button("Посмотреть предложения", key=f"req_details_{request_id}", use_container_width=True):
            st.session_state["selected_request_id"] = request_id
            st.switch_page("pages/request_details.py")


def render_good_card(good_item: dict) -> None:
    good_id = good_item["id"]

    with st.container(border=True):
        if good_item.get("image_url"):
            st.image(good_item["image_url"], use_container_width=True)
        else:
            st.info("Изображение товара отсутствует")

        st.subheader(good_item["name"])
        if good_item.get("brand"):
            st.caption(f"Бренд: {good_item['brand']} | Категория: {good_item.get('category', 'Разное')}")

        if st.button("Хочу этот товар (Создать запрос)", key=f"good_want_{good_id}", type="primary",
                     use_container_width=True):
            if not is_authenticated():
                st.warning("Войдите в систему, чтобы создать запрос.")
            else:
                st.session_state["create_request_good_id"] = good_id
                st.switch_page("pages/create_request.py")

        render_admin_good_actions(good_id, key_prefix="good_card")
