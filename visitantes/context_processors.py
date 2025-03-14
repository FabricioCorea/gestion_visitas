from django.urls import resolve

def active_menu(request):
    """
    Retorna el nombre del menú activo según la URL.
    """
    url_name = resolve(request.path_info).url_name  # Obtiene el nombre de la URL actual

    # Definir las secciones principales y sus subrutas
    active_pages = {
        "inicio": ["inicio"],
        "mis_visitas": ["mis_visitas", "nueva_visita", "editar_visita"],
        "usuarios": ["usuarios", "agregar_usuario", "editar_usuario", "eliminar_usuario"],
    }

    # Buscar qué sección principal coincide con la URL actual
    active_section = None
    for key, urls in active_pages.items():
        if url_name in urls:
            active_section = key
            break

    return {"active_page": active_section}
