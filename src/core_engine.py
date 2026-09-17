import random
from typing import Dict, Any, List, Optional
from src.database import Database
from src.affinity_matrix import AffinityMatrix
from src.validator import CohesionValidator


class GenerationEngine:
    """Motor combinatório inteligente baseado na Matriz de 8 Eixos com filtros de afinidade semântica."""

    def __init__(self, database: Optional[Database] = None):
        self.db = database or Database()
        self.affinity = AffinityMatrix()
        self.validator = CohesionValidator(affinity_matrix=self.affinity)

    def get_theoretical_combinations(self) -> int:
        """Calcula o volume teórico de combinações segundo N1 x N2 x ... x N8."""
        counts = [
            len(self.db.macro_temas) or 1,
            len(self.db.personas) or 1,
            len(self.db.dores) or 1,
            len(self.db.diferenciais) or 1,
            len(self.db.bairros) or 1,
            len(self.db.formatos) or 1,
            len(self.db.tons) or 1,
            len(self.db.ancoras) or 1,
        ]
        total = 1
        for c in counts:
            total *= c
        return total

    def get_options(self, axis_key: str) -> List[str]:
        """Retorna os rótulos de cada eixo para preenchimento dos menus do Streamlit."""
        mapping = {
            "macro_temas": (self.db.macro_temas, "titulo"),
            "personas": (self.db.personas, "nome"),
            "dores": (self.db.dores, "resumo"),
            "diferenciais_indaiatuba": (self.db.diferenciais, "pilar"),
            "bairros": (self.db.bairros, "nome"),
            "formatos": (self.db.formatos, "nome"),
            "tons": (self.db.tons, "nome"),
            "ancoras": (self.db.ancoras, "conceito"),
        }
        dataset, field = mapping.get(axis_key, ([], "nome"))
        options = []
        for item in dataset:
            val = item.get(field) or item.get("nome") or item.get("id")
            if val:
                options.append(str(val))
        return options

    def generate_harmonized_combination(
        self, overrides: Optional[Dict[str, Optional[str]]] = None, max_attempts: int = 50
    ) -> Dict[str, Any]:
        """
        Gera uma combinação harmônica aplicando afinidade semântica e respeitando
        quaisquer parâmetros sobrescritos manualmente pelo operador.
        """
        overrides = overrides or {}

        for _ in range(max_attempts):
            # 1. Seleciona ou resgata Persona
            if overrides.get("persona"):
                persona = self.db.get_by_label("personas", overrides["persona"]) or random.choice(self.db.personas)
            else:
                persona = random.choice(self.db.personas) if self.db.personas else {}

            # 2. Seleciona Macro Tema guiado por afinidade
            if overrides.get("macro_tema"):
                tema = self.db.get_by_label("macro_temas", overrides["macro_tema"]) or random.choice(self.db.macro_temas)
            else:
                tema = self.affinity.sample_compatible_theme(persona, self.db.macro_temas)

            # 3. Seleciona Ponto de Dor guiado por afinidade
            if overrides.get("dor"):
                dor = self.db.get_by_label("dores", overrides["dor"]) or random.choice(self.db.dores)
            else:
                dor = self.affinity.sample_compatible_pain(persona, tema, self.db.dores)

            # 4. Seleciona Revelação Geográfica / Diferencial Indaiatuba
            if overrides.get("diferencial_indaiatuba"):
                diferencial = self.db.get_by_label("diferenciais", overrides["diferencial_indaiatuba"]) or random.choice(self.db.diferenciais)
            else:
                diferencial = self.affinity.sample_compatible_differential(tema, dor, self.db.diferenciais)

            # 5. Seleciona Bairro / Microterritório (assets/bairros.json)
            if overrides.get("bairro"):
                bairro = self.db.get_by_label("bairros", overrides["bairro"]) or random.choice(self.db.bairros)
            else:
                bairro = self.affinity.sample_compatible_neighborhood(persona, self.db.bairros)

            # 6. Formato de Conteúdo
            if overrides.get("formato"):
                formato = self.db.get_by_label("formatos", overrides["formato"]) or random.choice(self.db.formatos)
            else:
                formato = random.choice(self.db.formatos) if self.db.formatos else {}

            # 7. Tom de Voz
            if overrides.get("tom"):
                tom = self.db.get_by_label("tons", overrides["tom"]) or random.choice(self.db.tons)
            else:
                tom = self.affinity.sample_compatible_tone(formato, tema, self.db.tons)

            # 8. Âncora Saber
            if overrides.get("ancora"):
                ancora = self.db.get_by_label("ancoras", overrides["ancora"]) or random.choice(self.db.ancoras)
            else:
                ancora = self.affinity.sample_compatible_anchor(persona, tema, self.db.ancoras)

            candidate = {
                "macro_tema": tema,
                "persona": persona,
                "dor": dor,
                "diferencial_indaiatuba": diferencial,
                "bairro": bairro,
                "formato": formato,
                "tom": tom,
                "ancora": ancora,
            }

            # Validação de coesão ortogonal
            if self.validator.is_coherent(candidate):
                return candidate

        # Fallback seguro para o último candidato gerado
        return candidate
