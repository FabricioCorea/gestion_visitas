from django.contrib import admin
from django.urls import path
from visitantes import views as vistasVisitantes
from usuarios import views as vistasUsuarios

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vistasVisitantes.index, name='inicio'),
    path('MisVisitas/', vistasVisitantes.visitas, name='mis_visitas'),
    path('nuevaVisita/', vistasVisitantes.nuevaVisita, name='nueva_visita'),
    path('editarVisita/', vistasVisitantes.nuevaVisita, name='editar_visita'),
    path('login/', vistasUsuarios.user_login, name='login'),  
    path('logout/', vistasUsuarios.user_logout, name='logout'),  
    path('usuarios/', vistasUsuarios.user_list, name='usuarios'), 
    path('usuarios/cambiar_estado/<int:user_id>/', vistasUsuarios.toggle_user_status, name='toggle_user_status'),
    path('usuarios/agregar/', vistasUsuarios.add_user, name='agregar_usuario'),
    path('usuarios/editar/', vistasUsuarios.edit_user, name='editar_usuario'),
    path('usuarios/eliminar/<int:user_id>/', vistasUsuarios.delete_user, name='eliminar_usuario'),
]
