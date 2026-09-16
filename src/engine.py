"""
Motor de geração de narrativas de estilo de vida.
"""
import os
import google.generativeai as genai
from typing import Dict, Any
from src.builder import build_lifestyle_prompt


class LifestyleEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.model = None

    def gerar_narrativa(self, pilar: Dict[str, Any], formato: str = "manifesto") -> str:
        """
        Gera uma peça de conteúdo que vende o estilo de vida sem vender o imóvel.
        """
        prompt = build_lifestyle_prompt(pilar, formato)
        
        if not self.model:
            return (
                "[Modo de Demonstração - Defina a variável GEMINI_API_KEY]\n\n"
                f"Tópico: {pilar.get('nome')}\n"
                f"Conflito: {pilar.get('dor')}\n"
                f"Ideal: {pilar.get('aspiracao')}\n\n"
                "Exemplo de narrativa: O silêncio da manhã não deveria ser privilégio de finais de semana. "
                "Quando o dia começa com luz natural e passos descalços na grama, o trabalho rende mais e o corpo agradece. "
                "A vida além do trânsito não é um luxo distante, é uma decisão de rota. Descubra o ritmo Saber."
            )

        resposta = self.model.generate_content(prompt)
        return resposta.text.strip()
