import requests
import pandas as pd
import streamlit as st


@st.cache_data(ttl=1800)
def obter_dados(ticker):

    try:
        chave = st.secrets["ALPHA_KEY"]

        simbolo = ticker.replace(".SA", ".SAO")

        url = (
            "https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_DAILY"
            f"&symbol={simbolo}"
            f"&apikey={chave}"
            "&outputsize=compact"
        )

        resposta = requests.get(
            url,
            timeout=20
        ).json()

        if "Time Series (Daily)" not in resposta:
            print(ticker, resposta)
            return None

        serie = resposta["Time Series (Daily)"]

        dados = []

        for data, valores in serie.items():

            dados.append({
                "Date": pd.to_datetime(data),
                "Open": float(valores["1. open"]),
                "High": float(valores["2. high"]),
                "Low": float(valores["3. low"]),
                "Close": float(valores["4. close"]),
                "Volume": float(valores["5. volume"])
            })

        df = pd.DataFrame(dados)

        df = df.sort_values("Date")

        df = df.dropna()

        return df

    except Exception as erro:
        print(ticker, erro)
        return None