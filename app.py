import os
import streamlit as st
from src.builder import build_astro_markdown, slugify

# Configuração visual do Streamlit
st.set_page_config(
    page_title="SaberGerador - AstroWind Edition",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 SaberGerador — Artigos para AstroWind")
st.markdown("Gere artigos prontos no padrão Markdown com Frontmatter YAML e formulário Kit.com integrados.")

# Formulário no Streamlit
col1, col2 = st.columns([2, 1])

with col1:
    titulo = st.text_input("Título do Artigo", placeholder="Ex: A Física da Luz em Grandes Vãos: Estética vs. Eficiência Térmica")
    resumo = st.text_area("Resumo / Excerpt (1 a 2 frases)", placeholder="Ex: Como gerenciar a luz natural em casas amplas de Indaiatuba sem criar um efeito estufa.")
    corpo = st.text_area("Corpo do Artigo (em Markdown)", height=350, placeholder="Escreva o texto aqui usando cabeçalhos ##, listas, tabelas e parágrafos normais...")

with col2:
    st.subheader("Metadados Astro")
    categoria = st.selectbox("Categoria", ["Insights Estratégicos", "Análises de Mercado", "Urbanismo", "Investimentos"])
    tags_input = st.text_input("Tags (separadas por vírgula)", value="Indaiatuba, Mercado Imobiliário, Urbanismo")
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    
    slug_sugerido = slugify(titulo) if titulo else ""
    slug = st.text_input("Slug do Artigo (Nome do arquivo .md)", value=slug_sugerido)

st.divider()

if st.button("Gerar Artigo para Astro", type="primary"):
    if not titulo or not corpo:
        st.error("Por favor, preencha pelo menos o Título e o Corpo do artigo.")
    else:
        final_slug, markdown_pronto = build_astro_markdown(
            title=titulo,
            excerpt=resumo if resumo else titulo,
            body=corpo,
            category=categoria,
            tags=tags,
            custom_slug=slug
        )

        nome_arquivo = f"{final_slug}.md"

        # Tenta salvar automaticamente caso esteja rodando no seu computador
        caminho_local_windows = r"C:\blog-saber\src\data\post"
        salvo_localmente = False
        
        if os.path.exists(caminho_local_windows):
            caminho_destino = os.path.join(caminho_local_windows, nome_arquivo)
            try:
                with open(caminho_destino, "w", encoding="utf-8") as f:
                    f.write(markdown_pronto)
                salvo_localmente = True
            except Exception as e:
                pass

        st.success(f"✅ Artigo gerado com sucesso!")
        
        if salvo_localmente:
            st.info(f"📁 Arquivo salvo automaticamente em: `{caminho_destino}`")
        else:
            st.info("Clique no botão abaixo para baixar o arquivo `.md` e colocar na pasta `src/data/post/`:")

        # Botão para download direto do arquivo .md pelo navegador
        st.download_button(
            label=f"📥 Baixar {nome_arquivo}",
            data=markdown_pronto,
            file_name=nome_arquivo,
            mime="text/markdown",
            type="secondary"
        )

        # Pré-visualização do código Markdown gerado
        with st.expander("Visualizar Conteúdo do Arquivo Markdown (.md)", expanded=True):
            st.code(markdown_pronto, language="markdown")
