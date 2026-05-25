import pandas as pd
import os

ARQUIVO = "logs/trades.csv"


def salvar_sinal(
    ativo,
    score,
    tendencia,
    entrada,
    stop,
    take,
    preco
):

    novo = {

        "ativo":ativo,

        "score":score,

        "tendencia":tendencia,

        "entrada":entrada,

        "preco":preco,

        "stop":stop,

        "take":take

    }

    if os.path.exists(
        ARQUIVO
    ):

        df = pd.read_csv(
            ARQUIVO
        )

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [novo]
                )
            ]
        )

    else:

        df = pd.DataFrame(
            [novo]
        )

    df.to_csv(
        ARQUIVO,
        index=False
    )