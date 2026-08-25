from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuentas/ingresar/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('cuentas/salir/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('inventario.urls')),
    path('', include('Producto.urls')),
    path('', include('Proveedor.urls')),
    path('', include('Categoria.urls')),
    path('', include('Movimiento.urls')),
] + debug_toolbar_urls()
