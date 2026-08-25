from django import forms
from Categoria.models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}
