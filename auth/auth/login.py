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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    users = load_users()
    user = users.get(username)

    if not user:
        return None

    if user["password"] == hash_password(password):
        return user

    return None

def login_screen():
    st.title("🔐 Portal Expedição")
    st.subheader("Acesso ao sistema")

    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            user = authenticate(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.username = username
                st.success("Login realizado com sucesso")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")
