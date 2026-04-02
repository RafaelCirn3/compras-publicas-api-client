"""
Utilitários para automação com Selenium
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urlencode, urlparse


class SeleniumBot:
    """Bot para automação do Portal de Compras Públicas"""
    
    def __init__(self, implicitly_wait: int = 10, timeout: int = 20):
        """
        Inicializa o driver do Selenium
        
        Args:
            implicitly_wait: Tempo de espera implícita em segundos
            timeout: Tempo máximo de espera para elementos em segundos
        """
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(implicitly_wait)
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, timeout)
        self.url_base = "https://www.portaldecompraspublicas.com.br"
        self.log_history = []
    
    def _log(self, mensagem: str, tipo: str = "INFO") -> None:
        """
        Registra uma mensagem de log com timestamp
        
        Args:
            mensagem: Mensagem a ser registrada
            tipo: Tipo de log (INFO, ERRO, XPATH, SUCESSO)
        """
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        prefixos = {
            "INFO": f"[{timestamp}] ℹ️ ",
            "ERRO": f"[{timestamp}] ✗ ",
            "XPATH": f"[{timestamp}] 🔍 ",
            "SUCESSO": f"[{timestamp}] ✓ ",
            "TENTATIVA": f"[{timestamp}] 🔄 "
        }
        
        prefixo = prefixos.get(tipo, f"[{timestamp}] ")
        msg_formatada = f"{prefixo}{mensagem}"
        print(msg_formatada)
        self.log_history.append(msg_formatada)
    
    def _encontrar_elemento(self, nome: str, seletores: List[tuple], tentativas_timeout: int = 5) -> Any:
        """
        Tenta encontrar um elemento usando múltiplos seletores com logs detalhados
        
        Args:
            nome: Nome descritivo do elemento
            seletores: Lista de tuplas (tipo_seletor, valor_seletor)
            tentativas_timeout: Timeout para espera do elemento
            
        Returns:
            Elemento encontrado ou None
            
        Raises:
            Exception: Se nenhum seletor funcionar
        """
        self._log(f"Buscando: {nome}", "INFO")
        
        for idx, (tipo, valor) in enumerate(seletores, 1):
            try:
                tipo_nome = tipo.name if hasattr(tipo, 'name') else str(tipo)
                self._log(f"Tentativa {idx}/{len(seletores)} - Tipo: {tipo_nome}", "XPATH")
                
                # Testa o seletor
                wait = WebDriverWait(self.driver, tentativas_timeout)
                elemento = wait.until(EC.presence_of_element_located((tipo, valor)))
                
                self._log(f"{nome} encontrado com sucesso! (tipo: {tipo_nome})", "SUCESSO")
                return elemento
                
            except Exception as e:
                erro_msg = str(e)
                tipo_nome = tipo.name if hasattr(tipo, 'name') else str(tipo)
                # Limita a mensagem de erro
                if len(erro_msg) > 150:
                    erro_msg = erro_msg[:150] + "..."
                self._log(f"Tentativa {idx}/{len(seletores)} ({tipo_nome}) falhou", "ERRO")
                continue
        
        # Se chegou aqui, nenhum seletor funcionou
        erro_completo = f"Nenhum seletor funcionou para '{nome}'. Seletores testados: {len(seletores)}"
        self._log(erro_completo, "ERRO")
        raise Exception(erro_completo)
    
    def _clicar_elemento(self, nome: str, seletores: List[tuple]) -> bool:
        """
        Encontra um elemento clicável e clica nele
        
        Args:
            nome: Nome descritivo do elemento
            seletores: Lista de tuplas (tipo_seletor, valor_seletor)
            
        Returns:
            True se conseguiu clicar, False caso contrário
        """
        try:
            self._log(f"Clicando em: {nome}", "INFO")
            
            for idx, (tipo, valor) in enumerate(seletores, 1):
                try:
                    tipo_nome = tipo.name if hasattr(tipo, 'name') else str(tipo)
                    wait = WebDriverWait(self.driver, self.timeout)
                    elemento = wait.until(EC.element_to_be_clickable((tipo, valor)))
                    elemento.click()
                    time.sleep(1)
                    
                    self._log(f"{nome} clicado com sucesso! (tipo: {tipo_nome})", "SUCESSO")
                    return True
                    
                except Exception as e:
                    erro_msg = str(e)[:100]
                    tipo_nome = tipo.name if hasattr(tipo, 'name') else str(tipo)
                    self._log(f"Clique {idx}/{len(seletores)} ({tipo_nome}) falhou", "ERRO")
                    continue
            
            self._log(f"Falha ao clicar em '{nome}' com todos os seletores", "ERRO")
            return False
            
        except Exception as e:
            self._log(f"Erro crítico ao clicar '{nome}': {str(e)[:100]}", "ERRO")
            return False

    def _aguardar_estabilizacao_resultados(self, contexto: str = "pesquisa", timeout: int = 30) -> None:
        """Aguarda o fim do carregamento e a estabilização dos resultados na tela."""
        self._log(f"Aguardando estabilização da tela após {contexto}...", "INFO")

        try:
            WebDriverWait(self.driver, min(timeout, 10)).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except Exception:
            self._log("document.readyState não confirmou 'complete' no tempo esperado", "INFO")

        seletores_loading = [
            (By.CSS_SELECTOR, ".loading"),
            (By.CSS_SELECTOR, ".spinner"),
            (By.CSS_SELECTOR, ".loader"),
            (By.CSS_SELECTOR, "ngx-spinner"),
            (By.CSS_SELECTOR, "[aria-busy='true']"),
            (By.XPATH, "//*[contains(@class,'loading') or contains(@class,'spinner') or contains(@class,'loader')]")
        ]

        inicio = time.time()
        ultimo_loading_visto_em = None
        loading_foi_visto = False

        while time.time() - inicio < timeout:
            total_loading_visivel = 0

            for tipo, seletor in seletores_loading:
                try:
                    elementos = self.driver.find_elements(tipo, seletor)
                    for elemento in elementos:
                        try:
                            if elemento.is_displayed():
                                total_loading_visivel += 1
                        except Exception:
                            continue
                except Exception:
                    continue

            if total_loading_visivel > 0:
                loading_foi_visto = True
                ultimo_loading_visto_em = time.time()
            else:
                if loading_foi_visto and ultimo_loading_visto_em and (time.time() - ultimo_loading_visto_em) >= 1.2:
                    break
                if not loading_foi_visto and (time.time() - inicio) >= 2.0:
                    break

            time.sleep(0.25)

        xpath_articles = "/html/body/app-root/div/main/app-process/main/div/section/section/section/article"
        xpath_paginacao = "/html/body/app-root/div/main/app-process/main/div/section/section/div/app-pagination"
        xpath_sem_resultado = "//*[contains(translate(text(), 'NENHUMRESULTADO', 'nenhumresultado'), 'nenhum') and contains(translate(text(), 'PROCESSO', 'processo'), 'processo')]"

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: (
                    len(d.find_elements(By.XPATH, xpath_articles)) > 0
                    or len(d.find_elements(By.XPATH, xpath_paginacao)) > 0
                    or len(d.find_elements(By.XPATH, xpath_sem_resultado)) > 0
                )
            )
            self._log(f"Tela estabilizada após {contexto}", "SUCESSO")
        except Exception:
            self._log(
                f"Tempo de estabilização após {contexto} excedido; seguindo com o que estiver renderizado",
                "INFO"
            )
    
    def acessar_portal(self) -> None:
        """Acessa a página inicial do portal"""
        try:
            self._log("Acessando Portal de Compras Públicas...", "INFO")
            self.driver.get(self.url_base)
            time.sleep(2)
            self._log(f"Portal carregado: {self.url_base}", "SUCESSO")
        except Exception as e:
            self._log(f"Erro ao acessar portal: {str(e)}", "ERRO")
            raise

    def acessar_processos_com_url_injection(
        self,
        pagina: int = 1,
        uf: str | None = None,
        status: str | None = None,
        objeto: str | None = None,
    ) -> str:
        """
        Acessa diretamente a listagem de processos usando query params (URL-injection).

        Args:
            pagina: Número da página inicial
            uf: Código numérico da UF no portal
            status: Código numérico do status no portal
            objeto: Texto do objeto para filtro

        Returns:
            URL final utilizada na navegação
        """
        try:
            self._log("Montando URL com filtros (URL-injection)...", "INFO")

            params = {"pagina": pagina}

            opcionais = {
                "uf": uf,
                "status": status,
                "objeto": objeto,
            }
            for chave, valor in opcionais.items():
                if valor is not None and str(valor).strip() != "":
                    params[chave] = valor

            query_string = urlencode(params)
            url = f"{self.url_base}/processos?{query_string}"

            self._log(f"Acessando URL injetada: {url}", "INFO")
            self.driver.get(url)
            self._aguardar_estabilizacao_resultados(contexto="acesso por URL-injection", timeout=35)

            self._log("Página de processos carregada via URL-injection", "SUCESSO")
            return url
        except Exception as e:
            self._log(f"Erro ao acessar processos via URL-injection: {str(e)}", "ERRO")
            raise
    
    def aceitar_termos(self) -> None:
        """Aceita os termos do portal clicando no botão de aceitar"""
        try:
            self._log("Aceitando termos do portal...", "INFO")
            
            seletores = [
                (By.ID, "adopt-accept-all-button"),
                (By.XPATH, "//button[@id='adopt-accept-all-button']"),
                (By.CSS_SELECTOR, "button#adopt-accept-all-button"),
            ]
            
            if self._clicar_elemento("Botão de aceitar termos", seletores):
                self._log("Termos aceitos com sucesso", "SUCESSO")
            else:
                raise Exception("Não foi possível aceitar os termos")
                
        except Exception as e:
            self._log(f"Erro ao aceitar termos: {str(e)}", "ERRO")
            raise
    
    def selecionar_uf(self, uf: str = "PB") -> None:
        """
        Seleciona a UF no dropdown
        
        Args:
            uf: Estado a ser selecionado (ex: PB, SP)
        """
        try:
            self._log(f"Selecionando UF: {uf}...", "INFO")
            
            # XPath exato do botão dropdown (fornecido pelo usuário)
            seletores_button = [
                (By.XPATH, "/html/body/app-root/div/main/app-home/main/div/app-hero/section/div/div[1]/app-filter-principal/div[1]/div[1]/div[3]/div[1]/div[1]/button"),
                (By.XPATH, "//div[@class*='uf-dropdown']//button"),
                (By.XPATH, "//button[contains(@class, 'uf')]"),
            ]
            
            if not self._clicar_elemento("Botão dropdown UF", seletores_button):
                raise Exception("Não conseguiu clicar no botão dropdown de UF")
            
            time.sleep(1)
            
            # XPath exato do input (fornecido pelo usuário)
            seletores_input = [
                (By.XPATH, "/html/body/app-root/div/main/app-home/main/div/app-filter-principal/div[1]/div[1]/div[3]/div[1]/div[1]/ul/li[1]/input"),
                (By.XPATH, "//div[@class*='uf-dropdown']//input"),
                (By.CSS_SELECTOR, ".uf-dropdown input"),
            ]
            
            uf_input = self._encontrar_elemento("Campo de input UF", seletores_input)
            uf_input.clear()
            uf_input.send_keys(uf)
            time.sleep(1)
            self._log(f"UF '{uf}' digitada no campo", "SUCESSO")
            
            # XPath exato da opção UF (fornecido pelo usuário)
            seletores_opcao = [
                (By.XPATH, "/html/body/app-root/div/main/app-home/main/div/app-filter-principal/div[1]/div[1]/div[3]/div[1]/div[1]/ul/li[2]/button"),
                (By.XPATH, f"//div[@class*='uf-dropdown']//button[contains(text(), '{uf}')]"),
                (By.XPATH, f"//li//button[contains(text(), '{uf}')]"),
            ]
            
            if self._clicar_elemento(f"Opção {uf}", seletores_opcao):
                self._log(f"UF {uf} selecionada com sucesso", "SUCESSO")
            else:
                raise Exception(f"Não conseguiu selecionar a opção {uf}")
            
        except Exception as e:
            self._log(f"Erro ao selecionar UF: {str(e)}", "ERRO")
            self._log(f"Estado da página: {len(self.driver.page_source)} caracteres", "INFO")
            raise
    
    def abrir_busca_avancada(self) -> None:
        """Abre o formulário de busca avançada"""
        try:
            self._log("Abrindo busca avançada...", "INFO")
            
            seletores = [
                (By.XPATH, "/html/body/app-root/div/main/app-home/main/div/app-hero/section/div/div[1]/app-filter-principal/div[1]/div[2]/button"),
                (By.XPATH, "//button[contains(text(), 'Busca Avançada') or contains(text(), 'busca avançada')]"),
                (By.XPATH, "//button[@class*='advanced']"),
                (By.XPATH, "//div[@class*='hero-content']//button[2]"),
            ]
            
            if self._clicar_elemento("Botão busca avançada", seletores):
                self._log("Busca avançada aberta", "SUCESSO")
            else:
                raise Exception("Não conseguiu abrir busca avançada")
                
        except Exception as e:
            self._log(f"Erro ao abrir busca avançada: {str(e)}", "ERRO")
            raise
    
    def selecionar_status(self, status: str = "RECEBENDO PROPOSTAS") -> None:
        """
        Seleciona o status desejado
        
        Args:
            status: Status a ser selecionado
        """
        try:
            self._log(f"Selecionando status: {status}...", "INFO")
            
            # Clica no botão dropdown de status
            seletores_status = [
                (By.XPATH, "/html/body/app-root/div/main/app-home/main/div/app-hero/section/div/div[1]/app-filter-principal/div[1]/div[2]/div/div[1]/div[1]/button"),
                (By.XPATH, "//div[@class*='status-dropdown']//button"),
                (By.CSS_SELECTOR, ".status-dropdown button"),
                (By.XPATH, "//button[contains(@class, 'status')]"),
            ]
            
            if not self._clicar_elemento("Botão dropdown Status", seletores_status):
                raise Exception("Não conseguiu clicar no botão dropdown de status")
            
            time.sleep(1)
            
            # Clica na opção de status
            seletores_opcao = [
                (By.XPATH, f"//button[contains(text(), '{status}') or contains(text(), 'Recebendo')]"),
                (By.XPATH, "//div[@class*='status-dropdown']//li[2]//button"),
                (By.XPATH, f"//li//button[contains(text(), '{status}')]"),
            ]
            
            if self._clicar_elemento(f"Opção {status}", seletores_opcao):
                self._log(f"Status '{status}' selecionado com sucesso", "SUCESSO")
            else:
                raise Exception(f"Não conseguiu selecionar status '{status}'")
            
        except Exception as e:
            self._log(f"Erro ao selecionar status: {str(e)}", "ERRO")
            raise
    
    def preencher_palavra_chave(self, palavra: str = "Material Elétrico") -> None:
        """
        Preenche o campo de palavra-chave
        
        Args:
            palavra: Palavra-chave a ser preenchida
        """
        try:
            self._log(f"Preenchendo palavra-chave: '{palavra}'...", "INFO")
            
            seletores = [
                (By.XPATH, "//*[@id='objeto']"),
                (By.ID, "objeto"),
                (By.XPATH, "//input[@id='objeto']"),
            ]
            
            keyword_input = self._encontrar_elemento("Campo de palavra-chave", seletores)
            keyword_input.clear()
            keyword_input.send_keys(palavra)
            time.sleep(1)
            
            self._log(f"Palavra-chave preenchida: '{palavra}'", "SUCESSO")
            
        except Exception as e:
            self._log(f"Erro ao preencher palavra-chave: {str(e)}", "ERRO")
            raise
    
    def clicar_pesquisar(self) -> None:
        """Clica no botão de pesquisa para aplicar os filtros"""
        try:
            self._log("Clicando em pesquisar para aplicar filtros...", "INFO")
            
            # XPath exato do botão de pesquisa dentro dos filtros
            seletores = [
                (By.XPATH, "/html/body/app-root/div/main/app-process/main/div/div/section/app-filter-principal/div[1]/div[1]/div[3]/div[2]/button[2]"),
                (By.XPATH, "//button[contains(@class, 'btn-search') or contains(text(), 'Pesquisar')]"),
                (By.XPATH, "//button[@class*='search']"),
                (By.CSS_SELECTOR, ".btn-search"),
            ]
            
            if self._clicar_elemento("Botão pesquisar/filtro", seletores):
                seletores_popup = [
                    (By.XPATH, "/html/body/app-root/div/main/app-process/main/div/app-alert-register/div/div[1]/button"),
                ]
                time.sleep(3)
                if self._clicar_elemento("Botão fechar popup", seletores_popup):
                    self._log("Popup fechado com sucesso", "SUCESSO")
                else:
                    self._log("Popup não encontrado após pesquisar (seguindo fluxo)", "INFO")

                self._aguardar_estabilizacao_resultados(contexto="clicar em pesquisar", timeout=35)
                self._log("Pesquisa executada com sucesso", "SUCESSO")
            else:
                raise Exception("Não conseguiu clicar no botão pesquisar")
                
        except Exception as e:
            self._log(f"Erro ao clicar em pesquisar: {str(e)}", "ERRO")
            raise

    def _extrair_processos_da_pagina(self, palavra_chave: str, pagina_atual: int) -> List[Dict[str, Any]]:
        """Extrai processos da página atual de resultados"""
        processos_pagina = []
        
        # Procura pelos articles na estrutura correta
        xpath_articles = "/html/body/app-root/div/main/app-process/main/div/section/section/section/article"
        articles = self.driver.find_elements(By.XPATH, xpath_articles)

        self._log(f"Página {pagina_atual}: {len(articles)} artigos encontrados no XPath correto", "INFO")

        for idx, article in enumerate(articles, 1):
            try:
                # Extrai a descrição/objeto do artigo de div/div[2]/p
                try:
                    descricao_element = article.find_element(By.XPATH, "./div/div[2]/p")
                    descricao = descricao_element.text
                except Exception:
                    descricao = "N/A"

                # Verifica se contém a palavra-chave na descrição
                if palavra_chave.upper() not in descricao.upper():
                    continue

                # Extrai o link do botão em footer/app-button-pill/button
                try:
                    botao = article.find_element(By.XPATH, "./footer/app-button-pill/button")
                    link_bruto = botao.get_attribute('routerlink') or botao.get_attribute('href')
                    if link_bruto:
                        link_bruto = link_bruto.strip()
                        parsed_link = urlparse(link_bruto)
                        if parsed_link.scheme and parsed_link.scheme not in {"http", "https"}:
                            link = None
                        elif not parsed_link.scheme and not parsed_link.netloc and not link_bruto.startswith("//"):
                            link = link_bruto
                        else:
                            link = None
                    else:
                        link = None
                except Exception:
                    link = None

                # Tenta extrair número/referência do artigo
                try:
                    numero_element = article.find_element(By.XPATH, "./div/div[1]//strong | ./div//h3 | ./div//h2")
                    numero = numero_element.text
                except Exception:
                    numero = f"Artigo_{idx}"

                # Tenta extrair órgão/publisher
                try:
                    orgao_element = article.find_element(By.XPATH, "./div/div[1]//span | ./div//p")
                    orgao = orgao_element.text
                except Exception:
                    orgao = "N/A"

                # Constrói o objeto do processo
                processo = {
                    'numero': numero,
                    'orgao': orgao,
                    'objeto': descricao,
                    'palavraChave': palavra_chave,
                    'link': link,
                }

                processos_pagina.append(processo)
                self._log(f"Página {pagina_atual} - Artigo {idx} com palavra-chave encontrado: {numero}", "SUCESSO")

            except Exception as e:
                self._log(f"Página {pagina_atual} - Erro ao processar artigo {idx}: {str(e)[:80]}", "ERRO")
                continue

        self._log(
            f"Página {pagina_atual}: {len(processos_pagina)} processos com '{palavra_chave}'",
            "INFO"
        )
        return processos_pagina

    def _ir_para_proxima_pagina(self) -> bool:
        """Rola até o botão de próxima página e clica; retorna False quando não houver próxima"""
        xpath_proxima = "/html/body/app-root/div/main/app-process/main/div/section/section/div/app-pagination/div/button[7]"
        try:
            self._log("Paginação: aguardando processamento antes do scroll (5s)", "INFO")
            time.sleep(5)

            posicao_inicial = self.driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || 0;")
            altura_total = self.driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")
            self._log(
                f"Paginação: posição inicial de scroll = {int(posicao_inicial)}px | altura da página = {int(altura_total)}px",
                "INFO"
            )

            # Scroll lento de 5 segundos para facilitar reconhecimento/renderização do elemento
            duracao_scroll = 5.0
            passos = 50  # Aumentado para scroll mais suave e deslizante
            delay_por_passo = duracao_scroll / passos

            self._log("Paginação: iniciando scroll deslizante de 5s até 70%", "INFO")
            for passo in range(1, passos + 1):
                percentual = passo / passos
                # Rola até 70% da página de forma progressiva e fluida
                self.driver.execute_script(
                    "window.scrollTo(0, Math.floor((document.body.scrollHeight * 0.70) * arguments[0]));",
                    percentual
                )
                time.sleep(delay_por_passo)

            posicao_apos_scroll = self.driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || 0;")
            self._log(
                f"Paginação: scroll lento concluído (de {int(posicao_inicial)}px para {int(posicao_apos_scroll)}px)",
                "SUCESSO"
            )

            botoes = self.driver.find_elements(By.XPATH, xpath_proxima)
            self._log(f"Paginação: botões encontrados com XPath full = {len(botoes)}", "INFO")
            if not botoes:
                self._log("Botão de próxima página não encontrado. Fim da paginação.", "INFO")
                return False

            botao = botoes[0]
            if not botao.is_displayed() or not botao.is_enabled():
                self._log("Botão de próxima página indisponível. Fim da paginação.", "INFO")
                return False

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
            time.sleep(0.8)
            posicao_no_botao = self.driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || 0;")
            self._log(
                f"Paginação: scrollIntoView no botão executado. Posição atual = {int(posicao_no_botao)}px",
                "INFO"
            )

            self.driver.execute_script("arguments[0].click();", botao)
            self._log("Próxima página acionada", "SUCESSO")
            self._aguardar_estabilizacao_resultados(contexto="avançar para próxima página", timeout=30)
            return True

        except Exception as e:
            self._log(f"Não foi possível avançar de página: {str(e)[:120]}", "INFO")
            return False
    
    def extrair_processos(self, palavra_chave: str = "MATERIAL ELETRICO") -> List[Dict[str, Any]]:
        """
        Extrai os dados dos processos encontrados
        
        Args:
            palavra_chave: Palavra-chave para filtrar resultados
            
        Returns:
            Lista de processos encontrados com a palavra-chave
        """
        try:
            self._log(f"Extraindo processos com '{palavra_chave}' em todas as páginas...", "INFO")

            processos: List[Dict[str, Any]] = []
            vistos = set()
            pagina_atual = 1

            while True:
                processos_pagina = self._extrair_processos_da_pagina(palavra_chave, pagina_atual)

                novos = 0
                for processo in processos_pagina:
                    chave = (
                        processo.get('numero', 'N/A'),
                        processo.get('orgao', 'N/A'),
                        processo.get('objeto', 'N/A')
                    )
                    if chave not in vistos:
                        vistos.add(chave)
                        processos.append(processo)
                        novos += 1

                self._log(f"Página {pagina_atual}: {novos} novos processos adicionados", "INFO")

                if not self._ir_para_proxima_pagina():
                    break

                pagina_atual += 1

            print("\n" + "=" * 60)
            print("RESUMO DA PAGINAÇÃO")
            print("=" * 60)
            print(f"Total de páginas consultadas: {pagina_atual}")
            print(f"Total de processos únicos encontrados: {len(processos)}")
            print(f"Filtro utilizado: {palavra_chave}")
            print("=" * 60 + "\n")

            self._log(f"Total de processos com '{palavra_chave}': {len(processos)}", "SUCESSO")
            return processos
            
        except Exception as e:
            self._log(f"Erro ao extrair processos: {str(e)}", "ERRO")
            return []
    
    def fechar(self) -> None:
        """Fecha o navegador"""
        try:
            self._log("Fechando navegador...", "INFO")
            if self.driver:
                self.driver.quit()
            self._log("Navegador fechado", "SUCESSO")
        except Exception as e:
            self._log(f"Erro ao fechar navegador: {str(e)}", "ERRO")
    
    def exibir_logs(self) -> None:
        """Exibe todos os logs registrados durante a execução"""
        print("\n" + "="*70)
        print("HISTÓRICO DE LOGS")
        print("="*70)
        for log in self.log_history:
            print(log)
        print("="*70 + "\n")
