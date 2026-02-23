import streamlit as st
import json
import os
import uuid

DB_FILE = "database/fornecedores.json"

# =========================
# BANCO
# =========================
def load_fornecedores():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_fornecedores(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# TELA
# =========================
def tela_fornecedores():

    st.title("🏭 Cadastro de Fornecedores")

    fornecedores = load_fornecedores()

    st.subheader("➕ Novo fornecedor")

    with st.form("form_fornecedor"):
        razao = st.text_input("Razão Social")
        cnpj = st.text_input("CNPJ")
        endereco = st.text_input("Endereço")
        divisao = st.text_input("Divisão (ex: Padaria)")
        cond_pag = st.text_input("Condição de Pagamento (ex: 30 dias)")
        comprador = st.text_input("Comprador (ex: Fernando)")
        tolerancia = st.number_input("Tolerância de Prazo de Pagamento (dias)", min_value=0, step=1)

        submit = st.form_submit_button("Cadastrar fornecedor")

        if submit:
            if not razao or not cnpj:
                st.error("Razão Social e CNPJ são obrigatórios")
            else:
                fornecedor_id = str(uuid.uuid4())

                fornecedores[fornecedor_id] = {
                    "razao_social": razao,
                    "cnpj": cnpj,
                    "endereco": endereco,
                    "divisao": divisao,
                    "condicao_pagamento": cond_pag,
                    "comprador": comprador,
                    "tolerancia_pagamento": tolerancia
                }

                save_fornecedores(fornecedores)
                st.success("Fornecedor cadastrado com sucesso!")
                st.rerun()

    st.divider()

    # =========================
    # LISTAGEM
    # =========================
    st.subheader("📋 Fornecedores cadastrados")

    if not fornecedores:
        st.info("Nenhum fornecedor cadastrado.")
    else:
        for fid, f in fornecedores.items():
            with st.expander(f["razao_social"]):
                st.write(f"**CNPJ:** {f['cnpj']}")
                st.write(f"**Endereço:** {f['endereco']}")
                st.write(f"**Divisão:** {f['divisao']}")
                st.write(f"**Condição de pagamento:** {f['condicao_pagamento']}")
                st.write(f"**Comprador:** {f['comprador']}")
                st.write(f"**Tolerância:** {f['tolerancia_pagamento']} dias")
