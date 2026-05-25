import yfinance as yf
import pandas as pd

def obter_dados(ticker):

    try:

        df = yf.download(

            ticker,

            period="1y",

            interval="1d",

            auto_adjust=True,

            progress=False

        )

        if df.empty:

            return None

        # remove MultiIndex novo do Yahoo
        if isinstance(
            df.columns,
            pd.MultiIndex
        ):

            df.columns = df.columns.droplevel(
                1
            )

        df = df.reset_index()

        colunas = [

            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"

        ]

        df = df[
            colunas
        ]

        df = df.dropna()

        return df

    except Exception as erro:

        print(
            ticker,
            erro
        )

        return None