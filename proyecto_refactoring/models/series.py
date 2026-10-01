"""Modelo de datos para series."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Series:
    """Serie con los campos normalizados de la API TVMaze."""

    id: int = 0
    name: str = ""
    language: str = "N/A"
    genres: list[str] = field(default_factory=list)
    status: str = "N/A"
    premiered: str = "N/A"
    ended: str = "N/A"
    runtime: str = "N/A"
    rating: str = "N/A"
    summary: str = "N/A"
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_tvmaze(cls, data: dict[str, Any]) -> "Series":
        """Construye una serie desde la respuesta de TVMaze (objeto show)."""
        return cls(
            id=int(data.get("id", 0) or 0),
            name=data.get("name", ""),
            language=data.get("language", "N/A"),
            genres=list(data.get("genres", []) or []),
            status=data.get("status", "N/A"),
            premiered=data.get("premiered", "N/A"),
            ended=data.get("ended", "N/A"),
            runtime=str(data.get("runtime", "N/A") or "N/A"),
            rating=str(
                (data.get("rating") or {}).get("average", "N/A")
            ),
            summary=data.get("summary", "N/A") or "N/A",
            raw=data,
        )

    @classmethod
    def from_search_result(cls, resultado: dict[str, Any]) -> "Series":
        """Construye una serie desde un resultado de búsqueda (".show")."""
        show = resultado.get("show", resultado)
        return cls.from_tvmaze(show)

    def to_dict(self) -> dict[str, Any]:
        """Convierte el modelo a diccionario estilo show de TVMaze."""
        return {
            "id": self.id,
            "name": self.name,
            "language": self.language,
            "genres": self.genres,
            "status": self.status,
            "premiered": self.premiered,
            "ended": self.ended,
            "runtime": self.runtime,
            "rating": {"average": self.rating} if self.rating != "N/A" else {},
            "summary": self.summary,
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Acceso estilo dict a los campos normalizados."""
        return self.to_dict().get(key, default)
