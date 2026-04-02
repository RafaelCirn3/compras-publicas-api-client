"""
Serviço principal de automação do bot RPA com URL-injection.
"""
from typing import Dict, Any
from src.utils.selenium_utils import SeleniumBot


class UrlInjectionBotService:
    """Pipeline principal para busca de processos via injeção de parâmetros na URL"""

    def __init__(
        self,
        uf_codigo: str | None = None,
        status_codigo: str | None = None,
        objeto: str | None = None,
        pagina: int = 1
    ):
        self.uf_codigo = uf_codigo
        self.status_codigo = status_codigo
        self.objeto = objeto
        self.pagina = pagina
        self.url_utilizada = ""
        self.bot = None
        self.processos_encontrados = []

    def executar_busca(self) -> Dict[str, Any]:
        """Executa a busca completa usando URL-injection"""
        try:
            self.bot = SeleniumBot()

            print("\n" + "=" * 60)
            print("INICIANDO BOT RPA - URL INJECTION")
            print("=" * 60)
            print(f"Página: {self.pagina}")
            print(f"UF (código): {self.uf_codigo}")
            print(f"Status (código): {self.status_codigo}")
            print(f"Objeto: {self.objeto}")
            print("=" * 60 + "\n")

            self.url_utilizada = self.bot.acessar_processos_com_url_injection(
                pagina=self.pagina,
                uf=self.uf_codigo,
                status=self.status_codigo,
                objeto=self.objeto
            )

            try:
                self.bot.aceitar_termos()
            except Exception:
                self.bot._log("Banner de termos não encontrado após URL-injection (seguindo fluxo)", "INFO")

            self.processos_encontrados = self.bot.extrair_processos(self.objeto)

            return {
                "sucesso": True,
                "total_processos": len(self.processos_encontrados),
                "processos": self.processos_encontrados,
                "uf": self.uf_codigo,
                "status": self.status_codigo,
                "palavra_chave": self.objeto,
                "pagina": self.pagina,
                "url": self.url_utilizada
            }

        except Exception as e:
            print(f"\n✗ Erro durante execução do bot (URL-injection): {str(e)}\n")

            if self.bot:
                print("\n" + "=" * 70)
                print("HISTÓRICO DE EXECUÇÃO:")
                print("=" * 70)
                self.bot.exibir_logs()

            return {
                "sucesso": False,
                "erro": str(e),
                "total_processos": len(self.processos_encontrados),
                "processos": self.processos_encontrados,
                "pagina": self.pagina,
                "url": self.url_utilizada
            }

        finally:
            if self.bot:
                self.bot.fechar()

    def exibir_resumo(self, resultado: Dict[str, Any]) -> None:
        """Exibe um resumo dos resultados no console"""
        print("\n" + "=" * 60)
        print("RESUMO DOS RESULTADOS")
        print("=" * 60)

        if resultado.get("sucesso"):
            print("✓ Busca realizada com sucesso!")
            print(f"Total de processos encontrados: {resultado['total_processos']}")
            print(f"UF: {resultado['uf']}")
            print(f"Status: {resultado['status']}")
            print(f"Palavra-chave: {resultado['palavra_chave']}")

            if resultado.get("processos"):
                print("\n" + "-" * 60)
                print("PROCESSOS ENCONTRADOS:")
                print("-" * 60)

                for idx, processo in enumerate(resultado["processos"], 1):
                    print(f"\n[{idx}] Processo:")
                    print(f"    Número: {processo.get('numero', 'N/A')}")
                    print(f"    Órgão: {processo.get('orgao', 'N/A')}")
                    print(f"    Objeto: {processo.get('objeto', 'N/A')}")
                    print(f"    Link: {processo.get('link', 'N/A')}")
            else:
                print("\n✗ Nenhum processo encontrado com os critérios especificados.")
        else:
            print(f"✗ Erro na busca: {resultado.get('erro', 'Erro desconhecido')}")

        print("\n" + "=" * 60 + "\n")

    def salvar_resultados(self, resultado: Dict[str, Any], arquivo: str = "processos_encontrados.txt") -> None:
        """Salva os resultados em um arquivo"""
        try:
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("RESULTADOS DA BUSCA RPA\n")
                f.write("=" * 60 + "\n\n")

                f.write(f"UF: {resultado.get('uf', 'N/A')}\n")
                f.write(f"Status: {resultado.get('status', 'N/A')}\n")
                f.write(f"Palavra-chave: {resultado.get('palavra_chave', 'N/A')}\n")
                f.write(f"Total de processos: {resultado.get('total_processos', 0)}\n\n")

                if resultado.get("processos"):
                    f.write("-" * 60 + "\n")
                    f.write("PROCESSOS ENCONTRADOS:\n")
                    f.write("-" * 60 + "\n\n")

                    for idx, processo in enumerate(resultado["processos"], 1):
                        f.write(f"[{idx}] Processo\n")
                        f.write(f"    Número: {processo.get('numero', 'N/A')}\n")
                        f.write(f"    Órgão: {processo.get('orgao', 'N/A')}\n")
                        f.write(f"    Objeto: {processo.get('objeto', 'N/A')}\n")
                        f.write(f"    Link: {processo.get('link', 'N/A')}\n\n")

                f.write("=" * 60 + "\n")

            print(f"✓ Resultados salvos em: {arquivo}")

        except Exception as e:
            print(f"✗ Erro ao salvar resultados: {str(e)}")