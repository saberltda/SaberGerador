"""
Módulo responsável pela construção de prompts avançados de SEO e geração de posts Markdown.
Alinhado com as especificações do Saber Prompt Studio v5.0.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import unicodedata
import re

@dataclass
class PautaContext:
    title: str
    bairro: str
    category: str
    vias: str
    dor: str
    crenca: str
    mecanica: str
    limite: str
    insight: str
    kw_primary: str
    kw_secondary: str
    tags: List[str] = field(default_factory=list)
    angulo_key: str = "analise-critica"
    intent_key: str = "informational"
    depth_key: str = "padrao"
    tom_key: str = "analista"
    localismo_key: str = "alto"

ANGULOS = {
    "analise-critica": {
        "label": "Análise Crítica / Desmontagem",
        "instrucao": "Desmonte a crença comum com evidências de campo, mecânica urbana e consequências reais na rotina. Tom analítico, sem condescendência."
    },
    "protocolo-campo": {
        "label": "Protocolo de Campo / Checklist",
        "instrucao": "Estruture o artigo como um protocolo prático de visita e decisão. Inclua perguntas específicas, medições simples e sinais de alerta que o leitor pode aplicar sozinho."
    },
    "comparativo": {
        "label": "Comparativo Local",
        "instrucao": "Compare implicitamente ou explicitamente este bairro/tema com 1–2 alternativas reais de Indaiatuba (sem ranking genérico). Mostre trade-offs concretos."
    },
    "custo-oculto": {
        "label": "Custo Oculto & CAPEX",
        "instrucao": "Foque em dinheiro, tempo e risco financeiro. Quantifique ordens de grandeza quando possível (sem inventar números precisos) e ensine como o leitor valida os custos."
    },
    "rotina-real": {
        "label": "Rotina Real do Morador",
        "instrucao": "Conte a história a partir da rotina semanal/mensal de quem já mora ou vai morar. Use horários, deslocamentos, tarefas de manutenção e momentos de atrito."
    },
    "mito-vs-fato": {
        "label": "Mito vs. Fato Urbano",
        "instrucao": "Estruture em blocos claros de mito → realidade local → o que fazer na prática. Linguagem direta e memorável."
    },
    "decisao-familia": {
        "label": "Decisão Familiar / Longo Prazo",
        "instrucao": "Enquadre a decisão sob a ótica de 5–15 anos: filhos, envelhecimento, mudança de rotina, liquidez futura e custo emocional."
    },
    "vistoria-tecnica": {
        "label": "Vistoria Técnica Profunda",
        "instrucao": "Escreva como um engenheiro/arquiteto que ensina o leitor a enxergar o que o corretor não mostra. Detalhe pontos de inspeção, perguntas ao vendedor e documentos a pedir."
    }
}

INTENTS = {
    "informational": "O leitor quer entender o tema com profundidade antes de qualquer decisão de compra. Priorize clareza, exemplos locais e autoridade.",
    "commercial": "O leitor está comparando opções e avaliando prós/contras. Ajude-o a eliminar opções ruins e a fazer perguntas melhores.",
    "transactional": "O leitor está perto de decidir. Entregue critérios claros de “sim / não / só se…” e um protocolo de validação final.",
    "navigational-local": "O leitor busca informação hiperlocal (“em [bairro]”, “perto de…”). Maximize referências a vias, dinâmicas e sinais de campo reais."
}

DEPTHS = {
    "padrao": {"palavras": "900 a 1.200", "instrucao": "Texto denso e completo, sem enrolação. Cada parágrafo deve carregar informação nova."},
    "denso": {"palavras": "1.300 a 1.700", "instrucao": "Análise profunda com mais exemplos de campo, nuances e um checklist mais completo. Ainda assim, zero filler."},
    "pillar": {"palavras": "1.800 a 2.400", "instrucao": "Artigo pillar definitivo. Cubra o tema de forma abrangente, com seções bem demarcadas, FAQ implícito e valor de referência por anos."},
    "rapido": {"palavras": "700 a 900", "instrucao": "Cirúrgico e direto. Máxima densidade informativa por parágrafo. Ideal para intenção comercial rápida."}
}

TONS = {
    "analista": "Tom de analista urbano independente (estilo guia Michelin + análise de mercado honesta). Frases precisas, sem hype.",
    "mentor": "Tom de mentor pragmático (REI / HubSpot method). Direto, útil, com “faça isso / evite aquilo”.",
    "investigativo": "Tom de jornalista investigativo local. Revela o que não está no anúncio, com evidências de campo.",
    "tecnico": "Tom de engenheiro/arquiteto técnico. Precisão de linguagem, foco em desempenho, normas e diagnóstico.",
    "familia": "Tom de consultor de família e rotina. Empático, mas realista; fala de tempo, energia e qualidade de vida de longo prazo."
}

LOCALISMOS = {
    "alto": "Cite vias reais, microclima, dinâmicas de tráfego, horários de pico e sinais de campo específicos do bairro. O leitor deve sentir que o texto só poderia ter sido escrito por quem conhece Indaiatuba de perto.",
    "medio": "Mencione o bairro, 1–2 eixos principais e características urbanas relevantes. Evite excesso de nomes de rua se não agregarem.",
    "contextual": "Mantenha o foco em Indaiatuba como cidade, usando o bairro como exemplo principal sem hiperlocalismo excessivo."
}


def slugify(text: str, max_length: int = 72) -> str:
    """Gera slug em kebab-case limpo para arquivos .md."""
    if not text:
        return "post-saber"
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).lower().strip()
    text = re.sub(r"[\s-]+", "-", text)
    return text[:max_length].rstrip("-")


class PromptBuilder:
    """Montador do prompt completo para LLMs com os padrões de SEO v5."""

    @staticmethod
    def build_prompt(ctx: PautaContext) -> str:
        angulo = ANGULOS.get(ctx.angulo_key, ANGULOS["analise-critica"])
        intent = INTENTS.get(ctx.intent_key, INTENTS["informational"])
        depth = DEPTHS.get(ctx.depth_key, DEPTHS["padrao"])
        tom = TONS.get(ctx.tom_key, TONS["analista"])
        localismo = LOCALISMOS.get(ctx.localismo_key, LOCALISMOS["alto"])
        kebab = slugify(ctx.title)
        tags_str = ", ".join(ctx.tags) if ctx.tags else ctx.category

        nl = "\n"

        prompt = (
            f"# SYSTEM: VOCÊ É O EDITOR-CHEFE DO BLOG DA IMOBILIÁRIA SABER (INDAIATUBA){nl}"
            f"Sua única missão nesta tarefa é redigir UM artigo inédito, de altíssimo valor prático e SEO, sobre moradia e decisão de compra em Indaiatuba-SP. O texto deve ser publicável imediatamente no blog Astro (AstroWind / content collection) como arquivo .md.{nl}{nl}"
            f"Você opera com o princípio **\"Vender sem vender\"**: autoridade geográfica real + utilidade cirúrgica + honestidade radical. O leitor deve terminar o artigo mais preparado para decidir (ou para não comprar) do que qualquer visita a estande.{nl}{nl}"
            f"---{nl}"
            f"## 1. DIRETRIZES FUNDAMENTAIS (NÃO NEGOCIÁVEIS){nl}{nl}"
            f"### Tom e Persona{nl}"
            f"- {tom}{nl}"
            f"- Você NÃO é corretor de estande, copywriter de lançamento nem influencer de \"vida no interior\".{nl}"
            f"- Você é a pessoa que o leitor gostaria de ter ao lado na vistoria: experiente, direta e sem conflito de interesse aparente.{nl}{nl}"
            f"### Proibições Absolutas de Linguagem{nl}"
            f"É PROIBIDO usar (ou paráfrases óbvias de):{nl}"
            f"\"refúgio definitivo\", \"porto seguro\", \"jogada de mestre\", \"sweet spot\", \"blindagem patrimonial\", \"elite paulistana\", \"deslumbrante\", \"espetacular\", \"venha realizar o sonho\", \"oportunidade única\", \"não perca\", \"exclusivo\", \"alto padrão incomparável\", \"qualidade de vida inigualável\", \"o melhor bairro de Indaiatuba\".{nl}"
            f"Também é proibido: listas de adjetivos vazios, CTAs agressivos de venda, depoimentos inventados e qualquer forma de hype imobiliário.{nl}{nl}"
            f"### Anti-Alucinação e Honestidade de Dados{nl}"
            f"- NÃO invente percentuais de valorização, preços médios, rankings, \"dados de mercado\" ou depoimentos.{nl}"
            f"- Se um número ou fato não puder ser verificado pelo leitor (cartório, prefeitura, visita de campo, concessionária), ensine COMO checar em vez de afirmar.{nl}"
            f"- Prefira ordens de grandeza honestas (\"costuma custar várias vezes mais\", \"na prática leva 30–50 minutos\") a cifras falsamente precisas.{nl}{nl}"
            f"### SEO & Qualidade Editorial (padrão mundial){nl}"
            f"- Escreva para humanos primeiro. O Google recompensa experiência, expertise, autoridade e confiança (E-E-A-T) + utilidade real.{nl}"
            f"- Intenção de busca prioritária desta pauta: **{ctx.intent_key}**. {intent}{nl}"
            f"- Palavra-chave primária a ser trabalhada de forma natural: **\"{ctx.kw_primary}\"**.{nl}"
            f"- Keywords e entidades secundárias (LSI / semantic): {ctx.kw_secondary or tags_str}.{nl}"
            f"- Varie estruturas de frase e aberturas de parágrafo. Evite padrões sintáticos repetitivos de IA.{nl}"
            f"- Use linguagem concreta, sensorial e local (horários, vias, sensações térmicas, sons, tempos de deslocamento).{nl}"
            f"- Inclua pelo menos uma seção que responda diretamente a uma pergunta que o leitor digitaria no Google.{nl}"
            f"- Nível de localismo exigido: {localismo}{nl}{nl}"
            f"### Formato Técnico do Blog{nl}"
            f"- Sem H1 no corpo do artigo (o AstroWind já renderiza o title do frontmatter como H1).{nl}"
            f"- Inicie o corpo em parágrafo de abertura forte ou em <h2>.{nl}"
            f"- Sem citações formais estilo acadêmico (CITE).{nl}"
            f"- Extensão alvo: **{depth['palavras']} palavras** de análise útil. {depth['instrucao']}{nl}"
            f"- Termine o artigo EXATAMENTE com o script ConvertKit (não altere o código):{nl}"
            f"<script async data-uid=\"d188d73e78\" src=\"https://sabernovidades.kit.com/d188d73e78/index.js\"></script>{nl}{nl}"
            f"---{nl}"
            f"## 2. BRIEFING DA PAUTA (FONTE DA VERDADE){nl}{nl}"
            f"• **Título proposto:** {ctx.title}{nl}"
            f"• **Bairro / Região:** {ctx.bairro} (Indaiatuba – SP){nl}"
            f"• **Categoria editorial:** {ctx.category}{nl}"
            f"• **Vias e eixos reais:** {ctx.vias}{nl}"
            f"• **Dor / ponto cego do comprador:** {ctx.dor}{nl}"
            f"• **Crença de mercado a desarmar:** {ctx.crenca}{nl}"
            f"• **Mecânica urbana, solo e clima:** {ctx.mecanica}{nl}"
            f"• **Contraindicação honesta:** {ctx.limite}{nl}"
            f"• **Insight único / ângulo diferencial (obrigatório usar):** {ctx.insight}{nl}"
            f"• **Ângulo editorial desta geração:** {angulo['label']} — {angulo['instrucao']}{nl}"
            f"• **Tags para frontmatter:** {tags_str}{nl}{nl}"
            f"---{nl}"
            f"## 3. ESTRUTURA OBRIGATÓRIA DO ARTIGO (.md){nl}{nl}"
            f"### 3.1 Frontmatter YAML (completo e válido){nl}"
            f"```yaml{nl}"
            f"---{nl}"
            f"title: \"{ctx.title}\"{nl}"
            f"excerpt: \"1–2 frases sem hype, até 160 caracteres, que façam o leitor querer continuar\"{nl}"
            f"description: \"Meta description objetiva para SEO local, até 160 caracteres, com a keyword primária de forma natural\"{nl}"
            f"category: \"{ctx.category}\"{nl}"
            f"tags:{nl}"
        )

        for tag in (ctx.tags if ctx.tags else [ctx.category]):
            prompt += f"  - {tag.strip()}{nl}"

        prompt += (
            f"---{nl}"
            f"```{nl}{nl}"
            f"### 3.2 Corpo do Artigo (ordem recomendada){nl}"
            f"1. **Abertura de vida concreta** — Comece com tempo, ruído, insolação, deslocamento, custo ou estresse real. Nada de definição de dicionário.{nl}"
            f"2. **A crença que falha** — Enuncie a crença comum e mostre por que ela desaba na rotina de Indaiatuba / deste bairro.{nl}"
            f"3. **A mecânica real** — Solo, relevo, vias, ventos, horários, infraestrutura. Cite as vias e dinâmicas do briefing.{nl}"
            f"4. **O insight diferencial** — Desenvolva o insight único fornecido. É o que torna este artigo impossível de ser genérico.{nl}"
            f"5. **Limite honesto** — \"Isso NÃO serve se…\". Seja específico e útil.{nl}"
            f"6. **Protocolo / Checklist de campo** — Perguntas e verificações que o leitor pode levar na próxima visita (mínimo 5–7 itens acionáveis).{nl}"
            f"7. **Consequência patrimonial sutil** — Como a escolha correta de planta, orientação, bairro ou tipologia protege tempo, dinheiro e liquidez — sem forçar venda.{nl}"
            f"8. **Fecho memorável** — Uma frase curta, precisa e humana + o script ConvertKit.{nl}{nl}"
            f"### 3.3 Qualidade de Escrita Exigida{nl}"
            f"- Cada seção deve adicionar informação nova. Corte qualquer parágrafo que só \"embelezaria\".{nl}"
            f"- Prefira substantivos e verbos concretos a adjetivos.{nl}"
            f"- Varie o ritmo: frases curtas para impacto + períodos um pouco mais longos para análise.{nl}"
            f"- O texto deve parecer escrito por alguém que já andou nas vias citadas, não por modelo de linguagem genérico.{nl}{nl}"
            f"---{nl}"
            f"## 4. FORMATO DE ENTREGA ESPERADO{nl}{nl}"
            f"Entregue nesta ordem:{nl}"
            f"1. **Nome do arquivo** em kebab-case limpo: `{kebab}.md`{nl}"
            f"2. **O bloco Markdown completo** (frontmatter + corpo), pronto para ser salvo em `src/data/post/` do blog Astro.{nl}{nl}"
            f"Não inclua explicações meta sobre o que você vai fazer. Vá direto ao artigo.{nl}{nl}"
            f"Gere agora o artigo completo com máxima profundidade analítica, localismo real e utilidade prática:"
        )

        return prompt

    @staticmethod
    def build_yaml_only(ctx: PautaContext) -> str:
        """Gera apenas o bloco de frontmatter YAML."""
        nl = "\n"
        out = f"---{nl}title: \"{ctx.title}\"{nl}excerpt: \"\"{nl}description: \"\"{nl}category: \"{ctx.category}\"{nl}tags:{nl}"
        for tag in ctx.tags:
            out += f"  - {tag.strip()}{nl}"
        out += "---"
        return out
