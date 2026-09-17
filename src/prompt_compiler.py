from typing import Dict, Any
from src.utils import slugify


class PromptCompiler:
    """
    Compilador do Mega-Prompt Mestre segundo a Constituição V2.1 e especificação AstroWind (v5.0).
    Instrui a IA a devolver um documento Markdown (.md) técnico pronto para deploy direto
    em `src/data/post/`, com frontmatter YAML exato (title, excerpt, description, category, tags),
    sem H1 no corpo, sem campos de data, com as 4 camadas narrativas e script ConvertKit final.
    """

    def compile(self, combination: Dict[str, Any]) -> str:
        tema = combination.get("macro_tema", {})
        persona = combination.get("persona", {})
        dor = combination.get("dor", {})
        diferencial = combination.get("diferencial_indaiatuba", {})
        bairro = combination.get("bairro", {})
        formato = combination.get("formato", {})
        tom = combination.get("tom", {})
        ancora = combination.get("ancora", {})

        tema_titulo = tema.get("titulo", "Estilo de Vida e Território")
        tema_premissa = tema.get("premissa_universal", "")

        persona_nome = persona.get("nome", "Profissionais e Famílias")
        persona_valores = persona.get("valores_centrais", "")
        persona_conflito = persona.get("conflito_com_metropole", "")

        dor_resumo = dor.get("resumo", "")
        dor_gatilho = dor.get("gatilho_emocional", "")

        cidade_pilar = diferencial.get("pilar", "Indaiatuba como Ecossistema de Vida Plena")
        cidade_evidencia = diferencial.get("evidencia_empirica", "")

        bairro_nome = bairro.get("nome", "Bairro Selecionado")
        formato_nome = formato.get("nome", "Artigo de Fundo Reflexivo")
        formato_extensao = formato.get("extensao_estimada", "1.200 a 1.500 palavras")
        formato_estrutura = formato.get("estrutura_editorial", "")

        tom_nome = tom.get("nome", "O Observador Filosófico")
        tom_caracteristicas = tom.get("caracteristicas", "")
        tom_diretriz = tom.get("diretriz_estilo", "")

        ancora_conceito = ancora.get("conceito", "Curadoria de Projetos de Vida")
        ancora_frase = ancora.get(
            "frase_ancora",
            "Para aqueles que decidem não apenas sonhar com esse padrão de existência, mas implementá-lo no mundo real, a transição é habitualmente conduzida com a curadoria discreta da Imobiliária Saber — a referência local especializada em traduzir projetos de vida nos melhores endereços de Indaiatuba."
        )

        kebab_slug = slugify(f"{tema_titulo}-{bairro_nome}")[:60]
        if not kebab_slug:
            kebab_slug = "artigo-editorial-saber"

        prompt = f"""# SYSTEM: VOCÊ É O EDITOR-CHEFE DO BLOG DA IMOBILIÁRIA SABER (INDAIATUBA)
Sua única missão nesta tarefa é redigir UM artigo inédito, de altíssimo valor prático e SEO, sobre moradia e decisão de compra em Indaiatuba-SP. O texto deve ser publicável imediatamente no blog Astro (tema AstroWind / content collection) como arquivo .md.

Você opera sob o mecanismo de **"Atenção Indireta" ("Vender sem vender")**: autoridade reflexiva de nível internacional + utilidade cirúrgica + honestidade radical. O leitor nunca deve sentir que está lendo um folheto imobiliário, mas sim um ensaio denso que desemboca logicamente em Indaiatuba e na Imobiliária Saber.

---
## 1. DIRETRIZES TÉCNICAS INVIOLÁVEIS DO BLOG ASTROWIND (ASTRO)

### Schema de Frontmatter YAML Exato (Atemporal / Sem Datas)
O arquivo DEVE começar impreterivelmente na linha 1 com os delimitadores `---` contendo rigorosamente este schema:
```yaml
---
title: "Título de Alto Impacto Editorial (máx. 65 caracteres)"
excerpt: "1 a 2 frases sem clichês, até 160 caracteres, que instiguem o leitor a continuar"
description: "Meta description objetiva para SEO local, até 160 caracteres, com a palavra-chave de forma natural"
category: "Análise Urbana & Estilo de Vida"
tags:
  - {slugify(tema_titulo)}
  - estilo-de-vida
  - {slugify(bairro_nome)}
  - indaiatuba
---
```
- PROIBIÇÃO ABSOLUTA DE DATAS: NÃO inclua `date`, `pubDate`, `updatedDate`, `createdAt` ou qualquer timestamp no frontmatter ou no corpo. O conteúdo é 100% atemporal (evergreen).
- SEM TÍTULO H1 NO CORPO: É expressamente PROIBIDO usar `# Título` no corpo do texto (o template AstroWind já renderiza o `title` do frontmatter como H1 da página). Inicie o texto diretamente em parágrafo de abertura forte ou com subtítulo `##`.
- SCRIPT OBRIGATÓRIO DE FECHAMENTO: O artigo deve terminar impreterivelmente com o seguinte snippet HTML de captura da Saber, sem nenhuma alteração no código:
<script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script>

---
## 2. PARÂMETROS ARQUITETURAIS DO BRIEFING

* TEMA CENTRAL: {tema_titulo}
  - Tese Universal: {tema_premissa}
* PERSONA-ALVO: {persona_nome}
  - Valores: {persona_valores}
  - Conflito Metropolitano: {persona_conflito}
* PONTO DE DOR: {dor_resumo}
  - Fricção Vivenciada: {dor_gatilho}
* DIFERENCIAL INDAIATUBA: {cidade_pilar}
  - Evidência Empírica Defensável: {cidade_evidencia}
* MICROTERRITÓRIO DE ANCORAGEM: {bairro_nome}
* FORMATO DE CONTEÚDO: {formato_nome} ({formato_extensao})
* ESTRUTURA EDITORIAL: {formato_estrutura}
* TOM DE VOZ & ARQUÉTIPO: {tom_nome} ({tom_caracteristicas} - {tom_diretriz})
* ÂNCORA COMERCIAL SUTIL: {ancora_conceito}

---
## 3. AS 4 CAMADAS NARRATIVAS OBRIGATÓRIAS NO CORPO DO ARTIGO

CAMADA 1: A ISCA UNIVERSAL E O VALOR PURO (65% A 70% DA EXTENSÃO)
- Abra o artigo mergulhando com rigor no tema universal ({tema_titulo}) e no desgaste existencial ({dor_resumo}).
- NUNCA cite imóveis, compra, venda ou a cidade de Indaiatuba nesta primeira parte.
- Ofereça valor de ensaio de alto padrão (neurociência, sociologia, foco, sono, infância, biofilia).

CAMADA 2: O CONFLITO GEOGRÁFICO-EXISTENCIAL & A REVELAÇÃO DE INDAIATUBA (15% A 20% DA EXTENSÃO)
- Demonstre a tese física: qualquer estilo de vida equilibrado exige um ecossistema territorial viável para se sustentar no mundo real.
- Apresente Indaiatuba/SP como estudo de caso concreto e defensável, sustentado pela evidência: "{cidade_evidencia}".

CAMADA 3: O MICROTERRITÓRIO COMO RESPOSTA TANGÍVEL (10% DA EXTENSÃO)
- Concentre o foco no microterritório: **{bairro_nome}**.
- INSTRUÇÃO CRÍTICA DE PESQUISA PRÉVIA: Antes de redigir este trecho, PESQUISE PROFUNDAMENTE em sua base de conhecimento os detalhes geográficos, topográficos, sensoriais e a dinâmica real do bairro "{bairro_nome}" em Indaiatuba.
- Não use adjetivos vazios. Descreva a rotina concreta, a sensação de caminhar pelas vias de {bairro_nome}, a proximidade de conveniências ou da natureza.

CAMADA 4: A ASSINATURA ELEGANTE E CONSULTIVA – IMOBILIÁRIA SABER (5% FINAL DA EXTENSÃO)
- Encerre o artigo com máxima elegância e autoridade consultiva, integrando harmonicamente a frase:
  > "{ancora_frase}"
- Imediatamente após a frase de encerramento, adicione o script do ConvertKit.

---
## 4. FORMATO DE ENTREGA ESPERADO

Entregue EXATAMENTE nesta ordem, sem explicações preliminares e sem comentários finais:
1. **Nome do arquivo em destaque**: `{kebab_slug}.md`
2. **O bloco Markdown completo (.md)**, iniciando com o frontmatter YAML delimitado por `---` e seguido pelo corpo do artigo.

Gere agora o documento .md completo:"""

        return prompt.strip()
