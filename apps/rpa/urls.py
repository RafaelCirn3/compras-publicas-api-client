from django.urls import path

from . import views

app_name = "rpa"

urlpatterns = [
    path("executar/<int:filtro_id>/", views.executar, name="executar"),
    path("resultado/", views.resultado, name="resultado"),
    path("resultado/exportar-csv/", views.exportar_resultado_csv, name="exportar_csv"),
]
