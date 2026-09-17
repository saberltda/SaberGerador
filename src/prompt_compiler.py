from typing import Dict, Any


class PromptCompiler:
    """
    Compilador do Mega-Prompt Mestre segundo as 4 Camadas Narrativas da Constituição V2.1.
    Garante que a instrução de pesquisa profunda do bairro (assets/bairros.json)
    esteja explicitamente presente para a IA receptora.
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
        formato_canal = formato.get("canal_veiculo", "Publicação Editorial")
        formato_estrutura = formato.get("estrutura_editorial", "")

        tom_nome = tom.get("nome", "O Observador Filosófico")
        tom_caracteristicas = tom.get("caracteristicas", "")
        tom_diretriz = tom.get("diretriz_estilo", "")

        ancora_conceito = ancora.get("conceito", "Curadoria de Projetos de Vida")
        ancora_frase = ancora.get(
            "frase_ancora",
            "Para aqueles que decidem não apenas sonhar com esse padrão de existência, mas implementá-lo no mundo real, a transição é habitualmente conduzida com a curadoria discreta da Imobiliária Saber — a referência local especializada em traduzir projetos de vida nos melhores endereços de Indaiatuba."
        )

        prompt = f"""Você é um escritor e ensaísta de nível editorial internacional. Sua missão é redigir um conteúdo completo no formato: **{formato_nome}** ({formato_extensao}), idealizado para veiculação em **{formato_canal}**.

================================================================================
DIRETRIZ ESTRUTURAL OBRIGATÓRIA: MECANISMO DE ATENÇÃO INDIRETA ("EFEITO RED BULL")
================================================================================
O objetivo deste conteúdo é gerar altíssima retenção orgânica, educando, inspirando e conectando com as inquietações existenciais mais profundas do leitor, conduzindo-o de forma subliminar até o território de Indaiatuba e à autoridade da Imobiliária Saber.
O texto final NUNCA pode soar como panfleto imobiliário tradicional ("compre já", "excelente oportunidade de investimento", "ligue agora").

--------------------------------------------------------------------------------
PARÂMETROS ARQUITETURAIS DA NARRATIVA:
--------------------------------------------------------------------------------
* TEMA CENTRAL: {tema_titulo}
  - Tese Universal: {tema_premissa}
* PERSONA-ALVO: {persona_nome}
  - Valores Centrais: {persona_valores}
  - Conflito Metropolitano: {persona_conflito}
* PONTO DE DOR / GATILHO EMOCIONAL: {dor_resumo}
  - Fricção Vivenciada: {dor_gatilho}
* REVELAÇÃO GEOGRÁFICA (INDAIATUBA): {cidade_pilar}
  - Evidência Empírica Defensável: {cidade_evidencia}
* MICROTERRITÓRIO DE ANCORAGEM: {bairro_nome}
* TOM DE VOZ & ARQUÉTIPO: {tom_nome}
  - Identidade: {tom_caracteristicas}
  - Diretriz de Estilo: {tom_diretriz}
* ÂNCORA COMERCIAL SUTIL: {ancora_conceito}

--------------------------------------------------------------------------------
REQUISITOS DE COMPOSIÇÃO NAS 4 CAMADAS OBRIGATÓRIAS:
--------------------------------------------------------------------------------

CAMADA 1: A ISCA UNIVERSAL E O VALOR PURO (65% A 70% DA EXTENSÃO)
- Abra exclusivamente mergulhando no tema universal ({tema_titulo}).
- NUNCA mencione imóveis, termos comerciais, transações financeiras ou a cidade de Indaiatuba no primeiro terço do texto.
- Desenvolva com densidade reflexiva, profundidade científica e sensibilidade humana a dor ({dor_resumo}), validando o desgaste existencial da persona ({persona_nome}).
- Proporcione valor genuíno, gerando o impacto de um ensaio da New Yorker ou de um artigo aprofundado de caderno cultural.

CAMADA 2: O CONFLITO GEOGRÁFICO-EXISTENCIAL & A REVELAÇÃO DE INDAIATUBA (15% A 20% DA EXTENSÃO)
- Estabeleça a transição orgânica: teses de estilo de vida, sono, foco ou família exigem um ecossistema físico viável para florescer no mundo real.
- Apresente Indaiatuba/SP como estudo de caso concreto e irrefutável, respaldando-se na evidência: "{cidade_evidencia}".
- Mostre a cidade como resposta pacífica ao colapso do tempo metropolitano, destacando a conectividade com Viracopos e eixos viários, sem adjetivações vazias.

CAMADA 3: O MICROTERRITÓRIO COMO RESPOSTA TANGÍVEL (10% DA EXTENSÃO)
- Foco específico no bairro/condomínio: **{bairro_nome}**.
- INSTRUÇÃO CRÍTICA DE PESQUISA PRÉVIA: Como modelo de IA, antes de redigir esta seção, acesse sua base de conhecimento e PESQUISE PROFUNDAMENTE as características geográficas, topográficas, sensoriais, históricas e de vizinhança específicas do bairro "{bairro_nome}" em Indaiatuba.
- Não invente detalhes genéricos. Descreva a rotina concreta, a sensação de caminhar pelas alamedas de {bairro_nome}, a proximidade de conveniências ou da natureza, traduzindo o local como a morada tangível da paz buscada pela persona.

CAMADA 4: A ASSINATURA ELEGANTE E CONSULTIVA – IMOBILIÁRIA SABER (5% FINAL DA EXTENSÃO)
- Encerre a narrativa com elegância máxima, inserindo harmonicamente a seguinte ancoragem:
  > "{ancora_frase}"
- O fechamento deve posicionar a Imobiliária Saber no topo da pirâmide de valor como curadora discreta e consultiva de projetos de vida, jamais como vendedora de imóveis.

--------------------------------------------------------------------------------
DIRETRIZES TÉCNICAS E PROIBIÇÕES INVIOLÁVEIS:
--------------------------------------------------------------------------------
1. ESTRUTURA EDITORIAL DO FORMATO: Siga a cadência de: {formato_estrutura}.
2. PROIBIDO: Usar linguagem de anúncio ("não perca", "últimas unidades", "excelente oportunidade", "compre já", "ligue agora").
3. PROIBIDO: Usar termos depreciativos, ofensivos ou ataques nominais a outras cidades ou capitais (trabalhe exclusivamente com contrastes empíricos universais: horas de trânsito, poluição sonora, horizonte visual).
4. RESPEITO À VERACIDADE: Todas as informações e evidências sobre Indaiatuba devem ser defensáveis e verídicas.
5. O texto gerado deve ser integral, refinado e pronto para publicação direta."""

        return prompt.strip()
