import streamlit as st
from database.manager import load, insert
import hashlib

# ---------- CONSTANTES ----------
LOJAS = [
    "São Geraldo",
    "Conselheiro",
    "Olaria",
    "Mury",
    "Teresópolis",
    "Cordeiro",
    "Centro NF",
    "Bom Jardim",
    "Todas"
]

# ---------- SEGURANÇA ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- TELA ----------
def tela_usuarios():
    st.subheader("👥 Gestão de Usuários")

    users = load("users")

    abas = st.tabs(["➕ Cadastrar Usuário", "📋 Usuários Cadastrados"])

    # ===============================
    # ABA 1 — CADASTRO
    # ===============================
    with abas[0]:
        st.markdown("### Cadastro de novo usuário")

        with st.form("form_cadastro_usuario"):
            nome = st.text_input("Nome")
            cargo = st.text_input("Cargo")
            setor = st.text_input("Setor")
            usuario = st.text_input("Usuário (login)")
            senha = st.text_input("Senha", type="password")

            role = st.selectbox("Perfil", ["user", "admin"])

            lojas = st.multiselect(
                "Lojas permitidas",
                LOJAS,
                default=[]
            )

            submit = st.form_submit_button("Cadastrar usuário")

            if submit:
                if not all([nome, cargo, setor, usuario, senha]):
                    st.error("Preencha todos os campos obrigatórios")
                    return

                if not lojas:
                    st.error("Selecione pelo menos uma loja")
                    return

                if usuario in users:
                    st.error("Usuário já existe")
                    return

                # Regra: se marcar "Todas", ignora as outras
                if "Todas" in lojas:
                    lojas = ["Todas"]

                novo_user = {
                    "name": nome,
                    "cargo": cargo,
                    "setor": setor,
                    "role": role,
                    "lojas": lojas,
                    "password": hash_password(senha)
                }

                insert("users", usuario, novo_user)

                st.success("Usuário cadastrado com sucesso!")
                st.rerun()

    # ===============================
    # ABA 2 — LISTAGEM
    # ===============================
    with abas[1]:
        st.markdown("### Usuários do sistema")

        if not users:
            st.info("Nenhum usuário cadastrado")
        else:
            for u, data in users.items():
                with st.expander(f"👤 {data['name']} ({u})"):
                    st.write(f"**Cargo:** {data['cargo']}")
                    st.write(f"**Setor:** {data['setor']}")
                    st.write(f"**Perfil:** {data['role']}")
                    st.write(f"**Lojas:** {', '.join(data.get('lojas', []))}")
