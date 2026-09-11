import streamlit as st
import datetime
import os
from src.config import GenesisConfig
from src.database import GenesisData, GenesisRules
from src.engine import GenesisEngine
from src.builder import PromptBuilder, slugify
from src.scanner import BlogScanner

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Genesis Magneto V.72 - AstroWind", 
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
    scanner.mapear()
    return data, rules, engine, builder, scanner

data, rules, engine, builder, scanner = iniciar_modulos_centrais()

# ==========================================
# 3. INTERFACE E MANUAIS DIDÁTICOS
# ==========================================
st.title("⚡ Genesis Magneto V.72 — Centro de Comando Editorial")
st.markdown(f"**Versão:** {GenesisConfig.VERSION} | **Deploy Engine:** AstroWind (.md) | **Status:** Online")
st.divider()

# Abas para separar a Geração do Super-Prompt e a Montagem Final do Post
tab_prompt, tab_conversor = st.tabs(["🚀 1. Engenharia do Prompt Mestre", "📦 2. Montador do Post Astro (.md)"])

with tab_prompt:
    st.markdown("""
    ### 🧠 O Segredo da Máquina: Engenharia de Prompt
    Configure os parâmetros estratégicos para gerar o prompt perfeito. Após copiar o prompt, cole no seu modelo de IA (Claude / ChatGPT / Gemini).
    """)
    st.divider()

    st.markdown("#### 🎭 1. Contexto / Modo de Escrita")
    contexto = st.selectbox(
        "Selecione o Modo de Escrita (Obrigatório):", 
        options=["Corretor de Imóveis", "Jornalístico"]
    )
    st.divider()

    if contexto == "Corretor de Imóveis":
        st.markdown("### 🏢 MODO: CORRETOR DE IMÓVEIS (FOCO COMERCIAL)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📍 2. Localização Exata (Bairro)")
            nomes_bairros = ["FORCE_CITY_MODE"] + [b["nome"] for b in data.bairros]
            bairro_val = st.selectbox(
                "Selecione o Bairro / Localização (Obrigatório):", 
                options=nomes_bairros,
                format_func=lambda x: "Abordagem Macro - Cidade Inteira (Indaiatuba)" if x == "FORCE_CITY_MODE" else x
            )

        with col2:
            st.markdown("#### 🏢 3. Ativo / Assunto Principal")
            ativo_val = st.text_input("Descreva o Produto (Seja detalhista):", placeholder="Ex: Casa térrea de alto padrão com 3 suítes, pé direito duplo e piscina...")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### 🎯 4. Persona / Público-Alvo")
            persona_val = st.text_input("Descreva o Público-Alvo com clareza:", placeholder="Ex: Investidores focados em renda passiva e valorização imobiliária...")

        with col4:
            st.markdown("#### 🧠 5. Gatilho Emocional")
            gatilho_val = st.text_input("Gatilho Dominante:", placeholder="Ex: Gatilho de Escassez e Exclusividade...")

        col5, col6 = st.columns(2)
        with col5:
            st.markdown("#### 📖 6. Tópico Abordado (Argumento Central)")
            topico_val = st.text_input("Tese / Argumento Principal:", placeholder="Ex: O potencial de valorização do entorno do Parque Ecológico...")

        with col6:
            st.markdown("#### 📐 7. Formato do Texto")
            formato_val = st.text_input("Estrutura do Conteúdo:", placeholder="Ex: Guia definitivo detalhando infraestrutura, escolas e lazer...")

        st.markdown("#### ⚠️ 8. Solicitações Específicas / Diretrizes (Opcional)")
        dicas_val = st.text_area(
            "Exigências inegociáveis:", 
            placeholder="Ex: Cite o condomínio X e o lançamento Y. Mencione a rua principal... Fale do desconto à vista.", 
            height=120
        )

    else:
        st.markdown("### 📰 MODO: PORTAL DA CIDADE (JORNALISMO)")
        bairro_val = "FORCE_CITY_MODE"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🗞️ 2. Caderno / Editoria")
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
            ativo_val = st.text_input("Descreva a Pauta (O Fato):", placeholder="Ex: Prefeitura aprova revitalização do Parque Ecológico...")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### 👥 4. Leitor-Alvo / Público")
            persona_val = st.text_input("Perfil do Leitor:", placeholder="Ex: Moradores da zona sul e motoristas que utilizam a rodovia X...")

        with col4:
            st.markdown("#### 🎙️ 5. Abordagem Jornalística (Tom)")
            gatilho_val = st.text_input("Tom / Abordagem:", placeholder="Ex: Tom de utilidade pública e alerta aos moradores...")

        col5, col6 = st.columns(2)
        with col5:
            st.markdown("#### 🎯 6. Ângulo / Tese da Matéria")
            topico_val = st.text_input("Ângulo Principal:", placeholder="Ex: O impacto prático do trânsito na vida diária devido às obras...")

        with col6:
            st.markdown("#### 📐 7. Estrutura da Notícia")
            formato_val = st.text_input("Formato do Texto:", placeholder="Ex: Reportagem investigativa com dados, histórico e citações...")

        st.markdown("#### ⚠️ 8. Diretrizes Editoriais e Apuração (Opcional)")
        dicas_val = st.text_area(
            "Regras e Fatos Inegociáveis:", 
            placeholder="Ex: Citar o secretário João Silva. Mencionar a verba de 2 milhões aprovada. Manter total neutralidade política...", 
            height=120
        )

    st.divider()

    if st.button("🚀 COMPILAR PROMPT MESTRE (MAGNETO V.72)", type="primary", use_container_width=True):
        with st.spinner("Compilando parâmetros e regras inegociáveis..."):
            if contexto == "Corretor de Imóveis":
                contexto_normalizado = "Comercial Imobiliário"
            else:
                contexto_normalizado = f"Jornalismo Local (Caderno: {editoria_val})"

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
            
            pacote_final = engine.run(user_inputs)
            bairro_alvo = pacote_final['bairro']['nome']
            
            datetime_alvo = datetime.datetime.now(GenesisConfig.TZ_BRASILIA)
            data_pub = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
            data_mod = datetime_alvo.strftime("%Y-%m-%dT%H:%M:%S") + GenesisConfig.FUSO_PADRAO
            
            regras_injetadas = rules.get_for_prompt(bairro_alvo)
            prompt_gerado = builder.build(pacote_final, data_pub, data_mod, regras_injetadas)
            
            st.success("✨ Prompt Mestre Compilado com Sucesso!")
            st.info("Passe o mouse no canto superior direito do bloco abaixo e clique em **Copy**. Cole-o na IA:")
            st.code(prompt_gerado, language="markdown")


with tab_conversor:
    st.markdown("""
    ### 📦 2. Montador e Empacotador para AstroWind
    Cole aqui os elementos gerados pela IA para gerar o arquivo `.md` 100% compatível com a estrutura de `C:\\blog-saber\\src\\data\\post\\`.
    """)

    c1, c2 = st.columns([2, 1])
    with c1:
        post_title = st.text_input("Título do Post (H1 gerado pela IA)")
        post_excerpt = st.text_area("Resumo / Excerpt (1 a 2 frases)", height=80)
        post_body = st.text_area("Conteúdo do Artigo (Markdown ou HTML retornado pela IA)", height=380)

    with c2:
        post_category = st.selectbox("Categoria", ["Insights Estratégicos", "Análises de Mercado", "Urbanismo", "Investimentos"])
        post_tags_str = st.text_input("Tags (separadas por vírgula)", value="Indaiatuba, Mercado Imobiliário, Urbanismo")
        slug_auto = slugify(post_title) if post_title else ""
        post_slug = st.text_input("Slug (Nome do arquivo .md)", value=slug_auto)

    if st.button("⚡ Empacotar Post Astro (.md)", type="primary", use_container_width=True):
        if not post_title or not post_body:
            st.error("Preencha pelo menos o Título e o Conteúdo do artigo.")
        else:
            tags_list = [t.strip() for t in post_tags_str.split(",") if t.strip()]
            final_slug, md_final = PromptBuilder.build_astro_file(
                title=post_title,
                excerpt=post_excerpt if post_excerpt else post_title,
                body=post_body,
                category=post_category,
                tags=tags_list,
                custom_slug=post_slug
            )

            file_name = f"{final_slug}.md"

            # Se rodar local no Windows, tenta gravar direto na pasta
            caminho_local_windows = r"C:\blog-saber\src\data\post"
            salvo_direto = False
            if os.path.exists(caminho_local_windows):
                try:
                    with open(os.path.join(caminho_local_windows, file_name), "w", encoding="utf-8") as f:
                        f.write(md_final)
                    salvo_direto = True
                except Exception:
                    pass

            st.success(f"✅ Artigo empacotado: **{file_name}**")
            
            if salvo_direto:
                st.info(f"📁 Gravado diretamente em: `{os.path.join(caminho_local_windows, file_name)}`")
            else:
                st.info("Baixe o arquivo abaixo e coloque em `src/data/post/`:")

            st.download_button(
                label=f"📥 Baixar {file_name}",
                data=md_final,
                file_name=file_name,
                mime="text/markdown"
            )

            with st.expander("👁️ Prévia do arquivo `.md` compilado"):
                st.code(md_final, language="markdown")
