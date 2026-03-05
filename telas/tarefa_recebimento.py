import streamlit as st
from datetime import datetime, timedelta
from dal.manager import load

# =========================================
# LISTAS
# =========================================

CATEGORIAS = [
    "Açougue","Bebidas","Cadastro","Commodities","Hortifruti","Hplu",
    "Mercearia salgada","Mercearias doce","Padaria","Perecíveis","Uso e consumo"
]

PENDENCIAS = [
    "Cadastro","Condições de pagamento","Custo","Nota 100% sem pedido",
    "Nota devolvida","Quantidade acima","Sem pedido","Tributação"
]

DIVERGENCIAS = [
    "DIVERGÊNCIA DE RELACIONAMENTO",
    "DIVERGÊNCIA DE ITEM FORA DO MIX DA LOJA",
    "DIVERGÊNCIA DE ITEM SEM PEDIDO",
    "DIVERGÊNCIA DE CUSTO",
    "DIVERGÊNCIA DE QUANTIDADE ACIMA DO PEDIDO",
    "DIVERGÊNCIA DE CONDIÇÃO PAGAMENTO DA NOTA X COND. NEGOCIADA NO PEDIDO",
    "DIVERGÊNCIA DE PRAZO DE PAGAMENTO X DATA DE EMISSÃO DA NOTA",
    "DIVERGÊNCIA ABAIXO DA CONDIÇÃO PAGAMENTO AUTORIZADO PELA CONTROLADORIA",
    "DIVERGÊNCIA DE NOTA COM PEDIDO BLOQUEADO",
    "DIVERGÊNCIA DE NOTA COM PEDIDO SEM SALDO",
    "DIVERGÊNCIA DE NOTA COM PEDIDO EXPIRADO",
    "DIVERGÊNCIA DE NOTA 100% SEM PEDIDO",
    "DIVERGÊNCIA DE ITEM BONIFICADO SEM PEDIDO",
    "DIVERGÊNCIA DE NOTA DE BONIFICAÇÃO 100% SEM PEDIDO"
]

# =========================================
# FUNÇÕES
# =========================================

def calcular_vencimento(dias):
    return datetime.now().date() + timedelta(days=int(dias))


def formatar_data(data_obj):

    if not data_obj:
        return "-"

    if isinstance(data_obj, str):
        try:
            data_obj = datetime.fromisoformat(data_obj).date()
        except:
            return data_obj

    return data_obj.strftime("%d/%m/%y")


# =========================================
# TELA PRINCIPAL
# =========================================

def tela_tarefa(usuario="prevenção", loja="Loja 01"):

    st.set_page_config(layout="wide")

    st.title("AUTORIZAR RECEBIMENTO DE MERCADORIAS")

    # =========================================
    # CORES POR SETOR
    # =========================================

    cores_setor = {
        "expedição": "#1f77b4",
        "compras": "#ff7f0e",
        "cadastro": "#2ca02c",
        "prevenção": "#d62728",
        "uso e consumo": "#9467bd",
        "admin": "#0d6efd"
    }

    cor_barra = cores_setor.get(usuario.lower(), "#111111")

    # =========================================
    # CSS DA BARRA FIXA
    # =========================================

    st.markdown(f"""
    <style>

    .block-container {{
        padding-bottom:140px;
    }}

    .barra-fixa {{
        position:fixed;
        bottom:0;
        left:0;
        width:100%;
        background:{cor_barra};
        padding:18px;
        z-index:9999;
        box-shadow:0 -4px 15px rgba(0,0,0,0.4);
    }}

    .texto-envio {{
        color:white;
        font-weight:bold;
        margin-bottom:10px;
    }}

    </style>
    """, unsafe_allow_html=True)

    fornecedores_db = load("fornecedores") or {}

    st.markdown(f"**Usuário:** {usuario}")
    st.markdown(f"**Loja:** {loja}")
    st.markdown("---")

    # =========================================
    # FORNECEDORES
    # =========================================

    fornecedores_nomes = list(fornecedores_db.keys())

    selecionados = st.multiselect(
        "Fornecedor",
        fornecedores_nomes + ["Outros"]
    )

    if "Outros" in selecionados:
        st.text_input("Nome fornecedor (Outros)")

    st.text_input("Notas (separadas por vírgula)")

    for nome in selecionados:

        st.markdown("---")

        if nome == "Outros":
            st.subheader("Fornecedor (Outros)")
            continue

        dados = fornecedores_db.get(nome, {})

        razao_social = dados.get("razao_social") or nome
        prazo = dados.get("condicao_pagamento", 0)

        venc_normal = calcular_vencimento(prazo)

        st.subheader(razao_social)
        st.write(f"Prazo: {prazo} dias")
        st.write(f"Vencimento: {formatar_data(venc_normal)}")

    # =========================================
    # CATEGORIAS
    # =========================================

    st.markdown("---")

    st.subheader("Categorias")

    st.multiselect(
        "Selecione categorias",
        CATEGORIAS
    )

    st.subheader("Pendências")

    st.multiselect(
        "Selecione pendências",
        PENDENCIAS
    )

    # =========================================
    # DIVERGÊNCIAS
    # =========================================

    st.markdown("---")

    st.subheader("Divergências")

    for div in DIVERGENCIAS:

        if st.checkbox(div):

            st.text_input(f"Informar NF - {div}")
            st.file_uploader(f"Anexar - {div}")

    # =========================================
    # BARRA FIXA
    # =========================================

    st.markdown('<div class="barra-fixa">', unsafe_allow_html=True)

    st.markdown(
        '<div class="texto-envio">ENVIAR TAREFA PARA :</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("Expedição", use_container_width=True):
            st.success("Tarefa enviada para Expedição")

    with col2:
        if st.button("Compras", use_container_width=True):
            st.success("Tarefa enviada para Compras")

    with col3:
        if st.button("Cadastro", use_container_width=True):
            st.success("Tarefa enviada para Cadastro")

    with col4:
        if st.button("Prevenção", use_container_width=True):
            st.success("Tarefa enviada para Prevenção")

    with col5:
        if st.button("Uso e Consumo", use_container_width=True):
            st.success("Tarefa enviada para Uso e Consumo")

    st.markdown('</div>', unsafe_allow_html=True)
