import streamlit as st
from auth.login import cadastro_usuario
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

    # =========================
    # ABA USUÁRIOS
    # =========================
    with abas[0]:
        st.subheader("👥 Gestão de Usuários")
        cadastro_usuario()   # <-- AQUI É O VÍNCULO REAL

    # =========================
    # ABA PERMISSÕES
    # =========================
    with abas[1]:
        tela_permissoes()

    # =========================
    # ABA MÓDULOS
    # =========================
    with abas[2]:
        tela_modulos()

    # =========================
    # ABA CONFIGURAÇÕES
    # =========================
    with abas[3]:
        tela_configuracoes()
