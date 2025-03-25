from django.db import models

class Vencimento(models.Model):
    id_vencimento = models.AutoField(primary_key=True, db_column='id_vencimento')
    cpf = models.CharField(max_length=11, blank=True)
    cnpj = models.CharField(max_length=14, blank=True)
    id_prazo = models.ForeignKey('Prazo', on_delete=models.CASCADE, db_column='id_prazo')
    data_vencimento = models.DateField()

    class Meta:
        db_table = 'VENCIMENTO'
        managed = False

class Prazo(models.Model):
    id_prazo = models.IntegerField(primary_key=True)
    prazo_monitorado = models.CharField(max_length=30)

    class Meta:
        db_table = 'PRAZO'
        managed = False

    def __str__(self):
        return self.prazo_monitorado