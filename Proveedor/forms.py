from django import forms
from Proveedor.models import Proveedor


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion']
        widgets = {'direccion': forms.Textarea(attrs={'rows': 3})}
