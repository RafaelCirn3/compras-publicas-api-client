# Sistema SaaS RPA - Compras Publicas

Aplicacao Django com autenticacao, CRUD de filtros e execucao de automacao Selenium via URL injection.

## Stack

- Django Templates
- AdminLTE (CDN)
- SQLite
- Selenium (logica reaproveitada de `src/`)

## Estrutura

```text
compras-publicas-api-client/
├── manage.py
├── project/
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── accounts/
│   ├── filtros/
│   └── rpa/
├── src/
│   ├── services/url_injection_bot_service.py
│   └── utils/selenium_utils.py
└── tools/exportar_csv.py
```

## Como rodar

1. Ative o ambiente virtual.
2. Instale dependencias:

```bash
pip install -r requirements.txt
```

3. Execute migracoes:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Crie um usuario admin:

```bash
python manage.py createsuperuser
```

5. Inicie o servidor:

```bash
python manage.py runserver
```

## Fluxo funcional

1. Login em `/accounts/login/`
2. Criar filtro em `/filtros/novo/`
3. Executar RPA pelo dashboard
4. Ver resultados em `/rpa/resultado/`
5. Exportar CSV na tela de resultados
