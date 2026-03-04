import streamlit as st
from datetime import datetime, timedelta
from dal.manager import load, save

# ==============================================
# 📝 TELA DE TAREFA
# AUTORIZAR RECEBIMENTO DE MERCADORIAS
# ==============================================

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
    return datetime.now().date() + timedelta(days=dias)


def tela_tarefa(usuario="prevenção", loja="Loja 01"):
    st.title("AUTORIZAR RECEBIMENTO DE MERCADORIAS")

    fornecedores_db = load("fornecedores")

    # ==============================
    # Cabeçalho automático
    # ==============================
    st.markdown(f"**Prevenção:** {usuario}")
    st.markdown(f"**Loja:** {loja}")

    st.markdown("---")

    # ==============================
    # BLOCO 1 - Fornecedores
    # ==============================
    st.subheader("Bloco 1")

    fornecedores_nomes = list(fornecedores_db.keys())

    selecionados = st.multiselect(
        "Fornecedor",
        fornecedores_nomes + ["Outros"]
    )

    fornecedor_outro = None
    if "Outros" in selecionados:
        fornecedor_outro = st.text_input("Nome fornecedor (Outros)")

    notas = st.text_input("Notas (informar números separados por vírgula)")

    # Renderizar blocos dinamicamente
    for i, nome in enumerate(selecionados):
        st.markdown("---")
        st.subheader(f"Fornecedor {i+1}")

        if nome == "Outros":
            st.write(f"Fornecedor: {fornecedor_outro}")
            continue

        dados = fornecedores_db.get(nome, {})
        divisao = dados.get("divisao", "-")
        prazo = dados.get("condicao_pagamento", 0)

        venc_normal = calcular_vencimento(prazo)

        prazo_estendido = 0
        if dados.get("prazo_estendido_flags"):
            prazo_estendido = 3  # placeholder (depois aplicar regra real)

        venc_estendido = calcular_vencimento(prazo + prazo_estendido)

        st.write(f"Divisão: {divisao}")
        st.write(f"Prazo: {prazo} dias")
        st.write(f"Venc Normal: {venc_normal}")
        st.write(f"Venc Estendido: {venc_estendido}")

    # ==============================
    # Categorias e Pendências
    # ==============================
    st.markdown("---")
    st.subheader("Categorias")
    categorias_sel = st.multiselect("Selecione categorias", CATEGORIAS)

    st.subheader("Pendências")
    pendencias_sel = st.multiselect("Selecione pendências", PENDENCIAS)

    # ==============================
    # Mensagens
    # ==============================
    st.markdown("---")
    st.subheader("Mensagens")

    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    nova_msg = st.text_area("Escrever mensagem")

    if st.button("Adicionar Mensagem"):
        if nova_msg:
            st.session_state.mensagens.append({
                "usuario": usuario,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "texto": nova_msg
            })
            st.rerun()

    for msg in st.session_state.mensagens:
        st.write(f"[{msg['data']}] {msg['usuario']}: {msg['texto']}")

    # ==============================
    # Divergências (Expedição)
    # ==============================
    st.markdown("---")
    st.subheader("Divergências")

    for div in DIVERGENCIAS:
        if st.checkbox(div):
            nf = st.text_input(f"Informar NF - {div}")
            arquivo = st.file_uploader(f"Anexar arquivo - {div}")

    # ==============================
    # Anexos gerais
    # ==============================
    st.markdown("---")
    st.subheader("Anexar Notas para Autorizar Recebimento")
    anexos = st.file_uploader("Upload de notas", accept_multiple_files=True)

    # ==============================
    # Botões de fluxo
    # ==============================
    st.markdown("---")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.button("Enviar para Expedição")
    col2.button("Enviar para Compras")
    col3.button("Enviar para Cadastro")
    col4.button("Enviar para Prevenção")
    col5.button("Enviar para Uso e Consumo")

    if usuario == "prevenção":
        if st.button("FINALIZAR TAREFA"):
            st.success("Tarefa finalizada e enviada ao Financeiro")
