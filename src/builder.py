# src/builder.py
import datetime
import re
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão Refatorada).
    Mapeamento direto (Chave-Valor) implementado. Dependência de substrings removida.
    Garante montagem estruturada e limpa dos prompts finais.
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
        # Substituição da lógica frágil baseada em substrings (ex: 'Resumo in editoria')
        # por mapeamento direto nas chaves da configuração
        if editoria_key == "DESTAQUE_DIARIO":
            return "## 5. ESTRUTURA: REVISTA DIGITAL DIÁRIA\n1. Manchete do Dia\n2. Notícia Principal (Longform)\n3. Giro Rápido (Sub-manchetes)\n4. Agenda Cultural\n5. Previsão do Tempo e Trânsito"
        
        structures = {
            "NOTICIA_IMPACTO": "## 5. ESTRUTURA: HARD NEWS COMPLETA\nLide, Corpo da Notícia, Contexto Histórico e Serviço.",
            "EXPLAINER": "## 5. ESTRUTURA: EXPLAINER\nContexto, Detalhes Técnicos e Impacto na Vida Real.",
            "DOSSIE_INVESTIGATIVO": "## 5. ESTRUTURA: DOSSIÊ\nProblema, Causas, Contraponto e Histórias Reais.",
            "CHECAGEM_FATOS": "## 5. ESTRUTURA: FACT-CHECKING\nOrigem do Boato, Investigação, Provas e Veredito.",
            "LISTA_CURADORIA": "## 5. ESTRUTURA: CURADORIA\nTop 5 Melhores, Endereços, Preços e Dica Secreta.",
            "SERVICO_PASSO_A_PASSO": "## 5. ESTRUTURA: TUTORIAL\nDocumentos, Prazos, Passo a Passo e Locais.",
            "ENTREVISTA_PING_PONG": "## 5. ESTRUTURA: ENTREVISTA\nPerfil, Perguntas Diretas e Respostas na Íntegra."
        }
        return structures.get(formato_key, structures["NOTICIA_IMPACTO"])

    def _get_real_estate_guidelines(self, formato_key, cluster, bairro):
        base = "## 5. ESTRUTURA: COPYWRITING IMOBILIÁRIO\nFoco em Storytelling, Valorização e Estilo de Vida."
        structures = {
            "LISTA_POLEMICA": base + "\n- Mitos vs Verdades.",
            "COMPARATIVO_TECNICO": base + "\n- Prós e Contras honestos."
        }
        return structures.get(formato_key, base)

    def _get_tone_guidelines(self, gatilho_key):
        if gatilho_key == "NEUTRAL_JOURNALISM":
            return "### 🧠 MENTALIDADE (JORNALISMO)\n- Imparcial, Profundo e Baseado em Fatos."
        
        return """### 🧠 MENTALIDADE (COPYWRITING HUMANIZADO)
- Persuasivo e Acolhedor.
- Use vocabulário que remeta a 'Lar' (ex: tranquilo, aconchego, refúgio, convivência).
- Evite termos técnicos frios em excesso; foque no benefício emocional do espaço.
- Fale como um consultor humano, não como um catálogo de vendas."""

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
## GENESIS MAGNETO V.71 — PORTAL NEWS (REFACTORED)
**Objetivo:** JORNALISMO DE PROFUNDIDADE (LONGFORM).
**Persona:** PORTAL DA CIDADE.
**Timestamp:** {data_mod} (Horário de Brasília)

## 1. A PAUTA
- **EDITORIA:** {editoria_display}
- **TEMA:** {tema_display}
- **LOCAL:** Indaiatuba (Cidade Inteira)
- **FORMATO:** {formato_display}

## 2. MISSÃO
Você é um repórter sênior. Escreva um texto denso e completo.
- **Busca:** Se for "Resumo do Dia", busque fatos reais de HOJE.
- **Estilo:** Parágrafos bem desenvolvidos. Nada de listas secas.

{structure}
{tone}

## 3. INSUMOS
**DIRETRIZ SUPREMA:**
1. IGNORAR persona de Vendas.
2. ENCARNAR JORNALISTA SÊNIOR.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1)
2. LIDE + CONTEÚDO
3. JSON-LD: Schema 'NewsArticle'
4. MARCADORES: {self._generate_seo_tags(d)}
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
## GENESIS MAGNETO V.71 — REAL ESTATE (REFACTORED)
**Objetivo:** Copywriting Imobiliário.
**Persona:** IMOBILIÁRIA SABER.
**Timestamp:** {data_mod} (Horário de Brasília)

## 1. O CENÁRIO
- **ATIVO:** {ativo}
- **LOCAL:** {bairro}
- **CLIENTE:** {d['persona']['nome']}
- **FORMATO:** {formato_display}
- **GATILHO:** {gatilho_display}

## 2. MISSÃO
Escreva um texto rico e persuasivo. Venda o sonho.
{structure}
{tone}

## 3. INSUMOS
**DIRETRIZ SUPREMA:**
1. IGNORAR persona de Jornalismo.
2. ENCARNAR CORRETOR ESPECIALISTA.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1)
2. CONTEÚDO
3. JSON-LD: Schema 'BlogPosting'
4. MARCADORES: {self._generate_seo_tags(d)}
""".strip()
