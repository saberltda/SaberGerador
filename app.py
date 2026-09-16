"""
Interface do SaberGerador - Edição Estilo de Vida & Narrativas
"""
import json
import os
from pathlib import Path
import streamlit as st

# Garante a resolução do path mesmo se o config tiver delay de cache
try:
    from src.config import PILARES_JSON_PATH
except ImportError:
    BASE_DIR = Path(__file__).resolve().parent
    PILARES_JSON_PATH = BASE_DIR / "assets" / "pilares_estilo_de_vida.json"

from src.engine import LifestyleEngine

st.set_page_config(
    page_title="Saber • Vender Sem Vender",
    page_icon="🌿",
    layout="centered"
)

@st.cache_data
def carregar_pilares():
    caminho = Path(PILARES_JSON_PATH)
    if not caminho.exists():
        st.error(f"Arquivo não encontrado: {caminho}")
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados.get("pilares_estilo_de_vida", [])

pilares = carregar_pilares()
engine = LifestyleEngine()

st.title("Saber • Vender Sem Vender")
st.caption("Gere manifestos e crônicas sobre liberdade, rotina e tempo de qualidade.")

if not pilares:
    st.warning("Nenhum pilar encontrado em assets/pilares_estilo_de_vida.json.")
    st.stop()

opcoes_pilares = {p["nome"]: p for p in pilares}
escolha_nome = st.selectbox("Escolha o Território Temático:", list(opcoes_pilares.keys()))
pilar_selecionado = opcoes_pilares[escolha_nome]

col1, col2 = st.columns(2)
with col1:
    formato = st.selectbox(
        "Formato do Conteúdo:",
        options=["manifesto", "cronica", "post_reflexivo"],
        format_func=lambda x: {
            "manifesto": "Manifesto Visceral",
            "cronica": "Crônica de Rotina",
            "post_reflexivo": "Post Reflexivo Curto"
        }[x]
    )

st.markdown("---")
st.markdown(f"**Conflito abordado:** {pilar_selecionado['dor']}")
st.markdown(f"**Aspiração central:** {pilar_selecionado['aspiracao']}")

if st.button("Gerar Peça de Conteúdo", type="primary"):
    with st.spinner("Construindo a narrativa..."):
        conteudo = engine.gerar_narrativa(pilar_selecionado, formato=formato)
        st.markdown("### Resultado:")
        st.write(conteudo)
        st.download_button(
            label="Baixar Texto",
            data=conteudo,
            file_name=f"narrativa_{pilar_selecionado['id']}.txt",
            mime="text/plain"
        )
