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

    CTA_CAPTURE_CODE = """
<div>
<form action="https://app.kit.com/forms/8984117/subscriptions" class="seva-form formkit-form" method="post" data-sv-form="8984117" data-uid="d188d73e78" data-format="inline" data-version="5" style="background-color:#f9fafb;border-radius:4px;padding:20px;border:1px solid #e3e3e3;margin-top:2rem;">
  <div data-style="minimal">
    <div class="formkit-header" style="color:#3b5998;font-size:24px;font-weight:700;margin-bottom:12px;text-align:center;">
      <h2>Receba uma seleção dos melhores imóveis de Indaiatuba</h2>
    </div>
    <div class="formkit-subheader" style="color:#686868;font-size:16px;margin-bottom:18px;text-align:center;">
      <p>Para sua segurança e evitar spam, enviaremos um link de confirmação: ative seu cadastro clicando nele.</p>
    </div>
    <div class="seva-fields formkit-fields" style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;">
      <input class="formkit-input" name="email_address" placeholder="Digite aqui o seu e-mail..." required="" type="email" style="flex:1;min-width:240px;padding:12px;border:1px solid #e3e3e3;border-radius:4px;font-size:15px;">
      <button data-element="submit" class="formkit-submit" style="color:#fff;background-color:#098b18;border:none;border-radius:4px;padding:12px 24px;font-size:15px;font-weight:600;cursor:pointer;">
        <span>QUERO RECEBER OPORTUNIDADES</span>
      </button>
    </div>
    <div class="formkit-guarantee" style="color:#4d4d4d;font-size:12px;margin-top:12px;text-align:center;">
      <p>Nós respeitamos sua privacidade. Cancele o cadastro a qualquer momento.</p>
    </div>
  </div>
</form>
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
1. DOSSIÊ DE PESQUISA PROFUNDA (Use a tag <research_process> trazendo o que você sabe de verdade sobre o local para usar no texto).
2. TÍTULO SUGERIDO (H1 otimizado para SEO).
3. RESUMO / EXCERPT (1 ou 2 frases densas e instigantes para o card do artigo).
4. CONTEÚDO DO ARTIGO (Em Markdown ou HTML limpo, usando subtítulos ## e parágrafos bem estruturados).
5. MARCADORES/TAGS (Crie de 5 a 10 tags baseadas no bairro e no assunto principal, separadas por vírgula).
""".strip()

    @staticmethod
    def build_astro_file(title: str, excerpt: str, body: str, category: str, tags: list, custom_slug: str = None) -> tuple[str, str]:
        """
        Empacota o retorno da IA gerando o arquivo Markdown (.md) com Frontmatter para o AstroWind.
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
        # Normaliza links para o padrão /blog/
        clean_body = re.sub(r'https?://(?:www\.)?saber\.imb\.br/blog/([^"\'\s>]+)', r'/blog/\1', body)
        clean_body = re.sub(r'https?://blog\.saber\.imb\.br/([^"\'\s>]+)', r'/blog/\1', clean_body)

        # Remove qualquer bloco de pesquisa prévia <research_process> se o usuário colar junto
        clean_body = re.sub(r'<research_process>[\s\S]*?<\/research_process>', '', clean_body).strip()

        final_content = f"{frontmatter}\n{clean_body}\n\n{PromptBuilder.CTA_CAPTURE_CODE.strip()}\n"
        return slug, final_content
