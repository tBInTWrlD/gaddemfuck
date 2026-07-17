import streamlit as st
from auth.state import is_authenticated, is_admin, is_buyer, current_profile

# 1. Настройка страницы должна идти строго первой
st.set_page_config(
    page_title="Реверс-Маркетплейс",
    page_icon="✈️",
    layout="wide"
)

# 2. 🎈 Запускаем летящие шарики при каждой загрузке главной страницы!
st.balloons()

# --- Остальной код твоей главной страницы без изменений ---
st.title("✈️ Международный Реверс-Маркетплейс")
st.markdown("""
### Добро пожаловать в проект типа «Авито Наоборот»!
Здесь **покупатели** выкладывают то, что они ищут, а профессиональные **баеры** привозят эти товары из-за границы.
""")

st.divider()
st.divider()
st.markdown("### 🤫 Секретная зона")
st.page_link("pages/platypus.py", label="Посетить секретный штаб Паши Утконоса (Наш талисман)", icon="🦫")

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

if is_authenticated():
    profile = current_profile()
    email = profile.get("email") if profile else "пользователь"
    st.write(f"Вы вошли как: **{email}**")
    st.page_link("pages/profile.py", label="Перейти в Личный кабинет", icon="👤")
else:
    st.warning("Вы не авторизованы. Войдите, чтобы создавать запросы или отправлять предложения.")
    st.page_link("pages/login.py", label="Войти в аккаунт", icon="🔓")
