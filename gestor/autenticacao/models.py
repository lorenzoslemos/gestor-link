from django.db import models

class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True, primary_key=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'USUARIOS'  # Nome da tabela no banco de dados
        managed = False  # Impede que o Django gerencie a criação da tabela

    def __str__(self):
        return self.username

    @classmethod
    def get_by_natural_key(cls, username):
        return cls.objects.get(username=username)

    @property
    def is_anonymous(self):
        return False  # Retorna sempre False, pois esse é um usuário autenticado

    @property
    def is_authenticated(self):
        return True  # Retorna sempre True, pois o usuário foi autenticado

    @property
    def is_active(self):
        return True  # Retorna True, caso você não precise de um campo is_active no seu modelo

    @property
    def is_staff(self):
        return False