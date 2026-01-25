from django.db import models

class Curso(models.Model):
    codigo = models.CharField(primary_key = True, max_length=6)
    nombre = models.CharField(max_length=58)
    creditos = models.PositiveSmallIntegerField()

    def __str__(self): #Mostrar texto de la clase o objeto
        texto = "{0} ({1})"
        return texto.format(self.nombre, self.creditos)

