from decimal import Decimal
from django.core.management.base import BaseCommand
from inventario.models import Categoria, Proveedor, Cliente, Producto, Movimiento, DetalleMovimiento

class Command(BaseCommand):
    help = 'Carga datos básicos de demostración (seguro de ejecutar varias veces).'
    def handle(self, *args, **opts):
        bebidas, _ = Categoria.objects.get_or_create(nombre='Bebidas')
        alimentos, _ = Categoria.objects.get_or_create(nombre='Alimentos')
        exotic, _ = Proveedor.objects.get_or_create(nombre='Exotic Liquids')
        grandma, _ = Proveedor.objects.get_or_create(nombre="Grandma Kelly's Homestead")
        cliente, _ = Cliente.objects.get_or_create(nombre='Cliente de demostración')
        productos = [("BEB-001", 'Chai', bebidas, exotic, '18.00', '25.00', '10'), ('ALI-001', "Grandma's Boysenberry Spread", alimentos, grandma, '20.00', '29.00', '8')]
        for codigo, nombre, cat, prov, compra, venta, minimo in productos:
            p, _ = Producto.objects.get_or_create(codigo=codigo, defaults={'nombre': nombre, 'categoria': cat, 'proveedor': prov, 'precio_compra': Decimal(compra), 'precio_venta': Decimal(venta), 'stock_minimo': Decimal(minimo)})
            if p.stock_actual == 0:
                mov = Movimiento.objects.create(tipo=Movimiento.ENTRADA, proveedor=prov, referencia='DEMO-ENTRADA')
                DetalleMovimiento.objects.create(movimiento=mov, producto=p, cantidad=Decimal('25'), costo_unitario=Decimal(compra))
        self.stdout.write(self.style.SUCCESS('Datos de demostración cargados.'))
