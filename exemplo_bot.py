"""
EXEMPLOS de uso do Bot RPA

Este arquivo contém exemplos de como usar a BotService
para diferentes casos de uso e personalizações.

Não execute este arquivo diretamente - use como referência.
"""

from src.services.bot_service import BotService


# ============================================================
# EXEMPLO 1: Busca padrão (PB - MATERIAL ELETRICO)
# ============================================================
def exemplo_busca_padrao():
    """Busca padrão conforme configurado em robo.py"""
    servico = BotService(
        uf="PB",
        status="RECEBENDO PROPOSTAS",
        palavra_chave="MATERIAL ELETRICO"
    )
    
    resultado = servico.executar_busca()
    servico.exibir_resumo(resultado)
    servico.salvar_resultados(resultado, "resultados_pb_material.txt")


# ============================================================
# EXEMPLO 2: Busca em outro estado (SP)
# ============================================================
def exemplo_busca_sp():
    """Busca de processos em São Paulo"""
    servico = BotService(
        uf="SP",
        status="RECEBENDO PROPOSTAS",
        palavra_chave="INFRAESTRUTURA"
    )
    
    resultado = servico.executar_busca()
    servico.exibir_resumo(resultado)


# ============================================================
# EXEMPLO 3: Busca com múltiplas palavras-chave
# ============================================================
def exemplo_busca_multiplas_palavras():
    """Busca com múltiplas palavras-chave"""
    # Fazer buscas sequenciais para diferentes palavras-chave
    palavras = ["MATERIAL ELETRICO", "CONSTRUÇÃO", "CONSULTORIA"]
    resultados_totais = []
    
    for palavra in palavras:
        print(f"\n\n{'='*60}")
        print(f"Buscando: {palavra}")
        print(f"{'='*60}")
        
        servico = BotService(
            uf="PB",
            status="RECEBENDO PROPOSTAS",
            palavra_chave=palavra
        )
        
        resultado = servico.executar_busca()
        servico.exibir_resumo(resultado)
        
        if resultado.get('processos'):
            resultados_totais.extend(resultado['processos'])
    
    print(f"\n\nTotal de processos encontrados: {len(resultados_totais)}")


# ============================================================
# EXEMPLO 4: Busca em múltiplos estados
# ============================================================
def exemplo_busca_multiplos_estados():
    """Busca em vários estados"""
    estados = ["PB", "PE", "BA"]
    
    for uf in estados:
        print(f"\n\n{'='*60}")
        print(f"Buscando em: {uf}")
        print(f"{'='*60}")
        
        servico = BotService(
            uf=uf,
            status="RECEBENDO PROPOSTAS",
            palavra_chave="MATERIAL ELETRICO"
        )
        
        resultado = servico.executar_busca()
        servico.exibir_resumo(resultado)
        
        # Salva com nome por estado
        servico.salvar_resultados(resultado, f"resultados_{uf}.txt")


# ============================================================
# EXEMPLO 5: Busca com diferentes status
# ============================================================
def exemplo_busca_multiplos_status():
    """Busca com diferentes status de processo"""
    status_list = ["RECEBENDO PROPOSTAS", "EM JULGAMENTO"]
    
    for status in status_list:
        print(f"\n\n{'='*60}")
        print(f"Buscando status: {status}")
        print(f"{'='*60}")
        
        servico = BotService(
            uf="PB",
            status=status,
            palavra_chave="MATERIAL ELETRICO"
        )
        
        resultado = servico.executar_busca()
        servico.exibir_resumo(resultado)


# ============================================================
# EXEMPLO 6: Busca usando configurações do settings.py
# ============================================================
def exemplo_busca_com_settings():
    """Usa as configurações do settings.py automaticamente"""
    from config import settings
    
    # Combina as keywords em uma string
    palavra_chave = " ".join(settings.KEYWORDS)
    
    servico = BotService(
        uf=settings.UF,
        status=settings.STATUS_ALVO,
        palavra_chave=palavra_chave
    )
    
    resultado = servico.executar_busca()
    servico.exibir_resumo(resultado)
    servico.salvar_resultados(resultado)


# ============================================================
# EXEMPLO 7: Busca com tratamento de erro avançado
# ============================================================
def exemplo_busca_com_tratamento_erro():
    """Busca com tratamento robusto de erros"""
    try:
        servico = BotService(
            uf="PB",
            status="RECEBENDO PROPOSTAS",
            palavra_chave="MATERIAL ELETRICO"
        )
        
        resultado = servico.executar_busca()
        
        # Verifica se foi bem-sucedida
        if resultado.get('sucesso'):
            servico.exibir_resumo(resultado)
            servico.salvar_resultados(resultado)
            print("\n✓ Busca completada com sucesso!")
            return True
        else:
            print(f"\n✗ Falha na busca: {resultado.get('erro')}")
            return False
    
    except KeyboardInterrupt:
        print("\n\n✗ Busca interrompida pelo usuário")
        return False
    
    except Exception as e:
        print(f"\n\n✗ Erro inesperado: {str(e)}")
        return False


# ============================================================
# EXEMPLO 8: Processamento dos resultados
# ============================================================
def exemplo_processar_resultados():
    """Executa busca e processa os resultados"""
    servico = BotService(
        uf="PB",
        status="RECEBENDO PROPOSTAS",
        palavra_chave="MATERIAL ELETRICO"
    )
    
    resultado = servico.executar_busca()
    
    if resultado.get('sucesso') and resultado.get('processos'):
        processos = resultado['processos']
        
        # Exemplo 1: Filtra apenas processos com número
        processos_com_numero = [
            p for p in processos 
            if p.get('numero') != 'N/A'
        ]
        print(f"Processos com número: {len(processos_com_numero)}")
        
        # Exemplo 2: Agrupa por órgão
        por_orgao = {}
        for p in processos:
            orgao = p.get('orgao', 'Sem órgão')
            if orgao not in por_orgao:
                por_orgao[orgao] = []
            por_orgao[orgao].append(p)
        
        print(f"\nProcessos por órgão:")
        for orgao, procs in por_orgao.items():
            print(f"  {orgao}: {len(procs)} processo(s)")
        
        # Exemplo 3: Lista de links para acessar processos
        links = [p.get('link') for p in processos if p.get('link') != 'N/A']
        print(f"\nLinks dos processos:")
        for link in links:
            print(f"  {link}")


# ============================================================
# EXEMPLO 9: Integração com pipeline de CI/CD
# ============================================================
def exemplo_pipeline_ci():
    """Exemplo para uso em CI/CD"""
    import sys
    
    servico = BotService(
        uf="PB",
        status="RECEBENDO PROPOSTAS",
        palavra_chave="MATERIAL ELETRICO"
    )
    
    resultado = servico.executar_busca()
    servico.exibir_resumo(resultado)
    
    # Retorna código de saída apropriado
    if resultado.get('sucesso'):
        print(f"\nChecagem OK: {resultado['total_processos']} processos encontrados")
        sys.exit(0)  # Sucesso
    else:
        print(f"\nChecagem FALHOU: {resultado.get('erro')}")
        sys.exit(1)  # Erro


# ============================================================
# INSTRUÇÕES DE USO
# ============================================================
"""
Para usar estes exemplos:

1. Abra um terminal no diretório do projeto
2. Ative o ambiente virtual: venv\\Scripts\\activate
3. Importe e execute a função desejada em Python:

    from exemplo_bot import exemplo_busca_padrao
    exemplo_busca_padrao()

Ou execute via terminal customizado:

    python -c "from exemplo_bot import exemplo_busca_padrao; exemplo_busca_padrao()"

Exemplos disponíveis:
  - exemplo_busca_padrao()              # Busca padrão
  - exemplo_busca_sp()                  # Busca em SP
  - exemplo_busca_multiplas_palavras()  # Múltiplas palavras
  - exemplo_busca_multiplos_estados()   # Múltiplos estados
  - exemplo_busca_multiplos_status()    # Múltiplos status
  - exemplo_busca_com_settings()        # Com settings.py
  - exemplo_busca_com_tratamento_erro() # Com tratamento de erro
  - exemplo_processar_resultados()      # Processar resultados
  - exemplo_pipeline_ci()               # Para CI/CD
"""
