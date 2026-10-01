"""Punto de entrada de la aplicación de películas y series."""

import sys

from api_movies import MovieApp
from ui.menu import menu_principal


def main() -> None:
    """Crea la aplicación y arranca el menú principal."""
    app = MovieApp()
    menu_principal(app)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido")
        sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)
