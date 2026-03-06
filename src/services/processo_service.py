"""
Serviço de processos de compras públicas
"""
from typing import List, Dict, Any
from src.api import ApiClient
from src.utils import filtrar_processos


class ProcessoService:
    """Serviço para gerenciar a busca e filtragem de processos"""
    
    def __init__(self):
        self.api_client = ApiClient()
    
    def buscar_processos_relevantes(self, pagina: int = 1) -> Dict[str, Any]:
        """
        Busca e filtra processos relevantes
        
        Args:
            pagina: Número da página
            
        Returns:
            Dicionário contendo processos totais e relevantes
        """
        # Busca processos na API
        dados = self.api_client.buscar_processos(pagina)
        processos = dados.get("data", [])
        
        # Filtra processos relevantes
        relevantes = filtrar_processos(processos)
        
        return {
            "total": len(processos),
            "relevantes": relevantes,
            "quantidade_relevantes": len(relevantes)
        }
    
    def exibir_processos(self, processos: List[Dict[str, Any]]) -> None:
        """
        Exibe processos formatados no console
        
        Args:
            processos: Lista de processos para exibir
        """
        for p in processos:
            print("\n" + "=" * 50)
            print(f"Órgão: {p.get('orgao', 'N/A')}")
            print(f"Objeto: {p.get('objeto', 'N/A')}")
            print(f"Valor estimado: {p.get('valorEstimado', 'N/A')}")
            print(f"Status: {p.get('situacao', 'N/A')}")
