import streamlit as st
from auth.login import login_screen
from cadastros.fornecedores import tela_fornecedores

st.set_page_config(page_title="Portal Expedição", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login_screen()
else:
    st.sidebar.title("📂 Menu")
    st.sidebar.write(f"👤 {st.session_state.user['name']}")
    st.sidebar.write(f"🏷️ {st.session_state.user['cargo']}")
    st.sidebar.write(f"🏢 {st.session_state.user['setor']}")
    st.sidebar.write(f"🔐 Perfil: {st.session_state.user['role']}")

    menu = st.sidebar.radio("Navegação", [
        "Home",
        "Administração",
        "Fornecedores",
        "Módulos",
        "Configurações"
    ])

    if st.sidebar.button("🚪 Sair"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    if menu == "Home":
        st.title("🏠 Home")
        st.success("Sistema autenticado")

    elif menu == "Administração":
        st.title("🛠 Painel Administrativo")
        st.write("Gestão do sistema")

    elif menu == "Fornecedores":
    tela_fornecedores()

    elif menu == "Módulos":
        st.title("🧩 Módulos do Sistema")

    elif menu == "Configurações":
        st.title("⚙️ Configurações do Sistema")

