from django.db import models

class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)

    class Meta:
        db_table = 'CLIENTE'
        managed = False