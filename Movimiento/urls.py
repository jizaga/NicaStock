from django.urls import path
from Movimiento import views

urlpatterns = [
    path('movimientos/', views.movimientos, name='movimientos'),
    path('movimientos/nuevo/', views.movimiento_nuevo, name='movimiento_nuevo'),
]
