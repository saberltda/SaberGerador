import os
import pytz

class GenesisConfig:
    VERSION = "7.2.0"
    TZ_BRASILIA = pytz.timezone("America/Sao_Paulo")
    FUSO_PADRAO = "-03:00"

# Caminhos e configurações do AstroWind
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ASTRO_POSTS_DIR = r"C:\blog-saber\src\data\post"
OUTPUT_POSTS_DIR = DEFAULT_ASTRO_POSTS_DIR if os.path.exists(DEFAULT_ASTRO_POSTS_DIR) else os.path.join(BASE_DIR, "dist", "posts")
os.makedirs(OUTPUT_POSTS_DIR, exist_ok=True)

SITE_CANONICAL_BASE = "https://saber.imb.br/blog"
FORMKIT_FORM_ID = "8984117"
FORMKIT_UID = "d188d73e78"
