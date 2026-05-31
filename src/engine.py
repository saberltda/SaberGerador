# src/engine.py

class GenesisEngine:
    """
    O 'Cérebro' (Modo Livre).
    Coleta as strings generativas do usuário e empacota para o Prompt.
    """
    
    def __init__(self, data_manager):
        self.data = data_manager

    def run(self, user_inputs):
        bairro_nome = user_inputs.get('bairro_nome', 'FORCE_CITY_MODE')
        
        # Resolve o objeto do bairro para garantir a zona geográfica correta
        if bairro_nome == "FORCE_CITY_MODE":
            bairro_obj = {"nome": "Indaiatuba", "zona_normalizada": "urbana", "slug": "indaiatuba"}
        else:
            bairro_obj = next((b for b in self.data.bairros if b['nome'] == bairro_nome), None)
            if not bairro_obj:
                bairro_obj = {"nome": "Indaiatuba", "zona_normalizada": "urbana", "slug": "indaiatuba"}

        # Pacote direto com os textos livres
        final_package = {
            "bairro": bairro_obj,
            "contexto": user_inputs.get('contexto'),
            "ativo": user_inputs.get('ativo'),
            "persona": user_inputs.get('persona'),
            "gatilho": user_inputs.get('gatilho'),
            "topico": user_inputs.get('topico'),
            "formato": user_inputs.get('formato'),
            "dicas": user_inputs.get('dicas')
        }

        return final_package
