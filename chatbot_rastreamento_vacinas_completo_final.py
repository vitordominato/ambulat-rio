
import streamlit as st
from pathlib import Path
from fpdf import FPDF

st.set_page_config(page_title="Rastreamento e Vacinas - Institucional", layout="centered")
st.title("🩺 Assistente de Rastreamento e Vacinação")

st.markdown("### ✅ Preencha os dados do paciente:")

with st.form("formulario"):
    sexo = st.selectbox("Sexo:", ["", "Feminino", "Masculino"])
    idade = st.number_input("Idade:", 0, 120, step=1)
    profissional_saude = st.checkbox("Profissional de Saúde")
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
        imunossuprimido = st.checkbox("Imunossuprimido (por doença ou medicamento)")
        cardiovascular = st.checkbox("Doença cardiovascular crônica")
        renal = st.checkbox("Doença renal crônica")
        hepatopatia = st.checkbox("Doença hepática crônica")
        cancer = st.checkbox("Neoplasia ativa")
    submit = st.form_submit_button("Gerar Recomendações")

def gerar_pdf(titulo, linhas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, titulo, ln=True)
    pdf.set_font("Arial", "", 12)
    for linha in linhas:
        pdf.multi_cell(0, 10, linha)
    nome_pdf = "resumo_recomendacoes.pdf"
    pdf.output(nome_pdf)
    return nome_pdf

if submit:
    respostas = []

    # Rastreio clínico
    if sexo == "Feminino":
        if 40 <= idade <= 74:
            respostas.append("✔️ Mamografia anual (40–74 anos). Encaminhar à Mastologia. [ACS 2022]")
        if ca_mama and idade >= 35:
            respostas.append("✔️ Mamografia antecipada (≥35 anos) por histórico. [Ministério da Saúde 2023]")
        if 25 <= idade <= 65:
            respostas.append("✔️ Papanicolau (25–65 anos). Encaminhar à Ginecologia. [INCA]")

    if sexo == "Masculino":
        if idade >= 50:
            respostas.append("✔️ PSA e USG prostático (≥50 anos). Encaminhar à Urologia. [SBU/SBOC 2023]")
        if ca_prostata and idade >= 45:
            respostas.append("✔️ Rastreamento antecipado de próstata (≥45 anos). [SBU/SBOC 2023]")

    if ca_colon and idade >= 38:
        respostas.append("✔️ Colonoscopia antecipada por histórico familiar. [INCA]")

    if tabagista:
        if 50 <= idade <= 80:
            respostas.append("✔️ TC de tórax de baixa dose (50–80 anos). Encaminhar à Pneumologia. [NLST]")
        else:
            respostas.append("ℹ️ TC de tórax recomendada apenas entre 50 e 80 anos. [NLST]")

    if imc_alto or dm or cardiovascular or renal or hepatopatia:
        respostas.append("✔️ Avaliação metabólica: perfil lipídico, glicemia, hemoglobina glicada, HOMA-IR, TSH. [Diretrizes de Obesidade 2016]")

    if idade >= 50:
        respostas.append("✔️ Eletroforese e imunofixação para rastreio de gamopatias monoclonais. [IMWG]")

    # Vacinas – Profissionais de saúde
    if profissional_saude:
        respostas.append("💉 DTPa: reforço a cada 10 anos. [PNI/SBIm]")
        respostas.append("💉 Hepatite B: 3 doses (0, 1, 6 meses). [PNI/SBIm]")
        respostas.append("💉 Gripe anual. [PNI/SBIm]")
        respostas.append("💉 COVID-19: reforços conforme calendário. [PNI]")

    # Vacinas por comorbidade / gestação
    if gestante:
        respostas.append("💉 DTPa: 1 dose entre 20–36 semanas. [PNI/SBIm]")
        respostas.append("💉 VSR (Abrysvo): entre 32–36 semanas. [SBIm/FDA]")

    if dpoc or cardiovascular or renal or imunossuprimido or gestante or dm or cancer or hepatopatia:
        respostas.append("💉 Pneumocócica 20V + 23V: aplicar 20V + 23V após 6–12 meses. [SBIm]")
        respostas.append("💉 Herpes-zóster: 2 doses (0, 2 meses). [SBIm]")
        if idade >= 60:
            respostas.append("💉 Dengue: indicada entre 4 e 60 anos conforme risco. [SBIm/PNI]")

    if idade >= 18 and idade <= 45:
        respostas.append("💉 HPV: 2 ou 3 doses conforme idade e condições. [SBIm/PNI]")

    # Apresentação dos resultados
    if respostas:
        st.subheader("📋 Recomendações Personalizadas:")
        for r in respostas:
            st.markdown(f"- {r}")
        if st.button("📄 Gerar PDF com resumo"):
            nome_pdf = gerar_pdf("Resumo de Recomendações", respostas)
            with open(nome_pdf, "rb") as f:
                st.download_button("⬇️ Baixar Resumo em PDF", f, file_name=nome_pdf)
    else:
        st.warning("⚠️ Nenhuma recomendação identificada com os dados fornecidos.")
