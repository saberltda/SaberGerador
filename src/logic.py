# Adicione estes imports no TOPO do arquivo src/logic.py
from pytrends.request import TrendReq
import time
import random

# ... [código da classe PlanoDiretor continua igual acima] ...

class SEOHeatmap:
    """
    Analisa tendências de busca reais via Google Trends.
    Descobre qual bairro de Indaiatuba está com maior volume de pesquisa.
    """
    def __init__(self):
        try:
            # Conecta ao Google Trends (Idioma PT-BR, Fuso horário de Brasília)
            self.pytrends = TrendReq(hl='pt-BR', tz=180, retries=2, backoff_factor=0.5)
            self.ativo = True
        except Exception as e:
            print(f"Aviso: Não foi possível conectar ao Google Trends: {e}")
            self.ativo = False

    def get_bairro_quente(self, lista_bairros_obj):
        """
        Avalia uma amostra de bairros e retorna o que está com maior tendência de busca.
        """
        if not self.ativo or not lista_bairros_obj:
            return random.choice(lista_bairros_obj)

        # O Google Trends permite comparar no máximo 5 termos por vez.
        amostra = random.sample(lista_bairros_obj, min(5, len(lista_bairros_obj)))
        
        # Monta as palavras-chave (Ex: "Jardim Europa Indaiatuba")
        kw_list = [f"{b['nome']} Indaiatuba" for b in amostra]

        try:
            # Busca os dados dos últimos 30 dias, filtrando para o Estado de SP (BR-SP)
            self.pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m', geo='BR-SP')
            df = self.pytrends.interest_over_time()

            if df.empty:
                return random.choice(amostra)

            # Calcula a média de interesse de cada bairro nos últimos 30 dias
            medias = df.mean().drop('isPartial', errors='ignore')
            
            # Encontra a palavra-chave com a maior média de buscas
            melhor_kw = medias.idxmax()
            
            # Retorna o nome original do bairro (removendo a palavra ' Indaiatuba')
            nome_vencedor = melhor_kw.replace(" Indaiatuba", "")
            
            for b in amostra:
                if b['nome'] == nome_vencedor:
                    return b
                    
        except Exception as e:
            print(f"Aviso: Timeout ou limite de requisições no Google Trends. Usando fallback. Erro: {e}")
            
        # Fallback de segurança caso a API limite as requisições
        return random.choice(amostra)
