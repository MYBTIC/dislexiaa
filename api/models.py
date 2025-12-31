from django.db import models

# 1. Creamos una base común para ambos modos
class PalabraBase(models.Model):
    nombre = models.CharField(max_length=20)
    imagen = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

# 2. El Modo 1 hereda de la base
class PalabraModo1(PalabraBase):
    palabra_dividida_letras = models.CharField(max_length=30)
    tamano = models.IntegerField()

# 3. El Modo 2 hereda de la base
class PalabraModo2(PalabraBase):
    palabra_dividida_silabas = models.CharField(max_length=30)
    silabas = models.IntegerField()

# 4. Tabla Oración con una sola clave foránea
class Oracion(models.Model):
    palabra = models.ForeignKey(PalabraBase, on_delete=models.CASCADE)
    oracion_texto = models.CharField(max_length=100)

    def __str__(self):
        return self.oracion_texto