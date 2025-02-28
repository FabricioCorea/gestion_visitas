from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

# Vista de login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Verificar si el usuario existe antes de autenticarlo
            user = User.objects.get(username=username)
            if not user.is_active:
                messages.warning(request, "Tu cuenta está inactiva. Contacta al administrador.")
                return render(request, "auth/login.html")
        except User.DoesNotExist:
            user = None

        # Autenticar usuario solo si existe y está activo
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Iniciar sesión
            return redirect("inicio")  # Redirige a la página principal
        else:
            messages.warning(request, "Usuario o contraseña incorrectos.")

    return render(request, "auth/login.html")

# Vista de logout
def user_logout(request):
    auth_logout(request)
    return redirect("login")  # Redirige a la página de login

# Vista de lista de usuarios con restricciones de grupo
@login_required
def user_list(request):
    is_super_admin_group = request.user.groups.filter(name='super_admin').exists()
    is_admin_group = request.user.groups.filter(name='admin_group').exists()

    # Filtrar usuarios según el grupo del usuario autenticado
    if is_super_admin_group:
        users = User.objects.prefetch_related('groups').all()  # ✅ Super Admin ve todos los usuarios
    elif is_admin_group:
        users = User.objects.prefetch_related('groups').exclude(groups__name="super_admin")  # ✅ Admin NO ve super_admin
    else:
        messages.error(request, "Acceso no permitido.")
        return redirect("inicio")  # ✅ Bloquear acceso a otros roles

    return render(request, 'auth/user_list.html', {
        'users': users,
        'is_super_admin_group': is_super_admin_group,
        'is_admin_group': is_admin_group
    })

# Vista para cambiar estado del usuario (Activo/Inactivo)
@login_required
def cambiar_estado_usuario(request, user_id):
    user = User.objects.get(id=user_id)

    # Solo Super Admin o Admin pueden cambiar estado
    if request.user.groups.filter(name="super_admin").exists() or request.user.groups.filter(name="admin_group").exists():
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "No tienes permisos para realizar esta acción."})
