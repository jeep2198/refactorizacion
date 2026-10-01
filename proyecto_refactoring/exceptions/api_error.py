"""Excepciones personalizadas del dominio de películas y series."""


class APIError(Exception):
    """Error al comunicarse con una API externa."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
