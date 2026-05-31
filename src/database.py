# src/database.py
import json
import os
from .utils import slugify

class GenesisData:
    def __init__(self, bairros_path: str = "assets/bairros.json"):
        self.bairros = self._carregar_bairros(bairros_path)

    def _carregar_bairros(self, path: str):
        if not os.path.exists(path):
            if os.path.exists(f"../{path}"):
                path = f"../{path}"
            else:
                raise RuntimeError(
                    f"ERRO CRÍTICO: Arquivo '{path}' não encontrado. "
                )

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Erro ao ler JSON de bairros: {e}")

        bairros_enriquecidos = []
        
        for b in raw:
            b2 = dict(b)
            nome_limpo = str(b.get("nome", "")).strip()
            b2["nome"] = nome_limpo
            b2["slug"] = slugify(nome_limpo)
            
            # Normalização da zona apenas para controle estrutural
            z = str(b.get("zona", "")).lower().strip()
            if "industrial" in z or "empresarial" in z:
                b2["zona_normalizada"] = "industrial"
            elif "condomínio" in z and "fechado" in z:
                b2["zona_normalizada"] = "residencial_fechado"
            elif "chácara" in z:
                b2["zona_normalizada"] = "chacaras"
            else:
                b2["zona_normalizada"] = "residencial_aberto"
                
            bairros_enriquecidos.append(b2)

        return bairros_enriquecidos


class GenesisRules:
    """
    Gerenciador de Regras de Compliance.
    Injeta as variáveis dinâmicas de localização no arquivo de Regras.
    """
    def __init__(self, path: str = "assets/REGRAS.txt"):
        if not os.path.exists(path):
            if os.path.exists(f"../{path}"):
                path = f"../{path}"
            else:
                raise RuntimeError(f"ERRO: Arquivo '{path}' de regras não encontrado.")
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.raw_text = f.read()
        except Exception as e:
            raise RuntimeError(f"Erro ao ler REGRAS.txt: {e}")

    def get_for_prompt(self, bairro_nome: str, localidade_macro: str = "Indaiatuba") -> str:
        txt = self.raw_text
        txt = txt.replace("{{BAIRRO}}", bairro_nome)
        txt = txt.replace("{{LOCAL}}", localidade_macro)
        return txt
