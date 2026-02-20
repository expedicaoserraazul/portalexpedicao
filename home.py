import streamlit as st

def render(user):
    st.title("📦 Portal de Expedição")

    st.success(f"Bem-vindo, {user['name']}")

    st.write("**Cargo:**", user["cargo"])
    st.write("**Setor:**", user["setor"])
    st.write("**Perfil:**", user["role"])

    st.divider()

    if st.button("Sair"):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.rerun()
