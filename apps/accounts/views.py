from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import RegistroForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


def registro_view(request):
    if request.user.is_authenticated:
        return redirect("filtros:dashboard")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso. Faca login para continuar.")
            return redirect("accounts:login")
    else:
        form = RegistroForm()

    return render(request, "accounts/register.html", {"form": form})
