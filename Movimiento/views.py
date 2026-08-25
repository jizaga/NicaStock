from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.shortcuts import redirect, render

from Movimiento.models import Movimiento, DetalleMovimiento
from Movimiento.forms import MovimientoForm, DetalleFormSet


@login_required
@permission_required('inventario.add_movimiento', raise_exception=True)
def movimiento_nuevo(request):
    form = MovimientoForm(request.POST or None)
    formset = DetalleFormSet(request.POST or None, prefix='detalles')
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            movimiento = form.save(commit=False); movimiento.usuario = request.user; movimiento.save()
            try:
                for detalle in formset.cleaned_data:
                    if detalle.get('producto'): DetalleMovimiento.objects.create(movimiento=movimiento, **detalle)
            except ValueError as exc:
                transaction.set_rollback(True); form.add_error(None, str(exc))
                return render(request, 'inventario/movimiento_form.html', {'form': form, 'formset': formset})
        messages.success(request, 'Movimiento registrado y stock actualizado.'); return redirect('movimientos')
    return render(request, 'inventario/movimiento_form.html', {'form': form, 'formset': formset})

@login_required
def movimientos(request):
    return render(request, 'inventario/movimientos.html', {'movimientos': Movimiento.objects.select_related('proveedor', 'cliente', 'usuario').prefetch_related('detalles__producto')[:100]})
