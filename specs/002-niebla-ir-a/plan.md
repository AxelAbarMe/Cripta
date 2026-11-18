# Plan de implementación: Niebla de guerra e «ir a»

**Rama**: `002-niebla-ir-a` | **Fecha**: 2026-11-15 | **Especificación**: [spec.md](spec.md)

## Resumen

La capacidad mantiene una representación propia del conocimiento del jugador, revela solo las salas alcanzadas por entradas ordinarias o por la antorcha, conserva una observación por puerta y calcula «ir a» sobre el subgrafo conocido. El plan usa listas indexadas por identificador entero y las estructuras manuales existentes. Cada actualización del conocimiento registra una operación inversa en el historial de la Parte I. Cada movimiento del viaje sigue pasando por la acción ordinaria del modelo y el servicio, para que reloj, eventos, retroceso y bitácora mantengan su semántica.

La búsqueda de «ir a» es una búsqueda de costo mínimo propia del jugador, separada de la del cazador prevista por la 001; solo comparte `HeapMinimo`. La alternativa de selección lineal del siguiente nodo también se implementa en la carga de medición. Los resultados son hipótesis hasta ejecutar `--bench`.

## Contexto técnico

- **Lenguaje**: Python 3.11 o superior.
- **Dependencias**: biblioteca estándar; no añadir bibliotecas de grafos ni de rutas.
- **Almacenamiento**: estado del modelo proyectado a `EstadoPartida`; la capacidad 004 define y es dueña del formato binario.
- **Pruebas**: `unittest` bajo `tests/`, con la estructura de paquetes existente.
- **Plataforma**: CLI existente, modalidad interactiva, `--replay` y `--bench` sin instanciar la vista.
- **Rendimiento**: consulta de sala y puerta O(1), revelación O(R) para R salas reveladas en la actualización y cálculo de un primer paso con Dijkstra O((V+E) log V) son complejidades estimadas. El objetivo de menos de 5 ms con el mapa completo de referencia también es una estimación hasta medir con `py -m cripta --bench --solo niebla_rutas --escala 1`.
- **Restricciones**: nada de `dict`/`set` como índice, caché o tabla de búsqueda; nada de `heapq`, `bisect`, `collections`, `networkx` o `sort`/`sorted` donde rigen las prohibiciones. No copiar el estado completo por acción. El modelo no conoce red, disco ni vista. Ningún dato de cripta concreta se fija en el código.
- **Alcance**: estados de conocimiento, evolución y reversión, consulta del mapa, viaje y registro. No define el formato binario ni reglas adicionales a [spec.md](spec.md).

## Comprobación de constitución

| Puerta | Resultado | Evidencia de diseño |
|---|---|---|
| Estructuras manuales y consultas sin tablas hash | Cumple | Tablas contiguas por id; Dijkstra usa `HeapMinimo` propio; sin bibliotecas prohibidas. |
| Determinismo | Cumple | Orden de vecinos N/S/E/O al revelar; desempate explícito por id; carga sintética con `random.Random(semilla)` local. |
| MVC y modos sin vista | Cumple | El modelo calcula y devuelve resultados; el controlador coordina la orden; la vista presenta mapa y motivos. `--replay`/`--bench` no crean vista. |
| Estado reversible sin instantáneas por acción | Cumple | Registrar inversas puntuales por celda cambiada en `HistorialRetroceso`. |
| Especificación y trazabilidad | Cumple | No se cambia spec ni checklist; la matriz al final enlaza requisitos, componentes y pruebas/mediciones. |
| Persistencia y línea de tiempo | Coordinación requerida | Se incorpora la proyección del conocimiento al estado de partida; capacidad 004 define el formato y su compatibilidad. |
| Revisión Parte I | Cumple con medición | Se conserva el mecanismo de inversas y se mide la carga adicional de modificaciones por antorcha. |

## Decisiones de diseño

### Conocimiento consultable y revelación incremental

**Operaciones y frecuencia esperada.** Consultar estado de una sala y estado recordado de una puerta ocurre en cada renderizado del mapa, durante los pasos de ruta y al actualizar observaciones; es frecuente (§5.3). Revelar una sala ocurre al entrar o al entrar con antorcha encendida y, en una actualización, está acotado por las salas que esa entrada revela. La inspección de salidas tiene grado máximo cuatro por las direcciones cardinales del modelo.

**Alternativas evaluadas.** (1) `VectorOrdenado` por id, reutilizado directamente para cada consulta: ahorra memoria para ids dispersos, pero hace O(log V) cada consulta y O(R log V) la revelación, en conflicto con la consulta barata y el costo proporcional a lo revelado. (2) `dict`/`set` por id o puerta: consultas esperadas O(1), pero están prohibidos. (3) Lista indexada por id: almacenamiento contiguo permitido, consulta/cambio O(1) y revelación O(R) más el grado constante de cada sala.

**Decisión.** Añadir `ConocimientoJugador` como estado del modelo. Mantener una lista de estados de sala indexada por id entero (`desconocida`, `avistada`, `explorada`) y una lista por sala con cuatro observaciones de puerta (`no_observada`, `abierta`, `cerrada`). Un id fuera del rango asignado se consulta como desconocido/sin observación, sin buscarlo en una tabla hash. Inicializar la sala inicial como explorada. Al explorar una sala, marcar sus destinos no explorados como avistados. Con antorcha, al entrar, revelar cada vecina como explorada y revelar solo la puerta que conecta con la sala de entrada; no inspeccionar el contenido de la vecina. Cada iteración visita solo las salidas de la sala actual y las salas nuevas, nunca recorre el mapa conocido completo.

La asignación contigua requiere espacio hasta el mayor id de sala. La carga y el informe medirán memoria y tiempo; ids muy dispersos son un límite conocido. No se cambia `CriptaMapa` ni se infiere un id que no conste en el esqueleto.

La capacidad se dimensiona una sola vez desde el mayor id que ya entrega el esqueleto al crear la partida. Así, la asignación inicial puede costar O(max_id), pero explorar después una sala no amplía ni recorre las listas: el costo de cada actualización sigue dependiendo de las celdas reveladas.

Los costos revelados se guardan en listas propias indexadas por id de sala y dirección, con consulta O(1). `ruta_conocida.py` consulta esos costos y no llama a `CriptaMapa.costo_de_conexion`. Se descarta consultar el costo al mapa real en cada relajación porque mezclaría la proyección del jugador con el esqueleto y añadiría una búsqueda por salida. Las pruebas de equivalencia y `--bench` compararán la alternativa de costo almacenado con la consulta al esqueleto sin fijar cifras anticipadas. Los costos forman parte de la proyección persistida y se restauran desde ella.

**Complejidad esperada.** Consultar sala/puerta O(1); revelar R salas y sus puertas incidentes O(R), dado que el grado está acotado por cuatro; memoria O(max_id + 4·max_id). Son estimaciones asintóticas, no mediciones.

### Observación, cierres y reversión

La observación se actualiza cuando el jugador entra a una sala y cuando permanece en una sala conectada a la puerta que cambia. La acción ordinaria de entrar observa las puertas incidentes; si la antorcha está encendida, también revela vecinas según FR-NIE-005. Si un cierre automático cambia una puerta mientras el jugador está en una de sus dos salas, el evento actualiza inmediatamente la observación recordada. Si el jugador no está en ninguno de sus extremos, solo cambia el estado real. Al entrar después a cualquiera de los extremos se sincroniza la observación con el estado real vigente. Este calendario aplica la regla declarada en spec.md sin exponer puertas fuera del conocimiento.

Para cada escritura que cambie una celda se conserva el valor anterior y se registra su inversa mediante `Reversible._registrar_inversa`, conectado a `HistorialRetroceso.registrar_cambio`. No se copia el mapa ni la lista completa por acción; si una entrada revela varias salas, se registran inversas solo para las celdas modificadas. Si una celda ya tenía el mismo valor, no se agrega una inversa redundante. El mecanismo LIFO revierte primero los cambios tardíos de la misma acción. La carga inicial restaura datos sin registrar inversas.

**Estado nuevo que se guarda.** El estado de partida debe contener, por sala, el nivel de conocimiento, los costos conocidos por salida y las cuatro últimas observaciones de puerta. Se serializa como datos planos, no como closures. La antorcha/efecto activo y su duración solo se incluyen si ya forman parte del estado general de efectos; esta capacidad no redefine ese estado. Esta capacidad define los campos lógicos y su proyección. La 004 define codificación binaria y versión y hará un solo cambio de versión. La restauración reconstruye `ConocimientoJugador` antes de permitir consultas o acciones; los costos se toman de la proyección persistida.

**Dependencia.** La 004 es dueña de la codificación binaria y su versión y realizará un solo cambio de versión. Esta capacidad define los campos lógicos del conocimiento y su proyección. Guardar y cargar (SC-NIE-005) depende de 004; no queda pendiente una decisión sobre propiedad del formato.

### Búsqueda y viaje «ir a»

**Operaciones y frecuencia esperada.** Una ruta se calcula antes del primer movimiento y se recalcula antes de cada paso (§3.4 y FR-NIE-012); las observaciones durante el paso pueden invalidarla. El tamaño es el subgrafo de salas exploradas y puertas recordadas abiertas.

**Alternativas.** (1) Reutilizar la búsqueda del cazador prevista por la 001 (`specs/001-terreno-cazador/plan.md`, `BuscadorRutas`): descartada porque calcula sobre el mapa real (vecinos y puertas transitables reales) y no sobre el conocimiento del jugador; poda por el rango de los cazadores; guarda una tabla con invalidación pensada para eventos de cazadores y no recibe destino. Adaptarla obligaría a modificar un archivo de otra capacidad que aún no está en `main`. (2) Búsqueda de costo mínimo propia con `HeapMinimo`: calcula sobre el subgrafo conocido, con O((V+E) log V). (3) La misma búsqueda con selección lineal manual del mínimo: O(V²+E); se implementa solo como alternativa de `--bench`.

**Decisión.** Opción 2, en `cripta/modelo/ruta_conocida.py` (Nuevo). Calcula las distancias desde el destino sobre salas exploradas y puertas recordadas abiertas, en una lista indexada por id. El primer paso es la vecina del origen que minimiza el costo de la salida más la distancia, con desempate por menor id. Se recalcula desde cero antes de cada paso. Respecto de la 001, solo reutiliza `HeapMinimo`, que necesita `esta_vacio` y `__len__`; esos métodos los añade la 001 (tarea T029 de su plan) y esta capacidad no los vuelve a definir.

**Complejidad esperada.** Búsqueda con heap binario propio: O((V+E) log V), memoria O(V+E) para distancias, predecesores y heap; cálculo repetido antes de cada paso. Selección lineal: O(V²+E), memoria O(V+E). No son cifras medidas.

**Bucle y MVC.** El bucle de la orden reside en `ControladorCripta`, que ya despacha órdenes interactivas. Antes de cada movimiento pide al modelo el siguiente paso/ruta, ejecuta `Accion("mover", direccion)` mediante `ServicioPartida.ejecutar` y evalúa el resultado completo antes de continuar. El bucle solo ejecuta los pasos de la propia orden y no despacha otras acciones entre ellos. El modelo no recibe objetos de vista ni formatea mensajes. El controlador entrega el mapa conocido a la vista y le presenta el motivo final de detención. Las acciones siguen siendo normales, de modo que eventos y pergamino actúan durante cada paso. Si se usa un pergamino, el viaje se cancela conforme a FR-NIE-017 y solo continúa con una nueva orden. La prueba de B-NIE-006 ejecuta el viaje paso a paso desde el servicio, intercala el pergamino y comprueba que se revirtió un solo paso y que no hubo pasos posteriores. Si el pergamino se usa después de un paso del viaje, ya sea como orden posterior al viaje detenido o intercalado desde el servicio en las pruebas, revierte solo el último paso y el viaje no se reanuda; esta redacción no añade reglas a FR-NIE-017.

**Bitácora.** `ServicioPartida` expone un método nuevo (nombre a proponer por la implementación) para registrar un único comentario de viaje. `ControladorCripta` lo llama una sola vez, antes del primer paso y solo cuando la ruta tiene al menos un paso; si no existe ruta al inicio, el destino es inválido o es la sala actual, no lo llama. Cada paso posterior se registra como acción ordinaria individual por `ServicioPartida`. Se amplían lector/replay para reconocer y omitir el comentario de depuración sin tratarlo como acción. Los turnos de enemigos continúan sin registro, según la regla de la 001 prevista en `specs/001-terreno-cazador/plan.md`; no se cita como código existente.

**Formato del comentario.** Cada línea posterior al encabezado es hoy una acción en forma de diccionario. El comentario se escribe como una línea que empieza con `#` seguida de la orden y su destino. `PartidaLog` gana un método para registrarlo y el lector descarta esas líneas, de modo que el replay solo ve acciones. Alternativa descartada: un objeto con clave `comentario`, porque obliga a todo consumidor de acciones a filtrarlo y mezcla metadatos con acciones. Límite conocido: una bitácora con comentarios no la lee el lector de la Parte I; las de la Parte I siguen leyéndose. Una prueba debe verificar que el replay conserva los números de línea físicos en sus mensajes de problema.

### Mediciones `--bench`

El subsistema nuevo `niebla_rutas` se seleccionará con este comando exacto:

```powershell
py -m cripta --bench --solo niebla_rutas --escala 1
```

La carga mide sin red ni vista:

1. **Referencia**: mapa conocido completo de la cripta de referencia, elegida como la de mayor total de salas del listado de fixtures sin fijar su id en el código, orígenes/destinos válidos y costo de cada cálculo del primer paso. Informa número de salas/salidas leído del fixture, mediana y máximo, y cumplimiento de 5 ms. El reloj de pared se usa solo para medir, no afecta estado del juego.
2. **Alternativas de ruta**: búsqueda con `HeapMinimo` (elegida) frente a selección lineal manual (descartada), sobre el mismo grafo y las mismas consultas, con semilla fija y `random.Random(semilla)` propio. Comprueba que ambas dan el mismo primer paso. También compara, sobre consultas idénticas, la ruta con costos guardados frente a consultar `CriptaMapa.costo_de_conexion`. La selección lineal se reporta aunque resulte más rápida en esta escala.
3. **Revelación**: varios R de salas nuevas sobre mapas de tamaños distintos, midiendo solo actualización; compara la ruta incremental con una pasada ingenua por todo el mapa, solo en el harness.
4. **Reversión**: registra y revierte cambios de antorcha y compara tiempo/número de inversas con copia completa del conocimiento como alternativa de medición, nunca de implementación.

La carga comprobará existencia, integridad y versión del fixture antes de medir. Toda cifra es hipótesis hasta ejecución; se reportarán mediana de corridas repetidas, unidades, entorno y semilla, sin inventar resultados previos.

### Límites conocidos

- El índice directo ocupa memoria hasta el mayor id, no solo hasta el número de salas, si los identificadores son dispersos.
- Dijkstra se recalcula en cada paso por requisito; un viaje largo repite búsquedas.
- La relajación de aristas se duplica respecto de la búsqueda del cazador; se acepta por las diferencias de interfaz descritas en la decisión.
- Esta capacidad y la 001 modifican `partida.py`, `efectos.py`, `cargas_bench.py`, `servicio_bench.py`, `heap_min.py` y `tests/infraestructura/test_partida_log.py`. La 001 debe fusionarse primero y esta rama traer `main` con merge antes de implementar. La 001 también cambia `SalidaVista` (costo), `EnemigoVista` (`es_cazador`), `Partida.vista()` y `_paneles_izquierdos`; con niebla esos datos deben salir del conocimiento. En esta rama los cambios aún están previstos por la 001, no implementados.
- El umbral de 5 ms depende del equipo y del mapa real de referencia; cada informe debe indicar entorno.
- Esta capacidad define los campos lógicos del conocimiento y su proyección. La 004 es dueña del formato binario y su versión y hará un solo cambio de versión; esta capacidad no controla checkpoints ni migración. El criterio de cripta de referencia (mayor total de salas o constante `CRIPTA_REFERENCIA` prevista por 001) se unificará con el grupo, sin decisión actual.

### Revisión de decisiones de la Parte I

| Decisión existente | Efecto potencial | Revisión |
|---|---|---|
| `Reversible` y `HistorialRetroceso` registran inversas puntuales | Una entrada con antorcha puede cambiar varias celdas | Mantener el mecanismo, añadir inversas por celda y medir registro/reversión frente a copia completa. |
| `CriptaMapa` usa `VectorOrdenado` por id y conoce el esqueleto completo | Vista y ruta no pueden usar ese mapa completo como conocimiento | Mantenerlo como estructura interna; interponer `ConocimientoJugador`. |
| `ServicioPartida.ejecutar` registra acciones aceptadas | Viaje produce movimientos individuales y un comentario | Reutilizar acciones; extender log/replay al comentario único y probar que no aparecen turnos enemigos. |
| Vista solo se construye en modo interactivo | Mapa conocido requiere presentación | Mantener creación condicional; replay y bench operan sin vista. |
| Persistencia P1 guarda el estado actual | Conocimiento pasa a ser estado consultable y persistente | Ampliación coordinada con 004; probar ida/vuelta y compatibilidad de pruebas P1. |

## Impacto en código existente

Las etiquetas describen esta rama, no el estado futuro. Las rutas **Nuevo** son destinos propuestos que se verificó que aún no existen. `BuscadorRutas` está **previsto por la 001** según su plan, no se presenta como código existente.

| Ruta | Estado | Impacto |
|---|---|---|
| `cripta/modelo/conocimiento_jugador.py` | Nuevo | Estado sala/puerta, consultas, revelación, observación e inversas. |
| `cripta/modelo/partida.py` | Modificado / previsto por 001 | Propiedad del conocimiento, inicialización, entradas/efectos y propuesta del siguiente paso; `Partida.vista()` se basa en conocimiento. |
| `cripta/modelo/resultado_partida.py` | Modificado / previsto por 001 | Proyección inmutable; `SalidaVista` (costo) y `EnemigoVista` (`es_cazador`) se integran con datos del conocimiento. |
| `cripta/modelo/persistencia_modelo.py` | Modificado | Proyectar/restaurar niveles y observaciones como datos planos. |
| `cripta/modelo/efectos.py` | Modificado | Avisar de cierres automáticos observables desde una sala vecina. |
| `cripta/modelo/cripta_mapa.py` | Sin cambios | Mantener representación real completa y costos; conocimiento es otra proyección. |
| `cripta/modelo/reversible.py` | Sin cambios | Reutilizar `_registrar_inversa` existente. |
| `cripta/modelo/historial_retroceso.py` | Sin cambios | Reutilizar `registrar_cambio`, LIFO e intervalos por acción. |
| `cripta/controlador/controlador_cripta.py` | Modificado | Órdenes de mapa/viaje, bucle por acciones ordinarias, llamada única al método de comentario antes del primer paso con ruta y motivo final. |
| `cripta/vista/vista_base.py` | Modificado | Contrato de presentación de mapa conocido y detención. |
| `cripta/vista/vista_consola.py` | Modificado / previsto por 001 | Comando de mapa, estados visibles y motivo; `_paneles_izquierdos` muestra datos derivados del conocimiento. |
| `cripta/servicios/servicio_partida.py` | Modificado | Método para registrar el comentario único de viaje y registro de movimientos individuales. |
| `cripta/infraestructura/partida_log.py` | Modificado | Comentario compatible con lectura/replay. |
| `cripta/servicios/servicio_replay.py` | Modificado | Omitir comentario de depuración y reproducir acciones. |
| `cripta/infraestructura/estado_guardado.py` | Modificado, coordinar 004 | Campo lógico para conocimiento; no define codificación binaria. |
| `cripta/infraestructura/guardado_binario.py` | Depende de 004 | La 004 incorpora la proyección al formato binario y realiza el único cambio de versión. |
| `cripta/bench/cargas_bench.py` | Modificado | Cargas de ruta, revelación y reversión con alternativas. |
| `cripta/servicios/servicio_bench.py` | Modificado | Registrar `niebla_rutas`; seguir sin vista. |
| `cripta/modelo/buscador_rutas.py` | Sin cambios (previsto por la 001) | No está en esta rama. No se reutiliza ni se modifica; ver la decisión de búsqueda. |
| `cripta/modelo/ruta_conocida.py` | Nuevo | Búsqueda de costo mínimo sobre el subgrafo conocido, con `HeapMinimo`, y primer paso con desempate por menor id. |
| `cripta/estructuras/heap_min.py` | Modificado por la 001 | La 001 añade `esta_vacio` y `__len__`; esta capacidad solo lo usa. |
| `tests/modelo/test_conocimiento_jugador.py` | Nuevo | Estados, puertas, antorcha, cierres y reversión con FR citados. |
| `tests/modelo/test_ir_a.py` | Nuevo | Ruta mínima, desempate, recálculo, detenciones y acciones normales. |
| `tests/controlador/test_controlador_cripta.py` | Modificado | Órdenes, motivos y no continuación tras pergamino. |
| `tests/infraestructura/test_partida_log.py` | Modificado | Comentario único, movimientos individuales y ausencia de turnos enemigos. |
| `tests/servicios/test_servicio_partida_guardado.py` | Modificado | Conservación de conocimiento, coordinada con 004. |
| `tests/vista/test_vista_consola.py` | Modificado | Presentación del mapa conocido y motivos de detención. |
| `tests/servicios/test_servicio_bench.py` | Nuevo | Equivalencia de resultados entre algoritmos y alternativas de revelación/reversión. |
| `tests/aceptacion/__init__.py` | Nuevo si falta | Paquete requerido para discover unittest. |
| `tests/aceptacion/test_niebla_ir_a.py` | Nuevo | Casos del Apéndice B y SC con FR citados. |

Las rutas existentes citadas se comprobaron en esta rama. Los destinos nuevos están marcados y no se presentan como archivos presentes.

## Trazabilidad requisito → componente → medición/prueba

Las rutas de pruebas de la tabla son propuestas futuras. Cada prueba citará los requisitos que cubre. `B-NIE-*` nombra los casos de niebla e «ir a» del Apéndice B de la Parte II.

| Requisito/caso | Componente | Medición o prueba prevista |
|---|---|---|
| FR-NIE-001 | `ConocimientoJugador`, `Partida` | Inicio explorado y estados válidos; `tests/modelo/test_conocimiento_jugador.py` (Nuevo). |
| FR-NIE-002 | Conocimiento y esqueleto/costo | Entrada revela nombre, salidas, costo y puertas. |
| FR-NIE-003 | Revelación de adyacencias | Avistada y desconocidas correctas; SC-NIE-001; `tests/modelo/test_conocimiento_jugador.py` (Nuevo). |
| FR-NIE-004 | Estado por puerta | Última observación sobrevive a cambio real; consulta O(1). |
| FR-NIE-005 | Entrada con antorcha | B-NIE-004; vecinas sin contenido ni activación; `tests/aceptacion/test_niebla_ir_a.py` (Nuevo). |
| FR-NIE-006 | Estado de partida/restauración/inversas | Guardado, carga, pergamino e historia con 004; SC-NIE-005. |
| FR-NIE-007 | Controlador/vista | Consulta sin tiempo/log/retroceso y sin filtración; SC-NIE-001; `tests/controlador/test_controlador_cripta.py` (Modificado), `tests/vista/test_vista_consola.py` (Modificado). |
| FR-NIE-008 | Proyección y proveedor de ruta | Solo conocimiento consultado; SC-NIE-001/002. |
| FR-NIE-009 | Validación del destino | No explorado/no existe, cero efectos; B-NIE-001; SC-NIE-002. |
| FR-NIE-010 | Dijkstra conocido | Costo, puerta no observada y empate por id; SC-NIE-002; bench. |
| FR-NIE-011 | Bucle y acción normal | Tiempo/eventos entre pasos; SC-NIE-003. |
| FR-NIE-012 | Recálculo previo | Ruta cambia tras observar puerta; SC-NIE-002/003. |
| FR-NIE-013 | Resultado del viaje | Motivos, prioridad y fin; B-NIE-003; SC-NIE-003; `tests/controlador/test_controlador_cripta.py` (Modificado), `tests/vista/test_vista_consola.py` (Modificado). |
| FR-NIE-014 | Proveedor de vecinos | No abre puerta aunque posea llave; SC-NIE-002. |
| FR-NIE-015 | Observación y cierre | B-NIE-002; actualización vecina y parada sin tiempo extra. |
| FR-NIE-016 | Servicio/`partida.log` | Comentario antes del primer paso, una vez; acciones separadas. |
| FR-NIE-017 | Pergamino y fin del bucle | B-NIE-006; revierte último paso y no reanuda. |
| FR-NIE-018 | `niebla_rutas` | Comando de bench en mapa completo; <5 ms por cálculo; corrección de alternativas en `tests/servicios/test_servicio_bench.py` (Nuevo). |
| FR-NIE-019 | Origen igual a destino | Cero tiempo, log, paso e historial; SC-NIE-002/003. |
| FR-NIE-020 | Parada tras entrada | Permite primer paso y para al entrar con enemigos vivos. |
| FR-NIE-021 | Búsqueda inicial | Sin ruta, sin paso/tiempo/log/historial; SC-NIE-002/003. |
| FR-NIE-022 | Estado antorcha/conocimiento | Apagar conserva salas/puertas; SC-NIE-001/005. |
| FR-NIE-023 | Activación de antorcha | Encender en sitio no revela hasta entrada; SC-NIE-001. |
| FR-NIE-024 | Inversas de revelación | B-NIE-005; celdas regresan al estado anterior; SC-NIE-005. |
| FR-NIE-025 | Salida sin puerta cerrable | Escenario 3.18 (decisión del grupo); abierta al explorar la sala. |
| SC-NIE-001 | Modelo y vista | Casos de estados y ocultamiento, FR-001–008/022/023; `tests/modelo/test_conocimiento_jugador.py` (Nuevo), `tests/vista/test_vista_consola.py` (Modificado), `tests/aceptacion/test_niebla_ir_a.py` (Nuevo). |
| SC-NIE-002 | Ruta y validación | FR-009/010/012/014/019/021 y `niebla_rutas`; `tests/modelo/test_ir_a.py` (Nuevo), `tests/servicios/test_servicio_bench.py` (Nuevo). |
| SC-NIE-003 | Bucle/resultado/servicio | FR-011/013/015/016/017/020 y aceptación integrada; `tests/controlador/test_controlador_cripta.py` (Modificado), `tests/vista/test_vista_consola.py` (Modificado), `tests/aceptacion/test_niebla_ir_a.py` (Nuevo). |
| SC-NIE-004 | Búsqueda | Bench exacto, fixture completo y límite <5 ms; corrección de alternativas en `tests/servicios/test_servicio_bench.py` (Nuevo). |
| SC-NIE-005 | Persistencia/inversas/historia | Integración 004; guardar/cargar/pergamino/historia; `tests/servicios/test_servicio_partida_guardado.py` (Modificado), `tests/aceptacion/test_niebla_ir_a.py` (Nuevo). |
| B-NIE-001: destino no explorado | Controlador/modelo | Cero tiempo y sin registro (FR-NIE-009). |
| B-NIE-002: puerta recordada abierta pero cerrada real | Evento/conocimiento/viaje | Observación desde vecina, recálculo y parada (FR-NIE-015). |
| B-NIE-003: entrada con enemigos dormidos | Bucle/activación | Activación normal y detención tras paso (FR-NIE-013). |
| B-NIE-004: antorcha sin activar contenido | Conocimiento/entrada | Vecinas exploradas, contenido intacto (FR-NIE-005). |
| B-NIE-005: pergamino revierte antorcha | Inversas/conocimiento | Estados de sala/puerta restaurados (FR-NIE-024). |
| B-NIE-006: pergamino durante viaje | Controlador/retroceso | Solo último paso y bucle terminado (FR-NIE-017). |

## Estructura elegida

Se mantiene el proyecto único: reglas en `cripta/modelo/`, orquestación en `cripta/controlador/` y `cripta/servicios/`, presentación en `cripta/vista/`, adaptadores en `cripta/infraestructura/`, cargas en `cripta/bench/` y pruebas paralelas en `tests/`. No se crea una capa de interfaz nueva ni se modifica estructura fuera de esta capacidad.

Árbol de las pruebas afectadas:

```text
tests/
├── controlador/
│   └── test_controlador_cripta.py (Modificado)
├── infraestructura/
│   └── test_partida_log.py (Modificado)
├── modelo/
│   ├── test_conocimiento_jugador.py (Nuevo)
│   └── test_ir_a.py (Nuevo)
├── servicios/
│   ├── test_servicio_bench.py (Nuevo)
│   └── test_servicio_partida_guardado.py (Modificado)
├── vista/
│   └── test_vista_consola.py (Modificado)
└── aceptacion/
    ├── __init__.py (Nuevo si falta)
    └── test_niebla_ir_a.py (Nuevo)
```

## Revisión de constitución posterior al diseño

El diseño cumple prohibiciones de estructuras, determinismo, MVC, idioma, errores y reversibilidad sin copia completa por acción. No queda una regla normativa necesaria fuera de `spec.md`. El guardado queda expresamente coordinado con 004 y no se define su formato. Las hipótesis de rendimiento solo se aceptan tras las mediciones indicadas.

La implementación deberá mantener compatible el conjunto de pruebas de Parte I, ejecutable con `py -m unittest discover -s tests -t .`; esta planificación no lo ejecutó.
