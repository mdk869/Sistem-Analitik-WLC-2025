# helper_auth.py
import streamlit as st
import hashlib

# Anda boleh simpan hash password terus di sini untuk auth manual
ADMIN_CREDENTIALS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
}

def check_admin_auth(username, password):
    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    return ADMIN_CREDENTIALS.get(username) == hashed_input
