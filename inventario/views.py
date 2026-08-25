import csv
from datetime import timedelta
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.db.models import Count, F
from django.db.models.functions import TruncDate
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CSVImportForm, CatalogoCSVImportForm

from Categoria.models import Categoria
from Proveedor.models import Proveedor
from Producto.models import Producto
from Movimiento.models import Movimiento



@login_required
def dashboard(request):
    bajos = Producto.objects.filter(activo=True, stock_actual__lte=F('stock_minimo'))
    desde = timezone.now() - timedelta(days=30)
    datos = (Movimiento.objects.filter(fecha__gte=desde).annotate(dia=TruncDate('fecha')).values('dia', 'tipo').annotate(total=Count('id')).order_by('dia'))
    labels = sorted({x['dia'].strftime('%d/%m') for x in datos})
    entradas = {x['dia'].strftime('%d/%m'): x['total'] for x in datos if x['tipo'] == Movimiento.ENTRADA}
    salidas = {x['dia'].strftime('%d/%m'): x['total'] for x in datos if x['tipo'] == Movimiento.SALIDA}
    return render(request, 'inventario/dashboard.html', {'productos': Producto.objects.filter(activo=True).count(), 'bajos': bajos, 'movimientos_hoy': Movimiento.objects.filter(fecha__date=timezone.localdate()).count(), 'labels': labels, 'entradas': [entradas.get(x, 0) for x in labels], 'salidas': [salidas.get(x, 0) for x in labels]})


def editar_catalogo(request, modelo, form_class, pk, destino, etiqueta):
    instancia = get_object_or_404(modelo, pk=pk) if pk else None
    permiso = f'inventario.{"change" if instancia else "add"}_{modelo._meta.model_name}'
    if not request.user.has_perm(permiso):
        return HttpResponseForbidden('No tiene permiso para realizar esta acción.')
    form = form_class(request.POST or None, instance=instancia)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'{etiqueta} guardado correctamente.')
        return redirect(destino)
    return render(request, 'inventario/catalogo_form.html', {'form': form, 'instancia': instancia, 'etiqueta': etiqueta, 'destino': destino})


def eliminar_catalogo(request, modelo, pk, destino, etiqueta):
    if not request.user.has_perm(f'inventario.delete_{modelo._meta.model_name}'):
        return HttpResponseForbidden('No tiene permiso para eliminar.')
    instancia = get_object_or_404(modelo, pk=pk)
    if request.method == 'POST':
        try:
            instancia.delete()
            messages.success(request, f'{etiqueta} eliminado correctamente.')
        except ProtectedError:
            messages.error(request, f'No se puede eliminar: hay productos o movimientos asociados a este {etiqueta.lower()}.')
        return redirect(destino)
    return render(request, 'inventario/catalogo_confirmar_eliminar.html', {'instancia': instancia, 'etiqueta': etiqueta, 'destino': destino})


def importar_catalogo_csv(request, modelo, campos, destino, etiqueta):
    permisos = [f'inventario.add_{modelo._meta.model_name}', f'inventario.change_{modelo._meta.model_name}']
    if not all(request.user.has_perm(permiso) for permiso in permisos):
        return HttpResponseForbidden('Se requieren permisos para crear y modificar registros antes de importar.')
    form = CatalogoCSVImportForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        try:
            filas = csv.DictReader(form.cleaned_data['archivo'].read().decode('utf-8-sig').splitlines())
            if not filas.fieldnames or 'nombre' not in filas.fieldnames:
                raise ValueError('El archivo debe incluir la columna obligatoria: nombre.')
            encabezados_invalidos = set(filas.fieldnames) - set(campos)
            if encabezados_invalidos:
                raise ValueError('Columnas no permitidas: ' + ', '.join(sorted(encabezados_invalidos)))
            cantidad = 0
            with transaction.atomic():
                for numero, fila in enumerate(filas, 2):
                    datos = {campo: (fila.get(campo) or '').strip() for campo in campos}
                    if not datos['nombre']:
                        raise ValueError(f'Fila {numero}: el nombre es obligatorio.')
                    modelo.objects.update_or_create(nombre=datos.pop('nombre'), defaults=datos)
                    cantidad += 1
            messages.success(request, f'{cantidad} {etiqueta.lower()}(s) importado(s) o actualizado(s).')
            return redirect(destino)
        except (UnicodeDecodeError, ValueError) as exc:
            form.add_error('archivo', str(exc))
    return render(request, 'inventario/importar_catalogo.html', {'form': form, 'etiqueta': etiqueta, 'campos': campos, 'destino': destino})


@login_required
@permission_required('inventario.importar_productos', raise_exception=True)
def importar_csv(request):
    form = CSVImportForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        try:
            filas = csv.DictReader(form.cleaned_data['archivo'].read().decode('utf-8-sig').splitlines())
            obligatorias = {'codigo','nombre','categoria','proveedor','precio_compra','precio_venta','stock_minimo'}
            if not filas.fieldnames or not obligatorias.issubset(set(filas.fieldnames)): raise ValueError('Encabezados requeridos: ' + ', '.join(sorted(obligatorias)))
            cantidad = 0
            with transaction.atomic():
                for n, fila in enumerate(filas, 2):
                    try:
                        categoria, _ = Categoria.objects.get_or_create(nombre=fila['categoria'].strip())
                        proveedor, _ = Proveedor.objects.get_or_create(nombre=fila['proveedor'].strip())
                        Producto.objects.update_or_create(codigo=fila['codigo'].strip(), defaults={'nombre': fila['nombre'].strip(), 'categoria': categoria, 'proveedor': proveedor, 'precio_compra': Decimal(fila['precio_compra']), 'precio_venta': Decimal(fila['precio_venta']), 'stock_minimo': Decimal(fila['stock_minimo']), 'activo': True})
                        cantidad += 1
                    except (InvalidOperation, ValueError, KeyError) as exc: raise ValueError(f'Fila {n}: {exc}')
            messages.success(request, f'{cantidad} producto(s) importado(s) o actualizado(s).'); return redirect('productos')
        except (UnicodeDecodeError, ValueError) as exc: form.add_error('archivo', str(exc))
    return render(request, 'inventario/importar.html', {'form': form})
