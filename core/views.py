from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from .models import UserProfile


# ------------------ LOGIN ------------------
def login(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        password = request.POST.get('clave')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('bienvenido')
        else:
            messages.error(request, 'Credenciales inválidas.')

    return render(request, 'core/login.html')


# ------------------ REGISTRO ------------------
def registrar(request):
    usuarios = []
    for u in User.objects.select_related('profile').all():
        perfil = getattr(u, 'profile', None)
        usuarios.append({
            'id': u.id,
            'identificacion': getattr(perfil, 'identificacion', ''),
            'apodo': getattr(perfil, 'apodo', ''),
            'nombre': u.first_name,
            'apellido': u.last_name,
            'email': u.email,
        })

    return render(request, 'core/registrar.html', {'usuarios': usuarios})


def guardar_usuario(request):
    if request.method != 'POST':
        return redirect('registrar_usuario')

    identificacion = request.POST.get('identificacion')
    apodo = request.POST.get('apodo')
    clave = request.POST.get('clave')
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    email = request.POST.get('email')

    username = apodo or identificacion

    if not username or not clave:
        messages.error(request, 'Usuario y clave son obligatorios.')
        return redirect('registrar_usuario')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'El usuario ya existe.')
        return redirect('registrar_usuario')

    user = User.objects.create_user(
        username=username,
        password=clave,
        first_name=nombre,
        last_name=apellido,
        email=email
    )

    # Crear o actualizar perfil
    UserProfile.objects.update_or_create(
        user=user,
        defaults={
            'identificacion': identificacion,
            'apodo': apodo,
        }
    )

    messages.success(request, 'Usuario registrado correctamente.')
    return redirect('login')


# ------------------ LISTAR USUARIOS ------------------
def listar_usuarios(request):
    usuarios = []
    for u in User.objects.select_related('profile').all():
        perfil = getattr(u, 'profile', None)
        usuarios.append({
            'id': u.id,
            'identificacion': getattr(perfil, 'identificacion', ''),
            'apodo': getattr(perfil, 'apodo', ''),
            'nombre': u.first_name,
            'apellido': u.last_name,
            'email': u.email,
        })

    return render(request, 'core/registrar.html', {'usuarios': usuarios})


# ------------------ ELIMINAR USUARIO ------------------
def eliminar_usuario(request, user_id):
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('listar_usuarios')

    try:
        u = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('listar_usuarios')

    if u.is_superuser:
        messages.error(request, 'No se puede eliminar un superusuario.')
        return redirect('listar_usuarios')

    nombre = u.username
    u.delete()

    messages.success(request, f'Usuario "{nombre}" eliminado.')
    return redirect('listar_usuarios')


# ------------------ BIENVENIDO ------------------
def bienvenido(request):
    return render(request, 'core/bienvenido.html')


# ------------------ VALIDAR ADMIN (FALTABA) ------------------
def validar_admin(request):
    if request.method == 'POST':
        clave = request.POST.get('clave_admin')

        # CONTRASEÑA DE ADMIN
        if clave == "admin123":
            return redirect('admin_panel')

        messages.error(request, 'Contraseña incorrecta.')
        return redirect('bienvenido')

    return redirect('bienvenido')


# ------------------ CERRAR SESIÓN ------------------
def cerrar_sesion(request):
    logout(request)
    return redirect('login')


# ------------------ EDITAR / ACTUALIZAR USUARIO ------------------
def editar_usuario(request, user_id):
    try:
        u = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('listar_usuarios')

    return render(request, 'core/editar_usuario.html', {'usuario': u})


def actualizar_usuario(request, user_id):
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('listar_usuarios')

    try:
        u = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
        return redirect('listar_usuarios')

    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')

    # Check username uniqueness (allow unchanged)
    if username and User.objects.exclude(pk=u.pk).filter(username=username).exists():
        messages.error(request, 'El nombre de usuario ya está en uso por otro usuario.')
        return redirect('editar_usuario', user_id=u.id)

    # Update fields
    if username:
        u.username = username

    u.email = email

    if password:
        u.set_password(password)

    u.save()
    messages.success(request, 'Usuario actualizado correctamente.')
    return redirect('listar_usuarios')


# ------------------ PANEL DE ADMINISTRACIÓN ------------------
def admin_panel(request):
    """Simple admin panel listing users and offering edit/delete links.

    Note: this is a minimal implementation — consider adding authentication/permissions.
    """
    usuarios = []
    for u in User.objects.select_related('profile').all():
        perfil = getattr(u, 'profile', None)
        usuarios.append({
            'id': u.id,
            'identificacion': getattr(perfil, 'identificacion', ''),
            'apodo': getattr(perfil, 'apodo', ''),
            'nombre': u.first_name,
            'apellido': u.last_name,
            'email': u.email,
        })

    return render(request, 'core/admin_panel.html', {'usuarios': usuarios})
