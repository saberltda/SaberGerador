import pytest
from src.database import Database
from src.core_engine import GenerationEngine
from src.prompt_compiler import PromptCompiler
from src.affinity_matrix import AffinityMatrix
from src.validator import CohesionValidator
from src.config import settings


@pytest.fixture
def database():
    return Database()


@pytest.fixture
def engine(database):
    return GenerationEngine(database=database)


@pytest.fixture
def compiler():
    return PromptCompiler()


def test_taxonomy_dimensions(database):
    """Valida se as bases cumprem as cotas mínimas da Constituição V2.1."""
    assert len(database.macro_temas) >= settings.min_macro_temas
    assert len(database.personas) >= settings.min_personas
    assert len(database.dores) >= settings.min_dores
    assert len(database.diferenciais) >= settings.min_diferenciais
    assert len(database.formatos) >= settings.min_formatos
    assert len(database.tons) >= settings.min_tons
    assert len(database.ancoras) >= settings.min_ancoras


def test_theoretical_combinations_exceeds_ten_million(engine):
    """Valida se o volume auditado ultrapassa a meta de 10 milhões de combinações."""
    total = engine.get_theoretical_combinations()
    assert total >= settings.min_theoretical_combinations


def test_generation_engine_combination_integrity(engine):
    """Valida se a combinação gerada preenche todos os 8 eixos de forma harmônica."""
    combination = engine.generate_harmonized_combination()
    required_keys = [
        "macro_tema",
        "persona",
        "dor",
        "diferencial_indaiatuba",
        "bairro",
        "formato",
        "tom",
        "ancora",
    ]
    for key in required_keys:
        assert key in combination
        assert bool(combination[key]) is True


def test_equestrian_cohesion_rule():
    """Valida se a regra rígida de afinidade equestre/Helvetia é aplicada pelo validador."""
    validator = CohesionValidator()

    incompatible = {
        "macro_tema": {
            "titulo": "A Cultura Equestre e o Hipismo",
            "premissa_universal": "Cocheiras e cavalos"
        },
        "persona": {
            "nome": "Entusiasta do Hipismo e Polo",
            "valores_centrais": "Vida equestre"
        },
        "dor": {"resumo": "Falta de haras perto"},
        "diferencial_indaiatuba": {"pilar": "Tradição equestre"},
        "bairro": {"nome": "Jardim Esplanada"},
        "formato": {"nome": "Artigo"},
        "tom": {"nome": "Clássico"},
        "ancora": {"conceito": "Tradição equestre"},
    }
    assert validator.is_coherent(incompatible) is False

    compatible = dict(incompatible)
    compatible["bairro"] = {"nome": "Helvetia Country"}
    assert validator.is_coherent(compatible) is True


def test_prompt_compiler_astro_frontmatter_and_seo(engine, compiler):
    """
    Valida se o compilador gera as diretrizes de Markdown para Blog Astro,
    frontmatter YAML de SEO, proibição explícita de campos de data e as 4 camadas narrativas.
    """
    combination = engine.generate_harmonized_combination()
    prompt = compiler.compile(combination)

    # Diretrizes de Saída Astro (.md) e Frontmatter
    assert "ARQUIVO .MD PARA ASTRO COM FRONTMATTER DE SEO (ATEMPORAL)" in prompt
    assert "PROIBIÇÃO TOTAL DE DATAS" in prompt
    assert "canonicalURL" in prompt
    assert "keywords:" in prompt

    # 4 Camadas Narrativas Obrigatórias
    assert "CAMADA 1: A ISCA UNIVERSAL E O VALOR PURO" in prompt
    assert "CAMADA 2: O CONFLITO GEOGRÁFICO-EXISTENCIAL" in prompt
    assert "CAMADA 3: O MICROTERRITÓRIO COMO RESPOSTA TANGÍVEL" in prompt
    assert "CAMADA 4: A ASSINATURA ELEGANTE E CONSULTIVA" in prompt

    # Entidades e Instrução Obrigatória de Pesquisa do Bairro
    assert "Imobiliária Saber" in prompt
    assert "Indaiatuba" in prompt
    assert "PESQUISE PROFUNDAMENTE" in prompt
    assert combination["bairro"]["nome"] in prompt
