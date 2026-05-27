# src/logic.py
import random
from .config import GenesisConfig

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
    (Placeholder) Analisa tendências de busca para sugerir tópicos quentes.
    Mantido para compatibilidade arquitetural com engine.py.
    """
    pass

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
        # Leitura infalível a partir das constantes ativas
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
        """Retorna um pacote aleatório válido e testado para o Portal"""
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
        # Leitura infalível a partir das constantes ativas
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
        """Retorna um pacote aleatório válido e testado para Imobiliária"""
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
