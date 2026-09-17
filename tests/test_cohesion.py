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
    """Valida se as bases de dados cumprem os quantitativos mínimos da Constituição V2.1."""
    assert len(database.macro_temas) >= settings.min_macro_temas
    assert len(database.personas) >= settings.min_personas
    assert len(database.dores) >= settings.min_dores
    assert len(database.diferenciais) >= settings.min_diferenciais
    assert len(database.formatos) >= settings.min_formatos
    assert len(database.tons) >= settings.min_tons
    assert len(database.ancoras) >= settings.min_ancoras


def test_generation_engine_combination(engine):
    """Valida se a geração de combinação entrega os 8 eixos povoados de forma coesa."""
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
    """Valida se a regra rígida de afinidade equestre/Helvetia é respeitada pelo validador."""
    validator = CohesionValidator()
    
    incompatible_candidate = {
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
        "bairro": {"nome": "Jardim Esplanada"},  # Incompatível com tema puramente de haras
        "formato": {"nome": "Artigo"},
        "tom": {"nome": "Clássico"},
        "ancora": {"conceito": "Tradição equestre"},
    }
    assert validator.is_coherent(incompatible_candidate) is False

    compatible_candidate = dict(incompatible_candidate)
    compatible_candidate["bairro"] = {"nome": "Helvetia Country"}
    assert validator.is_coherent(compatible_candidate) is True


def test_prompt_compiler_layers_and_instruction(engine, compiler):
    """Valida se o compilador gera o prompt contendo as 4 camadas e a instrução de pesquisa profunda do bairro."""
    combination = engine.generate_harmonized_combination()
    prompt = compiler.compile(combination)

    # Verifica menção das camadas narrativas
    assert "CAMADA 1: A ISCA UNIVERSAL E O VALOR PURO" in prompt
    assert "CAMADA 2: O CONFLITO GEOGRÁFICO-EXISTENCIAL" in prompt
    assert "CAMADA 3: O MICROTERRITÓRIO COMO RESPOSTA TANGÍVEL" in prompt
    assert "CAMADA 4: A ASSINATURA ELEGANTE E CONSULTIVA" in prompt

    # Verifica menção à Imobiliária Saber e Indaiatuba
    assert "Imobiliária Saber" in prompt
    assert "Indaiatuba" in prompt

    # Verifica a instrução mandatória de pesquisa profunda do bairro
    assert "PESQUISE PROFUNDAMENTE" in prompt
    assert combination["bairro"]["nome"] in prompt
