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
from core.executor import abrir, atualizar, ler_posicoes
from core.mercado import IBOV

st.set_page_config(
    page_title="NEXUS AI TRADER",
    layout="wide"
)

# =========================
# LOGIN
# =========================

if "user" not in st.session_state:

    tela_login()

    st.stop()

usuario = st.session_state["user"]

# =========================
# REFRESH
# =========================

st_autorefresh(
    interval=120000,
    key="refresh_2_min"
)

# =========================
# CSS
# =========================

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

# =========================
# HEADER
# =========================

st.title(
    "NEXUS AI TRADER"
)

st.caption(
    f"Institutional Trading Intelligence • {usuario.email}"
)

# =========================
# LOTE ROTATIVO
# =========================

TAMANHO_LOTE = 10

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

scanner = []

# =========================
# SCANNER
# =========================

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

        score,t,e,s,stop,take = gerar_score(
            df,
            True
        )

        preco = float(
            df["Close"].iloc[-1]
        )

        scanner.append({

            "Ativo":ativo,
            "Score":score,
            "Entrada":e,
            "Preço":round(preco,2),
            "Stop":round(stop,2),
            "Take":round(take,2),
            "Tendência":t

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
        "Scanner vazio"
    )

    st.stop()

scanner = scanner.sort_values(
    "Score",
    ascending=False
)

# =========================
# ROBO
# =========================

precos = {}

for _,row in scanner.iterrows():

    ativo = row["Ativo"]

    preco = row["Preço"]

    stop = row["Stop"]

    take = row["Take"]

    score = row["Score"]

    precos[
        ativo
    ] = preco

    if score >= 55:

        abrir(

            usuario.id,

            ativo,

            preco,

            stop,

            take

        )

pos,saldo = atualizar(

    usuario.id,

    precos

)

# =========================
# KPIS
# =========================

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

# =========================
# LAYOUT
# =========================

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
        pos,
        use_container_width=True,
        height=300
    )

with dir:

    ativo = st.selectbox(
        "Mercado",
        scanner["Ativo"]
    )

    df = obter_dados(
        ativo
    )

    df = indicadores(
        df
    )

    fig = go.Figure()

    fig.add_trace(

        go.Candlestick(

            x=df["Date"],

            open=df["Open"],

            high=df["High"],

            low=df["Low"],

            close=df["Close"]

        )

    )

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["EMA21"],

            name="EMA21"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["EMA80"],

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