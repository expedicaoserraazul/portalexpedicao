import streamlit as st
from datetime import datetime, timedelta
from dal.manager import load

# ==============================
# LISTAS
# ==============================

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

# ==============================
# FUNÇÕES AUXILIARES
# ==============================

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


# ==============================
# TELA PRINCIPAL
# ==============================

def tela_tarefa(usuario="prevenção", loja="Loja 01"):

    st.title("AUTORIZAR RECEBIMENTO DE MERCADORIAS")

    # ==============================
    # COR DINÂMICA POR SETOR
    # ==============================

    cores_setor = {
        "admin": "#0d6efd",
        "expedição": "#1f77b4",
        "compras": "#ff7f0e",
        "cadastro": "#2ca02c",
        "prevenção": "#d62728",
        "uso e consumo": "#9467bd"
    }

    usuario_normalizado = usuario.strip().lower()
    cor_barra = cores_setor.get(usuario_normalizado, "#111111")

    # ==============================
    # CSS GLOBAL
    # ==============================

    st.markdown(f"""
    <style>

    /* espaço para não cobrir conteúdo */
    .block-container {{
        padding-bottom: 200px;
    }}

    /* container da barra fixa */
    div[data-testid="stVerticalBlock"]:has(.barra-marker) {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: {cor_barra};
        padding: 20px 40px 25px 40px;
        z-index: 999999;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.4);
    }}

    .barra-titulo {{
        color: white;
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 16px;
    }}

    </style>
    """, unsafe_allow_html=True)

    fornecedores_db = load("fornecedores") or {}

    st.markdown(f"**Usuário:** {usuario}")
    st.markdown(f"**Loja:** {loja}")
    st.markdown("---")

    # ==============================
    # FORNECEDORES
    # ==============================

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

    # ==============================
    # CATEGORIAS
    # ==============================

    st.markdown("---")
    st.subheader("Categorias")
    st.multiselect("Selecione categorias", CATEGORIAS)

    st.subheader("Pendências")
    st.multiselect("Selecione pendências", PENDENCIAS)

    # ==============================
    # DIVERGÊNCIAS
    # ==============================

    st.markdown("---")
    st.subheader("Divergências")

    for div in DIVERGENCIAS:
        if st.checkbox(div):
            st.text_input(f"Informar NF - {div}")
            st.file_uploader(f"Anexar - {div}")

    # ==============================
    # BARRA FIXA REAL
    # ==============================

    barra = st.container()

    with barra:
        st.markdown("<div class='barra-marker'></div>", unsafe_allow_html=True)
        st.markdown("<div class='barra-titulo'>ENVIAR TAREFA PARA :</div>", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.button("Expedição", use_container_width=True)

        with col2:
            st.button("Compras", use_container_width=True)

        with col3:
            st.button("Cadastro", use_container_width=True)

        with col4:
            st.button("Prevenção", use_container_width=True)

        with col5:
            st.button("Uso e Consumo", use_container_width=True)
