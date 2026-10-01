"""Cliente de la API TVMaze de series."""

import urllib.parse

from models import Series

from .base_client import APIClient

BASE_URL = "https://api.tvmaze.com"


class TVMazeClient(APIClient):
    """Cliente para la API de TVMaze."""

    def __init__(self, **kwargs) -> None:
        super().__init__(base_url=BASE_URL, **kwargs)

    def buscar_series(self, nombre: str) -> list[Series]:
        """Busca series por nombre."""
        data = self.get_json(
            "search/shows", {"q": urllib.parse.quote(nombre)}
        )
        if isinstance(data, list):
            return [Series.from_search_result(item) for item in data]
        return []

    def obtener_detalles_serie(self, id_serie: int) -> Series | None:
        """Obtiene los detalles de una serie por id."""
        data = self.get_json(f"shows/{id_serie}")
        if isinstance(data, dict):
            return Series.from_tvmaze(data)
        return None
