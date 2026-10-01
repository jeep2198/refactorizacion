"""Menú principal: navegación por la aplicación."""

from ui import display


def menu_principal(app) -> None:
    """Menú principal de la aplicación."""
    while True:
        display.clear_screen()
        display.print_header("SISTEMA DE PELÍCULAS Y SERIES")
        print("1. Buscar película por título")
        print("2. Buscar por actor")
        print("3. Buscar series")
        print("4. Ver películas populares")
        print("5. Buscar por género")
        print("6. Ver favoritos")
        print("7. Ver historial")
        print("8. Ver estadísticas")
        print("9. Exportar datos")
        print("10. Importar datos")
        print("11. Configuración")
        print("12. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            _funcion_buscar_pelicula(app)
        elif opcion == "2":
            _funcion_buscar_actor(app)
        elif opcion == "3":
            _funcion_buscar_series(app)
        elif opcion == "4":
            _funcion_peliculas_populares(app)
        elif opcion == "5":
            _funcion_buscar_por_genero(app)
        elif opcion == "6":
            _funcion_ver_favoritos(app)
        elif opcion == "7":
            _funcion_ver_historial(app)
        elif opcion == "8":
            _funcion_estadisticas(app)
        elif opcion == "9":
            _funcion_exportar(app)
        elif opcion == "10":
            _funcion_importar(app)
        elif opcion == "11":
            _funcion_configuracion(app)
        elif opcion == "12":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")


def _funcion_buscar_pelicula(app) -> None:
    """Busca una película por título."""
    titulo = input("Ingrese el título de la película: ")
    print("Buscando...")

    pelicula = app.buscar_pelicula(titulo)
    display.mostrar_pelicula(pelicula)

    if pelicula is not None:
        app.agregar_al_historial(pelicula)
        opcion = input("\n¿Agregar a favoritos? (s/n): ")
        if opcion.lower() == "s":
            if app.agregar_a_favoritas(pelicula):
                print("¡Agregada a favoritos!")
            else:
                print("Ya está en favoritos")

    input("\nPresione Enter para continuar...")


def _funcion_buscar_actor(app) -> None:
    """Busca películas por actor."""
    actor = input("Ingrese el nombre del actor: ")
    print("Buscando películas del actor...")

    peliculas = app.buscar_peliculas_por_actor(actor)

    if peliculas:
        display.mostrar_lista_peliculas(peliculas)
        opcion = input("\nSeleccione una película para ver detalles (0 para volver): ")
        if opcion.isdigit():
            indice = int(opcion) - 1
            if 0 <= indice < len(peliculas):
                detalles = app.buscar_pelicula(peliculas[indice].title)
                display.mostrar_pelicula(detalles)
    else:
        print("No se encontraron películas para ese actor")

    input("\nPresione Enter para continuar...")


def _funcion_buscar_series(app) -> None:
    """Busca series por nombre."""
    nombre = input("Ingrese el nombre de la serie: ")
    print("Buscando series...")

    series = app.buscar_series(nombre)

    if series:
        display.mostrar_lista_series(series)
        opcion = input("\nSeleccione una serie para ver detalles (0 para volver): ")
        if opcion.isdigit():
            indice = int(opcion) - 1
            if 0 <= indice < len(series):
                id_serie = series[indice].id
                detalles = app.obtener_detalles_serie(id_serie)
                display.mostrar_serie(detalles)
    else:
        print("No se encontraron series")

    input("\nPresione Enter para continuar...")


def _funcion_peliculas_populares(app) -> None:
    """Muestra películas populares del catálogo local."""
    display.print_header("PELÍCULAS POPULARES")
    display.mostrar_lista_peliculas(app.obtener_peliculas_populares())
    input("\nPresione Enter para continuar...")


def _funcion_buscar_por_genero(app) -> None:
    """Busca películas por género."""
    print("Géneros disponibles: acción, comedia")
    genero = input("Ingrese el género: ")
    display.mostrar_lista_peliculas(app.buscar_peliculas_por_genero(genero))
    input("\nPresione Enter para continuar...")


def _funcion_ver_favoritos(app) -> None:
    """Muestra las películas favoritas."""
    display.print_header("MIS FAVORITOS")
    if app.favoritas:
        for i, pelicula in enumerate(app.favoritas, start=1):
            print(f"{i}. {pelicula.title}")

        opcion = input("\n¿Desea eliminar alguna? (número o Enter para volver): ")
        if opcion.isdigit():
            indice = int(opcion) - 1
            if 0 <= indice < len(app.favoritas):
                titulo = app.favoritas[indice].title
                if app.eliminar_de_favoritas(titulo):
                    print("Eliminada de favoritos")
    else:
        print("No tienes películas favoritas")

    input("\nPresione Enter para continuar...")


def _funcion_ver_historial(app) -> None:
    """Muestra el historial de búsquedas."""
    display.print_header("HISTORIAL DE BÚSQUEDAS")
    if app.historial:
        for i, registro in enumerate(app.historial, start=1):
            print(f"{i}. {registro['titulo']}")

        opcion = input("\n¿Limpiar historial? (s/n): ")
        if opcion.lower() == "s":
            app.limpiar_historial()
            print("Historial limpiado")
    else:
        print("No hay historial")

    input("\nPresione Enter para continuar...")


def _funcion_estadisticas(app) -> None:
    """Muestra las estadísticas de uso."""
    display.print_header("ESTADÍSTICAS")
    stats = app.obtener_estadisticas()
    print(f"Total favoritas: {stats['total_favoritas']}")
    print(f"Total historial: {stats['total_historial']}")
    input("\nPresione Enter para continuar...")


def _funcion_exportar(app) -> None:
    """Exporta los datos a JSON."""
    nombre = input("Nombre del archivo (sin extensión): ")
    try:
        app.exportar_a_json(f"{nombre}.json")
        print(f"Exportado a {nombre}.json")
    except OSError as err:
        print(f"Error al exportar archivo: {err}")
    input("\nPresione Enter para continuar...")


def _funcion_importar(app) -> None:
    """Importa datos desde un archivo JSON."""
    nombre = input("Nombre del archivo (sin extensión): ")
    try:
        app.importar_de_json(f"{nombre}.json")
        print(f"Importado desde {nombre}.json")
    except (OSError, ValueError) as err:
        print(f"Error al importar archivo: {err}")
    input("\nPresione Enter para continuar...")


def _funcion_configuracion(app) -> None:
    """Cambia la configuración de la aplicación."""
    display.print_header("CONFIGURACIÓN")
    print(f"1. Debug: {app.config['debug']}")
    print(f"2. Verbose: {app.config['verbose']}")
    print(f"3. Timeout: {app.config['timeout']}")

    opcion = input("\nSeleccione opción a cambiar (0 para volver): ")
    if opcion == "1":
        app.config["debug"] = not app.config["debug"]
        print(f"Debug ahora es: {app.config['debug']}")
    elif opcion == "2":
        app.config["verbose"] = not app.config["verbose"]
        print(f"Verbose ahora es: {app.config['verbose']}")
    elif opcion == "3":
        nuevo = input("Nuevo timeout: ")
        if nuevo.isdigit():
            app.config["timeout"] = int(nuevo)
            print(f"Timeout ahora es: {app.config['timeout']}")
        else:
            print("Timeout inválido")

    input("\nPresione Enter para continuar...")
