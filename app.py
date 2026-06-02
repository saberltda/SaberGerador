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
    page_icon="⚡", 
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

# ==========================================
# 3. INTERFACE E MANUAIS DIDÁTICOS (MAGNETO V.72)
# ==========================================
st.title("⚡ Genesis Magneto V.72 - Painel de Operação Mestre")
st.markdown(f"**Versão:** {GenesisConfig.VERSION} | **Status:** Online e Sincronizado")
st.divider()

st.markdown("""
### 🧠 O Segredo da Máquina: Engenharia de Prompt
Bem-vindo ao centro de comando. A inteligência artificial não cria do nada; ela **amplifica a sua estratégia**. 
O texto final será tão brilhante quanto as instruções que você fornecer abaixo. Não tenha pressa. Leia as instruções, entenda a psicologia por trás de cada campo e preencha com **intenção estratégica profunda**. Você está no controle.
""")
st.divider()

# --- SELEÇÃO DE MODO (Define a Interface Dinamicamente) ---
st.markdown("#### 🎭 1. Contexto / Modo de Escrita")
st.info("""
**A Alma e a Voz do Texto.**
Esta escolha define toda a postura, o vocabulário, a ética e as opções do painel abaixo:
* **🏢 Corretor de Imóveis (Foco Comercial):** Tom consultivo, persuasivo, focado em fechar negócios e provar retorno financeiro (ROI).
* **📰 Jornalístico (Portal da Cidade):** Tom imparcial, informativo, investigativo e de utilidade pública. Zero viés de venda.
""")
contexto = st.selectbox(
    "Selecione o Modo de Escrita (Obrigatório):", 
    options=["Corretor de Imóveis", "Jornalístico"]
)
st.divider()

# ==========================================
# BIFURCAÇÃO DA INTERFACE COM BASE NO MODO
# ==========================================

if contexto == "Corretor de Imóveis":
    st.markdown("### 🏢 MODO: CORRETOR DE IMÓVEIS (FOCO COMERCIAL)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📍 2. Localização Exata (Bairro)")
        st.info("A IA tende a 'alucinar' se você for genérico. Ao selecionar um bairro, você aciona os protocolos de **Pesquisa Geográfica** (ruas reais, hospitais próximos).")
        nomes_bairros = ["FORCE_CITY_MODE"] + [b["nome"] for b in data.bairros]
        bairro_val = st.selectbox(
            "Selecione o Bairro / Localização (Obrigatório):", 
            options=nomes_bairros,
            format_func=lambda x: "Abordagem Macro - Cidade Inteira (Indaiatuba)" if x == "FORCE_CITY_MODE" else x
        )

    with col2:
        st.markdown("#### 🏢 3. Ativo / Assunto Principal")
        st.info("**A Anatomia do seu Palco.** Descreva a categoria do ativo (High-End, Family, Urban, Logistics, etc.) e os detalhes essenciais.")
        ativo_val = st.text_input("Descreva o Produto (Seja detalhista):", placeholder="Ex: Casa térrea de alto padrão com 3 suítes, pé direito duplo e piscina...")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 🎯 4. Persona / Público-Alvo")
        st.info("**O Alvo do Dardo.** Para quem escrevemos? Família Êxodo (SP), Investidor Tubarão (ROI), Sonhador do 1º Imóvel, Profissional Home Office?")
        persona_val = st.text_input("Descreva o Público-Alvo com clareza:", placeholder="Ex: Investidores focados em renda passiva e valorização imobiliária...")

    with col4:
        st.markdown("#### 🧠 5. Gatilho Emocional")
        st.info("**A Engenharia Psicológica.** Qual emoção evocar? Autoridade, Segurança, Lucro, Escassez/Urgência, Exclusividade ou Prova Social?")
        gatilho_val = st.text_input("Gatilho Dominante:", placeholder="Ex: Gatilho de Escassez e Exclusividade...")

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("#### 📖 6. Tópico Abordado (Argumento Central)")
        st.info("**A Espinha Dorsal Argumentativa.** Qual é a tese principal que o seu texto vai defender e provar ao longo dos parágrafos?")
        topico_val = st.text_input("Tese / Argumento Principal:", placeholder="Ex: O potencial de valorização do entorno do Parque Ecológico...")

    with col6:
        st.markdown("#### 📐 7. Formato do Texto")
        st.info("**Design da Informação.** Guia Definitivo, Listicle Curadoria (Top 5), Mitos vs Verdades, ou Estudo de Caso.")
        formato_val = st.text_input("Estrutura do Conteúdo:", placeholder="Ex: Guia definitivo detalhando infraestrutura, escolas e lazer...")

    st.markdown("#### ⚠️ 8. Solicitações Específicas / Diretrizes (Opcional)")
    st.info("**O seu 'Override' Manual.** O que a IA DEVE incluir no texto de forma inegociável, sob pena de falhar na missão?")
    dicas_val = st.text_area(
        "Exigências inegociáveis:", 
        placeholder="Ex: Cite o condomínio X e o lançamento Y. Mencione a rua principal... Fale do desconto à vista.", 
        height=150
    )

else:
    # ------------------------------------------
    # INTERFACE: JORNALÍSTICO (PORTAL DA CIDADE)
    # ------------------------------------------
    st.markdown("### 📰 MODO: PORTAL DA CIDADE (JORNALISMO)")
    
    # Em jornalismo, forçamos a busca geográfica para o escopo da cidade inteira
    bairro_val = "FORCE_CITY_MODE"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🗞️ 2. Caderno / Editoria")
        st.info("A qual caderno pertence esta matéria? Isso define a seriedade da apuração e a categorização da notícia.")
        editoria_val = st.selectbox(
            "Selecione a Editoria:", 
            options=[
                "Notícia Local (Hard News)", 
                "Utilidade Pública e Serviços", 
                "Turismo, Lazer e História", 
                "Política e Cidade", 
                "Economia e Negócios", 
                "Infraestrutura e Obras", 
                "Cultura e Eventos", 
                "Esportes", 
                "Polícia e Segurança", 
                "Editorial / Opinião"
            ]
        )

    with col2:
        st.markdown("#### 🚨 3. A Pauta / Fato Principal")
        st.info("**O Acontecimento.** O que exatamente precisa ser noticiado ou investigado? Seja claro, direto e focado no fato.")
        ativo_val = st.text_input("Descreva a Pauta (O Fato):", placeholder="Ex: Prefeitura aprova revitalização do Parque Ecológico...")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 👥 4. Leitor-Alvo / Público")
        st.info("**Quem vai ler isso?** O cidadão comum, empresários locais, motoristas, pais de alunos da rede municipal?")
        persona_val = st.text_input("Perfil do Leitor:", placeholder="Ex: Moradores da zona sul e motoristas que utilizam a rodovia X...")

    with col4:
        st.markdown("#### 🎙️ 5. Abordagem Jornalística (Tom)")
        st.info("**Intenção da Reportagem.** Qual o viés? (Ex: Denúncia, Investigativo, Alerta à População, Inspiracional, Prestação de Serviço).")
        gatilho_val = st.text_input("Tom / Abordagem:", placeholder="Ex: Tom de utilidade pública e alerta aos moradores...")

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("#### 🎯 6. Ângulo / Tese da Matéria")
        st.info("**O Foco da Lente.** Mesmo noticiando um fato, qual aspecto você quer evidenciar ou aprofundar?")
        topico_val = st.text_input("Ângulo Principal:", placeholder="Ex: O impacto prático do trânsito na vida diária devido às obras...")

    with col6:
        st.markdown("#### 📐 7. Estrutura da Notícia")
        st.info("**Design da Matéria.** (Ex: Pirâmide Invertida, Dossiê Longform, Entrevista, Lista de Dicas Úteis, Checagem de Fatos).")
        formato_val = st.text_input("Formato do Texto:", placeholder="Ex: Reportagem investigativa com dados, histórico e citações...")

    st.markdown("#### ⚠️ 8. Diretrizes Editoriais e Apuração (Opcional)")
    st.info("**Dados Obrigatórios.** Nomes de autoridades, secretarias, dados estatísticos ou restrições editoriais que a IA DEVE acatar rigorosamente.")
    dicas_val = st.text_area(
        "Regras e Fatos Inegociáveis:", 
        placeholder="Ex: Citar o secretário João Silva. Mencionar a verba de 2 milhões aprovada. Manter total neutralidade política...", 
        height=150
    )

st.divider()

# ==========================================
# 4. CENTRAL DE PROCESSAMENTO E ENGENHARIA
# ==========================================
if st.button("🚀 INICIAR GERAÇÃO DE CONTEÚDO (MAGNETO V.72)", type="primary", use_container_width=True):
    with st.spinner("Compilando parâmetros e acionando arquitetura gerativa..."):
        
        # 1. Normaliza o Contexto dependendo do Modo Escolhido
        if contexto == "Corretor de Imóveis":
            contexto_normalizado = "Comercial Imobiliário"
        else:
            contexto_normalizado = f"Jornalismo Local (Caderno: {editoria_val})"

        # 2. Empacota os inputs livres coletados
        user_inputs = {
            'bairro_nome': bairro_val,
            'contexto': contexto_normalizado,
            'ativo': ativo_val or ("Ativo não especificado" if contexto == "Corretor de Imóveis" else "Pauta não especificada"),
            'persona': persona_val or ("Público Geral" if contexto == "Corretor de Imóveis" else "Cidadãos e População em geral"),
            'gatilho': gatilho_val or ("Persuasivo" if contexto == "Corretor de Imóveis" else "Imparcial e Informativo"),
            'topico': topico_val or "Apresentação dos fatos",
            'formato': formato_val or ("Artigo Web" if contexto == "Corretor de Imóveis" else "Hard News"),
            'dicas': dicas_val or "Siga estritamente as regras originais do sistema."
        }
        
        # 3. Consolida o pacote final usando o cérebro (engine)
        pacote_final = engine.run(user_inputs)
        
        # 4. Verifica colisões estruturais com o Scanner do feed
        bairro_alvo = pacote_final['bairro']['nome']
        alerta_saturacao = ""
        if bairro_alvo not in ["Indaiatuba", "FORCE_CITY_MODE"]:
            if scanner.ja_publicado(bairro_alvo):
                alerta_saturacao = f"⚠️ **Aviso do Radar de SEO:** O local '{bairro_alvo}' já possui registro de publicação indexada recentemente no feed do site. Avalie a necessidade de alternar a região."
        
        # 5. Formatação Temporal Baseada nas Configurações do Sistema (-03:00)
        datetime_alvo = datetime.datetime.now(GenesisConfig.TZ_BRASILIA)
        data_pub = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
        data_mod = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
        
        # 6. Injeta regras estruturais geográficas lendo o arquivo REGRAS.txt
        regras_injetadas = rules.get_for_prompt(bairro_alvo)
        
        # 7. Constrói o Prompt Mestre Final Combinado
        prompt_gerado = builder.build(pacote_final, data_pub, data_mod, regras_injetadas)
        
        st.success("✨ Parâmetros absorvidos com sucesso. Modo Generativo Dinâmico Ativado.")
        
        if alerta_saturacao:
            st.warning(alerta_saturacao)
            
        with st.expander("📊 Ver Resumo do Dossiê Processado", expanded=True):
            st.write(f"**Modo de Interpretação:** {contexto_normalizado}")
            st.write(f"**Ancoragem Geográfica:** {bairro_alvo} ({pacote_final['bairro'].get('zona_normalizada', 'urbana')})")
            st.write(f"**Objeto Central:** {user_inputs['ativo']}")
            st.write(f"**Direcionamento/Tom:** {user_inputs['gatilho']} direcionado para {user_inputs['persona']}")
        
        # 8. Área de Saída com o Prompt Mestre Pronto para Cópia
        st.markdown("### 📋 Prompt Mestre Gerado")
        st.info("💡 **Instrução de Operação:** Passe o mouse sobre a caixa preta abaixo. No canto superior direito dela aparecerá um botão escrito **'Copy'**. Clique nele e cole o conteúdo diretamente no chat da Inteligência Artificial.")
        
        # O bloco de código abaixo possui o botão nativo de cópia do Streamlit
        st.code(prompt_gerado, language="markdown")
