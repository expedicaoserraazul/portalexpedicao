import streamlit as st
import json
import os

# =========================
# CONFIG
# =========================
DB_PATH = "database"
DB_FILE = os.path.join(DB_PATH, "fornecedores.json")

# =========================
# BANCO
# =========================
def carregar_fornecedores():
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_fornecedores(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# TELA
# =========================
def tela_fornecedores():
    st.subheader("📋 Cadastro de Fornecedores")

    fornecedores = carregar_fornecedores()

    with st.form("form_fornecedor"):
        st.markdown("### 🏢 Dados do Fornecedor")
        nome = st.text_input("Nome do fornecedor")
        cnpj = st.text_input("CNPJ")
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")

        st.markdown("### 📍 Endereço")
        cep = st.text_input("CEP")
        logradouro = st.text_input("Logradouro")
        bairro = st.text_input("Bairro")
        numero = st.text_input("Número")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")

        submit = st.form_submit_button("💾 Cadastrar fornecedor")

    if submit:
        if not nome or not cnpj:
            st.error("Nome e CNPJ são obrigatórios.")
            return

        if cnpj in fornecedores:
            st.error("Fornecedor já cadastrado com esse CNPJ.")
            return

        fornecedores[cnpj] = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "endereco": {
                "cep": cep,
                "logradouro": logradouro,
                "bairro": bairro,
                "numero": numero,
                "cidade": cidade,
                "estado": estado
            }
        }

        salvar_fornecedores(fornecedores)
        st.success("Fornecedor cadastrado com sucesso!")
        st.rerun()

    st.divider()
    st.subheader("📦 Fornecedores cadastrados")

    if not fornecedores:
        st.info("Nenhum fornecedor cadastrado.")
    else:
        for cnpj, dados in fornecedores.items():
            with st.expander(f"🏢 {dados['nome']} — {cnpj}"):
                st.write(f"📧 Email: {dados.get('email','')}")
                st.write(f"📞 Telefone: {dados.get('telefone','')}")

                endereco = dados.get("endereco", {})
                st.markdown("**📍 Endereço:**")
                st.write(f"CEP: {endereco.get('cep','')}")
                st.write(f"Logradouro: {endereco.get('logradouro','')}")
                st.write(f"Bairro: {endereco.get('bairro','')}")
                st.write(f"Número: {endereco.get('numero','')}")
                st.write(f"Cidade: {endereco.get('cidade','')}")
                st.write(f"Estado: {endereco.get('estado','')}")
