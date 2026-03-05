import streamlit as st
from datetime import datetime, timedelta
from dal.manager import load, save

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


def tela_tarefa(usuario="prevenção", loja="Loja 01"):

    st.title("AUTORIZAR RECEBIMENTO DE MERCADORIAS")

    # ==============================
    # 🎨 COR DINÂMICA POR SETOR
    # ==============================

    cores_setor = {
        "expedição": "#1f77b4",
        "compras": "#ff7f0e",
        "cadastro": "#2ca02c",
        "prevenção": "#d62728",
        "uso e consumo": "#9467bd"
    }

    cor_barra = cores_setor.get(usuario.lower(), "#111111")

    # ==============================
    # 🔥 CSS FIXO REAL
    # ==============================

    st.markdown(f"""
    <style>

    .barra-inferior {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: {cor_barra};
        padding: 15px;
        display: flex;
        justify-content: space-around;
        z-index: 999999;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.4);
    }}

    .barra-inferior button {{
        background-color: white;
        color: black;
        padding: 10px 15px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        cursor: pointer;
    }}

    .main {{
        padding-bottom: 120px;
    }}

    </style>
    """, unsafe_allow_html=True)

    fornecedores_db = load("fornecedores") or {}

    st.markdown(f"**Usuário:** {usuario}")
    st.markdown(f"**Loja:** {loja}")
    st.markdown("---")

    # ==============================
    # BLOCO 1
    # ==============================

    fornecedores_nomes = list(fornecedores_db.keys())

    selecionados = st.multiselect(
        "Fornecedor",
        fornecedores_nomes + ["Outros"]
    )

    fornecedor_outro = None
    if "Outros" in selecionados:
        fornecedor_outro = st.text_input("Nome fornecedor (Outros)")

    st.text_input("Notas (separadas por vírgula)")

    for nome in selecionados:

        st.markdown("---")

        if nome == "Outros":
            st.subheader(fornecedor_outro if fornecedor_outro else "Fornecedor (Outros)")
            continue

        dados = fornecedores_db.get(nome, {})

        razao_social = dados.get("razao_social") or nome
        st.subheader(razao_social)

        prazo = dados.get("condicao_pagamento", 0)
        venc_normal = calcular_vencimento(prazo)

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
    # ESPAÇO RESERVA SCROLL
    # ==============================

    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

    # ==============================
    # 🔥 BARRA FIXA FUNCIONAL
    # ==============================

    st.markdown(f"""
    <div class="barra-inferior">
        <button>Expedição</button>
        <button>Compras</button>
        <button>Cadastro</button>
        <button>Prevenção</button>
        <button>Uso e Consumo</button>
    </div>
    """, unsafe_allow_html=True)
