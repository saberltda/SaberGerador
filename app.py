import streamlit as st
import datetime
from src.config import GenesisConfig
from src.database import GenesisData, GenesisRules
from src.engine import GenesisEngine
from src.builder import PromptBuilder
from src.scanner import BlogScanner

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Genesis Magneto V.71", 
    page_icon="⚙️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. INICIALIZAÇÃO DE RECURSOS (CACHE)
# ==========================================
@st.cache_resource
def iniciar_modulos_centrais():
    data = GenesisData()
    rules = GenesisRules()
    engine = GenesisEngine(data)
    builder = PromptBuilder()
    scanner = BlogScanner()
    # Pré-carrega o escaneamento do blog na memória
    scanner.mapear()
    return data, rules, engine, builder, scanner

data, rules, engine, builder, scanner = iniciar_modulos_centrais()

def humanizar(texto):
    return texto.replace("_", " ").title()

# ==========================================
# 3. INTERFACE PRINCIPAL
# ==========================================
st.title("⚙️ Genesis Magneto - Gerador de Pautas")
st.markdown(f"**Versão:** {GenesisConfig.VERSION} | **Status:** Online e Sincronizado")
st.divider()

# Divisão de layout principal
col_esq, col_dir = st.columns([1, 2])

with col_esq:
    st.subheader("1. Configurações da Pauta")
    
    # MODO DE OPERAÇÃO
    tipo_pauta = st.radio(
        "Modo de Operação (Domínio):", 
        ["IMOBILIARIA", "PORTAL"], 
        format_func=lambda x: "🏢 Imobiliária (Comercial)" if x == "IMOBILIARIA" else "📰 Portal da Cidade (Jornalismo)"
    )
    
    eh_portal = (tipo_pauta == "PORTAL")
    
    # SELEÇÃO DE BAIRRO
    nomes_bairros = ["ALEATÓRIO", "FORCE_CITY_MODE"] + [b["nome"] for b in data.bairros]
    bairro_selecionado = st.selectbox(
        "Localização / Bairro:", 
        options=nomes_bairros,
        format_func=lambda x: "Qualquer Bairro (Sorteio)" if x == "ALEATÓRIO" else ("Cidade Inteira (Indaiatuba)" if x == "FORCE_CITY_MODE" else x)
    )
    
    # SELEÇÃO DE CATEGORIA E ATIVO
    st.markdown("### Seleção de Ativo")
    if eh_portal:
        chaves_categoria = ["ALEATÓRIO"] + list(GenesisConfig.PORTAL_CATALOG.keys())
        categoria = st.selectbox("Editoria:", chaves_categoria, format_func=lambda x: "Sorteio Automático" if x == "ALEATÓRIO" else humanizar(x))
        
        opcoes_sub = ["ALEATÓRIO"]
        if categoria != "ALEATÓRIO":
            opcoes_sub += GenesisConfig.PORTAL_CATALOG[categoria]
        sub_ativo = st.selectbox("Notícia/Foco:", opcoes_sub)
    else:
        chaves_categoria = ["ALEATÓRIO"] + list(GenesisConfig.ASSETS_CATALOG.keys())
        categoria = st.selectbox("Cluster de Imóveis:", chaves_categoria, format_func=lambda x: "Sorteio Automático" if x == "ALEATÓRIO" else humanizar(x))
        
        opcoes_sub = ["ALEATÓRIO"]
        if categoria != "ALEATÓRIO":
            opcoes_sub += GenesisConfig.ASSETS_CATALOG[categoria]
        sub_ativo = st.selectbox("Imóvel Específico:", opcoes_sub)

    # SELEÇÃO DE PERSONA (Apenas Imobiliária)
    if not eh_portal:
        st.markdown("### Psicologia")
        chaves_personas = ["ALEATÓRIO"] + [k for k in GenesisConfig.PERSONAS.keys() if k != "CITIZEN_GENERAL"]
        persona_selecionada = st.selectbox("Persona / Público-Alvo:", chaves_personas, format_func=lambda x: "Sorteio Automático" if x == "ALEATÓRIO" else GenesisConfig.PERSONAS[x]['nome'])
        
        chaves_gatilho = ["ALEATÓRIO"] + list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.keys())
        gatilho_selecionado = st.selectbox("Gatilho Emocional:", chaves_gatilho, format_func=lambda x: "Sorteio Automático" if x == "ALEATÓRIO" else GenesisConfig.EMOTIONAL_TRIGGERS_MAP[x])
    else:
        persona_selecionada = "CITIZEN_GENERAL"
        gatilho_selecionado = "NEUTRAL_JOURNALISM"
        
    # FORMATO E TÓPICO
    st.markdown("### Estrutura de Conteúdo")
    
    dict_topicos = GenesisConfig.PORTAL_TOPICS_MAP if eh_portal else GenesisConfig.TOPICS_MAP
    chaves_topicos = ["ALEATÓRIO"] + list(dict_topicos.keys())
    topico_selecionado = st.selectbox("Tópico Abordado:", chaves_topicos, format_func=lambda x: "Sorteio Automático" if x == "ALEATÓRIO" else dict_topicos[x])
    
    dict_formatos = GenesisConfig.PORTAL_FORMATS_MAP if eh_portal else GenesisConfig.REAL_ESTATE_FORMATS_MAP
    chaves_formatos = ["ALEATÓRIO"] + list(dict_formatos.keys())
    formato_selecionado = st.selectbox("Formato do Texto:", chaves_formatos, format_func=lambda x: "Sorteio Automático" if x == "ALEATÓRIO" else dict_formatos[x])

    # CONFIGURAÇÃO DE TEMPO (CORRIGIDA COMPATIBILIDADE)
    st.markdown("### Agendamento Cronológico")
    # Substituído st.toggle por st.checkbox para evitar quebra em versões antigas do Streamlit
    usar_data_atual = st.checkbox("Usar data e hora atual do sistema", value=True)
    
    if not usar_data_atual:
        data_customizada = st.date_input("Data de Publicação:", datetime.date.today())
        hora_customizada = st.time_input("Hora de Publicação (Fuso -03:00):", datetime.time(9, 0))
        # Combina os inputs em um objeto datetime bruto
        datetime_alvo = datetime.datetime.combine(data_customizada, hora_customizada)
    else:
        datetime_alvo = datetime.datetime.now(GenesisConfig.TZ_BRASILIA)

    st.write("")
    btn_gerar = st.button("🚀 Processar Parâmetros e Gerar Pauta", use_container_width=True, type="primary")

with col_dir:
    st.subheader("2. Central de Orquestração")
    
    if btn_gerar:
        with st.spinner("Processando arquitetura da pauta..."):
            
            # 1. Empacota as escolhas exatas feitas pelos operadores humanos
            user_inputs = {
                'tipo_pauta': tipo_pauta,
                'bairro_nome': bairro_selecionado,
                'ativo': categoria,
                'sub_ativo': sub_ativo,
                'persona_key': persona_selecionada,
                'gatilho': gatilho_selecionado,
                'topico': topico_selecionado,
                'formato': formato_selecionado
            }
            
            # 2. Roda a Engine para resolver cruzamentos e alucinações geográficas
            pacote_final = engine.run(user_inputs)
            
            # 3. Verifica colisões no Scanner (Evitar repetição biográfica de bairros)
            bairro_alvo = pacote_final['bairro']['nome']
            alerta_saturacao = ""
            if bairro_alvo not in ["Indaiatuba", "ALEATÓRIO", "FORCE_CITY_MODE"]:
                if scanner.ja_publicado(bairro_alvo):
                    alerta_saturacao = f"⚠️ **Aviso do Scanner:** O local '{bairro_alvo}' já possui registro de publicação indexada no feed. Avalie a necessidade de alternar a região geográfica."
            
            # 4. Formatação de Strings Temporais conforme ISO 8601 exigido pelo validador
            data_pub = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
            data_mod = datetime.datetime.now(GenesisConfig.TZ_BRASILIA).strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
            
            # 5. Injeta regras locais (Conversão das tags {{BAIRRO}} e {{LOCAL}})
            regras_injetadas = rules.get_for_prompt(bairro_alvo)
            
            # 6. Constrói o Prompt Final estruturado em Markdown
            # CORREÇÃO CRÍTICA: A variável regras_injetadas agora é passada corretamente.
            prompt_gerado = builder.build(pacote_final, data_pub, data_mod, regras_injetadas)
            
            # 7. Exibição de Resumo de Sucesso
            st.success("Parâmetros consolidados com sucesso. Filtros de segurança aplicados.")
            
            if alerta_saturacao:
                st.warning(alerta_saturacao)
                
            with st.expander("📊 Ver Relatório Analítico da Engine", expanded=True):
                st.write(f"**Persona Final:** {pacote_final['persona']['nome']}")
                st.write(f"**Desejo Alvo:** {pacote_final['persona']['desejo']}")
                st.write(f"**Local/Zona:** {bairro_alvo} ({pacote_final['bairro'].get('zona_normalizada', 'N/A')})")
                st.write(f"**Ativo Validado:** {pacote_final['ativo_definido']}")
                st.write(f"**Data Injetada no Script:** `{data_pub}`")
            
            st.markdown("### Copie o Prompt Abaixo:")
            st.code(prompt_gerado, language="markdown")
