"""Fachada de la aplicación de películas y series.

Delega en los submódulos de responsabilidad única:
  - api.omdb / api.tvmaze: clientes HTTP
  - services: estado (favoritas, historial, caché) y negocio
  - models: modelos de datos
"""

import logging

from api.omdb import OmdbClient
from api.tvmaze import TVMazeClient
from services import MovieService, SeriesService

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "debug": False,
    "verbose": False,
    "timeout": 10,
    "max_retries": 3,
}


class MovieApp:
    """Fachada que compone los servicios de películas y series."""

    def __init__(
        self, api_key_omdb: str = "trilogy", config: dict | None = None
    ) -> None:
        self.config = dict(DEFAULT_CONFIG)
        if config:
            self.config.update(config)

        cliente_omdb = OmdbClient(
            api_key=api_key_omdb or "",
            timeout=self.config["timeout"],
            max_retries=self.config["max_retries"],
            debug=self.config["debug"],
            verbose=self.config["verbose"],
        )
        cliente_tvmaze = TVMazeClient(
            timeout=self.config["timeout"],
            max_retries=self.config["max_retries"],
            debug=self.config["debug"],
            verbose=self.config["verbose"],
        )
        self.movie_service = MovieService(cliente_omdb)
        self.series_service = SeriesService(cliente_tvmaze)

    # ------------------------------------------------------- Estado delegado
    @property
    def favoritas(self):
        """Películas favoritas (models.Movie)."""
        return self.movie_service.favoritas

    @property
    def historial(self):
        """Historial de búsquedas."""
        return self.movie_service.historial

    # ------------------------------------------------------------- Películas
    def buscar_pelicula(self, titulo: str):
        """Busca una película por título usando caché."""
        return self.movie_service.buscar_pelicula(titulo)

    def buscar_peliculas_por_actor(self, actor: str):
        """Busca películas por actor."""
        return self.movie_service.buscar_peliculas_por_actor(actor)

    @staticmethod
    def obtener_peliculas_populares():
        """Catálogo local de películas populares."""
        return MovieService.obtener_peliculas_populares()

    @staticmethod
    def buscar_peliculas_por_genero(genero: str):
        """Películas de prueba según el género."""
        return MovieService.buscar_peliculas_por_genero(genero)

    # ---------------------------------------------------------------- Series
    def buscar_series(self, nombre: str):
        """Busca series por nombre usando caché."""
        return self.series_service.buscar_series(nombre)

    def obtener_detalles_serie(self, id_serie: int):
        """Obtiene los detalles de una serie por id."""
        return self.series_service.obtener_detalles_serie(id_serie)

    # --------------------------------------------------------- Favoritas
    def agregar_a_favoritas(self, pelicula) -> bool:
        """Agrega una película a favoritas si no existe."""
        return self.movie_service.agregar_a_favoritas(pelicula)

    def eliminar_de_favoritas(self, titulo: str) -> bool:
        """Elimina una película de favoritas por título."""
        return self.movie_service.eliminar_de_favoritas(titulo)

    # --------------------------------------------------------- Historial
    def agregar_al_historial(self, pelicula) -> None:
        """Registra la búsqueda en el historial."""
        self.movie_service.agregar_al_historial(pelicula)

    def limpiar_historial(self) -> None:
        """Limpia el historial de búsquedas."""
        self.movie_service.limpiar_historial()

    # ------------------------------------------------------- Estadísticas
    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas básicas de uso."""
        return self.movie_service.obtener_estadisticas()

    # -------------------------------------------------------- Persistencia
    def exportar_a_json(self, nombre_archivo: str) -> None:
        """Exporta favoritas e historial a un archivo JSON."""
        self.movie_service.exportar_a_json(nombre_archivo)

    def importar_de_json(self, nombre_archivo: str) -> None:
        """Importa favoritas e historial desde un archivo JSON."""
        self.movie_service.importar_de_json(nombre_archivo)
