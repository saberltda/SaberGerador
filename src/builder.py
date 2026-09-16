"""
Construtor de prompts em lote para artigos Astro Markdown.
"""
from typing import Dict, Any
from src.config import REGRAS_TXT_PATH


def carregar_regras() -> str:
    """Lê o arquivo de regras e diretrizes."""
    if REGRAS_TXT_PATH.exists():
        with open(REGRAS_TXT_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def build_astro_prompt(
    pilar: Dict[str, Any],
    angulo: str,
    formato: str,
    tom: str
) -> str:
    """
    Gera um bloco de instrução autocontido e pronto para colar no Gemini.
    """
    regras = carregar_regras()
    
    prompt = f"""### TAREFA: GERAR ARTIGO EM MARKDOWN (.MD) PARA ASTRO BLOG

{regras}

---
DADOS DO TEMA ESCOLHIDO:
- Pilar Central: {pilar.get('nome')}
- Conflito / Dor Urbana: {pilar.get('dor')}
- Aspiração / Experiência: {pilar.get('aspiracao')}
- Contexto Físico Implícito: {pilar.get('cenario_implicito')}
- Ângulo de Abordagem: {angulo}
- Formato Textual: {formato}
- Tom de Voz: {tom}

---
INSTRUÇÃO FINAL PARA O MODELO:
Gere o artigo completo formatado estritamente como arquivo .md compatível com Astro, iniciando obrigatoriamente com o frontmatter YAML demarcado por '---'. Não faça saudações antes do markdown.
"""
    return prompt.strip()
