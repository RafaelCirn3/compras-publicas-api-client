"""
Script de exemplo para exportar processos para CSV
Este é um exemplo de ferramenta auxiliar que pode ser criada na pasta tools/
"""
import csv
from datetime import datetime
from pathlib import Path


def exportar_para_csv(processos: list, nome_arquivo: str = None):
    """
    Exporta processos para um arquivo CSV
    
    Args:
        processos: Lista de processos
        nome_arquivo: Nome do arquivo (opcional)
    """
    if not nome_arquivo:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"processos_{timestamp}.csv"
    
    # Cria pasta exports se não existir
    exports_dir = Path(__file__).parent.parent / "exports"
    exports_dir.mkdir(exist_ok=True)
    
    filepath = exports_dir / nome_arquivo
    
    # Campos para exportar
    campos = ['orgao', 'objeto', 'valorEstimado', 'situacao', 'dataPublicacao']
    
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(processos)
    
    print(f"Arquivo exportado: {filepath}")
    return filepath


def main():
    """Exemplo de uso da ferramenta"""
    print("Ferramenta de Exportação de Processos")
    print("-" * 50)
    print("Forneça uma lista de processos para exportação usando exportar_para_csv().")


if __name__ == "__main__":
    main()
