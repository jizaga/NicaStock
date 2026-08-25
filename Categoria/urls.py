from django.urls import path
from Categoria import views


urlpatterns = [
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/nueva/', views.categoria_editar, name='categoria_nueva'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),
    path('categorias/importar/', views.importar_categorias_csv, name='importar_categorias_csv'),
]
