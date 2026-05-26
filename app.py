import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time
import math

from core.auth import tela_login
from core.dados import obter_dados
from core.indicadores import indicadores
from core.score import gerar_score
from core.executor import abrir, atualizar
from core.mercado import IBOV

st.set_page_config(
    page_title="NEXUS AI TRADER",
    layout="wide"
)

if "user" not in st.session_state:

    tela_login()

    st.stop()

usuario = st.session_state["user"]

st_autorefresh(
    interval=120000,
    key="refresh_2_min"
)

st.markdown("""
<style>
.stApp{
background:#050b14;
color:white;
}

[data-testid="metric-container"]{
background:#111827 !important;
padding:20px;
border-radius:16px;
border:1px solid #1f2937;
}

[data-testid="metric-container"] *{
color:white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("NEXUS AI TRADER")

st.caption(
    f"Institutional Trading Intelligence • {usuario.email} • "
    f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)

TAMANHO_LOTE = 4

INTERVALO_SEGUNDOS = 120

total_lotes = math.ceil(
    len(IBOV) / TAMANHO_LOTE
)

lote_atual = int(
    time.time() // INTERVALO_SEGUNDOS
) % total_lotes

inicio = lote_atual * TAMANHO_LOTE

fim = inicio + TAMANHO_LOTE

ativos_scan = IBOV[
    inicio:fim
]

st.caption(
    f"Lote {lote_atual + 1}/{total_lotes} • "
    f"Escaneando {len(ativos_scan)} ativos"
)

scanner = []

dados_grafico = {}

for ativo in ativos_scan:

    try:

        df = obter_dados(
            ativo
        )

        if df is None:

            continue

        df = indicadores(
            df
        )

        score,tendencia,entrada,sinais,stop,take = gerar_score(
            df,
            True
        )

        preco = float(
            df["Close"].iloc[-1]
        )

        dados_grafico[
            ativo
        ] = df

        scanner.append({
            "Ativo":ativo,
            "Score":score,
            "Entrada":entrada,
            "Preço":round(preco,2),
            "Stop":round(stop,2),
            "Take":round(take,2),
            "Tendência":tendencia
        })

    except Exception as erro:

        print(
            ativo,
            erro
        )

scanner = pd.DataFrame(
    scanner
)

if scanner.empty:

    st.error(
        "Scanner vazio neste lote. A API gratuita limitou as consultas. Aguarde a próxima rodada."
    )

    st.stop()

scanner = scanner.sort_values(
    "Score",
    ascending=False
)

precos = {}

for _,row in scanner.iterrows():

    ativo = row["Ativo"]

    preco = float(
        row["Preço"]
    )

    score = float(
        row["Score"]
    )

    stop = float(
        row["Stop"]
    )

    take = float(
        row["Take"]
    )

    precos[
        ativo
    ] = preco

    if score >= 55:

        abrir(
            ativo,
            preco,
            stop,
            take,
            100000
        )

pos,saldo = atualizar(
    precos,
    100000
)

wins = len(
    pos[
        pos["status"]=="WIN"
    ]
)

loss = len(
    pos[
        pos["status"]=="LOSS"
    ]
)

abertas = len(
    pos[
        pos["status"]=="ABERTA"
    ]
)

pl = saldo - 100000

k1,k2,k3,k4,k5,k6 = st.columns(6)

k1.metric(
    "💰 Patrimônio",
    f"R$ {saldo:,.2f}"
)

k2.metric(
    "📈 P/L",
    f"R$ {pl:,.2f}"
)

k3.metric(
    "🏆 WIN",
    wins
)

k4.metric(
    "❌ LOSS",
    loss
)

k5.metric(
    "🟢 ABERTAS",
    abertas
)

k6.metric(
    "📊 SINAIS",
    len(
        scanner[
            scanner["Score"]>=55
        ]
    )
)

esq,dir = st.columns(
    [1,2]
)

with esq:

    st.subheader(
        "TOP OPORTUNIDADES"
    )

    st.dataframe(
        scanner,
        use_container_width=True,
        height=350
    )

    st.subheader(
        "POSIÇÕES"
    )

    st.dataframe(
        pos.tail(20),
        use_container_width=True,
        height=300
    )

with dir:

    ativo_grafico = st.selectbox(
        "Mercado",
        scanner["Ativo"]
    )

    df_grafico = dados_grafico[
        ativo_grafico
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df_grafico["Date"],
            open=df_grafico["Open"],
            high=df_grafico["High"],
            low=df_grafico["Low"],
            close=df_grafico["Close"]
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_grafico["Date"],
            y=df_grafico["EMA21"],
            name="EMA21"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_grafico["Date"],
            y=df_grafico["EMA80"],
            name="EMA80"
        )
    )

    fig.update_layout(
        height=700,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )