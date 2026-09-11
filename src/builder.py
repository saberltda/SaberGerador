import re
from datetime import datetime, timezone
from src.config import SITE_CANONICAL_BASE, FORMKIT_FORM_ID, FORMKIT_UID
from src.utils import slugify

def build_kit_form_html():
    """Gera o bloco de formulário HTML do Kit.com idêntico ao dos artigos originais."""
    return f"""
<div>
<form action="https://app.kit.com/forms/{FORMKIT_FORM_ID}/subscriptions" class="seva-form formkit-form" method="post" data-sv-form="{FORMKIT_FORM_ID}" data-uid="{FORMKIT_UID}" data-format="inline" data-version="5" style="background-color:#f9fafb;border-radius:4px;padding:20px;border:1px solid #e3e3e3;margin-top:2rem;">
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

def build_astro_post(title: str, excerpt: str, body_markdown: str, category: str = "Insights Estratégicos", tags: list = None, slug: str = None, publish_date: datetime = None) -> tuple[str, str]:
    """
    Monta o arquivo Markdown (.md) completo para o AstroWind.
    Retorna (slug, conteúdo_final_markdown).
    """
    if not slug:
        slug = slugify(title)
        
    if not publish_date:
        publish_date = datetime.now(timezone.utc)
        
    iso_date = publish_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    canonical_url = f"{SITE_CANONICAL_BASE}/{slug}"
    
    if not tags:
        tags = ["Indaiatuba", "Mercado Imobiliário", "Investimento"]
        
    tags_yaml = "\n".join([f'  - "{t}"' for t in tags])
    clean_title = title.replace('"', '\\"')
    clean_excerpt = excerpt.replace('"', '\\"')

    # Cabeçalho Frontmatter padrão do AstroWind
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

    # Ajusta referências a links para a nova rota interna /blog/
    body_markdown = re.sub(r'https?://(?:www\.)?saber\.imb\.br/blog/([^"\'\s>]+)', r'/blog/\1', body_markdown)
    body_markdown = re.sub(r'https?://blog\.saber\.imb\.br/([^"\'\s>]+)', r'/blog/\1', body_markdown)

    form_html = build_kit_form_html()
    
    final_content = f"{frontmatter}\n{body_markdown.strip()}\n\n{form_html.strip()}\n"
    return slug, final_content
