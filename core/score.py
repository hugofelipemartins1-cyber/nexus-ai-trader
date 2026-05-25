def gerar_score(
    df,
    detalhes=False
):

    ultimo = df.iloc[-1]

    score = 0

    sinais=[]

    tendencia="BAIXA"

    entrada="SEM ENTRADA"

    stop=0

    take=0

    if ultimo["EMA21"] > ultimo["EMA80"]:

        score += 40

        tendencia="ALTA"

        sinais.append(
            "EMA21 > EMA80"
        )

    if ultimo["RSI"] < 65:

        score += 30

        sinais.append(
            "RSI"
        )

    if ultimo["Volume"] > ultimo["VOL_MEDIA"]:

        score += 20

        sinais.append(
            "Volume"
        )

    if score >=55:

        entrada="COMPRA"

        stop = float(
            ultimo["Close"]
        )*0.97

        take = float(
            ultimo["Close"]
        )*1.05

    elif score>=40:

        entrada="OBSERVAR"

    if detalhes:

        return (

            score,

            tendencia,

            entrada,

            sinais,

            stop,

            take

        )

    return score