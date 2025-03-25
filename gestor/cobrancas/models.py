from django.db import models

class Cobranca(models.Model):
    id_cobranca = models.IntegerField(primary_key=True)
    cpf = models.CharField(max_length=11)
    cnpj = models.CharField(max_length=14)
    descricao = models.CharField(max_length=50)
    valor = models.FloatField()
    data_vencimento = models.DateField()
    status_pagamento = models.CharField(max_length=6)

    class Meta:
        db_table = 'COBRANCA'
        managed = False