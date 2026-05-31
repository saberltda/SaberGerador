import streamlit as st
import datetime
from src.config import GenesisConfig
from src.database import GenesisData, GenesisRules
from src.engine import GenesisEngine
from src.builder import PromptBuilder
from src.scanner import BlogScanner

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E RECURSOS
# ==========================================
st.set_page_config(
    page_title="Genesis Magneto V.72",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# 2. INTERFACE E MANUAIS DIDÁTICOS
# ==========================================
st.title("⚡ Genesis Magneto V.72 - Painel de Operação")
st.markdown(f"**Versão:** {GenesisConfig.VERSION} | **Status:** Online e Sincronizado")
st.divider()

st.markdown("""
### 🧠 Como usar este gerador
Bem-vindo ao centro de comando. A inteligência artificial não adivinha; ela **amplifica** a sua estratégia. 
Para que o pauta gerada tenha qualidade cirúrgica, profunda e não pareça um robô escrevendo, você precisa alimentar os campos abaixo com **intenção**. Leia as instruções de cada módulo e preencha os campos.
""")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎭 1. Contexto / Modo de Escrita")
    st.info("Define a 'alma' e a voz do texto. Se você escolher **'Corretor de Imóveis'**, a IA atuará como um corretor consultivo focado em gerar desejo e conversão. Se escolher **'Jornalístico'**, o tom será imparcial, informativo e de utilidade pública.")
    contexto = st.selectbox(
        "Selecione o Modo de Escrita (Obrigatório):", 
        options=["Corretor de Imóveis", "Jornalístico"]
    )

with col2:
    st.markdown("#### 📍 2. Localização Exata (Bairro)")
    st.info("A geografia é a âncora da realidade. Selecione o bairro correspondente da lista oficial de Indaiatuba para injetar dados analíticos geográficos precisos e evitar alucinações.")
    nomes_bairros = ["FORCE_CITY_MODE"] + [b["nome"] for b in data.bairros]
    bairro_selecionado = st.selectbox(
        "Selecione o Bairro / Localização (Obrigatório):", 
        options=nomes_bairros,
        format_func=lambda x: "Cidade Inteira (Indaiatuba)" if x == "FORCE_CITY_MODE" else x
    )

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🏢 3. Ativo / Assunto Principal")
    st.info("O que exatamente estamos promovendo ou noticiando? Seja muito específico. Em vez de escrever apenas 'Apartamento', escreva **'Apartamento de 2 dormitórios com 1 suíte'**.")
    ativo = st.text_input("Produto ou Assunto:", placeholder="Ex: Apartamento de 2 dormitórios e 1 suíte")

with col4:
    st.markdown("#### 🎯 4. Persona / Público-Alvo")
    st.info("Para quem estamos escrevendo? A linguagem muda drasticamente se o texto for para **'Jovens casais'** versus **'Investidores seniores'**.")
    persona = st.text_input("Público-Alvo:", placeholder="Ex: Jovens casais")

st.divider()

col5, col6 = st.columns(2)

with col5:
    st.markdown("#### 🧠 5. Gatilho Emocional")
    st.info("Qual botão psicológico queremos apertar no leitor para que ele aja? Exemplos: **'Segurança'** (proteger a família/dinheiro), **'Escassez'** (últimas unidades), **'Status'**.")
    gatilho = st.text_input("Gatilho Dominante:", placeholder="Ex: Segurança")

with col6:
    st.markdown("#### 📖 6. Tópico Abordado (Argumento Central)")
    st.info("Qual é a 'espinha dorsal' da sua tese neste texto? Qual ideia central você quer provar? Exemplo: **'Liquidez e construção de patrimônio'**.")
    topico = st.text_input("Argumento Principal:", placeholder="Ex: Liquidez e construção de patrimônio")

st.divider()

st.markdown("#### 📐 7. Formato do Texto")
st.info("Como o leitor consumirá essa informação? A estrutura visual e a narrativa dependem disso. Exemplo: **'motivos para comprar um apartamento em Indaiatuba'**.")
formato = st.text_input("Estrutura do Texto:", placeholder="Ex: motivos para comprar um apartamento em Indaiatuba")

st.markdown("#### ⚠️ 8. Solicitações Específicas / Dicas Livres")
st.info("Este é o seu espaço de controle total. O que a IA **DEVE** incluir no texto de forma inegociável? Coloque nomes de marcas, empreendimentos ou caminhos específicos.")
dicas = st.text_area(
    "Exigências, citações obrigatórias e direcionamentos extras:", 
    placeholder="Ex: Cite o Manai que já está entregue e oportunidades na planta como o Aurora, ambos da construtora Masotti.", 
    height=150
)

st.divider()

# ==========================================
# 3. CENTRAL DE PROCESSAMENTO E ENGENHARIA
# ==========================================
if st.button("🚀 INICIAR GERAÇÃO DE CONTEÚDO (MAGNETO V.72)", type="primary", use_container_width=True):
    with st.spinner("Processando arquitetura gerativa da pauta..."):
        
        # Traduz a opção do usuário para o formato esperado pelas regras internas do sistema
        contexto_normalizado = "Comercial Imobiliário" if contexto == "Corretor de Imóveis" else "Jornalismo Local"

        # 1. Empacota os inputs livres coletados na interface
        user_inputs = {
            'bairro_nome': bairro_selecionado,
            'contexto': contexto_normalizado,
            'ativo': ativo or "Não especificado (Defina organicamente)",
            'persona': persona or "Público Amplo / Geral",
            'gatilho': gatilho or "Tom neutro, focado em clareza",
            'topico': topico or "Aspectos gerais e contextuais",
            'formato': formato or "Artigo denso e estruturado",
            'dicas': dicas or "Nenhuma solicitação extra pontuada."
        }
        
        # 2. Consolida o pacote final usando o cérebro (engine)
        pacote_final = engine.run(user_inputs)
        
        # 3. Verifica colisões estruturais com o Scanner do feed
        bairro_alvo = pacote_final['bairro']['nome']
        alerta_saturacao = ""
        if bairro_alvo not in ["Indaiatuba", "FORCE_CITY_MODE"]:
            if scanner.ja_publicado(bairro_alvo):
                alerta_saturacao = f"⚠️ **Aviso do Scanner:** O local '{bairro_alvo}' já possui registro de publicação indexada no feed. Avalie a necessidade de alternar a região."
        
        # 4. Formatação Temporal Baseada nas Configurações do Sistema (-03:00)
        datetime_alvo = datetime.datetime.now(GenesisConfig.TZ_BRASILIA)
        data_pub = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
        data_mod = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
        
        # 5. Injeta regras estruturais geográficas
        regras_injetadas = rules.get_for_prompt(bairro_alvo)
        
        # 6. Constrói o Prompt Mestre Final Combinado
        prompt_gerado = builder.build(pacote_final, data_pub, data_mod, regras_injetadas)
        
        st.success("Parâmetros absorvidos com sucesso. Modo Generativo Dinâmico Ativado.")
        
        if alerta_saturacao:
            st.warning(alerta_saturacao)
            
        with st.expander("📊 Ver Resumo do Dossiê Solicitado", expanded=True):
            st.write(f"**Local/Zona Alvo:** {bairro_alvo} ({pacote_final['bairro'].get('zona_normalizada', 'urbana')})")
            st.write(f"**Foco Principal:** {user_inputs['ativo']}")
            st.write(f"**Público-Alvo:** {user_inputs['persona']}")
            st.write(f"**Formato Escolhido:** {user_inputs['formato']}")
        
        # 7. Área de Saída com o Prompt Mestre Pronto para Cópia
        st.markdown("### 📋 Prompt Mestre Gerado")
        st.info("💡 **Instrução:** Clique no botão **'Copy'** no canto superior direito do bloco abaixo e cole diretamente na sua IA.")
        st.code(prompt_gerado, language="markdown")
