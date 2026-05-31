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

# --- LINHA 1: MODO E LOCAL ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎭 1. Contexto / Modo de Escrita")
    st.info("""
    **A Alma e a Voz do Texto.**
    Esta escolha define toda a postura, o vocabulário e a ética da Inteligência Artificial:
    
    * **🏢 Corretor de Imóveis (Foco Comercial):** A IA assumirá a voz de um corretor sênior, hiper-especialista na região. O tom será consultivo, persuasivo, focado em quebrar objeções, gerar desejo, provar valorização (ROI) e encaminhar o leitor para o fechamento do negócio.
    * **📰 Jornalístico (Portal da Cidade):** A IA atuará como uma redação de notícias. O tom será imparcial, informativo, investigativo e de utilidade pública. **Regra de Ouro:** Zero viés de venda. É feito para educar a população, rankear no Google e gerar autoridade.
    """)
    contexto = st.selectbox(
        "Selecione o Modo de Escrita (Obrigatório):", 
        options=["Corretor de Imóveis", "Jornalístico"]
    )

with col2:
    st.markdown("#### 📍 2. Localização Exata (Bairro)")
    st.info("""
    **A Âncora da Realidade Física.**
    A inteligência artificial tem a tendência de "alucinar" (inventar coisas) se você for genérico. Ao selecionar um bairro específico desta lista oficial, você aciona os protocolos de **Pesquisa Geográfica** do Magneto. 
    
    A IA será forçada a buscar as ruas reais daquele bairro, os hospitais próximos, as vias de acesso (ex: Rodovia Santos Dumont), a proximidade com o Parque Ecológico e o perfil real de quem mora ali. Selecione com precisão.
    """)
    nomes_bairros = ["FORCE_CITY_MODE"] + [b["nome"] for b in data.bairros]
    bairro_selecionado = st.selectbox(
        "Selecione o Bairro / Localização (Obrigatório):", 
        options=nomes_bairros,
        format_func=lambda x: "Abordagem Macro - Cidade Inteira (Indaiatuba)" if x == "FORCE_CITY_MODE" else x
    )

st.divider()

# --- LINHA 2: PRODUTO E PÚBLICO ---
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🏢 3. Ativo / Assunto Principal")
    st.info("""
    **A Anatomia do seu Palco.** O que exatamente estamos promovendo ou noticiando? Fuja do genérico.
    Em vez de apenas "Casa", detalhe a categoria do seu ativo. Inspire-se nestes Clusters:
    
    * 💎 **High-End (Luxo):** Mansão em condomínio fechado, cobertura duplex, arquitetura autoral, automação total.
    * 👨‍👩‍👧‍👦 **Family (Família):** Casa térrea com espaço gourmet, sobrado moderno, quintal amplo para pets.
    * 🏙️ **Urban (Urbano):** Studio moderno no centro, apartamento compacto de alto padrão (Short Stay).
    * 🚚 **Logistics / Corporate:** Galpão logístico AAA, laje corporativa, terreno industrial.
    * 🌿 **Rural Lifestyle:** Chácara de veraneio, sítio de lazer, haras.
    
    **Exemplo ideal:** *"Apartamento de 2 dormitórios (1 suíte), varanda gourmet envidraçada e 2 vagas, focado na planta inteligente."*
    """)
    ativo = st.text_input("Descreva o Produto ou Assunto (Seja detalhista):", placeholder="Ex: Casa térrea de alto padrão com 3 suítes, pé direito duplo e piscina aquecida...")

with col4:
    st.markdown("#### 🎯 4. Persona / Público-Alvo")
    st.info("""
    **O Alvo do Dardo.** Para quem estamos escrevendo? O texto muda radicalmente se você falar com um bilionário ou com um estagiário. 
    Inspire-se no nosso catálogo histórico de Personas:
    
    * ✈️ **Família Êxodo (Elite SP):** Fugindo da violência e trânsito da capital, buscam oásis, segurança armada e qualidade de vida no interior.
    * 🦈 **Investidor Tubarão (ROI):** Frio e calculista. Quer planilhas, custo de oportunidade, *yield* de locação e tese de valorização do Plano Diretor.
    * 🔑 **Sonhador do 1º Imóvel:** Jovem casal espremido pelo aluguel, tem medo da burocracia do financiamento e busca conforto e aprovação de crédito.
    * 💻 **Profissional Home Office:** Busca silêncio absoluto, acústica, escritório isolado e fácil acesso a Viracopos.
    * 🍷 **Melhor Idade Ativa:** Seniores buscando casas 100% térreas (sem escadas), hortas, sol da manhã e proximidade de hospitais (HAOC).
    """)
    persona = st.text_input("Descreva o Público-Alvo com clareza:", placeholder="Ex: Investidores focados em renda passiva e valorização imobiliária...")

st.divider()

# --- LINHA 3: PSICOLOGIA E ARGUMENTAÇÃO ---
col5, col6 = st.columns(2)

with col5:
    st.markdown("#### 🧠 5. Gatilho Emocional")
    st.info("""
    **A Engenharia Psicológica.** Qual botão subconsciente queremos apertar no cérebro do leitor para que ele tome uma ação imediata?
    
    * 👑 **Autoridade:** "Eu sou o especialista". Texto recheado de dados de mercado, termos técnicos traduzidos e postura consultiva.
    * 🛡️ **Segurança (Mito da Caverna):** Focado em proteger a família (portaria 24h) ou blindar o patrimônio contra a inflação.
    * 💰 **Ganância / Lucro:** Para investidores. Mostra a assimetria do mercado, a chance de multiplicar o capital, comprar na planta e revender (*flip*).
    * 🚨 **Escassez e Urgência:** "A janela está fechando". Ideal para últimas unidades ou virada de tabela de preço. Aciona o medo de perder.
    * ✨ **Exclusividade / Status:** "Para poucos". Vende a sensação de pertencer a um clube de elite, a assinatura do arquiteto, o ego e o requinte.
    * 👥 **Prova Social:** "O movimento inteligente que todos estão fazendo". Validação comunitária.
    """)
    gatilho = st.text_input("Gatilho Dominante (Qual emoção evocar?):", placeholder="Ex: Gatilho de Escassez e Urgência")

with col6:
    st.markdown("#### 📖 6. Tópico Abordado (Argumento Central)")
    st.info("""
    **A Espinha Dorsal Argumentativa.** Qual é a tese principal que o seu texto vai defender e provar ao longo dos parágrafos?
    
    **Inspirações Imobiliárias:**
    * 📈 Potencial de Valorização e Crescimento Econômico da Região.
    * 🌿 Qualidade de Vida, Biofilia e Proximidade com a Natureza (Parques).
    * 📱 Casa Inteligente (Smart Home) e Inovação Construtiva.
    * ⚖️ Segurança Jurídica da Transação e Documentação Descomplicada.
    
    **Inspirações de Portal/Jornalismo:**
    * 🔍 Fiscal do Povo (Transparência, Denúncia).
    * 📊 Jornalismo de Dados (O que os números econômicos da cidade dizem).
    * 🏛️ Resgate da Memória (História de fundação de um local icônico).
    """)
    topico = st.text_input("Tese / Argumento Principal:", placeholder="Ex: O potencial de valorização do entorno do Parque Ecológico...")

st.divider()

# --- LINHA 4: FORMATO E CONTROLE TOTAL ---
st.markdown("#### 📐 7. Formato do Texto (Design da Informação)")
st.info("""
Como o cérebro do leitor vai digerir e visualizar essa informação na tela? A estrutura dita o engajamento e o tempo de retenção.

**Formatos Campeões de Imobiliária:**
* 🗺️ **Guia Definitivo de Bairro:** Um raio-X (história, escolas, padarias, segurança).
* 🏆 **Listicle Curadoria (Top 5):** Ex: "Os 5 melhores condomínios para quem tem Pets".
* 🎭 **Mitos vs Verdades:** Quebra sistemática de objeções do cliente inseguro.
* 📈 **Estudo de Caso (Storytelling):** A Jornada do Herói de um cliente que prosperou com você.

**Formatos Campeões de Portal/Notícia:**
* 📰 **Hard News (Pirâmide Invertida):** Notícia de impacto, direto ao fato principal.
* 🕵️ **Dossiê Investigativo:** Longform profundo, histórico e recheado de provas.
* 🧠 **Explainer (Guia Prático):** Desenhando um conceito complexo ou lei para a população entender passo a passo.
""")
formato = st.text_input("Estrutura do Conteúdo:", placeholder="Ex: Guia definitivo detalhando infraestrutura, escolas e lazer...")

st.markdown("#### ⚠️ 8. Solicitações Específicas / Diretriz Suprema (Opcional, mas vital)")
st.info("""
**O seu "Override" Manual.** Este é o espaço de controle total. O que a IA **DEVE** incluir no texto de forma inegociável, sob pena de falhar na missão?
Jogue aqui todos os detalhes específicos da pauta que não couberam acima. 

* Exemplo: *"Cite o condomínio Manai (já entregue) e o lançamento Aurora, ambos da Masotti. Mencione que a rua principal acabou de ser recapeada pela prefeitura. Não use a palavra 'imperdível'. Fale do desconto de 10% para pagamento à vista."*
""")
dicas = st.text_area(
    "Exigências, citações de marcas, campanhas e regras inegociáveis:", 
    placeholder="Escreva livremente todos os detalhes cruciais que a IA precisa saber e citar obrigatoriamente...", 
    height=200
)

st.divider()

# ==========================================
# 4. CENTRAL DE PROCESSAMENTO E ENGENHARIA
# ==========================================
if st.button("🚀 INICIAR GERAÇÃO DE CONTEÚDO (MAGNETO V.72)", type="primary", use_container_width=True):
    with st.spinner("Compilando parâmetros e acionando arquitetura gerativa..."):
        
        # Traduz a opção do usuário para o formato esperado pelas regras internas do sistema
        contexto_normalizado = "Comercial Imobiliário" if contexto == "Corretor de Imóveis" else "Jornalismo Local"

        # 1. Empacota os inputs livres coletados na interface hiper-específica
        user_inputs = {
            'bairro_nome': bairro_selecionado,
            'contexto': contexto_normalizado,
            'ativo': ativo or "Imóvel / Tema não especificado (Adote uma abordagem ampla)",
            'persona': persona or "Público-Geral da cidade",
            'gatilho': gatilho or "Tom informativo e acolhedor (Neutro)",
            'topico': topico or "Apresentação geral das características e vantagens",
            'formato': formato or "Artigo estruturado para Web (Leads, H2, H3 e Bullets)",
            'dicas': dicas or "Siga estritamente as regras originais do sistema sem solicitações avulsas."
        }
        
        # 2. Consolida o pacote final usando o cérebro (engine)
        pacote_final = engine.run(user_inputs)
        
        # 3. Verifica colisões estruturais com o Scanner do feed
        bairro_alvo = pacote_final['bairro']['nome']
        alerta_saturacao = ""
        if bairro_alvo not in ["Indaiatuba", "FORCE_CITY_MODE"]:
            if scanner.ja_publicado(bairro_alvo):
                alerta_saturacao = f"⚠️ **Aviso do Rada de SEO:** O local '{bairro_alvo}' já possui registro de publicação indexada recentemente no feed do site. Avalie a necessidade de alternar a região geográfica para evitar canibalização de palavras-chave."
        
        # 4. Formatação Temporal Baseada nas Configurações do Sistema (-03:00)
        datetime_alvo = datetime.datetime.now(GenesisConfig.TZ_BRASILIA)
        data_pub = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
        data_mod = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
        
        # 5. Injeta regras estruturais geográficas lendo o arquivo REGRAS.txt
        regras_injetadas = rules.get_for_prompt(bairro_alvo)
        
        # 6. Constrói o Prompt Mestre Final Combinado
        prompt_gerado = builder.build(pacote_final, data_pub, data_mod, regras_injetadas)
        
        st.success("✨ Parâmetros absorvidos com sucesso. Modo Generativo Dinâmico Ativado.")
        
        if alerta_saturacao:
            st.warning(alerta_saturacao)
            
        with st.expander("📊 Ver Resumo do Dossiê Processado pela Engine", expanded=True):
            st.write(f"**Modo de Interpretação:** {contexto_normalizado}")
            st.write(f"**Ancoragem Geográfica:** {bairro_alvo} ({pacote_final['bairro'].get('zona_normalizada', 'urbana')})")
            st.write(f"**Objeto Principal:** {user_inputs['ativo']}")
            st.write(f"**Psicologia Aplicada:** Gatilho de {user_inputs['gatilho']} direcionado para {user_inputs['persona']}")
        
        # 7. Área de Saída com o Prompt Mestre Pronto para Cópia
        st.markdown("### 📋 Prompt Mestre Gerado")
        st.info("💡 **Instrução de Operação:** Passe o mouse sobre a caixa preta abaixo. No canto superior direito dela aparecerá um botão escrito **'Copy'**. Clique nele e cole o conteúdo diretamente no chat da Inteligência Artificial.")
        
        # O bloco de código abaixo possui o botão nativo de cópia do Streamlit
        st.code(prompt_gerado, language="markdown")
