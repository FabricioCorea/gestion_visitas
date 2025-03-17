from django.contrib import admin
from django.urls import path
from visitantes import views as vistasVisitantes
from usuarios import views as vistasUsuarios
from lista_negra import views as vistaListaNegra
from eventos import views as vistaEventos
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vistasVisitantes.index, name='inicio'),

    path('listaNegra', vistaListaNegra.listaNegra, name='lista_negra'),

    path('MisVisitas/', vistasVisitantes.visitas, name='mis_visitas'),
    path('nuevaVisita/', vistasVisitantes.nuevaVisita, name='nueva_visita'),
    path('editarVisita/<int:visita_id>/', vistasVisitantes.editarVisita, name='editar_visita'),
    path('mis_visitas/eliminar/<int:visita_id>/', vistasVisitantes.eliminarVisita, name='eliminar_visita'),

    path('MisEventos/', vistaEventos.eventos, name='mis_eventos'),
    path('nuevoEvento/', vistaEventos.nuevoEvento, name='nuevo_evento'),
    path('editarEvento/<int:evento_id>/', vistaEventos.editarEvento, name='editar_evento'),
    path('mis_eventos/eliminar/<int:evento_id>/', vistaEventos.eliminarEvento, name='eliminar_evento'),

    path('login/', vistasUsuarios.user_login, name='login'),  
    path('logout/', vistasUsuarios.user_logout, name='logout'),  

    path('usuarios/', vistasUsuarios.user_list, name='usuarios'), 
    path('usuarios/cambiar_estado/<int:user_id>/', vistasUsuarios.toggle_user_status, name='toggle_user_status'),
    path('usuarios/agregar/', vistasUsuarios.add_user, name='agregar_usuario'),
    path('usuarios/editar/', vistasUsuarios.edit_user, name='editar_usuario'),
    path('usuarios/eliminar/<int:user_id>/', vistasUsuarios.delete_user, name='eliminar_usuario'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)