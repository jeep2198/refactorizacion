"""Tests unitarios para los clientes de API (con mocks de requests)."""

from unittest.mock import patch

import pytest
import requests

from api.omdb import OmdbClient
from api.tvmaze import TVMazeClient
from exceptions import APIError


class TestOmdbClient:
    def test_buscar_pelicula(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "Response": "True",
                "Title": "Titanic",
                "Year": "1997",
            }
            cliente = OmdbClient(api_key="test")
            pelicula = cliente.buscar_pelicula("Titanic")
            assert pelicula is not None
            assert pelicula.title == "Titanic"

            url, kwargs = mock_get.call_args
            assert kwargs["params"]["apikey"] == "test"
            assert kwargs["params"]["t"] == "Titanic"
            # La key no debe ir en la URL
            assert "apikey" not in url[0]

    def test_buscar_pelicula_no_encontrada(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "Response": "False",
                "Error": "Movie not found",
            }
            cliente = OmdbClient(api_key="test")
            assert cliente.buscar_pelicula("xyz") is None

    def test_reintentos_backoff(self):
        with patch("requests.get", side_effect=requests.ConnectionError("boom")), patch(
            "time.sleep"
        ) as mock_sleep:
            cliente = OmdbClient(api_key="test", max_retries=3)
            with pytest.raises(ConnectionError):
                cliente.buscar_pelicula("x")
            assert mock_sleep.call_count == 3

    def test_error_http(self):
        with patch("requests.get") as mock_get:
            mock_error = requests.HTTPError("500")
            mock_get.return_value.raise_for_status.side_effect = mock_error
            mock_get.return_value.status_code = 500
            cliente = OmdbClient(api_key="test", max_retries=1)
            with pytest.raises(ConnectionError):
                cliente.buscar_pelicula("x")

    def test_usa_https(self):
        from api import omdb, tvmaze

        assert omdb.BASE_URL.startswith("https")
        assert tvmaze.BASE_URL.startswith("https")

    def test_buscar_por_actor(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "Response": "True",
                "Search": [{"Title": "Inception", "Year": "2010"}],
            }
            cliente = OmdbClient(api_key="test")
            peliculas = cliente.buscar_peliculas_por_actor("DiCaprio")
            assert len(peliculas) == 1
            assert peliculas[0].title == "Inception"


class TestTVMazeClient:
    def test_buscar_series(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = [
                {"show": {"id": 1, "name": "Breaking Bad", "status": "Ended"}}
            ]
            cliente = TVMazeClient()
            series = cliente.buscar_series("Breaking")
            assert len(series) == 1
            assert series[0].name == "Breaking Bad"

    def test_obtener_detalles(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "id": 1,
                "name": "Breaking Bad",
                "rating": {"average": 9.5},
            }
            cliente = TVMazeClient()
            serie = cliente.obtener_detalles_serie(1)
            assert serie is not None
            assert serie.rating == "9.5"


class TestAPIError:
    def test_status_code(self):
        err = APIError("boom", status_code=500)
        assert err.status_code == 500
