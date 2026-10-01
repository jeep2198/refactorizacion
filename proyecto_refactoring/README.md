# Proyecto de Refactoring - Películas y Series

Proyecto educativo con malas prácticas intencionales para practicar refactoring.

## Objetivo

Conectar a APIs públicas de películas (OMDB y TVMaze) sin requerir API keys. El código está intencionalmente lleno de malas prácticas para que los estudiantes practiquen refactoring.

## Malas Prácticas Incluidas

### Arquitectura
- Variables globales en todas partes
- Sin separación de responsabilidades
- Sin principio SOLID
- Archivos de configuración excesivos (~60+ archivos `*_config.py`)

### Código
- Sin type hints
- Sin manejo de errores adecuado
- `from api_movies import *` (wildcard import)
- Strings hardcodeados
- Duplicación de código extrema
- Sin documentación
- `bare except:` clauses
- Argumentos mutables por defecto

### Estructura
- ~100 archivos Python en un solo directorio
- Múltiples implementaciones del mismo módulo (logger.py, log_manager.py)
- Configuración de caché de API con ~50+ archivos `api_cache_*_config.py`
- Sin tests unitarios
- Sin requirements.txt
- Sin virtual environment

### Seguridad
- Contraseñas en texto plano
- Sin validación de entrada
- Sin logging con módulo `logging`

## APIs Utilizadas

- **OMDB API**: demo key "trilogy" (no requiere registro)
- **TVMaze API**: pública, sin key

## Setup (una vez)

```bash
python3 -m venv .venv                # crear entorno virtual
.venv/bin/pip install -r requirements.txt   # instalar dependencias
```

Si el entorno ya existe, solo instalar/actualizar dependencias:

```bash
.venv/bin/pip install -r requirements.txt
```

## Cómo Ejecutar

```bash
.venv/bin/python main.py
```

La app arranca el menú interactivo de películas y series. La colección por defecto usa la API key de demo "trilogy"; para usar una propia, definir `OMDB_API_KEY` en el entorno.

## Cómo Ejecutar las Pruebas

La configuración está en `pyproject.toml` (`[tool.pytest.ini_options]`): descubre `tests/test_*.py` y ejecuta cobertura automáticamente (`--cov`).

```bash
.venv/bin/python -m pytest                    # todas las pruebas (55) + tabla de cobertura
.venv/bin/python -m pytest -q                 # más silencioso
.venv/bin/python -m pytest tests/test_apis.py # una sola suite
.venv/bin/python -m pytest -k "buscar"        # filtrar pruebas por nombre
.venv/bin/python -m pytest -o addopts=""      # sin cobertura automática
```

## Lint y Tipado

```bash
.venv/bin/ruff check .                # linter (config en pyproject.toml)
.venv/bin/ruff check --select S .     # reglas de seguridad (bandit-compatibles)
.venv/bin/mypy main.py api_movies.py  # chequeo estático de tipos (strict)
```

## Cómo Refactorizar

1. Eliminar variables globales
2. Separar responsabilidades en módulos claros
3. Agregar type hints
4. Implementar manejo de errores
5. Crear tests unitarios
6. Eliminar código duplicado
7. Usar f-strings en lugar de concatenación
8. Implementar inyección de dependencias
9. Seguir principios SOLID
10. Reducir archivos de configuración
