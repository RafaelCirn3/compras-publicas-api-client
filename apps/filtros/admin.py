from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse

from apps.rpa.playwright_sync import sincronizar_filtros_dropdown

from .models import FiltroOpcao, Filtros


@admin.register(Filtros)
class FiltrosAdmin(admin.ModelAdmin):
    list_display = ("id", "objeto", "uf", "status", "criado_em")
    search_fields = ("objeto", "orgao", "processo", "municipio")
    list_filter = ("uf", "status", "modalidade", "criado_em")
    change_list_template = "admin/filtros/filtros/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sincronizar-filtros/",
                self.admin_site.admin_view(self.sincronizar_filtros_view),
                name="filtros_filtros_sincronizar",
            )
        ]
        return custom_urls + urls

    def sincronizar_filtros_view(self, request):
        try:
            resultado = sincronizar_filtros_dropdown(headless=True)
            self.message_user(
                request,
                f"Sincronizacao concluida. {resultado.get('total_criados', 0)} opcoes carregadas.",
                level=messages.SUCCESS,
            )
        except Exception as exc:
            self.message_user(
                request,
                f"Falha ao sincronizar filtros: {exc}",
                level=messages.ERROR,
            )

        changelist_url = reverse("admin:filtros_filtros_changelist")
        return redirect(changelist_url)


@admin.register(FiltroOpcao)
class FiltroOpcaoAdmin(admin.ModelAdmin):
    list_display = ("id", "campo", "valor", "criado_em")
    list_filter = ("campo",)
    search_fields = ("campo", "valor")
