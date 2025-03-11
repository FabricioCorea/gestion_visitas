from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from visitantes.models import *
# Vista de inicio
@login_required
def index(request):
    return render(request, 'inicio/inicio.html')
# Vista de visitas
@login_required
def visitas(request):
    visitas = Visita.objects.all()
    return render(request, 'visitantes/mis-visitas.html', {
        "visitas": visitas})
# Vista de agregar visita
@login_required
def nuevaVisita(request):
    if request.method == "POST":
        # Obtener datos del formulario
        visitante_nombres = request.POST.getlist("visitante_nombre[]")
        visitante_documentos = request.POST.getlist("visitante_documento[]")
        motivo_id = request.POST.get("motivo")
        area_departamento_id = request.POST.get("area_departamento")
        persona_visitada = request.POST.get("persona_visitada")
        fecha_visita = request.POST.get("fecha_visita")
        hora_ingreso = request.POST.get("hora_ingreso")
        hora_salida = request.POST.get("hora_salida")
        foto_documento_identificacion = request.FILES.get("foto_documento_identificacion")

        # Crear código único de la visita
        cod_visita = uuid.uuid4().hex[:10]

        # Guardar cada visitante ingresado
        visitantes_guardados = []
        for nombre, documento in zip(visitante_nombres, visitante_documentos):
            visitante, created = Visitante.objects.get_or_create(
                documento_identificacion=documento,
                defaults={"nombre": nombre}
            )
            # Asociar el visitante con la visita 
            visitante.cod_visita = cod_visita
            visitante.save()

            visitantes_guardados.append(visitante)

        # Crear la visita con los datos recopilados
        visita = Visita.objects.create(
            cod_visita=cod_visita,
            visitante=", ".join([v.nombre for v in visitantes_guardados]),  # Lista de nombres concatenados
            motivo=MotivoVisita.objects.get(id=motivo_id).descripcion,
            area_departamento=AreaDepto.objects.get(id=area_departamento_id).nombre,
            persona_visitada=persona_visitada,
            fecha_visita=fecha_visita,
            hora_ingreso=hora_ingreso,
            hora_salida=hora_salida,
            usuario_registro=request.user.username,
            foto_documento_identificacion=foto_documento_identificacion
        )

        messages.success(request, "Visita registrada correctamente.")
        return redirect("nueva_visita")

    # Obtener datos para el formulario
    motivos = MotivoVisita.objects.filter(estado="activo")
    areas = AreaDepto.objects.filter(estado="activo")

    return render(request, "visitantes/nueva-visita.html", {
        "motivos": motivos,
        "areas": areas
    })
@login_required
def editarVisita(request):
    if request.method == "POST":
        # Obtener datos del formulario
        visitante_nombres = request.POST.getlist("visitante_nombre[]")
        visitante_documentos = request.POST.getlist("visitante_documento[]")
        motivo_id = request.POST.get("motivo")
        area_departamento_id = request.POST.get("area_departamento")
        persona_visitada = request.POST.get("persona_visitada")
        fecha_visita = request.POST.get("fecha_visita")
        hora_ingreso = request.POST.get("hora_ingreso")
        hora_salida = request.POST.get("hora_salida")
        foto_documento_identificacion = request.FILES.get("foto_documento_identificacion")

        # Crear código único de la visita
        cod_visita = uuid.uuid4().hex[:10]

        # Guardar cada visitante ingresado
        visitantes_guardados = []
        for nombre, documento in zip(visitante_nombres, visitante_documentos):
            visitante, created = Visitante.objects.get_or_create(
                documento_identificacion=documento,
                defaults={"nombre": nombre}
            )
            # Asociar el visitante con la visita 
            visitante.cod_visita = cod_visita
            visitante.save()

            visitantes_guardados.append(visitante)

        # Crear la visita con los datos recopilados
        visita = Visita.objects.create(
            cod_visita=cod_visita,
            visitante=", ".join([v.nombre for v in visitantes_guardados]),  # Lista de nombres concatenados
            motivo=MotivoVisita.objects.get(id=motivo_id).descripcion,
            area_departamento=AreaDepto.objects.get(id=area_departamento_id).nombre,
            persona_visitada=persona_visitada,
            fecha_visita=fecha_visita,
            hora_ingreso=hora_ingreso,
            hora_salida=hora_salida,
            usuario_registro=request.user.username,
            foto_documento_identificacion=foto_documento_identificacion
        )

        messages.success(request, "Visita registrada correctamente.")
        return redirect("nueva_visita")

    # Obtener datos para el formulario
    motivos = MotivoVisita.objects.filter(estado="activo")
    areas = AreaDepto.objects.filter(estado="activo")

    return render(request, "visitantes/editar-visita.html", {
        "motivos": motivos,
        "areas": areas
    })

