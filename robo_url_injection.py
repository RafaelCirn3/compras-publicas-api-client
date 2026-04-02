"""
Bot RPA com URL-injection para busca de processos de compras públicas
Exemplo de URL:
https://www.portaldecompraspublicas.com.br/processos?pagina=1&uf=100125&status=1&objeto=Material%20El%C3%A9trico
"""
from src.services.url_injection_bot_service import UrlInjectionBotService


def main():
    """Função principal do bot RPA com URL-injection"""

    print("\n")
    print("╔" + "═" * 64 + "╗")
    print("║" + " " * 64 + "║")
    print("║" + "  BOT RPA - URL INJECTION".center(64) + "║")
    print("║" + "  Portal de Compras Públicas (query params)".center(64) + "║")
    print("║" + " " * 64 + "║")
    print("╚" + "═" * 64 + "╝")
    print("\n")

    try:
        servico_bot = UrlInjectionBotService(
            pagina=1,
            uf_codigo="100125",
            status_codigo="1",
            objeto="Material Elétrico"
        )

        resultado = servico_bot.executar_busca()
        servico_bot.exibir_resumo(resultado)

        if resultado.get("sucesso"):
            servico_bot.salvar_resultados(resultado, "processos_material_eletrico_url_injection.txt")
            print(f"URL utilizada: {resultado.get('url', 'N/A')}")

        return 0 if resultado.get("sucesso") else 1

    except Exception as e:
        print(f"\n✗ Erro crítico: {str(e)}\n")
        return 1


if __name__ == "__main__":
    exit(main())
