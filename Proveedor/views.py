from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Proveedor.models import Proveedor
from Proveedor.forms import ProveedorForm
from inventario.views import editar_catalogo, eliminar_catalogo, importar_catalogo_csv


@login_required
def proveedores(request):
    return render(request, 'inventario/proveedores.html', {'proveedores': Proveedor.objects.all()})

@login_required
def proveedor_editar(request, pk=None):
    return editar_catalogo(request, Proveedor, ProveedorForm, pk, 'proveedores', 'Proveedor')

@login_required
def proveedor_eliminar(request, pk):
    return eliminar_catalogo(request, Proveedor, pk, 'proveedores', 'Proveedor')

@login_required
def importar_proveedores_csv(request):
    return importar_catalogo_csv(request, Proveedor, ['nombre', 'contacto', 'telefono', 'email', 'direccion'], 'proveedores', 'Proveedor')
