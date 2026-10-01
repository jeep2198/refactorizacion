"""Tests unitarios para modelos y presentación."""

from models import Movie, Series
from ui import display


class TestModels:
    def test_movie_from_omdb(self):
        pelicula = Movie.from_omdb(
            {"Title": "Titanic", "Year": "1997", "imdbRating": "7.9"}
        )
        assert pelicula.title == "Titanic"
        assert pelicula.year == "1997"
        assert pelicula.rating == "7.9"
        assert pelicula.get("Genre") == "N/A"

    def test_movie_to_dict_usa_claves_omdb(self):
        pelicula = Movie.from_omdb({"Title": "Titanic", "Year": "1997"})
        data = pelicula.to_dict()
        assert data["Title"] == "Titanic"
        assert data["Year"] == "1997"

    def test_movie_defaults(self):
        pelicula = Movie()
        assert pelicula.title == ""
        assert pelicula.rating == "N/A"

    def test_series_from_search(self):
        serie = Series.from_search_result(
            {
                "show": {
                    "id": 7,
                    "name": "Dexter",
                    "status": "Ended",
                    "genres": ["Crime"],
                }
            }
        )
        assert serie.id == 7
        assert serie.name == "Dexter"
        assert "Crime" in serie.genres

    def test_series_from_tvmaze_rating(self):
        serie = Series.from_tvmaze({"id": 1, "name": "BB", "rating": {"average": 9.5}})
        assert serie.rating == "9.5"

    def test_series_to_dict(self):
        serie = Series.from_tvmaze({"id": 1, "name": "BB"})
        data = serie.to_dict()
        assert data["name"] == "BB"
        assert data["id"] == 1


class TestDisplay:
    def test_formato_separador(self, capsys):
        display.print_separator()
        out = capsys.readouterr().out
        assert out == "=" * 60 + "\n"

    def test_muestra_pelicula_sin_datos(self, capsys):
        display.mostrar_pelicula(None)
        out = capsys.readouterr().out
        assert "No se encontró la película" in out

    def test_muestra_pelicula_con_modelo(self, capsys):
        pelicula = Movie.from_omdb({"Title": "Titanic", "Year": "1997"})
        display.mostrar_pelicula(pelicula)
        out = capsys.readouterr().out
        assert "Titanic" in out
        assert "1997" in out

    def test_muestra_lista_series(self, capsys):
        series = [Series.from_tvmaze({"id": 1, "name": "BB"})]
        display.mostrar_lista_series(series)
        out = capsys.readouterr().out
        assert "1. BB" in out
