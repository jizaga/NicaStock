from django import forms
from django.forms import formset_factory
from Movimiento.models import Movimiento
from Producto.models import Producto
from decimal import Decimal

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['tipo', 'referencia', 'proveedor', 'cliente', 'observaciones']
        widgets = {'observaciones': forms.Textarea(attrs={'rows': 2})}
    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
        if tipo == Movimiento.ENTRADA and not cleaned.get('proveedor'): self.add_error('proveedor', 'Seleccione el proveedor.')
        if tipo == Movimiento.SALIDA and not cleaned.get('cliente'): self.add_error('cliente', 'Seleccione el cliente.')
        return cleaned

class DetalleForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.filter(activo=True), required=False)
    cantidad = forms.DecimalField(min_value=Decimal('0.01'), decimal_places=2, required=False)
    costo_unitario = forms.DecimalField(min_value=Decimal('0'), decimal_places=2, required=False)
    def clean(self):
        data = super().clean()
        values = [data.get('producto'), data.get('cantidad'), data.get('costo_unitario')]
        if any(v is not None for v in values) and not all(v is not None for v in values):
            raise forms.ValidationError('Complete producto, cantidad y costo en cada línea.')
        return data
DetalleFormSet = formset_factory(DetalleForm, extra=5, min_num=1, validate_min=True)
