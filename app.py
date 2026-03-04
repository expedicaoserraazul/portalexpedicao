import streamlit as st
from auth.login import login_screen
from cadastros.fornecedores import tela_fornecedores
from admin.painel import painel_admin
from security.authorization import modulos_permitidos
from telas.tarefa_recebimento import tela_tarefa

st.set_page_config(page_title="Portal Expedição", layout="centered")

# ---------- SESSION INIT ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ---------- LOGIN ----------
if not st.session_state.authenticated:
    login_screen()

# ---------- SISTEMA ----------
else:
    st.sidebar.title("📂 Menu")

    st.sidebar.write(f"👤 {st.session_state.user['name']}")
    st.sidebar.write(f"🏷️ {st.session_state.user['cargo']}")
    st.sidebar.write(f"🏢 {st.session_state.user['setor']}")
    st.sidebar.write(f"🔐 Perfil: {st.session_state.user['role']}")

    role = st.session_state.user["role"]

    # ---------- RBAC ----------
    modulos = modulos_permitidos(role)

    menu_labels = {
        "home": "Home",
        "admin": "Administração",
        "fornecedores": "Fornecedores",
        "tarefa_recebimento": "Autorizar Recebimento",
        "modulos": "Módulos",
        "configuracoes": "Configurações"
    }

    # Filtra apenas módulos permitidos
    menu_opcoes = [menu_labels[m] for m in modulos if m in menu_labels]

    menu = st.sidebar.radio(
        "Navegação",
        menu_opcoes
    )

    # ---------- LOGOUT ----------
    if st.sidebar.button("🚪 Sair"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # ---------- MENU ROUTER ----------
    label_to_key = {v: k for k, v in menu_labels.items()}
    menu_key = label_to_key[menu]

    # ---------- TELAS ----------
    if menu_key == "home":
        st.title("🏠 Home")
        st.success("Sistema autenticado")

    elif menu_key == "admin":
        painel_admin()

    elif menu_key == "fornecedores":
        tela_fornecedores()

    elif menu_key == "tarefa_recebimento":
        tela_tarefa(
            usuario=st.session_state.user["name"],
            loja=st.session_state.user.get("loja", "Loja não definida")
        )

    elif menu_key == "modulos":
        st.title("🧩 Módulos do Sistema")
        st.info("Gestão de módulos do sistema")

    elif menu_key == "configuracoes":
        st.title("⚙️ Configurações do Sistema")
        st.info("Configurações gerais da plataforma")
