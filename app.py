import streamlit as st
import hashlib
import json
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Portal Expedição", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "users_db.json")

# =========================
# BANCO
# =========================
def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# SEGURANÇA
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password, users):
    user = users.get(username)
    if not user:
        return False
    if user["password"] == hash_password(password):
        return user
    return False

def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# =========================
# SESSION INIT
# =========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# =========================
# LOAD USERS
# =========================
users_db = load_users()

# =========================
# LOGIN
# =========================
if not st.session_state.authenticated:
    st.title("🔐 Portal Expedição")
    st.subheader("Acesso ao sistema")

    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            user = login(username, password, users_db)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.username = username
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

# =========================
# SISTEMA
# =========================
else:
    st.sidebar.title("📂 Menu")
    st.sidebar.write(f"👤 {st.session_state.user['name']}")
    st.sidebar.write(f"🏷️ {st.session_state.user['cargo']}")
    st.sidebar.write(f"🏢 {st.session_state.user['setor']}")

    menu = st.sidebar.radio(
        "Navegação",
        ["Home", "Cadastro de Usuários", "Painel"]
    )

    if st.sidebar.button("🚪 Sair"):
        logout()

    # =========================
    # HOME
    # =========================
    if menu == "Home":
        st.title("🏠 Home")
        st.success("Sistema autenticado")
        st.info("Portal Expedição operacional")

    # =========================
    # CADASTRO DE USUÁRIOS
    # =========================
    elif menu == "Cadastro de Usuários":

        if st.session_state.user["role"] != "admin":
            st.error("Acesso restrito ao administrador")
        else:
            st.title("👥 Cadastro de Usuários")

            with st.form("user_form"):
                nome = st.text_input("Nome")
                cargo = st.text_input("Cargo")
                setor = st.text_input("Setor")
                user = st.text_input("Usuário (login)")
                senha = st.text_input("Senha", type="password")
                role = st.selectbox("Perfil", ["user", "admin"])

                submit = st.form_submit_button("Cadastrar")

                if submit:
                    if user in users_db:
                        st.error("Usuário já existe")
                    else:
                        users_db[user] = {
                            "name": nome,
                            "cargo": cargo,
                            "setor": setor,
                            "user": user,
                            "password": hash_password(senha),
                            "role": role
                        }
                        save_users(users_db)
                        st.success("Usuário cadastrado com sucesso!")
                        st.rerun()

    # =========================
    # PAINEL
    # =========================
    elif menu == "Painel":
        st.title("📊 Painel")
        st.write("Área operacional do sistema")
        st.success("Base pronta para workflows, tarefas e processos")
