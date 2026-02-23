import streamlit as st
import json
import os
import hashlib

DB_FILE = "database/users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def tela_usuarios():
    st.subheader("👥 Gestão de Usuários")

    users = load_users()

    st.markdown("### 📋 Usuários cadastrados")

    for username, data in users.items():
        with st.expander(f"👤 {data['name']} ({username})"):
            st.write(f"Cargo: {data['cargo']}")
            st.write(f"Setor: {data['setor']}")
            st.write(f"Perfil: {data['role']}")

    st.divider()
    st.markdown("### ➕ Criar novo usuário")

    with st.form("novo_usuario_admin"):
        nome = st.text_input("Nome")
        cargo = st.text_input("Cargo")
        setor = st.text_input("Setor")
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        role = st.selectbox("Perfil", ["user", "admin"])

        submit = st.form_submit_button("Cadastrar")

        if submit:
            if user in users:
                st.error("Usuário já existe")
            else:
                users[user] = {
                    "name": nome,
                    "cargo": cargo,
                    "setor": setor,
                    "user": user,
                    "password": hash_password(senha),
                    "role": role
                }
                save_users(users)
                st.success("Usuário criado com sucesso")
                st.rerun()
