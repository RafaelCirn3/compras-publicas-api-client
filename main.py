"""Arquivo legado: a entrada principal agora e o Django via manage.py."""


def main():
    """Mantido apenas por compatibilidade."""
    print("Este projeto agora usa Django. Execute: python manage.py runserver")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())