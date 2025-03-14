from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EventoCapacitacion(models.Model):
    """Registro de eventos o capacitaciones con visitantes"""
    nombre = models.CharField(max_length=255)
    organizador = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cantidad_visitantes = models.IntegerField()
    usuario_registro = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class EventoVisitante(models.Model):
    """Registro de los visitantes que asisten a eventos/capacitaciones"""
    id_evento = models.ForeignKey(EventoCapacitacion, on_delete=models.CASCADE)
    nombre_visitante = models.CharField(max_length=255)
    documento_identificacion = models.CharField(max_length=50)
    entrada = models.BooleanField(default=0)
    hora_entrada = models.TimeField(null=True, blank=True)
    salida = models.BooleanField(default=0)
    hora_salida = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_visitante} - {self.id_evento.nombre}"
