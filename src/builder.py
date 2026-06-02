# src/builder.py
import datetime

class PromptBuilder:
    """
    O 'Redator' (Modo Livre).
    Monta o prompt mestre passando todas as intenções diretas do usuário de forma agnóstica 
    para abranger tanto Jornalismo quanto Setor Imobiliário.
    """

    CTA_CAPTURE_CODE = """
<div style="text-align:center; margin: 40px 0;">
<script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script>
</div>
"""

    def __init__(self):
        pass

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        bairro = d['bairro']['nome']
        
        return f"""
## GENESIS MAGNETO V.72 — MODO GENERATIVO LIVRE
**Objetivo:** Produzir um conteúdo magistral, com profundidade cirúrgica, baseado estritamente nas diretrizes livres do operador humano.
**Data de Publicação Alvo:** {data_pub}
**Timestamp (Atual):** {data_mod} (Horário de Brasília)

## 1. INSTRUÇÕES DO OPERADOR (PARÂMETROS ESTRATÉGICOS)
O usuário definiu parâmetros exatos abaixo. Você DEVE guiar todo o seu estilo, linguagem, estrutura e linha argumentativa por eles:
- **CONTEXTO / MODO DA ESCRITA:** {d['contexto']}
- **LOCALIZAÇÃO GEOGRÁFICA ALVO:** {bairro}
- **OBJETO CENTRAL (PRODUTO OU PAUTA):** {d['ativo']}
- **PÚBLICO-ALVO / LEITOR:** {d['persona']}
- **ABORDAGEM / GATILHO PSICOLÓGICO:** {d['gatilho']}
- **TESE / ÂNGULO PRINCIPAL:** {d['topico']}
- **FORMATO DO CONTEÚDO:** {d['formato']}

## 2. DIRETRIZES MANUAIS / EXIGÊNCIAS (IMPORTANTE)
Atenção absoluta a este direcionamento extra exigido pelo usuário:
> "{d['dicas']}"

## 3. MISSÃO E PESQUISA DE CAMPO
A internet exige qualidade. É inegociável que você mergulhe em sua base de dados e traga contexto real da região:
- **Zero Obviedade:** Detalhe fatos reais, ruas, localização geográfica verdadeira, infraestrutura e história.
- **Autoridade:** Aja com maestria absoluta dentro do Contexto estipulado acima, fundindo suas palavras à Persona e à Abordagem de maneira invisível e fluida.

## 4. INSUMOS (LEIS INEGOCIÁVEIS DO SISTEMA)
<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 5. CTA (Call To Action) OBRIGATÓRIO
No local exato estipulado nas regras (Fim do HTML), você DEVE inserir o código abaixo rigorosamente:
{self.CTA_CAPTURE_CODE}

## 6. CHECKLIST FINAL (ORDEM DA SUA RESPOSTA)
1. DOSSIÊ DE PESQUISA PROFUNDA (Use a tag <research_process> trazendo o que você sabe de verdade sobre o local para usar no texto).
2. TÍTULO SUGERIDO (H1 otimizado para SEO).
3. CONTEÚDO EM HTML (Estruturado conforme o "Formato do Conteúdo" e injetando o script JSON-LD exigido).
4. MARCADORES/TAGS (Crie de 5 a 10 tags baseadas no conteúdo e no assunto principal, separadas por vírgula).
""".strip()
