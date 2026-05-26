import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
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

if "user" not in st.session_state:
    tela_login()
    st.stop()

usuario = st.session_state["user"]

# Atualiza a cada 5 minutos para aliviar API gratuita
st_autorefresh(
    interval=300000,
    key="refresh_5_min"
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

agora = datetime.now(
    ZoneInfo("America/Sao_Paulo")
)

st.title("NEXUS AI TRADER")

st.caption(
    f"Institutional Trading Intelligence • {usuario.email} • "
    f"{agora.strftime('%d/%m/%Y %H:%M:%S')} BRT"
)

# ======================
# LOTE LEVE
# ======================

TAMANHO_LOTE = 2
INTERVALO_SEGUNDOS = 300

total_lotes = math.ceil(
    len(IBOV) / TAMANHO_LOTE
)

lote_atual = int(
    time.time() // INTERVALO_SEGUNDOS
) % total_lotes

inicio = lote_atual * TAMANHO_LOTE
fim = inicio + TAMANHO_LOTE

ativos_scan = IBOV[inicio:fim]

st.caption(
    f"Lote {lote_atual + 1}/{total_lotes} • "
    f"Escaneando {len(ativos_scan)} ativos • Somente sinais de COMPRA"
)

scanner = []
compras = []
dados_grafico = {}
precos = {}

for ativo in ativos_scan:

    try:

        df = obter_dados(ativo)

        if df is None:
            continue

        df = indicadores(df)

        score, tendencia, entrada, sinais, stop, take = gerar_score(
            df,
            True
        )

        preco = float(
            df["Close"].iloc[-1]
        )

        dados_grafico[ativo] = df
        precos[ativo] = preco

        linha = {
            "Ativo": ativo,
            "Score": score,
            "Entrada": entrada,
            "Preço": round(preco, 2),
            "Stop": round(stop, 2),
            "Take": round(take, 2),
            "Tendência": tendencia
        }

        scanner.append(linha)

        if entrada == "COMPRA" or score >= 55:
            compras.append(linha)

            abrir(
                ativo,
                preco,
                stop,
                take,
                100000
            )

    except Exception as erro:
        print(ativo, erro)

pos, saldo = atualizar(
    precos,
    100000
)

scanner = pd.DataFrame(scanner)
compras = pd.DataFrame(compras)

wins = len(pos[pos["status"] == "WIN"])
loss = len(pos[pos["status"] == "LOSS"])
abertas = len(pos[pos["status"] == "ABERTA"])
pl = saldo - 100000

k1,k2,k3,k4,k5,k6 = st.columns(6)

k1.metric("💰 Patrimônio", f"R$ {saldo:,.2f}")
k2.metric("📈 P/L", f"R$ {pl:,.2f}")
k3.metric("🏆 WIN", wins)
k4.metric("❌ LOSS", loss)
k5.metric("🟢 ABERTAS", abertas)
k6.metric("🛒 COMPRAS", 0 if compras.empty else len(compras))

esq,dir = st.columns([1,2])

with esq:

    st.subheader("SINAIS DE COMPRA")

    if compras.empty:

        st.info(
            "Nenhuma ação boa para compra neste lote. "
            "O robô continuará escaneando automaticamente."
        )

    else:

        st.dataframe(
            compras,
            use_container_width=True,
            height=260
        )

    st.subheader("POSIÇÕES")

    st.dataframe(
        pos.tail(20),
        use_container_width=True,
        height=320
    )

with dir:

    if not compras.empty:

        ativo_grafico = st.selectbox(
            "Gráfico do sinal",
            compras["Ativo"]
        )

        df_grafico = dados_grafico[ativo_grafico]

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

    else:

        st.subheader("Monitoramento ativo")

        st.write(
            "O robô está varrendo os lotes automaticamente. "
            "Quando uma ação atingir critério de compra, ela aparecerá aqui."
        )

        if not scanner.empty:
            st.caption("Ativos analisados neste lote:")
            st.dataframe(
                scanner,
                use_container_width=True,
                height=260
            )