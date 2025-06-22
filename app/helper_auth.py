# app/helper_auth.py
import streamlit as st

def check_login():
    """Login asas menggunakan kombinasi username & password."""
    # Guna session_state untuk kekalkan status login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Jika belum login, papar borang login
    if not st.session_state.logged_in:
        st.subheader("🔐 Login Admin")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.button("Log Masuk")

        if login:
            # Gantikan dengan username/password sebenar anda
            if username == "admin" and password == "wlc2025":
                st.session_state.logged_in = True
                st.success("✅ Login berjaya!")
            else:
                st.error("❌ Username atau password salah.")

    return st.session_state.logged_in
