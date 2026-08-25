from django.urls import path
from Producto import views

urlpatterns = [
    path('productos/', views.productos, name='productos'),
    path('productos/nuevo/', views.producto_editar, name='producto_nuevo'),
    path('productos/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
]
