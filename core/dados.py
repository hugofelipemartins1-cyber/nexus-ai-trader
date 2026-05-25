import requests
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def obter_dados(ticker):

    try:

        chave = st.secrets["ALPHA_KEY"]

        simbolo = ticker.replace(
            ".SA",
            ""
        )

        url = (

        "https://www.alphavantage.co/query"

        f"?function=TIME_SERIES_DAILY"

        f"&symbol={simbolo}"

        f"&apikey={chave}"

        "&outputsize=full"

        )

        r = requests.get(
            url
        ).json()

        serie = r[
            "Time Series (Daily)"
        ]

        linhas=[]

        for d,v in serie.items():

            linhas.append({

            "Date":d,

            "Open":float(
            v["1. open"]
            ),

            "High":float(
            v["2. high"]
            ),

            "Low":float(
            v["3. low"]
            ),

            "Close":float(
            v["4. close"]
            ),

            "Volume":float(
            v["5. volume"]
            )

            })

        df=pd.DataFrame(
            linhas
        )

        df["Date"]=pd.to_datetime(
            df["Date"]
        )

        df=df.sort_values(
            "Date"
        )

        return df

    except:

        return None