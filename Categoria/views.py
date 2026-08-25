from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Categoria.models import Categoria
from Categoria.forms import CategoriaForm
from inventario.views import editar_catalogo, eliminar_catalogo, importar_catalogo_csv


@login_required
def categorias(request):
    return render(request, 'inventario/categorias.html', {'categorias': Categoria.objects.all()})

@login_required
def categoria_editar(request, pk=None):
    return editar_catalogo(request, Categoria, CategoriaForm, pk, 'categorias', 'Categoría')

@login_required
def categoria_eliminar(request, pk):
    return eliminar_catalogo(request, Categoria, pk, 'categorias', 'Categoría')

@login_required
def importar_categorias_csv(request):
    return importar_catalogo_csv(request, Categoria, ['nombre', 'descripcion'], 'categorias', 'Categoría')

