import streamlit as st

from core.database import (

    criar_usuario,
    login_usuario,
    criar_carteira

)

def tela_login():

    st.title(
        "NEXUS AI TRADER"
    )

    menu = st.selectbox(

        "Acesso",

        [

            "Entrar",
            "Cadastrar"

        ]

    )

    email = st.text_input(
        "Email"
    )

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if menu=="Cadastrar":

        if st.button(
            "Criar Conta"
        ):

            user = criar_usuario(
                email,
                senha
            )

            try:

                uid = user.user.id

                criar_carteira(
                    uid
                )

                st.success(
                    "Conta criada"
                )

            except:

                st.error(
                    "Erro cadastro"
                )

    else:

        if st.button(
            "Entrar"
        ):

            user = login_usuario(
                email,
                senha
            )

            if user:

                st.session_state[
                    "user"
                ] = user.user

                st.rerun()

            else:

                st.error(
                    "Login inválido"
                )