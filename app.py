import streamlit as st
from src.core_engine import GenerationEngine
from src.prompt_compiler import PromptCompiler
from src.telemetry import TelemetryTracker
from src.utils import slugify

# Configuração da página da aplicação
st.set_page_config(
    page_title="Gerador Saber V2 | Astro Blog Edition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialização de recursos cacheados
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

# Inicialização do estado de sessão
if "current_combination" not in st.session_state:
    st.session_state.current_combination = None
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""
if "history" not in st.session_state:
    st.session_state.history = telemetry.get_recent_history(limit=20)
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0

# Estilos CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #0F172A;
        margin-bottom: 0.1rem;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin: 0.2rem;
        font-size: 0.82rem;
        font-weight: 600;
        border-radius: 6px;
        background-color: #F8FAFC;
        color: #334155;
        border: 1px solid #CBD5E1;
    }
    .badge-highlight {
        background-color: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da Aplicação
st.markdown('<div class="main-title">⚡ Gerador Saber V2</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Engenharia de Atenção Indireta & Formatação Markdown (.md) para Blog Astro (SEO Atemporal)</div>', unsafe_allow_html=True)

# Linha de Métricas Auditadas
theoretical_combinations = engine.get_theoretical_combinations()
if theoretical_combinations >= 1_000_000_000_000:
    formatted_comb = f"{theoretical_combinations / 1_000_000_000_000:.2f} Trilhões"
elif theoretical_combinations >= 1_000_000_000:
    formatted_comb = f"{theoretical_combinations / 1_000_000_000:.2f} Bilhões"
elif theoretical_combinations >= 1_000_000:
    formatted_comb = f"{theoretical_combinations / 1_000_000:.2f} Milhões"
else:
    formatted_comb = f"{theoretical_combinations:,}".replace(",", ".")

col_m1, col_m2, col_m3 = st.columns([1.2, 1, 1.8])
with col_m1:
    st.metric(
        label="Combinações Teóricas (8 Eixos)",
        value=formatted_comb,
        help=f"Total auditado: {theoretical_combinations:,}".replace(",", ".")
    )
with col_m2:
    st.metric(
        label="Prompts Gerados na Sessão",
        value=st.session_state.generation_count
    )
with col_m3:
    st.caption("🚀 Saída configurada para Astro Content Collections com Frontmatter YAML e SEO Atemporal (sem datas).")

st.divider()

# Ação Hero
col_btn, _ = st.columns([1.2, 2.8])
with col_btn:
    generate_clicked = st.button("⚡ GERAR PROMPT ASTRO (.MD)", type="primary", use_container_width=True)

# Painel Modular de Ajustes Finos
with st.expander("🛠️ Ajustes Finos Paramétricos (Opcional - sobrescreve seleção autônoma)"):
    st.caption("Deixe em '[Aleatório / Automático]' para que o motor harmonize os 8 eixos via afinidade semântica.")
    
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
            "3. Ponto de Dor / Conflito Urbano",
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
            "5. Microterritório / Bairro (assets/bairros.json)",
            options=["[Aleatório / Automático]"] + engine.get_options("bairros"),
            index=0
        )
        custom_formato = st.selectbox(
            "6. Formato de Conteúdo / Canal",
            options=["[Aleatório / Automático]"] + engine.get_options("formatos"),
            index=0
        )

    with col_p3:
        custom_tom = st.selectbox(
            "7. Tom de Voz / Arquétipo",
            options=["[Aleatório / Automático]"] + engine.get_options("tons"),
            index=0
        )
        custom_ancora = st.selectbox(
            "8. Âncora da Imobiliária Saber",
            options=["[Aleatório / Automático]"] + engine.get_options("ancoras"),
            index=0
        )

# Execução da Geração
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

# Exibição dos Parâmetros Ativos
if st.session_state.current_combination:
    comb = st.session_state.current_combination
    st.markdown("##### 🎯 Parâmetros Ativos do Post Astro")
    
    badge_html = f"""
    <div>
        <span class="badge badge-highlight">📌 Tema: {comb.get('macro_tema', {}).get('titulo', 'N/A')}</span>
        <span class="badge badge-highlight">👤 Persona: {comb.get('persona', {}).get('nome', 'N/A')}</span>
        <span class="badge">⚠️ Conflito: {comb.get('dor', {}).get('resumo', 'N/A')}</span>
        <span class="badge">📍 Território: {comb.get('diferencial_indaiatuba', {}).get('pilar', 'N/A')}</span>
        <span class="badge">🏡 Microterritório: {comb.get('bairro', {}).get('nome', 'N/A')}</span>
        <span class="badge">📰 Formato: {comb.get('formato', {}).get('nome', 'N/A')}</span>
        <span class="badge">🎙️ Tom: {comb.get('tom', {}).get('nome', 'N/A')}</span>
        <span class="badge">⚓ Âncora: {comb.get('ancora', {}).get('conceito', 'N/A')}</span>
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)
    st.write("")

# Área Principal: Mega-Prompt Mestre para Geração do Post Astro
col_prompt, col_side_actions = st.columns([4, 1.1])

with col_prompt:
    st.markdown("#### 📄 Mega-Prompt Mestre para Criação do Post Astro (.md)")
    prompt_text = st.text_area(
        label="Prompt Mestre Astro",
        value=st.session_state.current_prompt,
        height=470,
        label_visibility="collapsed"
    )

with col_side_actions:
    st.markdown("#### 🚀 Exportação")
    
    # Gera slug dinâmico para nomenclatura do arquivo .md
    current_slug = "post-editorial-saber"
    if st.session_state.current_combination:
        tema_txt = st.session_state.current_combination.get("macro_tema", {}).get("titulo", "")
        if tema_txt:
            current_slug = slugify(tema_txt)[:45]

    st.download_button(
        label="📥 Baixar Prompt (.md)",
        data=st.session_state.current_prompt,
        file_name=f"{current_slug}.md",
        mime="text/markdown",
        use_container_width=True
    )
    
    st.download_button(
        label="📄 Baixar Prompt (.txt)",
        data=st.session_state.current_prompt,
        file_name=f"{current_slug}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.info("💡 **Dica de Publicação:** Ao colar este mega-prompt em sua IA de preferência, copie a resposta integral gerada e salve diretamente como `.md` dentro de `src/content/blog/` no seu projeto Astro.")

# Histórico Recente
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
