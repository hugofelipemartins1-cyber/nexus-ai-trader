from supabase import create_client
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================
# USUARIO
# =========================

def criar_usuario(

    email,
    senha

):

    try:

        user = supabase.auth.sign_up({

            "email":email,
            "password":senha

        })

        return user

    except Exception as e:

        return str(e)

def login_usuario(

    email,
    senha

):

    try:

        user = supabase.auth.sign_in_with_password({

            "email":email,
            "password":senha

        })

        return user

    except Exception as e:

        return None

# =========================
# CARTEIRA
# =========================

def criar_carteira(

    usuario_id

):

    supabase.table(
        "carteiras"
    ).insert({

        "usuario_id":usuario_id,
        "saldo":100000,
        "lucro":0

    }).execute()

def buscar_carteira(

    usuario_id

):

    dados = supabase.table(
        "carteiras"
    ).select("*").eq(
        "usuario_id",
        usuario_id
    ).execute()

    return dados.data

# =========================
# OPERAÇÕES
# =========================

def salvar_operacao(

    usuario_id,
    ativo,
    entrada,
    stop,
    take,
    quantidade,
    status,
    pl

):

    supabase.table(
        "operacoes"
    ).insert({

        "usuario_id":usuario_id,
        "ativo":ativo,
        "entrada":entrada,
        "stop":stop,
        "take":take,
        "quantidade":quantidade,
        "status":status,
        "pl":pl

    }).execute()

def buscar_operacoes(

    usuario_id

):

    dados = supabase.table(
        "operacoes"
    ).select("*").eq(
        "usuario_id",
        usuario_id
    ).execute()

    return dados.data

# =========================
# PATRIMONIO
# =========================

def salvar_patrimonio(

    usuario_id,
    saldo

):

    supabase.table(
        "patrimonio"
    ).insert({

        "usuario_id":usuario_id,
        "saldo":saldo

    }).execute()

def buscar_patrimonio(

    usuario_id

):

    dados = supabase.table(
        "patrimonio"
    ).select("*").eq(
        "usuario_id",
        usuario_id
    ).execute()

    return dados.data