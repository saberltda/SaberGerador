import unicodedata
import re

def slugify(value: str) -> str:
    """Normaliza strings removendo acentos e convertendo para slug URL-friendly."""
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-')
