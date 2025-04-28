import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Rastreamento e Vacinação", layout="centered")

st.markdown("# 🏥 Assistente de Rastreamento e Vacinação")

# Formulário principal
with st.form("formulario"):
    sexo = st.selectbox("Sexo biológico", ["", "Feminino", "Masculino"])
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    profissional_saude = st.checkbox("Profissional de Saúde")

    st.markdown("### 📋 Fatores clínicos e antecedentes")
    col1, col2 = st.columns(2)
    with col1:
        imc_alto = st.checkbox("IMC ≥ 25")
        tabagista = st.checkbox("Tabagista ou ex-tabagista")
        gestante = st.checkbox("Gestante")
        ca_mama = st.checkbox("Histórico familiar de câncer de mama")
        ca_prostata = st.checkbox("Histórico familiar de câncer de próstata")
        ca_colon = st.checkbox("Histórico familiar de câncer colorretal")
    with col2:
        dm = st.checkbox("Diabetes Mellitus")
        dpoc = st.checkbox("DPOC")
        imunossuprimido = st.checkbox("Imunossuprimido")
        cardiovascular = st.checkbox("Doença cardiovascular crônica")
        renal = st.checkbox("Doença renal crônica")
        hepatopatia = st.checkbox("Doença hepática crônica")
        cancer = st.checkbox("Neoplasia ativa")

    submit = st.form_submit_button("Gerar Recomendações")

if submit:
    respostas = []

    # Rastreio
    if sexo == "Feminino":
        if 40 <= idade <= 74:
            respostas.append("✔️ Mamografia anual recomendada. [Ver diretriz (PDF)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/cancer%20mama%20rastreo.pdf)")
        if ca_mama and idade >= 35:
            respostas.append("✔️ Rastreio antecipado para câncer de mama.")
        if 25 <= idade <= 65:
            respostas.append("✔️ Papanicolau recomendado. [Ver diretriz (PDF)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/diretrizes_para_o_rastreamento_do_cancer_do_colo_do_utero_2016_corrigido.pdf)")

    if sexo == "Masculino":
        if idade >= 50:
            respostas.append("✔️ PSA e USG prostático recomendados. [Ver diretriz (PDF)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/rastreamento_prostat_2023_sociedades.pdf)")
        if ca_prostata and idade >= 45:
            respostas.append("✔️ Rastreio antecipado para câncer de próstata.")

    if ca_colon and idade >= 38:
        respostas.append("✔️ Colonoscopia antecipada recomendada. [Ver diretriz (PDF)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/CÂNCER%20COLORRETAL_DO%20DIAGNÓSTICO%20AO%20TRATAMENTO.pdf)")

    if tabagista and 50 <= idade <= 80:
        respostas.append("✔️ TC de Tórax de baixa dose para tabagistas. [Ver diretriz (PDF)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/tabagismo%20ca%20pulmao.pdf)")

    if imc_alto or dm or cardiovascular or renal or hepatopatia:
        respostas.append("✔️ Avaliação metabólica recomendada. [Ver diretriz (PDF)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/Diretrizes-Brasileiras-de-Obesidade-2016.pdf)")

    if idade >= 50:
        respostas.append("✔️ Avaliação para gamopatias monoclonais. [Ver diretriz (PDF)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/Gamopatias_monoclonais_criterios_diagnosticos.pdf)")

    # Vacinas
    if profissional_saude:
        respostas.append("💉 Recomendada vacinação DTPa, Hepatite B, Influenza, COVID-19 (profissionais de saúde).")

    if gestante:
        respostas.append("💉 Recomendada vacinação DTPa (20–36 semanas) e VSR (32–36 semanas) para gestantes.")

    if dpoc or cardiovascular or renal or imunossuprimido or gestante or dm or cancer or hepatopatia:
        respostas.append("💉 Indicação de vacinação pneumocócica 20V + 23V; considerar herpes-zóster; considerar vacina para dengue.")

    if 18 <= idade <= 45:
        respostas.append("💉 Vacinação contra HPV recomendada.")

    # Exibição das respostas
    if respostas:
        st.success("✅ Recomendações:")
        for r in respostas:
            st.markdown(f"- {r}")

        st.info("Calendários Oficiais de Vacinação – SBIm")
        st.markdown("""
        Consulte abaixo os esquemas vacinais recomendados pela SBIm:

        - [Ver Calendário SBIm – Adultos (20–59 anos)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/calend-pg-adulto-20-.pdf)
        - [Ver Calendário SBIm – Idosos (≥ 60 anos)](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/calend-sbim-idoso.pdf)
        - [Ver Calendário SBIm – Gestantes](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/calend-sbim-gestante.pdf)
        - [Ver Calendário SBIm – Profissionais de Saúde](https://raw.githubusercontent.com/vitordominato/ambulatorio/main/calend-sbim-ocupacio.pdf)
        """)
    else:
        st.info("Nenhuma recomendação encontrada com os critérios informados.")

