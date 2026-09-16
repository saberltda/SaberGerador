"""
Motor de combinações e montagem do arquivo TXT para download.
"""
from typing import List, Dict, Any
from src.builder import build_astro_prompt

ANGULOS = [
    "O Custo Invisível do Tempo Perdido",
    "A Ilusão do Conforto Metropolitano",
    "A Psicologia do Silêncio e Produtividade",
    "Criar Filhos no Mundo Real vs Confinamento",
    "A Nova Definição de Luxo: Autonomia e Ar Puro"
]

FORMATOS = [
    "Ensaio Reflexivo com Crônica de Rotina",
    "Manifesto Editorial Visceral",
    "Guia Prático de Transição de Estilo de Vida"
]

TONS = [
    "Provocativo, maduro e reflexivo",
    "Sensorial, intimista e acolhedor",
    "Direto, analítico e pragmático"
]


class CombinadorEngine:
    def __init__(self, pilares: List[Dict[str, Any]]):
        self.pilares = pilares

    def gerar_arquivo_combinado(
        self,
        pilares_selecionados: List[Dict[str, Any]] = None,
        multiplicar_todos: bool = False
    ) -> str:
        """
        Gera um arquivo TXT contendo todas as combinações prontas para colar no Gemini.
        """
        alvos = pilares_selecionados if pilares_selecionados else self.pilares
        blocos = []
        contador = 1

        for pilar in alvos:
            if multiplicar_todos:
                for angulo in ANGULOS:
                    for formato in FORMATOS:
                        for tom in TONS:
                            prompt = build_astro_prompt(pilar, angulo, formato, tom)
                            bloco = f"{'='*70}\nCOMBINAÇÃO #{contador:04d} | {pilar['nome']} | {angulo}\n{'='*70}\n\n{prompt}\n\n"
                            blocos.append(bloco)
                            contador += 1
            else:
                for angulo in ANGULOS:
                    prompt = build_astro_prompt(pilar, angulo, FORMATOS[0], TONS[0])
                    bloco = f"{'='*70}\nCOMBINAÇÃO #{contador:04d} | {pilar['nome']} | {angulo}\n{'='*70}\n\n{prompt}\n\n"
                    blocos.append(bloco)
                    contador += 1

        cabecalho = (
            f"SABER GERADOR - COLEÇÃO DE PROMPTS PARA ASTRO BLOG (ESTILO RED BULL)\n"
            f"Total de Prompts Gerados: {len(blocos)}\n"
            f"Como usar: Copie qualquer um dos blocos abaixo e cole no Gemini para obter o arquivo .md pronto.\n\n"
        )
        return cabecalho + "".join(blocos)
