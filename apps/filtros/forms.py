from django import forms
from django.core.exceptions import ValidationError

from .models import FiltroOpcao, Filtros


# Lista estática de UFs brasileiras
UFS_BRASIL = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
]


class FiltrosForm(forms.ModelForm):
    class Meta:
        model = Filtros
        fields = [
            "objeto",
            "processo",
            "orgao",
            "uf",
            "municipio",
            "status",
            "modalidade",
            "realizacao",
            "julgamento",
            "periodo_inicio",
            "periodo_fim",
        ]
        widgets = {
            "uf": forms.Select(attrs={
                "class": "form-control select2-dropdown",
                "id": "id_uf",
            }),
            "municipio": forms.Select(attrs={
                "class": "form-control select2-dropdown",
                "id": "id_municipio",
            }),
            "periodo_inicio": forms.DateInput(attrs={"type": "date"}),
            "periodo_fim": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uf_valor_atual = self.data.get("uf") if self.data else (self.instance.uf if self.instance and getattr(self.instance, "pk", None) else "")
        municipio_valor_atual = self.data.get("municipio") if self.data else (self.instance.municipio if self.instance and getattr(self.instance, "pk", None) else "")

        # Configurar campo UF
        uf_choices = [("", "Selecione um estado")] + UFS_BRASIL
        self.fields["uf"] = forms.ChoiceField(
            choices=uf_choices,
            required=False,
            label="Estado (UF)",
            initial=uf_valor_atual,
            widget=forms.Select(
                attrs={
                    "class": "form-control select2-dropdown",
                    "id": "id_uf",
                }
            ),
        )

        # Configurar campo Município (inicialmente vazio; carregado dinamicamente via endpoint)
        municipios_choices = [("", "Selecione um município")]
        if municipio_valor_atual:
            municipios_choices.append((municipio_valor_atual, municipio_valor_atual))

        self.fields["municipio"] = forms.ChoiceField(
            choices=municipios_choices,
            required=False,
            label="Município",
            initial=municipio_valor_atual,
            widget=forms.Select(
                attrs={
                    "class": "form-control select2-dropdown",
                    "id": "id_municipio",
                    "data-selected": municipio_valor_atual or "",
                }
            ),
        )

        # Configurar campos de filtro sincronizado
        for campo in ["status", "realizacao", "modalidade", "julgamento"]:
            opcoes_db = list(
                FiltroOpcao.objects.filter(campo=campo).values_list("valor", flat=True)
            )

            valor_atual = None
            if self.instance and getattr(self.instance, "pk", None):
                valor_atual = getattr(self.instance, campo)
                if valor_atual and valor_atual not in opcoes_db:
                    opcoes_db.insert(0, valor_atual)

            choices = [("", "Selecione...")] + [(valor, valor) for valor in opcoes_db]
            self.fields[campo] = forms.ChoiceField(
                choices=choices,
                required=False,
                label=self.fields[campo].label,
            )
            if valor_atual:
                self.initial[campo] = valor_atual

        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()

    def clean(self):
        cleaned_data = super().clean()
        periodo_inicio = cleaned_data.get("periodo_inicio")
        periodo_fim = cleaned_data.get("periodo_fim")

        if periodo_inicio and periodo_fim and periodo_inicio > periodo_fim:
            raise ValidationError("A data inicial não pode ser posterior à data final.")

        return cleaned_data
