# src/utils.py
import unicodedata
import re

def slugify(texto: str) -> str:
    """
    Transforma texto em slug URL-friendly de forma segura.
    Garante que não haverá espaços duplos ou underlines sobrando nas bordas.
    Ex: ' Jardim   Amstalden ' -> 'jardim_amstalden'
    """
    if not isinstance(texto, str):
        return ""
    
    # Remove espaços nas pontas e normaliza acentos
    texto = texto.strip()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    
    # Substitui qualquer combinação de espaços, barras ou hífens por um único espaço
    texto = re.sub(r'[\s/\\-]+', ' ', texto)
    
    # Remove todos os caracteres que não sejam letras, números ou espaços
    texto = re.sub(r'[^a-z0-9 ]', '', texto)
    
    # Troca o espaço restante por underline
    texto = texto.replace(" ", "_")
    
    # Garante que o slug resultante não tenha underlines nas bordas
    return texto.strip('_')
