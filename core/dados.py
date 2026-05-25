import yfinance as yf
import pandas as pd
import streamlit as st
from core.mercado import IBOV

@st.cache_data(ttl=300)
def baixar_mercado():

    try:

        dados = yf.download(

            tickers=IBOV,

            period="1y",

            interval="1d",

            auto_adjust=True,

            progress=False,

            group_by="ticker",

            threads=False

        )

        return dados

    except:

        return None


def obter_dados(ticker):

    mercado = baixar_mercado()

    if mercado is None:

        return None

    try:

        df = mercado[ticker]

        df = df.reset_index()

        df = df[[
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]]

        df = df.dropna()

        return df

    except:

        return None