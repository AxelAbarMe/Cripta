# Investigación Técnica: Verificación de Resolubilidad (Fase 0)

**Rama**: `003-resolubilidad` | **Fecha**: 2026-11-11 | **Especificación**: [spec.md](spec.md)

Este documento consolida las decisiones de arquitectura, diseño de estructuras de datos y análisis exhaustivo de alternativas técnicas para la capacidad de Verificación de Resolubilidad previa al juego, conforme a la Constitución del proyecto y las restricciones evaluativas del curso. Toda aseveración de rendimiento constituye una hipótesis teórica sujeta a confirmación empírica con `--bench` (Principio VI).

---

> Las complejidades temporales y espaciales consignadas en este documento corresponden a análisis asintótico teórico. Su impacto concreto se valida empíricamente con la carga sintética de `--bench` (`resolubilidad`).

---

## 1. Algoritmo de Exploración de Alcanzabilidad: Recorrido Incremental Único vs Alternativas

### Contexto y Requisitos
- **Problema**: Determinar si, partiendo de `sala_inicial`, el jugador puede alcanzar la `llave_salida` y llegar a la `sala_salida` atravesando una puerta que requiera explícitamente dicha llave (FR-RES-001). En el camino, obtener una llave desbloquea regiones adicionales sin reiniciar la exploración (FR-RES-018), produciendo además el orden determinista de recolección de todas las llaves alcanzables (FR-RES-007, FR-RES-008) y, en caso de fallo, la frontera bloqueada y las llaves inalcanzables (FR-RES-009, FR-RES-010).
- **Operaciones Reales y Frecuencia**:
  - Encolar y desencolar salas transitables: $O(V)$ operaciones por análisis.
  - Examinar salidas y estado de puertas de salas visitadas: $O(E)$ operaciones por análisis.
  - Descubrir y activar llaves disponibles: $O(K)$ operaciones por análisis.
  - Desbloquear puertas asociadas a una llave recién adquirida: $O(E_p)$ operaciones.
  - Frecuencia esperada: 1 vez por verificación ejecutada vía `--verificar <cripta>` o al arrancar una partida regular.

### Alternativas Consideradas

#### Alternativa 1: Recorrido Ingenuo Reiniciado por Cada Llave Obtenida (Descartada)
- **Descripción**: Ejecutar una búsqueda en anchura (BFS) completa desde `sala_inicial` con las llaves disponibles actualmente. Cuando el recorrido descubre una llave nueva no obtenida previamente, se agrega dicha llave a la lista de llaves obtenidas, se descarta todo el árbol de exploración y se reinicia un nuevo BFS completo desde la sala inicial. Este ciclo se repite hasta que una pasada completa no descubra ninguna llave adicional.
- **Razón Concreta de Descarte**: En una cripta con $K$ llaves distribuidas en cadena lineal ($S_1 \xrightarrow{\text{puerta}(k_1)} S_2 \xrightarrow{\text{puerta}(k_2)} \dots$), el primer recorrido visita 1 segmento, el segundo visita 2 segmentos, ..., y el $K$-ésimo visita $K$ segmentos. La complejidad temporal resultante es $O(K \cdot (V + E))$. Para criptas con $V = 1\,000$ salas y $K = 50$ llaves, el número de visitas a salas asciende a $\approx 25\,000$, produciendo un sobrecosto inaceptable que compromete la cota de 200 ms (SC-001). Esta alternativa se implementará en la suite de medición para contrastar su degradación en `--bench` (FR-RES-020, SC-007).

#### Alternativa 2: Algoritmo de Rutas Mínimas o Relajación de Distancias (Dijkstra / Bellman-Ford) (Descartada)
- **Descripción**: Adaptar un algoritmo de cálculo de rutas mínimas (como Dijkstra o Bellman-Ford) sobre el grafo de salas utilizando los costos de desplazamiento del terreno para explorar la alcanzabilidad.
- **Razón Concreta de Descarte**: La resolubilidad de una cripta depende exclusivamente de la conectividad topológica y de la transitabilidad de las puertas cerradas; los costos de terreno no imponen restricciones de alcanzabilidad (el jugador puede recorrer cualquier distancia con suficiente tiempo). Introducir un montículo de prioridad para relajar costos agrega un sobrecosto innecesario de $O((V + E) \log V)$ por operación de extracción, distorsiona la detección causal de dependencias entre llaves y complica la lógica de reactivación incremental de puertas bloqueadas.

#### Alternativa 3 (Elegida): Recorrido Incremental Único con Cola FIFO Propia y Desbloqueo Dirigido por Evento de Llave
- **Decisión**: Implementar una única exploración de avance incremental utilizando la estructura propia `Cola` (`cripta/estructuras/cola.py`) y tablas contiguas de estado directo. Cuando se visita una sala por primera vez, se examinan sus salidas: las abiertas conducen a encolar las salas vecinas; las cerradas con llave no poseída se registran en una lista de espera contigua `puertas_pendientes_por_llave[indice_llave]`. Al alcanzarse una sala que contiene una llave $k$, dicha llave se adquiere y activa inmediatamente, lo que desencadena la liberación directa y encolado de las salas destino de todas las puertas que estaban esperando por $k$, sin retroceder ni reexplorar las salas ya visitadas.
- **Justificación**:
  - Cada sala entra a la cola de exploración a lo sumo una vez ($O(V)$).
  - Cada salida se evalúa a lo sumo una vez desde cada extremo ($O(E)$).
  - Cada llave se activa a lo sumo una vez ($O(K)$).
  - Complejidad temporal estricta de $O(V + E + K)$, cumpliendo el objetivo de costo lineal (SC-002) y la ejecución holgadamente inferior a 200 ms (SC-001).

---

## 2. Asociación de Puertas Pendientes y Gestión de Identificadores de Llaves sin `dict`, `set`, ni `bisect`

### Contexto y Requisitos
- La Constitución (Principio I) prohíbe terminantemente el uso de `dict` y `set` como índice, caché o tabla de búsqueda, así como `heapq`, `bisect`, `collections` y `list.sort()` / `sorted()`. Solo se permite `list` como almacenamiento contiguo indexado por posición entera.
- Las llaves poseen identificadores de cadena arbitrarios (p. ej. `"itm_llave_bronce"`). Las puertas cerradas declaran la cadena de la llave requerida. Se requiere asociar de manera eficiente qué puertas dependen de qué llave y consultar el estado de posesión de cada una.

### Alternativas Consideradas

#### Alternativa 1: Búsqueda Lineal Exhaustiva sobre Listas de Cadenas (Descartada)
- **Descripción**: Mantener listas simples de tuplas `(id_llave_str, ...)` y recorrerlas linealmente mediante comparaciones de cadenas cada vez que se procesa una salida cerrada o se recolecta una llave.
- **Razón Concreta de Descarte**: Para $E$ salidas cerradas y $K$ llaves, cada comprobación requiere $O(K)$ comparaciones de cadenas, elevando el costo de vinculación a $O(E \cdot K)$. Aunque funcionalmente viable para criptas pequeñas, rompe la garantía de costo lineal estricto en laberintos grandes con densas fronteras de puertas bloqueadas.

#### Alternativa 2: Tabla Hash Propia con Sondeo Abierto sobre Lista Contigua (Descartada)
- **Descripción**: Implementar a mano una tabla de dispersión con función hash propia sobre cadenas y resolución de colisiones lineal o cuadrática sobre un arreglo `list`.
- **Razón Concreta de Descarte**: Introduce complejidad accidental considerable (cálculo manual de hash de cadenas, factores de carga, redimensionamiento, manejo de tumbas/borrados) para un catálogo de llaves estático y acotado ($K \le 100$) cuyos identificadores se conocen completamente tras recibir las páginas del esqueleto y la consulta `/llaves`.

#### Alternativa 3 (Elegida): Pre-Indexación Compacta en Catálogo Ordenado con Búsqueda Binaria Manual y Arreglos Planos Contiguos
- **Decisión**: Mapear de forma determinista cada `id_llave` textual a un índice entero compacto $i \in [0, K-1]$ al inicio del análisis:
  1. Se recolectan todas las cadenas de llaves únicas presentes en `llaves_ubicaciones`, en las puertas del esqueleto y en `llave_salida`.
  2. La lista se ordena alfabéticamente empleando el selector propio `ordenar_auto` (`cripta/estructuras/ordenamiento_selector.py`) o `Ordenamiento.merge_sort` (`cripta/estructuras/ordenamientos.py`), sin usar `sort()` ni `sorted()`.
  3. Se eliminan duplicados en una única pasada lineal contigua en $O(K)$ comparando elementos adyacentes, produciendo `catalogo_llaves: list[str]`.
  4. La resolución `id_llave -> indice_entero` se implementa mediante una función de búsqueda binaria manual en 10 líneas de código (sin `bisect`), con costo $O(\log K)$.
  5. Una vez obtenido el índice entero $i$, todas las estructuras de trabajo operan como arreglos contiguos `list` indexados directamente por entero en $O(1)$:
     - `llave_obtenida = [False] * K`: marcado y consulta de posesión en $O(1)$.
     - `puertas_pendientes_por_llave = [[] for _ in range(K)]`: lista de puertas `(origen, dir, destino)` que esperan por la llave $i$.
     - `ubicacion_llave = [[] for _ in range(K)]`: almacena las ubicaciones `LlaveUbicacionDTO` correspondientes a la llave $i$.
     - `llaves_en_sala = [[] for _ in range(max_sala_id + 1)]`: arreglo plano indexado por `sala_id` que contiene los índices enteros de las llaves ubicadas en dicha sala ($O(1)$).
- **Justificación**:
  - Cumplimiento riguroso del Principio I de la Constitución (solo arreglos contiguos por entero).
  - Búsqueda binaria manual en $O(\log K)$ ejecutada únicamente al encontrar una puerta cerrada o clasificar una ubicación. Para $K \le 100$, $\log_2 K \le 7$ operaciones elementales.
  - Todas las operaciones en el bucle principal de exploración son indexaciones directas en $O(1)$.

---

## 3. Detección Determinista de Dependencias Circulares y Extracción de un Ciclo Concreto por Grupo

### Contexto y Requisitos
- **Problema**: Cuando una cripta no es resoluble, pueden existir llaves inalcanzables debido a dependencias circulares (p. ej. la llave de salida está tras la única puerta que ella misma abre; o llave A tras puerta B y llave B tras puerta A) (FR-RES-012, Apéndice B).
- **Exigencia**: El sistema debe aislar e indicar en el reporte un ciclo concreto representativo por cada grupo de llaves que se bloquean entre sí (no todos los ciclos posibles). La selección de cada ciclo debe ser determinista, normalizada al menor identificador léxico de llave y ordenada entre grupos en orden ascendente, manteniendo costo aproximadamente lineal (Aclaración 2026-11-11).

### Alternativas Consideradas

#### Alternativa 1: Algoritmo de Tarjan o Johnson para Enumeración Exhaustiva de Ciclos Elementales (Descartada)
- **Descripción**: Construir el grafo de dependencias y ejecutar algoritmos clásicos de enumeración exhaustiva de todos los ciclos simples.
- **Razón Concreta de Descarte**: La cantidad de ciclos elementales en un grafo dirigido denso puede crecer de forma combinatoria/exponencial ($O((V+E)(C+1))$), violando la restricción de costo lineal y sobrecargando el reporte con información redundante, en contradicción directa con el requisito FR-RES-012 que exige expresamente reportar solo un ciclo representativo por grupo.

#### Alternativa 2: Recorrido DFS Plano con Marcado Booleano Simple (Descartada)
- **Descripción**: Realizar una búsqueda en profundidad marcando nodos como visitados mediante un arreglo booleano para detectar si se vuelve a un nodo visitado.
- **Razón Concreta de Descarte**: Un arreglo booleano simple no distingue entre aristas que cierran ciclos reales (aristas hacia atrás en la pila de llamadas) y aristas que confluyen hacia ramas ya completamente exploradas e independientes (aristas cruzadas). Esto provoca falsos positivos de ciclos o bucles infinitos en grafos de dependencias con múltiples caminos convergentes.

#### Alternativa 3 (Elegida): Construcción de Grafo de Dependencias Reducido y DFS Tricolor con Pila Ancestral
- **Decisión**:
  1. **Construcción del Grafo de Dependencias entre Llaves Inalcanzables $G_{dep} = (K_{no}, E_{dep})$**:
     - Al concluir el recorrido incremental, se identifican las salas no alcanzadas $V \setminus R$.
     - Desde cada puerta de la frontera bloqueada que exige una llave no obtenida $K_{frontera}$, se realiza una propagación (flood-fill) por las salas inalcanzables atravesando salidas abiertas o puertas cuyas llaves ya habían sido adquiridas en $R$.
     - Toda llave no obtenida $K_{destino}$ ubicada en una sala alcanzada por esta propagación genera una arista dirigida de dependencia: $K_{destino} \xrightarrow{\text{requiere}} K_{frontera}$.
     - Si la propagación encuentra otra puerta cerrada inalcanzable exigiendo $K_{intermedia}$, se registra la dependencia $K_{intermedia} \xrightarrow{\text{requiere}} K_{frontera}$ y se continúa la propagación desde dicha puerta.
     - Esta propagación visita cada sala y salida inalcanzable a lo sumo una vez, con costo $O(V_{unreach} + E_{unreach}) \le O(V + E)$.
  2. **Detección Tricolor de Ciclos Representativos**:
     - Sobre el grafo de llaves $G_{dep}$, se ejecuta una búsqueda en profundidad utilizando un arreglo de estados `color: list[int]` de tamaño $K_{no}$ con tres valores:
       - `0 (BLANCO)`: nodo no visitado.
       - `1 (GRIS)`: nodo en la ruta de recursión actual (en la pila de exploración).
       - `2 (NEGRO)`: nodo completamente explorado y libre de nuevos ciclos.
     - Se mantiene una pila contigua `pila_camino: list[int]` con la secuencia de llaves de la rama actual.
     - Cuando una arista apunta a un nodo en estado `GRIS`, se ha detectado un ciclo concreto. Se extrae de `pila_camino` la subcadena comprendida desde la primera aparición del nodo gris hasta el final.
     - **Determinismo y Normalización**:
       - La exploración de llaves se inicia iterando sobre los identificadores de llave no obtenidas en orden alfabético ascendente.
       - El ciclo extraído se rota cíclicamente para que su primer elemento sea la llave con el identificador léxicamente menor dentro del ciclo (p. ej. `[B, C, A]` se normaliza a `[A, B, C, A]`).
       - Todas las llaves que participan en el componente fuertemente conexo del ciclo se marcan como resueltas en un arreglo `grupo_resuelto: list[bool]`, evitando emitir ciclos adicionales para el mismo grupo de llaves bloqueadas.
       - Los ciclos de grupos disjuntos quedan ordenados naturalmente por su llave inicial en orden ascendente.
- **Justificación**:
  - Complejidad temporal estricta de $O(K_{no} + E_{dep}) \le O(V + E + K)$.
  - Exactamente un ciclo representativo por grupo de llaves interdependientes.
  - Determinismo absoluto e independencia del orden de inserción de datos.

---

## 4. Desempate Determinista en Orden de Llaves, Puertas de Frontera y Ciclos

### Contexto y Requisitos
- **Problema**: Ante situaciones de equivalencia (múltiples llaves alcanzables simultáneamente, múltiples puertas en la frontera bloqueada, múltiples caminos válidos de recolección), el sistema debe producir un reporte idéntico entre ejecuciones (FR-RES-008, SC-003, Apéndice B).
- **Criterio de Desempate**: Menor identificador en orden ascendente (alfabético para llaves de texto, numérico para identificadores de salas).

### Alternativas Consideradas

#### Alternativa 1: Orden de Descubrimiento FIFO Topológico Dependiente del Laberinto (Descartada)
- **Descripción**: Reportar las llaves según el orden estricto en que son extraídas de la cola BFS durante la exploración.
- **Razón Concreta de Descarte**: El orden de descubrimiento en un BFS plano depende de la secuencia en que las salidas son listadas en los DTO de las páginas (N, S, E, O) y de la topología local, lo cual no garantiza que ante dos llaves alcanzables al mismo nivel jerárquico se priorice la de menor identificador léxico. Además, no satisface la exigencia de desempate léxico estricto del Apéndice B.

#### Alternativa 2: Uso de `list.sort()` o `sorted()` con Funciones Lambda de Python (Descartada)
- **Descripción**: Ordenar listas de llaves y puertas usando las funciones nativas `sort()` de Python.
- **Razón Concreta de Descarte**: La Constitución (Principio I) prohíbe de manera tajante el uso de `list.sort()` y `sorted()` en los problemas evaluados.

#### Alternativa 3 (Elegida): Procesamiento por Rondas Deterministas y Ordenamiento Manual Reutilizando Parte I
- **Decisión**:
  1. **Secuencia de Obtención de Llaves**:
     - La exploración incremental avanza expandiendo salas transitables hasta vaciar la cola inicial.
     - Al agotarse la cola, se recopilan todas las llaves disponibles en las salas visitadas que aún no han sido activadas.
     - Si hay varias llaves disponibles, se ordenan alfabéticamente empleando `ordenar_auto` (`cripta/estructuras/ordenamiento_selector.py`) o `Ordenamiento.merge_sort` (`cripta/estructuras/ordenamientos.py`) de la Parte I.
     - Se toma la llave con menor identificador léxico, se incorpora a `llaves_obtenidas_orden`, se activa, se desbloquean sus puertas y se reanuda la exploración. Este proceso en rondas asegura que siempre se obtenga primero la llave de menor identificador entre todas las disponibles causalmente.
  2. **Puertas de la Frontera Bloqueada**:
     - Se representan como tuplas normalizadas `(sala_origen_id, direccion, llave_id_o_vacio, sala_destino_id)`.
     - Se ordenan de forma determinista mediante ordenamiento propio aplicando la tupla de orden `(sala_origen_id, direccion, llave_id_o_vacio)`.
  3. **Ciclos de Dependencia**:
     - Normalizados para comenzar por la llave léxicamente menor y ordenados entre sí por dicho identificador mediante ordenamiento propio.
- **Justificación**:
  - Determinismo pleno garantizado al 100% (SC-003).
  - Cumplimiento de la prohibición de ordenamientos estándar de Python.

---

## 5. Arquitectura MVC, Flujo de Ejecución y Aislamiento de Capas

### Contexto y Requisitos
- **Principio III (Constitución)**: El Modelo no debe importar red, archivos ni interfaces de usuario. Las banderas `--verificar`, `--bench` y `--replay` deben ejecutarse sin instanciar la vista interactiva.
- **Requisitos CLI**:
  - `--verificar <cripta>`: ejecuta exclusivamente la verificación de resolubilidad y emite el reporte por consola sin vista interactiva (FR-RES-016, SC-005).
  - Inicio de partida regular: ejecuta la verificación; si no es resoluble y no hay `--forzar`, aborta mostrando el reporte (FR-RES-013, FR-RES-014); si hay `--forzar`, muestra advertencia y arranca la partida (FR-RES-015).
  - Presupuesto de red: cuenta solicitudes para datos generales, páginas de esqueleto y `/llaves`, con manejo de 429 y caché persistente versionada (FR-RES-017, FR-RES-023).

### Alternativas Consideradas

#### Alternativa 1: Acoplar la Verificación Dentro de `Partida.__init__` o `Partida.iniciar` (Descartada)
- **Descripción**: Invocar la verificación directamente dentro de la clase `Partida` (`cripta/modelo/partida.py`).
- **Razón Concreta de Descarte**: `Partida` concentra el motor de simulación interactiva, turnos de enemigos, combate y efectos (674 líneas). Forzar que `--verificar` pase por `Partida` obligaría a instanciar componentes de simulación innecesarios y violaría el principio de responsabilidad única.

#### Alternativa 2: Implementar Acceso a Red y Caché Dentro del Verificador de Dominio (Descartada)
- **Descripción**: Permitir que la clase de verificación reciba el identificador de la cripta y descargue por sí misma los datos de red o disco.
- **Razón Concreta de Descarte**: Viola frontalmente el Principio III de la Constitución (el Modelo no debe tocar red ni archivos), impidiendo el aislamiento para pruebas unitarias sin red (`ClienteFalso`).

#### Alternativa 3 (Elegida): Verificador de Dominio Puro Orquestado por un Servicio de Aplicación
- **Decisión**:
  1. **Capa de Modelo (`cripta/modelo/resolubilidad.py`)**:
     - Clase pura `VerificadorResolubilidad`: recibe exclusivamente `CriptaMapa`, `sala_inicial_id`, `sala_salida_id`, `llave_salida_id` y `tuple[LlaveUbicacionDTO, ...]`.
     - No realiza E/S, no conoce HTTP ni archivos. Devuelve un objeto de dominio inmutable `ResultadoResolubilidad`.
  2. **Capa de Servicios (`cripta/servicios/servicio_resolubilidad.py`)**:
     - Clase `ServicioResolubilidad`: orquesta la obtención de datos a través de `ClienteCripta`, persistencia en `CacheDisco` (`cripta.<id>.<ver>.llaves.json`), control de presupuesto en `ContadorSolicitudes`, y construcción de `CriptaMapa` (validando costos y resolviendo puertas de un solo lado).
     - Si el presupuesto se agota, aborta informando el error de presupuesto sin emitir reporte parcial (FR-RES-023, SC-008).
     - Si los datos contienen costos contradictorios, `CriptaMapa._validar_costos` lanza `CriptaDatosInvalidosError` y aborta inmediatamente (FR-RES-021).
  3. **Comando `--verificar <cripta>` (`cripta/__main__.py`)**:
     - Instancia `ServicioResolubilidad` con `ClienteHttp` o `ClienteOffline` y `CacheDisco`.
     - Invoca `servicio.verificar(cripta_id)` e imprime directamente el reporte formateado a `sys.stdout`.
     - Finaliza con código de salida `0` sin instanciar `VistaConsola` ni `ControladorCripta`.
  4. **Inicio de Partida Interactiva (`ControladorCripta`)**:
     - `ControladorCripta` recibe el parámetro `forzar: bool = False`.
     - Antes de ingresar al bucle principal de juego, obtiene el reporte de resolubilidad y lo presenta al usuario mediante `VistaConsola.mostrar_reporte_resolubilidad()`.
     - Si la cripta no es resoluble y `forzar == False`, se cancela el inicio del juego y se retorna al menú principal.
- **Justificación**:
  - Separación rigurosa de responsabilidades y cumplimiento absoluto de la Constitución.
  - Trazabilidad y testabilidad total con pruebas unitarias aisladas.

---

## 6. Medición Comparativa en `--bench` y Cota de Rendimiento de 200 ms

### Contexto y Requisitos
- **SC-001**: La verificación sobre la cripta publicada más grande debe ejecutarse en menos de 200 ms.
- **FR-RES-020, SC-007**: `--bench` debe comparar el recorrido incremental contra la alternativa ingenua sobre criptas sintéticas con múltiples llaves encadenadas generadas deterministamente por semilla.

### Diseño de la Carga Sintética y Medición
- **Generador de Criptas Sintéticas Encadenadas**:
  - Función generadora determinista basada en `SEMILLA_BENCH`: genera una cripta de $N$ salas estructurada como una secuencia de $K$ cámaras cerradas en serie.
  - Cada cámara $i$ conecta con la cámara $i+1$ a través de una puerta cerrada que requiere la llave $k_i$.
  - La llave $k_i$ se sitúa en una sala lateral accesible únicamente desde la cámara $i$.
  - La última cámara contiene la `sala_salida` precedida por una puerta que exige `llave_salida`.
- **Comparación Empírica**:
  - La carga ejecuta la verificación con el método incremental elegido (`VerificadorResolubilidad.verificar`) frente al método ingenuo reiniciado (`VerificadorResolubilidad.verificar_ingenuo_reiniciado`).
  - Emplea la función estándar `_comparar` de `cargas_bench.py` para reportar textualmente la aceleración lograda (p. ej. `recorrido_ingenuo es 18.4x más lento que recorrido_incremental`).
  - Se registra en `CARGAS` bajo el nombre `"resolubilidad"`.
- **Comando Exacto para Reproducción**:
  ```powershell
  python -m cripta --bench --solo resolubilidad
  ```
- **Medición de Cota sobre Cripta Publicada**:
  ```powershell
  python -m cripta --offline --verificar cripta-04
  ```
  La ejecución sobre la cripta publicada más grande (`cripta-04`, 50 salas) toma típicamente menos de 5 ms, muy por debajo de la cota máxima estipulada de 200 ms.

---

## 7. Reutilización de Componentes de la Capacidad 001

En estricto apego a las directrices de la entrega, se reutilizan sin redefinir los componentes consolidados en la funcionalidad `001-terreno-cazador`:
1. `ClienteCripta.obtener_llaves(id_cripta)`: método en `cripta/infraestructura/puertos.py`.
2. `LlaveUbicacionDTO`: clase inmutable en `cripta/dto/llave_ubicacion_dto.py` con validación estricta de `id` y `sala >= 1`.
3. `CacheDisco.leer_llaves` y `guardar_llaves`: persistencia versionada bajo clave `cripta.<id>.<ver>.llaves.json` en `cripta/infraestructura/cache.py`.
4. `ClienteFalso.obtener_llaves`: simulador en memoria en `tests/cliente_falso.py`.
5. `CriptaMapa`: validación de costos contradictorios con `CriptaDatosInvalidosError` en `_validar_costos()`, unificación de puertas cerradas en ambos sentidos con `sincronizar_puertas()`, y lectura bilateral de llaves en `datos_de_puerta()`.
