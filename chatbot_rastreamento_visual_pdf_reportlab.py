
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from pathlib import Path

st.set_page_config(page_title="Rastreamento e Vacinação", layout="centered")

st.markdown("""# 🏥 Assistente de Rastreamento e Vacinação
Preencha os dados do paciente para gerar orientações personalizadas de rastreio e vacinação.
""")

# Formulário guiado
with st.form("formulario"):
    sexo = st.selectbox("🧬 Sexo biológico", ["", "Feminino", "Masculino"])
    idade = st.number_input("🎂 Idade", min_value=0, max_value=120, step=1)
    profissional_saude = st.checkbox("🩺 Profissional de Saúde")

    st.markdown("### 📋 Fatores clínicos e antecedentes")
    col1, col2 = st.columns(2)
    with col1:
        imc_alto = st.checkbox("IMC ≥ 25")
        tabagista = st.checkbox("Tabagista ou ex-tabagista")
        gestante = st.checkbox("Gestante")
        ca_mama = st.checkbox("Hist. familiar de câncer de mama")
        ca_prostata = st.checkbox("Hist. familiar de câncer de próstata")
        ca_colon = st.checkbox("Hist. familiar de câncer colorretal")
    with col2:
        dm = st.checkbox("Diabetes Mellitus")
        dpoc = st.checkbox("DPOC")
        imunossuprimido = st.checkbox("Imunossuprimido (por doença ou medicação)")
        cardiovascular = st.checkbox("Doença cardiovascular crônica")
        renal = st.checkbox("Doença renal crônica")
        hepatopatia = st.checkbox("Doença hepática crônica")
        cancer = st.checkbox("Neoplasia ativa")

    submit = st.form_submit_button("🧾 Gerar Recomendações")

# Função para gerar PDF com ReportLab
def gerar_pdf(titulo, linhas, caminho_destino):
    c = canvas.Canvas(caminho_destino, pagesize=A4)
    largura, altura = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(largura / 2, altura - 2 * cm, "Hospital Universitário – Protocolo de Rastreamento")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, altura - 3 * cm, titulo)

    c.setFont("Helvetica", 11)
    y = altura - 4 * cm
    for linha in linhas:
        if y < 2 * cm:
            c.showPage()
            y = altura - 2 * cm
            c.setFont("Helvetica", 11)
        c.drawString(2 * cm, y, linha)
        y -= 1 * cm

    c.save()

if submit:
    respostas = []

    if sexo == "Feminino":
        if 40 <= idade <= 74:
            respostas.append("✔️ Mamografia anual. [Ver diretriz (PDF)](https://github.com/vitordominato/ambulat-rio/blob/main/cancer%20mama%20rastreo.pdf)")
        if ca_mama and idade >= 35:
            respostas.append("✔️ Mamografia antecipada por histórico familiar.")
        if 25 <= idade <= 65:
            respostas.append("✔️ Papanicolau. [Ver diretriz (PDF)](https://github.com/vitordominato/ambulat-rio/blob/main/diretrizes_para_o_rastreamento_do_cancer_do_colo_do_utero_2016_corrigido.pdf)")

    if sexo == "Masculino":
        if idade >= 50:
            respostas.append("✔️ PSA e USG prostático. [Ver diretriz (PDF)](https://github.com/vitordominato/ambulat-rio/blob/main/rastreamento_prostat_2023_sociedades.pdf)")
        if ca_prostata and idade >= 45:
            respostas.append("✔️ Rastreio antecipado de próstata.")

    if ca_colon and idade >= 38:
        respostas.append("✔️ Colonoscopia antecipada. [Ver diretriz (PDF)](https://github.com/vitordominato/ambulat-rio/blob/main/CÂNCER%20COLORRETAL_DO%20DIAGNÓSTICO%20AO%20TRATAMENTO.pdf)")

    if tabagista and 50 <= idade <= 80:
        respostas.append("✔️ TC de tórax de baixa dose. [Ver diretriz (PDF)](https://github.com/vitordominato/ambulat-rio/blob/main/tabagismo%20ca%20pulmao.pdf)")

    if imc_alto or dm or cardiovascular or renal or hepatopatia:
        respostas.append("✔️ Avaliação metabólica. [Ver diretriz (PDF)](https://github.com/vitordominato/ambulat-rio/blob/main/Diretrizes-Brasileiras-de-Obesidade-2016.pdf)")

    if idade >= 50:
        respostas.append("✔️ Rastreio de gamopatias. [Ver diretriz (PDF)](https://github.com/vitordominato/ambulat-rio/blob/main/Gamopatias_monoclonais_criterios_diagnosticos.pdf)")

    if profissional_saude:
        respostas.append("💉 DTPa, Hepatite B (0,1,6 meses), Gripe, COVID-19. [SBIm/PNI]")

    if gestante:
        respostas.append("💉 DTPa (20–36 semanas), VSR (32–36 semanas).")

    if dpoc or cardiovascular or renal or imunossuprimido or gestante or dm or cancer or hepatopatia:
        respostas.append("💉 Pneumo 20V + 23V; Herpes-zóster (0, 2 meses); considerar Dengue. [SBIm]")

    if 18 <= idade <= 45:
        respostas.append("💉 HPV: 2 ou 3 doses conforme idade e imunidade.")

    if respostas:
        st.success("✅ Recomendações geradas com sucesso!")
        for r in respostas:
            st.markdown(f"- {r}")
        if st.button("📄 Baixar Resumo em PDF"):
            nome_pdf = "resumo_rastreamento.pdf"
            gerar_pdf("Resumo de Recomendacoes Personalizadas", respostas, nome_pdf)
            with open(nome_pdf, "rb") as f:
                st.download_button("⬇️ Download do PDF", f, file_name=nome_pdf, mime="application/pdf")
    else:
        st.info("⚠️ Nenhuma recomendação encontrada com os critérios informados.")
