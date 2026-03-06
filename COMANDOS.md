# Comandos Úteis

## Configuração Inicial

```powershell
# Executar script de setup (recomendado)
.\setup.ps1

# OU manualmente:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## Executar o Projeto

```powershell
# Ativar ambiente virtual
venv\Scripts\activate

# Executar programa principal
python main.py

# Executar ferramenta de exportação
python tools\exportar_csv.py
```

## Desenvolvimento

```powershell
# Instalar nova dependência
pip install nome-pacote
pip freeze > requirements.txt

# Verificar estrutura
tree /F

# Listar arquivos Python
Get-ChildItem -Recurse -Filter "*.py"
```

## Estrutura de Pastas

- **config/** - Configurações e variáveis de ambiente
- **src/api/** - Cliente da API
- **src/services/** - Lógica de negócio
- **src/utils/** - Funções utilitárias
- **tools/** - Scripts e ferramentas auxiliares

## Variáveis de Ambiente (.env)

```env
PUBLIC_KEY=sua_chave_aqui
UF=PB
KEYWORDS=PALAVRA1,PALAVRA2
STATUS_ALVO=RECEBENDO PROPOSTAS
DIAS_BUSCA=30
```

## Git

```bash
# Inicializar repositório
git init

# Primeiro commit
git add .
git commit -m "Estrutura inicial do projeto"

# Adicionar remote
git remote add origin <url>
git push -u origin main
```
