# src/logic.py
import random
import time
from .config import GenesisConfig

# ====================================================
# TENTATIVA SEGURA DE IMPORTAÇÃO (Graceful Fallback)
# Evita que o app quebre no Streamlit Cloud se a 
# biblioteca pytrends não for instalada corretamente.
# ====================================================
try:
    from pytrends.request import TrendReq
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False
    print("Aviso: Biblioteca pytrends não encontrada. O SEOHeatmap operará em modo offline (sorteio).")


class PlanoDiretor:
    """
    Lógica de Compatibilidade Física (O 'Engenheiro').
    Verifica a tipologia do ativo e do bairro para impedir combinações incoerentes.
    """
    def refinar_ativo(self, cluster, bairro, ativos_base):
        zona = bairro.get("zona_normalizada", "indefinido")
        
        if isinstance(ativos_base, str):
            ativos_base = [ativos_base]
            
        ativo_final = random.choice(ativos_base)
        ativo_lower = ativo_final.lower()
        obs = f"Compatível com {zona}"

        # 1. Mapeamento de Tipologia (Case-Insensitive)
        is_condominio = "condomínio" in ativo_lower
        is_rural = cluster == "RURAL_LIFESTYLE" or "chácara" in ativo_lower or "sítio" in ativo_lower or "haras" in ativo_lower
        is_industrial = cluster == "LOGISTICS" or "galpão" in ativo_lower or "industrial" in ativo_lower
        is_apartamento = "apartamento" in ativo_lower or "studio" in ativo_lower or "cobertura" in ativo_lower

        # 2. Aplicação de Barreiras Lógicas Rígidas
        if zona == "industrial":
            if not is_industrial and cluster != "CORPORATE":
                ativo_final = "Terreno Industrial / Galpão Logístico"
                obs = "Ajuste Automático: Zona industrial não permite imóveis puramente residenciais."
        
        elif zona == "residencial_aberto":
            if is_condominio:
                ativo_final = "Casa de Rua / Sobrado Moderno"
                obs = "Ajuste Automático: Bairro de malha aberta não comporta condomínio fechado."
            if is_industrial:
                ativo_final = "Terreno Residencial"
                obs = "Ajuste Automático: Bairro residencial não comporta pólos industriais."
                
        elif zona == "residencial_fechado":
            # Em loteamento fechado, forçamos o rótulo de condomínio
            if not is_condominio and cluster in ["FAMILY", "HIGH_END"]:
                ativo_final = "Casa em Condomínio Fechado"
                obs = "Ajuste Automático: Zona exige tipologia controlada (condomínio)."
            if is_industrial:
                ativo_final = "Terreno em Condomínio"
                obs = "Ajuste Automático: Condomínio residencial fechado não aceita indústria."
                
        elif "chacaras" in zona:
            if is_apartamento:
                ativo_final = "Sítio de Lazer / Chácara"
                obs = "Ajuste Automático: Área rural ou de chácaras não permite verticalização densa."

        # 3. Blindagem de Isolamento Rural
        if is_rural and zona not in ["chacaras_aberto", "chacaras_fechado", "mista", "indefinido"]:
            ativo_final = "Casa Térrea com Quintal Amplo"
            obs = "Ajuste Automático: Ativo de características rurais adaptado para tipologia urbana compatível."

        return ativo_final, obs


class SEOHeatmap:
    """
    Analisa tendências de busca reais via Google Trends.
    Descobre qual bairro de Indaiatuba está com maior volume de pesquisa.
    """
    def __init__(self):
        self.ativo = False
        if HAS_PYTRENDS:
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


class RiscoJuridico:
    """
    (Placeholder) Verifica riscos legais básicos do ativo.
    Mantido para compatibilidade arquitetural com engine.py.
    """
    pass


class PortalSynchronizer:
    """
    Gerencia as listas e opções exclusivas do MODO PORTAL.
    """
    def get_editorias_display(self):
        raw = GenesisConfig.PORTAL_CATALOG
        
        labels_map = {
            "DESTAQUE_DIARIO": "🚨 Destaque / Resumo do Dia",
            "CIDADE_ALERTA": "🚔 Cidade Alerta (Polícia/Trânsito)",
            "PODER_POLITICA": "⚖️ Poder & Política",
            "VIVER_INDAIATUBA": "🎭 Viver Indaiatuba (Lazer/Cultura)",
            "SEU_DINHEIRO": "💰 Seu Dinheiro (Economia)",
            "EDUCACAO_FUTURO": "🎓 Educação & Futuro",
            "COMUNIDADE": "🤝 Comunidade & Pets"
        }
        
        display_list = []
        for k in raw.keys():
            label = labels_map.get(k, k.replace("_", " ").title())
            display_list.append((k, label))
        return display_list
    
    def get_valid_topics(self, editoria_key):
        return list(GenesisConfig.PORTAL_TOPICS_MAP.items())

    def get_valid_formats(self, editoria_key):
        return list(GenesisConfig.PORTAL_FORMATS_MAP.items())
    
    def get_random_set(self):
        editoria_key = random.choice(list(GenesisConfig.PORTAL_CATALOG.keys()))
        editoria_label = GenesisConfig.PORTAL_CATALOG[editoria_key][0]
        
        topico = random.choice(list(GenesisConfig.PORTAL_TOPICS_MAP.items()))
        formato = random.choice(list(GenesisConfig.PORTAL_FORMATS_MAP.items()))
        
        return {
            'editoria': (editoria_key, editoria_label),
            'topico': topico,
            'formato': formato
        }


class RealEstateSynchronizer:
    """
    Gerencia as listas e opções exclusivas do MODO IMOBILIÁRIA.
    """
    def get_clusters_display(self):
        raw = GenesisConfig.ASSETS_CATALOG
        
        labels_map = {
            "FAMILY": "👨‍👩‍👧‍👦 Família (Casas/Condomínios)",
            "HIGH_END": "💎 Alto Padrão (Luxo)",
            "URBAN": "🏙️ Urbano (Aptos/Centro)",
            "INVESTOR": "📈 Investidor (Terrenos/Flips)",
            "LOGISTICS": "🚚 Logística/Industrial",
            "RURAL_LIFESTYLE": "🌿 Rural/Chácaras",
            "CORPORATE": "🏢 Corporativo/Salas"
        }
        
        display_list = []
        for k in raw.keys():
            label = labels_map.get(k, k.replace("_", " ").title())
            display_list.append((k, label))
        return display_list

    def get_valid_assets(self, cluster_key):
        return GenesisConfig.ASSETS_CATALOG.get(cluster_key, ["Imóvel Padrão"])

    def get_valid_topics(self, cluster_key):
        return list(GenesisConfig.TOPICS_MAP.items())

    def get_valid_formats(self, cluster_key):
        return list(GenesisConfig.REAL_ESTATE_FORMATS_MAP.items())

    def get_random_set(self):
        cluster_key = random.choice(list(GenesisConfig.ASSETS_CATALOG.keys()))
        assets = GenesisConfig.ASSETS_CATALOG[cluster_key]
        ativo = random.choice(assets)
        
        topico = random.choice(list(GenesisConfig.TOPICS_MAP.items()))
        formato = random.choice(list(GenesisConfig.REAL_ESTATE_FORMATS_MAP.items()))
        
        return {
            'cluster': (cluster_key, cluster_key),
            'ativo': ativo,
            'topico': topico,
            'formato': formato
        }
