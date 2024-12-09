import streamlit as st
def pooo():
    st.title("Página de Listas")
    st.write("Esta é a página de listas.")
    if st.button("Voltar à Home", use_container_width=True):
        st.session_state.page = "PaginaInicial"



