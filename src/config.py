import os
from datetime import datetime

# Diretório base do SaberGerador
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Diretório padrão onde o Astro lê os artigos
# Se a pasta C:\blog-saber existir, salva direto nela; senão, salva em dist/posts local
DEFAULT_ASTRO_POSTS_DIR = r"C:\blog-saber\src\data\post"
if os.path.exists(DEFAULT_ASTRO_POSTS_DIR):
    OUTPUT_POSTS_DIR = DEFAULT_ASTRO_POSTS_DIR
else:
    OUTPUT_POSTS_DIR = os.path.join(BASE_DIR, "dist", "posts")

os.makedirs(OUTPUT_POSTS_DIR, exist_ok=True)

# URL Canônica Base
SITE_CANONICAL_BASE = "https://saber.imb.br/blog"

# Formulário Kit.com (embutido no final dos artigos)
FORMKIT_FORM_ID = "8984117"
FORMKIT_UID = "d188d73e78"
