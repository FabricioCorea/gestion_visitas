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
    eventos = EventoCapacitacion.objects.all()
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
        cantidad_visitantes = request.POST.get("cantidad_visitantes")

        # Crear el evento
        evento = EventoCapacitacion.objects.create(
            nombre= nombre,
            organizador=Colaborador.objects.get(id= organizador_id).nombre,
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
            
            if not created:  # Si ya existía, hay que asignarle el evento
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