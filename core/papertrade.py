from core.carteira import *


def abrir_posicao(

    preco,

    stop,

    saldo,

    risco=1

):

    perda_max = saldo * (

        risco / 100

    )

    risco_acao = abs(

        preco-stop

    )

    if risco_acao == 0:

        qtd = 0

    else:

        qtd = int(

            perda_max /

            risco_acao

        )

    return qtd


def calcular_pl(

    entrada,

    atual,

    qtd

):

    return round(

        (

            atual

            -

            entrada

        )

        *

        qtd,

        2

    )

