from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Producto.models import Producto
from Producto.forms import ProductoForm
from Categoria.models import Categoria
from django.db.models import Q
from Proveedor.models import Proveedor


@login_required
def productos(request):
    qs = Producto.objects.select_related('categoria', 'proveedor').all()
    categoria, proveedor, texto = request.GET.get('categoria'), request.GET.get('proveedor'), request.GET.get('q', '')
    if categoria: qs = qs.filter(categoria_id=categoria)
    if proveedor: qs = qs.filter(proveedor_id=proveedor)
    if texto: qs = qs.filter(Q(nombre__icontains=texto) | Q(codigo__icontains=texto))
    return render(request, 'inventario/productos.html', {'productos': qs, 'categorias': Categoria.objects.all(), 'proveedores': Proveedor.objects.all()})

@login_required
@permission_required('inventario.change_producto', raise_exception=True)
def producto_editar(request, pk=None):
    instancia = get_object_or_404(Producto, pk=pk) if pk else None
    form = ProductoForm(request.POST or None, instance=instancia)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Producto guardado correctamente.'); return redirect('productos')
    return render(request, 'inventario/producto_form.html', {'form': form, 'editar': bool(pk)})
