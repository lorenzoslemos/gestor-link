from django.db import models

class Empresa(models.Model):
    id_empresa = models.IntegerField(primary_key=True, db_column='id_empresa')
    cnpj = models.CharField(max_length=14)
    empresa = models.CharField(max_length=50)
    id_regime = models.ForeignKey('RegimeTributario', on_delete=models.CASCADE, db_column='id_regime')
    id_natureza = models.ForeignKey('NaturezaJuridica', on_delete=models.CASCADE, db_column='id_natureza')

    class Meta:
        db_table = 'EMPRESA'
        managed = False

class NaturezaJuridica(models.Model):
    id_natureza = models.IntegerField(primary_key=True)
    natureza_juridica = models.CharField(max_length=50)

    class Meta:
        db_table = 'NATUREZA_JURIDICA'
        managed = False

    def __str__(self):
        return self.natureza_juridica

class RegimeTributario(models.Model):
    id_regime = models.IntegerField(primary_key=True)
    regime_tributario = models.CharField(max_length=30)

    class Meta:
        db_table = 'REGIME_TRIBUTARIO'
        managed = False

    def __str__(self):
        return self.regime_tributario