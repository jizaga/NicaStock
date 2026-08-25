from django.db import models
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import F
from Proveedor.models import Proveedor
from Producto.models import Producto
from Cliente.models import Cliente


# Create your models here.
class Movimiento(models.Model):
    ENTRADA, SALIDA, AJUSTE = 'E', 'S', 'A'
    TIPO_CHOICES = [(ENTRADA, 'Entrada'), (SALIDA, 'Salida'), (AJUSTE, 'Ajuste')]
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    referencia = models.CharField(max_length=80, blank=True)
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.PROTECT, related_name='movimientos')
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT, related_name='movimientos')
    observaciones = models.TextField(blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
      ordering = ['-fecha']
      verbose_name = 'movimiento'
      verbose_name_plural = 'movimientos'

    def __str__(self):
      return f'{self.get_tipo_display()} #{self.pk}'

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.tipo == self.ENTRADA and not self.proveedor_id:
          raise ValidationError('Una entrada requiere proveedor.')
        if self.tipo == self.SALIDA and not self.cliente_id:
          raise ValidationError('Una salida requiere cliente.')

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_movimiento')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    class Meta:
      unique_together = [('movimiento', 'producto')]

    @property
    def subtotal(self):
      return self.cantidad * self.costo_unitario

    def save(self, *args, **kwargs):
        if self.pk:
          raise ValueError('Los detalles no se pueden modificar; cree un movimiento de ajuste.')
        with transaction.atomic():
            producto = Producto.objects.select_for_update().get(pk=self.producto_id)
            delta = self.cantidad if self.movimiento.tipo == Movimiento.ENTRADA else -self.cantidad
            if self.movimiento.tipo == Movimiento.AJUSTE: delta = self.cantidad
            if producto.stock_actual + delta < 0:
              raise ValueError(f'Stock insuficiente para {producto.nombre}.')
            super().save(*args, **kwargs)
            producto.stock_actual = F('stock_actual') + delta
            producto.save(update_fields=['stock_actual'])
