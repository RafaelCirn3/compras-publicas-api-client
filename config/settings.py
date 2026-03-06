"""
Módulo de configuração do projeto.
Carrega variáveis de ambiente do arquivo .env
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
    
    # Configurações da API
    API_BASE_URL: str = os.getenv('API_BASE_URL', 'https://apipcp.portaldecompraspublicas.com.br/publico')
    PUBLIC_KEY: str = os.getenv('PUBLIC_KEY', 'SUA_PUBLIC_KEY_AQUI')
    
    # Configurações de busca
    UF: str = os.getenv('UF', 'PB')
    DIAS_BUSCA: int = int(os.getenv('DIAS_BUSCA', '30'))
    
    # Filtros
    KEYWORDS: List[str] = os.getenv('KEYWORDS', 'MATERIAL,ELETRICO').split(',')
    STATUS_ALVO: str = os.getenv('STATUS_ALVO', 'RECEBENDO PROPOSTAS')
    
    # Paginação
    PAGE_SIZE: int = int(os.getenv('PAGE_SIZE', '1'))


# Instância global das configurações
settings = Settings()
