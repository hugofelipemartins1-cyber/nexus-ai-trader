import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(
    ttl=300
)

def obter_dados(

    ticker

):

    try:

        df=yf.download(

            ticker,

            period="1y",

            interval="1d",

            auto_adjust=True,

            progress=False,

            threads=False

        )

        if df.empty:

            return None

        if isinstance(
            df.columns,
            pd.MultiIndex
        ):

            df.columns=df.columns.droplevel(
                1
            )

        df=df.reset_index()

        df=df[[

            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"

        ]]

        return df

    except:

        return None