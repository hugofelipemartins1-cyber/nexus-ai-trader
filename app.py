import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time
import math

from core.dados import obter_dados
from core.indicadores import indicadores
from core.score import gerar_score
from core.executor import abrir, atualizar, ler_posicoes
from core.carteira import ler_carteira
from core.patrimonio import registrar, ler
from core.mercado import IBOV

st.set_page_config(
    page_title="NEXUS AI TRADER",
    layout="wide"
)

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

h1,h2,h3{
color:white;
}
</style>
""", unsafe_allow_html=True)

st.title("NEXUS AI TRADER")
st.caption(
    f"Institutional Trading Intelligence • Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)

# ======================
# LOTE ROTATIVO
# ======================

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

lote_base = IBOV[inicio:fim]

pos_atual = ler_posicoes()

ativos_abertos = []

if not pos_atual.empty:

    try:
        ativos_abertos = list(
            pos_atual[
                pos_atual["status"] == "ABERTA"
            ]["ativo"].unique()
        )
    except:
        ativos_abertos = []

ativos_scan = []

for ativo in ativos_abertos + lote_base:

    if ativo not in ativos_scan:

        ativos_scan.append(ativo)

ativos_scan = ativos_scan[:TAMANHO_LOTE]

st.caption(
    f"Lote {lote_atual + 1}/{total_lotes} • Escaneando {len(ativos_scan)} ativos"
)

# ======================
# SCANNER
# ======================

scanner = []

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

        score, tendencia, entrada, sinais, stop, take = gerar_score(
            df,
            True
        )

        preco = float(
            df["Close"].iloc[-1]
        )

        scanner.append({
            "Ativo": ativo,
            "Score": score,
            "Entrada": entrada,
            "Preço": round(preco, 2),
            "Stop": round(stop, 2),
            "Take": round(take, 2),
            "Tendência": tendencia
        })

    except Exception as erro:
        print(ativo, erro)
        continue

scanner = pd.DataFrame(
    scanner
)

if scanner.empty:

    st.error(
        "Scanner vazio neste lote. Aguarde a próxima rodada ou verifique o limite da API."
    )

    st.stop()

scanner = scanner.sort_values(
    "Score",
    ascending=False
)

# ======================
# CARTEIRA
# ======================

carteira = ler_carteira()

saldo = float(
    carteira["saldo"].iloc[0]
)

# ======================
# ROBO AUTÔNOMO
# ======================

precos = {}

for _, row in scanner.iterrows():

    ativo = row["Ativo"]
    preco = float(row["Preço"])
    score = float(row["Score"])
    stop = float(row["Stop"])
    take = float(row["Take"])

    precos[ativo] = preco

    if score >= 55:

        abrir(
            ativo,
            preco,
            stop,
            take,
            saldo
        )

pos, saldo = atualizar(
    precos,
    saldo
)

registrar(
    saldo
)

hist = ler()

# ======================
# KPIS
# ======================

wins = len(
    pos[
        pos["status"] == "WIN"
    ]
)

loss = len(
    pos[
        pos["status"] == "LOSS"
    ]
)

abertas = len(
    pos[
        pos["status"] == "ABERTA"
    ]
)

pl = saldo - 100000

k1, k2, k3, k4, k5, k6 = st.columns(6)

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
            scanner["Score"] >= 55
        ]
    )
)

# ======================
# LAYOUT
# ======================

esq, dir = st.columns(
    [1, 2]
)

with esq:

    st.subheader(
        "TOP OPORTUNIDADES"
    )

    st.dataframe(
        scanner,
        height=350,
        use_container_width=True
    )

    st.subheader(
        "POSIÇÕES"
    )

    st.dataframe(
        pos.tail(20),
        height=280,
        use_container_width=True
    )

with dir:

    ativo_grafico = st.selectbox(
        "Mercado",
        scanner["Ativo"]
    )

    df_grafico = obter_dados(
        ativo_grafico
    )

    df_grafico = indicadores(
        df_grafico
    )

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

st.subheader(
    "EVOLUÇÃO PATRIMÔNIO"
)

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=hist["data"],
        y=hist["saldo"],
        fill="tozeroy"
    )
)

fig2.update_layout(
    height=300,
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)