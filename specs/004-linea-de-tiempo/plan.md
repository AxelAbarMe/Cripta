# Plan de implementación: Línea de tiempo

**Rama**: `004-linea-de-tiempo` | **Fecha**: 2026-11-16 | **Especificación**: [spec.md](spec.md)

**Entrada**: Especificación de funcionalidad en `specs/004-linea-de-tiempo/spec.md`.

## Resumen

La capacidad permite consultar una partida vigente por tiempo virtual o por número de acción, reproducir una bitácora hasta un instante, y conservar el historial al guardar. Se propone registrar acciones del jugador y datos de cambio serializables entre puntos de control completos, con un punto como máximo cada K acciones. La consulta parte del punto de control más cercano y re-simula como máximo K acciones en una instancia de reconstrucción aislada. El formato binario pasa a una versión nueva. Las acciones revertidas por pergamino recortan el registro al límite de la acción conservada y descartan los puntos de control posteriores.

La decisión de re-simular se apoya en que `Partida._guardar_contadores` hoy registra closures y un estado RNG por acción, mientras que `persistencia_modelo.crear_estado` ya produce datos planos completos. No se reutilizarán las inversas de retroceso como registro histórico. Los valores de K y el rendimiento son hipótesis hasta medirlos.

## Contexto técnico

**Lenguaje y versión**: Python 3.11 o superior.

**Dependencias principales**: biblioteca estándar; estructuras propias existentes en `cripta/estructuras/`; sin nuevas dependencias externas.

**Almacenamiento**: `partida.sav` binario, con nueva versión; `partida.log` como fuente de las acciones aceptadas.

**Pruebas**: `unittest` bajo `tests/`, con carpetas paralelas a `cripta/` y cada prueba citando FR cubiertos.

**Plataforma**: CLI de Windows y otros entornos con Python 3.11+.

**Tipo de proyecto**: juego de consola MVC con modo replay y benchmarks sin vista interactiva.

**Objetivos de rendimiento**: consulta <50 ms en una partida de al menos 5 000 acciones con K predeterminado medido (FR-LIN-018); máximo K acciones reconstruidas por consulta (FR-LIN-015).

**Restricciones**: sin `heapq`, `bisect`, `collections`, `networkx`, bibliotecas de grafos, `dict` o `set` como índice/caché, ni `list.sort()`/`sorted()` en problemas evaluados. Sin I/O, red o vista en el modelo. Determinismo con `random.Random(semilla)` propio. No fijar K por conjetura.

**Escala y alcance**: historial de al menos 5 000 acciones; mapas obtenidos del fixture con mayor cantidad total de salas, seleccionado dinámicamente sin fijar su id. El benchmark sintético se genera con semilla propia.

## Comprobación de constitución

| Regla | Resultado previo al diseño |
|---|---|
| Estructuras implementadas a mano y prohibiciones de índices | Cumple: se usan listas por posición y búsqueda binaria manual; el diseño no usa tabla hash. |
| Determinismo | Cumple: checkpoints incluyen RNG; semilla local reproducible en bench. |
| MVC y modos sin vista | Cumple: reconstrucción en modelo/servicio; replay y bench no construyen la vista interactiva. |
| Sin datos de cripta concreta | Cumple: fixture mayor se detecta contando salas, sin id fijo. |
| Pruebas y trazabilidad FR | Cumple en diseño: árbol propuesto abajo y matriz FR → componente → medición/prueba. |
| Especificación precede a implementación | Cumple: este plan se apoya en `spec.md`; no crea tareas ni código. |
| Compatibilidad P1 | Condicionado: formato nuevo rechaza versión P1; se deben mantener las pruebas P1. Pergamino sigue con inversas puntuales. |

**Puerta previa**: sin violaciones conocidas. La semántica de evento en empate se toma del código y D.3: orden ascendente por `(tiempo, secuencia)`; reprogramar asigna secuencia nueva. Las decisiones de juego (semántica de t/#k, corte del replay, pergamino y K inválido) están explicitadas en la especificación y sus aclaraciones.

## Diseño

### Problemas, frecuencia y alternativas

| Problema y frecuencia esperada | Alternativa A | Alternativa B | Decisión y descarte concreto |
|---|---|---|---|
| Registrar acciones y consultar por `#k` (una inserción por acción; consultas ocasionales) | Lista de acciones aceptadas y posición de línea vigente | Reusar `partida.log` como único registro | A: registro interno indexable por posición y serializable junto al guardado. Se descarta B como única fuente porque la bitácora se puede copiar, truncar o marcar parcial y además no guarda checkpoints/estado derivado de la partida. |
| Crear checkpoint (cada K acciones) y localizar el anterior (una búsqueda por consulta) | Lista secuencial de checkpoints con búsqueda binaria manual por número de acción | Recorrer checkpoints desde el inicio | A: O(log C) localización, almacenamiento contiguo. Se descarta B porque crece linealmente con C por consulta; se medirá como alternativa. No se usa `bisect`. |
| Reconstruir estado (hasta una consulta por orden explícita) | Re-simular acciones desde checkpoint cercano, con RNG restaurado | Invertir cambios hasta t/#k usando registros de mutaciones | A: máximo K acciones (FR-LIN-015) y reutiliza la semántica real de acciones/eventos; almacena acciones más checkpoints, no estados por acción. B se medirá como alternativa, pero se descarta como estrategia principal porque requiere un tipo de cambio explícito para cada mutación del modelo y coordinarlo con todas las capacidades. El historial P1 son closures no serializables y solo cubre cinco intervalos. |
| Ejecutar consulta sin alterar la partida (pocas consultas frente a muchos turnos) | Reconstrucción en un contexto/Partida aislado desde el checkpoint | Mutar temporalmente la partida activa y restaurar un snapshot en `finally` | A: aislamiento evita efectos sobre bitácora, mensajes, historial de pergamino y estado actual. Se descarta B porque un fallo intermedio puede dejar recursos auxiliares o efectos laterales inconsistentes. |
| Pergamino recorta la historia (hasta cinco intervalos por uso) | Truncar registro por longitud de acción vigente y quitar checkpoints posteriores | Buscar y filtrar cada registro por tiempo | A: O(C) por checkpoints descartados, sin escanear todas las acciones; la longitud delimita la línea vigente. Se descarta B porque su costo crece con toda la historia y puede conservar estados de la rama revertida. |
| Persistir la historia (al guardar/cargar) | Extender el formato binario versionado actual | Crear un archivo lateral de historia separado | A: una transacción lógica y detección existente de magic/versión; sube `FORMATO_VERSION`. Se descarta B porque podría desincronizarse de `partida.sav` y no cumple conservarlo como un único guardado completo. |

### Registro de historia y reconstrucción

Se agregará un registro de línea vigente compuesto por acciones de jugador aceptadas y puntos de control. No se contarán órdenes rechazadas, comentarios, consultas ni turnos de enemigo, según FR-LIN-003 y FR-LIN-020. El estado inmediatamente anterior a acción k se obtiene desde el checkpoint previo más cercano y se aplican las acciones previas necesarias. Para una consulta temporal se reconstruye el mismo prefijo hasta el límite temporal, incluyendo eventos según la regla de FR-LIN-001/002.

La agenda desempata por `(tiempo, secuencia)` en `cripta/modelo/reloj.py::EventoProgramado.__lt__` y `RelojEventos.ejecutar_siguiente`; el reloj se mueve al tiempo del evento antes de ejecutar su acción. Una reprogramación recibe secuencia nueva (`RelojEventos.reprogramar`). La reproducción histórica debe detenerse en el punto de decisión del jugador: ejecutará todos los eventos anteriores en ese orden, aplicando en t los que la agenda procesa antes de dejar el turno al jugador. Si no existe decisión en t, agotará todos los eventos con tiempo `<= t`.

Los checkpoints se crearán como máximo tras cada múltiplo de K acciones de jugador; K se pasa desde `--checkpoint-cada K`. Se conservará la acción ejecutada y el estado completo del checkpoint en datos planos. Si re-simular requiere solo acciones, no se duplicarán snapshots ni por acción ni por sala. `EstadoRNG` serializa el estado para que el checkpoint reanude la misma secuencia aleatoria.

Para no tocar la partida activa, la consulta utilizará una instancia reconstruida con su agenda, estado del jugador, salas cargadas, objetos, efectos y conocimiento. El adaptador de reconstrucción se inyecta con los datos del checkpoint y las acciones posteriores. No realizará solicitudes de red; no se consultarán ubicaciones ausentes de los datos guardados. La integración deberá confirmar que el estado de la capacidad 002 está disponible en todos los checkpoints. Si el resultado exige datos de catálogo, se resolverán mediante el catálogo ya cargado en el servicio, fuera del modelo puro.

Al aceptar un pergamino, el registro se truncará en la posición del intervalo que se deshizo, eliminando acciones posteriores y checkpoints ubicados después de ese límite. El checkpoint previo retenido será el punto base de la rama vigente. Esta operación no iterará las acciones descartadas; una secuencia/lista contigua se podrá truncar desde el final.

### Rendimiento y benchmark

El subsistema de benchmark nuevo es `linea_tiempo`; comando exacto:

```powershell
py -m cripta --bench --solo linea_tiempo --escala 1
```

La carga usará una `random.Random(semilla)` local, una partida sintética determinista de al menos 5 000 acciones, y una cripta de referencia obtenida dinámicamente del fixture con más salas. No codificará ids ni datos de cripta. Reportará entorno, semilla, acciones, salas y salidas contadas, K, memoria estimada de acciones/checkpoints/cambios, mediana y máximo de consulta, y cumplimiento de 50 ms.

Comparaciones obligatorias:

1. K=100, K=500, K=1000 y sin checkpoints; reportar memoria y consulta para cada uno. Son valores experimentales del benchmark, no valores predeterminados del producto.
2. Re-simular desde checkpoint frente a reconstruir hacia atrás con cambios serializables, midiendo costo de registrar, memoria y consultas equivalentes. La alternativa de inversión se implementará solo dentro de la carga comparativa si se decide descartarla, sin convertir el historial de pergamino a copias completas.
3. Búsqueda binaria manual frente a búsqueda lineal del checkpoint previo.
4. Recorte por truncamiento desde el final frente a escaneo y filtrado (alternativa descartada), midiendo cantidad de registros procesados.
5. Como insumo separado, se citará el benchmark de `--bench --solo historial` de la 001 cuando el grupo informe sus mediciones de cazadores. El plan de 001 requiere reportarlo, pero no hay cifras disponibles aquí.

No se anotan cifras de rendimiento hasta ejecutar la carga. El grupo escogerá el K predeterminado a partir de las mediciones y verificará el umbral <50 ms para ese valor.

### Impacto en el código existente

Los estados describen la rama actual. «Nuevo» identifica una ruta ausente comprobada; «Modificado» una ruta presente. El plan no afirma que código previsto por 001/002 ya esté integrado.

| Ruta | Estado | Impacto previsto |
|---|---|---|
| `cripta/modelo/linea_tiempo.py` | Nuevo | Registro de acciones/checkpoints, corte por línea vigente y reconstrucción temporal por servicio de modelo aislado. |
| `cripta/modelo/partida.py` | Modificado | Notificar acciones confirmadas y pergamino al registro; proyección de estado histórico sin cambiar el estado vivo. Zona compartida con 001 y 002. |
| `cripta/modelo/reloj.py` | Sin cambios | Reutilizar y documentar el orden `(tiempo, secuencia)`; no cambiar semántica de agenda. |
| `cripta/modelo/persistencia_modelo.py` | Modificado | Crear/restaurar estado completo de checkpoint con RNG y campos declarados por 002. |
| `cripta/infraestructura/estado_guardado.py` | Modificado | Tipos planos para checkpoint, acciones/eventos de historia y conocimiento declarado por 002. |
| `cripta/infraestructura/guardado_binario.py` | Modificado | Nueva versión binaria, serialización/deserialización de línea y checkpoints; rechazo explícito de versión P1. |
| `cripta/infraestructura/partida_log.py` | Sin cambios | Formato append-only ya registra acciones aceptadas; los comentarios, cuando 002 se integre, no se numeran. |
| `cripta/servicios/servicio_partida.py` | Modificado | Configuración K, creación/checkpoint, coordinación de guardado/carga y proveedor de reconstrucción aislada. |
| `cripta/servicios/servicio_replay.py` | Modificado | Corte `hasta`, mismo resumen que historia y detección de final anterior; hoy reproduce todo el log. |
| `cripta/__main__.py` | Modificado | Flags `--checkpoint-cada` y `--hasta`; replay/bench sin vista. |
| `cripta/controlador/controlador_cripta.py` | Modificado | Interpretar `historia <t>` y `historia #k`, presentar rechazo o resumen. Depende de 002 para vista del conocimiento. |
| `cripta/vista/vista_base.py` | Modificado | Contrato de presentación de resumen histórico. |
| `cripta/vista/vista_consola.py` | Modificado | Sintaxis y salida de consulta histórica. |
| `cripta/bench/cargas_bench.py` | Modificado | Carga `linea_tiempo` con K y alternativas requeridas. |
| `cripta/servicios/servicio_bench.py` | Modificado | Registrar y ejecutar `linea_tiempo` sin vista. |
| `cripta/modelo/historial_retroceso.py` | Sin cambios | Mantener closures y máximo cinco intervalos; la línea histórica tiene un registro aparte. |
| `cripta/modelo/reversible.py` | Sin cambios | Las closures siguen dedicadas al pergamino y no se persisten. |
| `tests/modelo/test_linea_tiempo.py` | Nuevo | Límites temporales, #k, checkpoint, RNG, truncamiento y consulta aislada; cada prueba cita FR. |
| `tests/modelo/test_partida_linea_tiempo.py` | Nuevo | Gancho de acción, eventos empatados y pergamino, con FR citado. |
| `tests/infraestructura/test_guardado_binario.py` | Modificado | Round-trip de historia y rechazo de versión P1, con FR citado. |
| `tests/servicios/test_servicio_replay.py` | Modificado | `--hasta`, resumen equivalente y final anticipado, con FR citado. |
| `tests/servicios/test_servicio_partida_guardado.py` | Modificado | Línea completa tras guardar/cargar y estados de 002, con FR citado. |
| `tests/controlador/test_controlador_cripta.py` | Modificado | Comando historia válido/inválido y salida. |
| `tests/vista/test_vista_consola.py` | Modificado | Presentación de siete grupos de estado histórico. |
| `tests/servicios/test_servicio_bench.py` | Nuevo | Correctitud de comparaciones; semilla reproducible y modo sin vista. |
| `tests/aceptacion/__init__.py` | Nuevo si falta | Paquete unittest. |
| `tests/aceptacion/test_linea_tiempo.py` | Nuevo | Seis casos B-LIN y criterios SC con FR explícitos. |

### Coordinación con otras capacidades

- **Depende de 001** para los cambios aún no fusionados que esa capacidad haga en `Partida` y su carga `--bench --solo historial`. La 001 no modifica el formato binario; la 004 conserva la propiedad de versión. No se atribuye a 001 medición no recibida.
- **Depende de 002** para el estado de conocimiento por sala y puertas. Sus datos se incluyen en `EstadoPartida`, checkpoints y formato binario; la consulta presenta el mapa conocido reconstruido en el instante t. La 002 declara el estado, pero esta capacidad conserva la responsabilidad sobre versión y codificación.
- Los planes de 001 y 002 fueron consultados en las fuentes pedidas; no se leyó ni modificó 003.

### Contratos

Los contratos de CLI quedan en [contracts/cli.md](contracts/cli.md). No hay una API de red nueva. Los contratos internos entre modelo, controlador y almacenamiento se describen como proyecciones de datos planos y están sujetos a los campos que declaren las capacidades integradas.

### Árbol de pruebas afectadas

```text
tests/
├── aceptacion/
│   ├── __init__.py (Nuevo si falta)
│   └── test_linea_tiempo.py (Nuevo)
├── controlador/
│   └── test_controlador_cripta.py (Modificado)
├── infraestructura/
│   └── test_guardado_binario.py (Modificado)
├── modelo/
│   ├── test_linea_tiempo.py (Nuevo)
│   └── test_partida_linea_tiempo.py (Nuevo)
├── servicios/
│   ├── test_servicio_bench.py (Nuevo)
│   ├── test_servicio_partida_guardado.py (Modificado)
│   └── test_servicio_replay.py (Modificado)
└── vista/
    └── test_vista_consola.py (Modificado)
```

### Trazabilidad requisito → componente → medición/prueba

| Requisito | Componente | Medición o prueba prevista |
|---|---|---|
| FR-LIN-001 | `linea_tiempo`, agenda | Evento en t sin decisión; caso B-LIN-003; prueba de orden. |
| FR-LIN-002 | `RelojEventos`, reconstrucción | Empate por `(tiempo, secuencia)`; eventos antes/después de decisión; B-LIN-003. |
| FR-LIN-003 | Registro y controlador | `#k`, acciones aceptadas, rechazadas, comentarios y pasos «ir a»; B-LIN-002. |
| FR-LIN-004 | Proyección histórica y vista | Siete grupos de resumen; SC-LIN-001. |
| FR-LIN-005 | Contexto aislado | Comparar estado, reloj, log e historial antes/después; SC-LIN-002. |
| FR-LIN-006 | Validador temporal | t > reloj y límite tras pergamino; B-LIN-001/002. |
| FR-LIN-007 | Truncamiento | Pergamino elimina acciones/checkpoints posteriores sin recorrer la historia; B-LIN-002. |
| FR-LIN-008 | `ServicioReplay`, CLI | `--replay --hasta`; equivalencia con consulta; SC-LIN-005. |
| FR-LIN-009 | `ServicioReplay` | Log termina antes de t, muestra final y aviso; SC-LIN-005. |
| FR-LIN-010 | Guardado binario | Round-trip íntegro de línea/checkpoints; SC-LIN-006. |
| FR-LIN-011 | `GuardadoBinario` | Rechazo de versión antigua sin tocar archivo; B-LIN-006. |
| FR-LIN-012 | Carga/CLI | No ofrecer ruta de migración; B-LIN-006. |
| FR-LIN-013 | `Partida`, configuración | No más de un checkpoint cada K acciones; probar K=1 y K>N. |
| FR-LIN-014 | `--bench linea_tiempo` | Comparar K=100/500/1000 y sin checkpoints; justificar default con resultados del grupo. |
| FR-LIN-015 | Localización/reconstrucción | Contar máximo K acciones aplicadas/deshechas; benchmark a 5 000 acciones. |
| FR-LIN-016 | Registro/checkpoints | Memoria acciones+cambios+checkpoints, sin snapshot por acción; SC-LIN-004. |
| FR-LIN-017 | `EstadoRNG` | Checkpoint restaura estado aleatorio y reproduce mismas decisiones; B-LIN-003. |
| FR-LIN-018 | Benchmark `linea_tiempo` | Comando exacto, <50 ms al K predeterminado; SC-LIN-003. |
| FR-LIN-019 | Integración 002 | Comparar conocimiento en instante histórico; SC-LIN-001/006. Depende de 002. |
| FR-LIN-020 | Registro y comentario de viaje | Cada movimiento confirmado incrementa número; comentario excluido; B-LIN-002. Depende de 002. |
| FR-LIN-021 | `EstadoPartida`, binario | Round-trip de campos declarados por capacidades; SC-LIN-006. |
| FR-LIN-022 | Parser CLI | Cero, negativo y texto rechazan inicio sin iniciar partida. |
| FR-LIN-023 | Controlador | Errores de t/#k/sintaxis sin efectos; SC-LIN-007. |
| SC-LIN-001 | Proyección/vista | Verificar los siete grupos mínimos en consultas válidas. |
| SC-LIN-002 | Contexto aislado | Snapshot observable del estado/log/retroceso sin cambios tras consulta. |
| SC-LIN-003 | Bench | 5 000+ acciones y default medido bajo 50 ms. |
| SC-LIN-004 | Registro | Medición de memoria versus acciones y checkpoints; incluir sin checkpoint. |
| SC-LIN-005 | Replay | Comparar resumen con historia y final anticipado. |
| SC-LIN-006 | Persistencia/conocimiento | Guardar/cargar, formato viejo y mapa 002. |
| SC-LIN-007 | Validación | K e historia rechazados informan motivo y no afectan estado. |
| B-LIN-001: t mayor que el reloj | Validador temporal | Rechazar sin cambio del estado/reloj/log/retroceso (FR-LIN-006/023). |
| B-LIN-002: pergamino | Truncamiento | Línea y #k solo contienen acciones vigentes; corte sin escaneo (FR-LIN-007/020). |
| B-LIN-003: varios eventos en el mismo t | Agenda | Confirmar `(tiempo, secuencia)` y el límite predecisión (FR-LIN-001/002/017). |
| B-LIN-004: consulta sin efectos | Contexto aislado | Estado actual, reloj, log e historial permanecen iguales (FR-LIN-005). |
| B-LIN-005: `--hasta` posterior al final | Replay | Mostrar estado final e indicar fin anterior a t (FR-LIN-008/009). |
| B-LIN-006: archivo de la Parte I | Formato binario | Rechazo por versión, archivo intacto, sin migración (FR-LIN-011/012). |

## Revisión de decisiones de la Parte I

| Decisión P1 | Evidencia verificada | Riesgo/cambio para 004 | Acción y medición |
|---|---|---|---|
| Agenda con `HeapMinimo` y orden `(tiempo, secuencia)` | `EventoProgramado.__lt__`, `RelojEventos.ejecutar_siguiente`, `reprogramar` | FR-LIN-002 exige el mismo orden al reconstruir; cambiarlo rompería resultados | Mantener agenda; medir ciclo de eventos de partida cargada y verificar empate con B-LIN-003. |
| Historial de retroceso con closures, hasta cinco intervalos | `reversible.py`, `historial_retroceso.py` | No es serializable ni consultable; closures y estado RNG se guardan por acción; muchos cazadores pueden elevar costo por intervalo | Mantener separado. Bench `linea_tiempo` compara registro/reconstrucción contra cambio serializable; informar resultado de `--bench --solo historial` de 001 cuando exista, sin inventar cifra. |
| `Partida._guardar_contadores` guarda `getstate()` por acción | `cripta/modelo/partida.py` | El estado RNG de 625 enteros por intervalo no debe replicarse en cada acción histórica | Conservar RNG en cada checkpoint completo y medir memoria frente a K. |
| `partida.log` registra una línea JSON por acción aceptada; turnos enemigos no se registran | `cripta/infraestructura/partida_log.py`, `servicio_partida.py` | Fuente de orden de acciones, pero insuficiente como único historial persistente y puede tener comentarios al integrarse 002 | Mantener log operativo; registrar comentarios fuera de la numeración; comprobar round-trip de registro binario. |
| Replay reproduce todo el log y crea resultado sin vista interactiva | `ServicioReplay.reproducir`, `__main__._reproducir` | Falta corte temporal; resumen no debe crear vista | Añadir límite de simulación y salida de resumen puro; probar modo replay sin vista. |
| Guardado binario versión 1, valida magic/versión | `guardado_binario.py` | Debe guardar checkpoints y la línea; P1 incompatible | Subir versión y verificar rechazo P1 no destructivo, tamaño y tiempo de guardado/carga dentro del benchmark. |

El plan de 001 solicita `--bench --solo historial` con cazadores, pero no aporta resultados medidos en el artefacto leído. El dato queda como insumo pendiente de incorporar antes de cerrar las decisiones de implementación.

## Límites conocidos

- El registro de acciones permite reconstruir solo hasta el checkpoint más próximo; si las acciones entre checkpoints se almacenan como datos, deben conservar exactamente sus parámetros y orden.
- La reconstrucción depende del estado completo de capacidades integradas. El conocimiento de niebla no puede inferirse del mapa real; depende de los campos de 002.
- La historia consultable es una sola línea vigente: el pergamino descarta la rama revertida según FR-LIN-007.
- La frecuencia K predeterminada permanece abierta hasta contar con las mediciones del grupo. Los K experimentales no son configuración de producto anticipada.
- Guardar la historia aumenta tamaño y tiempo de E/S en proporción a acciones/cambios y checkpoints; este costo debe reportarse, no se fija un umbral que spec.md no exige.
- El benchmark de una máquina no demuestra el umbral en todos los equipos; el informe registra plataforma y versión de Python.
- Para t posterior al último evento o final, el límite de estado se define por la especificación y la condición terminal de la partida; el replay informa final anticipado cuando corresponda.

## Revisión posterior de constitución

El diseño mantiene estructuras propias, secuencias contiguas y búsqueda binaria manual. No introduce claves hash, dependencia externa ni datos fijos de una cripta. Los checkpoints contienen datos planos y RNG; el historial del pergamino conserva inversas por cambio. La consulta se aísla del modelo vivo y el replay/bench no requieren vista. Los errores de argumentos inválidos se modelan como `ValueError`; los archivos incompatibles siguen usando el error externo existente. Los resultados de rendimiento quedan pendientes de benchmark, sin cifras inventadas. No se observa una violación que requiera excepción o justificación de complejidad.
