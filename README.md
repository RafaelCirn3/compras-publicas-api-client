# Sistema de Busca de Processos de Compras Públicas

Sistema para buscar e filtrar processos de compras públicas através da API do Portal de Compras Públicas.

## 📁 Estrutura do Projeto

```
projeto/
├── .env                    # Variáveis de ambiente (não commitado)
├── .env.example            # Exemplo de configuração
├── .gitignore              # Arquivos ignorados pelo git
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
├── main.py                 # Ponto de entrada da aplicação
│
├── config/                 # Configurações
│   ├── __init__.py
│   └── settings.py         # Gerenciamento de configurações
│
├── src/                    # Código fonte
│   ├── __init__.py
│   │
│   ├── api/                # Cliente da API
│   │   ├── __init__.py
│   │   └── client.py       # ApiClient
│   │
│   ├── services/           # Lógica de negócio
│   │   ├── __init__.py
│   │   └── processo_service.py  # ProcessoService
│   │
│   └── utils/              # Utilitários
│       ├── __init__.py
│       └── filters.py      # Funções de filtragem
│
└── tools/                  # Ferramentas auxiliares
    └── __init__.py
```

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd projeto
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Edite o arquivo `.env` e adicione sua `PUBLIC_KEY`

```bash
copy .env.example .env
```

## ⚙️ Configuração

Edite o arquivo `.env` com suas configurações:

```env
# Configurações da API
API_BASE_URL=https://apipcp.portaldecompraspublicas.com.br/publico
PUBLIC_KEY=SUA_CHAVE_AQUI

# Configurações de Busca
UF=PB
DIAS_BUSCA=30

# Filtros
KEYWORDS=MATERIAL,ELETRICO
STATUS_ALVO=RECEBENDO PROPOSTAS

# Paginação
PAGE_SIZE=1
```

### Parâmetros configuráveis:

- **PUBLIC_KEY**: Sua chave de acesso à API
- **UF**: Unidade Federativa para busca (ex: PB, SP, RJ)
- **DIAS_BUSCA**: Número de dias retroativos para buscar processos
- **KEYWORDS**: Palavras-chave separadas por vírgula para filtrar processos
- **STATUS_ALVO**: Status dos processos a serem filtrados

## 📖 Uso

Execute o programa:

```bash
python main.py
```

O sistema irá:
1. Buscar processos nos últimos X dias (configurável)
2. Filtrar processos que contenham as palavras-chave
3. Filtrar apenas processos com status "RECEBENDO PROPOSTAS"
4. Exibir os resultados

## 📦 Módulos

### config/
Gerenciamento de configurações usando variáveis de ambiente

### src/api/
Cliente para comunicação com a API do Portal de Compras Públicas

### src/services/
Lógica de negócio da aplicação

### src/utils/
Funções utilitárias e filtros

### tools/
Ferramentas auxiliares e scripts

## 🛠️ Tecnologias

- Python 3.8+
- requests - Cliente HTTP
- python-dotenv - Gerenciamento de variáveis de ambiente

## 📝 Licença

Este projeto é de uso interno.
