import streamlit as st
import json
import hashlib
import os

DB_FILE = "users_db.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username: str, password: str):
    users = load_users()
    user = users.get(username)

    if not user:
        return False, None

    if user["password"] == hash_password(password):
        return True, user

    return False, None

def login_screen():
    st.title("🔐 Portal Expedição")
    st.subheader("Acesso ao sistema")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        success, user = authenticate(username, password)

        if success:
            st.session_state.authenticated = True
            st.session_state.user = user
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
