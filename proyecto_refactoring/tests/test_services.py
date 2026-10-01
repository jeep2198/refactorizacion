"""Tests unitarios para la fachada MovieApp y los servicios."""

from unittest.mock import patch

import pytest

from api_movies import MovieApp
from exceptions import MovieNotFoundError
from models import Movie, Series
from services import MovieService, SeriesService


def _movie_payload(**overrides):
    data = {
        "Title": "Titanic",
        "Year": "1997",
        "imdbRating": "7.9",
        "Genre": "Romance",
    }
    data.update(overrides)
    return data


class TestMovieService:
    def test_buscar_pelicula_con_modelo(self):
        service = MovieService()
        resultado = Movie.from_omdb(_movie_payload())
        with patch.object(
            service._api, "buscar_pelicula", return_value=resultado
        ):
            pelicula = service.buscar_pelicula("Titanic")
            assert isinstance(pelicula, Movie)
            assert pelicula.title == "Titanic"
            assert pelicula.year == "1997"

    def test_buscar_pelicula_vacio_retorna_none(self):
        service = MovieService()
        assert service.buscar_pelicula("   ") is None
        assert service.buscar_pelicula("") is None

    def test_buscar_pelicula_sin_conexion_retorna_none(self):
        service = MovieService()
        with patch.object(service._api, "buscar_pelicula", side_effect=ConnectionError):
            assert service.buscar_pelicula("x") is None

    def test_buscar_pelicula_cachea_resultado(self):
        service = MovieService()
        with patch.object(service._api, "buscar_pelicula") as mock_buscar:
            mock_buscar.return_value = Movie.from_omdb(_movie_payload())
            service.buscar_pelicula("Titanic")
            service.buscar_pelicula("Titanic")
            assert mock_buscar.call_count == 1

    def test_favoritas_no_duplica(self):
        service = MovieService()
        pelicula = Movie.from_omdb(_movie_payload())
        assert service.agregar_a_favoritas(pelicula) is True
        assert service.agregar_a_favoritas(pelicula) is False
        assert len(service.favoritas) == 1

    def test_eliminar_favorita(self):
        service = MovieService()
        service.agregar_a_favoritas(Movie.from_omdb(_movie_payload()))
        assert service.eliminar_de_favoritas("Titanic") is True
        assert service.eliminar_de_favoritas("Titanic") is False

    def test_historial_y_estadisticas(self):
        service = MovieService()
        service.agregar_al_historial(Movie.from_omdb(_movie_payload()))
        stats = service.obtener_estadisticas()
        assert stats["total_historial"] == 1
        assert service.historial[0]["titulo"] == "Titanic"
        service.limpiar_historial()
        assert service.obtener_estadisticas()["total_historial"] == 0

    def test_export_import_round_trip(self, tmp_path):
        service = MovieService()
        service.agregar_a_favoritas(Movie.from_omdb(_movie_payload()))
        archivo = tmp_path / "datos.json"
        service.exportar_a_json(str(archivo))
        otro = MovieService()
        otro.importar_de_json(str(archivo))
        assert len(otro.favoritas) == 1
        assert otro.favoritas[0].title == "Titanic"

    def test_import_formato_invalido(self, tmp_path):
        archivo = tmp_path / "malo.json"
        archivo.write_text('{"favoritas": {}}', encoding="utf-8")
        service = MovieService()
        with pytest.raises(ValueError):
            service.importar_de_json(str(archivo))

    def test_catalogo_populares_y_genero(self):
        assert len(MovieService.obtener_peliculas_populares()) == 5
        assert len(MovieService.buscar_peliculas_por_genero("accion")) == 2
        assert len(MovieService.buscar_peliculas_por_genero("comedia")) == 2
        assert len(MovieService.buscar_peliculas_por_genero("otro")) == 4


class TestMovieNotFound:
    def test_excepcion_disponible(self):
        err = MovieNotFoundError("No existe")
        assert isinstance(err, Exception)
        assert str(err) == "No existe"


class TestSeriesService:
    def test_buscar_series_por_nombre(self):
        service = SeriesService()
        with patch.object(service._api, "buscar_series") as mock_buscar:
            mock_buscar.return_value = [
                Series.from_search_result({"show": {"id": 1, "name": "Breaking Bad"}})
            ]
            series = service.buscar_series("Breaking")
            assert len(series) == 1
            assert isinstance(series[0], Series)
            assert series[0].name == "Breaking Bad"

    def test_buscar_series_sin_conexion(self):
        service = SeriesService()
        with patch.object(service._api, "buscar_series", side_effect=ConnectionError):
            assert service.buscar_series("x") == []

    def test_obtener_detalles_serie(self):
        service = SeriesService()
        with patch.object(service._api, "obtener_detalles_serie") as mock_det:
            mock_det.return_value = Series.from_tvmaze({"id": 1, "name": "BB"})
            detalle = service.obtener_detalles_serie(1)
            assert detalle is not None
            assert detalle.id == 1

    def test_buscar_series_vacio(self):
        service = SeriesService()
        assert service.buscar_series("  ") == []


class TestMovieAppFacade:
    def test_composicion(self):
        app = MovieApp()
        assert isinstance(app.movie_service, MovieService)
        assert isinstance(app.series_service, SeriesService)

    def test_delegacion_pelicula(self):
        app = MovieApp()
        with patch.object(app.movie_service._api, "buscar_pelicula") as mock:
            mock.return_value = Movie.from_omdb(_movie_payload())
            result = app.buscar_pelicula("Titanic")
            assert result is not None
            assert result.title == "Titanic"

    def test_favoritas_historial_via_fachada(self):
        app = MovieApp()
        pelicula = Movie.from_omdb(_movie_payload())
        assert app.agregar_a_favoritas(pelicula)
        app.agregar_al_historial(pelicula)
        assert len(app.favoritas) == 1
        assert len(app.historial) == 1
        stats = app.obtener_estadisticas()
        assert stats["total_favoritas"] == 1

    def test_config_configurable(self):
        app = MovieApp(config={"timeout": 5, "max_retries": 1})
        assert app.config["timeout"] == 5
        assert app.config["max_retries"] == 1
