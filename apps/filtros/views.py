import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FiltrosForm
from .models import Filtros


@login_required
def dashboard(request):
    filtros = Filtros.objects.all().order_by("-criado_em")
    return render(request, "filtros/dashboard.html", {"filtros": filtros})


@login_required
def filtro_list(request):
    filtros = Filtros.objects.all().order_by("-criado_em")
    return render(request, "filtros/filtro_list.html", {"filtros": filtros})


@login_required
def filtro_create(request):
    if request.method == "POST":
        form = FiltrosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Filtro criado com sucesso.")
            return redirect("filtros:list")
    else:
        form = FiltrosForm()
    return render(request, "filtros/filtro_form.html", {"form": form, "titulo": "Novo filtro"})


@login_required
def filtro_update(request, pk):
    filtro = get_object_or_404(Filtros, pk=pk)
    if request.method == "POST":
        form = FiltrosForm(request.POST, instance=filtro)
        if form.is_valid():
            form.save()
            messages.success(request, "Filtro atualizado com sucesso.")
            return redirect("filtros:list")
    else:
        form = FiltrosForm(instance=filtro)
    return render(request, "filtros/filtro_form.html", {"form": form, "titulo": "Editar filtro"})


@login_required
def filtro_delete(request, pk):
    filtro = get_object_or_404(Filtros, pk=pk)
    if request.method == "POST":
        filtro.delete()
        messages.success(request, "Filtro excluido com sucesso.")
        return redirect("filtros:list")
    return render(request, "filtros/filtro_delete.html", {"filtro": filtro})


def api_ufs(request):
    """Retorna lista de UFs para autocomplete"""
    ufs_brasil = [
        {"sigla": "AC", "nome": "Acre"},
        {"sigla": "AL", "nome": "Alagoas"},
        {"sigla": "AP", "nome": "Amapá"},
        {"sigla": "AM", "nome": "Amazonas"},
        {"sigla": "BA", "nome": "Bahia"},
        {"sigla": "CE", "nome": "Ceará"},
        {"sigla": "DF", "nome": "Distrito Federal"},
        {"sigla": "ES", "nome": "Espírito Santo"},
        {"sigla": "GO", "nome": "Goiás"},
        {"sigla": "MA", "nome": "Maranhão"},
        {"sigla": "MT", "nome": "Mato Grosso"},
        {"sigla": "MS", "nome": "Mato Grosso do Sul"},
        {"sigla": "MG", "nome": "Minas Gerais"},
        {"sigla": "PA", "nome": "Pará"},
        {"sigla": "PB", "nome": "Paraíba"},
        {"sigla": "PR", "nome": "Paraná"},
        {"sigla": "PE", "nome": "Pernambuco"},
        {"sigla": "PI", "nome": "Piauí"},
        {"sigla": "RJ", "nome": "Rio de Janeiro"},
        {"sigla": "RN", "nome": "Rio Grande do Norte"},
        {"sigla": "RS", "nome": "Rio Grande do Sul"},
        {"sigla": "RO", "nome": "Rondônia"},
        {"sigla": "RR", "nome": "Roraima"},
        {"sigla": "SC", "nome": "Santa Catarina"},
        {"sigla": "SP", "nome": "São Paulo"},
        {"sigla": "SE", "nome": "Sergipe"},
        {"sigla": "TO", "nome": "Tocantins"},
    ]
    
    query = request.GET.get("q", "").lower()
    resultados = [uf for uf in ufs_brasil if query in uf["sigla"].lower() or query in uf["nome"].lower()]
    
    return JsonResponse({"results": resultados})


def api_municipios(request):
    """Retorna lista de municipios por UF via API do IBGE"""
    uf = request.GET.get("uf", "").upper()
    query = request.GET.get("q", "").lower()
    
    if not uf or len(uf) != 2:
        return JsonResponse({"results": []})
    
    try:
        response = requests.get(
            f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios",
            timeout=10,
        )
        if response.status_code == 200:
            municipios = response.json()
            nomes_municipios = [m.get("nome", "") for m in municipios if m.get("nome")]

            if query:
                nomes_municipios = [nome for nome in nomes_municipios if query in nome.lower()]

            nomes_municipios = sorted(nomes_municipios)
            resultados = [{"id": nome, "text": nome} for nome in nomes_municipios]
            return JsonResponse({"results": resultados})
    except Exception as e:
        print(f"Erro ao buscar municipios: {e}")
    
    return JsonResponse({"results": []})
