# Modelo de Datos: Verificación de Resolubilidad (Fase 1)

**Rama**: `003-resolubilidad` | **Fecha**: 2026-11-11 | **Especificación**: [spec.md](spec.md)

Este documento describe formalmente las entidades de dominio, DTOs, estructuras de datos internas, relaciones, invariantes y reglas de validación para la verificación de resolubilidad previa al juego, en cumplimiento con la Constitución del proyecto.

---

## 1. Entidades de Dominio y Objetos de Valor

Todas las clases de datos son inmutables (`frozen=True, slots=True`) y están redactadas en español.

```
                    ┌───────────────────────────────┐
                    │     ResultadoResolubilidad    │
                    ├───────────────────────────────┤
                    │ + es_resoluble: bool          │
                    │ + llaves_obtenidas: tuple     │
                    │ + llaves_no_obtenibles: tuple │
                    │ + frontera_bloqueada: tuple   │
                    │ + ubicaciones_llaves: tuple   │
                    │ + ciclos_dependencia: tuple   │
                    │ + motivo_no_resoluble: str    │
                    └───────────────┬───────────────┘
                                    │ 1
               ┌────────────────────┼────────────────────┐
               │ *                  │ *                  │ *
┌──────────────▼─────────────┐ ┌────▼────────────────┐ ┌─▼────────────────────────┐
│  FronteraBloqueadaPuerta   │ │  CicloDependencia   │ │  UbicacionLlaveDiagnostico │
├────────────────────────────┤ ├─────────────────────┤ ├────────────────────────────┤
│ + sala_origen: int         │ │ + llaves: tuple[str]│ │ + id_llave: str            │
│ + direccion: str           │ │ + descripcion(): str│ │ + sala: int | None         │
│ + llave: str | None        │ └─────────────────────┘ │ + enemigo: str | None      │
│ + sala_destino: int        │                         │ + estado: str              │
└────────────────────────────┘                         └────────────────────────────┘
```

---

### 1.1 `ResultadoResolubilidad`
- **Ubicación**: `cripta/modelo/resolubilidad.py`
- **Propósito**: Representar el diagnóstico inmutable completo derivado del análisis de resolubilidad de una cripta.
- **Atributos**:
  - `es_resoluble` (`bool`): `True` si la cripta puede completarse legítimamente partiendo de `sala_inicial`; `False` en caso contrario.
  - `llaves_obtenidas` (`tuple[str, ...]`): Secuencia causal ordenada de todas las llaves obtenibles en la cripta alcanzable.
  - `llaves_no_obtenibles` (`tuple[str, ...]`): Conjunto ordenado alfabéticamente de identificadores de llaves presentes en la cripta que el jugador no puede alcanzar.
  - `frontera_bloqueada` (`tuple[FronteraBloqueadaPuerta, ...]`): Tupla ordenada de puertas cerradas que limitan la región alcanzable final.
  - `ubicaciones_llaves` (`tuple[UbicacionLlaveDiagnostico, ...]`): Diagnóstico de ubicación de todas las llaves no obtenidas o requeridas por la frontera.
  - `ciclos_dependencia` (`tuple[CicloDependenciaLlaves, ...]`): Lista determinista de ciclos representativos por cada grupo de llaves bloqueadas entre sí.
  - `motivo_no_resoluble` (`str | None`): Texto explicativo resumido cuando `es_resoluble` es `False` (p. ej. `"no es posible alcanzar la sala de salida atravesando una puerta que requiera la llave de salida"`).
- **Métodos**:
  - `reporte_texto() -> str`: Genera el texto legible y estructurado del reporte para consola según las especificaciones de formato.

---

### 1.2 `FronteraBloqueadaPuerta`
- **Ubicación**: `cripta/modelo/resolubilidad.py`
- **Propósito**: Representar una puerta cerrada adyacente a la región alcanzable final que impide continuar la exploración hacia una sala inalcanzable (FR-RES-010).
- **Atributos**:
  - `sala_origen` (`int`): Identificador numérico de la sala alcanzada desde la cual se observa la puerta ($\ge 1$).
  - `direccion` (`str`): Dirección cardinal de salida (`"N"`, `"S"`, `"E"`, `"O"`).
  - `llave` (`str | None`): Identificador de la llave requerida para abrir la puerta. Es `None` si la puerta está cerrada permanentemente sin especificar llave (FR-RES-022).
  - `sala_destino` (`int`): Identificador numérico de la sala inalcanzable al otro lado de la puerta ($\ge 1$).
- **Invariante**: `sala_origen` pertenece a la región alcanzable y `sala_destino` pertenece a la región inalcanzable.

---

### 1.3 `CicloDependenciaLlaves`
- **Ubicación**: `cripta/modelo/resolubilidad.py`
- **Propósito**: Representar una dependencia circular concreta donde un conjunto de llaves se bloquean mutuamente tras puertas cerradas (FR-RES-012).
- **Atributos**:
  - `llaves` (`tuple[str, ...]`): Cadena ordenada de identificadores de llaves que forman el ciclo cerrado. Comienza y termina obligatoriamente con el mismo identificador, el cual debe ser la llave léxicamente menor de todo el ciclo (p. ej. `("itm_a", "itm_b", "itm_a")`).
- **Métodos**:
  - `formato() -> str`: Devuelve la representación textual de la cadena (p. ej. `"itm_a -> itm_b -> itm_a"`).

---

### 1.4 `UbicacionLlaveDiagnostico`
- **Ubicación**: `cripta/modelo/resolubilidad.py`
- **Propósito**: Diagnóstico del paradero conocido de una llave requerida por la frontera o inalcanzable (FR-RES-011, FR-RES-022).
- **Atributos**:
  - `id_llave` (`str`): Identificador textual de la llave.
  - `sala` (`int | None`): Identificador de la sala donde reside la llave, o `None` si la llave fue requerida por una puerta pero no figura en la consulta de llaves.
  - `enemigo` (`str | None`): Identificador de catálogo del enemigo que suelta la llave en su sala inicial, o `None` si la llave descansa en el suelo o no tiene ubicación.
  - `estado` (`str`): Categoría diagnóstica (`"obtenible"`, `"no_obtenible"`, `"sin_ubicacion"`).

---

### 1.5 DTOs Reutilizados de la Capacidad 001
- **`LlaveUbicacionDTO`** (`cripta/dto/llave_ubicacion_dto.py`):
  - `id: str`: Identificador de la llave (no vacío).
  - `sala: int`: Sala inicial donde reside o donde inicia el enemigo que la porta ($\ge 1$).
  - `enemigo: str | None`: Identificador de ficha de enemigo, o `None` si está en el suelo.

---

## 2. Estructuras de Datos de Trabajo Interno (Memoria de Análisis)

Para dar cumplimiento estricto al Principio I de la Constitución (sin `dict`, sin `set`, sin `bisect`, solo arreglos contiguos por posición entera), el análisis en memoria estructura sus variables de la siguiente forma:

| Variable Interna | Tipo Concreto | Propósito | Complejidad Consulta |
|---|---|---|---|
| `catalogo_llaves` | `list[str]` | Catálogo ordenado alfabéticamente de todas las llaves únicas de la cripta | Búsqueda binaria manual $O(\log K)$ |
| `llave_obtenida` | `list[bool]` | Bandera contigua de tamaño $K$ que indica si la llave $i$ fue adquirida | Acceso directo $O(1)$ |
| `puertas_pendientes` | `list[list[tuple]]` | Arreglo contiguo de tamaño $K$ con listas de puertas `(origen, dir, destino)` que esperan por la llave $i$ | Inserción $O(1)$, drenado $O(E_p)$ |
| `ubicaciones_por_llave` | `list[list[LlaveUbicacionDTO]]`| Arreglo contiguo de tamaño $K$ con las ubicaciones registradas para la llave $i$ | Acceso directo $O(1)$ |
| `llaves_en_sala` | `list[list[int]]` | Arreglo contiguo de tamaño `max_sala_id + 1` con los índices enteros de llaves en cada sala | Acceso directo $O(1)$ |
| `visitada` | `list[bool]` | Arreglo contiguo de tamaño `max_sala_id + 1` de salas alcanzadas | Acceso directo $O(1)$ |
| `candidatas` | `HeapMinimo` (`cripta/estructuras/heap_min.py`) | Índices enteros de llaves alcanzables aún no activadas; el mínimo es la de menor identificador | Inserción y extracción $O(\log K)$ |
| `cola` | `Cola` (`cripta/estructuras/cola.py`) | Cola FIFO propia para recorrido incremental | Encolar/desencolar en $O(1)$ |

---

## 3. Invariantes del Modelo y Reglas de Validación

### Regla 1: Condición de Resolubilidad Estricta (FR-RES-001)
Una cripta se clasifica como `es_resoluble = True` si y solo si se satisfacen copulativamente dos condiciones:
1. La llave de salida `llave_salida` fue efectivamente obtenida durante la exploración alcanzable (`llave_salida in llaves_obtenidas`).
2. La sala de salida `sala_salida` fue alcanzada cruzando una puerta cerrada cuya llave exigida coincide con `llave_salida`.
*Caso límite*: Si el jugador puede llegar a la `sala_salida` exclusivamente a través de puertas abiertas o puertas con otras llaves sin cruzar una puerta que exija `llave_salida`, la cripta es clasificada como NO resoluble.

### Regla 2: Orden Causal de Llaves Obtenibles (FR-RES-007)
En el reporte de una cripta resoluble, la secuencia `llaves_obtenidas` debe reflejar la cadena causal válida: ninguna llave $k$ puede figurar en la secuencia antes que las llaves necesarias para franquear las puertas que conducen a la sala donde $k$ reside.

### Regla 3: Desempate Determinista por Menor Identificador (FR-RES-008, SC-003)
Ante cualquier ambigüedad de orden:
- Entre llaves alcanzables simultáneamente: se adquiere y procesa primero la llave con menor identificador léxico (`id_llave`).
- En la frontera bloqueada: las puertas se ordenan por `(sala_origen, direccion, llave or "")`.
- En los ciclos de dependencia: cada ciclo inicia y termina en la llave léxicamente menor del ciclo, y los ciclos de distintos grupos se ordenan por su llave inicial en orden ascendente.

### Regla 4: Puertas Infranqueables y Llaves sin Ubicación (FR-RES-022)
- Una puerta cerrada que no especifique llave (`llave is None`) se trata como permanentemente infranqueable, no como error; se incluye en la frontera bloqueada con `llave=None`.
- Una puerta cerrada que exija una llave ausente en la consulta `/llaves` se incluye en la frontera bloqueada y la llave se diagnostica con estado `"sin_ubicacion"`, contabilizándose como no obtenible.

### Regla 5: Detección de Costos Contradictorios (FR-RES-021)
Si `CriptaMapa` detecta que una salida entre dos salas declara costos diferentes en cada extremo, se lanza `CriptaDatosInvalidosError` y se aborta inmediatamente sin generar ningún reporte de resolubilidad.

### Regla 6: Control de Presupuesto (FR-RES-023, SC-008)
Si `ContadorSolicitudes` detecta que el presupuesto se agota al descargar datos generales, esqueleto o llaves y los datos no están en `CacheDisco`, se lanza `CriptaLimiteError` y se aborta sin emitir ningún reporte parcial.

---

## 4. Máquina de Estados del Verificador de Resolubilidad

```
 [Inicio: Mapa y Llaves Cargados]
                 │
                 ▼
     [Inicializar Tablas Contiguas] ─── (Pre-indexar llaves en O(K log K))
                 │
                 ▼
       [Exploración Incremental] ◄─────────────────────────┐
                 │                                         │
        (Encolar vecinos abiertos)                         │
        (Almacenar puertas cerradas en espera)             │
                 │                                         │
                 ▼                                         │
      ¿Cola vacía de salas?                                │
        ├── No ──► [Desencolar y expandir]                 │
        └── Sí ──► ¿Hay llaves alcanzables no activadas?   │
                     ├── Sí ──► [Elegir menor ID de llave] ┘
                     │          (Activar llave y desbloquear puertas)
                     └── No ──► [Fin de Exploración Alcanzable]
                                           │
                                           ▼
                       ¿Se cumplió condición de victoria?
                         ├── Sí ──► [Estado: RESOLUBLE]
                         │          (Generar secuencia ordenada de llaves)
                         └── No ──► [Estado: NO RESOLUBLE]
                                    │
                                    ▼
                         [Construir Grafo Dep. Llaves]
                         (Flood-fill desde frontera bloqueada)
                                    │
                                    ▼
                         [DFS Tricolor de Ciclos]
                         (Aislar un ciclo representativo por grupo)
                                    │
                                    ▼
                         [Construir Diagnóstico Completo]
```
