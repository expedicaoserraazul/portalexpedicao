import streamlit as st
import hashlib
from database.manager import load, insert

# =========================
# SEGURANÇA
# =========================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# AUTENTICAÇÃO
# =========================
def authenticate(username, password):
    users = load("users")
    user = users.get(username)

    if not user:
        return None

    if user["password"] == hash_password(password):
        return user

    return None

# =========================
# LOGIN SCREEN
# =========================
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
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

# =========================
# CADASTRO DE USUÁRIOS
# =========================
def cadastro_usuario():
    st.subheader("👥 Cadastro de Usuários")

    with st.form("cadastro_usuario_form"):
        nome = st.text_input("Nome")
        cargo = st.text_input("Cargo")
        setor = st.text_input("Setor")
        user = st.text_input("Usuário (login)")
        senha = st.text_input("Senha", type="password")
        role = st.selectbox("Perfil", ["user", "admin"])

        submit = st.form_submit_button("Cadastrar")

        if submit:
            users = load("users")

            if user in users:
                st.error("Usuário já existe")
                return

            novo_user = {
                "name": nome,
                "cargo": cargo,
                "setor": setor,
                "password": hash_password(senha),
                "role": role,
                "permissoes": ["ALL"] if role == "admin" else ["HOME", "FORNECEDORES"]
            }

            insert("users", user, novo_user)

            st.success("Usuário cadastrado com sucesso!")
            st.rerun()
