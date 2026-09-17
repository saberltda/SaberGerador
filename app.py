import streamlit as st
import json
from pathlib import Path
from src.core_engine import GenerationEngine
from src.prompt_compiler import PromptCompiler
from src.telemetry import TelemetryTracker

# Configuração da página - Interface limpa e moderna
st.set_page_config(
    page_title="Gerador Saber V2 | Engenharia de Atenção Indireta",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialização de dependências e estado
@st.cache_resource
def get_engine():
    return GenerationEngine()

@st.cache_resource
def get_compiler():
    return PromptCompiler()

@st.cache_resource
def get_telemetry():
    return TelemetryTracker()

engine = get_engine()
compiler = get_compiler()
telemetry = get_telemetry()

# Inicialização de variáveis de sessão
if "current_combination" not in st.session_state:
    st.session_state.current_combination = None
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""
if "history" not in st.session_state:
    st.session_state.history = telemetry.get_recent_history(limit=20)
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0

# Estilização CSS customizada
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin: 0.2rem;
        font-size: 0.82rem;
        font-weight: 600;
        border-radius: 6px;
        background-color: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
    }
    .badge-highlight {
        background-color: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
    }
    .metric-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da Aplicação
st.markdown('<div class="main-title">⚡ Gerador Saber V2</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Mecanismo de Atenção Indireta & Engenharia de Prompts Editoriais ("Vender sem Vender")</div>', unsafe_allow_html=True)

# Linha de métricas e status rápido
col_metric1, col_metric2, col_metric3 = st.columns([1, 1, 2])
with col_metric1:
    st.metric(label="Combinações Teóricas", value=f"{engine.get_theoretical_combinations():,}".replace(",", "."))
with col_metric2:
    st.metric(label="Prompts Gerados na Sessão", value=st.session_state.generation_count)
with col_metric3:
    st.write("")

st.divider()

# Painel de Ação Principal (Hero com One-Click Generation)
col_btn, col_empty = st.columns([1, 3])
with col_btn:
    generate_clicked = st.button("⚡ GERAR PROMPT MESTRE", type="primary", use_container_width=True)

# Painel Expansível de Ajustes Finos (Edição Paramétrica Modular Opcional)
with st.expander("🛠️ Ajustes Finos Paramétricos (Opcional - sobrescreve sorteio autônomo)"):
    st.caption("Deixe em branco ou em '[Aleatório / Automático]' para permitir que o motor de afinidade escolha a melhor combinação.")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        custom_tema = st.selectbox(
            "1. Macrotendência / Tema Central",
            options=["[Aleatório / Automático]"] + engine.get_options("macro_temas"),
            index=0
        )
        custom_persona = st.selectbox(
            "2. Persona Psicográfica",
            options=["[Aleatório / Automático]"] + engine.get_options("personas"),
            index=0
        )
        custom_dor = st.selectbox(
            "3. Ponto de Dor / Gatilho Emocional",
            options=["[Aleatório / Automático]"] + engine.get_options("dores"),
            index=0
        )

    with col_p2:
        custom_cidade = st.selectbox(
            "4. Revelação Geográfica (Indaiatuba)",
            options=["[Aleatório / Automático]"] + engine.get_options("diferenciais_indaiatuba"),
            index=0
        )
        custom_bairro = st.selectbox(
            "5. Bairro / Microterritório (assets/bairros.json)",
            options=["[Aleatório / Automático]"] + engine.get_options("bairros"),
            index=0
        )
        custom_formato = st.selectbox(
            "6. Formato de Publicação / Veículo",
            options=["[Aleatório / Automático]"] + engine.get_options("formatos"),
            index=0
        )

    with col_p3:
        custom_tom = st.selectbox(
            "7. Tom de Voz / Arquétipo Narrativo",
            options=["[Aleatório / Automático]"] + engine.get_options("tons"),
            index=0
        )
        custom_ancora = st.selectbox(
            "8. Âncora da Imobiliária Saber",
            options=["[Aleatório / Automático]"] + engine.get_options("ancoras"),
            index=0
        )

# Execução da Geração ao Clicar
if generate_clicked or st.session_state.current_prompt == "":
    manual_overrides = {
        "macro_tema": None if custom_tema.startswith("[") else custom_tema,
        "persona": None if custom_persona.startswith("[") else custom_persona,
        "dor": None if custom_dor.startswith("[") else custom_dor,
        "diferencial_indaiatuba": None if custom_cidade.startswith("[") else custom_cidade,
        "bairro": None if custom_bairro.startswith("[") else custom_bairro,
        "formato": None if custom_formato.startswith("[") else custom_formato,
        "tom": None if custom_tom.startswith("[") else custom_tom,
        "ancora": None if custom_ancora.startswith("[") else custom_ancora,
    }

    combination = engine.generate_harmonized_combination(overrides=manual_overrides)
    prompt = compiler.compile(combination)
    
    st.session_state.current_combination = combination
    st.session_state.current_prompt = prompt
    if generate_clicked:
        st.session_state.generation_count += 1
        telemetry.record_generation(combination, prompt)
        st.session_state.history = telemetry.get_recent_history(limit=20)

# Exibição dos Parâmetros Sorteados (Badges)
if st.session_state.current_combination:
    comb = st.session_state.current_combination
    st.markdown("##### 🎯 Parâmetros Ativos da Combinação")
    
    badge_html = f"""
    <div>
        <span class="badge badge-highlight">📌 Tema: {comb.get('macro_tema', {}).get('titulo', 'N/A')}</span>
        <span class="badge badge-highlight">👤 Persona: {comb.get('persona', {}).get('nome', 'N/A')}</span>
        <span class="badge">⚠️ Dor: {comb.get('dor', {}).get('resumo', 'N/A')}</span>
        <span class="badge">📍 Solução: {comb.get('diferencial_indaiatuba', {}).get('pilar', 'N/A')}</span>
        <span class="badge">🏡 Bairro: {comb.get('bairro', {}).get('nome', 'N/A')}</span>
        <span class="badge">📰 Formato: {comb.get('formato', {}).get('nome', 'N/A')}</span>
        <span class="badge">🎙️ Tom: {comb.get('tom', {}).get('nome', 'N/A')}</span>
        <span class="badge">⚓ Âncora: {comb.get('ancora', {}).get('conceito', 'N/A')}</span>
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)
    st.write("")

# Área Principal de Exibição do Mega-Prompt
col_text, col_actions = st.columns([4, 1])

with col_text:
    st.markdown("#### 📄 Mega-Prompt Mestre Pronto para Cópia")
    prompt_text = st.text_area(
        label="Prompt Mestre",
        value=st.session_state.current_prompt,
        height=430,
        label_visibility="collapsed"
    )

with col_actions:
    st.markdown("#### 🚀 Ações")
    
    # Download como Markdown
    st.download_button(
        label="📥 Baixar como .md",
        data=st.session_state.current_prompt,
        file_name="prompt_mestre_saber_v2.md",
        mime="text/markdown",
        use_container_width=True
    )
    
    # Download como TXT
    st.download_button(
        label="📄 Baixar como .txt",
        data=st.session_state.current_prompt,
        file_name="prompt_mestre_saber_v2.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.info("💡 **Dica rápida:** Clique no ícone de cópia no canto superior direito da caixa de texto do Streamlit para copiar com 1 clique.")

# Histórico Recente (Últimos 20 prompts)
st.divider()
with st.expander("📜 Histórico de Prompts Recentes (Últimos 20)"):
    if st.session_state.history:
        for idx, item in enumerate(st.session_state.history):
            with st.container():
                st.markdown(f"**#{idx+1} | {item.get('timestamp', '')}** — *{item.get('formato', '')} | {item.get('persona', '')} | {item.get('bairro', '')}*")
                with st.expander("Visualizar prompt gravado"):
                    st.code(item.get("prompt", ""), language="markdown")
    else:
        st.write("Nenhum prompt gerado no histórico recente ainda.")
