import requests
import streamlit as st

from frontend.api.client import get_error_message, register

st.header("Регистрация аккаунта")

with st.form("registration_form"):
    email = st.text_input("Почта (используется для входа)", key="registration_email")
    password = st.text_input(
        "Пароль",
        type="password",
        key="registration_password",
    )
    # Заменяем ФИО на Страну, чтобы соответствовать нашей схеме UserCreate
    country = st.text_input("Страна нахождения (например, Германия, США, Россия)", value="Russia", key="registration_country")
    submitted = st.form_submit_button("Зарегистрироваться")

if submitted:
    if not email.strip() or not password or not country.strip():
        st.error("Заполните все обязательные поля.")
        st.stop()

    try:
        response = register(
            email=email.strip(),
            password=password,
            country=country.strip(),
        )
    except requests.RequestException:
        st.error("Backend недоступен. Проверьте, запущен ли FastAPI.")
        st.stop()

    if response.status_code in (200, 201):
        st.success("Регистрация успешно выполнена! Теперь вы можете войти.")
        st.switch_page("pages/login.py")
    else:
        st.error(get_error_message(response))

st.page_link("pages/login.py", label="Уже есть аккаунт? Войти")
