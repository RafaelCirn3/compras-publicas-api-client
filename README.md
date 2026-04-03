# Sistema SaaS RPA - Compras Publicas

Aplicacao Django com autenticacao, CRUD de filtros e execucao de automacao Selenium via URL injection.

## Stack

- Django 6.0.3
- Django Templates + Bootstrap 5.3.3
- SQLite
- Selenium (automacao RPA)
- Python 3.x

## Requisitos Previos

- **Python 3.9+** instalado
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para clonar repositorio)

## Estrutura

```text
compras-publicas-api-client/
├── manage.py
├── requirements.txt
├── .env                          # ← Criar a partir de .env.example
├── .env.example                  # Modelo de variaveis de ambiente
├── static/                       # Arquivos CSS, JS, imagens
├── staticfiles/                  # Gerado apos collectstatic
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── middleware.py             # SecurityHeaders middleware
├── apps/
│   ├── accounts/
│   ├── filtros/
│   │   └── migrations/           # Incluindo 0003_filtros_user.py
│   └── rpa/
├── src/
│   ├── services/
│   └── utils/
└── tools/
    └── exportar_csv.py
```

## Setup Inicial (Passo a Passo)

### 1. Clonar ou baixar o repositorio

```bash
git clone <url-do-repo>
cd compras-publicas-api-client
```

### 2. Criar e ativar ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota:** Se receber erro de pacotes ausentes, certifique-se que o ambiente virtual esta ativo.

### 4. Configurar variaveis de ambiente

Copie `.env.example` para `.env`:

```bash
cp .env.example .env
# ou no Windows:
# copy .env.example .env
```

Edite o arquivo `.env` e preencha as variaveis obrigatorias:

```env
# OBRIGATORIO - Gere uma chave secreta forte
DJANGO_SECRET_KEY=seu-secreto-uber-seguro-aqui

# Desenvolvimento local (mude para false em producao)
DJANGO_DEBUG=true

# Para desenvolvimento local
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Email (opcional, necessario apenas se usar recuperacao de senha)
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app-google
```

**Para gerar DJANGO_SECRET_KEY, execute:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Setup do banco de dados

Execute as migracoes para criar as tabelas:

```bash
# Criar migrações (normalmente ja existem)
python manage.py makemigrations

# Aplicar migrações ao banco
python manage.py migrate
```

**Se receber erro de SECRET_KEY:**
- Certifique-se que `.env` foi criado e `.env` esta no `.gitignore`
- Verifique que `DJANGO_SECRET_KEY` esta preenchido no `.env`

### 6. Coletar arquivos estaticos

Este passo e **ESSENCIAL** para que CSS, JS e imagens funcionem:

```bash
python manage.py collectstatic --noinput
```

**Resultado esperado:** "132 static files copied" (ou numero similar)

**Se falhar:**
- Certifique-se que a pasta `static/` existe no raiz do projeto
- Verifique permissoes de escrita na pasta do projeto

### 7. Criar usuario administrativo

```bash
python manage.py createsuperuser
```

Siga as prompts para criar login/senha.

### 8. Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver
```

**Resultado esperado:**
```
Starting development server at http://127.0.0.1:8000/
```

Abra no navegador: **http://localhost:8000**

## Fluxo de Uso

1. **Login:** Acesse `/accounts/login/` com usuario criado
2. **Dashboard:** `/filtros/` - visualize e gerencia seus filtros
3. **Novo Filtro:** `/filtros/novo/` - configure criterios de busca
4. **Executar RPA:** Click no botao "Executar" no dashboard
5. **Resultados:** `/rpa/resultado/` - visualize e exporte dados
6. **Admin:** `/admin/` - gerenciamento de dados (usuario admin)

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'django'"

**Solucao:**
```bash
# Certifique-se que .venv esta ativo
.\.venv\Scripts\Activate.ps1  # Windows

# Reinstale dependencias
pip install -r requirements.txt
```

### ❌ "ImproperlyConfigured: The SECRET_KEY setting must not be empty"

**Solucao:**
1. Verifique se arquivo `.env` existe no raiz do projeto
2. Abra `.env` e confirme que `DJANGO_SECRET_KEY` nao esta vazio
3. Se vazio, gere uma chave:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### ❌ CSS/JS nao carregam (404 Not Found)

**Causa comum:** Arquivos estaticos nao foram coletados

**Solucao:**
```bash
python manage.py collectstatic --noinput
# Reinicie o servidor
python manage.py runserver
```

### ❌ "No such table: filtros_filtros"

**Causa comum:** Migracoes nao foram aplicadas

**Solucao:**
```bash
python manage.py migrate
```

### ❌ Erro ao fazer login ou criar filtro relacionado a "user"

**Causa comum:** Migracoes antigas nao aplicadas (migration 0003_filtros_user.py)

**Solucao:**
```bash
python manage.py migrate filtros 0003
python manage.py migrate filtros 0004
```

### ❌ "Port 8000 is already in use"

**Solucao (use porta diferente):**
```bash
python manage.py runserver 8080
# ou especifique IP e porta
python manage.py runserver 0.0.0.0:9000
```

## Checklist de Deploy

Antes de colocar em producao:

- [ ] `DJANGO_DEBUG=false` em `.env`
- [ ] `DJANGO_SECRET_KEY` alterada para valor seguro
- [ ] `DJANGO_ALLOWED_HOSTS` atualizado com dominio real
- [ ] `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD` configurados
- [ ] `python manage.py check --deploy` executado sem erros
- [ ] `collectstatic` executado
- [ ] Backup do banco SQLite realizado
- [ ] HTTPS habilitado (`DJANGO_USE_HTTPS=true`)

## Desenvolvimento

### Estrutura de Aplicacoes

- **accounts/**: Autenticacao e usuarios
- **filtros/**: CRUD de criterios de busca
- **rpa/**: Execucao de automacao e resultados

### Migrações de Banco

Se alterar modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Testes de Seguranca

```bash
python manage.py check --deploy
```

## Licenca

[Especificar licenca aqui]

## Suporte

Para problemas ou duvidas, abra uma issue no repositorio ou contate os mantenedores.
