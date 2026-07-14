import streamlit as st


def save_auth(access_token: str, profile: dict) -> None:
    st.session_state["access_token"] = access_token
    st.session_state["profile"] = profile


def clear_auth() -> None:
    st.session_state.pop("access_token", None)
    st.session_state.pop("profile", None)


def is_authenticated() -> bool:
    return bool(st.session_state.get("access_token"))


def current_profile() -> dict | None:
    return st.session_state.get("profile")


def is_admin() -> bool:
    profile = current_profile()
    return bool(profile and profile.get("role") == "admin")


def is_buyer() -> bool:
    """Проверка, является ли текущий пользователь подтвержденным баером"""
    profile = current_profile()
    return bool(profile and profile.get("role") == "buyer")


def require_login() -> None:
    if is_authenticated():
        return

    st.warning("Сначала войдите в аккаунт.")
    if st.button("Перейти ко входу", key="require_login_button"):
        st.switch_page("pages/login.py")
    st.stop()


def require_admin() -> None:
    require_login()

    if not is_admin():
        st.error("Эта страница доступна только администратору.")
        st.stop()


def require_buyer() -> None:
    """Ограничение доступа для страниц, предназначенных только для баеров"""
    require_login()

    if not is_buyer() and not is_admin():
        st.error("Эта страница доступна только верифицированным баерам.")
        st.stop()
