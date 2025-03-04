from django.contrib import admin
from django.urls import path, include
from visitantes import views as vistasVisitantes
from usuarios import views as vistasUsuarios


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vistasVisitantes.index, name='inicio'),
    path('nuevaVisita/', vistasVisitantes.nuevaVisita, name='nuevavisita'),
    path('login/', vistasUsuarios.user_login, name='login'),  
    path("logout/", vistasUsuarios.user_logout, name="logout"),  
    path('usuarios/', vistasUsuarios.user_list, name='usuarios'), 
    path('usuarios/cambiar_estado/<int:userId>/', vistasUsuarios.cambiar_estado_usuario, name='cambiar_estado_usuario'),

]
    

