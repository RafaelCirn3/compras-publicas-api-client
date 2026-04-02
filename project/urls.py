from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("filtros/", include("apps.filtros.urls")),
    path("rpa/", include("apps.rpa.urls")),
    path("", RedirectView.as_view(pattern_name="filtros:dashboard", permanent=False)),
]
