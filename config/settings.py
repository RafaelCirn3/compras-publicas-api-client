"""
Módulo de configuração do projeto.
Carrega variáveis de ambiente do arquivo .env.
"""
import os
from pathlib import Path
from typing import List


# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Tenta carregar o python-dotenv se disponível
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    print("Aviso: python-dotenv não instalado. Usando variáveis de ambiente do sistema.")


class Settings:
    """Configurações da aplicação"""

    UF: str = os.getenv('UF', 'PB')
    KEYWORDS: List[str] = [
        palavra.strip()
        for palavra in os.getenv('KEYWORDS', 'MATERIAL,ELETRICO').split(',')
        if palavra.strip()
    ]
    STATUS_ALVO: str = os.getenv('STATUS_ALVO', 'RECEBENDO PROPOSTAS')
    SELENIUM_TIMEOUT: int = int(os.getenv('SELENIUM_TIMEOUT', '20'))
    SELENIUM_IMPLICITLY_WAIT: int = int(os.getenv('SELENIUM_IMPLICITLY_WAIT', '10'))


# Instância global das configurações
settings = Settings()
