import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import (
    MACRO_TEMAS_PATH,
    PERSONAS_PATH,
    DORES_PATH,
    DIFERENCIAIS_PATH,
    BAIRROS_PATH,
    FORMATOS_PATH,
    TONS_PATH,
    ANCORAS_PATH,
    REGRAS_PATH
)


class Database:
    """Repositório de dados e carregamento de taxonomias para o Gerador Saber V2."""

    def __init__(self):
        self._macro_temas: List[Dict[str, Any]] = []
        self._personas: List[Dict[str, Any]] = []
        self._dores: List[Dict[str, Any]] = []
        self._diferenciais: List[Dict[str, Any]] = []
        self._bairros: List[Dict[str, Any]] = []
        self._formatos: List[Dict[str, Any]] = []
        self._tons: List[Dict[str, Any]] = []
        self._ancoras: List[Dict[str, Any]] = []
        self._regras_editoriais: str = ""
        self.reload_all()

    def _load_json(self, path: Path, default: Any = None) -> Any:
        if default is None:
            default = []
        if not path.exists():
            return default
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    def _load_text(self, path: Path) -> str:
        if not path.exists():
            return ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _normalize_bairros(self, raw_bairros: Any) -> List[Dict[str, Any]]:
        """
        Normaliza os bairros de assets/bairros.json para formato homogêneo de dicionários.
        Garante compatibilidade caso o arquivo original seja lista de strings,
        lista de dicts ou dicionário de categorias.
        """
        normalized: List[Dict[str, Any]] = []
        if isinstance(raw_bairros, list):
            for item in raw_bairros:
                if isinstance(item, str):
                    normalized.append({"id": item, "nome": item})
                elif isinstance(item, dict):
                    nome = item.get("nome") or item.get("id") or "Bairro Indaiatuba"
                    item_copy = dict(item)
                    item_copy.setdefault("id", nome)
                    item_copy.setdefault("nome", nome)
                    normalized.append(item_copy)
        elif isinstance(raw_bairros, dict):
            for k, v in raw_bairros.items():
                if isinstance(v, list):
                    for sub in v:
                        if isinstance(sub, str):
                            normalized.append({"id": f"{k}_{sub}", "nome": sub, "categoria": k})
                        elif isinstance(sub, dict):
                            nome = sub.get("nome") or sub.get("id") or str(sub)
                            sub_copy = dict(sub)
                            sub_copy.setdefault("id", f"{k}_{nome}")
                            sub_copy.setdefault("nome", nome)
                            sub_copy.setdefault("categoria", k)
                            normalized.append(sub_copy)
                elif isinstance(v, dict):
                    nome = v.get("nome") or k
                    v_copy = dict(v)
                    v_copy.setdefault("id", k)
                    v_copy.setdefault("nome", nome)
                    normalized.append(v_copy)
                else:
                    normalized.append({"id": k, "nome": str(v)})
        return normalized

    def reload_all(self) -> None:
        """Recarrega todos os 8 eixos e regras editoriais da memória física."""
        self._macro_temas = self._load_json(MACRO_TEMAS_PATH)
        self._personas = self._load_json(PERSONAS_PATH)
        self._dores = self._load_json(DORES_PATH)
        self._diferenciais = self._load_json(DIFERENCIAIS_PATH)
        
        raw_bairros = self._load_json(BAIRROS_PATH)
        self._bairros = self._normalize_bairros(raw_bairros)
        
        self._formatos = self._load_json(FORMATOS_PATH)
        self._tons = self._load_json(TONS_PATH)
        self._ancoras = self._load_json(ANCORAS_PATH)
        self._regras_editoriais = self._load_text(REGRAS_PATH)

    # Propriedades de acesso direto
    @property
    def macro_temas(self) -> List[Dict[str, Any]]:
        return self._macro_temas

    @property
    def personas(self) -> List[Dict[str, Any]]:
        return self._personas

    @property
    def dores(self) -> List[Dict[str, Any]]:
        return self._dores

    @property
    def diferenciais(self) -> List[Dict[str, Any]]:
        return self._diferenciais

    @property
    def bairros(self) -> List[Dict[str, Any]]:
        return self._bairros

    @property
    def formatos(self) -> List[Dict[str, Any]]:
        return self._formatos

    @property
    def tons(self) -> List[Dict[str, Any]]:
        return self._tons

    @property
    def ancoras(self) -> List[Dict[str, Any]]:
        return self._ancoras

    @property
    def regras_editoriais(self) -> str:
        return self._regras_editoriais

    def get_by_label(self, axis: str, label: str) -> Optional[Dict[str, Any]]:
        """Busca um item de um eixo pelo seu nome, título, resumo ou id."""
        dataset = getattr(self, axis, [])
        for item in dataset:
            identifier = (
                item.get("nome")
                or item.get("titulo")
                or item.get("resumo")
                or item.get("pilar")
                or item.get("conceito")
                or item.get("id")
            )
            if identifier == label:
                return item
        return None
