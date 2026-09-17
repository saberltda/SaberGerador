import json
import logging
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
    REGRAS_PATH,
    ASSETS_DIR,
    BASE_DIR
)

logger = logging.getLogger(__name__)


class Database:
    """
    Repositório central de dados e taxonomias do Gerador Saber V2.
    Garante o carregamento completo dos 8 eixos taxonômicos para atingir
    e ultrapassar a meta de 10 milhões de combinações teóricas auditadas.
    """

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

    def _resolve_candidate_path(self, canonical_path: Path) -> Path:
        """
        Garante a localização do arquivo mesmo se a execução do Streamlit
        for iniciada de diretórios alternativos (ex: raiz, /src, etc.).
        """
        if canonical_path.exists():
            return canonical_path

        # Tenta buscar relativo ao diretório de trabalho atual
        cwd_candidate = Path.cwd() / canonical_path.name
        if cwd_candidate.exists():
            return cwd_candidate

        # Tenta dentro de assets ou assets/taxonomy relativo ao CWD
        cwd_asset = Path.cwd() / "assets" / canonical_path.name
        if cwd_asset.exists():
            return cwd_asset

        cwd_taxonomy = Path.cwd() / "assets" / "taxonomy" / canonical_path.name
        if cwd_taxonomy.exists():
            return cwd_taxonomy

        return canonical_path

    def _load_json(self, path: Path, default: Any = None) -> Any:
        resolved_path = self._resolve_candidate_path(path)
        if not resolved_path.exists():
            logger.warning(f"Arquivo não encontrado: {resolved_path}")
            return default if default is not None else []
        try:
            with open(resolved_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            logger.error(f"Erro ao carregar JSON em {resolved_path}: {e}")
            return default if default is not None else []

    def _load_text(self, path: Path) -> str:
        resolved_path = self._resolve_candidate_path(path)
        if not resolved_path.exists():
            return ""
        try:
            with open(resolved_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Erro ao ler texto em {resolved_path}: {e}")
            return ""

    def _normalize_bairros(self, raw_bairros: Any) -> List[Dict[str, Any]]:
        """
        Normaliza os bairros de assets/bairros.json para formato homogêneo.
        Trata listas simples, listas de dicts ou estruturas agrupadas por categoria.
        """
        normalized: List[Dict[str, Any]] = []
        if isinstance(raw_bairros, list):
            for item in raw_bairros:
                if isinstance(item, str):
                    clean_name = item.strip()
                    if clean_name:
                        normalized.append({"id": clean_name, "nome": clean_name})
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

        # Fallback de integridade: caso bairros.json esteja ausente ou vazio,
        # injeta os microterritórios estratégicos canônicos da Constituição
        if not normalized:
            fallback_bairros = [
                "Helvetia Country", "Jardim Esplanada", "Vila Suíça", "Cidade Nova",
                "Chácara Areal", "Itaici", "Condomínio Terras de Itaici", "Jardim Pau Preto",
                "Colinas de Indaiatuba", "Jardim Europa", "Mosteiro de Itaici", "Vale das Laranjeiras",
                "Vila Castelo Branco", "Portal do Sol", "Jardim Bela Vista", "Parque das Nações",
                "Jardim Morada do Sol", "Vila Furlan", "Jardim Regina", "Residencial Dona Maria José"
            ]
            for b in fallback_bairros:
                normalized.append({"id": b, "nome": b})

        return normalized

    def reload_all(self) -> None:
        """Carrega e valida o conjunto completo dos 8 eixos em memória."""
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
