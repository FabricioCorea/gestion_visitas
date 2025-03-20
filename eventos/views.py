from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from visitantes.models import *
from eventos.models import *

@login_required
def eventos(request):
    eventos = EventoCapacitacion.objects.filter(usuario_registro=request.user.username)
    return render(request, 'eventos/mis-eventos.html', {
        "eventos": eventos})
@login_required
def nuevoEvento(request):
    if request.method == "POST":
        # Obtener datos del formulario
        visitante_nombres = request.POST.getlist("visitante_nombre[]")
        visitante_documentos = request.POST.getlist("visitante_documento[]")
        nombre = request.POST.get("nombre")
        organizador_id = request.POST.get("organizador")
        fecha_evento = request.POST.get("fecha_evento")
        hora_inicio = request.POST.get("hora_inicio")
        hora_fin = request.POST.get("hora_fin")

        # Calcular cantidad de visitantes dinámicamente
        cantidad_visitantes = len(visitante_nombres)

        # Crear el evento
        evento = EventoCapacitacion.objects.create(
            nombre=nombre,
            organizador=Colaborador.objects.get(id=organizador_id).nombre,
            fecha=fecha_evento,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            cantidad_visitantes=cantidad_visitantes,
            usuario_registro=request.user.username,
        )

        # Guardar cada visitante ingresado
        visitantes_guardados = []
        for nombre, documento in zip(visitante_nombres, visitante_documentos):
            visitante, created = EventoVisitante.objects.get_or_create(
                documento_identificacion=documento,
                defaults={"nombre_visitante": nombre, "id_evento": evento}
            )
            
            if not created:  # Si ya existía, asignarle el evento
                visitante.id_evento = evento
                visitante.save()
            visitantes_guardados.append(visitante)

        messages.success(request, "Evento registrado correctamente.")
        return redirect("mis_eventos")

    # Obtener datos para el formulario
    colaboradores = Colaborador.objects.filter(estado="activo")

    return render(request, "eventos/nuevo-evento.html", {
        "colaboradores": colaboradores
    })


@login_required
def editarEvento(request, evento_id):
    evento = get_object_or_404(EventoCapacitacion, id=evento_id)

    if request.method == "POST":
        # Obtener datos del formulario
        visitante_nombres = request.POST.getlist("visitante_nombre[]")
        visitante_documentos = request.POST.getlist("visitante_documento[]")
        nombre = request.POST.get("nombre")
        organizador_id = request.POST.get("organizador")
        fecha_evento = request.POST.get("fecha_evento")
        hora_inicio = request.POST.get("hora_inicio")
        hora_fin = request.POST.get("hora_fin")

        # Calcular cantidad de visitantes dinámicamente
        cantidad_visitantes = len(visitante_nombres)

        # Actualizar la información del evento
        evento.nombre = nombre
        evento.organizador = Colaborador.objects.get(id=organizador_id).nombre
        evento.fecha = fecha_evento
        evento.hora_inicio = hora_inicio
        evento.hora_fin = hora_fin
        evento.cantidad_visitantes = cantidad_visitantes
        evento.save()

        # Eliminar visitantes previos antes de agregar los nuevos
        EventoVisitante.objects.filter(id_evento=evento).delete()

        # Agregar los nuevos visitantes
        for nombre, documento in zip(visitante_nombres, visitante_documentos):
            EventoVisitante.objects.create(
                id_evento=evento,
                nombre_visitante=nombre,
                documento_identificacion=documento
            )

        messages.success(request, "Evento actualizado correctamente.")
        return redirect("mis_eventos")

    # Obtener datos para el formulario
    colaboradores = Colaborador.objects.filter(estado="activo")

    # Obtener visitantes del evento actual
    visitantes = EventoVisitante.objects.filter(id_evento=evento)

    return render(request, "eventos/editar-evento.html", {
        "evento": evento,
        "colaboradores": colaboradores,
        "visitantes": visitantes
    })

@login_required
def eliminarEvento(request, evento_id):
    if request.method == "POST":
        evento = get_object_or_404(EventoCapacitacion, id=evento_id)
        evento.delete()
        message = "Evento eliminado correctamente."
        return JsonResponse({"success": True, "message": message})
    
    return JsonResponse({"success": False, "message": "Método no permitido."}, status=400)
