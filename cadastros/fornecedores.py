import streamlit as st
import json
import os
from datetime import datetime

DB_FILE = "database/fornecedores.json"

def load_fornecedores():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_fornecedores(data):
    os.makedirs("database", exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def tela_fornecedores():

    st.title("🏭 Cadastro de Fornecedores")

    fornecedores = load_fornecedores()

    with st.form("form_fornecedor"):
        razao = st.text_input("Razão Social")
        cnpj = st.text_input("CNPJ")
        endereco = st.text_area("Endereço")
        divisao = st.text_input("Divisão (ex: Padaria)")
        cond_pg = st.text_input("Condição de Pagamento (ex: 30 dias)")
        comprador = st.text_input("Comprador responsável")
        tolerancia = st.number_input("Tolerância de prazo (dias)", min_value=0, step=1)

        submit = st.form_submit_button("Cadastrar fornecedor")

        if submit:
            if not razao or not cnpj:
                st.error("Razão Social e CNPJ são obrigatórios")
            else:
                fornecedores[cnpj] = {
                    "razao_social": razao,
                    "cnpj": cnpj,
                    "endereco": endereco,
                    "divisao": divisao,
                    "condicao_pagamento": cond_pg,
                    "comprador": comprador,
                    "tolerancia_dias": tolerancia,
                    "criado_em": datetime.now().isoformat()
                }
                save_fornecedores(fornecedores)
                st.success("Fornecedor cadastrado com sucesso!")
                st.rerun()

    st.divider()
    st.subheader("📋 Fornecedores cadastrados")

    if fornecedores:
        for f in fornecedores.values():
            st.markdown(f"""
**{f['razao_social']}**  
CNPJ: {f['cnpj']}  
Divisão: {f['divisao']}  
Condição: {f['condicao_pagamento']}  
Comprador: {f['comprador']}  
Tolerância: {f['tolerancia_dias']} dias  
--- 
""")
    else:
        st.info("Nenhum fornecedor cadastrado ainda.")
