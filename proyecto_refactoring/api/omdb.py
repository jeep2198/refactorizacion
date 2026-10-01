"""Cliente de la API OMDB de películas."""

from models import Movie

from .base_client import APIClient

BASE_URL = "https://www.omdbapi.com"


class OmdbClient(APIClient):
    """Cliente para la API de OMDB."""

    def __init__(self, api_key: str = "trilogy", **kwargs) -> None:
        super().__init__(base_url=BASE_URL, api_key=api_key, **kwargs)

    def buscar_pelicula(self, titulo: str) -> Movie | None:
        """Busca una película por título."""
        data = self.get_json(params={"t": titulo, "apikey": self.api_key})
        if isinstance(data, dict) and data.get("Response") == "True":
            return Movie.from_omdb(data)
        return None

    def buscar_peliculas_por_actor(self, actor: str) -> list[Movie]:
        """Busca películas por actor."""
        data = self.get_json(
            params={"s": actor, "type": "movie", "apikey": self.api_key}
        )
        if isinstance(data, dict) and data.get("Response") == "True":
            return [Movie.from_omdb(item) for item in data.get("Search", [])]
        return []
