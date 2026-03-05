import streamlit as st

st.set_page_config(layout="wide")

# Cor da barra inferior
cor_barra = "#f0f2f6"

# --- CSS ---
st.markdown(f"""
<style>

/* Espaço no final da página para não cobrir conteúdo */
.block-container {{
    padding-bottom:120px;
}}

/* Barra fixa inferior */
.barra-envio {{
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    background:{cor_barra};
    padding:15px 20px;
    z-index:9999;
    box-shadow:0 -3px 10px rgba(0,0,0,0.15);
}}

/* Container interno da barra */
.barra-conteudo {{
    max-width:1200px;
    margin:auto;
    display:flex;
    align-items:center;
    gap:10px;
}}

/* Texto da barra */
.barra-texto {{
    font-weight:600;
    font-size:15px;
    color:#333;
}}

/* Botões */
.barra-botoes {{
    display:flex;
    gap:10px;
    flex:1;
}}

.barra-botoes button {{
    flex:1;
    padding:10px;
    border-radius:8px;
    border:none;
    background:#1f2937;
    color:white;
    font-weight:bold;
    cursor:pointer;
}}

.barra-botoes button:hover {{
    background:#374151;
}}

</style>
""", unsafe_allow_html=True)


# --- SIDEBAR ---
st.sidebar.title("Menu")
st.sidebar.write("Exemplo de menu lateral")
st.sidebar.button("Opção 1")
st.sidebar.button("Opção 2")


# --- CONTEÚDO PRINCIPAL ---
st.title("Sistema de Tarefas")

st.write("Conteúdo da página...")
st.write("Role a página para testar a barra fixa.")

for i in range(30):
    st.write("Linha de exemplo", i)


# --- BARRA FIXA INFERIOR ---
st.markdown(f"""
<div class="barra-envio">
    <div class="barra-conteudo">

        <div class="barra-texto">
        Enviar tarefa para:
        </div>

        <div class="barra-botoes">
            <button>Fiscal</button>
            <button>Financeiro</button>
            <button>Compras</button>
            <button>TI</button>
        </div>

    </div>
</div>
""", unsafe_allow_html=True)
