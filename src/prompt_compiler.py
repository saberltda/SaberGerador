from typing import Dict, Any
from src.utils import slugify


class PromptCompiler:
    """
    Compilador do Mega-Prompt Mestre segundo a Constituição V2.1.
    Instrui a IA a devolver a resposta como um arquivo .md completo para Blog Astro,
    com frontmatter YAML contendo configurações de SEO avançadas e estritamente sem campos de data.
    Também impõe as 4 camadas narrativas e a pesquisa profunda prévia sobre o bairro.
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
        formato_canal = formato.get("canal_veiculo", "Blog Astro / Conteúdo Editorial")
        formato_estrutura = formato.get("estrutura_editorial", "")

        tom_nome = tom.get("nome", "O Observador Filosófico")
        tom_caracteristicas = tom.get("caracteristicas", "")
        tom_diretriz = tom.get("diretriz_estilo", "")

        ancora_conceito = ancora.get("conceito", "Curadoria de Projetos de Vida")
        ancora_frase = ancora.get(
            "frase_ancora",
            "Para aqueles que decidem não apenas sonhar com esse padrão de existência, mas implementá-lo no mundo real, a transição é habitualmente conduzida com a curadoria discreta da Imobiliária Saber — a referência local especializada em traduzir projetos de vida nos melhores endereços de Indaiatuba."
        )

        prompt = f"""Você é um redator sênior e estrategista de SEO editorial. Sua tarefa é redigir um arquivo Markdown (.md) completo e pronto para ser salvo diretamente na coleção de conteúdo de um Blog Astro (Content Collections).

================================================================================
DIRETRIZ DE SAÍDA: ARQUIVO .MD PARA ASTRO COM FRONTMATTER DE SEO (ATEMPORAL)
================================================================================
Sua resposta deve ser EXCLUSIVAMENTE o conteúdo do arquivo Markdown (.md), iniciando com o bloco frontmatter YAML delimitado por `---` e seguido pelo corpo do texto estruturado em Markdown.

REGRAS RÍGIDAS DE FRONTMATTER (SEO ATEMPORAL):
1. PROIBIÇÃO TOTAL DE DATAS: Não inclua campos como `date`, `pubDate`, `updatedDate`, `createdAt` ou qualquer timestamp (este conteúdo é 100% atemporal/evergreen).
2. O frontmatter DEVE conter obrigatoriamente as seguintes chaves preenchidas com precisão:
   - title: Título editorial de alto impacto (máx. 65 caracteres, instigante, sem clichês imobiliários).
   - description: Meta description atrativa e otimizada para CTR no Google (entre 140 e 155 caracteres).
   - slug: Slug em minúsculas separado por hífens derivado do tema.
   - author: "Redação Saber Editorial"
   - tags: Lista em YAML com 4 a 6 tags pertinentes (ex.: estilo-de-vida, neurociencia, qualidade-de-vida, indaiatuba).
   - canonicalURL: URL canônica sugerida (ex: "/artigos/slug-do-artigo").
   - draft: false
   - featured: true
   - seo:
       metaTitle: Título SEO refinado
       metaDescription: Descrição otimizada
       keywords: [lista de 5 termos de busca orgânica de cauda longa]

Exemplo de início obrigatório da sua resposta:
---
title: "O Título do Artigo Aqui"
description: "A meta description perfeita de 140 a 155 caracteres aqui..."
slug: "slug-amigavel-do-artigo"
author: "Redação Saber Editorial"
tags:
  - estilo-de-vida
  - qualidade-de-vida
  - indaiatuba
canonicalURL: "/artigos/slug-amigavel-do-artigo"
draft: false
featured: true
seo:
  metaTitle: "Título SEO para a SERP"
  metaDescription: "Meta description para o Google..."
  keywords:
    - qualidade de vida no interior
    - morar em indaiatuba
    - rotina saudavel
---

# [Título H1 idêntico ou complementar ao Title]

[Corpo do texto...]

================================================================================
MECANISMO DE CONTEÚDO: ATENÇÃO INDIRETA ("VENDER SEM VENDER")
================================================================================
* FORMATO DE SAÍDA: **{formato_nome}** ({formato_extensao}).
* TEMA CENTRAL: {tema_titulo}
  - Tese: {tema_premissa}
* PERSONA: {persona_nome}
  - Valores: {persona_valores}
  - Conflito: {persona_conflito}
* PONTO DE DOR: {dor_resumo}
  - Fricção: {dor_gatilho}
* DIFERENCIAL INDAIATUBA: {cidade_pilar}
  - Evidência Real: {cidade_evidencia}
* MICROTERRITÓRIO: {bairro_nome}
* TOM DE VOZ: {tom_nome} ({tom_caracteristicas} - {tom_diretriz})
* ÂNCORA COMERCIAL SUTIL: {ancora_conceito}

--------------------------------------------------------------------------------
AS 4 CAMADAS NARRATIVAS OBRIGATÓRIAS NO CORPO DO ARTIGO:
--------------------------------------------------------------------------------

CAMADA 1: A ISCA UNIVERSAL E O VALOR PURO (65% A 70% DO CONTEÚDO)
- Abra o artigo discutindo a fundo o tema universal ({tema_titulo}) e a dor existencial ({dor_resumo}).
- NUNCA mencione imóveis, transações imobiliárias ou Indaiatuba nos primeiros subtítulos/seções.
- Ofereça valor de alto nível (neurociência, sociologia, filosofia, comportamento). O leitor deve ser capturado pelo fascínio do conhecimento.

CAMADA 2: O CONFLITO GEOGRÁFICO-EXISTENCIAL (15% A 20% DO CONTEÚDO)
- Construa a ponte lógica demonstrando que todo projeto de qualidade de vida depende do ecossistema territorial no qual se habita.
- Apresente Indaiatuba como estudo de caso empírico de equilíbrio, sustentado pelo pilar "{cidade_pilar}" e pela evidência "{cidade_evidencia}".

CAMADA 3: O MICROTERRITÓRIO COMO RESPOSTA TANGÍVEL (10% DO CONTEÚDO)
- Concentre o foco no bairro: **{bairro_nome}**.
- REGRA CRÍTICA DE PESQUISA PRÉVIA: Antes de redigir este bloco, acesse seus dados e PESQUISE PROFUNDAMENTE o bairro "{bairro_nome}" em Indaiatuba (sua atmosfera, perfil de vizinhança, topografia, áreas verdes e conveniências). Descreva detalhes autênticos e sensoriais desse microterritório sem generalizações vazias.

CAMADA 4: A ASSINATURA ELEGANTE E CONSULTIVA – IMOBILIÁRIA SABER (5% FINAL)
- Feche o artigo com sofisticação inserindo organicamente a âncora:
  > "{ancora_frase}"
- O posicionamento deve ser puramente consultivo, sem nenhuma linguagem apelativa de anúncio.

--------------------------------------------------------------------------------
DIRETRIZES TÉCNICAS INVIOLÁVEIS:
--------------------------------------------------------------------------------
1. Entregue apenas o código Markdown válido, sem blocos de comentários introdutórios antes do frontmatter e sem explicações no final.
2. Formate subtítulos com `##` e `###` respeitando boa hierarquia para SEO.
3. PROIBIDO: Usar linguagem de anúncio ("não perca", "últimas unidades", "compre já", "ligue agora").
4. PROIBIDO: Ataques a outras cidades (trabalhe apenas com dados objetivos de contraste como tempo de deslocamento e decibéis)."""

        return prompt.strip()
