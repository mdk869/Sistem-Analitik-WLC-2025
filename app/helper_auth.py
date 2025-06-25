# app/helper_auth.py
import streamlit as st

# Database user asas (boleh upgrade ke Google Sheet atau database lain)
USER_CREDENTIALS = {
    "admin": {"password": "wlc2025", "role": "admin"},
    "organizer": {"password": "team2025", "role": "organizer"},
}

def check_login():
    """Login system with session state."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

    if st.session_state.logged_in:
        st.sidebar.success(f"✅ Selamat datang, {st.session_state.username.capitalize()}")
        if st.sidebar.button("🚪 Log Keluar"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.rerun()
    else:
        with st.sidebar:
            st.subheader("🔐 Login Admin")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login = st.button("Log Masuk")


        if login:
                user = USER_CREDENTIALS.get(username)
                if user and password == user["password"]:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = user["role"]
                    st.success("✅ Login berjaya!")
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah.")

    return st.session_state.logged_in
