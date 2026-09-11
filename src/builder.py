import re
import unicodedata
from datetime import datetime, timezone

def slugify(value: str) -> str:
    """Normaliza strings removendo acentos e gerando slug seguro para URL e arquivo."""
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-')

def build_kit_form_html() -> str:
    """Gera o formulário HTML do Kit.com para o rodapé do artigo."""
    return """
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

def build_astro_markdown(title: str, excerpt: str, body: str, category: str = "Insights Estratégicos", tags: list = None, custom_slug: str = None) -> tuple[str, str]:
    """
    Gera o conteúdo final no formato Markdown (.md) esperado pelo AstroWind.
    Retorna uma tupla (slug, markdown_string).
    """
    slug = custom_slug if custom_slug else slugify(title)
    iso_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    canonical_url = f"https://saber.imb.br/blog/{slug}"
    
    if not tags:
        tags = ["Indaiatuba", "Mercado Imobiliário", "Investimento"]
        
    tags_yaml = "\n".join([f'  - "{t}"' for t in tags])
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

    clean_body = re.sub(r'https?://(?:www\.)?saber\.imb\.br/blog/([^"\'\s>]+)', r'/blog/\1', body)
    clean_body = re.sub(r'https?://blog\.saber\.imb\.br/([^"\'\s>]+)', r'/blog/\1', clean_body)

    form_html = build_kit_form_html()
    final_content = f"{frontmatter}\n{clean_body.strip()}\n\n{form_html.strip()}\n"
    
    return slug, final_content
