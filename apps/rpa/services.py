from apps.filtros.models import Filtros
from src.services.url_injection_bot_service import UrlInjectionBotService


UF_PARA_CODIGO = {
    "AC": "100002",
    "AL": "100003",
    "AP": "100004",
    "AM": "100005",
    "BA": "100006",
    "CE": "100007",
    "DF": "100008",
    "ES": "100009",
    "GO": "100010",
    "MA": "100011",
    "MT": "100012",
    "MS": "100013",
    "MG": "100014",
    "PA": "100015",
    "PB": "100125",
    "PR": "100017",
    "PE": "100018",
    "PI": "100019",
    "RJ": "100020",
    "RN": "100021",
    "RS": "100022",
    "RO": "100023",
    "RR": "100024",
    "SC": "100025",
    "SP": "100026",
    "SE": "100027",
    "TO": "100028",
}

STATUS_PARA_CODIGO = {
    "RECEBENDO PROPOSTAS": "1",
}


def _mapear_uf(uf: str | None) -> str | None:
    if not uf:
        return None
    return UF_PARA_CODIGO.get(uf.upper())


def _mapear_status(status: str | None) -> str | None:
    if not status:
        return None
    return STATUS_PARA_CODIGO.get(status.upper())


def executar_rpa(filtro: Filtros):
    """
    Recebe um objeto Filtros
    Monta a URL com base nos campos
    Executa o Selenium usando o codigo existente
    Retorna lista de resultados
    """
    objeto = filtro.objeto or None

    servico = UrlInjectionBotService(
        pagina=1,
        uf_codigo=_mapear_uf(filtro.uf),
        status_codigo=_mapear_status(filtro.status),
        objeto=objeto,
    )
    resultado = servico.executar_busca()
    return resultado.get("processos", []), resultado
