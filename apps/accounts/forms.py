from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
	first_name = forms.CharField(max_length=150, label="Nome")
	last_name = forms.CharField(max_length=150, label="Sobrenome")
	email = forms.EmailField(label="Email")

	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "password1", "password2")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["password1"].label = "Senha"
		self.fields["password2"].label = "Confirmacao de senha"
		for field in self.fields.values():
			field.widget.attrs["class"] = "form-control"

	def save(self, commit=True):
		user = super().save(commit=False)
		user.username = self.cleaned_data["email"]
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		if commit:
			user.save()
		return user
