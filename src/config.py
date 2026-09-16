"""
Configurações e caminhos globais do SaberGerador.
"""
import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# Caminhos dos arquivos de dados
PILARES_JSON_PATH = ASSETS_DIR / "pilares_estilo_de_vida.json"
BAIRROS_JSON_PATH = ASSETS_DIR / "bairros.json"
REGRAS_TXT_PATH = ASSETS_DIR / "REGRAS.txt"

# Modelos e Chaves
DEFAULT_MODEL_NAME = "gemini-2.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
