import os
import sys
from src.config import OUTPUT_POSTS_DIR
from src.builder import build_astro_post
from src.engine import generate_article_content  # Mantém seu motor de geração existente

def main():
    print("=" * 60)
    print("  SABER GERADOR - Publicador AstroWind (Indaiatuba)")
    print("=" * 60)
    print(f"Diretório de saída: {OUTPUT_POSTS_DIR}\n")

    tema = input("Digite o TEMA ou TÍTULO do artigo: ").strip()
    if not tema:
        print("Operação cancelada.")
        return

    bairro = input("Bairro/Região (opcional, ex: Jardim Esplanada, Itaici): ").strip()

    print("\nGerando conteúdo com base nas regras analíticas...")
    # Chama o motor original de geração de texto
    artigo = generate_article_content(tema=tema, bairro=bairro)

    # Monta o arquivo no formato Astro
    slug, markdown_content = build_astro_post(
        title=artigo.get("title", tema),
        excerpt=artigo.get("excerpt", "Análise técnica do mercado imobiliário em Indaiatuba."),
        body_markdown=artigo.get("body", ""),
        category=artigo.get("category", "Insights Estratégicos"),
        tags=artigo.get("tags", ["Indaiatuba", "Mercado Imobiliário"])
    )

    caminho_arquivo = os.path.join(OUTPUT_POSTS_DIR, f"{slug}.md")

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print("\n" + "=" * 60)
    print(f"✅ Artigo gerado com sucesso!")
    print(f"📄 Arquivo: {caminho_arquivo}")
    print(f"🔗 URL compilada: /blog/{slug}")
    print("=" * 60)
    print("\nPara publicar na nuvem, basta rodar no terminal:")
    print("  cd C:\\blog-saber")
    print("  git add .")
    print(f'  git commit -m "Novo post: {artigo.get("title", tema)}"')
    print("  git push\n")

if __name__ == "__main__":
    main()
