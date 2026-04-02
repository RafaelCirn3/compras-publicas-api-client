from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.filtros.models import Filtros
from tools.exportar_csv import exportar_para_csv

from .services import executar_rpa


@login_required
def executar(request, filtro_id):
    filtro = get_object_or_404(Filtros, pk=filtro_id)

    if request.method == "POST":
        processos, resultado = executar_rpa(filtro)
        request.session["ultimo_resultado"] = processos
        request.session["ultimo_filtro_id"] = filtro.id
        if resultado.get("sucesso"):
            messages.success(request, f"RPA executado com sucesso. {len(processos)} processo(s) encontrado(s).")
        else:
            messages.error(request, f"Falha ao executar RPA: {resultado.get('erro', 'Erro desconhecido')}")
        return redirect("rpa:resultado")

    return render(request, "rpa/executar.html", {"filtro": filtro})


@login_required
def resultado(request):
    processos = request.session.get("ultimo_resultado", [])
    filtro_id = request.session.get("ultimo_filtro_id")
    filtro = None
    if filtro_id:
        filtro = Filtros.objects.filter(pk=filtro_id).first()
    return render(request, "rpa/resultado.html", {"processos": processos, "filtro": filtro})


@login_required
def exportar_resultado_csv(request):
    processos = request.session.get("ultimo_resultado", [])
    if not processos:
        messages.warning(request, "Nao ha resultados para exportar.")
        return redirect("rpa:resultado")

    filepath = exportar_para_csv(processos, nome_arquivo="resultado_rpa.csv")
    with open(filepath, "rb") as file_handle:
        data = file_handle.read()

    response = HttpResponse(data, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="resultado_rpa.csv"'
    return response
