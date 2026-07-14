import requests
import streamlit as st

from frontend.api.client import get_error_message, get_profile
from frontend.auth.state import clear_auth, require_login, save_auth, is_buyer

require_login()
st.header("Личный кабинет")

try:
    response = get_profile()
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

profile = response.json()
save_auth(st.session_state["access_token"], profile)

# Выводим обновленные поля нашей сущности User
st.write(f"**Почта:** {profile.get('email', 'Не указана')}")
st.write(f"**Страна нахождения:** {profile.get('country', 'Не указана')}")

role_mapping = {"user": "Покупатель", "buyer": "Баер (Доставщик)", "admin": "Администратор"}
current_role = profile.get('role', 'user')
st.write(f"**Ваш статус на платформе:** {role_mapping.get(current_role, current_role)}")

st.divider()

# Разводящие кнопки для сделок в зависимости от роли
if is_buyer():
    st.subheader("Управление заказами баера")
    st.page_link("pages/deliveries.py", label="📦 Посмотреть заказы в работе (Что мне нужно привезти)", icon="🚚")
else:
    st.subheader("Управление вашими заказами")
    st.page_link("pages/purchases.py", label="🛍️ Мои покупки (Принятые предложения от баеров)", icon="🛒")

st.divider()

if st.button("Выйти из аккаунта", type="primary"):
    clear_auth()
    st.switch_page("pages/login.py")
