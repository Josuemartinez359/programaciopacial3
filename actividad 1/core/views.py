from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import logout

def login(request):
    """Mostrar formulario de login y procesar POST para iniciar sesión."""
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('clave')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            # Redirigir al dashboard de bienvenida
            return redirect('bienvenido')
        else:
            messages.error(request, 'Credenciales inválidas, intenta de nuevo.')

    return render(request, 'core/login.html')



def registrar(request):
    """Mostrar formulario de registro."""
    return render(request, 'core/registrar.html')


def guardar_usuario(request):
    if request.method != 'POST':
        return redirect('registrar_usuario')

    identificacion = request.POST.get('identificacion')
    apodo = request.POST.get('apodo')
    clave = request.POST.get('clave')
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')

    username = apodo or identificacion
    if not username or not clave:
        messages.error(request, 'Faltan datos obligatorios (usuario/clave).')
        return redirect('registrar_usuario')

    # Evitar usuarios duplicados
    if User.objects.filter(username=username).exists():
        messages.error(request, 'El usuario ya existe. Elige otro apodo o identificación.')
        return redirect('registrar_usuario')

    # Crear usuario
    user = User.objects.create_user(
        username=username,
        password=clave,
        first_name=nombre or '',
        last_name=apellido or ''
    )

    # Crear perfil asociado (solo si no existe)
    UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'identificacion': identificacion or '',
            'apodo': apodo or '',
        }
    )

    messages.success(request, 'Usuario registrado correctamente.')
    return redirect('login')


def bienvenido(request):
    return render(request, 'core/bienvenido.html')




def cerrar_sesion(request):
    logout(request)
    return redirect('login')
