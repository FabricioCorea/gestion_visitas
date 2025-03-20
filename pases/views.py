from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from visitantes.models import *
from pases.models import *

@login_required
def pases(request):
    is_super_admin_group = request.user.groups.filter(name='super_admin').exists()
    is_admin_group = request.user.groups.filter(name='admin_group').exists()
    is_recepcion_group = request.user.groups.filter(name='recepcion_group').exists()

    if is_super_admin_group or is_admin_group or is_recepcion_group:
        pases = PaseAcceso.objects.all()
    else:
        messages.error(request, "Acceso no permitido.")
        return redirect("inicio")
    return render(request, 'pases/pases.html', {"pases": pases})

@login_required
def nuevo_pase(request):
    if request.method == "POST":
        numero_pase = request.POST.get("numero_pase")
        lugares_acceso = request.POST.get("lugares_acceso")
        estado = request.POST.get("estado")
        estado_pase = request.POST.get("estado_pase")
        comentario_reporte = request.POST.get("comentario_reporte", "")
        
        PaseAcceso.objects.create(
            numero_pase=numero_pase,
            lugares_acceso=lugares_acceso,
            estado=estado,
            estado_pase=estado_pase,
            comentario_reporte=comentario_reporte
        )
        messages.success(request, "Pase registrado correctamente.")
        return redirect("pases")
    
    return redirect("pases")

@login_required
def editar_pase(request, pase_id):
    pase = get_object_or_404(PaseAcceso, id=pase_id)
    if request.method == "POST":
        pase.numero_pase = request.POST.get("numero_pase")
        pase.lugares_acceso = request.POST.get("lugares_acceso")
        pase.estado = request.POST.get("estado")
        pase.estado_pase = request.POST.get("estado_pase")
        pase.comentario_reporte = request.POST.get("comentario_reporte", "")
        pase.save()
        messages.success(request, "Pase actualizado correctamente.")
        return redirect("pases")
    
    return redirect("pases")

@login_required
def eliminar_pase(request, pase_id):
    if request.method == "POST":
        pase = get_object_or_404(PaseAcceso, id=pase_id)
        pase.delete()
        return JsonResponse({"success": True, "message": "Pase eliminado correctamente."})
    return JsonResponse({"success": False, "message": "Método no permitido."}, status=400)

@login_required
def cambiar_estado_pase(request, pase_id):
    if request.method == "POST":
        pase = get_object_or_404(PaseAcceso, id=pase_id)
        
        # Cambiar entre "activo" e "inactivo" en lugar de booleano
        if pase.estado == "activo":
            pase.estado = "inactivo"
        else:
            pase.estado = "activo"

        pase.save()
        
        message = "El estado del pase se cambió correctamente."
        return JsonResponse({"success": True, "new_status": pase.estado, "message": message})

    return JsonResponse({"success": False, "message": "Error al actualizar estado"}, status=400)
