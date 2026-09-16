"""
Motor de orquestração editorial do SaberGerador.
Combina bairros, temas, dados urbanos e perfis analíticos para formular pautas completas.
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.builder import PautaContext, PromptBuilder, ANGULOS, INTENTS, DEPTHS, TONS, LOCALISMOS

TEMAS_COMPLETOS = [
    {
        "tema": "Acústica Urbana e Ventos",
        "crenca": "Achar que muro alto de condomínio ou vidro duplo resolve qualquer ruído da cidade.",
        "dor": "Comprar o imóvel e descobrir, na primeira noite de vento, que a curva de relevo e o alinhamento das vias canalizam o som da rodovia ou de avenidas expressas direto para a janela dos quartos.",
        "categoria": "Análise Urbana & Acústica",
        "tags": ["Acústica Urbana", "Indaiatuba", "Zoneamento", "Planejamento Residencial"],
        "insightBase": "O ruído em Indaiatuba raramente é “volume constante”; ele é direcional e depende de vento, topografia e horário de pico escolar/comercial."
    },
    {
        "tema": "Orientação Solar e Conforto Térmico",
        "crenca": "Achar que sol da tarde se resolve apenas instalando aparelhos potentes de ar-condicionado.",
        "dor": "Projetar ou comprar suítes viradas para o poente com fachadas envidraçadas que acumulam calor até as 22h, elevando a conta de luz e degradando a qualidade do sono.",
        "categoria": "Arquitetura & Conforto Térmico",
        "tags": ["Insolação", "Orientação Solar", "Arquitetura", "Imóveis Indaiatuba"],
        "insightBase": "Em Indaiatuba o sol de final de tarde (oeste/noroeste) é especialmente agressivo entre setembro e março; a solução mais barata quase sempre é projeto, não equipamento."
    },
    {
        "tema": "Casa Térrea vs. Sobrado",
        "crenca": "Achar que o sobrado sempre oferece o melhor aproveitamento de terreno e menor custo por metro quadrado.",
        "dor": "Ignorar a logística familiar de longo prazo: escadas que viram barreiras para crianças pequenas, pets idosos ou pós-operatórios, além do custo de manutenção de calhas e pintura externa duplicado.",
        "categoria": "Tipologia & Planta",
        "tags": ["Casa Térrea", "Sobrado", "Liquidez Imobiliária", "Acessibilidade"],
        "insightBase": "A liquidez de uma casa térrea bem localizada em Indaiatuba costuma ser superior à de sobrados equivalentes quando o comprador final tem mais de 50 anos ou filhos pequenos."
    },
    {
        "tema": "Logística Escolar e Trânsito Pendular",
        "crenca": "Achar que em cidade de médio porte qualquer trajeto leva menos de 5 minutos de carro.",
        "dor": "Gastar 35–50 minutos diários no cruzamento das rotatórias centrais nos horários de pico escolar (7h10–7h40 e 17h20–18h10), anulando a sonhada paz ao migrar de São Paulo.",
        "categoria": "Mobilidade & Rotina",
        "tags": ["Trânsito Escolar", "Mobilidade Urbana", "Rotina Familiar", "Indaiatuba"],
        "insightBase": "O gargalo real não é a distância em km, e sim a concentração de colégios e o desenho das rotatórias no eixo central em horários muito específicos."
    },
    {
        "tema": "Garagem Real vs. Dimensão de SUVs",
        "crenca": "Achar que “duas vagas cobertas” na planta atendem qualquer veículo moderno da família.",
        "dor": "Comprar a casa e constatar que, ao estacionar um SUV médio e outro veículo, os passageiros não conseguem abrir as portas sem bater no pilar ou no recuo lateral.",
        "categoria": "Engenharia de Uso",
        "tags": ["Garagem", "Planta Residencial", "Vistorias", "Projetos"],
        "insightBase": "A medida útil de uma vaga “de verdade” precisa considerar abertura de porta de SUV + carrinho de bebê ou cadeirante, não só o comprimento do carro."
    },
    {
        "tema": "Topografia do Lote e Capex Oculto",
        "crenca": "Achar que lote em declive com valor 15–25% abaixo da média compensa financeiramente a construção.",
        "dor": "Economizar na escritura e gastar três a quatro vezes mais em muros de arrimo, sapatas profundas, drenagem reforçada e bota-fora de terra.",
        "categoria": "Inteligência Financeira",
        "tags": ["Topografia", "Custo de Obra", "Terrenos em Condomínio", "Construção"],
        "insightBase": "Em Indaiatuba o custo de contenção e drenagem em terrenos com mais de 1,5 m de desnível costuma superar qualquer “desconto” de tabela."
    },
    {
        "tema": "Recuos Laterais e Privacidade Visual",
        "crenca": "Achar que 1,5 metro de recuo lateral nas normas municipais resguarda a intimidade da casa.",
        "dor": "Janelas de dormitórios alinhadas parede-com-parede com o terraço ou varanda gourmet do vizinho, obrigando ao uso de cortinas fechadas o dia inteiro.",
        "categoria": "Planejamento e Privacidade",
        "tags": ["Privacidade", "Recuos Obrigatórios", "Plano Diretor", "Qualidade de Vida"],
        "insightBase": "O problema quase nunca é o recuo mínimo da lei; é a falta de projeto de aberturas e a ausência de vegetação ou brise no momento da compra."
    },
    {
        "tema": "Retrofit e Potencial de Casas Antigas",
        "crenca": "Achar que reforma cosmética (pintura moderna e piso vinílico) valoriza casa antiga com segurança.",
        "dor": "Comprar casa dos anos 80/90 sem periciar a fiação elétrica, o encanamento de cobre/ferro e a impermeabilização dos baldrames, herdando infiltrações crônicas.",
        "categoria": "Retrofit & Valorização",
        "tags": ["Retrofit", "Casas Antigas", "Engenharia Diagnóstica", "Investimento Imobiliário"],
        "insightBase": "Em bairros como Jardim Pau Preto e Cidade Nova o potencial de retrofit é real, mas só se o diagnóstico estrutural e de instalações for feito antes da proposta."
    },
    {
        "tema": "Trabalho Híbrido SP–Indaiatuba",
        "crenca": "Achar que a viagem pela Rodovia dos Bandeirantes ou Santos Dumont é sempre fluida e previsível.",
        "dor": "Não computar o tempo “pós-pedágio” dentro da malha de tráfego local de Indaiatuba para chegar em casa após um dia extenuante de trabalho na capital.",
        "categoria": "Estilo de Vida & Migração",
        "tags": ["Trabalho Híbrido", "Migração SP", "Rodovia SP-075", "Vida no Interior"],
        "insightBase": "O diferencial real não é só o tempo de rodovia; é a distância da casa até o acesso à SP-075 ou Santos Dumont em horário de pico de retorno."
    },
    {
        "tema": "Lazer Gourmet e Custos de Manutenção",
        "crenca": "Achar que ter piscina com cascata e área gourmet imensa é puro lazer sem custo de tempo.",
        "dor": "Transformar as manhãs de sábado em tarefas mecânicas de aspiração, controle químico de cloro e limpeza de pedras atérmicas em vez de descansar com a família.",
        "categoria": "Custos de Posse & Rotina",
        "tags": ["Área Gourmet", "Custo de Posse", "Manutenção Residencial", "Uso Real"],
        "insightBase": "O custo real de uma área gourmet + piscina em Indaiatuba não é só financeiro; é a captura de 4–8 horas semanais de tempo do casal."
    },
    {
        "tema": "Densidade e Escala de Condomínio",
        "crenca": "Achar que condomínio fechado sempre entrega mais segurança e qualidade de vida que rua aberta.",
        "dor": "Descobrir que a taxa condominial, as regras de uso e a densidade de vizinhos geram mais atrito diário do que a vida em rua consolidada com boa vizinhança.",
        "categoria": "Condomínio vs. Rua",
        "tags": ["Condomínio Fechado", "Taxa Condominial", "Qualidade de Vida", "Indaiatuba"],
        "insightBase": "Em muitos bairros de Indaiatuba a percepção de segurança de rua aberta bem consolidada é igual ou superior à de condomínios de baixa densidade, com custo mensal muito menor."
    },
    {
        "tema": "Infraestrutura de Água, Esgoto e Energia",
        "crenca": "Achar que “água e esgoto da rua” significa zero risco de obra futura.",
        "dor": "Comprar imóvel em área de expansão e descobrir que a rede ainda é precária ou que a capacidade de energia exige reforço caro para o padrão de consumo atual (ar, carro elétrico, home office).",
        "categoria": "Infraestrutura & Risco",
        "tags": ["Infraestrutura", "Rede de Água", "Energia Elétrica", "Risco de Obra"],
        "insightBase": "O mapa oficial da prefeitura e o histórico de reclamações no bairro dizem mais sobre risco de infraestrutura do que o anúncio do corretor."
    },
    {
        "tema": "Home Office e Isolamento Acústico Real",
        "crenca": "Achar que qualquer quarto extra vira escritório funcional.",
        "dor": "Instalar o home office em cômodo com parede compartilhada com a rua ou com a área de serviço e descobrir que reuniões viram inviáveis entre 7h30 e 9h e entre 17h e 19h.",
        "categoria": "Trabalho Remoto & Planta",
        "tags": ["Home Office", "Isolamento Acústico", "Planta Residencial", "Produtividade"],
        "insightBase": "O melhor cômodo para home office em Indaiatuba quase nunca é o que tem a “melhor vista”; é o que tem a menor exposição a ruído de rua e de área de serviço."
    },
    {
        "tema": "Valorização vs. Liquidez Real",
        "crenca": "Achar que o bairro que mais valorizou nos últimos 5 anos é automaticamente o melhor lugar para comprar agora.",
        "dor": "Comprar no pico de valorização de um condomínio novo e descobrir que o tempo médio de venda (liquidez) é o dobro do de um bairro consolidado equivalente.",
        "categoria": "Inteligência de Mercado",
        "tags": ["Valorização Imobiliária", "Liquidez", "Mercado Imobiliário Indaiatuba", "Decisão de Compra"],
        "insightBase": "Em Indaiatuba, liquidez (tempo até vender) costuma ser mais importante para o patrimônio familiar do que a valorização percentual de curto prazo."
    },
    {
        "tema": "Arborização, Sombra e Manutenção",
        "crenca": "Achar que árvore grande no terreno é sempre um ativo de qualidade de vida.",
        "dor": "Herdar árvores de grande porte com raízes que ameaçam calçada, muro ou tubulação, e descobrir que a poda e a eventual remoção têm custo e burocracia significativos.",
        "categoria": "Paisagismo & Manutenção",
        "tags": ["Arborização", "Manutenção Residencial", "Paisagismo", "Custo de Posse"],
        "insightBase": "A sombra de uma árvore madura em Indaiatuba é valiosa, mas só se a espécie e a localização forem compatíveis com a infraestrutura do lote."
    }
]


class EditorialEngine:
    def __init__(self, bairros_path: Optional[Path] = None):
        if bairros_path and bairros_path.exists():
            with open(bairros_path, "r", encoding="utf-8") as f:
                self.bairros = json.load(f)
        else:
            default_path = Path(__file__).resolve().parent.parent / "assets" / "bairros.json"
            if default_path.exists():
                with open(default_path, "r", encoding="utf-8") as f:
                    self.bairros = json.load(f)
            else:
                self.bairros = []

    def gerar_titulo(self, tema: Dict[str, Any], bairro: Dict[str, Any], angulo_key: str) -> str:
        templates = [
            f"{tema['tema']} em {bairro['nome']}: O que a Planta e o Anúncio Não Contam",
            f"A Verdadeira Mecânica de Morar em {bairro['nome']}: Como Avaliar {tema['tema']}",
            f"{tema['tema']} em Indaiatuba: O Teste de Campo para Fazer em {bairro['nome']}",
            f"Antes de Comprar em {bairro['nome']}: O Impacto Real de {tema['tema']} na Rotina",
            f"A Leitura de Cidade em {bairro['nome']}: Por que {tema['tema']} Muda a Conta Final",
            f"{bairro['nome']} e {tema['tema']}: O Guia que o Corretor Não Entrega",
            f"O Erro Mais Comum ao Avaliar {tema['tema']} em {bairro['nome']}",
            f"{tema['tema']} em {bairro['nome']}: Mito, Realidade e Protocolo de Decisão",
            f"Por que {tema['tema']} Define se a Compra em {bairro['nome']} Compensa",
            f"Checklist de Campo: {tema['tema']} em {bairro['nome']} (Indaiatuba)",
            f"{bairro['nome']}: Como {tema['tema']} Afeta Conforto, Custo e Liquidez",
            f"A Decisão de Comprar em {bairro['nome']} Passa por {tema['tema']} — Veja Porquê"
        ]
        if angulo_key == "protocolo-campo":
            templates.append(f"Protocolo de Vistoria: {tema['tema']} em {bairro['nome']}")
            templates.append(f"O que Verificar em Campo sobre {tema['tema']} em {bairro['nome']}")
        elif angulo_key == "custo-oculto":
            templates.append(f"O Custo Real de Ignorar {tema['tema']} em {bairro['nome']}")
            templates.append(f"{tema['tema']} em {bairro['nome']}: Onde Está o Dinheiro Escondido")
        elif angulo_key == "mito-vs-fato":
            templates.append(f"Mito vs. Fato: {tema['tema']} em {bairro['nome']}")

        return random.choice(templates)

    def gerar_insight(self, tema: Dict[str, Any], bairro: Dict[str, Any]) -> str:
        extras = [
            f"Em {bairro['nome']}, {bairro.get('caracteristica', '')}.",
            f"O ponto cego mais frequente em {bairro['nome']} envolve {bairro.get('risco', 'a manutenção de infraestrutura')}.",
            f"Quem já mora no bairro costuma notar primeiro: {bairro.get('clima', 'a ventilação local')}.",
            tema.get("insightBase", ""),
            f"A combinação de {tema['tema'].lower()} com o perfil de {bairro.get('perfil', '')} cria um cenário que raramente aparece nos anúncios."
        ]
        fechos = [
            "Isso muda a forma como se avalia planta, horário de visita e proposta.",
            "Ignorar esse detalhe costuma custar mais caro do que qualquer “desconto” de tabela.",
            "O comprador atento usa isso como filtro antes mesmo de agendar a segunda visita.",
            "É o tipo de informação que separa decisão informada de decisão por impulso."
        ]
        return f"{random.choice(extras)} {random.choice(fechos)}"

    def gerar_limite(self, tema: Dict[str, Any], bairro: Dict[str, Any]) -> str:
        bases = [
            "Quem exige silêncio monástico de janelas abertas 24h e não tolera a dinâmica real do bairro.",
            "Famílias que precisam fazer tudo a pé e não querem planejar deslocamentos mínimos de carro.",
            "Compradores que buscam “zero manutenção” e não aceitam nenhum trade-off de planta ou localização.",
            "Investidores que priorizam apenas valorização de curto prazo e ignoram liquidez e custo de posse.",
            "Quem não tem paciência para vistoria técnica e prefere decidir só pelo feeling do estande ou do anúncio."
        ]
        return f"{random.choice(bases)} Em {bairro['nome']}, isso se agrava quando se ignora {tema['tema'].lower()}."

    def gerar_keywords(self, tema: Dict[str, Any], bairro: Dict[str, Any]) -> (str, str):
        primarias = [
            f"{tema['tema'].lower()} {bairro['nome'].lower()}",
            f"casa em {bairro['nome'].lower()} indaiatuba",
            f"{bairro['nome'].lower()} indaiatuba {tema['tags'][0].lower()}",
            f"morar em {bairro['nome'].lower()}",
            f"{tema['tags'][0].lower()} indaiatuba"
        ]
        kw_primary = random.choice(primarias)
        tags_raw = tema.get("tags", []) + [bairro["nome"], "Indaiatuba", "decisão imobiliária", "custo de posse"]
        kw_secondary = ", ".join(list(dict.fromkeys(tags_raw))[:5])
        return kw_primary, kw_secondary

    def sortear_pauta_completa(
        self,
        angulo_override: Optional[str] = None,
        intent_override: Optional[str] = None,
        depth_override: Optional[str] = None,
        tom_override: Optional[str] = None,
        localismo_override: Optional[str] = None
    ) -> PautaContext:
        bairro = random.choice(self.bairros)
        tema = random.choice(TEMAS_COMPLETOS)

        angulo_key = angulo_override or random.choice(list(ANGULOS.keys()))
        intent_key = intent_override or random.choice(list(INTENTS.keys()))
        depth_key = depth_override or random.choice(["padrao", "padrao", "denso", "rapido", "pillar"])
        tom_key = tom_override or random.choice(list(TONS.keys()))
        localismo_key = localismo_override or random.choice(["alto", "alto", "medio"])

        titulo = self.gerar_titulo(tema, bairro, angulo_key)
        insight = self.gerar_insight(tema, bairro)
        limite = self.gerar_limite(tema, bairro)
        kw_primary, kw_secondary = self.gerar_keywords(tema, bairro)

        mecanica = (
            f"{bairro.get('caracteristica', '')}. "
            f"Clima/ventos: {bairro.get('clima', '')}. "
            f"Ponto de atenção de infraestrutura/terreno: {bairro.get('risco', '')}."
        )

        tags = tema.get("tags", []) + [bairro["nome"], "Indaiatuba"]

        return PautaContext(
            title=titulo,
            bairro=bairro["nome"],
            category=tema["categoria"],
            vias=f"{bairro.get('via', '')} ({bairro.get('perfil', '')})",
            dor=tema["dor"],
            crenca=tema["crenca"],
            mecanica=mecanica,
            limite=limite,
            insight=insight,
            kw_primary=kw_primary,
            kw_secondary=kw_secondary,
            tags=tags,
            angulo_key=angulo_key,
            intent_key=intent_key,
            depth_key=depth_key,
            tom_key=tom_key,
            localismo_key=localismo_key
        )
