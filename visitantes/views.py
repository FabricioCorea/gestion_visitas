from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url="login")

# Vista de inicio
def index(request):
    return render(request, 'inicio/inicio.html')

@login_required(login_url="login")
# Vista de nueva visita
def nuevaVisita(request):
    return render(request, 'visitantes/nueva-visita.html')
