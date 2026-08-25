from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
      verbose_name = 'categoría'
      verbose_name_plural = 'categorías'
      ordering = ['nombre']

    def __str__(self):
      return self.nombre
