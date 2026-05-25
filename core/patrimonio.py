import pandas as pd
import os
from datetime import datetime

ARQ = "logs/patrimonio.csv"

def iniciar():

    if not os.path.exists(ARQ):

        pd.DataFrame(

            columns=[

                "data",
                "saldo"

            ]

        ).to_csv(

            ARQ,

            index=False

        )


def registrar(saldo):

    iniciar()

    hist = pd.read_csv(
        ARQ
    )

    nova = pd.DataFrame([{

        "data":

        datetime.now(),

        "saldo":saldo

    }])

    hist = pd.concat(
        [hist,nova]
    )

    hist.to_csv(
        ARQ,
        index=False
    )


def ler():

    iniciar()

    return pd.read_csv(
        ARQ
    )
