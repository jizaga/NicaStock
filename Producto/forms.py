from django import forms
from Producto.models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'categoria', 'proveedor', 'precio_compra', 'precio_venta', 'stock_minimo', 'activo']
        widgets = {
            'precio_compra': forms.NumberInput(attrs={'step': '.01'}),
            'precio_venta': forms.NumberInput(attrs={'step': '.01'}),
            'stock_minimo': forms.NumberInput(attrs={'step': '.01'})
            }
