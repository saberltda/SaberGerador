import random
from typing import Dict, Any, List, Set


class AffinityMatrix:
    """
    Matriz de compatibilidade semântica e harmonia cruzada entre eixos.
    Calcula scores de 0.0 a 1.0 e aplica filtros conceituais para garantir
    combinações coerentes antes da compilação do prompt.
    """

    def __init__(self):
        # Mapeamento de afinidade conceitual entre núcleos de temas e personas
        self._affinity_keywords: Dict[str, Set[str]] = {
            "tech": {"tech", "software", "remoto", "digital", "startup", "programador"},
            "saude": {"médico", "cirurgião", "saúde", "sono", "cortisol", "clínico", "hospital", "biológico"},
            "familia": {"filho", "escola", "infância", "criança", "pais", "paternidade", "multigeracional"},
            "esporte": {"atleta", "triatlo", "corrida", "ciclismo", "maratona", "raquete", "tênis", "endurance"},
            "equestre": {"hipismo", "polo", "haras", "cavalo", "equestre", "helvetia"},
            "executivo": {"executivo", "multinacional", "viracopos", "diretor", "c-level", "reunião"},
            "longevidade": {"aposentado", "longevidade", "zona azul", "idoso", "caminhabilidade"},
            "natureza": {"biofilia", "verde", "parque", "árvores", "jardim", "horizonte", "quintal"}
        }

    def _extract_text_blob(self, entity: Dict[str, Any]) -> str:
        """Agrega os campos textuais de um dicionário para busca por afinidade."""
        parts = []
        for k, v in entity.items():
            if isinstance(v, str):
                parts.append(v.lower())
        return " ".join(parts)

    def calculate_affinity_score(self, entity_a: Dict[str, Any], entity_b: Dict[str, Any]) -> float:
        """
        Calcula a compatibilidade semântica (0.0 a 1.0) entre dois elementos
        com base na interseção de núcleos conceituais.
        """
        if not entity_a or not entity_b:
            return 0.5

        blob_a = self._extract_text_blob(entity_a)
        blob_b = self._extract_text_blob(entity_b)

        matches = 0
        total_checks = 0

        for _, kw_set in self._affinity_keywords.items():
            in_a = any(kw in blob_a for kw in kw_set)
            in_b = any(kw in blob_b for kw in kw_set)
            if in_a or in_b:
                total_checks += 1
                if in_a and in_b:
                    matches += 1

        if total_checks == 0:
            return 0.6  # Afinidade neutra permissiva
        
        score = matches / total_checks
        # Normalização com patamar mínimo de compatibilidade
        return round(0.3 + (score * 0.7), 2)

    def sample_compatible_theme(self, persona: Dict[str, Any], themes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Amostra um macro tema com probabilidade ponderada pela afinidade com a persona."""
        if not themes:
            return {}
        if not persona:
            return random.choice(themes)

        scored = [(t, self.calculate_affinity_score(persona, t)) for t in themes]
        scored.sort(key=lambda x: x[1], reverse=True)
        # Seleciona entre os 30% mais compatíveis para unir coerência e variedade
        top_slice = scored[: max(3, int(len(scored) * 0.3))]
        return random.choice(top_slice)[0]

    def sample_compatible_pain(
        self, persona: Dict[str, Any], theme: Dict[str, Any], pains: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Amostra um ponto de dor alinhado tanto com a persona quanto com o tema central."""
        if not pains:
            return {}

        scored = []
        for p in pains:
            score_persona = self.calculate_affinity_score(persona, p)
            score_theme = self.calculate_affinity_score(theme, p)
            combined = (score_persona * 0.6) + (score_theme * 0.4)
            scored.append((p, combined))

        scored.sort(key=lambda x: x[1], reverse=True)
        top_slice = scored[: max(3, int(len(scored) * 0.3))]
        return random.choice(top_slice)[0]

    def sample_compatible_differential(
        self, theme: Dict[str, Any], pain: Dict[str, Any], differentials: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Amostra o diferencial de Indaiatuba que melhor responde à dor e ao tema sorteados."""
        if not differentials:
            return {}

        scored = []
        for d in differentials:
            score_theme = self.calculate_affinity_score(theme, d)
            score_pain = self.calculate_affinity_score(pain, d)
            combined = (score_pain * 0.6) + (score_theme * 0.4)
            scored.append((d, combined))

        scored.sort(key=lambda x: x[1], reverse=True)
        top_slice = scored[: max(3, int(len(scored) * 0.3))]
        return random.choice(top_slice)[0]

    def sample_compatible_neighborhood(
        self, persona: Dict[str, Any], neighborhoods: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Amostra um bairro ou microterritório preservando coerência de perfil."""
        if not neighborhoods:
            return {}

        persona_blob = self._extract_text_blob(persona)

        # Regra de afinidade direta para polos específicos
        if "equestre" in persona_blob or "hipismo" in persona_blob or "polo" in persona_blob:
            for b in neighborhoods:
                if "helvetia" in b.get("nome", "").lower():
                    return b

        return random.choice(neighborhoods)

    def sample_compatible_tone(
        self, format_item: Dict[str, Any], theme: Dict[str, Any], tones: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Amostra um tom de voz condizente com o veículo/formato e o tema central."""
        if not tones:
            return {}
        scored = [(t, self.calculate_affinity_score(theme, t)) for t in tones]
        scored.sort(key=lambda x: x[1], reverse=True)
        top_slice = scored[: max(2, int(len(scored) * 0.4))]
        return random.choice(top_slice)[0]

    def sample_compatible_anchor(
        self, persona: Dict[str, Any], theme: Dict[str, Any], anchors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Amostra a âncora Saber mais condizente com a dor e os valores da persona."""
        if not anchors:
            return {}
        scored = []
        for a in anchors:
            s_persona = self.calculate_affinity_score(persona, a)
            s_theme = self.calculate_affinity_score(theme, a)
            scored.append((a, (s_persona * 0.7) + (s_theme * 0.3)))

        scored.sort(key=lambda x: x[1], reverse=True)
        top_slice = scored[: max(2, int(len(scored) * 0.35))]
        return random.choice(top_slice)[0]
