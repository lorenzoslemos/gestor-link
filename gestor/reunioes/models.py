from django.db import models

class Reuniao(models.Model):
    id_reuniao = models.IntegerField(primary_key=True)
    cliente = models.CharField(max_length=20)
    pauta = models.CharField(max_length=1000)
    data_reuniao = models.DateField()

    class Meta:
        db_table = 'REUNIAO'
        managed = False