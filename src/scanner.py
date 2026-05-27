# src/scanner.py
import json
import urllib.request
import ssl
import re
from .config import GenesisConfig

class BlogScanner:
    """
    O 'Espião' (Versão Refatorada).
    Acessa o feed público do Blogger para mapear publicações.
    Usa extração de Tags (Categories) para precisão absoluta e regex estrito como fallback.
    """
    
    def __init__(self):
        base_url = GenesisConfig.BLOG_URL
        self.feed_url = f"{base_url}/feeds/posts/default?alt=json&max-results=9999"
        self.titulos_publicados = []
        self.tags_publicadas = set()

    def mapear(self):
        self.titulos_publicados = []
        self.tags_publicadas = set()
        
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(self.feed_url, context=ctx, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    
                    if "feed" in data and "entry" in data["feed"]:
                        for entry in data["feed"]["entry"]:
                            titulo = entry["title"]["$t"]
                            self.titulos_publicados.append(titulo)
                            
                            # Extrai as tags exatas (precisão máxima contra falsos positivos)
                            if "category" in entry:
                                for cat in entry["category"]:
                                    tag = cat.get("term", "").strip().lower()
                                    if tag:
                                        self.tags_publicadas.add(tag)
                                        
        except Exception as e:
            print(f"Aviso: Não foi possível escanear o feed do blog. Erro: {e}")

    def ja_publicado(self, nome_bairro: str) -> bool:
        """
        Verifica se a localidade já foi pauta recente.
        Blindado contra colisões parciais (ex: 'Vista' não dará match em 'Bela Vista').
        """
        if not nome_bairro or nome_bairro.lower() == "indaiatuba":
            return False
            
        bairro_lower = nome_bairro.lower().strip()
        
        # 1. Validação Primária: Busca Exata nas Tags do Post
        # Se a pauta foi sobre "Bela Vista", a tag será "bela vista". 
        # Uma busca isolada por "vista" retornará False, evitando colisões.
        if bairro_lower in self.tags_publicadas:
            return True

        # 2. Validação Secundária: Expressão Regular no Título
        # Fallback seguro que exige limites claros de palavra (\b)
        padrao = r'\b' + re.escape(nome_bairro) + r'\b'
        for titulo in self.titulos_publicados:
            if re.search(padrao, titulo, re.IGNORECASE):
                return True
                
        return False

    def get_ultimos_titulos(self, limite=10):
        return self.titulos_publicados[:limite]
