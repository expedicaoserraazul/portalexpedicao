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

# ==============================================
# TELA PRINCIPAL
# ==============================================

def tela_tarefa(usuario="prevenção", loja="Loja 01"):

    st.title("AUTORIZAR RECEBIMENTO DE MERCADORIAS")

    # =====================================================
    # 🔥 ALTERAÇÃO 1 + 2 — BARRA FIXA COM COR DINÂMICA
    # =====================================================

    cores_setor = {
        "expedição": "#1f77b4",
        "compras": "#ff7f0e",
        "cadastro": "#2ca02c",
        "prevenção": "#d62728",
        "uso e consumo": "#9467bd"
    }

    cor_barra = cores_setor.get(usuario.lower(), "#0e1117")

    st.markdown(f"""
    <style>
    .footer-fixo {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: {cor_barra};
        padding: 15px 30px;
        z-index: 9999;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.4);
    }}

    .footer-fixo button {{
        width: 100%;
    }}

    section.main > div {{
        padding-bottom: 140px;
    }}
    </style>
    """, unsafe_allow_html=True)

    fornecedores_db = load("fornecedores") or {}

    st.markdown(f"**Prevenção:** {usuario}")
    st.markdown(f"**Loja:** {loja}")
    st.markdown("---")

    # ==============================
    # BLOCO 1
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

    st.text_input("Notas (informar números separados por vírgula)")

    for nome in selecionados:

        st.markdown("---")

        if nome == "Outros":
            st.subheader(fornecedor_outro if fornecedor_outro else "Fornecedor (Outros)")
            continue

        dados = fornecedores_db.get(nome, {})

        razao_social = dados.get("razao_social") or nome
        st.subheader(razao_social)

        divisao = dados.get("divisao", "-")
        prazo = dados.get("condicao_pagamento", 0)

        venc_normal = calcular_vencimento(prazo)

        prazo_estendido = 3 if dados.get("prazo_estendido_flags") else 0
        venc_estendido = calcular_vencimento(int(prazo) + int(prazo_estendido))

        st.write(f"Divisão: {divisao}")
        st.write(f"Prazo: {prazo} dias")
        st.write(f"Venc Normal: {formatar_data(venc_normal)}")
        st.write(f"Venc Estendido: {formatar_data(venc_estendido)}")

    # ==============================
    # Categorias
    # ==============================

    st.markdown("---")
    st.subheader("Categorias")
    st.multiselect("Selecione categorias", CATEGORIAS)

    st.subheader("Pendências")
    st.multiselect("Selecione pendências", PENDENCIAS)

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
    # Divergências
    # ==============================

    st.markdown("---")
    st.subheader("Divergências")

    for div in DIVERGENCIAS:
        if st.checkbox(div):
            st.text_input(f"Informar NF - {div}")
            st.file_uploader(f"Anexar arquivo - {div}")

    # ==============================
    # Anexos
    # ==============================

    st.markdown("---")
    st.subheader("Anexar Notas para Autorizar Recebimento")
    st.file_uploader("Upload de notas", accept_multiple_files=True)

    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

    # ==============================
    # 🔥 BOTÕES FIXOS
    # ==============================

    st.markdown('<div class="footer-fixo">', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.button("Enviar para Expedição")

    with col2:
        st.button("Enviar para Compras")

    with col3:
        st.button("Enviar para Cadastro")

    with col4:
        st.button("Enviar para Prevenção")

    with col5:
        st.button("Enviar para Uso e Consumo")

    st.markdown('</div>', unsafe_allow_html=True)

    if usuario.lower() == "prevenção":
        if st.button("FINALIZAR TAREFA"):
            st.success("Tarefa finalizada e enviada ao Financeiro")
