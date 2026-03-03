import streamlit as st
from dal.manager import load, save

# ================================
# 📦 Cadastro de Fornecedor — Matriz e Filiais
# ================================

PRAZOS_FLAGS = [
    "3 dias dentro da cidade",
    "5 dias fora da cidade",
    "7 dias fora do estado"
]

UFS = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
    "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
    "RS","RO","RR","SC","SP","SE","TO"
]


def tela_fornecedores():
    st.title("🏭 Cadastro de Fornecedores")

    fornecedores = load("fornecedores")

    if "filiais_temp" not in st.session_state:
        st.session_state.filiais_temp = []

    st.subheader("➕ Novo fornecedor")

    # ================================
    # Dados principais
    # ================================
    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome do fornecedor")
        cnpj_matriz = st.text_input("CNPJ Matriz")
        divisao = st.text_input("Divisão")
        comprador = st.text_input("Comprador")

    with col2:
        condicao_pag = st.number_input("Condição de pagamento (dias)", min_value=0, step=1)
        prazo_flags = st.multiselect("Prazo estendido", PRAZOS_FLAGS)

    # ================================
    # Endereço da Matriz
    # ================================
    st.markdown("---")
    st.subheader("📍 Endereço da Matriz")

    col_end1, col_end2 = st.columns(2)

    with col_end1:
        cep = st.text_input("CEP")
        logradouro = st.text_input("Logradouro")
        numero = st.text_input("Número")
        complemento = st.text_input("Complemento")

    with col_end2:
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.selectbox("Estado (UF)", UFS)

    # ================================
    # Filiais
    # ================================
    st.markdown("---")
    st.subheader("🏢 Filiais")

    with st.expander("Adicionar filial"):
        filial_nome = st.text_input("Nome da filial")
        filial_cnpj = st.text_input("CNPJ da filial")

        if st.button("Adicionar filial"):
            if filial_nome and filial_cnpj:
                st.session_state.filiais_temp.append({
                    "nome": filial_nome,
                    "cnpj": filial_cnpj
                })
                st.success("Filial adicionada")
                st.rerun()
            else:
                st.error("Informe nome e CNPJ da filial")

    if st.session_state.filiais_temp:
        st.markdown("**Filiais adicionadas:**")
        for i, filial in enumerate(st.session_state.filiais_temp):
            col_a, col_b = st.columns([4,1])
            with col_a:
                st.write(f"{filial['nome']} - {filial['cnpj']}")
            with col_b:
                if st.button("❌", key=f"del_filial_{i}"):
                    st.session_state.filiais_temp.pop(i)
                    st.rerun()

    # ================================
    # Salvamento
    # ================================
    if st.button("💾 Salvar fornecedor"):
        if not nome or not cnpj_matriz:
            st.error("Nome e CNPJ Matriz são obrigatórios")
        else:
            fornecedores[nome] = {
                "nome": nome,
                "cnpj_matriz": cnpj_matriz,
                "divisao": divisao,
                "comprador": comprador,
                "condicao_pagamento": condicao_pag,
                "prazo_estendido_flags": prazo_flags,
                "endereco_matriz": {
                    "cep": cep,
                    "logradouro": logradouro,
                    "numero": numero,
                    "complemento": complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado
                },
                "filiais": st.session_state.filiais_temp
            }

            save("fornecedores", fornecedores)
            st.session_state.filiais_temp = []
            st.success("Fornecedor salvo com matriz e filiais")
            st.rerun()

    # ================================
    # Listagem
    # ================================
    st.divider()
    st.subheader("📋 Fornecedores cadastrados")

    if not fornecedores:
        st.info("Nenhum fornecedor cadastrado")
        return

    for k, f in fornecedores.items():
        with st.expander(f"🏭 {f.get('nome','')} - {f.get('cnpj_matriz','')}"):
            st.write(f"**Divisão:** {f.get('divisao','')}")
            st.write(f"**Comprador:** {f.get('comprador','')}")
            st.write(f"**Condição de pagamento:** {f.get('condicao_pagamento',0)} dias")
            st.write(f"**Prazo estendido:** {', '.join(f.get('prazo_estendido_flags',[]))}")

            endereco = f.get("endereco_matriz", {})
            st.markdown("**Endereço Matriz:**")
            st.write(
                f"{endereco.get('logradouro','')}, {endereco.get('numero','')} - {endereco.get('bairro','')}"
            )
            st.write(
                f"{endereco.get('cidade','')} - {endereco.get('estado','')} | CEP: {endereco.get('cep','')}"
            )

            filiais = f.get("filiais", [])
            if filiais:
                st.markdown("**Filiais:**")
                for filial in filiais:
                    st.write(f"- {filial.get('nome')} - {filial.get('cnpj')}")

            if st.button("🗑 Excluir", key=f"del_{k}"):
                del fornecedores[k]
                save("fornecedores", fornecedores)
                st.rerun()

