import pandas as pd
import os

ARQ="logs/posicoes.csv"

COLUNAS=[

"ativo",
"entrada",
"stop",
"take",
"quantidade",
"valor",
"status",
"pl"

]

def iniciar():

    if not os.path.exists(ARQ):

        pd.DataFrame(
            columns=COLUNAS
        ).to_csv(
            ARQ,
            index=False
        )

def ler_posicoes():

    iniciar()

    pos=pd.read_csv(
        ARQ
    )

    for c in COLUNAS:

        if c not in pos.columns:

            pos[c]=0

    return pos

def abrir(

    ativo,
    preco,
    stop,
    take,
    saldo

):

    pos=ler_posicoes()

    abertas=pos[
        pos["status"]=="ABERTA"
    ]

    if len(abertas)>=5:

        return

    if ativo in abertas["ativo"].values:

        return

    valor=saldo*0.2

    quantidade=int(
        valor/preco
    )

    nova={

        "ativo":ativo,

        "entrada":preco,

        "stop":stop,

        "take":take,

        "quantidade":quantidade,

        "valor":valor,

        "status":"ABERTA",

        "pl":0

    }

    pos.loc[
        len(pos)
    ]=nova

    pos.to_csv(
        ARQ,
        index=False
    )

def atualizar(

    precos,
    saldo

):

    pos=ler_posicoes()

    for i,row in pos.iterrows():

        if row["status"]!="ABERTA":

            continue

        ativo=row["ativo"]

        if ativo not in precos:

            continue

        atual=precos[
            ativo
        ]

        pl=(

            atual-

            row["entrada"]

        )*row["quantidade"]

        pos.loc[
            i,
            "pl"
        ]=round(
            pl,
            2
        )

        if atual>=row["take"]:

            saldo+=pl

            pos.loc[
                i,
                "status"
            ]="WIN"

        elif atual<=row["stop"]:

            saldo+=pl

            pos.loc[
                i,
                "status"
            ]="LOSS"

    pos.to_csv(
        ARQ,
        index=False
    )

    return pos,saldo