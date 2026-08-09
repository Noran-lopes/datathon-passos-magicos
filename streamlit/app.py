import streamlit as st
import pandas as pd
import numpy as np
import joblib

import plotly.express as px
import plotly.graph_objects as go

# =============================================================
# CONFIGURAÇÃO
# =============================================================

st.set_page_config(
    page_title="Passos Mágicos Analytics",
    page_icon="🎓",
    layout="wide"
)

# =============================================================
# FUNÇÕES
# =============================================================

@st.cache_data
def carregar_dados():
    return pd.read_csv("data/base_analitica_consolidada.csv")


@st.cache_resource
def carregar_modelo():

    modelo = joblib.load(
        "models/modelo_risco.pkl"
    )

    imputer = joblib.load(
        "models/imputer.pkl"
    )

    return modelo, imputer


def comentario(
    interpretacao,
    insight,
    recomendacao
):

    with st.expander(
        "📖 Comentários da análise",
        expanded=False
    ):

        st.markdown(f"""
### 🧠 Interpretação

{interpretacao}

### 💡 Insight

{insight}

### 🎯 Recomendação

{recomendacao}
""")


# =============================================================
# DADOS
# =============================================================

df = carregar_dados()

modelo = None
imputer = None

try:
    modelo, imputer = carregar_modelo()
except:
    pass

# =============================================================
# MENU
# =============================================================

pagina = st.sidebar.radio(
    "Menu",
    [
        "🏠 Visão Executiva",
        "📊 Diagnóstico Educacional",
        "🤖 Predição de Risco",
        "💡 Insights Estratégicos",
        "📚 Dicionário PEDE"
    ]
)

# =============================================================
# FILTROS GLOBAIS
# =============================================================

st.sidebar.markdown("---")

if "ANO" in df.columns:

    anos = sorted(
        df["ANO"].dropna().unique()
    )

    ano_selecionado = st.sidebar.selectbox(
        "Ano",
        ["Todos"] + list(anos)
    )

    if ano_selecionado != "Todos":

        df = df[
            df["ANO"] == ano_selecionado
        ]

# =============================================================
# VISÃO EXECUTIVA
# =============================================================

if pagina == "🏠 Visão Executiva":

    st.title(
        "🎓 Passos Mágicos Analytics Platform"
    )

    st.markdown(
        """
Monitoramento Educacional e Predição de Risco
"""
    )

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "👨‍🎓 Alunos",
        df["RA"].nunique()
    )

    col2.metric(
        "📈 INDE Médio",
        round(df["INDE"].mean(),2)
    )

    col3.metric(
        "📚 IDA Médio",
        round(df["IDA"].mean(),2)
    )

    col4.metric(
        "🎯 IAN Médio",
        round(df["IAN"].mean(),2)
    )

    st.divider()

    evolucao = (
        df.groupby("ANO")
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

    fig = px.line(
        evolucao,
        x="ANO",
        y=[
            "INDE",
            "IDA",
            "IEG",
            "IAN",
            "IPV"
        ],
        markers=True,
        title="Evolução dos Indicadores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    comentario(
        "Os indicadores apresentaram comportamento positivo ao longo dos anos analisados.",
        "O IAN foi o indicador com evolução mais consistente, sugerindo redução da defasagem educacional.",
        "Priorizar iniciativas que acelerem a evolução dos alunos nas fases iniciais."
    )

    col1,col2 = st.columns(2)

    with col1:

        pedras = (
            df["Pedra"]
            .value_counts()
            .reset_index()
        )

        pedras.columns = [
            "Pedra",
            "Quantidade"
        ]

        fig = px.bar(
            pedras,
            x="Pedra",
            y="Quantidade",
            color="Pedra",
            title="Distribuição das Pedras"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        if "CLASSE_DEFASAGEM" in df.columns:

            defasagem = (
                df["CLASSE_DEFASAGEM"]
                .value_counts()
                .reset_index()
            )

            defasagem.columns = [
                "Classe",
                "Quantidade"
            ]

            fig = px.pie(
                defasagem,
                names="Classe",
                values="Quantidade",
                hole=0.5,
                title="Perfil da Defasagem"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# =============================================================
# DIAGNÓSTICO EDUCACIONAL
# =============================================================

elif pagina == "📊 Diagnóstico Educacional":

    st.title(
        "📊 Diagnóstico Educacional"
    )

    aba1,aba2,aba3 = st.tabs(
        [
            "Defasagem",
            "Engajamento",
            "Pedras"
        ]
    )

    with aba1:

        fig = px.histogram(
            df,
            x="IAN",
            nbins=20,
            title="Distribuição do IAN"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        comentario(
            "A maior parte dos alunos encontra-se em defasagem moderada ou em fase adequada.",
            "Mais de 54% dos registros encontram-se em defasagem moderada.",
            "Concentrar esforços nos alunos moderadamente defasados."
        )

    with aba2:

        fig = px.scatter(
            df,
            x="IEG",
            y="IDA",
            color="Pedra"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        comentario(
            "Existe relação positiva entre engajamento e desempenho.",
            "A correlação encontrada entre IEG e IDA foi aproximadamente 0,54.",
            "Monitorar quedas no IEG como sinal precoce de risco."
        )

    with aba3:

        perfil = (
            df.groupby("Pedra")
            [
                [
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

        comentario(
            "Os alunos Topázio se destacam em todos os indicadores.",
            "IDA, IEG e IAN são os principais diferenciais dos melhores alunos.",
            "Utilizar o perfil Topázio como benchmark."
        )

# =============================================================
# PREDIÇÃO
# =============================================================

elif pagina == "🤖 Predição de Risco":

    st.title(
        "🤖 Motor Preditivo"
    )

    if modelo is None:

        st.error(
            "Modelo não encontrado."
        )

        st.stop()

    col1,col2 = st.columns(2)

    with col1:

        ida = st.slider("IDA",0.0,10.0,6.0)
        ieg = st.slider("IEG",0.0,10.0,8.0)
        iaa = st.slider("IAA",0.0,10.0,8.0)
        ips = st.slider("IPS",0.0,10.0,6.0)

    with col2:

        ipp = st.slider("IPP",0.0,10.0,7.0)
        ipv = st.slider("IPV",0.0,10.0,7.0)
        idade = st.slider("Idade",7,25,12)
        fase = st.slider("Fase",0,8,3)

    tempo = st.slider(
        "Tempo de Programa",
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

            st.error("🔴 ALTO RISCO")

        elif prob >= 0.40:

            st.warning("🟡 MÉDIO RISCO")

        else:

            st.success("🟢 BAIXO RISCO")

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=prob*100,
                title={
                    "text":"Score de Risco"
                },
                gauge={
                    "axis":{
                        "range":[0,100]
                    }
                }
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        comentario(
            f"O modelo estimou risco de {prob:.1%}.",
            "O Random Forest alcançou aproximadamente 81% de acurácia e ROC-AUC de 88,7%.",
            "Utilizar este indicador para priorizar acompanhamentos."
        )

# =============================================================
# INSIGHTS
# =============================================================

else:

    st.title(
        "💡 Insights Estratégicos"
    )

    st.success(
        "✅ O principal impulsionador do INDE é o IDA."
    )

    st.success(
        "✅ O engajamento influencia diretamente desempenho e IPV."
    )

    st.success(
        "✅ O IPP foi o principal impulsionador do IPV."
    )

    st.success(
        "✅ O modelo identifica aproximadamente 89% dos alunos em risco."
    )

    st.success(
        "✅ Alunos Topázio apresentam desempenho superior em todos os indicadores."
    )

    st.warning(
        """
44,5% dos alunos tendem a superestimar seu próprio desempenho,
indicando oportunidade para ações de autoconhecimento acadêmico.
"""
    )

    st.info(
        """
Recomendações:

1. Monitorar continuamente o IEG
2. Implementar alerta preditivo
3. Atuar nas fases iniciais
4. Reforçar acompanhamento psicopedagógico
5. Trabalhar percepção acadêmica dos alunos
"""
    )


# =============================================================
# DICIONÁRIO
# =============================================================

elif pagina == "📚 Dicionário PEDE":

    st.title("📚 Dicionário dos Indicadores PEDE")

    st.markdown("""
    Esta seção apresenta os principais indicadores utilizados
    pela Passos Mágicos para acompanhamento dos alunos.
    """)

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
### 📈 INDE
**Índice de Desenvolvimento Educacional**

Indicador consolidado que representa o desempenho global do aluno.
""")

        st.info("""
### 📚 IDA
**Indicador de Desempenho Acadêmico**

Mede o desempenho acadêmico do estudante.
""")

        st.info("""
### 🤝 IEG
**Indicador de Engajamento**

Avalia o nível de participação e envolvimento do aluno nas atividades.
""")

        st.info("""
### 🎯 IAN
**Indicador de Adequação ao Nível**

Mede se o aluno está no nível esperado para sua etapa educacional.

• 10 = Em Fase

• 5 = Defasagem Moderada

• 2,5 = Defasagem Severa
""")

    with col2:

        st.info("""
### 🪞 IAA
**Indicador de Autoavaliação**

Representa como o aluno percebe seu próprio desempenho.
""")

        st.info("""
### 🤝 IPS
**Indicador Psicossocial**

Relacionado a aspectos socioemocionais e psicossociais.
""")

        st.info("""
### 🧠 IPP
**Indicador Psicopedagógico**

Avalia aspectos de desenvolvimento psicopedagógico.
""")

        st.info("""
### 🚀 IPV
**Indicador de Ponto de Virada**

Representa sinais de transformação e evolução do estudante.
""")

    st.divider()

    st.subheader("💎 Classificação das Pedras")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.success("""
### ⚪ Quartzo

Necessita maior desenvolvimento.
""")

    with col2:
        st.info("""
### 🔵 Ágata

Desenvolvimento intermediário.
""")

    with col3:
        st.warning("""
### 🟣 Ametista

Bom desempenho geral.
""")

    with col4:
        st.error("""
### 🟠 Topázio

Grupo de destaque do programa.
""")

    st.divider()

    st.subheader("⚠️ Classificações de Defasagem")

    st.markdown("""
🟢 **Em Fase**  
Aluno dentro do nível esperado.

🟡 **Defasagem Moderada**  
Apresenta lacunas de aprendizagem que merecem atenção.

🔴 **Defasagem Severa**  
Necessita acompanhamento prioritário.
""")
