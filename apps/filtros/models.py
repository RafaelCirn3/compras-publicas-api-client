from django.db import models


class Filtros(models.Model):
    objeto = models.CharField(max_length=255, blank=True, null=True)
    processo = models.CharField(max_length=100, blank=True, null=True)
    orgao = models.CharField(max_length=255, blank=True, null=True)

    uf = models.CharField(max_length=2, blank=True, null=True)
    municipio = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(max_length=100, blank=True, null=True)
    modalidade = models.CharField(max_length=100, blank=True, null=True)

    realizacao = models.CharField(max_length=100, blank=True, null=True)
    julgamento = models.CharField(max_length=100, blank=True, null=True)

    periodo_inicio = models.DateField(blank=True, null=True)
    periodo_fim = models.DateField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Filtro"
        verbose_name_plural = "Filtros"
    def __str__(self):
        return f"Filtro {self.id} - {self.objeto or 'Sem objeto'}"


class FiltroOpcao(models.Model):
    CAMPO_CHOICES = [
        ("status", "Status"),
        ("realizacao", "Realizacao"),
        ("modalidade", "Modalidade"),
        ("julgamento", "Julgamento"),
    ]

    campo = models.CharField(max_length=30, choices=CAMPO_CHOICES)
    valor = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("campo", "valor")
        ordering = ["campo", "valor"]
        verbose_name = "Opção de Filtro"
        verbose_name_plural = "Opções de Filtro"

    def __str__(self):
        return f"{self.campo}: {self.valor}"

