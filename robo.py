"""
Bot RPA para busca de processos de compras públicas
Automação Selenium - Sem necessidade de secret-key
Palavras-chave: PB, MATERIAL ELETRICO, RECEBENDO PROPOSTAS
"""
from src.services.bot_service import BotService


def main():
    """Função principal do bot RPA"""
    
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  BOT RPA - PORTAL DE COMPRAS PÚBLICAS".center(58) + "║")
    print("║" + "  Automação Selenium sem Secret-Key".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        # Configurações específicas para esta busca
        # Keywords: PB, MATERIAL ELETRICO, RECEBENDO PROPOSTAS
        servico_bot = BotService(
            uf="PB",
            status="RECEBENDO PROPOSTAS",
            palavra_chave="MATERIAL ELETRICO"
        )
        
        # Executa a busca
        resultado = servico_bot.executar_busca()
        
        # Exibe o resumo
        servico_bot.exibir_resumo(resultado)
        
        # Salva os resultados em arquivo
        if resultado.get('sucesso'):
            servico_bot.salvar_resultados(resultado, "processos_material_eletrico.txt")
        
        return 0 if resultado.get('sucesso') else 1
        
    except Exception as e:
        print(f"\n✗ Erro crítico: {str(e)}\n")
        return 1


if __name__ == "__main__":
    exit(main())
