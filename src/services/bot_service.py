"""
Serviço de automação do bot RPA
"""
from typing import Dict, Any
from src.utils.selenium_utils import SeleniumBot
from config import settings


class BotService:
    """Serviço para automação de busca de processos com Selenium"""
    
    def __init__(self, uf: str = None, status: str = None, palavra_chave: str = None):
        """
        Inicializa o serviço de bot
        
        Args:
            uf: Unidade Federativa (padrão: settings.UF)
            status: Status dos processos (padrão: settings.STATUS_ALVO)
            palavra_chave: Palavra-chave para busca (padrão: primeira do settings.KEYWORDS)
        """
        self.uf = uf or settings.UF
        self.status = status or settings.STATUS_ALVO
        self.palavra_chave = palavra_chave or " ".join(settings.KEYWORDS)
        self.bot = None
        self.processos_encontrados = []
    
    def executar_busca(self) -> Dict[str, Any]:
        """
        Executa a busca completa no portal
        
        Returns:
            Dicionário com resultados da busca
        """
        try:
            # Inicializa o bot
            self.bot = SeleniumBot()
            
            print("\n" + "=" * 60)
            print("INICIANDO BOT RPA")
            print("=" * 60)
            print(f"UF: {self.uf}")
            print(f"Status: {self.status}")
            print(f"Palavra-chave: {self.palavra_chave}")
            print("=" * 60 + "\n")
            
            # Acessa o portal
            self.bot.acessar_portal()
            
            # Aceita os termos
            self.bot.aceitar_termos()
            
            # Seleciona a UF
            self.bot.selecionar_uf(self.uf)
            
            # Abre busca avançada
            self.bot.abrir_busca_avancada()

            # Preenche o campo objeto na busca avançada
            self.bot.preencher_palavra_chave("Material Elétrico")
            
            # Seleciona o status
            self.bot.selecionar_status(self.status)
            
            # Clica em pesquisar
            self.bot.clicar_pesquisar()
            
            # Extrai os processos
            self.processos_encontrados = self.bot.extrair_processos(self.palavra_chave)
            
            return {
                'sucesso': True,
                'total_processos': len(self.processos_encontrados),
                'processos': self.processos_encontrados,
                'uf': self.uf,
                'status': self.status,
                'palavra_chave': self.palavra_chave
            }
            
        except Exception as e:
            print(f"\n✗ Erro durante execução do bot: {str(e)}\n")
            
            # Exibe o histórico de logs para debug
            if self.bot:
                print("\n" + "="*70)
                print("HISTÓRICO DE EXECUÇÃO:")
                print("="*70)
                self.bot.exibir_logs()
            
            return {
                'sucesso': False,
                'erro': str(e),
                'total_processos': len(self.processos_encontrados),
                'processos': self.processos_encontrados
            }
        
        finally:
            # Fecha o navegador
            if self.bot:
                self.bot.fechar()
    
    def exibir_resumo(self, resultado: Dict[str, Any]) -> None:
        """
        Exibe um resumo dos resultados no console
        
        Args:
            resultado: Dicionário com resultados da busca
        """
        print("\n" + "=" * 60)
        print("RESUMO DOS RESULTADOS")
        print("=" * 60)
        
        if resultado.get('sucesso'):
            print("✓ Busca realizada com sucesso!")
            print(f"Total de processos encontrados: {resultado['total_processos']}")
            print(f"UF: {resultado['uf']}")
            print(f"Status: {resultado['status']}")
            print(f"Palavra-chave: {resultado['palavra_chave']}")
            
            if resultado['processos']:
                print("\n" + "-" * 60)
                print("PROCESSOS ENCONTRADOS:")
                print("-" * 60)
                
                for idx, processo in enumerate(resultado['processos'], 1):
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
        """
        Salva os resultados em um arquivo
        
        Args:
            resultado: Dicionário com resultados
            arquivo: Caminho do arquivo para salvar
        """
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("RESULTADOS DA BUSCA RPA\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"UF: {resultado.get('uf', 'N/A')}\n")
                f.write(f"Status: {resultado.get('status', 'N/A')}\n")
                f.write(f"Palavra-chave: {resultado.get('palavra_chave', 'N/A')}\n")
                f.write(f"Total de processos: {resultado.get('total_processos', 0)}\n\n")
                
                if resultado.get('processos'):
                    f.write("-" * 60 + "\n")
                    f.write("PROCESSOS ENCONTRADOS:\n")
                    f.write("-" * 60 + "\n\n")
                    
                    for idx, processo in enumerate(resultado['processos'], 1):
                        f.write(f"[{idx}] Processo\n")
                        f.write(f"    Número: {processo.get('numero', 'N/A')}\n")
                        f.write(f"    Órgão: {processo.get('orgao', 'N/A')}\n")
                        f.write(f"    Objeto: {processo.get('objeto', 'N/A')}\n")
                        f.write(f"    Link: {processo.get('link', 'N/A')}\n\n")
                
                f.write("=" * 60 + "\n")
            
            print(f"✓ Resultados salvos em: {arquivo}")
            
        except Exception as e:
            print(f"✗ Erro ao salvar resultados: {str(e)}")
