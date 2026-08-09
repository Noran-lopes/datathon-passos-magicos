import streamlit as st
import pandas as pd
import numpy as np
import joblib

import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Passos Mágicos",
    page_icon="🎓",
    layout="wide"
)

# =====================================================
# CARREGAMENTO
# =====================================================

@st.cache_data
def carregar_base():
    return pd.read_csv("../data/base_analitica_consolidada.csv")

@st.cache_resource
def carregar_modelo():
    modelo = joblib.load("../models/modelo_risco.pkl")
    imputer = joblib.load("../models/imputer.pkl")
    return modelo, imputer

df = carregar_base()
modelo, imputer = carregar_modelo()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎓 Menu")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "Dashboard Executivo",
        "Análises",
        "Predição de Risco"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

if pagina == "Dashboard Executivo":

    st.title("🎓 Dashboard Executivo")
    st.markdown("Associação Passos Mágicos")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "Alunos Únicos",
        df["RA"].nunique()
    )

    col2.metric(
        "INDE Médio",
        round(df["INDE"].mean(),2)
    )

    col3.metric(
        "IDA Médio",
        round(df["IDA"].mean(),2)
    )

    col4.metric(
        "IAN Médio",
        round(df["IAN"].mean(),2)
    )

    st.divider()

    col1,col2 = st.columns(2)

    with col1:

        pedra = (
            df["Pedra"]
            .value_counts()
            .reset_index()
        )

        pedra.columns = ["Pedra","Quantidade"]

        fig = px.bar(
            pedra,
            x="Pedra",
            y="Quantidade",
            title="Distribuição das Pedras"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        risco = (
            df["CLASSE_DEFASAGEM"]
            .value_counts()
            .reset_index()
        )

        risco.columns = [
            "Classe",
            "Quantidade"
        ]

        fig2 = px.pie(
            risco,
            names="Classe",
            values="Quantidade",
            title="Classificação da Defasagem"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.subheader("Evolução dos Indicadores")

    evolucao = (
        df.groupby("ANO")
        [
            [
                "INDE",
                "IDA",
                "IEG",
                "IAN"
            ]
        ]
        .mean()
        .reset_index()
    )

    fig3 = px.line(
        evolucao,
        x="ANO",
        y=[
            "INDE",
            "IDA",
            "IEG",
            "IAN"
        ],
        markers=True
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =====================================================
# ANALISES
# =====================================================

elif pagina == "Análises":

    st.title("📈 Análises dos Indicadores")

    ano = st.selectbox(
        "Ano",
        sorted(df["ANO"].dropna().unique())
    )

    df_filtrado = df[
        df["ANO"] == ano
    ]

    col1,col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            df_filtrado,
            x="INDE",
            nbins=20,
            title=f"Distribuição do INDE ({ano})"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.box(
            df_filtrado,
            x="Pedra",
            y="INDE",
            title="INDE por Pedra"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader(
        "Engajamento x Desempenho"
    )

    fig = px.scatter(
        df_filtrado,
        x="IEG",
        y="IDA",
        color="Pedra",
        hover_data=["ANO"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Perfil das Pedras"
    )

    perfil = (
        df.groupby("Pedra")
        [
            [
                "INDE",
                "IDA",
                "IEG",
                "IAN",
                "IPV"
            ]
        ]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        perfil,
        x="Pedra",
        y=[
            "IDA",
            "IEG",
            "IAN",
            "IPV"
        ],
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# PREDIÇÃO
# =====================================================

else:

    st.title("🤖 Predição de Risco")

    st.write(
        """
        Informe os indicadores do aluno e obtenha
        a probabilidade de risco de defasagem.
        """
    )

    col1,col2 = st.columns(2)

    with col1:

        ida = st.slider(
            "IDA",
            0.0,
            10.0,
            6.0
        )

        ieg = st.slider(
            "IEG",
            0.0,
            10.0,
            8.0
        )

        iaa = st.slider(
            "IAA",
            0.0,
            10.0,
            8.0
        )

        ips = st.slider(
            "IPS",
            0.0,
            10.0,
            6.0
        )

        ipp = st.slider(
            "IPP",
            0.0,
            10.0,
            7.0
        )

    with col2:

        ipv = st.slider(
            "IPV",
            0.0,
            10.0,
            7.0
        )

        idade = st.slider(
            "Idade",
            7,
            25,
            12
        )

        fase = st.slider(
            "Fase",
            0,
            8,
            3
        )

        tempo = st.slider(
            "Tempo no Programa",
            0,
            10,
            2
        )

    if st.button(
        "Calcular Probabilidade"
    ):

        entrada = pd.DataFrame({

            "IDA":[ida],
            "IEG":[ieg],
            "IAA":[iaa],
            "IPS":[ips],
            "IPP":[ipp],
            "IPV":[ipv],
            "Idade":[idade],
            "FASE_NUMERICA":[fase],
            "TEMPO_PROGRAMA":[tempo]

        })

        entrada = imputer.transform(
            entrada
        )

        prob = modelo.predict_proba(
            entrada
        )[0][1]

        st.metric(
            "Probabilidade de Risco",
            f"{prob:.2%}"
        )

        if prob >= 0.70:

            st.error(
                "🔴 ALTO RISCO"
            )

        elif prob >= 0.40:

            st.warning(
                "🟡 MÉDIO RISCO"
            )

        else:

            st.success(
                "🟢 BAIXO RISCO"
            )

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=prob*100,
                title={
                    "text":"Score de Risco"
                },
                gauge={
                    "axis":{
                        "range":[0,100]
                    },
                    "bar":{
                        "color":"red"
                    }
                }
            )
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )
