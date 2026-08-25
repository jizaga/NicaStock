from django.contrib import admin
from Categoria.models import Categoria
from Proveedor.models import Proveedor
from Cliente.models import Cliente
from Producto.models import Producto
from Movimiento.models import Movimiento, DetalleMovimiento
admin.site.register([Categoria, Proveedor, Cliente, Producto])


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'tipo', 'referencia', 'proveedor', 'cliente', 'usuario')
    readonly_fields = ('fecha', 'usuario')
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(DetalleMovimiento)
class DetalleMovimientoAdmin(admin.ModelAdmin):
    list_display = ('movimiento', 'producto', 'cantidad', 'costo_unitario')
    def has_change_permission(self, request, obj=None):
        return obj is None
    def has_delete_permission(self, request, obj=None):
        return False
