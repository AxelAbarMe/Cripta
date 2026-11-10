# Investigación Técnica: Terreno y Cazador (Fase 0)

**Rama**: `001-terreno-cazador` | **Fecha**: 2026-11-09 | **Especificación**: [spec.md](spec.md)

Este documento consolida las decisiones de arquitectura, diseño de estructuras de datos y análisis de alternativas para la capacidad de Terreno y Cazador, conforme a la Constitución del proyecto y las restricciones del curso. Toda afirmación de rendimiento es una hipótesis a confirmar con `--bench` (Principio VI).

---

> Las complejidades de este documento son análisis teórico, no mediciones. Su efecto real se mide con las cargas de `--bench` del plan (`ruta_cazador`, `invalidacion`).

## 1. Algoritmo de Búsqueda de Ruta de Costo Mínimo y Estructuras Auxiliares

### Contexto y Requisitos
- **Problema**: Calcular la ruta de costo mínimo a través de salidas abiertas con costos enteros $\ge 1$ entre actores (específicamente cazadores) y el objetivo (jugador), desempatando de forma determinista ante caminos de igual costo mínimo (FR-TER-010, FR-TER-012, FR-TER-013).
- **Restricciones de la Constitución**: Prohibido `heapq`, `bisect`, `collections`, `networkx`, `dict` o `set` como índice/tabla/caché. Estructuras a mano; reutilizar estructuras de la Parte I donde sea adecuado.

### Alternativas Consideradas

#### Alternativa 1: Dijkstra Unidireccional con Búsqueda Lineal del Mínimo sobre Lista Contigua
- **Descripción**: Mantener una lista contigua de nodos pendientes. En cada paso, recorrer linealmente la lista completa para encontrar el nodo con menor distancia tentativa.
- **Razón de Descarte**: En un laberinto con $V$ salas y rango amplio, la extracción del mínimo toma $O(V)$, lo que eleva el costo total a $O(V^2 + E)$. Se plantea como hipótesis a confirmar con `--bench` que, para criptas de cientos de salas con varios cazadores, esto comprometería el límite de 20 ms por ciclo de eventos (P2 §6.1).

#### Alternativa 2: Algoritmo A* hacia el Jugador con Heurística de Distancia Manhattan o Topológica
- **Descripción**: Implementar A* guiado por una función heurística para orientar la búsqueda hacia la sala del jugador.
- **Razón de Descarte**: El grafo de la cripta es una topología de salas conectadas por salidas N, S, E, O sin coordenadas espaciales garantizadas, por lo que no hay una heurística admisible conocida. Una heurística no admisible rompe la optimalidad y la equivalencia observable exigida por FR-TER-015. Además, A* individual por cada cazador impide reutilizar la búsqueda para múltiples cazadores persiguiendo al mismo objetivo.

#### Alternativa 3 (Elegida): Algoritmo de Dijkstra con Montículo Binario Propio (`HeapMinimo`) y Tabla Contigua Directa
- **Decisión**: Implementar el algoritmo de Dijkstra clásico utilizando la estructura propia `HeapMinimo` (reutilizada y complementada desde `cripta/estructuras/heap_min.py`) como cola de prioridad de pares `(distancia, sala_id)`, y un arreglo plano `list` indexado directamente por `sala_id` entero para el registro de distancias mínimas y nodos cerrados.
- **Justificación**:
  - `HeapMinimo` realiza inserción en $O(\log V)$ y extracción del mínimo en $O(\log V)$.
  - El acceso y actualización de distancias en una lista contigua `list[int | None]` indexada por entero toma $O(1)$ sin recurrir a `dict` ni `set`.
  - La complejidad temporal resultante es $O((V + E) \log V)$ con montículo binario, adecuada para grafos dispersos con grado acotado $\le 4$.

---

## 2. Registro de Distancias y Visitados sin `dict` ni `set`

### Contexto y Requisitos
- La Constitución prohíbe el uso de `dict` y `set` como índices, tablas de búsqueda o estructuras propias. Se permite únicamente `list` como almacenamiento contiguo indexado por posición entera.

### Alternativas Consideradas

#### Alternativa 1: `VectorOrdenado` de Pares `(sala_id, distancia)` (`cripta/estructuras/vector.py`)
- **Descripción**: Almacenar las distancias en un `VectorOrdenado` donde cada consulta o inserción realiza búsqueda binaria por clave `sala_id`.
- **Razón de Descarte**: Aunque la búsqueda es $O(\log V)$, la inserción dinámica desplaza elementos en $O(V)$. Para $V$ nodos descubiertos, la construcción de la tabla toma $O(V^2)$. Aunque se preasignara el vector con todas las salas, cada actualización o consulta de distancia requeriría $O(\log V)$ por búsqueda binaria frente al $O(1)$ del indexado directo.

#### Alternativa 2: Tabla Hash con Sondeo Abierto Implementada a Mano
- **Descripción**: Implementar una tabla de dispersión propia sobre una lista contigua con resolución de colisiones lineal o cuadrática.
- **Razón de Descarte**: Introduce complejidad innecesaria de factores de carga, funciones hash y redimensionamiento dinámico, cuando los identificadores de salas en el esqueleto son enteros acotados conocidos desde la carga inicial de la cripta.

#### Alternativa 3 (Elegida): Arreglo Plano Contiguo Indexado Directamente por `sala_id`
- **Decisión**: Utilizar una lista de tamaño `max_sala_id + 1` inicializada con un valor centinela (`-1` o `None`).
- **Justificación**:
  - Cumple el Principio I de la Constitución («almacenamiento contiguo indexado por posición entera»).
  - Acceso $O(1)$ para lectura y actualización de `dist[sala_id]`.
  - El conjunto de nodos visitados/cerrados se registra mediante una lista booleana contigua `visitados = [False] * (max_sala_id + 1)`, con consulta y marcado en $O(1)$.
  - Espacio $O(V)$ (la huella de memoria concreta es una hipótesis a confirmar con `--bench`).

---

## 3. Cálculo Compartido vs Individual ante Múltiples Cazadores

### Contexto y Requisitos
- Decenas de cazadores pueden estar activos simultáneamente persiguiendo al mismo objetivo (la sala actual del jugador $S_J$).
- El ciclo de eventos debe ejecutarse en menos de 20 ms (FR-TER-020).

### Alternativas Consideradas

#### Alternativa 1: Cálculo Individual por Cada Cazador (Dijkstra Hacia Adelante)
- **Descripción**: Cada vez que un cazador ejecuta su turno, lanza una búsqueda Dijkstra desde su sala $u$ hacia la sala del jugador $S_J$.
- **Razón de Descarte provisional**: Con $H$ cazadores activos en un ciclo, se ejecutan $H$ búsquedas independientes de Dijkstra. Para $H = 30$ cazadores, se plantea como hipótesis a confirmar con `--bench` que $30 \times ((V + E) \log V)$ superaría el límite de 20 ms.

#### Alternativa 2: Matriz de Todas las Rutas Más Cortas (Floyd-Warshall o All-Pairs)
- **Descripción**: Precalcular y mantener las distancias entre todos los pares de salas de la cripta.
- **Razón de Descarte**: Complejidad espacial $O(V^2)$ y temporal $O(V^3)$. Cualquier cambio de estado en una puerta (apertura o cierre automático) invalidaría la matriz completa, requiriendo un recálculo masivo.

#### Alternativa 3 (Elegida): Cálculo Compartido desde el Objetivo (Single-Source Dijkstra Inverso)
- **Decisión**: Ejecutar una **única** búsqueda de Dijkstra teniendo como nodo origen la sala actual del jugador $S_J$, explorando hacia afuera sobre las salidas abiertas.
- **Justificación y Equivalencia**:
  - Las conexiones del laberinto son simétricas en costo (FR-TER-002) y transitabilidad de puertas (si una puerta está abierta, lo está en ambos sentidos). `CriptaMapa` resuelve el costo desde ambos lados de la conexión: si solo un lado lo declara, rige para ambos; si difieren, el dato es inválido.
  - Por simetría de grafos no dirigidos ponderados, la distancia mínima de $u$ a $S_J$ es idéntica a la distancia mínima de $S_J$ a $u$:
    $$\text{dist}(u, S_J) = \text{dist}(S_J, u)$$
  - Un único recorrido calcula simultáneamente $\text{dist}(S_J, v)$ para todas las salas $v$ dentro del alcance.
  - Cada cazador en sala $u$ consulta en $O(1)$ sus a lo sumo 4 vecinas abiertas $v$, evaluando la condición de ruta mínima:
    $$\text{costo}(u, v) + \text{dist}(v, S_J) == d$$
  - Complejidad: 1 búsqueda $O((V_R + E_R) \log V_R) + H \times O(1)$. Para 30 cazadores, se plantea como hipótesis a confirmar con `--bench` que el tiempo se reduce a una fracción del cálculo individual.

### Condiciones de Rendimiento: Cuándo Conviene Cada Alternativa
- **Cálculo compartido**: Se espera superior cuando conviven múltiples cazadores activos ($H > 1$) o cuando los rangos de persecución son homogéneos, ya que una sola búsqueda cubre a todos los cazadores ($O((V_R + E_R) \log V_R) + H \times O(1)$).
- **Cálculo individual**: Podría convenir en rendimiento bajo condiciones específicas:
  1. **Muy pocos cazadores** (ej. $H = 1$), donde la sobrecarga de estructurar la búsqueda compartida no se amortiza.
  2. **Rangos muy heterogéneos con $R_{\max}$ grande**: Si un solo cazador tiene un rango muy amplio y varios otros tienen rangos muy pequeños, la búsqueda compartida se ve obligada a expandirse hasta $R_{\max}$, explorando potencialmente muchas más salas de las que explorarían individualmente los cazadores de rango corto.
- **Medición empírica**: Las condiciones de frontera exactas en que un enfoque aventaja al otro se medirán con `--bench` (carga `ruta_cazador`).

### Equivalencia del Resultado (Corrección, no Rendimiento)
- La decisión del cazador con cálculo compartido **no cambia** respecto a calcular desde cero individualmente si se respetan las siguientes condiciones:
  1. **Simetría de costos**: Establecida por FR-TER-002 y comprobada con una prueba sobre la cripta de referencia.
  2. **Estado idéntico de puertas**: La búsqueda solo expande aristas con puertas abiertas en ese instante.
  3. **Desempate determinista**: El cazador evalúa todas sus vecinas abiertas $v$ con $\text{costo}(u, v) + \text{dist}(v, S_J) == d$ y elige $\min(v.id)$ (FR-TER-013). Como $\text{dist}(v, S_J)$ es única, el conjunto de vecinas óptimas y el desempate por menor ID son idénticos en ambos enfoques.
  4. **Invalidación ante cambios**: Si el jugador cambia de sala o una puerta cambia de estado, la tabla compartida se invalida.

---

## 4. Política de Invalidación de Caché de Rutas

### Contexto y Requisitos
- FR-TER-015 exige equivalencia observable con el cálculo desde cero.

### Matriz de Eventos e Invalidación

| Evento | ¿Altera el Grafo o el Objetivo? | Acción sobre Caché | Justificación |
|---|---|---|---|
| **Movimiento del jugador** | Sí (cambia el nodo origen $S_J$) | **INVALIDAR** | Las distancias relativas al jugador cambian por completo. |
| **Apertura de puerta** (jugador con llave) | Sí (se añade una arista transitable) | **INVALIDAR** | Pueden aparecer nuevas rutas más cortas. |
| **Cierre de puerta** (`cierre_automatico`) | Sí (se elimina una arista transitable) | **INVALIDAR** | Las rutas que cruzaban dicha puerta quedan bloqueadas. |
| **Pergamino de retroceso** | Sí (revierte movimientos del jugador y estados de puertas) | **INVALIDAR** | Se restaura el estado previo, requiriendo sincronización limpia. |
| **Activación de un cazador con rango mayor al $R_{\max}$ calculado** | Sí (el alcance de la búsqueda era insuficiente) | **INVALIDAR (recalcular con el nuevo $R_{\max}$)** | La tabla no cubre la región que el nuevo cazador necesita. |
| **Carga de una partida guardada** | Sí (cambia el estado completo) | **INVALIDAR** | No hay garantía de que la tabla corresponda al estado cargado. |
| **Movimiento de un cazador** | No (los enemigos no bloquean salas ni puertas) | **CONSERVAR** | La posición del jugador y la transitabilidad del laberinto permanecen intactas. |
| **Muerte de un actor (enemigo)** | No (no afecta topología ni al jugador) | **CONSERVAR** | El grafo y la sala del jugador no se alteran. |
| **Cambio de velocidad de un actor** | No (solo altera el tiempo de agenda, no los costos espaciales) | **CONSERVAR** | El costo $d$ es suma de costos de salida, independiente de la velocidad. |

---

## 5. Límite por Rango de Persecución

### Contexto y Requisitos
- Cada cazador tiene un atributo `rango` entero $\ge 1$ en unidades de costo (FR-TER-008).
- Si la distancia mínima excede el rango ($d > \text{rango}$), el cazador espera (FR-TER-011).
- No recorrer toda la cripta si el rango es pequeño.

### Decisión Técnica
- Al invocar la búsqueda compartida de Dijkstra desde $S_J$, se determina el rango máximo relevante:
  $$R_{\max} = \max_{h \in \text{cazadores activos}} (h.\text{rango})$$
- **Poda temprana en Dijkstra**:
  Cuando el elemento extraído del montículo tiene una distancia acumulada $d_{\text{actual}} > R_{\max}$, el algoritmo **detiene la expansión** (break del bucle).
- **Corrección**:
  Dado que todos los costos de salida son enteros positivos ($c \ge 1$), no existen aristas de costo cero o negativo. Por la propiedad voraz de Dijkstra, cualquier extracción futura tendrá distancia $\ge d_{\text{actual}} > R_{\max}$. Ninguna sala con distancia $\le R_{\max}$ puede ser descubierta después.
- **Consulta del cazador**:
  Para un cazador con rango específico $R_h \le R_{\max}$:
  Si su sala $u$ no fue alcanzada en la búsqueda o $\text{dist}(u, S_J) > R_h$, el cazador espera con costo 100.
  Si $\text{dist}(u, S_J) \le R_h$, todas sus vecinas óptimas $v$ satisfacen $\text{dist}(v, S_J) = \text{dist}(u, S_J) - \text{costo}(u, v) < R_h \le R_{\max}$, por lo que están garantizadas de haber sido calculadas.

---

## 6. Desempate por Menor Identificador Numérico (FR-TER-013)

### Contexto y Requisitos
- Cuando existen dos o más salas vecinas $v$ que ofrecen rutas de costo mínimo idéntico $d$ hacia el jugador:
  $$\text{costo}(u, v) + \text{dist}(v, S_J) == d$$
  el cazador debe elegir la vecina con el menor identificador numérico (`min(v.id)`).

### Decisión Técnica
- Para el cazador situado en la sala $u$:
  1. Obtener todas las salidas que existen desde $u$ hacia vecinas $v$ (`mapa.vecinos(u)`).
  2. Filtrar únicamente aquellas con puerta abierta (`mapa.puerta_transitable(u, dir)`).
  3. Para cada vecina abierta $v$, calcular el costo total de ruta pasando por ella:
     $$D_v = \text{costo}(u, v) + \text{dist}(v, S_J)$$
     (donde $\text{dist}(v, S_J) = \infty$ si $v$ no fue alcanzada dentro del rango).
  4. Determinar la distancia mínima alcanzable $d = \min_{v} (D_v)$.
  5. Si no hay salidas transitables o $d > \text{rango}$ (o $d = \infty$), la decisión es esperar (costo 100).
  6. Si $d \le \text{rango}$, recolectar todas las vecinas que alcanzan exactamente $d$:
     $$\text{candidatas} = \{ (v.\text{id}, \text{dir}, \text{costo}(u, v)) \mid D_v == d \}$$
  7. Seleccionar la tupla con menor $v.\text{id}$.
  8. La dirección elegida es `dir` y el costo de la acción es `costo(u, v)`.
- **Determinismo**: La tupla `(v.id, dir, costo)` define un orden total sin ambigüedades.

---

## 7. Impacto en la Agenda y el Reloj Virtual

### Contexto y Requisitos
- Costos de movimiento variables: $c = \text{costo\_salida} \ge 1$.
- Intervalo virtual: $\text{intervalo} = \max(1, c \cdot 100 // \text{velocidad})$.
- Cambio de velocidad mientras está programada la próxima acción que siguió a un movimiento (el actor ya está en la sala destino):
  $$\text{restante\_nuevo} = \max(1, (t_{\text{sig}} - t) \cdot v_{\text{ant}} // v_{\text{nueva}})$$

### Decisión Técnica
- **Cálculo de Intervalo**: Reutilizar `calcular_intervalo` y `calcular_tiempo_reprogramado` de `cripta/modelo/reloj.py`.
- **Reprogramación con Nueva Secuencia**:
  En `RelojEventos.reprogramar(evento, nuevo_tiempo)`, se cancela el evento anterior y se inserta un nuevo `EventoProgramado` con un número de secuencia nuevo.
  Esto permite que los desempates en el mismo tick $t$ se resuelvan con un orden total determinista.
- **Frecuencia de Eventos**: Con salidas de costo 1 y velocidad 200, el intervalo es $\max(1, 100 // 200) = 1$. La agenda sobre `HeapMinimo` tiene inserción y extracción en $O(\log K)$. Se plantea como hipótesis a confirmar con `--bench --solo agenda` que la tasa de eventos no degrada el ciclo.

---

## 8. Arquitectura y Desacoplamiento del Contrato de Datos

### Contexto y Requisitos
- Las capacidades 002 (niebla e «ir a»), 003 (resolubilidad) y 004 (línea de tiempo) dependen de los datos de terreno (`costo`), catálogo (`rango`) y la nueva consulta `GET /criptas/{id}/llaves`.
- El contrato debe implementarse como un bloque autónomo y verificable de forma prioritaria.

### Componentes del Contrato de Datos
1. **`SalidaDTO` (`cripta/dto/salida_dto.py`)**:
   - Atributo inmutable `costo: int | None = None`.
   - `desde_json`: si `"costo"` está presente, validar entero $\ge 1$; si es nulo o ausente, dejar `None` (no declarado en este lado). El valor 100 por defecto lo aplica `CriptaMapa` al resolver la conexión, porque el costo puede venir declarado en un solo lado.
2. **`EnemigoDTO` (`cripta/dto/enemigo_dto.py`)**:
   - Atributo inmutable `rango: int | None = None`.
   - `desde_json`: si `comportamiento == "cazador"` y `"rango"` es un entero positivo $\ge 1$, se conserva. Si el rango es nulo, falta, no es entero o es menor que 1, no se lanza excepción: `rango` queda en `None` y el cazador se trata de forma pasiva (ataca si comparte sala con el jugador y si no espera con costo 100; nunca persigue), con un aviso a la bitácora de mensajes al activarse (FR-TER-008).
3. **`LlaveUbicacionDTO` (`cripta/dto/llave_ubicacion_dto.py` — Nuevo)**:
   - Nuevo DTO inmutable `(id: str, sala: int, enemigo: str | None = None)`.
   - Si `enemigo` es nulo o ausente, la llave está en el suelo de la sala. Si está presente, la porta el enemigo indicado.
4. **Puertos y Adaptadores (`cripta/infraestructura/`)**:
   - `ClienteCripta` (`puertos.py`): añadir `obtener_llaves(id_cripta: str) -> tuple[LlaveUbicacionDTO, ...]`.
   - `ClienteHttp`: llamada HTTP con cabecera `X-Cripta-Client-Id`, deducción de presupuesto y gestión de HTTP 429.
   - `ClienteOffline`: lectura de `fixtures/<id>/llaves.json`.
   - `CacheDisco`: almacenamiento de claves versionadas `cripta.<id>.<version>.llaves.json`.
5. **Control de Versión e Invalidación Formal**:
   - Las claves de caché integran la versión de la cripta y el catálogo. Cualquier discrepancia produce fallo de caché automático, sin requerir borrado de archivos en disco.