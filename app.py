import streamlit as st
import hashlib

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Portal Expedição", layout="centered")

# =========================
# BANCO SIMPLES DE USUÁRIOS (etapa 1)
# depois migramos para banco real (PostgreSQL / Firebase)
# =========================
USERS = {
    "admin": {
        "name": "Administrador",
        "password": hashlib.sha256("123456".encode()).hexdigest(),
        "role": "admin"
    },
    "expedicao": {
        "name": "Usuário Expedição",
        "password": hashlib.sha256("exp123".encode()).hexdigest(),
        "role": "user"
    }
}

# =========================
# FUNÇÕES
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    user = USERS.get(username)
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
# LOGIN SCREEN
# =========================
if not st.session_state.authenticated:
    st.title("🔐 Portal Expedição")
    st.subheader("Acesso ao sistema")

    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

        if submit:
            user = login(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.username = username
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

# =========================
# SISTEMA (PÓS-LOGIN)
# =========================
else:
    st.sidebar.title("📂 Menu")
    st.sidebar.write(f"Usuário: **{st.session_state.user['name']}**")
    st.sidebar.write(f"Perfil: **{st.session_state.user['role']}**")

    menu = st.sidebar.radio(
        "Navegação",
        ["Home", "Painel", "Configurações"]
    )

    if st.sidebar.button("🚪 Sair"):
        logout()

    # ===== TELAS =====
    if menu == "Home":
        st.title("🏠 Home")
        st.write("Bem-vindo ao Portal de Expedição")
        st.info("Sistema autenticado e operacional.")

    elif menu == "Painel":
        st.title("📊 Painel")
        st.write("Área principal do sistema")
        st.success("Pronto para receber módulos de negócio")

    elif menu == "Configurações":
        st.title("⚙️ Configurações")

        if st.session_state.user["role"] != "admin":
            st.error("Acesso restrito ao administrador")
        else:
            st.success("Área administrativa")
            st.write("Gestão de usuários, permissões e sistema")
