"""
Configurações e caminhos globais do SaberGerador.
"""
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# Caminhos dos arquivos de dados
PILARES_JSON_PATH = ASSETS_DIR / "pilares_estilo_de_vida.json"
BAIRROS_JSON_PATH = ASSETS_DIR / "bairros.json"
REGRAS_TXT_PATH = ASSETS_DIR / "REGRAS.txt"
