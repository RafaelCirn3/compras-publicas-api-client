"""
Cliente para API do Portal de Compras Públicas
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, Any
from config import settings


class ApiClient:
    """Cliente para interação com a API de processos de compras públicas"""
    
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.public_key = settings.PUBLIC_KEY
        self.uf = settings.UF
        self.dias_busca = settings.DIAS_BUSCA
    
    def buscar_processos(self, pagina: int = 1) -> Dict[str, Any]:
        """
        Busca processos abertos na API
        
        Args:
            pagina: Número da página para paginação
            
        Returns:
            Dicionário com os dados retornados pela API
            
        Raises:
            Exception: Se houver erro na requisição
        """
        data_fim = datetime.today()
        data_inicio = data_fim - timedelta(days=self.dias_busca)
        
        params = {
            "publicKey": self.public_key,
            "dataInicio": data_inicio.strftime("%Y-%m-%d"),
            "dataFim": data_fim.strftime("%Y-%m-%d"),
            "uf": self.uf,
            "pagina": pagina
        }
        
        url = f"{self.base_url}/processosabertos"
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição à API: {str(e)}")
