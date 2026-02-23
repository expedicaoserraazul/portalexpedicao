import streamlit as st
from admin.usuarios import tela_usuarios
from admin.permissoes import tela_permissoes
from admin.modulos import tela_modulos
from admin.configuracoes import tela_configuracoes

def painel_admin():
    st.title("🛠 Painel Administrativo")

    abas = st.tabs([
        "👥 Usuários",
        "🔐 Permissões",
        "🧩 Módulos",
        "⚙️ Configurações"
    ])

    with abas[0]:
        tela_usuarios()

    with abas[1]:
        tela_permissoes()

    with abas[2]:
        tela_modulos()

    with abas[3]:
        tela_configuracoes()
