"""
Saber Prompt Studio v5.0 — Interface Streamlit
Gerador de Briefings + Prompts de Alta Performance para o Blog Saber Indaiatuba
"""

import streamlit as st
from pathlib import Path
from src.engine import GenesisEngine
from src.builder import (
    PautaContext,
    PromptBuilder,
    ANGULOS,
    INTENTS,
    DEPTHS,
    TONS,
    LOCALISMOS,
    slugify
)

# Configuração da página Streamlit
st.set_page_config(
    page_title="Saber Prompt Studio v5.0 · Elite SEO",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Instancia o motor editorial
@st.cache_resource
def get_engine():
    return GenesisEngine()

engine = get_engine()

# Inicialização do estado de sessão
if "pauta" not in st.session_state:
    st.session_state.pauta = engine.sortear_ideia()

if "historico" not in st.session_state:
    st.session_state.historico = []

def callback_sortear_novo():
    """Sorteia uma pauta completamente nova e guarda no histórico."""
    nova_pauta = engine.sortear_ideia()
    st.session_state.pauta = nova_pauta
    
    # Registro de histórico anti-repetição
    registro = f"{nova_pauta.bairro} · {nova_pauta.category} · {ANGULOS.get(nova_pauta.angulo_key, {}).get('label', nova_pauta.angulo_key)}"
    st.session_state.historico.insert(0, registro)
    if len(st.session_state.historico) > 40:
        st.session_state.historico.pop()

# --- BARRA LATERAL (HEADER & CONTROLES DE VARIABILIDADE v5) ---
st.sidebar.title("🎲 Saber Studio v5.0")
st.sidebar.caption("Elite SEO Engine • Blog Saber Indaiatuba")

if st.sidebar.button("🎲 Sortear Briefing Completo", use_container_width=True, type="primary"):
    callback_sortear_novo()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Controles de Variação & SEO")

# Seletores do Framework v5.0
angulos_keys = list(ANGULOS.keys())
intent_keys = list(INTENTS.keys())
depth_keys = list(DEPTHS.keys())
tom_keys = list(TONS.keys())
localismo_keys = list(LOCALISMOS.keys())

sel_angulo = st.sidebar.selectbox(
    "Ângulo Editorial",
    options=angulos_keys,
    format_func=lambda x: ANGULOS[x]["label"],
    index=angulos_keys.index(st.session_state.pauta.angulo_key) if st.session_state.pauta.angulo_key in angulos_keys else 0
)

sel_intent = st.sidebar.selectbox(
    "Intenção de Busca Principal",
    options=intent_keys,
    format_func=lambda x: f"{x.capitalize()} ({INTENTS[x][:35]}...)",
    index=intent_keys.index(st.session_state.pauta.intent_key) if st.session_state.pauta.intent_key in intent_keys else 0
)

sel_depth = st.sidebar.selectbox(
    "Profundidade / Extensão",
    options=depth_keys,
    format_func=lambda x: f"{x.capitalize()} ({DEPTHS[x]['palavras']} palavras)",
    index=depth_keys.index(st.session_state.pauta.depth_key) if st.session_state.pauta.depth_key in depth_keys else 0
)

sel_tom = st.sidebar.selectbox(
    "Tom Editorial",
    options=tom_keys,
    format_func=lambda x: TONS[x][:42] + "...",
    index=tom_keys.index(st.session_state.pauta.tom_key) if st.session_state.pauta.tom_key in tom_keys else 0
)

sel_localismo = st.sidebar.selectbox(
    "Nível de Localismo",
    options=localismo_keys,
    format_func=lambda x: f"{x.capitalize()} (Hiperlocal)" if x == "alto" else x.capitalize(),
    index=localismo_keys.index(st.session_state.pauta.localismo_key) if st.session_state.pauta.localismo_key in localismo_keys else 0
)

st.sidebar.markdown("---")
st.sidebar.subheader("Histórico Recente")
if st.session_state.historico:
    for item in st.session_state.historico[:8]:
        st.sidebar.caption(f"• {item}")
else:
    st.sidebar.caption("Nenhum sorteio registrado nesta sessão.")

# --- ÁREA DE TRABALHO PRINCIPAL ---
st.title("Saber Prompt Studio v5.0 — Gerador de Artigos de Elite SEO")
st.info(
    "🎯 **Fluxo Elite:** O motor combina Bairro × Tema × Ângulo × Intenção de Busca × Profundidade × Tom. "
    "Edite os parâmetros abaixo e o script para IA se recalcula em tempo real."
)

col_esq, col_dir = st.columns([1.05, 0.95], gap="large")

with col_esq:
    st.subheader("Parâmetros do Briefing Editorial")

    f_title = st.text_input("Pauta / Título Sugerido", value=st.session_state.pauta.title)

    c1, c2 = st.columns(2)
    with c1:
        f_bairro = st.text_input("Bairro / Região", value=st.session_state.pauta.bairro)
    with c2:
        f_category = st.text_input("Categoria Editorial", value=st.session_state.pauta.category)

    f_vias = st.text_input("Vias, Eixos e Referências Reais", value=st.session_state.pauta.vias)
    f_dor = st.text_area("Dor Concreta / Ponto Cego do Comprador", value=st.session_state.pauta.dor, height=68)
    f_crenca = st.text_area("Crença de Mercado a Desarmar", value=st.session_state.pauta.crenca, height=68)
    f_mecanica = st.text_area("Mecânica Urbana, Solo, Clima e Tráfego", value=st.session_state.pauta.mecanica, height=80)
    f_limite = st.text_area("Contraindicação Honesta (Para quem NÃO serve)", value=st.session_state.pauta.limite, height=68)
    f_insight = st.text_area("Insight Único / Ângulo Diferencial (Obrigatório / Anti-Genérico)", value=st.session_state.pauta.insight, height=80)

    ck1, ck2 = st.columns(2)
    with ck1:
        f_kw_primary = st.text_input("Palavra-chave Primária (SEO)", value=st.session_state.pauta.kw_primary)
    with ck2:
        f_kw_secondary = st.text_input("Keywords Secundárias / LSI", value=st.session_state.pauta.kw_secondary)

    f_tags_raw = st.text_input("Tags para Frontmatter (separadas por vírgula)", value=", ".join(st.session_state.pauta.tags))
    tags_list = [t.strip() for t in f_tags_raw.split(",") if t.strip()]

# Atualiza contexto ativo com as edições feitas na tela
contexto_atual = PautaContext(
    title=f_title,
    bairro=f_bairro,
    category=f_category,
    vias=f_vias,
    dor=f_dor,
    crenca=f_crenca,
    mecanica=f_mecanica,
    limite=f_limite,
    insight=f_insight,
    kw_primary=f_kw_primary,
    kw_secondary=f_kw_secondary,
    tags=tags_list,
    angulo_key=sel_angulo,
    intent_key=sel_intent,
    depth_key=sel_depth,
    tom_key=sel_tom,
    localismo_key=sel_localismo
)

prompt_final = PromptBuilder.build_prompt(contexto_atual)
slug_arquivo = slugify(f_title)

with col_dir:
    st.subheader("Script Completo para a IA")

    chars = len(prompt_final)
    lines = len(prompt_final.splitlines())
    words = len(prompt_final.split())

    st.caption(f"📊 **Métricas:** {chars:,} caracteres | {lines:,} linhas | ~{words:,} palavras")

    st.text_area("Prompt Gerado (Pronto para Colar no ChatGPT / Claude / Gemini)", value=prompt_final, height=620)

    b1, b2 = st.columns(2)
    with b1:
        st.download_button(
            label="⬇️ Baixar Prompt (.txt)",
            data=prompt_final,
            file_name=f"prompt-{slug_arquivo}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with b2:
        yaml_frontmatter = PromptBuilder.build_yaml_only(contexto_atual)
        st.download_button(
            label="⬇️ Baixar Apenas YAML (.md)",
            data=yaml_frontmatter,
            file_name=f"{slug_arquivo}.md",
            mime="text/markdown",
            use_container_width=True
        )
