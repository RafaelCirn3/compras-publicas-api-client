from django.urls import path

from . import views

app_name = "filtros"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("lista/", views.filtro_list, name="list"),
    path("novo/", views.filtro_create, name="create"),
    path("<int:pk>/editar/", views.filtro_update, name="update"),
    path("<int:pk>/excluir/", views.filtro_delete, name="delete"),
    # API endpoints
    path("api/ufs/", views.api_ufs, name="api_ufs"),
    path("api/municipios/", views.api_municipios, name="api_municipios"),
]
