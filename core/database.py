from supabase import create_client
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

def criar_usuario(email, senha):

    try:
        resposta = supabase.auth.sign_up({
            "email": email,
            "password": senha
        })

        return {
            "ok": True,
            "data": resposta
        }

    except Exception as erro:

        return {
            "ok": False,
            "erro": str(erro)
        }


def login_usuario(email, senha):

    try:
        resposta = supabase.auth.sign_in_with_password({
            "email": email,
            "password": senha
        })

        return {
            "ok": True,
            "data": resposta
        }

    except Exception as erro:

        return {
            "ok": False,
            "erro": str(erro)
        }