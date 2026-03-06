import streamlit as st
from datetime import datetime, timedelta
from dal.manager import load


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


def calcular_vencimento_estendido(dias):
    return datetime.now().date() + timedelta(days=int(dias) + 7)


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

    cores_setor = {
        "expedição": "#1f77b4",
        "compras": "#ff7f0e",
        "cadastro": "#2ca02c",
        "prevenção": "#d62728",
        "uso e consumo": "#9467bd",
        "admin": "#0d6efd"
    }

    cor_barra = cores_setor.get(usuario.lower(), "#111111")

    st.markdown(f"""
    <style>

    .block-container {{
        padding-bottom:180px;
    }}

    .barra-envio {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: {cor_barra};
        padding: 18px;
        z-index: 9999;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.4);
    }}

    .barra-conteudo {{
        margin-left: 8cm;
        color:white;
        font-weight:bold;
        font-size:16px;
        display:flex;
        align-items:center;
        gap:15px;
        flex-wrap:wrap;
    }}

    .botao-barra {{
        background:white;
        color:black;
        border:none;
        padding:8px 14px;
        border-radius:6px;
        cursor:pointer;
        font-weight:bold;
    }}

    .botao-barra:hover {{
        background:#eeeeee;
    }}

    </style>
    """, unsafe_allow_html=True)

    fornecedores_db = load("fornecedores") or {}

    st.markdown(f"**Usuário:** {usuario}")
    st.markdown(f"**Loja:** {loja}")

    st.markdown("---")

    fornecedores_nomes = list(fornecedores_db.keys())

    selecionados = st.multiselect(
        "Fornecedor",
        fornecedores_nomes + ["Outros"]
    )

    if "Outros" in selecionados:
        st.text_input("Nome fornecedor (Outros)")

    notas_input = st.text_input("Notas (separadas por barra '/')")

    if notas_input:
        lista_notas = [n.strip() for n in notas_input.split("/") if n.strip()]

    st.file_uploader(
        "Anexar Notas para Autorizar Recebimento",
        type=["pdf","xml","jpg","png"],
        accept_multiple_files=True
    )

    for nome in selecionados:

        st.markdown("---")

        if nome == "Outros":
            st.subheader("Fornecedor (Outros)")
            continue

        dados = fornecedores_db.get(nome, {})
        razao_social = dados.get("razao_social") or nome
        prazo = dados.get("condicao_pagamento", 0)

        venc_normal = calcular_vencimento(prazo)
        venc_estendido = calcular_vencimento_estendido(prazo)

        st.subheader(razao_social)
        st.write(f"Prazo: {prazo} dias")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"Vencimento Normal: {formatar_data(venc_normal)}")

        with col2:
            st.warning(f"Vencimento Estendido: {formatar_data(venc_estendido)}")

    st.markdown("---")
    st.subheader("Categorias")
    st.multiselect("Selecione categorias", CATEGORIAS)

    st.subheader("Pendências")
    st.multiselect("Selecione pendências", PENDENCIAS)

    st.markdown("---")
    st.subheader("Mensagens")

    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    if "campo_mensagem" not in st.session_state:
        st.session_state.campo_mensagem = ""

    def adicionar_mensagem():

        texto = st.session_state.campo_mensagem.strip()

        if texto:
            st.session_state.mensagens.append({
                "usuario": usuario,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "texto": texto
            })

            st.session_state.campo_mensagem = ""

    st.text_area(
        "Escrever mensagem",
        key="campo_mensagem"
    )

    st.button(
        "Adicionar Mensagem",
        on_click=adicionar_mensagem
    )

    for msg in st.session_state.mensagens:
        st.write(f"[{msg['data']}] {msg['usuario']}: {msg['texto']}")

    st.markdown("---")
    st.subheader("Divergências")

    for div in DIVERGENCIAS:
        if st.checkbox(div):
            st.text_input(f"Informar NF - {div}")
            st.file_uploader(f"Anexar - {div}")

    st.markdown("---")

    st.file_uploader(
        "Anexar Devolução",
        type=["pdf","xml","jpg","png"],
        accept_multiple_files=True
    )

    st.markdown(f"""
    <div class="barra-envio">
        <div class="barra-conteudo">
            ENVIAR TAREFA PARA:
            <button class="botao-barra">Expedição</button>
            <button class="botao-barra">Compras</button>
            <button class="botao-barra">Cadastro</button>
            <button class="botao-barra">Prevenção</button>
            <button class="botao-barra">Uso e Consumo</button>
            <button class="botao-barra">Finalizar Tarefa</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
