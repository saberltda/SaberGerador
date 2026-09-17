from typing import Dict, Any, Optional
from src.affinity_matrix import AffinityMatrix


class CohesionValidator:
    """
    Validador de coesão semântica e regras invioláveis de compatibilidade
    entre persona, macro tema, dor, diferencial geográfico e microterritório.
    """

    def __init__(self, affinity_matrix: Optional[AffinityMatrix] = None):
        self.affinity_matrix = affinity_matrix or AffinityMatrix()

    def is_coherent(self, combination: Dict[str, Any]) -> bool:
        """
        Avalia se a combinação atende aos critérios de consistência narrativa
        e não viola regras estritas de incongruência.
        """
        if not combination:
            return False

        # Garante que todos os eixos principais estejam povoados
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
            if not combination.get(key):
                return False

        persona = combination["persona"]
        tema = combination["macro_tema"]
        bairro = combination["bairro"]

        # 1. Regra de Incompatibilidade Rígida: Hipismo / Equestre
        persona_text = f"{persona.get('nome', '')} {persona.get('valores_centrais', '')}".lower()
        tema_text = f"{tema.get('titulo', '')} {tema.get('premissa_universal', '')}".lower()
        bairro_name = bairro.get("nome", "").lower()

        is_equestrian_persona = any(kw in persona_text for kw in ["equestre", "hipismo", "polo country"])
        is_equestrian_theme = any(kw in tema_text for kw in ["equestre", "hipismo", "cocheiras"])

        # Se o tema ou persona for estritamente equestre, exige ancoragem em Helvetia ou microterritório rural compatível
        if (is_equestrian_persona or is_equestrian_theme) and "helvetia" not in bairro_name:
            return False

        # 2. Score Mínimo de Harmonia Semântica (Persona x Tema Central)
        score_persona_tema = self.affinity_matrix.calculate_affinity_score(persona, tema)
        if score_persona_tema < 0.35:
            return False

        # 3. Score Mínimo de Harmonia (Tema x Diferencial da Cidade)
        diferencial = combination["diferencial_indaiatuba"]
        score_tema_cidade = self.affinity_matrix.calculate_affinity_score(tema, diferencial)
        if score_tema_cidade < 0.30:
            return False

        return True
