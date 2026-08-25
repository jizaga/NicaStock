from django.urls import path
from Proveedor import views


urlpatterns = [
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/nuevo/', views.proveedor_editar, name='proveedor_nuevo'),
    path('proveedores/<int:pk>/editar/', views.proveedor_editar, name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_eliminar, name='proveedor_eliminar'),
    path('proveedores/importar/', views.importar_proveedores_csv, name='importar_proveedores_csv'),
]
