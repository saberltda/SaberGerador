# src/database.py
import json
import os
from .utils import slugify
from .config import GenesisConfig 

class GenesisData:
    def __init__(self, bairros_path: str = "assets/bairros.json"):
        """
        Carrega a lista de bairros e sanitiza os ativos imobiliários e do portal.
        """
        self.bairros = self._carregar_bairros(bairros_path)

        # 1. ATIVOS DA IMOBILIÁRIA (Normalização Case-Insensitive)
        self.ativos_imobiliaria = GenesisConfig.ASSETS_CATALOG
        self.ativos_por_cluster = self.ativos_imobiliaria 

        raw_assets = []
        for lista in self.ativos_imobiliaria.values():
            # Remove espaços perdidos nas bordas de cada string
            raw_assets.extend([item.strip() for item in lista])
            
        # Deduplicação baseada em lowercase para evitar que "Casa" e "CASA" se multipliquem
        unique_assets = {asset.lower(): asset for asset in raw_assets}
        
        # Ordenação alfabética
        self.todos_ativos_imoveis = sorted(list(unique_assets.values()))

        # 2. ATIVOS DO PORTAL (Normalização Case-Insensitive)
        self.ativos_portal = GenesisConfig.PORTAL_CATALOG
        raw_portal = []
        for lista in self.ativos_portal.values():
            raw_portal.extend([item.strip() for item in lista])
            
        unique_portal = {asset.lower(): asset for asset in raw_portal}
        self.todos_ativos_portal = sorted(list(unique_portal.values()))
        
        # Força o item destaque para o topo da lista
        ITEM_DESTAQUE = "Resumo das Principais Notícias do Dia"
        if ITEM_DESTAQUE in self.todos_ativos_portal:
            self.todos_ativos_portal.remove(ITEM_DESTAQUE)
            self.todos_ativos_portal.insert(0, ITEM_DESTAQUE)

        # Para compatibilidade, 'todos_ativos' padrão continua sendo imóveis
        self.todos_ativos = self.todos_ativos_imoveis

    def _carregar_bairros(self, path: str):
        if not os.path.exists(path):
            if os.path.exists(f"../{path}"):
                path = f"../{path}"
            else:
                raise RuntimeError(
                    f"ERRO CRÍTICO: Arquivo '{path}' não encontrado. "
                    "Verifique se a pasta 'assets' está na raiz do projeto."
                )

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Erro ao ler JSON de bairros: {e}")

        bairros_enriquecidos = []
        
        def _map_zona(zona_texto: str):
            z = str(zona_texto).lower().strip()
            if "industrial" in z or "empresarial" in z: return "industrial"
            if "condomínio" in z and "fechado" in z: return "residencial_fechado"
            if "chácara" in z: return "chacaras_aberto" if "aberto" in z else "chacaras_fechado"
            if "mista" in z: return "mista"
            return "residencial_aberto"

        for b in raw:
            b2 = dict(b)
            nome_limpo = str(b.get("nome", "")).strip()
            b2["nome"] = nome_limpo
            b2["slug"] = slugify(nome_limpo)
            b2["zona_normalizada"] = _map_zona(b.get("zona", ""))
            bairros_enriquecidos.append(b2)

        return bairros_enriquecidos


class GenesisRules:
    """
    Gerenciador de Regras de Compliance (Constituição do Blog).
    Lê o arquivo REGRAS.txt e injeta no prompt as variáveis de contexto geográfico.
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
        """
        Substitui as tags de localização criadas no arquivo de REGRAS.txt.
        """
        txt = self.raw_text
        txt = txt.replace("{{BAIRRO}}", bairro_nome)
        txt = txt.replace("{{LOCAL}}", localidade_macro)
        return txt
