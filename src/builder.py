"""
Construtor de prompts para geração de conteúdo no modelo Red Bull ("vender sem vender").
"""
from typing import Dict, Any


def build_lifestyle_prompt(pilar: Dict[str, Any], formato: str) -> str:
    """
    Monta o prompt para o modelo de linguagem focado na experiência de vida.
    """
    instrucao_formato = {
        "manifesto": "Escreva um manifesto visceral de 3 a 4 parágrafos sobre a retomada do tempo e do espaço.",
        "cronica": "Escreva uma crônica curta de rotina narrando o contraste entre a vida caótica urbana e a vida plena.",
        "post_reflexivo": "Escreva um texto curto em formato de reflexão direta para redes sociais com quebras de linha dinâmicas."
    }.get(formato, "Escreva uma reflexão envolvente e inspiradora.")

    prompt = f"""
Você é um ensaísta contemporâneo e estrategista de marca da Saber. Sua missão é escrever conteúdo que inspire pessoas das grandes metrópoles a reverem suas escolhas de vida, sem tentar vender imóveis diretamente.

TEMA CENTRAL: {pilar.get('nome')}
DOR URBANA: {pilar.get('dor')}
ASPIRAÇÃO / ESTILO DE VIDA: {pilar.get('aspiracao')}
CENÁRIO SUTIL: {pilar.get('cenario_implicito')}

DIRETRIZES RÍGIDAS:
1. {instrucao_formato}
2. Não mencione características técnicas de casas ou apartamentos (proibido falar de suítes, garagens ou acabamentos).
3. Não cite nomes de bairros específicos. Deixe que o estilo de vida fale por si.
4. Conclua com uma assinatura elegante que conecte a busca por essa rotina com a Saber (ex: 'O tempo é a única moeda que não se recupera. Conheça o ritmo da Saber.').
"""
    return prompt.strip()
