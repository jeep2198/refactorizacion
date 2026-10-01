"""Servicio de series: caché y operaciones sobre TVMaze."""

from api.tvmaze import TVMazeClient
from models import Series


class SeriesService:
    """Servicio de series con estado encapsulado (caché en memoria)."""

    def __init__(self, api: TVMazeClient | None = None) -> None:
        self._api = api or TVMazeClient()
        self._cache: dict[str, list[Series]] = {}
        self._cache_detalles: dict[int, Series] = {}

    def buscar_series(self, nombre: str) -> list[Series]:
        """Busca series por nombre usando caché en memoria."""
        if not nombre or not nombre.strip():
            return []
        cache_key = f"series_{nombre.strip()}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        try:
            series = self._api.buscar_series(nombre.strip())
        except ConnectionError:
            return []
        if isinstance(series, list):
            self._cache[cache_key] = series
            return series
        return []

    def obtener_detalles_serie(self, id_serie: int) -> Series | None:
        """Obtiene los detalles de una serie por id."""
        if id_serie in self._cache_detalles:
            return self._cache_detalles[id_serie]
        try:
            detalles = self._api.obtener_detalles_serie(id_serie)
        except ConnectionError:
            return None
        if detalles is not None:
            self._cache_detalles[id_serie] = detalles
        return detalles
