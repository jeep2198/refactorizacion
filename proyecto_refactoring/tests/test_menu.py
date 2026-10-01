"""Tests de integración para el menú y los flujos de UI."""

from unittest.mock import patch

from api_movies import MovieApp
from models import Movie, Series
from ui.menu import _funcion_buscar_pelicula, menu_principal


def _movie():
    return Movie.from_omdb({"Title": "Titanic", "Year": "1997", "Genre": "Romance"})


def _patch_busqueda(service):
    return patch.object(service._api, "buscar_pelicula", return_value=_movie())


class TestMenuFlows:
    def test_flujo_buscar_pelicula(self, capsys):
        app = MovieApp()
        with (
            _patch_busqueda(app.movie_service),
            patch("builtins.input", side_effect=["Titanic", "n", ""]),
        ):
            _funcion_buscar_pelicula(app)
        out = capsys.readouterr().out
        assert "Titanic" in out
        assert len(app.historial) == 1

    def test_flujo_buscar_pelicula_con_favorito(self):
        app = MovieApp()
        with (
            _patch_busqueda(app.movie_service),
            patch("builtins.input", side_effect=["Titanic", "s", ""]),
        ):
            _funcion_buscar_pelicula(app)
        assert len(app.favoritas) == 1

    def test_flujo_buscar_pelicula_no_encontrada(self, capsys):
        app = MovieApp()
        with (
            patch.object(app.movie_service._api, "buscar_pelicula", return_value=None),
            patch("builtins.input", side_effect=["xyz", ""]),
        ):
            _funcion_buscar_pelicula(app)
        out = capsys.readouterr().out
        assert "No se encontró la película" in out
        assert len(app.historial) == 0

    def test_menu_principal_salir(self):
        app = MovieApp()
        with patch("builtins.input", side_effect=["12"]):
            menu_principal(app)

    def test_menu_opcion_buscar(self):
        app = MovieApp()
        with (
            _patch_busqueda(app.movie_service),
            patch("builtins.input", side_effect=["1", "Titanic", "n", "", "", "12"]),
        ):
            menu_principal(app)
        assert len(app.historial) == 1

    def test_menu_opcion_invalida(self):
        app = MovieApp()
        with patch("builtins.input", side_effect=["99", "12"]):
            menu_principal(app)

    def test_menu_opciones_estaticas(self, capsys):
        app = MovieApp()
        with patch("builtins.input", side_effect=["4", "", "5", "accion", "", "12"]):
            menu_principal(app)
        out = capsys.readouterr().out
        assert "Shawshank" in out
        assert "Die Hard" in out

    def test_menu_favoritos_vacio(self, capsys):
        app = MovieApp()
        with patch("builtins.input", side_effect=["6", "", "12"]):
            menu_principal(app)
        out = capsys.readouterr().out
        assert "No tienes películas favoritas" in out

    def test_menu_historial_vacio(self, capsys):
        app = MovieApp()
        with patch("builtins.input", side_effect=["7", "", "12"]):
            menu_principal(app)
        out = capsys.readouterr().out
        assert "No hay historial" in out

    def test_menu_verificar_favorito_y_eliminar(self):
        app = MovieApp()
        app.agregar_a_favoritas(_movie())
        with patch("builtins.input", side_effect=["6", "1", "", "12"]):
            menu_principal(app)
        assert len(app.favoritas) == 0

    def test_menu_limpiar_historial(self):
        app = MovieApp()
        app.agregar_al_historial(_movie())
        with patch("builtins.input", side_effect=["7", "s", "", "12"]):
            menu_principal(app)
        assert len(app.historial) == 0

    def test_menu_estadisticas(self, capsys):
        app = MovieApp()
        app.agregar_a_favoritas(_movie())
        with patch("builtins.input", side_effect=["8", "", "12"]):
            menu_principal(app)
        out = capsys.readouterr().out
        assert "Total favoritas: 1" in out

    def test_menu_export_import(self, capsys):
        app = MovieApp()
        app.agregar_a_favoritas(_movie())
        with patch("builtins.input", side_effect=["9", "test_ui", "", "12"]):
            menu_principal(app)
        otro = MovieApp()
        with patch("builtins.input", side_effect=["10", "test_ui", "", "12"]):
            menu_principal(otro)
        assert len(otro.favoritas) == 1

    def test_menu_export_error(self, capsys):
        app = MovieApp()
        with (
            patch("builtins.input", side_effect=["9", "test_ui", "", "12", "stop"]),
            patch(
                "services.movie_service.MovieService.exportar_a_json",
                side_effect=OSError("sin permisos"),
            ),
        ):
            menu_principal(app)
        out = capsys.readouterr().out
        assert "Error al exportar" in out

    def test_menu_configuracion_timeout(self, capsys):
        app = MovieApp()
        with patch("builtins.input", side_effect=["11", "3", "20", "", "12"]):
            menu_principal(app)
        assert app.config["timeout"] == 20

    def test_menu_configuracion_invalido(self, capsys):
        app = MovieApp()
        with patch("builtins.input", side_effect=["11", "3", "abc", "", "12"]):
            menu_principal(app)
        out = capsys.readouterr().out
        assert "Timeout inválido" in out

    def test_buscar_series_flujo(self, capsys):
        app = MovieApp()
        serie = Series.from_tvmaze({"id": 1, "name": "BB", "status": "Ended"})
        series_mockeadas = patch.object(
            app.series_service._api, "buscar_series", return_value=[serie]
        )
        with (
            series_mockeadas,
            patch.object(
                app.series_service._api,
                "obtener_detalles_serie",
                return_value=serie,
            ),
            patch("builtins.input", side_effect=["3", "Breaking", "1", "", "12"]),
        ):
            menu_principal(app)
        out = capsys.readouterr().out
        assert "BB" in out
