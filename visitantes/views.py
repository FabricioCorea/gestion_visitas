from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages

@login_required(login_url="login")
# Vista de inicio
def index(request):
    return render(request, 'inicio/inicio.html')

@login_required(login_url="login")
# Vista de nueva visita
def nuevaVisita(request):
    return render(request, 'visitantes/nueva-visita.html')
