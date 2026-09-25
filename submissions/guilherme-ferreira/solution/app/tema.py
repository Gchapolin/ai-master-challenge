"""Visual do G4 aplicado por CSS. O config.toml não serve: no Streamlit Cloud, com o app numa
subpasta, ele teria de ficar na raiz do repositório."""
import base64
from pathlib import Path

import streamlit as st

AZUL = "#001F35"
DOURADO = "#B9915B"
DOURADO_ESCURO = "#8A6A3F"
OFF_WHITE = "#F5F4F3"
RODAPE = "Protótipo de candidato ao AI Master Challenge, sem vínculo oficial com o G4"
LOGO = Path(__file__).resolve().parent / "assets" / "logo_g4.svg"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital@1&family=Manrope:wght@200;400;600;800&display=swap');
.stApp {{ background: {OFF_WHITE}; color: {AZUL}; font-family: 'Manrope', sans-serif; }}
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp li, .stApp label {{ font-family: 'Manrope', sans-serif; color: {AZUL}; }}
.stApp h2, .stApp h3 {{ font-weight: 400; }}
header[data-testid="stHeader"] {{ background: {AZUL}; }}
header[data-testid="stHeader"] a, header[data-testid="stHeader"] span, header[data-testid="stHeader"] p {{ color: {OFF_WHITE}; }}
.radar-cabecalho {{ background: {AZUL}; border-radius: 10px; padding: 18px 24px; display: flex; flex-wrap: wrap;
  align-items: center; gap: 12px 20px; margin-bottom: 12px; }}
.radar-cabecalho img {{ height: 32px; }}
.radar-cabecalho h1 {{ color: {OFF_WHITE} !important; font-weight: 200; font-size: 1.9rem; margin: 0; padding: 0; }}
.radar-cabecalho em {{ font-family: 'Libre Baskerville', serif; font-style: italic; color: {DOURADO}; }}
div[data-testid="stMetric"] {{ background: #FFFFFF; border-top: 2px solid {DOURADO_ESCURO}; border-radius: 10px; padding: 12px 16px; }}
div[data-testid="stMetricValue"] {{ color: {AZUL}; font-weight: 600; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ background: #FFFFFF; border-radius: 10px; }}
.stButton > button {{ border-radius: 10px; border: 1px solid {AZUL}; color: {AZUL}; font-weight: 600; }}
.stButton > button[kind="primary"] {{ background: {DOURADO}; border-color: {DOURADO}; color: {AZUL}; font-weight: 800; }}
.radar-rodape {{ color: {DOURADO_ESCURO}; font-size: 0.8rem; text-align: center; margin: 40px 0 8px; }}
</style>
"""


def aplicar():
    st.markdown(CSS, unsafe_allow_html=True)


def cabecalho(titulo, destaque):
    logo = ""
    if LOGO.exists():
        logo = f'<img src="data:image/svg+xml;base64,{base64.b64encode(LOGO.read_bytes()).decode()}" alt="G4">'
    st.markdown(f'<div class="radar-cabecalho">{logo}<h1>{titulo} <em>{destaque}</em></h1></div>', unsafe_allow_html=True)


def rodape():
    st.markdown(f'<p class="radar-rodape">{RODAPE}</p>', unsafe_allow_html=True)
