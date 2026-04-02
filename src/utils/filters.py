"""
Módulo de filtros e utilitários
"""
from typing import List


def contem_palavra(texto: str, keywords: list[str] | None = None) -> bool:
    """
    Verifica se o texto contém alguma das palavras-chave informadas.
    
    Args:
        texto: Texto a ser verificado
        keywords: Lista de palavras-chave enviadas pelo usuário
        
    Returns:
        True se contém alguma palavra-chave, False caso contrário
    """
    if not keywords:
        return False

    texto = texto.upper()

    for palavra in keywords:
        if palavra.upper() in texto:
            return True
    
    return False


def filtrar_processos(
    lista: List[dict],
    keywords: list[str] | None = None,
    status_alvo: str | None = None,
) -> List[dict]:
    """
    Filtra processos com base nas palavras-chave e status enviados pelo usuário.
    
    Args:
        lista: Lista de processos para filtrar
        keywords: Lista de palavras-chave enviadas pelo usuário
        status_alvo: Status alvo enviado pelo usuário
        
    Returns:
        Lista de processos filtrados
    """
    relevantes = []
    
    for processo in lista:
        descricao = processo.get("objeto", "")
        status = (processo.get("situacao", "") or "").upper()

        # Só aplica filtro de status quando o usuário informou
        if status_alvo and status_alvo.upper() not in status:
            continue

        # Só aplica filtro por palavra-chave quando o usuário informou
        if keywords and not contem_palavra(descricao, keywords=keywords):
            continue

        relevantes.append(processo)
    
    return relevantes
