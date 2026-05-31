import streamlit as st
from datetime import datetime
import pytz

# Configuração da Página
st.set_page_config(
    page_title="Genesis Magneto - Gerador de Conteúdo",
    page_icon="⚡",
    layout="wide"
)

# Título Principal
st.title("⚡ Genesis Magneto V.72 - Painel de Operação")
st.markdown("---")
st.markdown("""
### 🧠 Como usar este gerador
Bem-vindo ao centro de comando. A inteligência artificial não adivinha; ela **amplifica** a sua estratégia. 
Para que o texto gerado tenha qualidade cirúrgica, profunda e não pareça um robô escrevendo, você precisa alimentar os campos abaixo com **intenção**. Leia as instruções de cada módulo e preencha os campos.
""")
st.markdown("---")

# ==========================================
# 1. CONTEXTO E LOCALIZAÇÃO
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎭 1. Contexto / Modo de Escrita")
    st.info("Define a 'alma' e a voz do texto. Se você escolher **'Comercial Imobiliário'**, a IA atuará como um corretor consultivo focado em gerar desejo e conversão. Se escolher **'Jornalístico'**, o tom será imparcial, informativo e de utilidade pública (sem tentar vender).")
    contexto = st.text_input("Modo de Escrita:", key="contexto")

with col2:
    st.markdown("#### 📍 2. Localização Exata")
    st.info("A geografia é a âncora da realidade. Evite ser genérico. Digite a **Cidade e o Bairro**. Isso obriga a IA a buscar cruzamentos, parques, avenidas e infraestruturas reais daquela região para validar os argumentos do texto.")
    local = st.text_input("Cidade / Bairro:", key="local")

st.markdown("---")

# ==========================================
# 2. O PRODUTO E O PÚBLICO
# ==========================================
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🏢 3. Ativo / Assunto Principal")
    st.info("O que exatamente estamos promovendo ou noticiando? Seja muito específico. Em vez de escrever apenas 'Apartamento', escreva **'Apartamento de 2 dormitórios com 1 suíte e varanda gourmet'**. Quanto mais detalhes físicos, mais rica será a descrição técnica.")
    ativo = st.text_input("Produto ou Assunto:", key="ativo")

with col4:
    st.markdown("#### 🎯 4. Persona / Público-Alvo")
    st.info("Para quem estamos escrevendo? A linguagem muda drasticamente se o texto for para **'Jovens casais buscando o 1º imóvel'** (foco em começo de vida e facilidade) versus **'Investidores seniores'** (foco em planilhas, rentabilidade e liquidez).")
    persona = st.text_input("Público-Alvo:", key="persona")

st.markdown("---")

# ==========================================
# 3. PSICOLOGIA E ARGUMENTAÇÃO
# ==========================================
col5, col6 = st.columns(2)

with col5:
    st.markdown("#### 🧠 5. Gatilho Emocional")
    st.info("Qual botão psicológico queremos apertar no leitor para que ele aja? Exemplos: **'Segurança'** (proteger a família/dinheiro), **'Escassez'** (últimas unidades), **'Status/Exclusividade'** (pertencer a um grupo seleto) ou **'Liberdade'**.")
    gatilho = st.text_input("Gatilho Dominante:", key="gatilho")

with col6:
    st.markdown("#### 📖 6. Tópico Abordado (Argumento Central)")
    st.info("Qual é a 'espinha dorsal' da sua tese neste texto? Qual ideia central você quer provar? Exemplo: **'A alta liquidez e a construção de patrimônio a longo prazo'** ou **'Como a proximidade com o parque ecológico aumenta a qualidade de vida'**.")
    topico = st.text_input("Argumento Principal:", key="topico")

st.markdown("---")

# ==========================================
# 4. FORMATO E DIRETRIZES FINAIS
# ==========================================
st.markdown("#### 📐 7. Formato do Texto")
st.info("Como o leitor consumirá essa informação? A estrutura visual e a narrativa dependem disso. \n\n*Exemplos práticos:* \n- 'Lista com 5 motivos para comprar no bairro X' \n- 'Guia definitivo de investimento' \n- 'Artigo de opinião longo e analítico'")
formato = st.text_input("Estrutura do Texto:", key="formato")

st.markdown("#### ⚠️ 8. Solicitações Específicas / Dicas Livres (Obrigatório seguir)")
st.info("Este é o seu espaço de controle total. O que a IA **DEVE** incluir no texto de forma inegociável? Quer citar nomes de empreendimentos específicos (ex: 'Cite o Manai e o Aurora da Masotti')? Tem alguma regra de financiamento que precisa ser dita? Jogue todos os detalhes e exigências aqui.")
dicas = st.text_area("Exigências, citações obrigatórias e direcionamentos extras:", height=150, key="dicas")

# ==========================================
# GERAÇÃO E ENVIO (BOTÃO)
# ==========================================
st.markdown("---")

if st.button("🚀 INICIAR GERAÇÃO DE CONTEÚDO (MAGNETO V.72)", type="primary", use_container_width=True):
    if not contexto or not local or not ativo:
        st.error("⚠️ Atenção: Preencha pelo menos o Contexto, Localização e Ativo para gerar o texto.")
    else:
        # Pega a data e hora atual no fuso horário de Brasília
        fuso_br = pytz.timezone('America/Sao_Paulo')
        timestamp_atual = datetime.now(fuso_br).isoformat()
        
        st.success("Sinal enviado. Processando inteligência de dados...")
        
        with st.spinner("Pesquisando dados reais e escrevendo o artigo..."):
            
            # ---------------------------------------------------------
            # AQUI ENTRA A INTEGRAÇÃO COM O SEU BACKEND (engine.py, etc)
            # Exemplo de montagem do dicionário (payload) para envio:
            # ---------------------------------------------------------
            parametros = {
                "contexto": contexto,
                "local": local,
                "ativo": ativo,
                "persona": persona,
                "gatilho": gatilho,
                "topico": topico,
                "formato": formato,
                "dicas_especificas": dicas,
                "timestamp": timestamp_atual
            }
            
            # SUGESTÃO DE CHAMADA:
            # from src.engine import gerar_artigo
            # resultado = gerar_artigo(parametros)
            # st.markdown(resultado)
            
            st.info("Integre a chamada da função do seu módulo `src/engine.py` aqui para exibir a resposta gerada.")
