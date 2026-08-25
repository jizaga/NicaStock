from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
      ordering = ['nombre']

    def __str__(self):
      return self.nombre
