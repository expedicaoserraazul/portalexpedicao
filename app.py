import streamlit as st
import json
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "users_db.json")

# -------------------------
# Utils
# -------------------------

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    users = load_users()
    if username not in users:
        return False, None

    user = users[username]
    input_hash = hash_password(password)

    if input_hash == user["password"]:
        return True, user
    return False, None

# -------------------------
# Session
# -------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_data" not in st.session_state:
    st.session_state.user_data = None

# -------------------------
# UI
# -------------------------

st.set_page_config(page_title="Portal Expedição", layout="centered")

if not st.session_state.authenticated:
    st.title("🔐 Portal Expedição")
    st.subheader("Acesso ao sistema")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        ok, user_data = authenticate(username, password)

        if ok:
            st.session_state.authenticated = True
            st.session_state.user_data = user_data
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
else:
    import home
    home.render(st.session_state.user_data)
