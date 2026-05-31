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
    page_title="Genesis Magneto V.72", 
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
    scanner.mapear()
    return data, rules, engine, builder, scanner

data, rules, engine, builder, scanner = iniciar_modulos_centrais()

# ==========================================
# 3. INTERFACE PRINCIPAL
# ==========================================
st.title("⚙️ Genesis Magneto - Gerador de Pautas (Modo Livre)")
st.markdown(f"**Versão:** {GenesisConfig.VERSION} | **Status:** Online e Sincronizado")
st.divider()

col_esq, col_dir = st.columns([1, 2])

with col_esq:
    st.subheader("1. Configurações da Pauta")
    
    # SELEÇÃO DE BAIRRO (MANTIDA)
    nomes_bairros = ["FORCE_CITY_MODE"] + [b["nome"] for b in data.bairros]
    bairro_selecionado = st.selectbox(
        "Localização / Bairro (Obrigatório):", 
        options=nomes_bairros,
        format_func=lambda x: "Cidade Inteira (Indaiatuba)" if x == "FORCE_CITY_MODE" else x
    )
    
    st.markdown("### Parâmetros de Criação")
    st.info("Descreva livremente o que deseja para cada tópico. A IA moldará o texto baseada nestas instruções.")
    
    contexto = st.text_input("1. Contexto / Modo de Operação:", placeholder="Ex: Escreva se o foco é Comercial Imobiliário, Jornalismo Local, Informativo da Prefeitura...")
    
    ativo = st.text_input("2. Ativo / Assunto Principal:", placeholder="Ex: Escreva o foco central, como 'Venda de casa de alto padrão', 'Terreno industrial' ou 'Notícia sobre segurança'...")
    
    persona = st.text_input("3. Persona / Público-Alvo:", placeholder="Ex: Escreva o perfil do leitor, como 'Investidor alta renda', 'Famílias com pets', 'Estudantes'...")
    
    gatilho = st.text_input("4. Gatilho Emocional / Abordagem:", placeholder="Ex: Escreva a emoção a gerar, como 'Urgência e escassez', 'Segurança familiar', 'Luxo e exclusividade'...")
    
    topico = st.text_input("5. Tópico / Eixo Principal:", placeholder="Ex: Escreva o tema central, como 'Potencial de valorização (ROI)', 'Qualidade de vida', 'Custo-benefício'...")
    
    formato = st.text_input("6. Formato do Texto:", placeholder="Ex: Escreva a estrutura desejada, como 'Guia definitivo de 10 passos', 'Hard news investigativo', 'Lista curada Top 5'...")
    
    dicas = st.text_area("7. Solicitações Específicas / Dicas Extras:", placeholder="Ex: Dê ênfase que o bairro é vizinho ao Parque Ecológico, cite que tem fácil acesso à Rodovia e evite usar termos jurídicos complexos...")

    st.markdown("### Agendamento Cronológico")
    usar_data_atual = st.checkbox("Usar data e hora atual do sistema", value=True)
    
    if not usar_data_atual:
        data_customizada = st.date_input("Data de Publicação:", datetime.date.today())
        hora_customizada = st.time_input("Hora de Publicação (Fuso -03:00):", datetime.time(9, 0))
        datetime_alvo = datetime.datetime.combine(data_customizada, hora_customizada)
    else:
        datetime_alvo = datetime.datetime.now(GenesisConfig.TZ_BRASILIA)

    st.write("")
    btn_gerar = st.button("🚀 Processar Parâmetros e Gerar Pauta", use_container_width=True, type="primary")

with col_dir:
    st.subheader("2. Central de Orquestração")
    
    if btn_gerar:
        with st.spinner("Processando arquitetura gerativa da pauta..."):
            
            # 1. Empacota os inputs livres
            user_inputs = {
                'bairro_nome': bairro_selecionado,
                'contexto': contexto or "Conteúdo Geral Informativo",
                'ativo': ativo or "Não especificado (Defina organicamente)",
                'persona': persona or "Público Amplo / Geral",
                'gatilho': gatilho or "Tom neutro, focado em clareza",
                'topico': topico or "Aspectos gerais e contextuais",
                'formato': formato or "Artigo denso e estruturado",
                'dicas': dicas or "Nenhuma solicitação extra pontuada."
            }
            
            # 2. Consolida o pacote final
            pacote_final = engine.run(user_inputs)
            
            # 3. Verifica colisões no Scanner
            bairro_alvo = pacote_final['bairro']['nome']
            alerta_saturacao = ""
            if bairro_alvo not in ["Indaiatuba", "FORCE_CITY_MODE"]:
                if scanner.ja_publicado(bairro_alvo):
                    alerta_saturacao = f"⚠️ **Aviso do Scanner:** O local '{bairro_alvo}' já possui registro de publicação indexada no feed. Avalie a necessidade de alternar a região."
            
            # 4. Formatação Temporal
            data_pub = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
            data_mod = datetime.datetime.now(GenesisConfig.TZ_BRASILIA).strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
            
            # 5. Injeta regras geográficas
            regras_injetadas = rules.get_for_prompt(bairro_alvo)
            
            # 6. Constrói o Prompt Final livre
            prompt_gerado = builder.build(pacote_final, data_pub, data_mod, regras_injetadas)
            
            st.success("Parâmetros absorvidos com sucesso. Modo Generativo Dinâmico Ativado.")
            
            if alerta_saturacao:
                st.warning(alerta_saturacao)
                
            with st.expander("📊 Ver Resumo do Dossiê Solicitado", expanded=True):
                st.write(f"**Local/Zona Alvo:** {bairro_alvo} ({pacote_final['bairro'].get('zona_normalizada', 'urbana')})")
                st.write(f"**Foco Principal:** {user_inputs['ativo']}")
                st.write(f"**Público-Alvo:** {user_inputs['persona']}")
                st.write(f"**Formato Escolhido:** {user_inputs['formato']}")
            
            # 7. ÁREA DE SAÍDA COM CÓPIA
            st.markdown("### 📋 Prompt Gerado")
            st.info("💡 **Instrução:** Clique no botão **'Copy'** que aparece no canto superior direito do bloco abaixo ao passar o mouse e jogue na IA.")
            
            st.code(prompt_gerado, language="markdown")
