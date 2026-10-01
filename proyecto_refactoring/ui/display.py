"""Presentación: formato y salida de datos en consola."""

import sys

CAMPOS_PELICULA = (
    ("Título", "Title"),
    ("Año", "Year"),
    ("Rating IMDB", "imdbRating"),
    ("Género", "Genre"),
    ("Director", "Director"),
    ("Actores", "Actors"),
    ("Trama", "Plot"),
    ("Idioma", "Language"),
    ("País", "Country"),
    ("Premios", "Awards"),
)


def clear_screen() -> None:
    """Limpia la pantalla de forma portable."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def print_separator(length: int = 60) -> None:
    """Imprime un separador."""
    print("=" * length)


def print_header(text: str) -> None:
    """Imprime un encabezado centrado."""
    print_separator()
    print(text.upper().center(60))
    print_separator()


def mostrar_pelicula(pelicula) -> None:
    """Muestra los datos de una película con valores por defecto."""
    print_separator()
    if pelicula is None:
        print("No se encontró la película")
        print_separator()
        return
    for etiqueta, clave in CAMPOS_PELICULA:
        print(f"{etiqueta}: {pelicula.get(clave, 'N/A')}")
    print_separator()


def mostrar_serie(serie) -> None:
    """Muestra los datos de una serie con valores por defecto."""
    print_separator()
    if serie is None:
        print("No se encontró la serie")
        print_separator()
        return
    print(f"Nombre: {serie.get('name', 'N/A')}")
    print(f"Idioma: {serie.get('language', 'N/A')}")
    print(f"Géneros: {serie.get('genres', [])}")
    print(f"Rating: {serie.get('rating', {}).get('average', 'N/A')}")
    print(f"Estado: {serie.get('status', 'N/A')}")

    resumen = str(serie.get("summary", "N/A"))
    if len(resumen) > 200:
        resumen = f"{resumen[:200]}..."
    print(f"Resumen: {resumen}")
    print_separator()


def mostrar_lista_peliculas(peliculas) -> None:
    """Muestra una lista indexada de películas (dict o modelos Movie)."""
    for i, pelicula in enumerate(peliculas, start=1):
        if not isinstance(pelicula, dict):
            print(f"{i}. {pelicula.title} ({pelicula.year}) - {pelicula.rating}")
        elif "titulo" in pelicula:
            ficha = pelicula["titulo"]
            print(f"{i}. {ficha} ({pelicula['anio']}) - {pelicula['rating']}")
        elif "Title" in pelicula:
            print(f"{i}. {pelicula['Title']} ({pelicula.get('Year', 'N/A')})")
        else:
            print(f"{i}. Película desconocida")


def mostrar_lista_series(series) -> None:
    """Muestra una lista indexada de series (dict o modelos Series)."""
    for i, serie in enumerate(series, start=1):
        if not isinstance(serie, dict):
            print(f"{i}. {serie.name} ({serie.status})")
        else:
            print(f"{i}. {serie.get('name', '')} ({serie.get('status', '')})")
