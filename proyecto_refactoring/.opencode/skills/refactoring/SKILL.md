---
name: refactoring
description: Identifica y elimina malas prácticas del código Python - mutable default arguments, bare except, wildcard imports, hardcoded secrets, god functions, concatenación de strings, type hints faltantes - con una remediación priorizada por severidad. Usar al revisar, auditar o limpiar código Python, antes de abrir un pull request, o cuando se pida mejorar calidad, legibilidad o mantenibilidad.
license: MIT
compatibility: opencode
metadata:
  version: "2.0"
  language: python
---

## Contexto

- Version: 2.0 (Reusable Structure)
- Project: Any Python project
- Origen: patrones de detección de `code-quality-analyzer`

## Descripción Genérica
Skill para identificar y eliminar malas prácticas del código Python, mejorando la calidad, legibilidad y mantenibilidad del software. Formato estandarizado para reutilización en diferentes codebases.

## Estructura Estándar (Aplicable a Cualquier Proyecto)

### 1. Anti-Patrones Detectados y Severidad

| # | Anti-Patrón | Severidad | Descripción |
|---|-------------|-----------|-------------|
| 1 | `mutable default arguments` | **High** | `def func(param=[])` - estado compartido entre llamadas |
| 2 | `bare except` | **Critical** | `except:` sin excepción específica - oculta KeyboardInterrupt |
| 3 | `wildcard imports` | **High** | `from module import *` - colisiones de namespace |
| 4 | `hardcoded secrets` | **Critical** | API keys, passwords en código fuente |
| 5 | `string concatenation` | **Low** | `"text" + var` en lugar de f-strings |
| 6 | `missing type hints` | **Medium** | Funciones sin annotations |
| 7 | `bare except with pass` | **High** | Errores silenciosamente ignorados |
| 8 | `god functions` | **High** | Funciones con >8 parámetros o >50 líneas |
| 9 | `while loops manual` | **Medium** | `while` counter que podría ser `for` |
| 10 | `missing docstrings` | **Low** | Funciones públicas sin documentación |

### 2. Remediación Estándar por Severidad

#### Critical - Action Required Immediately
- **Bare excepts**: Cambiar `except:` por `except Exception as e:` o tipos específicos
- **Hardcoded secrets**: Mover a variables de entorno / secret managers
- **Mutable default args**: Cambiar por `param=None` y manejar adentro

#### High - Important for Quality/Security
- **Wildcard imports**: Reemplazar por imports explícitos
- **Mutable default arguments** (already covered): Ver detalle crítico
- **Bare except with pass**: Especificar excepción, no hacer pass
- **God functions**: Extraer responsabilidades en funciones pequeñas

#### Medium - Maintainability Impact
- **Missing type hints**: Agregar annotations consistentes
- **While loops innecesarios**: Convertir a `for` comprehensions
- **String concatenation**: Reemplazar por f-strings o `str.join()`

#### Low - Minor Improvements
- **String concatenation isolated**: Casos puntuales de mejora
- **Missing docstrings**: Agregar docstrings a funciones públicas clave

### 3. Patrones de Detección Reutilizables

#### Detector de Mutable Default Arguments
```python
# Pattern to find: def func(param=[]) or def func(param={})
# Affected: Any function with mutable default parameters
# Remediation: def func(param=None) + if param is None: param = []
```

#### Detector de Bare Excepts
```python
# Pattern to find: except: or except Exception: pass
# Affected: Bloques de error que silencian errores
# Remediation: except Exception as e: logger.error(...); raise
```

#### Detector de Hardcoded Secrets
```python
# Pattern to find: api_key = "...", password = "...", secret = "..."
# Affected: Cualquier string duro en código fuente
# Remediation: os.getenv("VAR_NAME") o configuración externa
```

### 4. Checklist de Remediación Proyectos

#### Phase 1 - Críticos (primer sprint)
- [ ] Reemplazar `mutable default arguments` en todas las funciones
- [ ] Mover `hardcoded secrets` a variables de entorno
- [ ] Especificar excepciones en todos los `except:` blocks
- [ ] Reemplazar `wildcard imports` por imports explícitos

#### Phase 2 - Altos (segundo sprint)
- [ ] Agregar `type hints` a funciones y métodos públicos
- [ ] Convertir `string concatenation` a f-strings
- [ ] Reestructurar `god functions` en funciones pequeñas

#### Phase 3 - Medianos/Bajos (iterativo)
- [ ] Agregar docstrings a funciones públicas
- [ ] Convertir `while` loops a `for` cuando sea posible
- [ ] Refactorizar nombre de variables no descriptivas

### 5. Aplicación al Proyecto Actual (Contexto)

#### Problemas Identificados en Este Codebase

| Categoría | Problemas | Severidad |
|-----------|-----------|-----------|
| **Mutable Default Args** | `services/movie_service.py` - métodos con listas por defecto | High |
| **Hardcoded Secrets** | `api/omdb.py:13` - `api_key: str = "trilogy"` | Critical |
| **Bare Excepts** | Varios archivos - `except:` sin tipo | Critical |
| **Type Hints Faltantes** | La mayoría de funciones sin annotations | Medium |
| **Wildcard Imports** | Revisar todos los `import *` | High |
| **String Concatenation** | Pocos casos identificados | Low |
| **While Loops** | Revisar bucles manuales en código | Medium |

#### Próximos Pasos de Remediación

1. **Immediate**: Quitar `api_key: str = "trilogy"` de omdb.py, usar env var
2. **This sprint**: Arreglar mutable default args en services
3. **Next sprint**: Agregar type hints a todo el proyecto
4. **Ongoing**: Cobertura de tests automatizados