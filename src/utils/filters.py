"""
Módulo de filtros e utilitários
"""
from typing import List
from config import settings


def contem_palavra(texto: str) -> bool:
    """
    Verifica se o texto contém alguma das palavras-chave configuradas
    
    Args:
        texto: Texto a ser verificado
        
    Returns:
        True se contém alguma palavra-chave, False caso contrário
    """
    texto = texto.upper()
    
    for palavra in settings.KEYWORDS:
        if palavra.upper() in texto:
            return True
    
    return False


def filtrar_processos(lista: List[dict]) -> List[dict]:
    """
    Filtra processos com base nas palavras-chave e status
    
    Args:
        lista: Lista de processos para filtrar
        
    Returns:
        Lista de processos filtrados
    """
    relevantes = []
    
    for processo in lista:
        descricao = processo.get("objeto", "")
        status = processo.get("situacao", "")
        
        # Verifica se o status é o esperado
        if settings.STATUS_ALVO not in status.upper():
            continue
        
        # Verifica se contém palavras-chave
        if contem_palavra(descricao):
            relevantes.append(processo)
    
    return relevantes
