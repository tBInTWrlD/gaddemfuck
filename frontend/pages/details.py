import requests
import streamlit as st

from frontend.api.client import (
    get_error_message,
    get_request,
    get_offers_by_request,
    create_offer,
    create_order
)
from frontend.auth.state import is_authenticated, is_buyer, current_profile

request_id = st.session_state.get("selected_request_id")

if request_id is None:
    st.info("Сначала выберите запрос для просмотра.")
    st.page_link("pages/catalog.py", label="Перейти к списку товаров")
    st.stop()

# 1. Загружаем данные о самом запросе
try:
    req_response = get_request(request_id)
    offers_response = get_offers_by_request(request_id)
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not req_response.ok:
    st.error(get_error_message(req_response))
    st.stop()

request_data = req_response.json()
offers = offers_response.json() if offers_response.ok else []

# --- ОТОБРАЖЕНИЕ ЗАПРОСА ---
st.header(f"Запрос №{request_data['id']}")
st.subheader(f"Ищет товар ID: {request_data['good_id']}")
st.write(f"**Описание от покупателя:** {request_data.get('description') or 'Нет описания'}")
st.metric(label="Желаемая цена покупателя", value=f"{request_data['target_price']} ₽")

st.divider()

# --- БЛОК ДЛЯ БАЕРА: ОТПРАВКА ПРЕДЛОЖЕНИЯ ---
if is_authenticated() and is_buyer():
    st.subheader("⚡ Оставить свое предложение (Для баеров)")

    with st.form("send_offer_form"):
        price = st.number_input("Ваша цена доставки и выкупа (₽)", min_value=1, step=500)
        delivery_days = st.number_input("Срок доставки (в днях)", min_value=1, step=1)
        comment = st.text_area("Комментарий к предложению (например, условия возврата или нюансы)")
        offer_submitted = st.form_submit_button("Отправить предложение покупателю")

    if offer_submitted:
        payload = {"price": int(price), "delivery_days": int(delivery_days), "comment": comment.strip() or None}
        try:
            off_res = create_offer(request_id, payload)
        except requests.RequestException:
            st.error("Ошибка сети при отправке предложения.")
            st.stop()

        if off_res.status_code in (200, 201):
            st.success("Ваше предложение успешно отправлено!")
            st.rerun()
        else:
            st.error(get_error_message(off_res))

# --- СПИСОК ВСЕХ ПРЕДЛОЖЕНИЙ ОТ БАЕРОВ ---
st.subheader("💬 Предложения от баеров")
if not offers:
    st.info("На этот запрос пока нет откликов от баеров.")
else:
    for offer in offers:
        with st.container(border=True):
            profile = current_profile()
            is_owner = profile and profile.get("id") == request_data["user_id"]

            st.markdown(f"**Баер ID {offer['buyer_id']}** предлагает:")
            st.markdown(f"**Цена:** {offer['price']} ₽ | **Срок:** {offer['delivery_days']} дн.")
            if offer.get("comment"):
                st.caption(f"Комментарий: {offer['comment']}")

            # Если текущий пользователь — автор запроса, он может принять предложение и создать сделку
            if is_owner:
                if st.button("🤝 Принять предложение и заказать", key=f"accept_offer_{offer['id']}", type="primary"):
                    try:
                        order_res = create_order(offer["id"])
                    except requests.RequestException:
                        st.error("Ошибка при создании заказа.")
                        st.stop()

                    if order_res.status_code in (200, 201):
                        st.success("Заказ успешно создан! Переходим к вашим покупкам.")
                        st.switch_page("pages/purchases.py")
                    else:
                        st.error(get_error_message(order_res))
