# Informe de Refactoring y Correcciones

Proyecto: `proyecto_refactoring` — Fases F1 a F5 + estructura de directorios (F3/F4/F6) + validación final.
Fecha: 2026-09-22

## 1. Resumen de métricas (antes → después)

| Métrica | Inicial (121 archivos) | Tras Fase 2 (33 archivos) | Final (50 módulos analizados) | Cambio |
|---|---|---|---|---|
| Archivos `*_config.py` muertos | 90 | 0 | 0 | Eliminados |
| Variables globales mutables | ~120 | 33 | 0 estado mutable | Encapsuladas |
| Sentencias `global` | numerosas | numerosas | 0 | Eliminadas |
| Bare excepts `except:` | 27 | 27 | 0 | Especificados |
| Wildcard imports | 1 | 1 | 0 | Específicos |
| Concatenaciones `+` | ~361 | 194 | 0 | f-strings |
| Bucles `while` con contador | 13 | 13 | 0 manuales (2 legítimos `while True`) | `for/enumerate` |
| Compilación (módulos).py | — | OK (33) | 0 errores sintaxis (50) | Verificado |
| Imports (módulos) | — | OK | 0 fallos | Verificado |
| Tests automáticos | 0 | 0 | **55 passing, 90% coverage** | pytest |

> Nota: el `analyzer.py` original contaba las variables locales como "globales" (usaba
> `ast.walk` sobre todo el árbol). Se corrigió para contar solo asignaciones a nivel de
> módulo (`ast.parse` + `tree.body`) y ahora también escanea los paquetes de la
> estructura nueva (`api/`, `models/`, `services/`, `ui/`, `exceptions/`). Las
> variables no-constantes restantes son legítimas: 21 instancias singleton `_manager`,
> `logger` (x2), la instancia `app`, y los `__all__` de los `__init__.py`.

## 2. Cambios por módulo (Fase 3–5)

### api_movies.py — fachada `MovieApp`
- Estado encapsulado: favoritas/historial/cachés viven en `MovieService`/`SeriesService`.
- `MovieApp` compone `OmdbClient` + `TVMazeClient` + `MovieService` + `SeriesService`
  y delega: ya no contiene lógica HTTP propia (ver `api/base_client.py`).
- Config inyectada en constructor (`config=DEFAULT_CONFIG`), con timeout y max_retries.
- `APIClient.get_json` (en `api/base_client.py`): `requests.get` con timeout real,
  reintentos con backoff exponencial (`min(2**attempt, 4)`) y `raise_for_status`;
  propagación de `ConnectionError`.
- Sin `except:` bare; f-strings; validación de entrada vacía `if not titulo or not titulo.strip()`.
- URLs `http://` → `https://` (OMDB y TVMaze).
- API pública conservada: `buscar_pelicula`, `buscar_series`, `buscar_peliculas_por_actor`,
  `obtener_detalles_serie`, `obtener_peliculas_populares`, `buscar_peliculas_por_genero`,
  `agregar_a_favoritas`, `eliminar_de_favoritas`, `agregar_al_historial`,
  `limpiar_historial`, `obtener_estadisticas`, `exportar_a_json`, `importar_de_json`.

### main.py — reescrito
- Eliminado `from api_movies import *` → `from api_movies import MovieApp`.
- Instancia única `app = MovieApp()` (una variable de módulo, no estado global).
- `clear_screen()` portable (secuencia ANSI), sin `os.system("cls")`/plataforma.
- `mostrar_pelicula`/`mostrar_serie` con `.get()` y f-strings; formato de rating robusto.
- Loop de búsqueda con `for` y retry por intento en vez de `while` con contador manual.
- Manejo de `KeyboardInterrupt` y `except Exception as e` específico.
- El único `while True` restante es el menú principal (legítimo).

### app.py — reescrito como clase `MovieSearchApp`
- Mismo patrón: estado en instancia, `_get_json` con timeout y validación.
- **Seguridad**: la API key se movió de la URL a `params` (`requests.get(url, params=...)`),
  el error genérico no expone la key, y las URLs van por constantes.
- `http://` → `https://`; `urllib.parse.quote` para el query de series.
- `while True` solo para el menú; `for i, x in enumerate(...)` para listados.

### utils.py — reescrito
- Constantes inmutables `RESULTS_DIR`, `EXPORT_DIR`, `CAMPOS_PELICULA` (tuple).
- `format_movie_display`, `format_series_display`, `format_list_display` con f-strings.
- Sin bare excepts; type hints; `delay()` usa `time.sleep` directo.
- El `while True` restante es el de validación de entrada de `get_user_input` (legítimo).

### Managers (21 módulos) — patrón clase singleton
`audit_manager`, `cache_manager`, `cache_manager_v2`, `config_manager`,
`config_manager_v2`, `error_manager`, `favorites_manager`, `feature_manager`,
`history_manager`, `metadata_manager`, `notification_manager`, `permission_manager`,
`plugin_manager`, `report_manager`, `schedule_manager`, `settings_manager`,
`state_manager`, `stats_manager`, `tag_manager`, `user_manager`, `version_manager`.

- Cada módulo: clase singleton (`_instance` + `__new__`), inicialización lazy
  (`_ensure_initialized`), estado en `self.*`, persistencia con `encoding="utf-8"`.
- Al final del archivo: instancia única `_manager` + funciones wrapper con la misma
  firma → la API pública de cada módulo no cambia.
- Eliminadas todas las sentencias `global` y las variables globales mutables.
- `except:` bare → excepciones específicas (`ValueError`, `OSError`,
  `(TypeError, KeyError)`) siempre con `as e`.

### Otros
- `config_manager_v2.py`: `http://` → `https://` en `tvmaze_url`; última concatenación
  `print("\n" + "=" * 60)` → `f"\n{'=' * 60}"`.
- `constants.py`: `BASE_URL_OMDB`, `BASE_URL_TVMAZE` → HTTPS.
- `analyzer.py`: corregido conteo de variables globales (nivel módulo real).
- `.gitignore`: añadido `*.json` (con salvedad para los archivos de arquitectura),
  `cache/`, `backups/`, `imports/`, `exports/`, `plugins/`, `logs/`.

## 3. Validación de funcionamiento (loop)

- `py_compile`/`ast.parse` de los 50 módulos (raíz + paquetes): **0 errores**.
- `importlib.import_module` de todos los módulos: **0 fallos**.
- **pytest**: `tests/` con 55 pruebas (models, apis, services, menu, display) +
  mocks de red. Resultado: **55 passed**, coverage de la estructura nueva
  (api/models/services/ui/exceptions/api_movies): **90%** (mínimo pedido: 80%).
- Smoke test `MovieApp`: favoritas (sin duplicados), historial, estadísticas,
  export/import round-trip con modelos, cache (1 petición para 2 búsquedas),
  manejo sin red (`ConnectionError` → `None`), validación de entrada vacía.
- `main.py`: flujo opción 1 (buscar) + salida limpia con opción 12; opciones
  inválidas manejadas.
- `app.py`: instancia creada, búsqueda mockeada OK, respuesta inválida manejada.
- Managers: prueba de identidad singleton (`_manager is ClaseManager()`), delegación
  módulo→instancia, round-trip de caché/config/usuarios/estado, parse de logs.
- Carga de los 33 módulos raíz: **0.226 s**.

## 4. Estructura de directorios (reglas de diseño Fase 3/4/6)

Separación de responsabilidades real de `api_movies.py` en submódulos, sin romper
ningún flujo (la tarjeta `api_movies.py` sigue como fachada `MovieApp` que compone
los servicios).

| Regla pedida | Implementado |
|---|---|
| `api/omdb.py` + `api/tvmaze.py` | `api/` con `base_client.py` (HTTP/backoff común), `omdb.py` (`OmdbClient`→`Movie`), `tvmaze.py` (`TVMazeClient`→`Series`) |
| `services/movie_service.py` + `services/series_service.py` | `services/` con ambos servicios + `catalog.py` (catálogos estáticos) |
| `ui/menu.py` + `ui/display.py` | `ui/` con `menu_principal(app)` (inyección del facade) y helpers de presentación |
| `main.py` solo entrada | `main()` crea `MovieApp()` y llama `menu_principal(app)`; sin lógica de negocio |
| `models/movie.py` + `models/series.py` | `models/` con dataclasses `Movie`/`Series` (`.from_omdb`, `.from_tvmaze`, `.get`, `.to_dict`) |
| `exceptions/movie_not_found.py` (Fase 4) | `exceptions/` con `APIError`, `MovieNotFoundError`, `SeriesNotFoundError` |
| `tests/` con pytest (Fase 6) | `tests/` con 55 pruebas, mocks de red, coverage 90% |

Catálogos y configuración centralizados en `services/catalog.py` y `constants.py`.
Para probar por separado cualquier pieza no hace falta red: se mockea `requests.get`
en los tests.

## 5. Seguridad

| Hallazgo | Estado |
|---|---|
| `http://` en OMDB/TVMaze (tráfico plano) | Corregido → `https://` en todos los módulos |
| API key de OMDB en la URL (exponía key en logs/proxies) | Corregido → `params` en `requests.get` (app.py) |
| API key hardcodeada (`"trilogy"`) | Es la key pública demo de OMDB; `config.py` lee de `OMDB_API_KEY` (env). Documentado; quedó como default educativo |
| `ip_address: "127.0.0.1"` hardcodeado en `audit_manager` | Placeholder de entorno local; no es secreto. Queda documentado como pendiente opcional |
| `except:` (fragmenta manejo de errores) | 0 restantes |
| `eval`, `exec`, `pickle.load`, `subprocess` | 0 en todo el proyecto |
| Entradas sin validar | `buscar_pelicula`/`buscar_series` validan vacío; opciones de menú validadas |

## 6. Performance

| Ítem | Estado |
|---|---|
| Timeout de red | `config["timeout"]` aplicado (10s por defecto, configurable) |
| Reintentos | `max_retries` con backoff exponencial `min(2**attempt, 4)` (3 intentos ≈ 7s en fallo total) |
| Caché | En memoria en los servicios (películas y series); prueba: 1 request real para 2 búsquedas |
| Delays artificiales | Eliminados (antes `delay(1)` en flujos); solo backoff y helpers `delay()` |
| Bucles de contador manual | Convertidos a `for`/`enumerate` |
| Suite de tests | 55 tests en **1.8 s** |

## 7. Pendientes asumidos (no corregidos a propósito)

- API key por defecto `"trilogy"`: se mantiene por ser la key demo pública de OMDB;
  para uso real debe ir por `OMDB_API_KEY` en el entorno.
- `ip_address` en `audit_manager`: placeholder local; si el proyecto se conecta a una
  red real, debería tomarse del request.
- 2 `while True` (menú de `ui/menu.py`, validación de input en `utils.py`):
  son bucles de interacción deliberados, no se reemplazaron.
- No se ejecutaron requests reales a OMDB/TVMaze durante la validación (se mockeó la
  red); el comportamiento con la API real queda como prueba manual.