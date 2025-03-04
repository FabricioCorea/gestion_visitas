from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.db.models import Q
from django.utils.timezone import now
import json
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
@csrf_exempt
def toggle_user_status(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active  # Alternar estado
        user.save()
        return JsonResponse({"success": True, "new_status": user.is_active})
    return JsonResponse({"success": False}, status=400)
