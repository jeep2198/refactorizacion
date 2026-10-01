"""Modelo de datos para películas."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Movie:
    """Película con los campos normalizados de la API OMDB."""

    title: str = ""
    year: str = ""
    rating: str = "N/A"
    genre: str = "N/A"
    director: str = "N/A"
    actors: str = "N/A"
    plot: str = "N/A"
    language: str = "N/A"
    country: str = "N/A"
    awards: str = "N/A"
    poster: str = "N/A"
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_omdb(cls, data: dict[str, Any]) -> "Movie":
        """Construye una película desde la respuesta de OMDB."""
        return cls(
            title=data.get("Title", ""),
            year=data.get("Year", ""),
            rating=data.get("imdbRating", "N/A"),
            genre=data.get("Genre", "N/A"),
            director=data.get("Director", "N/A"),
            actors=data.get("Actors", "N/A"),
            plot=data.get("Plot", "N/A"),
            language=data.get("Language", "N/A"),
            country=data.get("Country", "N/A"),
            awards=data.get("Awards", "N/A"),
            poster=data.get("Poster", "N/A"),
            raw=data,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convierte el modelo a diccionario con claves OMDB."""
        return {
            "Title": self.title,
            "Year": self.year,
            "imdbRating": self.rating,
            "Genre": self.genre,
            "Director": self.director,
            "Actors": self.actors,
            "Plot": self.plot,
            "Language": self.language,
            "Country": self.country,
            "Awards": self.awards,
            "Poster": self.poster,
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Acceso estilo dict a los campos normalizados."""
        return self.to_dict().get(key, default)
