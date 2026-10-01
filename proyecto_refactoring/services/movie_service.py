"""Servicio de películas: caché, favoritas, historial, estadísticas y persistencia."""

import json
import logging
import time

from api.omdb import OmdbClient
from models import Movie

from .catalog import PELICULAS_ACCION, PELICULAS_COMEDIA, PELICULAS_POPULARES

logger = logging.getLogger(__name__)


class MovieService:
    """Servicio de películas con estado encapsulado."""

    def __init__(self, api: OmdbClient | None = None) -> None:
        self._api = api or OmdbClient()
        self.favoritas: list[Movie] = []
        self.historial: list[dict] = []
        self._cache: dict[str, Movie] = {}

    # ------------------------------------------------------------- Búsquedas
    def buscar_pelicula(self, titulo: str) -> Movie | None:
        """Busca una película por título usando caché en memoria."""
        if not titulo or not titulo.strip():
            return None
        titulo = titulo.strip()
        if titulo in self._cache:
            return self._cache[titulo]
        try:
            pelicula = self._api.buscar_pelicula(titulo)
        except ConnectionError:
            return None
        if pelicula is not None:
            self._cache[titulo] = pelicula
        return pelicula

    def buscar_peliculas_por_actor(self, actor: str) -> list[Movie]:
        """Busca películas por actor."""
        if not actor or not actor.strip():
            return []
        try:
            return self._api.buscar_peliculas_por_actor(actor.strip())
        except ConnectionError:
            return []

    # ----------------------------------------------------------- Catálogos
    @staticmethod
    def obtener_peliculas_populares() -> list[dict]:
        """Retorna el catálogo local de películas populares."""
        return PELICULAS_POPULARES

    @staticmethod
    def buscar_peliculas_por_genero(genero: str) -> list[dict]:
        """Retorna películas de prueba según el género."""
        genero_norm = genero.strip().lower() if genero else ""
        if genero_norm == "accion":
            return PELICULAS_ACCION
        if genero_norm == "comedia":
            return PELICULAS_COMEDIA
        return PELICULAS_ACCION + PELICULAS_COMEDIA

    # --------------------------------------------------------- Favoritas
    def agregar_a_favoritas(self, pelicula: Movie) -> bool:
        """Agrega una película a favoritas si no existe."""
        titulo = pelicula.title
        if any(p.title == titulo for p in self.favoritas):
            return False
        self.favoritas.append(pelicula)
        return True

    def eliminar_de_favoritas(self, titulo: str) -> bool:
        """Elimina una película de favoritas por título."""
        for i, pelicula in enumerate(self.favoritas):
            if pelicula.title == titulo:
                self.favoritas.pop(i)
                return True
        return False

    # --------------------------------------------------------- Historial
    def agregar_al_historial(self, pelicula: Movie) -> None:
        """Registra la búsqueda en el historial con la fecha real."""
        self.historial.append({
            "titulo": pelicula.title,
            "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def limpiar_historial(self) -> None:
        """Limpia el historial de búsquedas."""
        self.historial.clear()

    # ------------------------------------------------------- Estadísticas
    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas básicas de uso."""
        return {
            "total_favoritas": len(self.favoritas),
            "total_historial": len(self.historial),
        }

    # -------------------------------------------------------- Persistencia
    def exportar_a_json(self, nombre_archivo: str) -> None:
        """Exporta favoritas e historial a un archivo JSON."""
        data = {
            "favoritas": [_movie_to_dict(p) for p in self.favoritas],
            "historial": self.historial,
            "estadisticas": self.obtener_estadisticas(),
        }
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Exportado a %s", nombre_archivo)

    def importar_de_json(self, nombre_archivo: str) -> None:
        """Importa favoritas e historial desde un archivo JSON."""
        with open(nombre_archivo, encoding="utf-8") as f:
            data = json.load(f)
        favoritas = data.get("favoritas", [])
        historial = data.get("historial", [])
        if not isinstance(favoritas, list) or not isinstance(historial, list):
            raise ValueError("Formato de archivo inválido")
        self.favoritas = [Movie.from_omdb(p) for p in favoritas]
        self.historial = historial
        logger.info("Importado desde %s", nombre_archivo)


def _movie_to_dict(pelicula: Movie) -> dict:
    """Convierte un modelo Movie a dict OMDB, con fallback si ya es dict."""
    if isinstance(pelicula, dict):
        return pelicula
    return pelicula.to_dict()
