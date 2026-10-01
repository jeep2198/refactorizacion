"""Excepción cuando una película no se encuentra en la API."""


class MovieNotFoundError(Exception):
    """No se encontró la película solicitada."""
