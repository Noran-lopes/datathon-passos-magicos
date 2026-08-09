import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Passos Mágicos Analytics",
    page_icon="🎓",
    layout="wide"
)

# =====================================================
# ESTILO
# =====================================================

st.markdown("""
<style>

.main .block-container {
    padding-top: 1rem;
}

div[data-testid="stMetric"]{
    background-color:#131a2a;
    padding:15px;
    border-radius:12px;
    border:1px solid #2d3748;
}

h1,h2,h3{
    color:#4F8BF9;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNÇÕES
# =====================================================

@st.cache_data
def carregar_dados():

    return pd.read_csv(
        "data/base_analitica_consolidada.csv"
    )


@st.cache_resource
def carregar_modelo():

    try:

        modelo = joblib.load(
            "models/modelo_risco.pkl"
        )

        imputer = joblib.load(
            "models/imputer.pkl"
        )

        return modelo, imputer

    except:

        return None, None


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


# =====================================================
# DADOS
# =====================================================

df = carregar_dados()

modelo, imputer = carregar_modelo()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎓 Passos Mágicos")

st.sidebar.markdown("""
### Analytics Platform

Monitoramento Educacional,
Efetividade e Predição de Risco.
""")

pagina = st.sidebar.radio(
    "Menu",
    [
        "🏠 Visão Executiva",
        "📈 Jornada dos Alunos",
        "🤖 Simulador de Risco",
        "💡 Insights Estratégicos",
        "📖 Dicionário PEDE"
    ]
)

# =====================================================
# FILTROS
# =====================================================

st.sidebar.markdown("---")

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

# =====================================================
# DICIONÁRIO
# =====================================================

if pagina == "📖 Dicionário PEDE":

    st.title(
        "📖 Dicionário dos Indicadores PEDE"
    )

    col1,col2 = st.columns(2)

    with col1:

        st.info("""
### 📈 INDE

Índice de Desenvolvimento Educacional

Indicador consolidado que representa o desenvolvimento global do aluno.
""")

        st.info("""
### 📚 IDA

Indicador de Desempenho Acadêmico

Avalia o desempenho escolar do estudante.
""")

        st.info("""
### 🤝 IEG

Indicador de Engajamento

Representa participação e envolvimento nas atividades.
""")

        st.info("""
### 🎯 IAN

Indicador de Adequação ao Nível

Avalia se o aluno está no nível esperado.
""")

    with col2:

        st.info("""
### 🪞 IAA

Indicador de Autoavaliação

Percepção do aluno sobre seu próprio desempenho.
""")

        st.info("""
### 🤝 IPS

Indicador Psicossocial

Aspectos socioemocionais e contexto social.
""")

        st.info("""
### 🧠 IPP

Indicador Psicopedagógico

Aspectos ligados ao acompanhamento psicopedagógico.
""")

        st.info("""
### 🚀 IPV

Indicador de Ponto de Virada

Representa sinais de transformação e evolução do aluno.
""")

    st.divider()

    st.subheader(
        "💎 Classificação das Pedras"
    )

    c1,c2,c3,c4 = st.columns(4)

    c1.success("Quartzo")
    c2.info("Ágata")
    c3.warning("Ametista")
    c4.error("Topázio")

    st.stop()

# =====================================================
# VISÃO EXECUTIVA
# =====================================================

elif pagina == "🏠 Visão Executiva":

    st.title("🎓 Passos Mágicos Analytics")

    st.markdown("""
## Resumo Executivo

Esta análise consolida a jornada educacional dos alunos
atendidos pela Passos Mágicos entre 2022 e 2024.

A base analítica contém registros anuais dos estudantes,
permitindo acompanhar evolução, desempenho e fatores de risco.
""")

    # =====================================================
    # KPIS
    # =====================================================

    alunos_unicos = df["RA"].nunique()

    registros = len(df)

    inde_medio = round(
        df["INDE"].mean(),
        2
    )

    ida_medio = round(
        df["IDA"].mean(),
        2
    )

    ian_medio = round(
        df["IAN"].mean(),
        2
    )

    col1,col2,col3,col4,col5 = st.columns(5)

    col1.metric(
        "👨‍🎓 Alunos Únicos",
        alunos_unicos
    )

    col2.metric(
        "📄 Registros",
        registros,
        help="Cada registro representa um aluno em determinado ano."
    )

    col3.metric(
        "📈 INDE Médio",
        inde_medio
    )

    col4.metric(
        "📚 IDA Médio",
        ida_medio
    )

    col5.metric(
        "🎯 IAN Médio",
        ian_medio
    )

    st.divider()

    # =====================================================
    # PRINCIPAIS DESCOBERTAS
    # =====================================================

    st.subheader("📌 Principais Descobertas")

    c1,c2 = st.columns(2)

    with c1:

        st.success("""
✅ O programa acompanhou mais de mil alunos ao longo dos três anos.

✅ A maior parte dos estudantes encontra-se em Defasagem Moderada.

✅ O desempenho acadêmico é o principal impulsionador do desenvolvimento.
""")

    with c2:

        st.success("""
✅ O engajamento influencia diretamente os resultados.

✅ Alunos Topázio apresentam os melhores indicadores.

✅ O modelo preditivo alcançou ROC-AUC de aproximadamente 88,7%.
""")

    st.divider()

    # =====================================================
    # EVOLUÇÃO DOS INDICADORES
    # =====================================================

    st.subheader(
        "📈 Evolução dos Indicadores Educacionais"
    )

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
        title="Evolução Média dos Indicadores"
    )

    fig.update_layout(
        legend_title="Indicador"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    comentario(
        "Os indicadores apresentaram comportamento estável ou crescente durante o período analisado.",
        "O IAN demonstrou evolução consistente, sugerindo redução da defasagem educacional.",
        "Priorizar ações voltadas às fases iniciais para acelerar o desenvolvimento."
    )

    st.divider()

    # =====================================================
    # DEFASAGEM
    # =====================================================

    st.subheader(
        "🎯 Perfil da Defasagem Educacional"
    )

    col1,col2 = st.columns(2)

    with col1:

        perfil_defasagem = (
            df["CLASSE_DEFASAGEM"]
            .value_counts()
            .reset_index()
        )

        perfil_defasagem.columns = [
            "Classe",
            "Quantidade"
        ]

        fig = px.pie(
            perfil_defasagem,
            names="Classe",
            values="Quantidade",
            hole=0.55,
            title="Distribuição da Defasagem"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        if "ANO" in df.columns:

            evolucao_defasagem = (
                df.groupby(
                    [
                        "ANO",
                        "CLASSE_DEFASAGEM"
                    ]
                )
                .size()
                .reset_index(
                    name="Quantidade"
                )
            )

            fig = px.bar(
                evolucao_defasagem,
                x="ANO",
                y="Quantidade",
                color="CLASSE_DEFASAGEM",
                barmode="stack",
                title="Evolução das Classes de Defasagem"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    comentario(
        "A Defasagem Moderada representa a maior parcela da população analisada.",
        "Este grupo possui maior potencial de ganho com intervenções direcionadas.",
        "Criar ações preventivas antes da migração para Defasagem Severa."
    )

    st.divider()

    # =====================================================
    # PEDRAS
    # =====================================================

    st.subheader(
        "💎 Perfil das Pedras"
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

        perfil_pedra = (
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
            perfil_pedra,
            x="Pedra",
            y="INDE",
            color="Pedra",
            title="INDE Médio por Pedra"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    comentario(
        "Os alunos classificados como Topázio apresentam os maiores níveis de desenvolvimento.",
        "Existe uma distinção clara entre os grupos extremos (Topázio e Quartzo).",
        "Utilizar o perfil Topázio como referência para programas de desenvolvimento."
    )
    # =====================================================
# JORNADA DOS ALUNOS
# =====================================================

elif pagina == "📈 Jornada dos Alunos":

    st.title("📈 Jornada dos Alunos")

    st.markdown("""
Esta seção apresenta a evolução dos indicadores educacionais
e os fatores que diferenciam os alunos de maior desempenho.
""")

    # =====================================================
    # ABAS
    # =====================================================

    aba1, aba2, aba3, aba4 = st.tabs(
        [
            "📚 Desempenho x Engajamento",
            "💎 Perfil das Pedras",
            "📈 Efetividade",
            "⏳ Permanência"
        ]
    )

    # =====================================================
    # ABA 1
    # =====================================================

    with aba1:

        st.subheader(
            "📚 Relação entre Engajamento e Desempenho"
        )

        fig = px.scatter(
            df,
            x="IEG",
            y="IDA",
            color="Pedra",
            opacity=0.7,
            hover_data=[
                "ANO",
                "INDE"
            ]
        )

        fig.update_layout(
            title="Engajamento (IEG) x Desempenho Acadêmico (IDA)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        correlacao = round(
            df["IEG"].corr(df["IDA"]),
            2
        )

        st.metric(
            "Correlação IEG x IDA",
            correlacao
        )

        comentario(
            "Existe uma relação positiva entre engajamento e desempenho acadêmico.",
            f"A correlação observada foi de aproximadamente {correlacao}.",
            "Monitorar quedas no IEG como sinal precoce de risco."
        )

    # =====================================================
    # ABA 2
    # =====================================================

    with aba2:

        st.subheader(
            "💎 Perfil dos Grupos de Alunos"
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
        )

        if (
            "Topázio" in perfil.index
            and
            "Quartzo" in perfil.index
        ):

            categorias = [
                "INDE",
                "IDA",
                "IEG",
                "IAN",
                "IPV"
            ]

            fig = go.Figure()

            fig.add_trace(
                go.Scatterpolar(
                    r=perfil.loc["Topázio"],
                    theta=categorias,
                    fill="toself",
                    name="Topázio"
                )
            )

            fig.add_trace(
                go.Scatterpolar(
                    r=perfil.loc["Quartzo"],
                    theta=categorias,
                    fill="toself",
                    name="Quartzo"
                )
            )

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0,10]
                    )
                ),
                showlegend=True,
                title="Topázio x Quartzo"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        perfil_reset = (
            perfil
            .reset_index()
        )

        fig = px.bar(
            perfil_reset,
            x="Pedra",
            y=[
                "INDE",
                "IDA",
                "IEG",
                "IAN",
                "IPV"
            ],
            barmode="group",
            title="Indicadores Médios por Pedra"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        comentario(
            "Topázio apresenta vantagem consistente em todos os indicadores.",
            "O diferencial não está apenas no desempenho acadêmico, mas também no engajamento.",
            "Utilizar características do grupo Topázio como referência para programas de aceleração."
        )

    # =====================================================
    # ABA 3
    # =====================================================

    with aba3:

        st.subheader(
            "📈 Efetividade do Programa"
        )

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
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig2 = px.line(
            evolucao,
            x="ANO",
            y="IAN",
            markers=True,
            title="Evolução da Adequação ao Nível (IAN)"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        comentario(
            "Os indicadores apresentaram estabilidade e evolução ao longo dos anos monitorados.",
            "O IAN mostrou evolução consistente, indicando redução gradual da defasagem.",
            "Expandir iniciativas voltadas para alunos em fases iniciais."
        )

    # =====================================================
    # ABA 4
    # =====================================================

    with aba4:

        st.subheader(
            "⏳ Impacto do Tempo de Programa"
        )

        perfil_tempo = (
            df.groupby(
                "FAIXA_PERMANENCIA"
            )
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
            perfil_tempo,
            x="FAIXA_PERMANENCIA",
            y="INDE",
            color="FAIXA_PERMANENCIA",
            title="INDE Médio por Tempo de Permanência"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig2 = px.box(
            df,
            x="FAIXA_PERMANENCIA",
            y="INDE",
            color="FAIXA_PERMANENCIA",
            title="Distribuição do INDE por Tempo de Programa"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        comentario(
            "Alunos com maior permanência tendem a apresentar melhores indicadores.",
            "Existe evidência de ganho acumulado ao longo da jornada no programa.",
            "Focar em estratégias de retenção pode aumentar o impacto educacional."
        )
        # =====================================================
# SIMULADOR DE RISCO
# =====================================================

elif pagina == "🤖 Simulador de Risco":

    st.title("🤖 Simulador de Risco Educacional")

    st.markdown("""
Utilize os indicadores do aluno para estimar a probabilidade
de risco educacional.

O objetivo é identificar estudantes que podem precisar de
acompanhamento preventivo.
""")

    st.info("""
### 📚 Como interpretar os indicadores

📈 INDE → Desenvolvimento geral

📚 IDA → Desempenho acadêmico

🤝 IEG → Engajamento

🪞 IAA → Autoavaliação

🤝 IPS → Psicossocial

🧠 IPP → Psicopedagógico

🚀 IPV → Ponto de Virada

🎯 IAN → Adequação ao Nível
""")

    if modelo is None:

        st.error(
            "Modelo de Machine Learning não encontrado."
        )

        st.stop()

    # =====================================================
    # INPUTS
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        ida = st.slider(
            "📚 IDA",
            0.0,
            10.0,
            6.0
        )

        ieg = st.slider(
            "🤝 IEG",
            0.0,
            10.0,
            7.0
        )

        iaa = st.slider(
            "🪞 IAA",
            0.0,
            10.0,
            7.0
        )

        ips = st.slider(
            "🤝 IPS",
            0.0,
            10.0,
            7.0
        )

    with col2:

        ipp = st.slider(
            "🧠 IPP",
            0.0,
            10.0,
            7.0
        )

        ipv = st.slider(
            "🚀 IPV",
            0.0,
            10.0,
            7.0
        )

        idade = st.slider(
            "📅 Idade",
            7,
            25,
            12
        )

        fase = st.slider(
            "🏫 Fase",
            0,
            8,
            3
        )

    tempo_programa = st.slider(
        "⏳ Tempo de Programa (anos)",
        0,
        10,
        2
    )

    st.divider()

    # =====================================================
    # PREDIÇÃO
    # =====================================================

    if st.button(
        "🔍 Calcular Probabilidade de Risco",
        use_container_width=True
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
            "TEMPO_PROGRAMA":[tempo_programa]

        })

        entrada_imputada = imputer.transform(
            entrada
        )

        prob = modelo.predict_proba(
            entrada_imputada
        )[0][1]

        # =====================================================
        # RESULTADO
        # =====================================================

        st.subheader(
            "Resultado da Análise"
        )

        col1,col2 = st.columns([1,2])

        with col1:

            st.metric(
                "Probabilidade",
                f"{prob:.1%}"
            )

        with col2:

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

        # =====================================================
        # GAUGE
        # =====================================================

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
                    },

                    "bar":{
                        "color":"darkblue"
                    },

                    "steps":[

                        {
                            "range":[0,40],
                            "color":"green"
                        },

                        {
                            "range":[40,70],
                            "color":"gold"
                        },

                        {
                            "range":[70,100],
                            "color":"red"
                        }

                    ]
                }
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================================
        # EXPLICAÇÃO
        # =====================================================

        st.subheader(
            "🧠 Interpretação"
        )

        if prob >= 0.70:

            st.error("""
### Principais sinais observados

• Elevada probabilidade de vulnerabilidade educacional.

• Recomendado acompanhamento prioritário.

• Necessidade de monitoramento contínuo.

• Intervenções preventivas devem ser consideradas.
""")

        elif prob >= 0.40:

            st.warning("""
### Atenção

• O aluno apresenta sinais moderados de risco.

• Recomenda-se monitoramento periódico.

• Engajamento e desempenho devem ser acompanhados.
""")

        else:

            st.success("""
### Situação Favorável

• Baixa probabilidade de risco.

• Indicadores demonstram trajetória positiva.

• Recomendado manter acompanhamento regular.
""")

        # =====================================================
        # DIAGNÓSTICO RÁPIDO
        # =====================================================

        st.subheader(
            "📋 Diagnóstico Rápido"
        )

        pontos_alerta = []

        if ida < 5:
            pontos_alerta.append(
                "Baixo desempenho acadêmico (IDA)"
            )

        if ieg < 5:
            pontos_alerta.append(
                "Baixo engajamento (IEG)"
            )

        if ipv < 5:
            pontos_alerta.append(
                "Baixo ponto de virada (IPV)"
            )

        if ipp < 5:
            pontos_alerta.append(
                "Baixo indicador psicopedagógico (IPP)"
            )

        if len(pontos_alerta) == 0:

            st.success(
                "Nenhum fator crítico identificado."
            )

        else:

            for alerta in pontos_alerta:

                st.warning(
                    alerta
                )

        comentario(
            f"O modelo estimou uma probabilidade de risco de {prob:.1%}.",
            "O algoritmo Random Forest apresentou ROC-AUC próximo de 88,7%, demonstrando alta capacidade de separação entre grupos.",
            "Utilizar o score de risco para apoiar ações preventivas e priorização do acompanhamento."
        )

    # =====================================================
    # SOBRE O MODELO
    # =====================================================

    st.divider()

    st.subheader(
        "⚙️ Sobre o Modelo"
    )

    st.info("""
**Modelo utilizado:** Random Forest

✅ Accuracy aproximada: 81%

✅ ROC-AUC aproximado: 88,7%

✅ Recall para alunos em risco: ~89%

O objetivo do modelo não é substituir avaliações pedagógicas,
mas apoiar decisões preventivas através de dados.
""")

# =====================================================
# INSIGHTS ESTRATÉGICOS
# =====================================================

elif pagina == "💡 Insights Estratégicos":

    st.title("💡 Insights Estratégicos")

    st.markdown("""
Esta seção consolida os principais aprendizados obtidos a partir
das análises exploratórias e do modelo preditivo.
""")

    # =====================================================
    # PRINCIPAIS ACHADOS
    # =====================================================

    st.subheader("📌 Principais Achados")

    col1, col2 = st.columns(2)

    with col1:

        st.success("""
### 📚 IDA é o principal impulsionador do INDE

O desempenho acadêmico apresentou a maior influência
sobre o desenvolvimento global dos alunos.
""")

        st.success("""
### 🤝 Engajamento impulsiona desempenho

Alunos mais engajados tendem a apresentar
melhores resultados acadêmicos.
""")

        st.success("""
### 🚀 IPV está fortemente associado ao IPP

O acompanhamento psicopedagógico mostrou forte
relação com o Ponto de Virada.
""")

    with col2:

        st.success("""
### 💎 Topázio representa o perfil de excelência

Os alunos Topázio lideram todos os indicadores.
""")

        st.success("""
### 🎯 Defasagem Moderada concentra oportunidade

É o grupo com maior potencial de ganho educacional.
""")

        st.success("""
### 🤖 O modelo prevê risco com alta precisão

Recall aproximado de 89%.
ROC-AUC aproximado de 88,7%.
""")

    st.divider()

    # =====================================================
    # RECOMENDAÇÕES
    # =====================================================

    st.subheader("🎯 Recomendações para a Passos Mágicos")

    st.info("""
### 1️⃣ Criar Monitoramento Contínuo de Engajamento

O IEG demonstrou forte relação com o desempenho acadêmico.

Acompanhamentos preventivos podem ser iniciados
quando houver queda de engajamento.
""")

    st.info("""
### 2️⃣ Priorizar Alunos em Defasagem Moderada

Este grupo representa a maior parcela da base e possui
elevado potencial de evolução.

Intervenções precoces tendem a gerar maior retorno.
""")

    st.info("""
### 3️⃣ Expandir Estratégias Psicopedagógicas

O IPP apresentou forte associação com o IPV.

Investimentos nessa dimensão podem acelerar
a transformação dos alunos.
""")

    st.info("""
### 4️⃣ Implantar Alerta Preditivo de Risco

Utilizar o modelo de Machine Learning para destacar
alunos prioritários para acompanhamento.

Isso permite atuação antes do agravamento das dificuldades.
""")

    st.info("""
### 5️⃣ Replicar Boas Práticas dos Alunos Topázio

Topázio apresentou os melhores resultados em:

• INDE

• IDA

• IEG

• IPV

Esses padrões podem orientar novos programas
de desenvolvimento.
""")

    st.divider()

    # =====================================================
    # ROADMAP
    # =====================================================

    st.subheader("🛣️ Roadmap de Implementação")

    roadmap = pd.DataFrame({

        "Prazo":[
            "Curto Prazo",
            "Curto Prazo",
            "Médio Prazo",
            "Longo Prazo"
        ],

        "Ação":[
            "Monitoramento de Engajamento",
            "Painel de Risco",
            "Programa Psicopedagógico",
            "Personalização do Acompanhamento"
        ]
    })

    st.dataframe(
        roadmap,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================================
    # IMPACTO
    # =====================================================

    st.subheader("📈 Potencial de Impacto")

    impacto = pd.DataFrame({

        "Iniciativa":[

            "Monitoramento de Engajamento",

            "Alerta de Risco",

            "Suporte Psicopedagógico",

            "Programa Topázio"
        ],

        "Impacto Esperado":[

            "Alto",

            "Muito Alto",

            "Alto",

            "Médio"
        ]
    })

    fig = px.bar(
        impacto,
        x="Iniciativa",
        y=[
            3,
            4,
            3,
            2
        ],
        color="Impacto Esperado",
        title="Potencial Relativo de Impacto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # CONCLUSÃO
    # =====================================================

    st.subheader("✅ Conclusão Final")

    st.success("""
A análise indica que a Passos Mágicos gera impacto
positivo na trajetória educacional dos alunos.

Os resultados mostram que:

• Engajamento influencia desempenho.

• Desempenho influencia desenvolvimento.

• O programa reduz sinais de defasagem.

• É possível identificar alunos em risco
antes da ocorrência de resultados negativos.

A combinação entre análise de dados e acompanhamento
educacional pode ampliar ainda mais o impacto social
da organização.
""")
