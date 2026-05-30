# src/builder.py
import datetime
import re
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão Refatorada e Blindada contra IA Preguiçosa).
    Mapeamento direto (Chave-Valor) implementado. Dependência de substrings removida.
    Força a IA a agir em capacidade máxima de pesquisa.
    """

    CTA_CAPTURE_CODE = """
<div style="text-align:center; margin: 40px 0;">
<script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script>
</div>
"""

    def __init__(self):
        pass

    def _format_date_blogger(self, iso_date_str):
        try:
            if isinstance(iso_date_str, datetime.datetime): 
                dt = iso_date_str
            else: 
                dt = datetime.datetime.strptime(iso_date_str.split("T")[0], "%Y-%m-%d")
            meses = {1:"jan.", 2:"fev.", 3:"mar.", 4:"abr.", 5:"mai.", 6:"jun.", 7:"jul.", 8:"ago.", 9:"set.", 10:"out.", 11:"nov.", 12:"dez."}
            return f"{dt.day} de {meses[dt.month]} de {dt.year}"
        except: 
            return iso_date_str

    def _humanize_key(self, key):
        if not key: return ""
        return key.replace("_", " ").title()

    def _get_display_value(self, key):
        if key in GenesisConfig.CONTENT_FORMATS_MAP:
            return GenesisConfig.CONTENT_FORMATS_MAP[key]
        if key in GenesisConfig.TOPICS_MAP:
            return GenesisConfig.TOPICS_MAP[key]
        if key in GenesisConfig.PORTAL_TOPICS_MAP:
            return GenesisConfig.PORTAL_TOPICS_MAP[key]
        return self._humanize_key(key)

    def _generate_seo_tags(self, d):
        if d.get('tipo_pauta') == "PORTAL":
            tags = ["Indaiatuba", "Notícias Indaiatuba", "Portal da Cidade", "Giro de Notícias"]
        else:
            tags = ["Indaiatuba", "Imóveis Indaiatuba", "Mercado Imobiliário", "Morar em Indaiatuba"]

        if d.get('bairro') and d['bairro']['nome'] != "Indaiatuba":
            tags.append(d['bairro']['nome'])
        
        raw_ativo = d.get('ativo_definido', '')
        ativo_limpo = raw_ativo.split('(')[0].strip()
        if "_" in ativo_limpo and ativo_limpo.isupper():
            ativo_limpo = self._humanize_key(ativo_limpo)
        if ativo_limpo: tags.append(ativo_limpo)
        
        raw_topico = d.get('topico', '')
        if raw_topico:
            if "_" in raw_topico and raw_topico.isupper():
                tags.append(self._humanize_key(raw_topico))
            else:
                clean_text = re.sub(r'[^\w\s,]', '', raw_topico).strip()
                tags.append(clean_text)
        
        seen = set()
        final_tags = [x for x in tags if not (x in seen or seen.add(x))]
        return ", ".join(final_tags[:12])

    def _get_portal_structure(self, formato_key, editoria_key, tema_key):
        if editoria_key == "DESTAQUE_DIARIO":
            return "## 5. ESTRUTURA: REVISTA DIGITAL DIÁRIA\n1. Manchete do Dia\n2. Notícia Principal (Longform)\n3. Giro Rápido (Sub-manchetes)\n4. Agenda Cultural\n5. Previsão do Tempo"
        
        structures = {
            "NOTICIA_IMPACTO": "## 5. ESTRUTURA: HARD NEWS COMPLETA\nLide (Quem, Quando, Onde, O que), Corpo da Notícia, Contexto Histórico e Serviço.",
            "COBERTURA_CONTINUA": "## 5. ESTRUTURA: FOLLOW-UP\nResumo do que se sabe até agora, Novos desdobramentos, Impacto imediato e Próximos passos.",
            "EXPLAINER": "## 5. ESTRUTURA: EXPLAINER\nPergunta central, Contexto prático, Detalhes técnicos traduzidos, Impacto no dia a dia da população.",
            "DOSSIE_INVESTIGATIVO": "## 5. ESTRUTURA: DOSSIÊ LONGFORM\nContexto do Problema, Linha do Tempo, Dados e Provas, Contraponto/Culpados e Vítimas/Histórias Reais.",
            "DATA_STORYTELLING": "## 5. ESTRUTURA: JORNALISMO DE DADOS\nApresentação do dado mais chocante, Evolução histórica, O que o número significa na prática, Projeção futura.",
            "CHECAGEM_FATOS": "## 5. ESTRUTURA: FACT-CHECKING\nOrigem do Boato (O que estão dizendo), A Investigação (O que descobrimos), Provas, Veredito Oficial.",
            "SERVICO_PASSO_A_PASSO": "## 5. ESTRUTURA: GUIA DE UTILIDADE\nO que é o serviço, Quem tem direito, Documentos necessários, Passo a passo prático, Prazos e Onde resolver.",
            "LISTA_CURADORIA": "## 5. ESTRUTURA: LISTICLE\nIntrodução temática, Os Itens da lista com justificativa (Top 3 a 10), Dica Secreta da redação e Conclusão.",
            "REVIEW_ANALISE": "## 5. ESTRUTURA: REVIEW LOCAL\nContexto da visita/teste, Pontos Fortes, Pontos Fracos, Preços/Custo-Benefício, Veredito Final.",
            "ENTREVISTA_PING_PONG": "## 5. ESTRUTURA: ENTREVISTA\nMini-perfil do entrevistado, Perguntas curtas e provocativas e Respostas na íntegra.",
            "PERFIL_BIOGRAFICO": "## 5. ESTRUTURA: PERFIL (STORYTELLING)\nInício no clímax da vida da pessoa, Retrospecto/Origem, As grandes lutas, A situação atual e Legado.",
            "EDITORIAL_OPINIAO": "## 5. ESTRUTURA: OPINIÃO OFICIAL\nPosicionamento claro no primeiro parágrafo, Argumento principal suportado por fatos, Refutação ao lado contrário, Chamada à ação.",
            "ANTES_E_DEPOIS": "## 5. ESTRUTURA: MEMÓRIA DA CIDADE\nComo era (Contexto da época), O estopim da mudança, O processo de transformação, Como está hoje e o impacto na cidade."
        }
        return structures.get(formato_key, structures["NOTICIA_IMPACTO"])

    def _get_real_estate_guidelines(self, formato_key, cluster, bairro):
        base = "## 5. ESTRUTURA: COPYWRITING IMOBILIÁRIO\nFoco em Storytelling, Valorização e Estilo de Vida."
        
        structures = {
            "GUIA_BAIRRO": base + "\n- História da região, Infraestrutura (saúde/educação), Perfil dos moradores, Potencial de valorização e Principais atrativos.",
            "LISTICLE_CURADORIA": base + "\n- Introdução magnética, Lista curada detalhando características de cada item, Vantagem exclusiva de cada um e Chamada à ação direta.",
            "MITOS_VERDADES": base + "\n- Apresente objeções comuns do mercado e destrua cada mito com fatos técnicos e dados reais.",
            "GLOSSARIO_TERMOS": base + "\n- Explicação hiper-didática em formato de verbetes ou tópicos. Seja claro para que um leigo entenda, mas técnico para manter autoridade.",
            "GUIA_PASSO_A_PASSO": base + "\n- Um mapa numerado (Fase 1, Fase 2, etc.). Liste armadilhas e atalhos de mercado. Crie um tom didático e acolhedor.",
            "COMPARATIVO_DIRETO": base + "\n- Divida a estrutura em: Critério 1, Critério 2, Prós de A, Prós de B, Contras de A, Contras de B e um 'Veredito do Especialista' no fim.",
            "ERROS_FATAIS": base + "\n- Tom de alerta profundo. Liste problemas técnicos (jurídicos, de vistoria, escolha de planta) e mostre como sua imobiliária blinda o cliente contra eles.",
            "CENARIO_ANALITICO": base + "\n- Comece com números duros. Explique tendências macro, depois desça para a rua/bairro. Termine com uma previsão de valorização.",
            "ENTREVISTA_ESPECIALISTA": base + "\n- Simule uma conversa franca com um engenheiro ou jurista da área imobiliária. Foco na segurança da transação.",
            "ESTUDO_DE_CASO": base + "\n- Estrutura PAS (Problema, Agitação, Solução). Mostre o drama inicial do cliente fictício e como a Inteligência e curadoria da sua Imobiliária resolveu.",
            "ANALISE_ROI": base + "\n- Foco em números. Rentabilidade de aluguel (Yield), Potencial de revenda (Flip), Crescimento do Plano Diretor e liquidez.",
            "INSIGHT_DE_CORRETOR": base + "\n- Texto em primeira pessoa, persuasivo, mostrando que o cliente está diante de uma assimetria de mercado absurda que os leigos não veem.",
            "CHECKLIST_TECNICO": base + "\n- Foco em utilidade prática. Checklist marcável (bullets), apontando detalhes elétricos, estruturais, solares e acústicos a serem observados."
        }
        return structures.get(formato_key, base)

    def _get_tone_guidelines(self, gatilho_key):
        if gatilho_key == "NEUTRAL_JOURNALISM":
            return "### 🧠 MENTALIDADE (JORNALISMO)\n- Imparcial, Profundo e Baseado em Fatos Verídicos Pesquisados."
        
        return "### 🧠 MENTALIDADE (COPYWRITING HUMANIZADO)\n- Persuasivo e Acolhedor, mas embasado em DADOS REAIS da sua pesquisa.\n- Use vocabulário que remeta a 'Lar' (ex: tranquilo, aconchego, refúgio, convivência).\n- Evite clichês genéricos; foque no benefício emocional do espaço com provas geográficas.\n- Fale como um consultor humano hyper-local, não como um robô."

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        formato_key = d.get('formato', 'NOTICIA_IMPACTO')
        formato_display = self._get_display_value(formato_key)
        editoria_key = d.get('ativo_definido', 'Geral')
        editoria_display = self._humanize_key(editoria_key) if ("_" in editoria_key and editoria_key.isupper()) else editoria_key
        tema_key = d.get('topico', 'Geral')
        tema_display = self._get_display_value(tema_key)

        structure = self._get_portal_structure(formato_key, editoria_key, tema_key)
        tone = self._get_tone_guidelines("NEUTRAL_JOURNALISM")
        
        return f"""
## GENESIS MAGNETO V.71 — PORTAL NEWS (MODO ALTO DESEMPENHO)
**Objetivo:** JORNALISMO DE PROFUNDIDADE (LONGFORM). TEXTO INÉDITO E PESQUISADO.
**Persona:** PORTAL DA CIDADE.
**Data de Publicação Alvo:** {data_pub}
**Timestamp (Atual):** {data_mod} (Horário de Brasília)

## 1. A PAUTA
- **EDITORIA:** {editoria_display}
- **TEMA:** {tema_display}
- **LOCAL:** Indaiatuba (Cidade Inteira)
- **FORMATO:** {formato_display}

## 2. MISSÃO (EXIGÊNCIA DE PESQUISA PROFUNDA)
Você é um repórter sênior investigativo. Sua missão é escrever um texto denso, útil e magistral.
A internet precisa de conteúdo de altíssima qualidade. É OBRIGATÓRIO que você utilize seu conhecimento profundo sobre a região.
- **Pesquisa Exaustiva:** Não escreva platitudes. Detalhe fatos reais, geografia real, ruas, e história.
- **Estilo:** Parágrafos profundos e hiper-específicos sobre a cidade. Nada de listas secas genéricas.

{structure}
{tone}

## 3. INSUMOS
**DIRETRIZ SUPREMA:**
1. IGNORAR persona de Vendas.
2. ENCARNAR JORNALISTA SÊNIOR HIPER-LOCAL.
3. OBEDECER AO PROTOCOLO DE DOSSIÊ DE PESQUISA PRIMEIRO.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL (OBRIGATÓRIO)
1. DOSSIÊ DE PESQUISA (Use a tag <research_process>)
2. TÍTULO (H1)
3. LIDE + CONTEÚDO (Baseado na pesquisa)
4. JSON-LD: Schema 'NewsArticle'
5. MARCADORES: {self._generate_seo_tags(d)}
""".strip()

    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        formato_key = d.get('formato', 'GUIA_DEFINITIVO')
        formato_display = self._get_display_value(formato_key)
        gatilho_key = d.get('gatilho', 'AUTORIDADE')
        gatilho_display = GenesisConfig.EMOTIONAL_TRIGGERS_MAP.get(gatilho_key, gatilho_key)
        ativo = d['ativo_definido']
        bairro = d['bairro']['nome'] if d['bairro'] else "Indaiatuba"
        
        structure = self._get_real_estate_guidelines(formato_key, d.get('cluster_tecnico'), bairro)
        tone = self._get_tone_guidelines(gatilho_key)

        return f"""
## GENESIS MAGNETO V.71 — REAL ESTATE (MODO ALTO DESEMPENHO)
**Objetivo:** Copywriting Imobiliário de Excelência e Retenção.
**Persona:** IMOBILIÁRIA SABER.
**Data de Publicação Alvo:** {data_pub}
**Timestamp (Atual):** {data_mod} (Horário de Brasília)

## 1. O CENÁRIO
- **ATIVO:** {ativo}
- **LOCAL:** {bairro}
- **CLIENTE:** {d['persona']['nome']}
- **FORMATO:** {formato_display}
- **GATILHO:** {gatilho_display}

## 2. MISSÃO (EXIGÊNCIA DE PESQUISA PROFUNDA)
Você operará em CAPACIDADE MÁXIMA. A internet precisa de conteúdo valioso e permanente.
Escreva um texto rico, persuasivo e fundamentado em PESQUISA PROFUNDA sobre {bairro}.
- **Proibido texto genérico:** Venda o sonho usando fatos geográficos reais, citando ruas reais, pontos de referência exatos, parques e dados locais.
- **Proibido clichês de vendedor:** Atue como um consultor sênior hiper-especializado no bairro.

{structure}
{tone}

## 3. INSUMOS
**DIRETRIZ SUPREMA:**
1. IGNORAR persona de Jornalismo.
2. ENCARNAR CORRETOR ESPECIALISTA HIPER-LOCAL.
3. OBEDECER AO PROTOCOLO DE DOSSIÊ DE PESQUISA PRIMEIRO.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL (OBRIGATÓRIO)
1. DOSSIÊ DE PESQUISA (Use a tag <research_process>)
2. TÍTULO (H1)
3. CONTEÚDO (Baseado estritamente na pesquisa acima)
4. JSON-LD: Schema 'BlogPosting'
5. MARCADORES: {self._generate_seo_tags(d)}
""".strip()
