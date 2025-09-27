from django.db import models

TIPO_PROCESSO_CHOICES = [
    ('abertura', 'Abertura'),
    ('alteracao', 'Alteração'),
    ('baixa', 'Baixa'),
]

STATUS_PROCESSO_CHOICES = [
    ('pendente', 'Pendente'),
    ('finalizado', 'Finalizado'),
    ('em andamento', 'Em Andamento'),
]

RESPONSAVEL_CHOICES = [
    ('myllena.cristina', 'Myllena Cristina'),
    ('ana.maria', 'Ana Maria'),
    ('jessica.baches', 'Jéssica Baches'),
    ('kimber.rossi', 'Kimber Rossi'),
]

class Processo(models.Model):
    id_processo = models.IntegerField(primary_key=True)
    cpf = models.CharField(max_length=11)
    cnpj = models.CharField(max_length=14)
    tipo_processo =models.CharField(max_length=30, choices=TIPO_PROCESSO_CHOICES)
    status_processo = models.CharField(max_length=30, choices=STATUS_PROCESSO_CHOICES)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    descricao = models.CharField(max_length=1000)
    responsavel = models.CharField(max_length=16, choices=RESPONSAVEL_CHOICES)

    class Meta:
        db_table = 'PROCESSO'
        managed = False