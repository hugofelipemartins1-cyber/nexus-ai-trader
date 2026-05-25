import ta


def indicadores(df):

    close = df["Close"].squeeze()

    high = df["High"].squeeze()

    low = df["Low"].squeeze()

    volume = df["Volume"].squeeze()

    df["EMA21"] = ta.trend.ema_indicator(
        close,
        window=21
    )

    df["EMA80"] = ta.trend.ema_indicator(
        close,
        window=80
    )

    df["RSI"] = ta.momentum.rsi(
        close,
        window=14
    )

    df["ATR"] = ta.volatility.average_true_range(
        high,
        low,
        close
    )

    df["VOL_MEDIA"] = volume.rolling(
        20
    ).mean()

    return df