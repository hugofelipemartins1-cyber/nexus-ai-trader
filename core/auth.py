import streamlit as st

from core.database import (
    criar_usuario,
    login_usuario
)

def tela_login():

    st.title("NEXUS AI TRADER")

    menu = st.selectbox(
        "Acesso",
        [
            "Entrar",
            "Cadastrar"
        ]
    )

    email = st.text_input("Email")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if menu == "Cadastrar":

        if st.button("Criar Conta"):

            if not email or not senha:

                st.error("Informe email e senha.")

                return

            resposta = criar_usuario(
                email,
                senha
            )

            if resposta["ok"]:

                st.success(
                    "Conta criada com sucesso. Agora selecione Entrar."
                )

            else:

                st.error(
                    f"Erro cadastro: {resposta['erro']}"
                )

    else:

        if st.button("Entrar"):

            resposta = login_usuario(
                email,
                senha
            )

            if resposta["ok"]:

                st.session_state["user"] = resposta["data"].user

                st.rerun()

            else:

                st.error(
                    f"Login inválido: {resposta['erro']}"
                )