# ANÁLISIS AUTOMÁTICO DEL PROYECTO

Generado por analyzer.py

## 1. Variables Globales Identificadas

### error_manager.py
- `_manager` (línea 213) - variable

### feature_manager.py
- `_manager` (línea 226) - variable

### version_manager.py
- `_manager` (línea 197) - variable

### state_manager.py
- `_manager` (línea 255) - variable

### stats_manager.py
- `_manager` (línea 226) - variable

### backup_manager.py
- `BACKUP_DIR` (línea 7) - constant
- `MAX_BACKUPS` (línea 8) - constant

### cache_manager_v2.py
- `_manager` (línea 251) - variable

### log_manager.py
- `LOG_DIR` (línea 5) - constant
- `LOG_FILE` (línea 6) - constant
- `ERROR_LOG_FILE` (línea 7) - constant
- `DEBUG_LOG_FILE` (línea 8) - constant

### favorites_manager.py
- `_manager` (línea 216) - variable

### user_manager.py
- `_manager` (línea 227) - variable

### schedule_manager.py
- `_manager` (línea 218) - variable

### logger.py
- `LOG_FILE` (línea 5) - constant
- `LOG_LEVEL` (línea 6) - constant
- `LOG_FORMAT` (línea 7) - constant

### cache_manager.py
- `_manager` (línea 175) - variable

### data_manager.py
- `DATA_DIR` (línea 7) - constant
- `BACKUP_DIR` (línea 8) - constant
- `DATA_FILE` (línea 9) - constant
- `BACKUP_FILE` (línea 10) - constant

### tag_manager.py
- `_manager` (línea 191) - variable

### permission_manager.py
- `_manager` (línea 195) - variable

### settings_manager.py
- `_manager` (línea 200) - variable

### history_manager.py
- `_manager` (línea 233) - variable

### report_manager.py
- `_manager` (línea 204) - variable

### config_manager.py
- `_manager` (línea 103) - variable

### config_manager_v2.py
- `_manager` (línea 242) - variable

### api_movies.py
- `logger` (línea 15) - variable
- `DEFAULT_CONFIG` (línea 17) - constant

### metadata_manager.py
- `_manager` (línea 196) - variable

### notification_manager.py
- `_manager` (línea 212) - variable

### export_manager.py
- `EXPORT_DIR` (línea 9) - constant
- `IMPORT_DIR` (línea 10) - constant

### plugin_manager.py
- `_manager` (línea 219) - variable

### audit_manager.py
- `_manager` (línea 193) - variable

### utils.py
- `RESULTS_DIR` (línea 7) - constant
- `EXPORT_DIR` (línea 8) - constant
- `CAMPOS_PELICULA` (línea 58) - constant

### api/__init__.py
- `__all__` (línea 5) - variable

### api/tvmaze.py
- `BASE_URL` (línea 9) - constant

### api/base_client.py
- `logger` (línea 8) - variable
- `DEFAULT_TIMEOUT` (línea 10) - constant
- `DEFAULT_MAX_RETRIES` (línea 11) - constant
- `BACKOFF_CAP` (línea 12) - constant

### api/omdb.py
- `BASE_URL` (línea 7) - constant

### models/__init__.py
- `__all__` (línea 4) - variable

### services/__init__.py
- `__all__` (línea 4) - variable

### services/movie_service.py
- `logger` (línea 12) - variable

### ui/__init__.py
- `__all__` (línea 4) - variable

### ui/display.py
- `CAMPOS_PELICULA` (línea 5) - constant

### exceptions/__init__.py
- `__all__` (línea 5) - variable

**Total: 54 variables globales**

## 2. Bare Excepts

**Total: 0 bare excepts**

## 3. Wildcard Imports

**Total: 0 wildcard imports**

## 4. Archivos *_config.py Sin Uso

No se encontraron archivos config sin uso.

**Total: 0 archivos sin uso**

## 5. Concatenaciones de Strings


**Total: 0 concatenaciones con +**

## 6. Bucles While (candidatos a for)

- utils.py: 1 bucles while
- ui/menu.py: 1 bucles while

**Total: 2 bucles while**

## 7. Resumen

| Categoría | Cantidad |
|-----------|----------|
| Variables globales | 54 |
| Bare excepts | 0 |
| Wildcard imports | 0 |
| Archivos config sin uso | 0 |
| Concatenaciones string | 0 |
| Bucles while | 2 |

---

# APÉNDICE B: Comparación con SAST automatizado + correcciones (2026-09-22, tarde)

> El proyecto evolucionó el mismo día tras el análisis principal (apareció `.venv/`, una capa
> `api/`+`services/`+`models/`+`ui/`+`exceptions/` y 4 archivos de tests). Este apéndice
> documenta qué detectó blanco==herramienta automatizada==, qué NO detectó, y corrige los
> hallazgos del documento principal que quedaron desactualizados.

## B.1 Herramientas ejecutadas

| Herramienta | Método | Alcance |
|-------------|--------|---------|
| bandit 1.9.4 (venv aislado `/tmp/opencode/bandit-venv`) | SAST por firma (regla por línea) | 56 archivos `.py` del proyecto, `.venv` excluido |
| ruff (set `S` = reglas de bandit) | SAST por AST | idéntico |
| ruff (set `F` = pyflakes) | dead code / imports / variables | idéntico |
| pytest (`.venv`, instalado por el propio repo) | ejecución | suite `tests/` |

## B.2 Resultados bandit + ruff (solo código del proyecto, sin `.venv`)

| Regla | Cantidad | Ubicación | ¿Hallazgo real? |
|-------|----------|-----------|-----------------|
| B101/S101 `assert` usado | 93 | las **93 en `tests/`** (test_services 40, test_models 19, test_menu 18, test_apis 16) | No — patrón correcto en tests. 0 en código de producción |
| B311/S311 `random.randint` no criptográfico | 1 | `utils.py:182` (`generate_random_id`) | Sí, Low — usar `secrets` si el id debe ser no predecible |
| F401 `time` importado sin usar | 5 | `cache_manager_v2.py`, `config_manager_v2.py`, `settings_manager.py`, `state_manager.py`, `user_manager.py` (línea 3 de cada uno) | Sí, Low |
| F841 `e` asignado y nunca usado | 4 | `favorites_manager.py:103,170`, `log_manager.py:185,207` | Confirma FIND-011 (excepts silenciosos) |

**Totales bandit en código real: High 0 · Medium 0 · Low 94.** (Un primer escaneo mostró
High 13 / Medium 35 / Low 974, pero provenía de `.venv/` (pip, pytest, coverage) — excluido,
queda limpio.)

## B.3 Lo que el SAST NO detectó (y el análisis manual sí)

| Hallazgo manual | ¿Lo ve bandit/ruff? | Por qué se escapa |
|-----------------|---------------------|-------------------|
| API key `"trilogy"` en 4 ubicaciones (FIND-004) | ❌ No (B105 = 0) | B105 matchea nombres exactos como `password`/`api_key`; aquí la variable es `api_key_omdb: str = "trilogy"` y el valor no tiene forma de secret |
| Passwords en texto plano (FIND-003, CWE-256) | ❌ No | Es lógica de aplicación (asignación/comparación de atributos), no una llamada en blacklist |
| IP hardcodeada en audit (FIND-006) | ❌ No | No está en las reglas por firma |
| Side effects al import (FIND-005, 14 módulos) | ❌ No | Es diseño, no patrón de llamada |
| Dead code 30 managers / duplicados v1-v2 (FIND-001/002) | ❌ No | bandit escanea lo que existe, no el grafo de imports |

Conclusión honesta: **el SAST automatizado (bandit/ruff) aporta poco aquí** — 0 hallazgos
medios/altos en código real. Los hallazgos de seguridad de peso del proyecto son de
**patrón/lógica/diseño**, que solo un análisis por lectura o por AST a medida encuentra.

## B.4 Correcciones por evolución del repo (el mismo día)

1. **FIND-009 «0 tests» → FALSO ahora.** Es el cambio más grande: se crearon
   `tests/test_apis.py`, `test_menu.py`, `test_models.py`, `test_services.py` y un
   `.venv/` con pytest y coverage. **`pytest -q` → 55 passed en 2.4s** (verificado).
   Cobertura total: **15%**; la capa viva cubre bien (api 100%, menu 86%, services 84-91%),
   pero **los 30 managers cotizan 0%** (refuerza FIND-001).

2. **Fue creada una nueva capa limpia** y está **cableada y viva**:
   - `api/`: `base_client.py` (APIClient), `omdb.py` (OmdbClient), `tvmaze.py` (TVMazeClient)
   - `services/`: `movie_service.py`, `series_service.py`, `catalog.py`
   - `models/`: `movie.py`, `series.py` (dataclasses)
   - `exceptions/`: `api_error.py`, `movie_not_found.py`, `series_not_found.py`
   - `ui/`: `menu.py`, `display.py`
   - `api_movies.py` ya delega en `OmdbClient`/`TVMazeClient`/`MovieService`/`SeriesService`;
     `main.py` usa `ui.menu`.
   El patrón de la nueva capa es consistente con Python 3.10+ (hints, dataclasses,
   excepciones específicas, `raise ... from`). Este es el camino correcto; el código de la
   mañana (managers singleton + app.py) es el residuo a eliminar.

3. **FIND-018 (imports sin uso) → se amplía**: no son 2, son **5** archivos con `import time`
   huérfano (ver B.2). Corregido.

4. **FIND-001/002/007 se mantienen vigentes**: re-verificado, **nadie importa** `app.py`,
   `logger.py`, `log_manager.py`, `data_manager.py`, `user_manager.py`, ni ningún par v1/v2
   (`cache_manager`, `cache_manager_v2`, `config_manager`, `config_manager_v2`). Los 30
   managers + `app.py` + `analyzer.py` siguen siendo código muerto; su coverage es 0%.

## B.5 Severidades tras el SAST (sin cambios en el top)

| Hallazgo | Severidad | Estatus |
|----------|-----------|---------|
| Dead code 30 managers + app.py + dupes v1/v2 | High | Se mantiene (cobertura 0% lo confirma) |
| Passwords en texto plano (user_manager) | High | Se mantiene (bandit no lo ve) |
| API key "trilogy" hardcodeada | High | Se mantiene (bandit no lo ve) |
| Side effects al import | High | Se mantiene |
| IP en auditoría | Medium (a la espera: ver si la nueva capa la hereda) | Se mantiene |
| 0 tests → **15% con 55 tests, solo capa viva** | **Baja de High a Medium** | Corregido: la capa viva ya tiene tests; falta cubrir/decidir los managers |

