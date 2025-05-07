import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard de Logística - Login", page_icon="LOGINLOGO.PNG")

# === Estilo Personalizado ===
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    h1, h2, h3 {
        color: #1f4e79;
    }
    .title-container {
        text-align: center;
        padding: 10px 0;
    }
    .title-container h1 {
        font-size: 2.5em;
        font-weight: 700;
        color: #1f4e79;
        margin-bottom: 0;
    }
    .title-container p {
        font-size: 1.1em;
        color: #444;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# === Cabeçalho ===
st.markdown("""
    <div class="title-container">
        <h1>🚛 Dashboard Logística - Login</h1>
    </div>
""", unsafe_allow_html=True)

# === Carregando os dados ===
df = pd.read_csv("logistica_login_logistica_2024.csv", sep=";", decimal=",")
df.columns = df.columns.str.encode('latin1').str.decode('utf-8').str.strip()

# === Conversão e limpeza ===
if "Data da Entrega" in df.columns:
    df["Data da Entrega"] = pd.to_datetime(df["Data da Entrega"], format="%d/%m/%Y", errors='coerce')

df["Quantidade de Volumes"] = pd.to_numeric(df["Quantidade de Volumes"], errors="coerce")
df["Peso Total (kg)"] = pd.to_numeric(df["Peso Total (kg)"], errors="coerce")
df["Valor do Frete (R$)"] = pd.to_numeric(df["Valor do Frete (R$)"], errors="coerce")
df["Tempo de Entrega (dias)"] = pd.to_numeric(df["Tempo de Entrega (dias)"], errors="coerce")
df = df.drop_duplicates()

# Logo no topo da barra lateral
st.sidebar.image("LOGINLOGO.png", use_container_width=True)

# === Filtros ===
meses_disponiveis = df["Mês"].dropna().unique()
mes = st.sidebar.selectbox("📅 Selecione o Mês", sorted(meses_disponiveis))

# Filtro de Nome do Motorista
motoristas_disponiveis = df["Nome do Motorista"].dropna().unique()
motorista = st.sidebar.selectbox("🚚 Filtrar por Nome do Motorista", ["Todos"] + sorted(motoristas_disponiveis))

# Filtro de Produto Avariado
produto_avariado_opcoes = ["Todos", "Sim", "Não"]
produto_avariado = st.sidebar.selectbox("⚠️ Filtrar por Produto Avariado (Sim/Não)", produto_avariado_opcoes)

# Filtro de Empresa
empresas_disponiveis = df["Empresa"].dropna().unique()
empresa = st.sidebar.selectbox("🏢 Filtrar por Empresa", ["Todos"] + sorted(empresas_disponiveis))

# Filtro
df_filtrado = df[df["Mês"] == mes]

if motorista != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Nome do Motorista"] == motorista]

# Ajustando o filtro de "Produto Avariado"
if produto_avariado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Produto Avariado"] == produto_avariado]

# Filtro de Empresa
if empresa != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Empresa"] == empresa]

st.markdown(f"### 📦 Dados do mês selecionado: `{mes}` - Motorista: `{motorista}` - Produto Avariado: `{produto_avariado}` - Empresa: `{empresa}`")
st.dataframe(df_filtrado, use_container_width=True)

# === Linha 1 ===
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 💰 Valor do Frete por Tipo de Carga")
    fig_carga = px.bar(
        df_filtrado,
        x="Tipo de Carga",
        y="Valor do Frete (R$)",
        color="Status da Carga",
        title="",
        barmode="group",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    fig_carga.update_layout(hoverlabel=dict(font_size=26))
    st.plotly_chart(fig_carga, use_container_width=True)

with col2:
    st.markdown("#### ⚖️ Peso Transportado por Tipo de Veículo")
    fig_veiculo = px.bar(
        df_filtrado,
        x="Tipo de Veículo",
        y="Peso Total (kg)",
        color="Empresa",
        title="",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    fig_veiculo.update_layout(hoverlabel=dict(font_size=26))
    st.plotly_chart(fig_veiculo, use_container_width=True)

# === Linha 2 ===
col3, col4 = st.columns(2)
with col3:
    st.markdown("#### 🌎 Volumes por Estado de Destino")
    fig_estado = px.bar(
        df_filtrado,
        x="Estado de Destino",
        y="Quantidade de Volumes",
        color="Status da Carga",
        title="",
        color_discrete_sequence=px.colors.sequential.Purples
    )
    fig_estado.update_layout(hoverlabel=dict(font_size=26))
    st.plotly_chart(fig_estado, use_container_width=True)

with col4:
    st.markdown("#### 🚨 Distribuição de Produtos Avariados")
    fig_pizza = px.pie(
        df_filtrado,
        names="Produto Avariado",
        title="",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_pizza.update_layout(hoverlabel=dict(font_size=26))
    st.plotly_chart(fig_pizza, use_container_width=True)
