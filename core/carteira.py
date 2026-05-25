import pandas as pd
import os

ARQUIVO = "logs/carteira.csv"


def iniciar_carteira():

    if not os.path.exists(
        ARQUIVO
    ):

        df = pd.DataFrame(
            [

                {

                    "saldo":100000,

                    "lucro":0,

                    "operacoes":0,

                    "wins":0,

                    "losses":0

                }

            ]
        )

        df.to_csv(
            ARQUIVO,
            index=False
        )


def ler_carteira():

    iniciar_carteira()

    return pd.read_csv(
        ARQUIVO
    )


def atualizar_carteira(df):

    df.to_csv(
        ARQUIVO,
        index=False
    )

