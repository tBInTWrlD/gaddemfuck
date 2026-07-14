import streamlit as st
from auth.state import is_authenticated, is_admin, is_buyer, current_profile

st.set_page_config(
    page_title="Реверс-Маркетплейс",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Международный Реверс-Маркетплейс")
st.markdown("""
### Добро пожаловать в проект типа «Авито Наоборот»!
Здесь **покупатели** выкладывают то, что они ищут, а профессиональные **баеры** привозят эти товары из-за границы.
""")

st.divider()

# Навигационный блок в теле главной страницы для удобства
col1, col2 = st.columns(2)

with col1:
    st.info("### 🛍️ Для Покупателей")
    st.write("Изучите каталог готовых товаров, выберите нужный бренд или модель и оставьте заявку со своей ценой.")
    st.page_link("pages/catalog.py", label="Открыть каталог товаров", icon="📦")

with col2:
    st.success("### 🚚 Для Баеров")
    st.write("Загляните в ленту активных запросов от пользователей, оцените условия и предложите свою цену доставки.")
    st.page_link("pages/requests.py", label="Смотреть ленту запросов покупателей", icon="🛒")

st.divider()

# Показываем статус авторизации прямо на главной странице
if is_authenticated():
    profile = current_profile()
    email = profile.get("email") if profile else "пользователь"
    st.write(f"Вы вошли как: **{email}**")
    st.page_link("pages/profile.py", label="Перейти в Личный кабинет", icon="👤")
else:
    st.warning("Вы не авторизованы. Войдите, чтобы создавать запросы или отправлять предложения.")
    st.page_link("pages/login.py", label="Войти в аккаунт", icon="🔓")
