# ANÁLISIS DEL PROYECTO

## 1. Variables Globales Identificadas

### api_movies.py
- `API_KEY_OMDB` (línea 5) - API key hardcodeada
- `API_KEY_TMDB` (línea 6) - API key vacía
- `BASE_URL_OMDB` (línea 7) - URL base OMDB
- `BASE_URL_TMDB` (línea 8) - URL base TMDB
- `BASE_URL_TVMAZE` (línea 9) - URL base TVMaze
- `USUARIO_LOGUEADO` (línea 12) - No se usa
- `PELICULAS_FAVORITAS` (línea 13) - Lista mutable global
- `HISTORIAL_BUSQUEDAS` (línea 14) - Lista mutable global
- `CACHE_PELICULAS` (línea 15) - Diccionario cache global
- `CACHE_SERIES` (línea 16) - Diccionario cache global
- `CONFIG` (línea 17-22) - Diccionario configuración global

### main.py
- No declara variables globales propias, pero usa `from api_movies import *` que importa todas las globales de api_movies.py

## 2. Dependencias Entre Módulos

### api_movies.py
- Importa: `requests`, `json`
- No tiene dependencias internas del proyecto

### main.py
- Importa: `sys`, `os`, `time`, `random`
- Importa: `from api_movies import *` (wildcard import - mala práctica)
- Usa todas las funciones y variables globales de api_movies.py

## 3. Duplicación de Código Identificada

### api_movies.py
1. **Líneas 115-119 y 130-133**: Lógica de verificación de duplicados en favoritas
2. **Líneas 151-157**: Contadores manuales que podrían usar `len()`
3. **Líneas 27, 32, 42, 175, 185**: Concatenación de strings con `+` en lugar de f-strings

### main.py
1. **Líneas 35-78**: Bloques try/except repetitivos para mostrar campos de película
2. **Líneas 100-108, 159-163, 199-202, 220-223**: Bucles while con contador manual en lugar de for/enumerate

## 4. Bare Excepts y Manejo de Errores Deficiente

### api_movies.py
- **No hay manejo de errores** en `hacer_request()` (línea 24-34)
- **No hay validación** de respuestas de API
- **No hay manejo** de errores de red, timeouts, JSON inválido

### main.py
- **Línea 37**: `except:` bare para Title
- **Línea 42**: `except:` bare para Year
- **Línea 47**: `except:` bare para imdbRating
- **Línea 52**: `except:` bare para Genre
- **Línea 57**: `except:` bare para Director
- **Línea 62**: `except:` bare para Actors
- **Línea 67**: `except:` bare para Plot
- **Línea 72**: `except:` bare para Country
- **Línea 77**: `except:` bare para Awards
- **Línea 253**: `except:` bare para importar archivo

**Total: 10 bare excepts en main.py**

## 5. Archivos *_config.py Sin Uso

Se encontraron **93 archivos *_config.py** que NO se importan ni usan en el código:

- accessibility_config.py
- api_auth_config.py
- api_bulkhead_config.py
- api_cache_alerting_config.py
- api_cache_analytics_config.py
- api_cache_architecture_config.py
- api_cache_best_practices_config.py
- api_cache_cleanup_config.py
- api_cache_collaboration_config.py
- api_cache_compliance_config.py
- api_cache_compression_config.py
- api_cache_config.py
- api_cache_debug_config.py
- api_cache_deprecation_config.py
- api_cache_deprecation_schedule_config.py
- api_cache_disaster_recovery_config.py
- api_cache_distribution_config.py
- api_cache_documentation_config.py
- api_cache_evolution_config.py
- api_cache_failover_config.py
- api_cache_future_config.py
- api_cache_governance_config.py
- api_cache_innovation_config.py
- api_cache_integration_config.py
- api_cache_intelligence_config.py
- api_cache_intelligence_config.py
- api_cache_invalidation_config.py
- api_cache_legacy_config.py
- api_cache_lifecycle_config.py
- api_cache_load_testing_config.py
- api_cache_mentoring_config.py
- api_cache_metrics_config.py
- api_cache_migration_config.py
- api_cache_migration_schedule_config.py
- api_cache_monitoring_config.py
- api_cache_observability_config.py
- api_cache_performance_config.py
- api_cache_performance_testing_config.py
- api_cache_preloading_config.py
- api_cache_recommendations_config.py
- api_cache_recovery_config.py
- api_cache_reporting_config.py
- api_cache_resilience_testing_config.py
- api_cache_scalability_config.py
- api_cache_security_config.py
- api_cache_security_testing_config.py
- api_cache_serialization_config.py
- api_cache_stress_testing_config.py
- api_cache_testing_config.py
- api_cache_training_config.py
- api_cache_validation_config.py
- api_cache_warming_config.py
- api_caching_strategy_config.py
- api_circuit_breaker_config.py
- api_config.py
- api_debug_config.py
- api_degradation_config.py
- api_error_handling_config.py
- api_failover_config.py
- api_logging_config.py
- api_monitoring_config.py
- api_performance_config.py
- api_rate_limit_config.py
- api_rate_limiter_config.py
- api_retry_config.py
- api_security_config.py
- api_testing_config.py
- api_timeout_config.py
- api_timeout_retry_config.py
- backup_config.py
- cache_config.py
- cache_expiry_config.py
- database_config.py
- debug_config.py
- display_config.py
- email_config.py
- language_config.py
- log_config.py
- maintenance_config.py
- network_config.py
- notification_config.py
- performance_config.py
- privacy_config.py
- proxy_config.py
- search_config.py
- security_config.py
- storage_config.py
- theme_config.py
- ui_config.py

**Estos archivos deben eliminarse en la Fase 2.**

## 6. Otros Problemas Detectados

### Seguridad
- API keys hardcodeadas en api_movies.py (líneas 5-6)
- No hay validación de entrada del usuario
- No hay sanitización de nombres de archivo en exportar/importar

### Código Muerto
- `USUARIO_LOGUEADO` declarado pero nunca usado
- `API_KEY_TMDB` declarado pero nunca usado
- `random` importado en main.py pero nunca usado

### Malas Prácticas
- `delay(1)` innecesario en línea 114 de main.py
- `os.system()` para limpiar pantalla (no portable)
- Wildcard import `from api_movies import *`
- Funciones con más de 50 líneas
- Mezcla de lógica de negocio con UI

### Tipado
- **Cero type hints** en todo el código
- No hay validación de tipos en funciones

## 7. Resumen de Problemas Críticos

| Categoría | Cantidad |
|-----------|----------|
| Variables globales | 11 |
| Bare excepts | 10 |
| Archivos config sin uso | 93 |
| Funciones sin type hints | ~30 |
| Strings concatenados con + | ~20 |
| Bucles while manuales | 6 |
| Bloques try/except duplicados | 9 |
