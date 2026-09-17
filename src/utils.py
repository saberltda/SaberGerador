import re
import unicodedata
from typing import Any, Dict, List


def slugify(text: str) -> str:
    """Normaliza uma string para formato slug (minúsculas, sem acentos e separada por hífens)."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def truncate_text(text: str, max_length: int = 120) -> str:
    """Trunca um texto mantendo palavras inteiras quando possível."""
    if len(text) <= max_length:
        return text
    truncated = text[:max_length].rsplit(" ", 1)[0]
    return f"{truncated}..."


def format_combination_summary(combination: Dict[str, Any]) -> str:
    """Gera um resumo textual legível dos parâmetros de uma combinação sorteada."""
    tema = combination.get("macro_tema", {}).get("titulo", "N/A")
    persona = combination.get("persona", {}).get("nome", "N/A")
    bairro = combination.get("bairro", {}).get("nome", "N/A")
    formato = combination.get("formato", {}).get("nome", "N/A")
    tom = combination.get("tom", {}).get("nome", "N/A")

    return f"[{formato}] {tema} | Persona: {persona} | Bairro: {bairro} | Tom: {tom}"
