import streamlit as st

# BARRA FIXA INFERIOR
st.markdown("""
<style>

.barra-envio {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #ffffff;
    border-top: 1px solid #ddd;
    padding: 12px 0;
    z-index: 9999;
}

.barra-conteudo {
    margin-left: 8cm; /* MOVE OS BOTÕES 8CM PARA DIREITA */
    display: flex;
    align-items: center;
    gap: 12px;
}

.texto-envio {
    font-weight: bold;
    font-size: 16px;
}

.botao-expedicao button{
    background-color: #2E86C1;
    color: white;
}

.botao-compras button{
    background-color: #27AE60;
    color: white;
}

.botao-cadastro button{
    background-color: #8E44AD;
    color: white;
}

.botao-prevencao button{
    background-color: #D35400;
    color: white;
}

.botao-uso button{
    background-color: #16A085;
    color: white;
}

.botao-finalizar button{
    background-color: #C0392B;
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="barra-envio"><div class="barra-conteudo">', unsafe_allow_html=True)

st.markdown('<div class="texto-envio">ENVIAR TAREFA PARA :</div>', unsafe_allow_html=True)

col1,col2,col3,col4,col5,col6 = st.columns(6)

with col1:
    st.markdown('<div class="botao-expedicao">', unsafe_allow_html=True)
    if st.button("Expedição"):
        enviar_para("Expedição")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="botao-compras">', unsafe_allow_html=True)
    if st.button("Compras"):
        enviar_para("Compras")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="botao-cadastro">', unsafe_allow_html=True)
    if st.button("Cadastro"):
        enviar_para("Cadastro")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="botao-prevencao">', unsafe_allow_html=True)
    if st.button("Prevenção"):
        enviar_para("Prevenção")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="botao-uso">', unsafe_allow_html=True)
    if st.button("Uso e Consumo"):
        enviar_para("Uso e Consumo")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="botao-finalizar">', unsafe_allow_html=True)
    if st.button("Finalizar Tarefa"):
        finalizar_tarefa()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
