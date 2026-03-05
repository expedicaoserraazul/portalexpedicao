# ==============================
# 🔥 BARRA FIXA REAL (FUNCIONA)
# ==============================

# Espaço para não cobrir conteúdo
st.markdown("<div style='height:170px'></div>", unsafe_allow_html=True)

# Container real do Streamlit
barra = st.container()

# CSS aplicado ao container correto
st.markdown(f"""
<style>
div[data-testid="stVerticalBlock"]:has(div.fixed-bar-marker) {{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: {cor_barra};
    padding: 20px 40px 25px 40px;
    z-index: 999999;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.4);
}}

.fixed-title {{
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
}}

section.main > div {{
    padding-bottom: 200px;
}}
</style>
""", unsafe_allow_html=True)

with barra:
    st.markdown("<div class='fixed-bar-marker'></div>", unsafe_allow_html=True)
    st.markdown("<div class='fixed-title'>ENVIAR TAREFA PARA :</div>", unsafe_allow_html=True)

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
