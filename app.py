import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
import os

# Configuração da página
st.set_page_config(
    page_title="Monitoramento de Motor",
    layout="wide"
)

# Auto refresh a cada 15 segundos
st_autorefresh(
    interval=15_000,
    limit=None,
    key="dashboard_refresh"
)

# Carregar variáveis de ambiente
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    st.error("SUPABASE_URL ou SUPABASE_KEY não encontrados no arquivo .env")
    st.stop()

# Conectar ao Supabase
supabase = create_client(url, key)

st.title("📈 Monitoramento de Vibração do Motor")

# Buscar dados
dados = (
    supabase
    .table("sensor_data")
    .select("*")
    .order("created_at", desc=False)
    .execute()
)

df = pd.DataFrame(dados.data)

if df.empty:
    st.warning("Nenhum dado encontrado.")
    st.stop()

# Garantir formato de data
df["created_at"] = pd.to_datetime(df["created_at"])

# Último registro
ultima = df.iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Vibração Atual",
        f"{ultima['vibration']:.2f} g"
    )

with col2:
    st.metric(
        "Temperatura",
        f"{ultima['temperature']:.2f} °C"
    )

# Gráficos
fig1 = px.line(
    df,
    x="created_at",
    y="vibration",
    title="Vibração ao longo do tempo"
)

fig2 = px.line(
    df,
    x="created_at",
    y="temperature",
    title="Temperatura ao longo do tempo"
)

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Últimos registros")
st.dataframe(df.tail(20), use_container_width=True)