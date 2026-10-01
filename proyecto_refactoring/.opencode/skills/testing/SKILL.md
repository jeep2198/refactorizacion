---
name: testing
description: Crea y mantiene tests automatizados con pytest - estructura Arrange-Act-Assert, mocks de requests con unittest.mock y MagicMock, fixtures y test data builders, cobertura de casos de error con pytest.raises, y detección de gaps de cobertura. Usar al escribir o ampliar la suite de tests, identificar módulos sin cubrir, o alcanzar objetivos de coverage por módulo.
license: MIT
compatibility: opencode
metadata:
  version: "2.0"
  language: python
---

## Contexto

- Version: 2.0 (Reusable Structure)
- Project: Any Python project
- Runner: pytest

## Descripción

Formato estandarizado para la creación y mantenimiento de tests automatizados en cualquier proyecto Python.

## Patrones de detección de necesidades de testing

### 1. Test Coverage Gaps
- Identificar módulos sin archivos de test correspondientes
- Detectar tests que solo cubren happy path (sin error cases)
- Buscar tests con assertions débiles (`assert True`, `assert result`)
- **Severidad**: Medium - riesgo de regresión no detectada

### 2. Unit Tests Structure
- **Arrange-Act-Assert** pattern en todos los tests
- **Nombre descriptivo**: `test_<funcion>_<escenario>`
- **Isolation**: Mock dependencias externas (bases de datos, APIs)
- **Independencia**: Tests no deben depender del orden de ejecución

### 3. Mock Strategies
- **`unittest.mock.patch`** para funciones y métodos
- **`unittest.mock.MagicMock`** para objetos complejos
- **Fixtures** de pytest para setup/teardown compartido
- **Test data builders** para objetos de dominio

### 4. Error Case Coverage
- Probar excepciones esperadas con `pytest.raises`
- Cubrir casos de borde (edge cases)
- Validar mensajes de error apropiados
- Tests de fallo gracefull (fallback behavior)

### 5. Integration Tests Patterns
- **Database transactions** rollback después de cada test
- **API endpoints** con clients de test configurados
- **Estado inicial** consistente en cada test
- **Limpieza** de recursos después de tests

## Aplicación al proyecto actual

### Tests existentes (`tests/` directory)
- `test_apis.py`: Tests unitarios con mocks de `requests.get` para OMDB y TVMaze
- `test_services.py`: Tests para servicios de películas y series
- `test_models.py`: Tests para modelos de datos (Movie, Series)
- `test_menu.py`: Tests para el menú de UI

### Cobertura actual y gaps identificados

| Módulo | Tests | Cobertura |
|--------|-------|-----------|
| `api.omdb.OmdbClient` | ✅ test_apis.py | Happy path + reintentos |
| `api.tvmaze.TVMazeClient` | ✅ test_apis.py | Búsqueda y detalles |
| `exceptions.APIError` | ✅ test_apis.py | Error status_code |
| `services.MovieService` | ⚠️ N/A | No hay tests de servicio |
| `models.Movie` | ⚠️ N/A | No hay tests de modelo |
| `ui.menu` | ⚠️ N/A | No hay tests de interfaz |
| `services.SeriesService` | ⚠️ N/A | No hay tests de servicio |

### Tests prioritarios por crear

#### Críticos (sin cobertura)
1. **MovieService tests** - Búsquedas, favoritas, historial, export/import
2. **Movie model tests** - `from_omdb`, `to_dict`, `get` methods
3. **SeriesService tests** - Búsqueda y detalles de series

#### Altos
4. **OmdbClient edge cases** - Respuestas inválidas, keys faltantes
5. **TVMaze encoding** - Nombres con caracteres especiales
6. **Error handling** - Timeouts, errores HTTP 500

#### Medianos
7. **MovieService caching** - Comportamiento con cache hit/miss
8. **Historial management** - Limpiar y registrar búsquedas
9. **Estadísticas** - Cálculo correcto de totales

#### Bajos
10. **UI menu** - Opciones válidas e inválidas
11. **Config files** - Carga e importación de config

## Ejemplos de tests a añadir

### Test para MovieService (crítico)
```python
def test_buscar_pelicula_con_cache(mock_requests_get):
    """Should use cache when movie already searched."""
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        "Response": "True",
        "Title": "Titanic",
        "Year": "1997",
    }
    
    from services import MovieService
    service = MovieService()
    
    # First call - hits API
    pelicula1 = service.buscar_pelicula("Titanic")
    assert pelicula1 is not None
    assert len(service._cache) == 1
    
    # Second call - uses cache
    pelicula2 = service.buscar_pelicula("Titanic")
    assert pelicula2 is not None
    # Debería no hacer segunda llamada a API
    assert mock_requests_get.call_count == 1
```

### Test para modelo Movie (crítico)
```python
def test_from_omdb_constructor():
    """Should build Movie from OMDB response data."""
    data = {
        "Title": "Inception",
        "Year": "2010",
        "imdbRating": "8.8",
        "Genre": "Sci-Fi",
        "Director": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio",
        "Plot": "A thief who steals...",
        "Language": "English",
        "Country": "USA",
        "Awards": "Wins.",
        "Poster": "http://poster.com",
    }
    
    pelicula = Movie.from_omdb(data)
    assert pelicula.title == "Inception"
    assert pelicula.year == "2010"
    assert pelicula.rating == "8.8"
    assert pelicula.genre == "Sci-Fi"
```

### Test para error handling (alto)
```python
def test_buscar_pelicula_error_http():
    """Should raise ConnectionError on HTTP 500."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = HTTPError("500")
        mock_get.return_value.status_code = 500
        
        cliente = OmdbClient(api_key="test")
        with pytest.raises(ConnectionError):
            cliente.buscar_pelicula("x")
```

### Test for edge cases (medio)
```python
def test_buscar_pelicula_vacio():
    """Should return None for empty title."""
    cliente = OmdbClient(api_key="test")
    assert cliente.buscar_pelicula("") is None
    assert cliente.buscar_pelicula("   ") is None
```

## Checklist de testing robusto

### Unit Tests
- [ ] Todos los funciones públicas tienen tests
- [ ] Tests para casos normales y edge cases
- [ ] Tests para excepciones esperadas
- [ ] Mock de todas las dependencias externas
- [ ] Tests independientes (no comparten state)

### Fixtures de pytest
- [ ] `client_fixture` para OmdbClient/TVMazeClient
- [ ] `sample_movie_fixture` datos de película de prueba
- [ ] `sample_series_fixture` datos de serie de prueba
- [ ] `mock_requests_get` fixture global

### Coverage goals
- [ ] Mínimo 80% coverage en servicios
- [ ] Mínimo 90% coverage en modelos
- [ ] Tests críticos cubriendo paths de error
- [ ] No happy-path-only tests

### Integración CI
- [ ] `pytest` en pipeline de CI
- [ ] Reporte de cobertura en cada push
- [] Fallo build si coverage < threshold
- [] Ejecutar `pytest --tb=short` para debugging