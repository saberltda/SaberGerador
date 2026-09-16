"""
Interface do SaberGerador - Modo Fábrica de Prompts (Astro MD)
"""
import json
from pathlib import Path
import streamlit as st

try:
    from src.config import PILARES_JSON_PATH
except ImportError:
    BASE_DIR = Path(__file__).resolve().parent
    PILARES_JSON_PATH = BASE_DIR / "assets" / "pilares_estilo_de_vida.json"

from src.engine import CombinadorEngine, ANGULOS, FORMATOS, TONS
from src.builder import build_astro_prompt

st.set_page_config(
    page_title="Saber • Gerador de Prompts Astro",
    page_icon="⚡",
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

st.title("⚡ Saber • Fábrica de Artigos Astro")
st.caption("Gere combinações completas em .txt para copiar, colar no Gemini e receber o .md pronto para o blog.")

if not pilares:
    st.warning("Nenhum pilar encontrado em assets/pilares_estilo_de_vida.json.")
    st.stop()

engine = CombinadorEngine(pilares)

aba1, aba2 = st.tabs(["🔥 Lote Completo (Centenas de Variações)", "🎯 Prompt Específico"])

with aba1:
    st.markdown("### Exportação em Massa")
    st.write("Gere um arquivo `.txt` contendo todas as permutações dos pilares de estilo de vida com múltiplos ângulos, tons e formatos.")
    
    modo_profundo = st.checkbox("Matriz Completa (Cruzar todos os ângulos x formatos x tons)", value=True)
    
    total_estimado = len(pilares) * (len(ANGULOS) * len(FORMATOS) * len(TONS) if modo_profundo else len(ANGULOS))
    st.info(f"Total a ser gerado: **{total_estimado} prompts prontos**")
    
    if st.button("Preparar Arquivo TXT para Download", type="primary"):
        with st.spinner("Compilando combinações..."):
            txt_resultado = engine.gerar_arquivo_combinado(multiplicar_todos=modo_profundo)
            st.success(f"{total_estimado} prompts gerados com sucesso!")
            st.download_button(
                label="📥 Baixar Arquivo TXT Completo",
                data=txt_resultado,
                file_name="prompts_astro_saber_completo.txt",
                mime="text/plain"
            )

with aba2:
    st.markdown("### Seleção Direta")
    opcoes = {p["nome"]: p for p in pilares}
    pilar_nome = st.selectbox("Pilar:", list(opcoes.keys()))
    pilar = opcoes[pilar_nome]
    
    angulo = st.selectbox("Ângulo:", ANGULOS)
    formato = st.selectbox("Formato:", FORMATOS)
    tom = st.selectbox("Tom de Voz:", TONS)
    
    if st.button("Gerar Este Prompt"):
        prompt_individual = build_astro_prompt(pilar, angulo, formato, tom)
        st.markdown("#### Pronto para colar no Gemini:")
        st.code(prompt_individual, language="markdown")
        st.download_button(
            label="Baixar Este Prompt (.txt)",
            data=prompt_individual,
            file_name=f"prompt_{pilar['id']}.txt",
            mime="text/plain"
        )
