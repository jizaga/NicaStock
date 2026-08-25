from django.db import models
from Proveedor.models import Proveedor
from Categoria.models import Categoria
from django.core.validators import MinValueValidator


class Producto(models.Model):
    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=160)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='productos')
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    stock_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    activo = models.BooleanField(default=True)

    class Meta:
      ordering = ['nombre']
      permissions = [('importar_productos', 'Puede importar productos desde CSV')]

    def __str__(self):
      return f'{self.codigo} - {self.nombre}'

    @property
    def bajo_minimo(self): return self.stock_actual <= self.stock_minimo
