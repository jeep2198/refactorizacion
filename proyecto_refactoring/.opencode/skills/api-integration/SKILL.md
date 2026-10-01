---
name: api-integration
description: Implementa y consume APIs REST de forma robusta, confiable y segura en Python - clientes con reintentos y backoff exponencial, manejo seguro de API keys vía variables de entorno, requests parametrizados, timeouts, rate limiting, y jerarquía de manejo de errores HTTP. Usar al crear o revisar clientes HTTP, integrar servicios externos como OMDB o TVMaze, o resolver timeouts, rate limits y errores 4xx/5xx.
license: MIT
compatibility: opencode
metadata:
  version: "2.0"
  language: python
---

## Contexto

- Version: 2.0 (Reusable Structure)
- Language: Python
- Target: Any Python project using REST APIs

## Descripción Genérica
Skill para implementar y consumir APIs REST de manera robusta, confiable y segura. Patrones aplicables a cualquier proyecto Python que consuma servicios web externos.

## Patrones de Integración API Estándar

### 1. Base Client con Reintentos y Backoff

#### Problema Resuelto
Llamadas a APIs externas fallan por causas temporales (network blips, rate limiting, timeouts). Los clientes deben reintentar automáticamente.

#### Patrón Estándar
```python
class APIClient:
    def __init__(self, base_url, timeout=10, max_retries=3, backoff_cap=4):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_cap = backoff_cap
    
    def get_json(self, path, params=None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as err:
                last_error = err
                sleep_time = min(2 ** attempt, self.backoff_cap)
                time.sleep(sleep_time)
        
        raise ConnectionError(f"Fallaron {self.max_retries} intentos para {url}") from last_error
```

#### Mejora Recomendada: Jitter Aleatorio
```python
import random

sleep_time = min(2 ** attempt, self.backoff_cap) + random.uniform(0, 0.1)
```
*Evita thundering herd cuando múltiples instancias fallan simultáneamente.*

### 2. Manejo Seguro de API Keys

#### Problema Crítico
Keys duras en código fuente son la principal vulnerabilidad de seguridad en proyectos Python.

#### Patrón Antiguo (A EVITAR)
```python
class OmdbClient:
    def __init__(self, api_key: str = "trilogy", **kwargs):  # ❌ MAL
        self.api_key = api_key
```

#### Patrón Recomendado
```python
import os

class OmdbClient:
    def __init__(self, **kwargs):
        api_key = os.getenv("OMDB_API_KEY")  # ✅ BIEN
        if not api_key:
            raise ValueError("OMDB_API_KEY environment variable required")
        self.api_key = api_key
```

#### Factory Pattern para Inyección
```python
def create_omdb_client() -> OmdbClient:
    """Factory que asegura configuración correcta."""
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        raise ValueError("OMDB_API_KEY no configurada en entorno")
    return OmdbClient(api_key=api_key)
```

### 3. Parameterized Requests (Nunca Concatenación)

#### Patrón Seguro
```python
# ✅ CORRECTO - Usar params dict
response = requests.get(base_url, params={"t": titulo, "apikey": key})

# ❌ INCORRECTO - Concatenación en URL
response = requests.get(f"{base_url}?t={titulo}&apikey={key}")
```

#### Benefits de `params=` dict
- Encoding automático de caracteres especiales
- Ordering consistente de parámetros
- Mejor legibilidad del código
- Prevención de injection attacks

### 4. Manejo Completo de Errores

#### Cuatro Tipos de Errores a Manejar

| Tipo | Causa | Manejo |
|------|-------|--------|
| **ConnectionError** | DNS fallo, network down, timeout | Retry con backoff |
| **HTTPError** | 4xx (client error) o 5xx (server error) | `raise_for_status()`, lanzar excepción personalizada |
| **ValueError** | Respuesta no es JSON válido | Capturar y logar, retornar None o default |
| **Timeout** | Lenta respuesta de API | Configurar timeout apropiado, retry o fallback |

#### Ejemplo de Manejo Comprehensivo
```python
def get_json_robust(self, path, params=None):
    try:
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        logger.error("Timeout calling %s", url)
        raise ConnectionError("Timeout reaching API")
    except requests.HTTPError as e:
        if 400 <= response.status_code < 500:
            raise APIError(f"Error de cliente: {response.status_code}", status_code=response.status_code)
        else:
            raise APIError(f"Error de servidor: {response.status_code}", status_code=response.status_code)
    except ValueError as e:
        logger.error("Invalid JSON response from %s", url)
        raise APIError("Invalid response from API")
```

### 5. HTTPS y Validación de URLs

#### Checklist de Seguridad
- [ ] Todas las BASE_URL comienzan con `https://`
- [ ] Verificar certificados SSL (verify=True por defecto en requests)
- [ ] No desactivar warnings de SSL innecesariamente
- [ ] Validar hostnames antes de conectar

### 6. Rate Limiting y Jitter

#### Estrategia de Backoff con Jitter
```
Attempt 0: wait 1s
Attempt 1: wait 2s + jitter(0, 0.5s) → 2-2.5s
Attempt 2: wait 4s + jitter(0, 0.5s) → 4-4.5s
Cap: max 4s (o configured value)
```

#### Header Retry-After
- Si la API retorna `Retry-After` header, usarlo en lugar de backoff calculado
- Compatible con políticas de la API server-side

## Aplicación por Tipo de API

### APIs de Búsqueda (OMDB, TVMaze, etc.)
- Parámetros de query variables (`?t=`, `?q=`, `?s=`)
- Manejo de respuestas paginadas
- Rate limiting considerado

### APIs de Datos (Bases de datos, servicios internos)
- Autenticación via tokens en headers
- Manejo de conexiones persistentes
- Timeout más corto (5-10s)

### APIs de Subida (Files, media)
- Chunked upload para archivos grandes
- Progress tracking
- Content-Type headers apropiados

## Checklist de Integración Robusta (Por Proyecto)

### Setup Inicial
- [ ] Base URL usa HTTPS
- [ ] Timeout configurado (default: 10s)
- [ ] Max retries configurado (default: 3)
- [ ] Backoff exponencial implementado
- [ ] Jitter añadido en backoff

### Autenticación
- [ ] API Keys de env vars (NUNCA hardcoded)
- [ ] Validation de key al inicio (raise ValueError si falta)
- [ ] Rotación de keys planificada

### Error Handling
- [ ] `raise_for_status()` después de toda petición
- [ ] Múltiples tipos de excepción capturados
- [ ] Excepciones personalizadas con status_code
- [ ] Logging de errores (sin filtrar datos sensibles)

### Request Construction
- [ ] `params=` dict usado (nunca concatenación URL)
- [ ] Encoding automático de parámetros
- [ ] Headers apropiados para cada endpoint

### Testing
- [ ] `pytest` tests con `requests.get` mock
- [ ] Tests para reintentos y backoff
- [ ] Tests para error handling (4xx, 5xx, timeout)
- [ ] Tests para params pasados correctamente
- [ ] Validación que apikey no va en URL

### Observability
- [ ] Logging de llamadas exitosas y fallidas
- [ ] Métricas de latency por endpoint
- [ ] Contador de reintentos fallidos
- [ ] Alertas para patrones de error repetidos