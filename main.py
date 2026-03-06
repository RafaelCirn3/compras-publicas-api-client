"""
Sistema de Busca de Processos de Compras Públicas
Ponto de entrada da aplicação
"""
from src.services import ProcessoService


def main():
    """Função principal da aplicação"""
    print("=" * 50)
    print("Sistema de Busca de Processos de Compras Públicas")
    print("=" * 50)
    print()
    
    # Inicializa o serviço
    servico = ProcessoService()
    
    try:
        print("Buscando processos...")
        
        # Busca e filtra processos
        resultado = servico.buscar_processos_relevantes()
        
        print(f"\nProcessos encontrados: {resultado['total']}")
        print(f"Processos relevantes: {resultado['quantidade_relevantes']}")
        
        if resultado['quantidade_relevantes'] > 0:
            print("\n" + "=" * 50)
            print("PROCESSOS RELEVANTES")
            print("=" * 50)
            servico.exibir_processos(resultado['relevantes'])
        else:
            print("\nNenhum processo relevante encontrado.")
    
    except Exception as e:
        print(f"\nErro ao buscar processos: {str(e)}")
        return 1
    
    print("\n" + "=" * 50)
    print("Busca finalizada!")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    exit(main())