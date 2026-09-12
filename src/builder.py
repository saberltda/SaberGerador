# src/builder.py
import re
import unicodedata
from datetime import datetime, timezone

def slugify(value: str) -> str:
    """Normaliza strings removendo acentos e gerando slug seguro para URL e arquivo."""
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-')

class PromptBuilder:
    """
    O 'Redator' (Genesis Magneto V.72).
    Monta o prompt mestre preservando a engenharia de prompts original.
    """

    # Formulário Único e Limpo do Kit.com
    CTA_CAPTURE_CODE = """
<div style="text-align:center; margin: 40px 0;">  
  <script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script>
</div>
"""

    def __init__(self):
        pass

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        bairro = d['bairro']['nome']
        
        return f"""
## GENESIS MAGNETO V.72 — MODO GENERATIVO LIVRE
**Objetivo:** Produzir um conteúdo magistral, com profundidade cirúrgica, baseado estritamente nas diretrizes livres do operador humano.
**Data de Publicação Alvo:** {data_pub}
**Timestamp (Atual):** {data_mod} (Horário de Brasília)

## 1. INSTRUÇÕES DO OPERADOR (PARÂMETROS LIVRES)
O usuário definiu parâmetros exatos abaixo. Você DEVE guiar todo o seu estilo, linguagem, estrutura e linha argumentativa por eles:
- **CONTEXTO / MODO:** {d['contexto']}
- **LOCAL / BAIRRO:** {bairro}
- **ATIVO / ASSUNTO PRINCIPAL:** {d['ativo']}
- **PERSONA / PÚBLICO-ALVO:** {d['persona']}
- **GATILHO EMOCIONAL / ABORDAGEM:** {d['gatilho']}
- **TÓPICO ABORDADO:** {d['topico']}
- **FORMATO DO TEXTO:** {d['formato']}

## 2. SOLICITAÇÕES ESPECÍFICAS / DICAS (IMPORTANTE)
Atenção absoluta a este direcionamento extra exigido pelo usuário:
> "{d['dicas']}"

## 3. MISSÃO E PESQUISA DE CAMPO
A internet exige qualidade. É inegociável que você mergulhe em sua base de dados e traga contexto real da região:
- **Zero Obviedade:** Detalhe fatos reais, ruas, localização geográfica verdadeira e história.
- **Autoridade:** Aja com maestria absoluta dentro do Contexto estipulado acima, fundindo suas palavras à Persona e ao Gatilho Emocional de maneira invisível e fluida.

## 4. INSUMOS (LEIS INEGOCIÁVEIS DO SISTEMA)
<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 5. CHECKLIST FINAL (ORDEM DA SUA RESPOSTA)
1. TÍTULO SUGERIDO (H1 otimizado para SEO).
2. RESUMO / EXCERPT (1 ou 2 frases densas e instigantes para o card do artigo).
3. CONTEÚDO DO ARTIGO (Em HTML limpo ou Markdown, com subtítulos ##, tabelas e parágrafos estruturados). 
   *(Nota: NÃO inclua blocos de JSON-LD, tags <script> de formulário ou imagens externas do Blogger no seu texto; entregue apenas o conteúdo limpo).*
4. MARCADORES/TAGS (Crie de 5 a 10 tags baseadas no bairro e no assunto principal, separadas por vírgula).
""".strip()

    @staticmethod
    def build_astro_file(title: str, excerpt: str, body: str, category: str, tags: list, custom_slug: str = None) -> tuple[str, str]:
        """
        Empacota o retorno da IA gerando o arquivo Markdown (.md) limpo para o AstroWind.
        Remove automaticamente tags indesejadas (JSON-LD manual, scripts duplicados e imagens externas).
        """
        slug = custom_slug if custom_slug else slugify(title)
        iso_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        canonical_url = f"https://saber.imb.br/blog/{slug}"
        
        tags_yaml = "\n".join([f'  - "{t.strip()}"' for t in tags if t.strip()])
        clean_title = title.replace('"', '\\"')
        clean_excerpt = excerpt.replace('"', '\\"')

        frontmatter = f"""---
publishDate: {iso_date}
title: "{clean_title}"
excerpt: "{clean_excerpt}"
image: "~/assets/images/default.png"
category: "{category}"
tags:
{tags_yaml}
metadata:
  canonical: "{canonical_url}"
---
"""
        # 1. Remove blocos de JSON-LD manuais que a IA traga (o Astro já gera o SEO nativamente)
        clean_body = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', body, flags=re.IGNORECASE)
        
        # 2. Remove tags HTML de imagem avulsas ou corrompidas que venham de caches antigos
        clean_body = re.sub(r'<img\b[^>]*>', '', clean_body, flags=re.IGNORECASE)

        # 3. Normaliza links internos para o padrão /blog/ do Worker
        clean_body = re.sub(r'https?://(?:www\.)?saber\.imb\.br/blog/([^"\'\s>]+)', r'/blog/\1', clean_body)
        clean_body = re.sub(r'https?://blog\.saber\.imb\.br/([^"\'\s>]+)', r'/blog/\1', clean_body)

        # Limpa espaços excessivos
        clean_body = clean_body.strip()

        # Monta o arquivo final garantindo o formulário do Kit.com inserido APENAS UMA VEZ no final
        final_content = f"{frontmatter}\n{clean_body}\n\n{PromptBuilder.CTA_CAPTURE_CODE.strip()}\n"
        return slug, final_content
