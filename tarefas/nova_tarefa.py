from services.calculo_prazos import calcular_vencimentos
from dal.fornecedores import get_fornecedor_por_id
import streamlit as st

def tela_nova_tarefa():

    st.title("📋 Nova Tarefa")

    fornecedor_id = st.selectbox(
        "Fornecedor",
        options=lista_ids_fornecedores(),  # função que você já tem
        format_func=lambda x: nome_fornecedor(x)
    )

    if fornecedor_id:
        fornecedor = get_fornecedor_por_id(fornecedor_id)

        condicao = fornecedor["condicao_pagamento"]
        prazo_flag = fornecedor["prazo_estendido"]

        calculo = calcular_vencimentos(condicao, prazo_flag)

        st.subheader("📌 Dados Financeiros Importados")

        st.write(f"🧾 Condição de pagamento: {condicao}")
        st.write(f"🚚 Prazo estendido: {prazo_flag}")

        st.divider()

        st.write(f"📅 Data base: {calculo['data_base']}")
        st.write(f"📆 Vencimento normal: {calculo['vencimento_normal']}")
        st.write(f"📦 Dias extras: {calculo['dias_extra']}")
        st.success(f"📆 Vencimento com prazo estendido: {calculo['vencimento_estendido']}")

        # Persistência futura
        st.session_state["financeiro_tarefa"] = calculo
