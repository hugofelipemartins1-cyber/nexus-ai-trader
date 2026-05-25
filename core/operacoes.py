import pandas as pd
import os

ARQUIVO = "logs/posicoes.csv"


def abrir_trade(

    ativo,
    preco,
    stop,
    take,
    qtd

):

    if qtd <= 0:

        return

    if os.path.exists(
        ARQUIVO
    ):

        df = pd.read_csv(
            ARQUIVO
        )

    else:

        df = pd.DataFrame()

    abertas = df[

        (df["ativo"] == ativo)

        &

        (df["status"] == "ABERTO")

    ]

    if len(
        abertas
    ) > 0:

        return

    novo = pd.DataFrame(

        [

            {

                "ativo":ativo,

                "entrada":preco,

                "stop":stop,

                "take":take,

                "qtd":qtd,

                "status":"ABERTO"

            }

        ]

    )

    df = pd.concat(
        [
            df,
            novo
        ],
        ignore_index=True
    )

    df.to_csv(
        ARQUIVO,
        index=False
    )


def monitorar_trade(

    ativo,

    preco_atual,

    carteira

):

    if not os.path.exists(
        ARQUIVO
    ):

        return carteira

    pos = pd.read_csv(
        ARQUIVO
    )

    for i in range(
        len(pos)
    ):

        linha = pos.iloc[i]

        if (

            linha["ativo"]

            !=

            ativo

        ):

            continue

        if (

            linha["status"]

            !=

            "ABERTO"

        ):

            continue

        entrada = linha["entrada"]

        stop = linha["stop"]

        take = linha["take"]

        qtd = linha["qtd"]

        pl = (

            preco_atual

            -

            entrada

        ) * qtd

        if preco_atual <= stop:

            carteira.loc[
                0,
                "saldo"
            ] += pl

            carteira.loc[
                0,
                "losses"
            ] += 1

            carteira.loc[
                0,
                "operacoes"
            ] += 1

            pos.loc[
                i,
                "status"
            ] = "LOSS"

        elif preco_atual >= take:

            carteira.loc[
                0,
                "saldo"
            ] += pl

            carteira.loc[
                0,
                "wins"
            ] += 1

            carteira.loc[
                0,
                "operacoes"
            ] += 1

            pos.loc[
                i,
                "status"
            ] = "WIN"

    pos.to_csv(
        ARQUIVO,
        index=False
    )

    return carteira
