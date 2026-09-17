import os
from pathlib import Path
from pydantic import BaseModel, Field

# Resolução Dinâmica e Robusta dos Diretórios do Projeto
CURRENT_FILE: Path = Path(__file__).resolve()
SRC_DIR: Path = CURRENT_FILE.parent
BASE_DIR: Path = SRC_DIR.parent
ASSETS_DIR: Path = BASE_DIR / "assets"
TAXONOMY_DIR: Path = ASSETS_DIR / "taxonomy"
TESTS_DIR: Path = BASE_DIR / "tests"

# Caminhos Canônicos dos Arquivos de Dados e Regras
REGRAS_PATH: Path = ASSETS_DIR / "REGRAS.txt"
BAIRROS_PATH: Path = ASSETS_DIR / "bairros.json"

# Caminhos da Matriz Taxonômica (8 Eixos da Constituição V2.1)
MACRO_TEMAS_PATH: Path = TAXONOMY_DIR / "macro_temas.json"
PERSONAS_PATH: Path = TAXONOMY_DIR / "personas.json"
DORES_PATH: Path = TAXONOMY_DIR / "dores_metropolitanas.json"
DIFERENCIAIS_PATH: Path = TAXONOMY_DIR / "diferenciais_indaiatuba.json"
FORMATOS_PATH: Path = TAXONOMY_DIR / "formatos_conteudo.json"
TONS_PATH: Path = TAXONOMY_DIR / "tons_de_voz.json"
ANCORAS_PATH: Path = TAXONOMY_DIR / "ancoras_saber.json"

# Caminho para Armazenamento Local de Telemetria e Histórico
TELEMETRY_LOG_PATH: Path = BASE_DIR / "telemetry_history.json"


class GenerationSettings(BaseModel):
    """Parâmetros, metas de dimensionamento e cotas mínimas da Constituição V2.1."""
    min_macro_temas: int = Field(default=60, description="Mínimo N1 para Eixo 1")
    min_personas: int = Field(default=40, description="Mínimo N2 para Eixo 2")
    min_dores: int = Field(default=45, description="Mínimo N3 para Eixo 3")
    min_diferenciais: int = Field(default=50, description="Mínimo N4 para Eixo 4")
    min_bairros: int = Field(default=80, description="Mínimo N5 para Eixo 5")
    min_formatos: int = Field(default=25, description="Mínimo N6 para Eixo 6")
    min_tons: int = Field(default=20, description="Mínimo N7 para Eixo 7")
    min_ancoras: int = Field(default=20, description="Mínimo N8 para Eixo 8")

    # Meta mínima combinatória auditada
    min_theoretical_combinations: int = Field(
        default=10_000_000,
        description="Meta de volume teórico mínimo de altíssima qualidade"
    )

    # Proporções Narrativas Canônicas da Constituição ("Vender sem Vender")
    layer1_percentage: str = "65% a 70%"
    layer2_percentage: str = "15% a 20%"
    layer3_percentage: str = "10%"
    layer4_percentage: str = "5%"

    # Configuração de Telemetria
    max_history_entries: int = 20


settings = GenerationSettings()
