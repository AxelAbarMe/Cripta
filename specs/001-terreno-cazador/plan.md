# Plan de Implementación: Terreno y Cazador

**Rama**: `001-terreno-cazador` | **Fecha**: 2026-11-09 | **Especificación**: [spec.md](spec.md)

**Entrada**: Especificación de funcionalidad desde `specs/001-terreno-cazador/spec.md` y restricciones obligatorias de la Constitución (`.specify/memory/constitution.md`).

---

## Resumen

La capacidad **Terreno y Cazador** introduce costos de desplazamiento variables en las salidas del laberinto ($\text{costo} \ge 1$, por defecto 100) y un nuevo comportamiento de enemigo inteligente (**cazador**) dotado de un atributo de `rango` de percepción. El cazador persigue al jugador a través de la ruta de costo acumulado mínimo sobre salidas abiertas en ese instante, atacando si comparte sala, esperando si no hay ruta o si la distancia excede su rango, y desempatando siempre a favor de la sala vecina con menor identificador numérico.

Para garantizar un tiempo de ciclo de eventos menor a 20 ms con decenas de cazadores activos sin violar las prohibiciones del curso (`heapq`, `bisect`, `collections`, `networkx`, `set` y `dict`), el diseño adopta:
1. Una búsqueda de camino más corto compartida (Dijkstra único desde la sala actual del jugador) acotada por el rango máximo de los cazadores activos.
2. La reutilización y ampliación del montículo binario propio `HeapMinimo` (`cripta/estructuras/heap_min.py`) como cola de prioridad.
3. Un arreglo plano contiguo `list` indexado directamente por posición entera de `sala_id` para el registro de distancias mínimas y visitados en $O(1)$.
4. Una estrategia de invalidación dirigida por eventos (movimiento del jugador, cambios en puertas, retroceso), manteniendo la tabla intacta ante movimientos de cazadores o cambios de velocidad.
5. Un bloque inicial y separable de contrato de datos (`costo` en `SalidaDTO`, `rango` en `EnemigoDTO`, nuevo DTO `LlaveUbicacionDTO` y método `obtener_llaves` en `ClienteCripta`) listo para fusionarse de forma temprana y desbloquear las capacidades 002, 003 y 004.

---

## Contexto Técnico

**Lenguaje/Versión**: Python 3.11+ (desarrollado y probado sobre Python 3.12.3 en Windows con finales de línea CRLF).

**Dependencias Principales**: Ninguna biblioteca externa nueva. Solo biblioteca estándar (`struct`, `json`, `math`, `typing`) y `requests` (ya presente en `requirements.txt`). Prohibido terminantemente el uso de `heapq`, `bisect`, `collections`, `networkx` o bibliotecas de grafos.

**Almacenamiento**: Persistencia local en `datos/cache/` (JSON estructurado por clave versionada) y `datos/partida.sav` (formato binario propio con `struct`, ruta en tiempo de ejecución). Detección automática de incompatibilidad por versión sin borrado manual de archivos.

**Pruebas**: Módulo estándar `unittest` en `tests/`, con ejecutores deterministas `cliente_falso.py` y `cripta_artificial.py`. Todas las pruebas de aceptación citan explícitamente su requisito `FR-TER-NNN`.

**Plataforma Objetivo**: Terminal de consola de al menos 113 columnas en Windows / Linux / macOS.

**Tipo de Proyecto**: Juego de mazmorra por turnos y simulador de eventos discretos en arquitectura MVC estricta con CLI y modo `--offline` desacoplado.

**Objetivos de Rendimiento**:
- Ciclo de eventos completo entre dos decisiones del jugador $< 20\text{ ms}$ en la cripta de referencia, aun con decenas de cazadores activos en persecución simultánea (FR-TER-020).
- Tiempo de decisión por cazador en modo compartido: $O(1)$ tras la búsqueda inicial (hipótesis a confirmar con `--bench` de sobrecosto marginal).

**Restricciones**:
- Cumplimiento irrestricto de la Constitución: estructuras a mano, determinismo con `random.Random(semilla)` local, prohibición total de `dict` y `set` como índice o caché evaluada, sin datos fijos de criptas en código.
- Cero líneas adicionales en `partida.log` por movimientos o decisiones de cazadores (solo acciones aceptadas del jugador).
- Compatibilidad retroactiva: las 222 pruebas de la Parte I deben seguir terminando en `OK`.

**Escala/Alcance**: Laberintos de hasta 1 000 salas, con decenas de cazadores activos simultáneos y rangos de 1 a 1 000 unidades de costo.

---

## Verificación Constitucional

*Control de Paso: Debe aprobarse antes de la investigación de Fase 0. Re-verificar tras el diseño de Fase 1.*

| Principio Constitucional | Estado | Evidencia y Justificación en este Plan |
|---|---|---|
| **I. Estructuras a mano** | **PASÓ** | No se utiliza `heapq`, `bisect`, `collections`, `networkx`, `set` ni `dict` en la búsqueda de rutas ni en el registro de distancias. Se reutiliza y extiende `HeapMinimo` propio y se usa `list` como almacenamiento contiguo indexado por posición entera. |
| **II. Determinismo** | **PASÓ** | Desempate estricto por menor identificador numérico de sala vecina (FR-TER-013) y menor número de secuencia en agenda (FR-TER-022). Aleatoriedad gobernada por `random.Random(semilla)`. |
| **III. MVC y adaptadores** | **PASÓ** | `BuscadorRutas` reside en el Modelo sin llamadas de red, archivos ni vista. Las banderas `--bench` y `--replay` se ejecutan sin instanciar componentes de presentación interactiva. |
| **IV. Sin datos de cripta concreta** | **PASÓ** | Ningún ID de sala, costo ni rango específico está codificado en el código fuente. Todos los parámetros se leen dinámicamente desde el esqueleto y catálogo. |
| **V. Presupuesto de red** | **PASÓ** | La consulta `GET /criptas/{id}/llaves` descuenta una solicitud de `presupuesto_solicitudes`, maneja HTTP 429 con reintentos y soporta persistencia en caché versionada. |
| **VI. Rendimiento con --bench** | **PASÓ** | Se planifican cargas sintéticas reproducibles por semilla (`ruta_cazador`, `invalidacion`) comparando el diseño frente a las alternativas descartadas (cálculo individual y recalcular siempre). |
| **VII. Especificación antes que código** | **PASÓ** | `spec.md` fue completado y clarificado previamente sin mención de clases ni estructuras. Todas las tareas de diseño trazan a requisitos funcionales `FR-TER-NNN`. |
| **VIII. Compatibilidad con Parte I** | **PASÓ** | Se garantiza que las 222 pruebas previas pasen intactas. El contrato es tolerante hacia campos nuevos y compatible con los formatos existentes. |

---

## Estructura del Proyecto

### Documentación (esta funcionalidad)

```text
specs/001-terreno-cazador/
├── spec.md              # Requisitos y escenarios de aceptación (Fase 2 spec)
├── plan.md              # Este documento técnico de implementación (Fase 4 plan)
├── research.md          # Investigación técnica y análisis de alternativas (Fase 0)
├── data-model.md        # Entidades, campos y máquinas de estado (Fase 1)
├── quickstart.md        # Guía paso a paso de validación y pruebas (Fase 1)
├── contracts/           # Contratos formales de interfaces y JSON Schemas (Fase 1)
│   ├── contrato_servicio_llaves.json
│   └── contrato_datos_p2.md
└── tasks.md             # Tareas ejecutables (Fase 5 tasks - generado por /speckit-tasks)
```

### Código Fuente (raíz del repositorio)

```text
cripta/
├── dto/
│   ├── salida_dto.py            # Modificado: agrega campo costo (int >= 1, def 100)
│   ├── enemigo_dto.py           # Modificado: agrega campo rango (int >= 1 para cazador), valida datos externos con CriptaDatosInvalidosError/CriptaApiError
│   └── llave_ubicacion_dto.py   # Nuevo: DTO inmutable para GET /criptas/{id}/llaves
├── infraestructura/
│   ├── puertos.py               # Modificado: protocolo ClienteCripta agrega obtener_llaves()
│   ├── cliente_http.py          # Modificado: implementa obtener_llaves() con presupuesto y 429
│   ├── cliente_offline.py       # Modificado: implementa obtener_llaves() leyendo fixtures
│   ├── cliente_general.py       # Modificado: delegación sincronizada de obtener_llaves()
│   ├── cache.py                 # Modificado: almacenamiento de llaves versionado
│   └── serializacion.py         # Modificado: serialización y deserialización de costo y rango
├── modelo/
│   ├── buscador_rutas.py        # Nuevo: Dijkstra compartido, cola HeapMinimo y tabla plana
│   ├── comportamiento_enemigo.py# Modificado: incorpora lógica de decisión _decidir_cazador
│   ├── enemigo.py               # Modificado: expone propiedad rango de la ficha
│   └── partida.py               # Modificado: costos variables en movimiento, invalidación, agenda
├── estructuras/
│   └── heap_min.py              # Modificado: agrega métodos esta_vacio() y __len__()
└── bench/
    └── cargas_bench.py          # Modificado: añade cargas ruta_cazador e invalidacion

scripts/
└── generar_fixtures.py          # Modificado: añade regeneración de fixtures con costo, rango y endpoint /llaves

tests/
├── dto/
│   ├── test_salida_dto.py       # Nuevo: Pruebas de costo por defecto y validación
│   ├── test_enemigo_dto.py      # Nuevo: Pruebas de rango obligatorio para cazador
│   └── test_llave_ubicacion_dto.py # Nuevo: Pruebas del DTO de llaves
├── infraestructura/
│   ├── test_cliente_offline_llaves.py # Nuevo: Pruebas de cliente offline y presupuesto
│   └── test_cache_llaves.py     # Nuevo: Pruebas de invalidación por versión
├── modelo/
│   ├── test_buscador_rutas.py   # Nuevo: Pruebas unitarias de Dijkstra, poda por rango y desempate
│   └── test_cazador_decisiones.py # Nuevo: Pruebas de decisiones del cazador (ataque, espera, movimiento)
└── aceptacion/
    ├── test_terreno_costos.py   # Nuevo: Escenarios de aceptación de costos y velocidad (FR-TER-001 a 006)
    └── test_cazador_persecucion.py # Nuevo: Escenarios de persecución y desempate (FR-TER-008 a 015)
```

---

## Detalle Técnico y Decisiones por Problema

### 1. Búsqueda de Ruta de Costo Mínimo y Selección del Siguiente Nodo

- **Operaciones Reales y Frecuencia**:
  - En cada ciclo donde hay al menos un cazador activo persiguiendo al jugador: selección del siguiente nodo de menor costo acumulado y cálculo de distancias hacia el objetivo. Frecuencia: 1 búsqueda Dijkstra por cada movimiento del jugador o cambio de puertas.
- **Alternativas Evaluadas y Descarte**:
  - *Alternativa A (Búsqueda lineal en lista contigua)*: Descartada porque extraer el mínimo toma $O(V)$, resultando en $O(V^2 + E)$. Con 400 salas, se plantea como hipótesis a confirmar con `--bench` que la búsqueda lineal excedería el límite de 20 ms por ciclo.
  - *Alternativa B (Algoritmo A\* individual con heurística)*: Descartada porque el laberinto no garantiza una métrica euclidiana admisible y A\* individual impide compartir el cálculo entre múltiples cazadores.
- **Decisión**: Algoritmo de Dijkstra clásico utilizando la cola de prioridad propia `HeapMinimo` (`cripta/estructuras/heap_min.py`) insertando tuplas `(distancia_acumulada, sala_id)`.
- **Complejidad**: $O((V + E) \log V)$ para la búsqueda completa; con poda por rango $R_{\max}$, acotada a $O((V_R + E_R) \log V_R)$.

---

### 2. Registro de Distancias y Nodos Visitados sin `dict` ni `set`

- **Operaciones Reales y Frecuencia**:
  - Consulta y actualización de la distancia tentativa a cada sala descubierta. Frecuencia: tantas veces como aristas se relajen ($4 \times V_R$).
- **Alternativas Evaluadas y Descarte**:
  - *Alternativa A (`VectorOrdenado` por `sala_id`)*: Descartada porque cada inserción dinámica toma $O(V)$, costando $O(V^2)$ para construir la tabla.
  - *Alternativa B (Tabla hash propia con sondeo abierto)*: Descartada por complejidad innecesaria cuando los identificadores de sala son enteros densos acotados.
- **Decisión**: Arreglo plano `list[int | None]` de tamaño `max_sala_id + 1` inicializado con `None`, y lista booleana `list[bool]` para nodos cerrados.
- **Complejidad**: Consulta y actualización en $O(1)$ puro. Espacio $O(V)$.

---

### 3. Cálculo Compartido vs Individual ante Múltiples Cazadores

- **Operaciones Reales y Frecuencia**:
  - $H$ cazadores ($H \in [1, 30]$) deben decidir su siguiente paso en un mismo ciclo de eventos hacia la sala actual del jugador $S_J$.
- **Alternativas Evaluadas y Descarte**:
  - *Alternativa A (Dijkstra individual hacia adelante por cada cazador)*: Descartada porque con 30 cazadores se ejecutan 30 búsquedas independientes ($30 \times O((V + E) \log V)$), con la hipótesis a confirmar con `--bench` de que superaría el límite de 20 ms por ciclo.
  - *Alternativa B (Matriz de todos los pares / Floyd-Warshall)*: Descartada por costo prohibitivo de memoria $O(V^2)$ y tiempo $O(V^3)$, y necesidad de recalcularla entera ante cualquier cambio de puerta.
- **Decisión**: Cálculo compartido mediante una **única búsqueda Dijkstra inverso desde la sala del jugador $S_J$**.
  - Dado que los costos y las puertas son simétricos (FR-TER-002), $\text{dist}(u, S_J) = \text{dist}(S_J, u)$.
  - Cada cazador en sala $u$ examina en su turno sus salidas abiertas hacia vecinas $v$ y evalúa la condición de optimalidad:
    $$\text{costo}(u, v) + \text{dist}(v, S_J) == d$$
- **Condiciones de rendimiento: cuándo conviene cuál y medición con `--bench`**:
  - *Cálculo compartido*: Es la opción conveniente cuando hay múltiples cazadores activos ($H > 1$) y rangos relativamente homogéneos, al amortizar la búsqueda $O((V_R + E_R) \log V_R)$ entre todos los cazadores ($+ H \times O(1)$).
  - *Cálculo individual*: Podría convenir en rendimiento únicamente en casos de muy pocos cazadores (ej. $H = 1$) o cuando los rangos son sumamente dispares con un $R_{\max}$ grande (un solo cazador con rango inmenso que obliga a explorar gran parte del laberinto, mientras los demás tienen rangos mínimos). En ese escenario extremo, búsquedas individuales acotadas localmente podrían visitar menos aristas que una búsqueda compartida expandida hasta $R_{\max}$.
  - *Validación empírica*: Esta disyuntiva y las condiciones exactas donde el cálculo compartido supera al individual se medirán con `--bench` (carga `ruta_cazador`).
- **Condiciones bajo las cuales cambia la respuesta**:
  - La respuesta **nunca cambia** respecto a calcular desde cero si: (a) se evalúa el estado actual de puertas; (b) se desempata por $\min(v.id)$; (c) se invalida la tabla si el jugador se mueve o una puerta cambia de estado.
- **Complejidad**: 1 búsqueda Dijkstra $O((V_R + E_R) \log V_R) + H \times O(1)$. Para 30 cazadores, se plantea como hipótesis a confirmar con `--bench` que el tiempo total se mantendrá sustancialmente por debajo de los 20 ms.

---

### 4. Política de Invalidación de Caché y Eventos del Laberinto

- **Operaciones Reales y Frecuencia**:
  - Evaluación de la validez de la tabla de distancias ante cada evento del juego.
- **Alternativas Evaluadas y Descarte**:
  - *Alternativa A (Recalcular siempre sin caché)*: Descartada porque re-ejecuta Dijkstra en cada turno de cada cazador, incluso cuando nada en el laberinto ha cambiado.
  - *Alternativa B (Algoritmos dinámicos de actualización de caminos más cortos / D\* Lite)*: Descartada por alta complejidad de implementación en Python sin estructuras estándar, con sobrecosto superior a un Dijkstra estático limpio en grafos de este tamaño.
- **Decisión**: Reutilización con **invalidación selectiva dirigida por eventos**:
  - Se invalida la tabla ante: (1) `Partida._mover`: el jugador cambia de sala; (2) `Partida._abrir`: se abre una puerta; (3) `EfectoCierrePuerta`: se cierra una puerta; (4) `Partida._usar_pergamino`: retroceso temporal.
  - Se **conserva** la tabla ante: turnos y movimientos de cazadores (no bloquean salas ni puertas), muerte de enemigos, cambios de velocidad de cualquier actor.
- **Complejidad**: Comprobación de validez en $O(1)$ (`if not self._valido: ...`).

---

### 5. Límite por Rango de Persecución

- **Operaciones Reales y Frecuencia**:
  - Cada cazador posee un atributo `rango` ($\ge 1$). Si la distancia excede el rango, espera (FR-TER-011).
- **Alternativas Evaluadas y Descarte**:
  - *Alternativa A (Explorar el laberinto completo siempre)*: Descartada porque desperdicia tiempo explorando cientos de salas lejanas cuando los cazadores tienen rangos pequeños (ej. rango 150 en cripta de 1 000 salas).
  - *Alternativa B (Búsquedas individuales acotadas por el rango de cada cazador)*: Descartada porque pierde los beneficios del cálculo compartido.
- **Decisión**: Durante la búsqueda compartida desde $S_J$, acotar la expansión fijando $R_{\max} = \max_{h \in \text{cazadores activos}} (h.\text{rango})$.
  - Al extraer un nodo del montículo con distancia $> R_{\max}$, el bucle de Dijkstra se detiene inmediatamente.
  - Dado que todos los costos de salida son enteros $\ge 1$, ninguna sala futura puede tener distancia $\le R_{\max}$.
- **Complejidad**: El costo temporal depende de la sub-región de radio $R_{\max}$, no del tamaño total del laberinto ($O((V_R + E_R) \log V_R)$ con $V_R \ll V$).

---

### 6. Desempate Determinista por Menor Identificador (FR-TER-013)

- **Operaciones Reales y Frecuencia**:
  - Cada vez que un cazador se mueve y existen múltiples rutas de igual costo mínimo total $d$.
- **Alternativas Evaluadas y Descarte**:
  - *Alternativa A (Desempate interno en la cola de prioridad)*: Descartada porque el orden de extracción en Dijkstra desde el objetivo no refleja necesariamente el identificador de la primera vecina saliente desde la posición del cazador.
  - *Alternativa B (Selección aleatoria entre candidatas)*: Descartada porque viola el principio fundamental de determinismo estricto.
- **Decisión**: En el turno del cazador en la sala $u$:
  1. Para cada vecina abierta $v \in \text{vecinos}(u)$, calcular $D_v = \text{costo}(u, v) + \text{dist}(v, S_J)$.
  2. Determinar la distancia mínima alcanzable $d = \min_{v} (D_v)$.
  3. Filtrar todas las vecinas que cumplen exactamente $D_v == d$.
  4. Seleccionar deterministamente aquella vecina con menor identificador numérico: $\min(v.\text{id})$.
- **Complejidad**: $O(1)$ (a lo sumo 4 salidas evaluadas por sala).

---

### 7. Impacto en la Agenda del Reloj Virtual

- **Operaciones Reales y Frecuencia**:
  - Cálculo de intervalos para desplazamientos: $\text{intervalo} = \max(1, \text{costo} \cdot 100 // \text{velocidad})$.
  - Reprogramación de eventos ante cambios de velocidad: $\text{restante} = \max(1, (t_{\text{sig}} - t) \cdot v_{\text{ant}} // v_{\text{nueva}})$.
- **Decisión**:
  - Reutilizar `calcular_intervalo` y `calcular_tiempo_reprogramado` de `cripta/modelo/reloj.py`.
  - Asegurar que salidas de costo 1 y velocidad 200 produzcan un intervalo de al menos 1 unidad temporal.
  - Todo evento reprogramado se inserta en `RelojEventos` asignando un nuevo número de secuencia determinista incremental (`self._secuencia += 1`), garantizando desempates totales sin recurrir al reloj real.

---

### 8. Contrato de Datos y Desacoplamiento para Fusión Temprana

- **Operaciones Reales y Frecuencia**:
  - Ingesta de esqueleto con `costo`, catálogo con `rango`, consulta `GET /criptas/{id}/llaves`, regeneración de fixtures (`scripts/generar_fixtures.py`) y validación de versiones.
- **Decisión**:
  - Modelar como un bloque modular de código y pruebas (DTOs, interfaces de puerto, clientes HTTP y offline, regeneración de fixtures en `scripts/generar_fixtures.py` y caché versionada) que puede integrarse en un PR inicial a `main` antes de la lógica del cazador, desbloqueando el trabajo concurrente de las funcionalidades 002, 003 y 004.

---

## Impacto en Código Existente

| Archivo (Ruta Real) | Cambio Requerido | Justificación Técnica |
|---|---|---|
| `cripta/dto/salida_dto.py` | Modificado | Agregar campo `costo: int = 100` y validación en `desde_json` ($\ge 1$). |
| `cripta/dto/enemigo_dto.py` | Modificado | Agregar campo `rango: int \| None = None` y validación para cazadores lanzando `CriptaDatosInvalidosError`/`CriptaApiError` con ID de ficha en el mensaje si es inválido. |
| `cripta/dto/llave_ubicacion_dto.py` | **Nuevo** | Definición inmutable de `LlaveUbicacionDTO` para `GET /criptas/{id}/llaves`. |
| `cripta/infraestructura/puertos.py` | Modificado | Añadir método abstracto `obtener_llaves(id_cripta)` en protocolo `ClienteCripta`. |
| `cripta/infraestructura/cliente_http.py` | Modificado | Implementar `obtener_llaves` con presupuesto, timeout y reintentos 429. |
| `cripta/infraestructura/cliente_offline.py` | Modificado | Implementar `obtener_llaves` leyendo `fixtures/<id>/llaves.json`. |
| `cripta/infraestructura/cliente_general.py` | Modificado | Añadir delegación sincronizada a `obtener_llaves`. |
| `cripta/infraestructura/cache.py` | Modificado | Persistencia y recuperación de `llaves.json` versionado por versión de cripta. |
| `cripta/infraestructura/serializacion.py` | Modificado | Incluir `costo` en esqueleto y `rango` en catálogo al serializar a JSON. |
| `scripts/generar_fixtures.py` | Modificado | Incorporar regeneración y verificación de fixtures con `costo` en salidas, `rango` en catálogo y consulta de `llaves.json`. |
| `cripta/modelo/buscador_rutas.py` | **Nuevo** | Implementación de `BuscadorRutas` (Dijkstra compartido, poda y desempate). |
| `cripta/modelo/comportamiento_enemigo.py` | Modificado | Añadir función `_decidir_cazador` y enlace en `decidir_accion_enemigo`. |
| `cripta/modelo/enemigo.py` | Modificado | Exponer propiedad `rango` tomada de su ficha de catálogo. |
| `cripta/modelo/partida.py` | Modificado | Usar costo de salida en `_mover`, costo de salida en `_turno_enemigo`, invalidar `BuscadorRutas` en eventos clave (`_mover`, `_abrir`, etc.). |
| `cripta/estructuras/heap_min.py` | Modificado | Añadir métodos `esta_vacio()` y `__len__()` sobre la lista existente. |
| `cripta/bench/cargas_bench.py` | Modificado | Registrar cargas sintéticas `ruta_cazador` e `invalidacion`. |
| `cripta/servicios/servicio_bench.py` | Modificado | Habilitar ejecución de las nuevas cargas de `--bench`. |
| `cripta/modelo/resultado_partida.py` | **Sin cambios** | Ningún requisito funcional (FR) de la especificación solicita cambios en las vistas del resultado ni DTOs de presentación. |
| `cripta/vista/vista_consola.py` | **Sin cambios** | Ningún requisito funcional (FR) solicita modificaciones en la interfaz de consola en esta funcionalidad. |
| `cripta/constantes.py` | **Sin cambios** | Mantiene constantes de acciones y direcciones intactas. |
| `cripta/excepciones.py` | **Sin cambios** | Reutiliza excepciones existentes de la Parte I: se usa `CriptaDatosInvalidosError` (en `--offline`/fixtures) y `CriptaApiError` (en API REST) con el ID de la ficha en el mensaje para cazadores sin rango u otros datos externos corruptos; `ValueError` se reserva estrictamente para errores de programación interna. |
| `cripta/modelo/actor.py` | **Sin cambios** | Atributos base de actor compatibles. |
| `cripta/modelo/jugador.py` | **Sin cambios** | Comportamiento del jugador se mantiene idéntico. |
| `cripta/modelo/inventario.py` | **Sin cambios** | Gestión de inventario sobre lista doble enlazada sin alteraciones. |
| `cripta/modelo/combate.py` | **Sin cambios** | Fórmulas de daño y azar se conservan intactas. |
| `cripta/modelo/bitacora_mensajes.py` | **Sin cambios** | Bitácora en cola circular sin alteraciones. |
| `cripta/modelo/historial_retroceso.py` | **Sin cambios** | Historial de 5 intervalos funciona sin modificaciones. |
| `cripta/infraestructura/guardado_binario.py` | **Sin cambios** | Compatible con el formato actual (la versión nueva corresponde a 004). |
| `cripta/infraestructura/partida_log.py` | **Sin cambios** | Mantiene registro exclusivo de acciones del jugador. |

---

## Mediciones `--bench` Previstas

### 1. Carga `ruta_cazador` (Cálculo Compartido vs Alternativa Descartada Individual)
- **Comando**: `py -m cripta --bench --solo ruta_cazador`
- **Configuración Sintética**: Cripta sintética generada deterministamente con semilla fija (`SEMILLA_BENCH = 42`), 400 salas, salidas con costos aleatorios ponderados entre 10 y 250.
- **Escenarios Evaluados**:
  - $H = 1, 10, 30$ cazadores activos simultáneos.
  - Rangos de persecución: pequeño ($R = 100$) vs amplio ($R = 500$).
- **Métricas a Reportar**:
  - Tiempo por ciclo con **cálculo compartido** (Decisión elegida).
  - Tiempo por ciclo con **cálculo individual desde cada cazador** (Alternativa descartada).
  - Factor de aceleración: $\text{Tiempo}_{\text{individual}} / \text{Tiempo}_{\text{compartido}}$.
- **Criterio de Aceptación**: Con 30 cazadores, el cálculo compartido debe completar el ciclo en $< 5\text{ ms}$ (bien por debajo del límite de 20 ms), mientras que el cálculo individual superará previsiblemente los 35–50 ms.

---

### 2. Carga `invalidacion` (Reutilización con Invalidación vs Alternativa Descartada "Recalcular Siempre")
- **Comando**: `py -m cripta --bench --solo invalidacion`
- **Configuración Sintética**: 20 cazadores activos durante 100 ticks virtuales en dos regímenes:
  - **Escenario Puertas Estables**: El jugador espera o ataca sin cambiar de sala; ninguna puerta cambia de estado.
  - **Escenario Puertas Inestables**: 5 puertas con cierres automáticos frecuentes (cada 15 ticks) que obligan a invalidar periódicamente.
- **Métricas a Reportar**:
  - Número de ejecuciones de Dijkstra y tiempo acumulado con **invalidación selectiva** (Decisión elegida).
  - Número de ejecuciones de Dijkstra y tiempo acumulado con **recalcular siempre en cada turno** (Alternativa descartada).
- **Criterio de Aceptación**: En puertas estables, la decisión elegida realiza exactamente 1 búsqueda frente a cientos de recálculos de la alternativa descartada ($> 50\times$ más rápida). En puertas inestables, el recálculo selectivo mantiene el ciclo dentro del presupuesto de 20 ms.

---

### 3. Mediciones de Regresión de la Parte I
- **Comandos**:
  - `py -m cripta --bench --solo ciclo` (verificar $< 20\text{ ms}$ con terreno y cazadores activos).
  - `py -m cripta --bench --solo agenda` (verificar rendimiento de `HeapMinimo` con intervalos variables y reprogramaciones densas).
  - `py -m cripta --bench --solo historial` (verificar costo de reversión de closures ante desplazamientos de cazadores).

---

## Límites Conocidos de la Decisión

1. **Topología con Identificadores de Sala Dispersos**:
   - La tabla contigua directa `list[int | None]` asume que `max_sala_id` es del orden del número de salas $V$. Si una cripta presentara IDs arbitrariamente gigantescos (ej. ID $10^8$), una lista directa consumiría memoria excesiva. En caso de detectarse laberintos con IDs hiper-dispersos en la validación, la alternativa es indexar por posición densa ordenada ($0 \dots V-1$).
2. **Cazadores con Rangos Extremadamente Heterogéneos**:
   - Dado que la búsqueda compartida expande hasta $R_{\max} = \max(rango)$, si un solo cazador tiene rango 1 000 y otros 20 tienen rango 50, la búsqueda explora hasta 1 000. No obstante, al ser una única búsqueda compartida, el costo total sigue siendo drásticamente menor que 20 búsquedas independientes.
3. **Multiplicidad de Objetivos (Extensión Teórica Futura)**:
   - El diseño de Dijkstra inverso asume un único objetivo común (el jugador). Si en el futuro los cazadores persiguieran objetivos distintos simultáneamente, se requeriría una búsqueda compartida por cada objetivo único.

---

## Revisión de Decisiones de la Parte I que esta Carga pueda Invalidar

1. **Agenda de Eventos (`reloj.py` / `RelojEventos` sobre `HeapMinimo`)**:
   - *Decisión Parte I*: Intervalos fijos derivados de costo base 100.
   - *Impacto Parte II*: Con salidas de costo 1 y velocidad 200, el intervalo es 1 tick. Los cazadores pueden generar eventos en cada unidad temporal, multiplicando la densidad de eventos en la agenda por factor de hasta $10\times$.
   - *Revisión*: La estructura `HeapMinimo` con inserción y extracción $O(\log K)$ demostró ser robusta. Sin embargo, se confirma la necesidad de verificar con `--bench --solo agenda` y `--solo ciclo` que la tasa de despacho se mantenga dentro de los 20 ms.
2. **Historial de Retroceso (`historial_retroceso.py` / closures por `__setattr__`)**:
   - *Decisión Parte I*: Registro de cambios mediante closures de asignación en pilas LIFO para 5 intervalos.
   - *Impacto Parte II*: Con 30 cazadores moviéndose entre dos acciones del jugador, un solo intervalo acumula cientos de closures (sala, lista de enemigos, tiempos).
   - *Revisión*: Para los 5 intervalos del pergamino de retroceso, el consumo de memoria (~50 KB) y el tiempo de reversión (~1.3 ms) siguen siendo perfectamente aceptables. Sin embargo, este volumen masivo de closures **invalida terminantemente la viabilidad de usar closures para la capacidad 004 (Línea de Tiempo de 5 000 acciones)**, haciendo indispensable que la capacidad 004 implemente puntos de control con deltas planos en lugar de cierres dinámicos.

---

## Trazabilidad: Requisitos -> Componentes -> Mediciones

| Requisito Funcional | Componente de Software | Escenario de Prueba / Medición `--bench` |
|---|---|---|
| **FR-TER-001** (costo entero $\ge 1$, por defecto 100) | `cripta/dto/salida_dto.py` | `tests.dto.test_salida_dto` / Escenario Quickstart 1 |
| **FR-TER-002** (costo estrictamente simétrico) | `cripta/modelo/cripta_mapa.py` | `tests.aceptacion.test_terreno_costos` / Escenario Quickstart 2 |
| **FR-TER-003** (costo de movimiento = costo de salida) | `cripta/modelo/partida.py` (`_mover`) | `tests.aceptacion.test_terreno_costos` / Escenario Quickstart 2 |
| **FR-TER-004** (intervalo $\max(1, c \cdot 100 // v)$) | `cripta/modelo/reloj.py` | `tests.aceptacion.test_terreno_costos` / Escenario Quickstart 2 |
| **FR-TER-005** (escalado de tiempo ante cambio velocidad) | `cripta/modelo/reloj.py` (`reprogramar`) | `tests.aceptacion.test_terreno_costos` / Escenario Quickstart 2 |
| **FR-TER-006** (costos fijos para acciones sin movimiento) | `cripta/modelo/partida.py` | `tests.aceptacion.test_terreno_costos` / Escenario Quickstart 2 |
| **FR-TER-007** (errantes y rastreadores usan costo salida) | `cripta/modelo/partida.py` (`_turno_enemigo`) | `tests.modelo.test_comportamiento_enemigo` |
| **FR-TER-008** (ficha cazador requiere rango entero $\ge 1$) | `cripta/dto/enemigo_dto.py` | `tests.dto.test_enemigo_dto` / Escenario Quickstart 1 |
| **FR-TER-009** (cazador ataca si comparte sala, costo 100) | `cripta/modelo/comportamiento_enemigo.py` | `tests.aceptacion.test_cazador_persecucion` / Escenario Quickstart 3 |
| **FR-TER-010** (evaluación de costo mínimo hacia jugador) | `cripta/modelo/buscador_rutas.py` | `tests.modelo.test_buscador_rutas` |
| **FR-TER-011** (espera costo 100 si no hay ruta o $d > \text{rango}$) | `cripta/modelo/comportamiento_enemigo.py` | `tests.aceptacion.test_cazador_persecucion` / Escenario Quickstart 3 |
| **FR-TER-012** (movimiento por ruta mínima de costo $d$) | `cripta/modelo/comportamiento_enemigo.py` | `tests.aceptacion.test_cazador_persecucion` / Escenario Quickstart 3 |
| **FR-TER-013** (desempate obligatorio por menor ID de vecina) | `cripta/modelo/buscador_rutas.py` | `tests.aceptacion.test_cazador_persecucion` / Escenario Quickstart 3 |
| **FR-TER-014** (conoce esqueleto y puertas, sin niebla) | `cripta/modelo/buscador_rutas.py` | `tests.aceptacion.test_cazador_persecucion` / Escenario Quickstart 3 |
| **FR-TER-015** (equivalencia observable con recálculo cero) | `cripta/modelo/buscador_rutas.py` | `tests.aceptacion.test_cazador_persecucion` / Escenario Quickstart 3 |
| **FR-TER-016** (lectura de costo de esqueleto en servicio) | `cripta/infraestructura/serializacion.py` | `tests.infraestructura.test_cliente_offline_llaves` |
| **FR-TER-017** (lectura y validación de cazador en catálogo) | `cripta/infraestructura/serializacion.py` | `tests.dto.test_enemigo_dto` |
| **FR-TER-018** (consulta `/llaves`, presupuesto y portador) | `cripta/infraestructura/cliente_http.py` | `tests.infraestructura.test_cliente_offline_llaves` |
| **FR-TER-019** (invalidación formal por versión de cripta) | `cripta/infraestructura/cache.py` | `tests.infraestructura.test_cache_llaves` |
| **FR-TER-020** (ciclo de eventos $< 20\text{ ms}$ con cazadores) | `cripta/modelo/buscador_rutas.py` | `--bench --solo ruta_cazador ciclo` / Escenario 5 |
| **FR-TER-021** (bitácora `partida.log` solo acciones jugador) | `cripta/infraestructura/partida_log.py` | `tests.infraestructura.test_partida_log` |
| **FR-TER-022** (desempate de agenda por menor secuencia) | `cripta/modelo/reloj.py` (`RelojEventos`) | `tests.modelo.test_reloj` |
| **FR-TER-023** (desplazamientos rechazados sin tiempo ni log) | `cripta/modelo/partida.py` (`_despachar`) | `tests.controlador.test_controlador_errores` |

---

## Complexity Tracking

> Ninguna violación constitucional. Todas las estructuras evaluadas son implementadas a mano o reutilizadas de la Parte I sin recurrir a bibliotecas prohibidas.

| Posible Riesgo Detectado | Estrategia de Mitigación Elegida | Alternativa Rechazada y Justificación |
|---|---|---|
| Uso prohibido de `heapq` para Dijkstra | Reutilizar `HeapMinimo` propio de `cripta/estructuras/heap_min.py` | Rechazada cualquier biblioteca externa por Principio I de la Constitución. |
| Uso prohibido de `dict`/`set` para distancias y visitados | Arreglo contiguo `list[int \| None]` indexado por posición entera de `sala_id` | Rechazado `dict` por Principio I y `VectorOrdenado` por costo $O(V)$ de inserción. |
| Sobrecosto por decenas de cazadores persiguiendo | Dijkstra compartido inverso desde la sala del jugador acotado por $R_{\max}$ | Rechazado cálculo individual ($30\times$ más lento, viola límite de 20 ms). |
