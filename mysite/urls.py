from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN
    path('', views.login, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    # REGISTRO
    path('registrar/', views.registrar, name='registrar_usuario'),
    path('guardar_usuario/', views.guardar_usuario, name='guardar_usuario'),

    # ADMINISTRACIÓN DE USUARIOS
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('actualizar_usuario/<int:user_id>/', views.actualizar_usuario, name='actualizar_usuario'),

    # BIENVENIDO
    path('bienvenido/', views.bienvenido, name='bienvenido'),

    # VALIDAR ADMIN
    path('validar_admin/', views.validar_admin, name='validar_admin'),

    # PANEL DE ADMINISTRADOR (ESTE FALTABA)
    path('admin_panel/', views.admin_panel, name='admin_panel'),
]
