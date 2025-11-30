from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login, name='login'),  # Página inicial

    # Registro
    path('registrar/', views.registrar, name='registrar_usuario'),
    path('guardar_usuario/', views.guardar_usuario, name='guardar_usuario'),

    # Bienvenida y logout
    path('bienvenido/', views.bienvenido, name='bienvenido'),
    path('logout/', views.cerrar_sesion, name='logout'),
]
