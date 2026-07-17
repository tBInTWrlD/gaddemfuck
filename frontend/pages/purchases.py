import requests
import streamlit as st

from api.client import get_error_message, get_my_purchases, change_offer_status
from auth.state import require_login

require_login()
st.header("🛍️ Мои заказы (Покупки)")

try:
    response = get_my_purchases()
except requests.RequestException:
    st.error("Бэкенд недоступен.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

my_orders = response.json()

if not my_orders:
    st.info("У вас пока нет оформленных заказов.")
    st.page_link("pages/requests.py", label="Посмотреть ленту своих запросов")
    st.stop()

for order in my_orders:
    with st.container(border=True):
        st.subheader(f"Заказ по предложению №{order['id']}")
        st.write(f"**Цена сделки:** {order['price']} ₽")
        st.write(f"**Срок доставки:** {order['delivery_days']} дней")
        st.info(f"Текущий статус: **{order['status'].upper()}**")

        # Если товар доставлен баером, покупатель может закрыть сделку
        if order['status'] == 'shipped':
            if st.button("✅ Подтвердить получение товара", key=f"confirm_del_{order['id']}"):
                res = change_offer_status(order['id'], "delivered")
                if res.ok:
                    st.success("Статус обновлен!")
                    st.rerun()
