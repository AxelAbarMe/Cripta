# Plan de Implementación: Verificación de Resolubilidad

**Rama**: `003-resolubilidad` | **Fecha**: 2026-11-11 | **Especificación**: [spec.md](spec.md)

**Entrada**: Especificación de funcionalidad desde `specs/003-resolubilidad/spec.md`, investigación técnica en [research.md](research.md), modelo de datos en [data-model.md](data-model.md), contratos en [contracts/contrato_resolubilidad.md](contracts/contrato_resolubilidad.md), y restricciones normativas de la Constitución (`.specify/memory/constitution.md`).

---

## Resumen

La capacidad de **Verificación de Resolubilidad** introduce un mecanismo formal de análisis estático previo al inicio de una partida para determinar deterministamente si una cripta puede completarse bajo las reglas del juego. Una cripta es resoluble si y solo si el jugador, partiendo de la `sala_inicial`, puede obtener la `llave_salida` y acceder a la `sala_salida` atravesando una puerta que requiera explícitamente dicha llave (FR-RES-001).

Para garantizar una ejecución estrictamente inferior a 200 ms sobre la cripta publicada más grande (SC-001) con un costo total aproximadamente lineal en salas, salidas y llaves ($O(V + E + K \log K)$, SC-002) y en pleno cumplimiento de las prohibiciones constitucionales (`heapq`, `bisect`, `collections`, `networkx`, `set`, `dict` como índice/tabla y `list.sort()`/`sorted()`), el diseño adopta:
1. **Recorrido Incremental Único**: Un algoritmo de avance integrado sobre el grafo mediante una `Cola` FIFO propia (`cripta/estructuras/cola.py`). La adquisición de una llave desbloquea y encola directamente las puertas que estaban esperando por ella sin retroceder ni reiniciar el recorrido desde la sala inicial (FR-RES-018).
2. **Pre-Indexación y Tablas Contiguas Directas sin `dict` ni `set`**: Un catálogo compacto de identificadores de llaves ordenado con ordenamiento propio (`catalogo_llaves: list[str]`), resolución `id_llave -> indice_entero` mediante búsqueda binaria manual en $O(\log K)$ (sin `bisect`), y arreglos planos contiguos `list` indexados por entero en $O(1)$ para posesión de llaves, puertas pendientes, llaves por sala y salas visitadas.
3. **Detección Determinista de Ciclos de Dependencia por DFS Tricolor**: Construcción en tiempo lineal de un grafo reducido de dependencias de llaves $G_{dep} = (K_{no}, E_{dep})$ mediante flood-fill desde la frontera bloqueada sobre las salas inalcanzables ($O(V_{unreach} + E_{unreach})$), seguido de una búsqueda en profundidad (DFS) con estados tricolores (blanco, gris, negro) y pila ancestral. Aísla de forma determinista exactamente un ciclo concreto representativo por cada grupo de llaves que se bloquean entre sí, normalizado al menor identificador léxico de llave (FR-RES-012).
4. **Desempate Determinista Estricto**: Resolución causal en rondas donde las llaves alcanzables simultáneas se activan priorizando el menor identificador léxico mediante `HeapMinimo` (`cripta/estructuras/heap_min.py`, Parte I) cargado con los índices enteros del catálogo ordenado, de modo que el menor índice es el menor identificador (FR-RES-008, SC-003). Las puertas de la frontera y los ciclos se ordenan deterministamente bajo el mismo criterio.
5. **Aislamiento Arquitectónico MVC**: Un modelo de dominio puro `VerificadorResolubilidad` (`cripta/modelo/resolubilidad.py`) desacoplado de la red y el disco, orquestado por `ServicioResolubilidad` (`cripta/servicios/servicio_resolubilidad.py`). La opción CLI `--verificar <cripta>` y la opción `--bench` se ejecutan sin instanciar la vista (SC-005, Principio III). Al iniciar una partida interactiva, el reporte se muestra a través de `VistaConsola`, impidiendo el inicio sin `--forzar` ante criptas no resolubles (FR-RES-014, FR-RES-015).
6. **Medición Comparativa en `--bench`**: Implementación de la carga `resolubilidad` que compara empíricamente el recorrido incremental contra la alternativa ingenua descartada de repetir el recorrido completo por llave sobre criptas sintéticas con cadenas largas de llaves encadenadas, reproducibles por semilla (FR-RES-020, SC-007).
7. **Reutilización de Contratos de la Capacidad 001**: Aprovechamiento directo de `obtener_llaves`, `LlaveUbicacionDTO`, la persistencia versionada en `CacheDisco`, `ClienteFalso` y `CriptaMapa` (validación de costos contradictorios con `CriptaDatosInvalidosError` y resolución bilateral de puertas y llaves).

---

## Contexto Técnico

**Lenguaje/Versión**: Python 3.11+ (finales de línea CRLF en Windows).

**Dependencias Principales**: Biblioteca estándar únicamente (`typing`, `dataclasses`, `sys`, `time`). Queda terminantemente PROHIBIDO el uso de `heapq`, `bisect`, `collections` (`deque`, `OrderedDict`, `defaultdict`, `Counter`), `networkx`, `set`, y `dict` como índice, caché o tabla de búsqueda en los módulos evaluados. Prohibido el uso de `list.sort()` y `sorted()`.

**Almacenamiento**: Persistencia local en `datos/cache/` mediante `CacheDisco` (`cripta/infraestructura/cache.py`), utilizando la clave versionada `cripta.<id>.<ver>.llaves.json` para desacoplar el consumo de red de reintentos futuros (FR-RES-017).

**Pruebas**: Módulo estándar `unittest` en `tests/`, ejecutado con `python -m unittest discover -s tests -t .`. Pruebas deterministas sin red apoyadas en `tests/cliente_falso.py` y fixtures sintéticos. Cada prueba de aceptación cita explícitamente el requisito `FR-RES-NNN` que cubre.

**Plataforma Objetivo**: Terminal de consola en Windows, Linux y macOS.

**Tipo de Proyecto**: Juego de mazmorra por turnos y simulador de eventos discretos en arquitectura MVC desacoplada con modo `--offline` y verificación por línea de comandos.

**Objetivos de Rendimiento**:
- Tiempo de verificación $< 200\text{ ms}$ en la cripta publicada más grande (hoy `cripta-06`, 300 salas) en el equipo local de referencia (SC-001).
- Costo total de tiempo aproximadamente lineal en función de $V$ (salas), $E$ (salidas) y $K$ (llaves): $O(V + E + K \log K)$ (SC-002).
- Sobrecosto marginal en memoria lineal $O(V + K)$ sobre listas contiguas indexadas por entero.

**Restricciones Constitucionales**:
- Estructuras implementadas a mano.
- Determinismo absoluto: misma cripta y configuración genera exactamente el mismo reporte carácter por carácter (Principio II).
- Separación MVC: el modelo no conoce red, disco ni interfaz; `--verificar` y `--bench` no instancian componentes de vista (Principio III).
- Ningún dato de cripta concreta fijado en el código (Principio IV).
- Respeto del presupuesto de solicitudes de red: la consulta `/llaves` descuenta una solicitud y maneja reintentos 429; el agotamiento de presupuesto aborta la ejecución sin emitir reportes parciales (Principio V, FR-RES-023, SC-008).
- Afirmaciones de rendimiento respaldadas con `--bench` (Principio VI).
- Especificación antes que código (Principio VII).
- Compatibilidad retroactiva: las 222 pruebas previas deben continuar ejecutándose en `OK` (Principio VIII).

---

## Verificación Constitucional

*Control de Paso: Aprobación previa antes de implementar código.*

| Principio Constitucional | Estado | Evidencia y Justificación en este Plan |
|---|---|---|
| **I. Estructuras a mano** | **PASÓ** | No se utiliza `heapq`, `bisect`, `collections`, `networkx`, `set` ni `dict` en el verificador de dominio. Se reutiliza la estructura propia `Cola` (`cripta/estructuras/cola.py`), búsqueda binaria manual en 10 líneas para mapear texto a entero, ordenamiento selector propio (`ordenar_auto` / merge sort), y arreglos contiguos `list` indexados por entero. |
| **II. Determinismo** | **PASÓ** | Desempate por menor identificador léxico en orden de llaves obtenibles (FR-RES-008), tupla de orden ascendente en puertas de frontera (`sala_origen`, `direccion`, `llave`), y normalización de ciclos iniciados en la llave menor y ordenados entre grupos (SC-003). |
| **III. MVC y adaptadores** | **PASÓ** | `VerificadorResolubilidad` es un módulo puro en `cripta/modelo/resolubilidad.py` sin llamadas HTTP, sin lectura de disco y sin vista. `--verificar` imprime directamente a `sys.stdout` sin instanciar `VistaConsola` (SC-005). La vista interactiva solo se instancia en el controlador de juego. |
| **IV. Sin datos de cripta concreta** | **PASÓ** | Ningún número de sala, nombre de llave ni conexión está fijo en el código. Toda la información se lee dinámicamente del esqueleto y del endpoint `/llaves` o fixtures offline. |
| **V. Presupuesto de red** | **PASÓ** | La consulta `GET /v1/criptas/{dungeon_id}/llaves` descuenta una solicitud de `ContadorSolicitudes`, soporta reintentos por 429 y se persiste en `CacheDisco`. Si el presupuesto se agota, aborta informando el error sin reporte parcial (FR-RES-023, SC-008). |
| **VI. Rendimiento con --bench** | **PASÓ** | Se planifica e implementa la carga sintética `resolubilidad` en `cripta/bench/cargas_bench.py`, contrastando el recorrido incremental frente a la alternativa ingenua reiniciada sobre criptas sintéticas con cadenas de llaves dependientes de `SEMILLA_BENCH` (FR-RES-020, SC-007). Cota $< 200\text{ ms}$ a medir sobre la cripta publicada más grande (SC-001). |
| **VII. Especificación antes que código** | **PASÓ** | La especificación formal `spec.md` fue aprobada previamente sin mención de clases ni estructuras. Todas las tareas de diseño y código trazan a requisitos `FR-RES-NNN`. |
| **VIII. Compatibilidad con Parte I** | **PASÓ** | Las 222 pruebas preexistentes permanecen intactas. `CriptaMapa` reutiliza la validación de costos contradictorios y la unificación bilateral de puertas cerradas. |

---

## Estructura del Proyecto

### Documentación (esta funcionalidad)

```text
specs/003-resolubilidad/
├── spec.md              # Requisitos funcionales y escenarios de aceptación
├── plan.md              # Este documento técnico de implementación
├── research.md          # Investigación técnica y análisis de alternativas (Fase 0)
├── data-model.md        # Entidades, campos, invariantes y diagramas de estado (Fase 1)
├── quickstart.md        # Guía paso a paso de validación y escenarios ejecutables (Fase 1)
├── contracts/           # Contratos formales de interfaces y esquemas (Fase 1)
│   ├── contrato_resolubilidad.md
│   └── esquema_reporte_resolubilidad.json
└── checklists/          # Listas de control de calidad
```

### Código Fuente (raíz del repositorio)

```text
cripta/
├── dto/
│   ├── salida_dto.py                    # Sin cambios (ya posee costo de 001)
│   ├── enemigo_dto.py                   # Sin cambios (ya posee rango de 001)
│   └── llave_ubicacion_dto.py           # Sin cambios (reutilizado de 001)
├── infraestructura/
│   ├── puertos.py                       # Sin cambios (ClienteCripta ya posee obtener_llaves)
│   ├── cliente_http.py                  # Sin cambios (implementa obtener_llaves con presupuesto)
│   ├── cliente_offline.py               # Sin cambios (implementa obtener_llaves desde fixtures)
│   ├── cliente_general.py               # Sin cambios (delegación sincronizada)
│   ├── cache.py                         # Sin cambios (persistencia de llaves versionada)
│   └── serializacion.py                 # Sin cambios (serialización de llaves en JSON)
├── modelo/
│   ├── cripta_mapa.py                   # Sin cambios (reutiliza _validar_costos y sincronizar_puertas)
│   └── resolubilidad.py                 # NUEVO: VerificadorResolubilidad, ResultadoResolubilidad,
│                                        #        FronteraBloqueadaPuerta, CicloDependenciaLlaves,
│                                        #        UbicacionLlaveDiagnostico (modelo puro)
├── servicios/
│   ├── servicio_resolubilidad.py        # NUEVO: ServicioResolubilidad (orquestador de red/disco)
│   ├── servicio_partida.py              # MODIFICADO: invoca verificación al iniciar partida
│   └── servicio_bench.py                # Sin cambios (ejecuta CARGAS dinámicamente)
├── controlador/
│   └── controlador_cripta.py            # MODIFICADO: soporte de bandera --forzar y presentación
├── vista/
│   ├── vista_base.py                    # MODIFICADO: contrato mostrar_reporte_resolubilidad()
│   └── vista_consola.py                 # MODIFICADO: implementación de formateo de reporte
├── bench/
│   └── cargas_bench.py                  # MODIFICADO: agrega carga "resolubilidad" y generador
├── __main__.py                          # MODIFICADO: soporte CLI para --verificar y --forzar
tests/
├── cliente_falso.py                     # Sin cambios (reutilizado de 001)
├── modelo/
│   └── test_resolubilidad.py            # NUEVO: pruebas unitarias de dominio puro (FR-RES-001 a 012, 018)
├── servicios/
│   └── test_servicio_resolubilidad.py   # NUEVO: pruebas de servicio, presupuesto y caché (FR-RES-017, 021, 023)
└── controlador/
    └── test_controlador_resolubilidad.py# NUEVO: pruebas de flujo interactivo y --forzar (FR-RES-013 a 015)
```

---

## 1. Problema y Operaciones Reales con su Frecuencia Esperada

### 1.1 Exploración Causal de Alcanzabilidad y Activación de Llaves
- **Problema**: Evaluar si desde `sala_inicial` se puede obtener `llave_salida` y llegar a `sala_salida` por una puerta que la exija (FR-RES-001), asumiendo que las llaves no se consumen (FR-RES-003), todo enemigo es derrotable (FR-RES-004), llaves de enemigos están en su sala inicial (FR-RES-005), y trampas/cierres automáticos no impiden el paso (FR-RES-006).
- **Operaciones Reales**:
  - Encolar salas alcanzables descubiertas: $O(V)$ encolados en total.
  - Examinar salidas adyacentes de salas transitables: $O(E)$ revisiones (con $E \le 4V$).
  - Activar una llave al ser descubierta y drenar sus puertas pendientes: $O(K)$ activaciones, $O(E_p)$ puertas liberadas.
- **Frecuencia**: 1 vez por verificación CLI (`--verificar`) o al seleccionar una cripta al arrancar el juego.

### 1.2 Mapeo y Consulta de Identificadores de Llaves sin Estructuras Prohibidas
- **Problema**: Asociar puertas cerradas con su llave requerida (`id_llave: str`) y consultar si una llave está obtenida o qué puertas esperan por ella, sin usar `dict`, `set`, ni `bisect`.
- **Operaciones Reales**:
  - Ordenar y deduplicar el catálogo de llaves únicas al inicio: $O(K \log K)$ comparaciones.
  - Búsqueda binaria manual de `id_llave -> indice_entero`: $O(\log K)$ operaciones elementales (frecuencia: $O(E)$ al encontrar puertas y $O(K)$ al clasificar ubicaciones).
  - Consulta y actualización de posesión `llave_obtenida[indice]`: $O(1)$ por acceso (frecuencia: $O(E)$).
  - Consulta de llaves en una sala `llaves_en_sala[sala_id]`: $O(1)$ por acceso directo (frecuencia: $O(V)$).

### 1.3 Detección Determinista de Ciclos de Dependencia
- **Problema**: Ante una cripta no resoluble, identificar qué llaves inalcanzables se bloquean mutuamente tras puertas cerradas y extraer deterministamente exactamente un ciclo representativo por grupo de llaves interdependientes (FR-RES-012).
- **Operaciones Reales**:
  - Flood-fill desde las puertas de la frontera bloqueada sobre el subgrafo inalcanzable $V \setminus R$: $O(V_{unreach} + E_{unreach})$ visitas.
  - DFS tricolor sobre el grafo de llaves inalcanzables $G_{dep}$: $O(K_{no} + E_{dep})$ pasos.
  - Extracción y rotación cíclica de la cadena representativa: $O(L_{ciclo})$ donde $L_{ciclo} \le K_{no}$.
- **Frecuencia**: 1 vez al final del análisis exclusivamente si la cripta resulta NO resoluble.

### 1.4 Desempate Determinista en Ordenamiento
- **Problema**: Desempatar llaves obtenibles disponibles simultáneamente, ordenar puertas de la frontera bloqueada y ordenar ciclos de dependencia por menor identificador (FR-RES-008, SC-003).
- **Operaciones Reales**:
  - Inserción y extracción de llaves candidatas en `HeapMinimo`: $O(\log K)$ por llave.
  - Ordenamiento de puertas de la frontera bloqueada: $O(E_{frontera} \log E_{frontera})$.
  - Ordenamiento de ciclos representativos: $O(C \log C)$ con $C \le K$.
- **Frecuencia**: 1 vez durante o al cierre del análisis.

### 1.5 Control de Acceso CLI e Integración MVC
- **Problema**: Ejecutar la verificación sin instanciar la vista interactiva (`--verificar`, SC-005) o integrar la compuerta de inicio interactiva con `--forzar` (FR-RES-013 a 015).
- **Operaciones Reales**: Comprobación de banderas CLI en `__main__.py` y despacho condicional en `ControladorCripta._iniciar_partida()`. Frecuencia: 1 vez al arrancar el ejecutable.

---

## 2. Alternativas por Problema y Razón Concreta de Descarte

### Problema A: Exploración de Alcanzabilidad de Salas y Llaves
1. **Alternativa A.1 (Descartada - Medida en `--bench`)**: *Recorrido Ingenuo Reiniciado por Cada Llave*. Realiza un BFS completo desde la sala inicial; cada vez que descubre una llave nueva, la registra y reinicia el BFS desde cero.
   - *Razón concreta de descarte*: Complejidad temporal $O(K \cdot (V + E))$. Para cadenas largas de llaves ($K = 50$, $V = 1\,000$), realiza $\approx 25\,000$ visitas redundantes a salas ya exploradas. Se implementa como método `verificar_ingenuo_reiniciado` para evidenciar su degradación empírica en `--bench` (FR-RES-020).
2. **Alternativa A.2 (Descartada)**: *Algoritmo de Rutas Mínimas (Dijkstra / Bellman-Ford)*.
   - *Razón concreta de descarte*: La resolubilidad es una propiedad de conectividad topológica y no de optimización de costos de terreno. Utilizar un montículo de prioridad añade un sobrecosto innecesario de $O((V + E) \log V)$ por extracción y complica artificialmente la reactivación de puertas bloqueadas.

### Problema B: Mapeo y Asociación de Llaves sin `dict`, `set`, ni `bisect`
1. **Alternativa B.1 (Descartada)**: *Búsqueda Lineal Exhaustiva sobre Listas de Cadenas*. Comparar cadenas de texto elemento por elemento cada vez que se procesa una puerta o se adquiere una llave.
   - *Razón concreta de descarte*: Complejidad $O(E \cdot K)$ en comparaciones de cadenas. En criptas densas con cientos de puertas, degrada significativamente el tiempo de verificación, alejándose del objetivo de costo lineal.
2. **Alternativa B.2 (Descartada)**: *Tabla Hash con Sondeo Abierto Implementada a Mano*.
   - *Razón concreta de descarte*: Requiere diseñar funciones hash manuales sobre cadenas, gestionar colisiones, redimensionamiento y factores de carga dinámicos. Esto introduce alta complejidad accidental para un conjunto estático y acotado de llaves ($K \le 100$) cuyos identificadores se conocen previamente al iniciar el análisis.

### Problema C: Detección de Ciclos de Dependencia entre Llaves
1. **Alternativa C.1 (Descartada)**: *Algoritmo de Johnson o Tarjan para Enumeración Exhaustiva de Ciclos*.
   - *Razón concreta de descarte*: En grafos dirigidos densos, la cantidad de ciclos simples puede crecer exponencialmente ($O((V+E)(C+1))$). Viola la restricción de costo lineal y contradice el requisito FR-RES-012, que pide expresamente reportar solo *un ciclo representativo por grupo* de llaves interdependientes.
2. **Alternativa C.2 (Descartada)**: *Búsqueda DFS Plana con Arreglo Booleano Simple de Visitados*.
   - *Razón concreta de descarte*: No distingue aristas hacia atrás (ciclos reales) de aristas cruzadas (convergencia a ramas ya procesadas), generando falsos positivos de dependencias circulares y órdenes no reproducibles.

### Problema D: Desempate Determinista
1. **Alternativa D.1 (Descartada)**: *Orden Topológico de Descubrimiento FIFO Dependiente del API*.
   - *Razón concreta de descarte*: Depende del orden de entrega de páginas del API y del orden local de salidas (N, S, E, O). Rompe el determinismo exigido por FR-RES-008 y falla los escenarios de aceptación del Apéndice B.
2. **Alternativa D.2 (Descartada)**: *Uso de `list.sort()` o `sorted()` de Python*.
   - *Razón concreta de descarte*: PROHIBIDO expresamente por el Principio I de la Constitución en los problemas evaluados.

### Problema E: Arquitectura y Desacoplamiento de Vista
1. **Alternativa E.1 (Descartada)**: *Incrustar la Verificación en `Partida.__init__`*.
   - *Razón concreta de descarte*: Sobrecarga la clase `Partida` (674 líneas) y fuerza a instanciar la simulación interactiva completa aun para la bandera `--verificar`, violando el Principio III de la Constitución.
2. **Alternativa E.2 (Descartada)**: *Consultas de Red Directas desde el Verificador de Dominio*.
   - *Razón concreta de descarte*: Acopla el modelo con HTTP y el sistema de archivos, impidiendo la ejecución de pruebas unitarias aisladas con `ClienteFalso` y violando la arquitectura en capas.

---

## 3. Decisión (Estructura y Estrategia) y Complejidad

### 3.1 Decisiones Adoptadas
1. **Recorrido Incremental Único**:
   - Estructura: `Cola` FIFO propia (`cripta/estructuras/cola.py`).
   - Estrategia: Las salas transitables descubiertas se encolan. Al encontrar una puerta cerrada con llave no obtenida, la puerta se añade a `puertas_pendientes_por_llave[indice_llave]`. Cuando la cola se vacía, si existen llaves alcanzables disponibles, se selecciona la de menor identificador léxico, se marca como obtenida y se activan sus puertas pendientes encolando las salas destino, reanudando el recorrido sin reexplorar lo ya visitado.
2. **Pre-Indexación Compacta y Tablas Contiguas**:
   - `catalogo_llaves: list[str]`: Arreglo ordenado alfabéticamente con merge sort propio y deduplicado en $O(K \log K)$ sin `set`.
   - Búsqueda binaria manual: Función iterativa propia de 10 líneas que devuelve el índice entero $i \in [0, K-1]$ en $O(\log K)$ sin usar `bisect`.
   - Tablas contiguas `list` indexadas por entero: `llave_obtenida` ($O(1)$), `puertas_pendientes` ($O(1)$), `llaves_en_sala` ($O(1)$), y `visitada` ($O(1)$).
3. **Grafo Reducido de Dependencias y DFS Tricolor**:
   - Si no es resoluble, un único pase $O(V + E)$ etiqueta las salas inalcanzables en bloques conectados por salidas abiertas (arreglo `bloque_de_sala`), sin visitar ninguna sala más de una vez. Cada puerta cerrada que entra a un bloque aporta una arista bloque -> llave exigida, y cada llave no obtenida aporta una arista llave -> bloque donde está. $G_{dep}$ tiene a lo sumo $K + E$ aristas y el DFS tricolor corre sobre él en tiempo lineal. El ciclo se informa solo con llaves.
   - Se ejecuta DFS con estados tricolores (0=blanco, 1=gris, 2=negro) iterando sobre las llaves en orden alfabético ascendente. Una arista hacia un nodo gris extrae el ciclo desde la pila ancestral.
   - Normalización: El ciclo se rota para iniciar en su llave léxicamente menor y se marcan las llaves del componente como agrupadas para emitir exactamente un ciclo representativo por grupo.
4. **Desempate Determinista por Menor Identificador**:
   - Las llaves alcanzables disponibles entran una sola vez a un `HeapMinimo` (`cripta/estructuras/heap_min.py`, Parte I) como índices enteros del catálogo ordenado. Al vaciarse la cola de salas se extrae el mínimo, que es la llave de menor identificador, en $O(\log K)$. Se descartó reordenar la lista de candidatas en cada ronda: costaría hasta $O(K^2 \log K)$.
   - Las puertas de la frontera bloqueada y los ciclos se ordenan mediante ordenamiento propio aplicando comparadores en tuplas.
5. **Servicio y CLI Desacoplados**:
   - `VerificadorResolubilidad` (modelo puro en `cripta/modelo/resolubilidad.py`) devuelve `ResultadoResolubilidad`.
   - `ServicioResolubilidad` (`cripta/servicios/servicio_resolubilidad.py`) gestiona `ClienteCripta`, `CacheDisco` y `ContadorSolicitudes`.
   - `__main__.py` despacha `--verificar` imprimiendo el reporte por `sys.stdout` sin vista.
   - `ControladorCripta` gestiona `--forzar` e interactúa con `VistaConsola.mostrar_reporte_resolubilidad()`.
6. **Condición de victoria (FR-RES-001)**:
   - Se mantiene la bandera `entro_por_llave_salida`. Se activa cuando una sala alcanzada tiene una puerta cerrada que exige `llave_salida`, esa llave ya está obtenida y el destino de la puerta es `sala_salida`. Se evalúa al examinar la puerta (si la llave ya se posee) y al drenar `puertas_pendientes` (si la llave llega después).
   - La cripta es resoluble si `llave_salida` fue obtenida y la bandera está activa. Entrar a `sala_salida` por una puerta abierta o por una puerta de otra llave no activa la bandera.

### 3.2 Complejidad de las Operaciones Más Frecuentes

| Operación | Frecuencia en una Verificación | Estructura de Datos | Complejidad Temporal | Complejidad Espacial |
|---|---|---|---|---|
| Construcción de catálogo y deduplicación | 1 vez al inicio | `list[str]` con merge sort propio | $O(K \log K)$ | $O(K)$ |
| Búsqueda de índice de llave (`id_llave -> int`) | $O(E + K)$ consultas | Búsqueda binaria manual | $O(\log K)$ | $O(1)$ |
| Consulta y actualización de sala visitada | $O(V)$ consultas | Arreglo plano `list[bool]` | $O(1)$ | $O(V)$ |
| Consulta y actualización de llave obtenida | $O(E + K)$ consultas | Arreglo plano `list[bool]` | $O(1)$ | $O(K)$ |
| Encolar / desencolar salas transitables | $O(V)$ operaciones | `Cola` enlazada propia | $O(1)$ | $O(V)$ |
| Registro y liberación de puertas pendientes | $O(E_p)$ puertas | `list[list[tuple]]` contiguo | $O(1)$ inserción / drenado | $O(E_p)$ |
| Flood-fill sobre salas inalcanzables | 1 vez (solo si no es resoluble) | `Cola` / arreglo `visitada_unreach` | $O(V_{unreach} + E_{unreach})$ | $O(V)$ |
| Detección de ciclos por DFS tricolor | 1 vez (solo si no es resoluble) | `list[int]` tricolor + pila contigua | $O(K_{no} + E_{dep})$ | $O(K)$ |
| **Costo Total del Recorrido Incremental** | **1 vez por verificación** | **Estructuras integradas** | **$O(V + E + K \log K)$** | **$O(V + E + K \log K)$** |

> Como $K \le 100$ en criptas reales, $K \log_2 K \le 700$ operaciones elementales, por lo que el costo total es efectivamente lineal en $V$ y $E$, cumpliendo holgadamente el criterio SC-002 y la cota de 200 ms (SC-001).

---

## 4. Impacto en Código Existente: Archivo por Archivo

| Archivo (Ruta Real) | Estado | Descripción del Cambio o Justificación |
|---|---|---|
| `cripta/dto/salida_dto.py` | **Sin cambios** | Mantiene `SalidaDTO` con campo opcional `costo` (consolidado en 001). |
| `cripta/dto/enemigo_dto.py` | **Sin cambios** | Mantiene `EnemigoDTO` con campo opcional `rango` (consolidado en 001). |
| `cripta/dto/llave_ubicacion_dto.py` | **Sin cambios** | Reutiliza `LlaveUbicacionDTO` inmutable (consolidado en 001). |
| `cripta/infraestructura/puertos.py` | **Sin cambios** | Protocolo `ClienteCripta` ya incluye `obtener_llaves(id_cripta)` (consolidado en 001). |
| `cripta/infraestructura/cliente_http.py` | **Sin cambios** | Ya implementa `obtener_llaves` con presupuesto y manejo de 429 (consolidado en 001). |
| `cripta/infraestructura/cliente_offline.py` | **Sin cambios** | Ya implementa `obtener_llaves` leyendo `fixtures/` (consolidado en 001). |
| `cripta/infraestructura/cliente_general.py` | **Sin cambios** | Ya delega `obtener_llaves` de forma sincronizada (consolidado en 001). |
| `cripta/infraestructura/cache.py` | **Sin cambios** | Ya implementa `leer_llaves` y `guardar_llaves` con clave versionada `cripta.<id>.<ver>.llaves.json` (consolidado en 001). |
| `cripta/modelo/cripta_mapa.py` | **Sin cambios** | Ya valida costos contradictorios con `_validar_costos()` lanzando `CriptaDatosInvalidosError`, sincroniza puertas con `sincronizar_puertas()` y resuelve datos de puertas bilateralmente con `datos_de_puerta()` (consolidado en 001). |
| `cripta/modelo/resolubilidad.py` | **NUEVO** | Implementa las entidades `ResultadoResolubilidad`, `FronteraBloqueadaPuerta`, `CicloDependenciaLlaves`, `UbicacionLlaveDiagnostico` y la clase pura `VerificadorResolubilidad` (métodos `verificar` y `verificar_ingenuo_reiniciado`). |
| `cripta/servicios/servicio_resolubilidad.py` | **NUEVO** | Implementa `ServicioResolubilidad` que orquesta `ClienteCripta`, `CacheDisco`, `ContadorSolicitudes`, construye `CriptaMapa` e invoca el verificador. |
| `cripta/servicios/servicio_partida.py` | **MODIFICADO** | En `_armar` o previo a instanciar `Partida`, integra la verificación de resolubilidad y expone el resultado para el controlador. |
| `cripta/controlador/controlador_cripta.py` | **MODIFICADO** | Acepta parámetro `forzar: bool = False`. En `_iniciar_partida`, solicita y muestra el reporte mediante la vista; si no es resoluble y `forzar == False`, aborta el inicio sin entrar al bucle interactivo. |
| `cripta/vista/vista_base.py` | **MODIFICADO** | Agrega método abstracto `mostrar_reporte_resolubilidad(resultado: ResultadoResolubilidad, forzada: bool = False)`. |
| `cripta/vista/vista_consola.py` | **MODIFICADO** | Implementa `mostrar_reporte_resolubilidad` imprimiendo el diagnóstico estructurado en formato de 113 columnas. |
| `cripta/__main__.py` | **MODIFICADO** | Agrega banderas `--verificar` (recibe ID de cripta) y `--forzar`. Si `--verificar` está presente, ejecuta `ServicioResolubilidad.verificar()`, imprime el reporte a `sys.stdout` y retorna 0 sin instanciar la vista ni el controlador. Pasa `forzar` a `ControladorCripta`. |
| `cripta/bench/cargas_bench.py` | **MODIFICADO** | Agrega generador sintético determinista de criptas con llaves encadenadas y la función `bench_resolubilidad` registrada en `CARGAS` bajo `"resolubilidad"`. |
| `cripta/servicios/servicio_bench.py` | **Sin cambios** | Despacha dinámicamente las cargas registradas en `CARGAS`, por lo que detecta `"resolubilidad"` automáticamente. |
| `tests/cliente_falso.py` | **Sin cambios** | Ya incluye `obtener_llaves` y retorno de `LlaveUbicacionDTO` (consolidado en 001). |
| `tests/cripta_artificial.py` | **Sin cambios** | Mantiene generador en cuadrícula de la Parte I. |
| `tests/modelo/test_resolubilidad.py` | **NUEVO** | Pruebas unitarias de dominio puro (FR-RES-001 a FR-RES-012, FR-RES-018, Apéndice B). |
| `tests/servicios/test_servicio_resolubilidad.py` | **NUEVO** | Pruebas de servicio, presupuesto, caché versionada y errores (FR-RES-017, FR-RES-021, FR-RES-023). |
| `tests/controlador/test_controlador_resolubilidad.py` | **NUEVO** | Pruebas de integración del controlador, compuerta `--forzar` y reportes interactivos (FR-RES-013 a FR-RES-015). |

---

## 5. Mediciones `--bench` Previstas (Incluida la Alternativa Descartada)

### 5.1 Carga Sintética `resolubilidad`: Recorrido Incremental vs Recorrido Ingenuo Reiniciado
- **Objetivo**: Demostrar empíricamente que el recorrido incremental único ($O(V + E + K \log K)$) supera ampliamente a la alternativa ingenua descartada de repetir el recorrido completo por cada llave descubierta ($O(K \cdot (V + E))$) sobre criptas sintéticas con muchas llaves encadenadas (FR-RES-020, SC-007).
- **Diseño de la Carga Sintética**:
  - Función generadora determinista regida por `SEMILLA_BENCH = 20260928`.
  - Construye una cripta de $K = 40$ llaves encadenadas en serie a través de $V = 800$ salas ($20$ salas por segmento).
  - Cada segmento $i$ contiene una puerta cerrada que requiere la llave $k_i$, y la llave $k_i$ reside en una sala lateral accesible únicamente desde el segmento $i$.
  - La última sala contiene la puerta final que exige `llave_salida`.
- **Medición**:
  - Se mide el tiempo de `VerificadorResolubilidad.verificar()` frente a `VerificadorResolubilidad.verificar_ingenuo_reiniciado()` ejecutando 3 repeticiones con `_medir`.
  - Se reporta la razón de aceleración con `_comparar`.
- **Comando Exacto para Reproducir**:
  ```powershell
  python -m cripta --bench --solo resolubilidad
  ```
- **Formato de salida (los valores se obtienen al medir)**:   [2 coincidencias]
  ```text
  === RESOLUBILIDAD  (X.XX s) ===
    40 llaves encadenadas, 800 salas: recorrido incremental: X.XXX ms
        -> recorrido_ingenuo_reiniciado es N.Nx más lento que recorrido_incremental
  ```

### 5.2 Medición de la Cota de 200 ms en la Cripta Publicada más Grande
- **Objetivo**: Verificar que la verificación sobre la cripta publicada más grande (hoy `cripta-06`, 300 salas; la carga la elige por el mayor total de salas del listado, sin fijar su id en el código, Principio IV) se ejecute en un tiempo estrictamente inferior a 200 ms (SC-001).
- **Comando Exacto para Reproducir**:
  ```powershell
  python -m cripta --bench --solo resolubilidad_cota
  ```
- **Formato de salida (los valores se obtienen al medir)**:   [2 coincidencias]
  ```text
  === RESOLUBILIDAD_COTA  (X.XX s) ===
    verificación cripta-06 (300 salas): X.XXX ms  (límite 200.0 ms: CUMPLE)
  ```

---

## 6. Límites Conocidos de la Decisión

1. **Escalamiento con Identificadores de Sala Dispersos**:
   - El arreglo `visitada = [False] * (max_sala_id + 1)` y `llaves_en_sala` asumen que `max_sala_id` es proporcional al número de salas $V$. Si una cripta maliciosa o patológica utilizara identificadores astronómicos (p. ej. `sala_id = 10_000_000` con solo 10 salas), la asignación de memoria crecería innecesariamente. Dado que el catálogo del API numera las salas de forma correlativa desde 1 hasta $V$, esta decisión es óptima en tiempo y espacio para las escalas de diseño del curso ($V \le 1\,000$).
2. **Escala del Catálogo de Llaves**:
   - La búsqueda binaria manual en `catalogo_llaves` es $O(\log K)$. Para los valores normales de una mazmorra ($K \le 50$), $\log_2 K \le 6$, es decir, a lo sumo 6 comparaciones por búsqueda. Si una cripta presentara más de $100\,000$ llaves únicas, el pre-ordenamiento inicial $O(K \log K)$ tendría un costo que solo `--bench` puede confirmar.
3. **Representatividad de Ciclos**:
   - Por mandato expreso de FR-RES-012 y la Aclaración 2026-11-11, el algoritmo reporta exactamente *un ciclo concreto representativo por cada grupo de llaves interdependientes* y no todos los ciclos combinatorios posibles. En un laberinto donde un grupo de 4 llaves admita 6 ciclos elementales entrelazados, el reporte presentará uno solo de ellos (el que comience con la llave léxicamente menor del grupo), lo cual satisface la especificación pero no enumera exhaustivamente las dependencias redundantes.

---

## 7. Revisión de Decisiones de la Parte I que esta Carga Pueda Invalidar

1. **Uso de `VectorOrdenado` para Búsqueda de Salas (`CriptaMapa._salas`)**:
   - En la Parte I, `CriptaMapa` almacena las salas en un `VectorOrdenado` donde `obtener(sala_id)` realiza búsqueda binaria en $O(\log V)$.
   - *Evaluación bajo la carga nueva*: Durante la verificación de resolubilidad, se examinan las salidas de las salas transitables $O(E)$ veces. Para $V = 1\,000$ salas y $E \le 4\,000$ salidas, realizar consultas a través de `CriptaMapa` implicaría $4\,000 \times \log_2(1\,000) \approx 40\,000$ comparaciones, un costo que se confirmará con la medición de la cota (`resolubilidad_cota`).
   - *Decisión*: Se mantiene `CriptaMapa` intacto. No obstante, para el estado de exploración de resolubilidad (salas visitadas y llaves en sala), **NO se utiliza `VectorOrdenado`**, sino listas contiguas indexadas por entero en $O(1)$, evitando duplicar búsquedas binarias.
2. **Presupuesto de Solicitudes y Endpoint `/llaves`**:
   - En la Parte I, cada cripta trae su propio `presupuesto_solicitudes` (en su `general.json`), que cuenta los datos generales, las páginas del esqueleto y el contenido de las salas.
   - *Impacto*: Agregar una solicitud remota obligatoria a `/llaves` consume 1 unidad del presupuesto. Si se ejecutara en red viva sin caché, podría agotar el presupuesto en partidas que apuren el límite.
   - *Mitigación y confirmación*: La persistencia en `CacheDisco` (`cripta.<id>.<ver>.llaves.json`) garantiza que en ejecuciones sucesivas, en modo `--offline` y durante `--bench`, la consulta de llaves se resuelva en disco con costo 0 contra el presupuesto, respetando el Principio V.

---

## 8. Trazabilidad: Requisitos `FR-RES` ↔ Componentes ↔ Pruebas / Mediciones

| Requisito Funcional | Componente de Implementación | Escenario de Aceptación / Caso de Prueba | Medición `--bench` |
|---|---|---|---|
| **FR-RES-001**: Evaluación de resolubilidad partiendo de sala inicial hacia sala de salida con llave | `VerificadorResolubilidad.verificar` | `test_resolubilidad_completitud_basica` | `bench_resolubilidad` |
| **FR-RES-002**: Tránsito por salidas abiertas y cerradas con llave obtenida | `VerificadorResolubilidad._examinar_salidas` | `test_puertas_abiertas_y_cerradas_con_llave` | N/A |
| **FR-RES-003**: Llaves no consumibles al abrir puertas | `VerificadorResolubilidad` | `test_llaves_reutilizables_multiples_puertas` | N/A |
| **FR-RES-004**: Todo enemigo asumido derrotable | `VerificadorResolubilidad` | `test_llaves_enemigos_derrotables` | N/A |
| **FR-RES-005**: Llaves de enemigos obtenibles en sala inicial del enemigo | `VerificadorResolubilidad` | `test_llave_enemigo_errante_sala_inicial` (Apéndice B) | N/A |
| **FR-RES-006**: Trampas y cierres automáticos no impiden el paso | `VerificadorResolubilidad` | `test_trampas_y_cierres_no_bloquean` | N/A |
| **FR-RES-007**: Secuencia causal ordenada de todas las llaves obtenibles | `VerificadorResolubilidad.verificar` | `test_secuencia_causal_todas_las_llaves` | N/A |
| **FR-RES-008**: Determinismo estricto y desempate por menor identificador | `VerificadorResolubilidad._ordenar_candidatos` | `test_determinismo_desempate_menor_id` (SC-003, Apéndice B) | N/A |
| **FR-RES-009**: Identificación de llaves no obtenibles | `ResultadoResolubilidad.llaves_no_obtenibles` | `test_deteccion_llaves_no_obtenibles` (SC-004) | N/A |
| **FR-RES-010**: Identificación y detalle de frontera bloqueada | `ResultadoResolubilidad.frontera_bloqueada` | `test_frontera_bloqueada_puertas` (SC-004) | N/A |
| **FR-RES-011**: Ubicación conocida de llaves no obtenibles y de frontera | `ResultadoResolubilidad.ubicaciones_llaves` | `test_ubicaciones_llaves_no_obtenibles` | N/A |
| **FR-RES-012**: Detección de ciclos concretos por grupo con costo lineal | `VerificadorResolubilidad._detectar_ciclos_dfs` | `test_ciclo_llave_salida_tras_su_puerta` (Apéndice B) | N/A |
| **FR-RES-013**: Verificación automática al iniciar partida regular | `ControladorCripta._iniciar_partida` | `test_inicio_partida_ejecuta_verificacion` | N/A |
| **FR-RES-014**: Cancelación de inicio sin `--forzar` en no resoluble | `ControladorCripta._iniciar_partida` | `test_no_resoluble_sin_forzar_aborta` (Apéndice B) | N/A |
| **FR-RES-015**: Inicio permitido con `--forzar` mostrando advertencia | `ControladorCripta._iniciar_partida` | `test_no_resoluble_con_forzar_inicia` | N/A |
| **FR-RES-016**: Comando CLI `--verificar` sin vista | `cripta/__main__.py:main` | `test_cli_verificar_sin_vista` (SC-005) | N/A |
| **FR-RES-017**: Consulta de llaves bajo contrato 001 con presupuesto y caché | `ServicioResolubilidad.verificar` | `test_servicio_llaves_presupuesto_y_cache` (SC-006) | N/A |
| **FR-RES-018**: Recorrido incremental único sin recorridos extra | `VerificadorResolubilidad.verificar` | `test_recorrido_incremental_un_solo_paso` | `bench_resolubilidad` |
| **FR-RES-019**: Puertas cerradas en un lado resueltas bilateralmente | `CriptaMapa.sincronizar_puertas` | `test_puerta_unilateral_sincronizada` | N/A |
| **FR-RES-020**: Comparación en `--bench` contra alternativa ingenua | `bench/cargas_bench.py` | `test_bench_resolubilidad_reproducible` (SC-007) | `bench_resolubilidad` |
| **FR-RES-021**: Costos contradictorios abortan con `CriptaDatosInvalidosError`| `CriptaMapa._validar_costos` | `test_costos_contradictorios_aborta_sin_reporte`| N/A |
| **FR-RES-022**: Puertas cerradas sin llave y llaves ausentes en consulta | `VerificadorResolubilidad` | `test_puerta_sin_llave_y_llave_sin_ubicacion` | N/A |
| **FR-RES-023**: Presupuesto agotado aborta con `CriptaLimiteError` | `ServicioResolubilidad` | `test_presupuesto_agotado_sin_reporte_parcial` (SC-008) | N/A |
| **SC-001**: Verificación $< 200\text{ ms}$ en la mayor cripta publicada | `VerificadorResolubilidad` | `test_cota_rendimiento_cripta_mayor` | `bench_resolubilidad_cota` |
| **SC-002**: Costo lineal en salas, salidas y llaves | `VerificadorResolubilidad` | `test_escalabilidad_lineal_sintetica` | `bench_resolubilidad` |
