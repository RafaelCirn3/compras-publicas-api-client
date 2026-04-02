# Compras Públicas API Client

Projeto em RPA com o fluxo de URL injection como caminho principal.

## Estado atual

- `main.py` executa o fluxo principal de URL injection.
- A camada de API foi removida.
- O fluxo manual de abertura do site e seleção de filtros pela interface foi removido da execução principal.
- Os módulos de automação existentes foram preservados para evolução futura.

## Estrutura principal

```text
compras-publicas-api-client/
├── main.py
├── config/
│   └── settings.py
├── src/
│   ├── services/
│   │   └── url_injection_bot_service.py
│   └── utils/
│       ├── filters.py
│       └── selenium_utils.py
├── tools/
│   └── exportar_csv.py
└── requirements.txt
```

## Configuração

O arquivo `.env.example` contém apenas parâmetros gerais e de Selenium.

## Execução

```bash
python main.py
```

O entrypoint atual é apenas uma base neutra para a próxima etapa.
