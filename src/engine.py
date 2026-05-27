# src/engine.py
import random
import datetime
from .logic import PlanoDiretor, SEOHeatmap, RiscoJuridico, PortalSynchronizer, RealEstateSynchronizer
from .config import GenesisConfig

class GenesisEngine:
    """
    O 'Cérebro' (Versão 72 - Flow Control Refactored).
    Coordena a escolha inteligente dos parâmetros da pauta.
    Bug de sobrescrita corrigido: a Persona agora se curva ao Ativo escolhido pelo usuário.
    Garante o isolamento absoluto entre Portal (Jornalismo) e Imobiliária (Comercial).
    """
    
    def __init__(self, data_manager):
        self.data = data_manager
        self.plano_diretor = PlanoDiretor()
        self.seo_bot = SEOHeatmap()
        self.juridico = RiscoJuridico()
        self.portal_sync = PortalSynchronizer()
        self.imob_sync = RealEstateSynchronizer()

    def run(self, user_inputs):
        """
        Executa o pipeline de decisão com respeito absoluto às escolhas humanas.
        """
        # 1. MODO DE OPERAÇÃO
        modo = user_inputs.get('tipo_pauta', 'IMOBILIARIA')
        eh_portal = (modo == "PORTAL")

        # 2. RESOLUÇÃO DE CONFLITO: Input do Usuário vs Persona
        # A escolha humana de um ativo específico NUNCA deve ser descartada.
        sub_ativo_input = user_inputs.get('sub_ativo', 'ALEATÓRIO')
        persona_key = user_inputs.get('persona_key', 'ALEATÓRIO')
        
        cluster_forcado = None
        if not eh_portal and sub_ativo_input != 'ALEATÓRIO':
            # Rastreia a qual categoria (cluster) o imóvel exigido pertence
            for c_key, ativos in GenesisConfig.ASSETS_CATALOG.items():
                if sub_ativo_input in ativos:
                    cluster_forcado = c_key
                    break

        # 3. SELEÇÃO DE PERSONA INTELIGENTE
        if persona_key == "ALEATÓRIO" or not persona_key:
            if eh_portal:
                persona_key = "CITIZEN_GENERAL" # Persona exclusiva do Portal
            else:
                if cluster_forcado:
                    # Adapta as opções de persona para combinar com o imóvel exigido pelo usuário
                    opcoes = [k for k, v in GenesisConfig.PERSONAS.items() if v.get('cluster_ref') == cluster_forcado and k != "CITIZEN_GENERAL"]
                    if not opcoes: # Fallback de segurança
                        opcoes = [k for k in GenesisConfig.PERSONAS.keys() if k != "CITIZEN_GENERAL"]
                    persona_key = random.choice(opcoes)
                else:
                    opcoes = [k for k in GenesisConfig.PERSONAS.keys() if k != "CITIZEN_GENERAL"]
                    persona_key = random.choice(opcoes)

        # Resgata o objeto completo da Persona escolhida
        persona_obj = GenesisConfig.PERSONAS.get(persona_key, GenesisConfig.PERSONAS["CITIZEN_GENERAL" if eh_portal else "FIRST_HOME_DREAMER"])

        # 4. SELEÇÃO DE BAIRRO
        bairro_nome = user_inputs.get('bairro_nome', 'ALEATÓRIO')
        
        if bairro_nome == "ALEATÓRIO":
            bairro_obj = random.choice(self.data.bairros)
        elif bairro_nome == "FORCE_CITY_MODE":
            bairro_obj = {"nome": "Indaiatuba", "zona_normalizada": "urbana", "slug": "indaiatuba"}
        else:
            bairro_obj = next((b for b in self.data.bairros if b['nome'] == bairro_nome), None)
            if not bairro_obj:
                bairro_obj = {"nome": "Indaiatuba", "zona_normalizada": "urbana", "slug": "indaiatuba"}

        # 5. DEFINIÇÃO DE CONTEÚDO (Isolamento de Domínios)
        if eh_portal:
            result_content = self._decide_portal_content(user_inputs)
        else:
            result_content = self._decide_real_estate_content(user_inputs, persona_obj, bairro_obj, cluster_forcado)

        # 6. MONTAGEM DO PACOTE FINAL
        final_package = {
            "tipo_pauta": modo,
            "persona": persona_obj,
            "bairro": bairro_obj,
            "ativo_definido": result_content['ativo'], 
            "topico": result_content['topico'],
            "formato": result_content['formato'],
            "gatilho": user_inputs.get('gatilho', 'ALEATÓRIO'),
            "inputs_originais": user_inputs 
        }

        # Ajuste final de gatilho para preencher lacunas baseadas no modo
        if final_package['gatilho'] == 'ALEATÓRIO':
            if eh_portal:
                 final_package['gatilho'] = "NEUTRAL_JOURNALISM"
            else:
                 final_package['gatilho'] = random.choice(list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.keys()))

        return final_package

    def _decide_portal_content(self, inputs):
        """Lógica Isolada Estrita para o PORTAL DA CIDADE."""
        editoria_input = inputs.get('ativo', 'ALEATÓRIO')
        
        if editoria_input != 'ALEATÓRIO' and editoria_input in GenesisConfig.PORTAL_CATALOG:
            editoria_key = editoria_input
        else:
            editoria_key = random.choice(list(GenesisConfig.PORTAL_CATALOG.keys()))
            
        lista_itens = GenesisConfig.PORTAL_CATALOG[editoria_key]
        if lista_itens:
            ativo_final = random.choice(lista_itens)
        else:
            ativo_final = editoria_key

        topico_input = inputs.get('topico', 'ALEATÓRIO')
        if topico_input != 'ALEATÓRIO' and topico_input in GenesisConfig.PORTAL_TOPICS_MAP:
            topico_final = topico_input
        else:
            topico_final = random.choice(list(GenesisConfig.PORTAL_TOPICS_MAP.keys()))

        formato_input = inputs.get('formato', 'ALEATÓRIO')
        if formato_input != 'ALEATÓRIO' and formato_input in GenesisConfig.PORTAL_FORMATS_MAP:
            formato_final = formato_input
        else:
            if topico_final == "GIRO_NOTICIAS":
                formato_final = "NOTICIA_IMPACTO"
            elif topico_final == "SERVICO_ESSENCIAL":
                formato_final = "SERVICO_PASSO_A_PASSO"
            else:
                formato_final = random.choice(list(GenesisConfig.PORTAL_FORMATS_MAP.keys()))

        return {
            "ativo": ativo_final,
            "topico": topico_final,
            "formato": formato_final
        }

    def _decide_real_estate_content(self, inputs, persona, bairro, cluster_forcado=None):
        """Lógica Isolada Estrita para IMOBILIÁRIA."""
        sub_ativo_input = inputs.get('sub_ativo', 'ALEATÓRIO')
        cluster_input = inputs.get('ativo', 'ALEATÓRIO')

        # Prioridade 1: O usuário escolheu um ativo (imóvel) específico
        if sub_ativo_input != 'ALEATÓRIO' and cluster_forcado:
            cluster_escolhido = cluster_forcado
            ativo_base = sub_ativo_input
        
        # Prioridade 2: O usuário escolheu uma categoria (cluster) macro
        elif cluster_input != 'ALEATÓRIO' and cluster_input in GenesisConfig.ASSETS_CATALOG:
            cluster_escolhido = cluster_input
            ativo_base = random.choice(GenesisConfig.ASSETS_CATALOG[cluster_escolhido])
        
        # Prioridade 3: Adaptação Orgânica baseada na Persona
        else:
            pref = persona.get('cluster_ref')
            if pref and pref in GenesisConfig.ASSETS_CATALOG and random.random() > 0.3:
                cluster_escolhido = pref
            else:
                cluster_escolhido = random.choice(list(GenesisConfig.ASSETS_CATALOG.keys()))
            ativo_base = random.choice(GenesisConfig.ASSETS_CATALOG[cluster_escolhido])

        # O Plano Diretor faz a auditoria final, barrando anomalias geográficas
        ativo_final, _ = self.plano_diretor.refinar_ativo(cluster_escolhido, bairro, [ativo_base])

        topico_input = inputs.get('topico', 'ALEATÓRIO')
        if topico_input != 'ALEATÓRIO' and topico_input in GenesisConfig.TOPICS_MAP:
            topico_final = topico_input
        else:
            topico_final = random.choice(list(GenesisConfig.TOPICS_MAP.keys()))

        formato_input = inputs.get('formato', 'ALEATÓRIO')
        if formato_input != 'ALEATÓRIO' and formato_input in GenesisConfig.REAL_ESTATE_FORMATS_MAP:
            formato_final = formato_input
        else:
            formato_final = random.choice(list(GenesisConfig.REAL_ESTATE_FORMATS_MAP.keys()))

        return {
            "ativo": ativo_final,
            "topico": topico_final,
            "formato": formato_final,
            "cluster_tecnico": cluster_escolhido
        }
