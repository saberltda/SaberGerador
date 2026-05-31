# src/config.py
import datetime

class GenesisConfig:
    VERSION = "GERADOR V.72 (FREE-TEXT GENERATIVE MODE)"

    # =====================================================
    # CONFIGURAÇÃO CRÍTICA DE FUSO HORÁRIO
    # =====================================================
    TZ_BRASILIA = datetime.timezone(datetime.timedelta(hours=-3))
    FUSO_PADRAO = "-03:00"

    # Cores e URLs do Sistema
    COLOR_PRIMARY = "#003366"
    COLOR_ACTION  = "#28a745"
    BLOG_URL = "https://saber.imb.br/blog"
