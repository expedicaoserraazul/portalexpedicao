import streamlit as st
from dal.manager import load, save

# ================================
# 📦 Cadastro de Fornecedor — Atualizado com Endereço
# ================================

PRAZOS_FLAGS = [
    "3 dias dentro da cidade",
    "5 dias fora da cidade",
    "7 dias fora do estado"
]


def tela_fornecedores():
    st.title("🏭 Cadastro de Fornecedores")

    fornecedores = load("fornecedores")

    st.subheader("➕ Novo fornecedor")

    # ================================
    # Dados principais
    # ================================
    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome do fornecedor")
        cnpj = st.text_input("CNPJ")
        divisao = st.text_input("Divisão")
        comprador = st.text_input("Comprador")

    with col2:
        condicao_pag = st.number_input("Condição de pagamento (dias)", min_value=0, step=1)
        prazo_flags = st.multiselect("Prazo estendido", PRAZOS_FLAGS)

    # ================================
    # Endereço
    # ================================
    st.markdown("---")
    st.subheader("📍 Endereço")

    col_end1, col_end2 = st.columns(2)

    with col_end1:
        cep = st.text_input("CEP")
        logradouro = st.text_input("Logradouro")
        numero = st.text_input("Número")
        complemento = st.text_input("Complemento")

    with col_end2:
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        ufs = [
            "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
            "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
            "RS","RO","RR","SC","SP","SE","TO"
        ]
        estado = st.selectbox("Estado (UF)", ufs)

    # ================================
    # Salvamento
    # ================================
    if st.button("💾 Salvar fornecedor"):
        if not nome or not cnpj:
            st.error("Nome e CNPJ são obrigatórios")
        else:
            fornecedores[nome] = {
                "nome": nome,
                "cnpj": cnpj,
                "divisao": divisao,
                "comprador": comprador,
                "condicao_pagamento": condicao_pag,
                "prazo_estendido_flags": prazo_flags,
                "endereco": {
                    "cep": cep,
                    "logradouro": logradouro,
                    "numero": numero,
                    "complemento": complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado
                }
            }

            save("fornecedores", fornecedores)
            st.success("Fornecedor cadastrado com sucesso")
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
        with st.expander(f"🏭 {f.get('nome','')} - {f.get('cnpj','')}"):
            st.write(f"**Divisão:** {f.get('divisao','')}")
            st.write(f"**Comprador:** {f.get('comprador','')}")
            st.write(f"**Condição de pagamento:** {f.get('condicao_pagamento',0)} dias")
            st.write(f"**Prazo estendido:** {', '.join(f.get('prazo_estendido_flags',[]))}")

            endereco = f.get("endereco", {})

            st.markdown("**Endereço:**")
            st.write(
                f"{endereco.get('logradouro','')}, {endereco.get('numero','')} - {endereco.get('bairro','')}"
            )
            st.write(
                f"{endereco.get('cidade','')} - {endereco.get('estado','')} | CEP: {endereco.get('cep','')}"
            )
            if endereco.get("complemento"):
                st.write(f"Complemento: {endereco.get('complemento')}")

            col_a, col_b = st.columns(2)

            with col_a:
                if st.button("🗑 Excluir", key=f"del_{k}"):
                    del fornecedores[k]
                    save("fornecedores", fornecedores)
                    st.rerun()

            with col_b:
                st.caption("Edição será implementada na próxima etapa")

