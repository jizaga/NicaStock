from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from Cliente import views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('cuentas/ingresar/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('cuentas/salir/', auth_views.LogoutView.as_view(), name='logout'),
    path('importar/', views.importar_csv, name='importar_csv'),
    path('', include('Producto.urls')),
    path('', include('Proveedor.urls')),
    path('', include('Categoria.urls')),
    path('', include('Movimiento.urls')),
]
