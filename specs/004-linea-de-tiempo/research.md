# Investigación: línea de tiempo

## Registro consultable

**Decisión**: Mantener las acciones numeradas vigentes, ajustes de inventario y puntos de control en una línea de tiempo propia. `partida.log` conserva las líneas append-only de acciones revertidas y la línea del pergamino, mientras que la numeración `#k` se calcula sobre la secuencia vigente. #k se refiere solo a la línea vigente: las acciones revertidas dejan de tener número y k se rechaza si es cero o mayor que la cantidad de acciones vigentes. El pergamino no se numera; después del recorte, el siguiente número parte de la última acción vigente. No reutilizar el registro de closures del pergamino.

**Razón**: `cripta/modelo/reversible.py` registra closures de inversión. `cripta/modelo/historial_retroceso.py` conserva solo cinco intervalos y los ejecuta en LIFO; no representa tiempos ni se puede guardar como datos. `Partida._guardar_contadores` guarda además `random.Random.getstate()` en cada intervalo. El registro aparte permite consultar y persistir sin alterar el mecanismo de pergamino.

**Alternativas consideradas**: usar closures del historial (descartado por no ser consultable ni serializable y por su límite de cinco intervalos); emitir un registro plano de cada mutación (apto para invertir, pero exige cobertura explícita de cada campo y coordinación con 001/002). Se medirá esta segunda alternativa contra re-simulación antes de descartar su factibilidad.

## Reconstrucción de una consulta

**Decisión**: Partir del checkpoint más cercano anterior al objetivo y re-simular las acciones necesarias en un contexto aislado, con estado RNG restaurado y `HistorialRetroceso.sin_registrar()` activo. La reconstrucción no adjunta bitácora ni emite mensajes. Tomará el contenido estático (esqueleto, fichas, tipos de enemigos y trampas) de las salas ya materializadas en la partida viva o cargada, y aplicará encima solo el estado dinámico del checkpoint. La vía de restauración no llamará a `precarga.preparar_sala`; fixtures no serán fuente de estado de una partida y no habrá solicitudes de red ni consumo del presupuesto.

**Razón**: `cripta/modelo/persistencia_modelo.py::crear_estado` produce `EstadoPartida` con datos planos y `EstadoRNG`. Así se limita el trabajo a K acciones (FR-LIN-015) y la consulta no toca la partida activa (FR-LIN-005). La ruta vigente de `restaurar_sala` llama a `precarga.preparar_sala` por sala con contenido cargado, lo que implica E/S por consulta. La vía elegida reutiliza lo ya materializado y restaura el estado dinámico sin esa preparación.

**Alternativas consideradas**: reutilizar `restaurar_sala` tal cual (descartado por E/S, y posible red por consulta); guardar el contenido estático dentro de cada checkpoint (descartado por memoria); invertir mutaciones serializables hasta el objetivo (requiere cubrir todas las mutaciones del motor); reconstruir desde el inicio sin checkpoints (simple, pero no satisface el límite K). El benchmark `linea_tiempo` compara restauración actual y elegida, reconstrucción por inversión y caso sin checkpoints.

**Transición del pergamino e inventario**: Parte I no restaura el pergamino consumido ni devuelve al suelo el pergamino recogido en el intervalo revertido (`Partida._usar_pergamino`, `Inventario._deshacer_recoger`). Al aceptar el pergamino se anexa a la línea un ajuste con las instancias afectadas, en la posición del uso; no recibe número ni cuenta para K. La reconstrucción aplica el ajuste al llegar a esa posición. Si un pergamino posterior trunca por detrás de él, los ajustes se acumulan en el nuevo final de la línea para mantener el mismo inventario vivo. Se prueba que, tras usar un pergamino, `historia` del reloj actual coincide con el inventario de la partida viva (FR-LIN-005). `Inventario._no_reversibles` excluye el cursor, que pertenece a la interfaz: el resumen histórico no depende de su posición.

## Orden temporal

**Decisión**: Reproducir con el mismo orden determinista que la agenda existente y respetar el corte antes de la siguiente decisión del jugador.

**Razón**: `cripta/modelo/reloj.py::EventoProgramado.__lt__` compara `(tiempo, secuencia)`. `RelojEventos.ejecutar_siguiente` extrae el mínimo vigente, fija el reloj al tiempo del evento y ejecuta la acción. `reprogramar` crea un evento con secuencia nueva. D.3 del contexto confirma secuencia creciente como desempate. Este es el orden relevante para FR-LIN-002.

**Alternativas consideradas**: agrupar eventos solo por tiempo e ignorar la secuencia (descartado porque puede cambiar el estado observable); reproducir todas las acciones del mismo instante antes de devolver el control al jugador (descartado porque contradice el límite predecisión de FR-LIN-002).

## Localización y recorte

**Decisión**: Guardar checkpoints en una secuencia contigua ordenada por acción, localizar el previo con búsqueda binaria manual y recortar la línea vigente desde el final al aceptar pergamino. Se descartan exactamente los checkpoints cuyo número de acciones sea mayor que la longitud vigente después del recorte; el checkpoint en el borde se conserva. Para convertir t en límite de acción, usar búsqueda binaria manual sobre los instantes de acción ordenados no decrecientemente (O(log N)); búsqueda lineal queda descartada y se mide en el benchmark.

**Razón**: Los checkpoints se insertan en orden. La búsqueda binaria reduce la localización a O(log C); truncar la secuencia y quitar checkpoints posteriores evita recorrer el historial completo. Las operaciones son compatibles con el uso de `list` como almacenamiento contiguo y no requieren `bisect`, `dict` ni `set`.

**Alternativas consideradas**: escaneo lineal de checkpoints (más simple, O(C) por consulta); filtrar todos los registros por tiempo al usar pergamino (O(N), innecesario dado que la línea vigente tiene un límite de longitud).

**Medición y trazabilidad de t→acción**: ambas búsquedas recibirán los mismos límites ordenados y consultas deterministas; reportarán mediana, máximo y cantidad de límites inspeccionados. La binaria elegida es O(log N), la lineal O(N) y queda descartada por su crecimiento lineal. La regla FR-LIN-001/002 resuelve los empates temporales. Sin cifras previas. FR-LIN-001/002/006, SC-LIN-003; harness `linea_tiempo`.

## Persistencia y compatibilidad

**Decisión**: Extender `EstadoPartida` y el formato binario existente con el único cambio de versión del grupo, realizado por 004, y rechazar explícitamente archivos P1. Se incluyen los campos de conocimiento y su proyección definidos por 002, incluidos los costos conocidos de salida.

**Razón**: `cripta/infraestructura/guardado_binario.py` declara `FORMATO_VERSION = 1` y ya lanza `CriptaFormatoIncompatibleError` cuando magic o versión no coinciden. `EstadoPartida` y sus clases auxiliares son el canal de datos planos.

**Alternativas consideradas**: cargar P1 en silencio (prohibido por FR-LIN-011); ofrecer migración (prohibido por FR-LIN-012); guardar la línea en archivo lateral (puede desincronizarse del guardado principal y no cumple el guardado completo atómico a nivel lógico).

## Replay y CLI

**Decisión**: `--replay --hasta t` reproduce la bitácora completa para construir la misma línea vigente que la partida viva y consulta con el mismo componente que `historia <t>`. Limita t al reloj final e indica el final anticipado si t lo supera. Agregar el parámetro y los comandos/configuración de historia y checkpoints a la CLI, sin instanciar la vista interactiva en replay o bench.

**Razón**: `ServicioReplay.reproducir(ruta)` itera toda la bitácora y `cripta/__main__.py::_reproducir` imprime el resultado completo. La ruta de replay ya se ejecuta antes de crear `ControladorCripta` y `VistaConsola`.

**Alternativas consideradas**: detener la simulación al primer instante que llega a t (descartado porque el reloj retrocede con pergaminos y puede devolver acciones revertidas); filtrar o truncar el archivo log para simular un corte (descartado porque altera la fuente y no respeta eventos temporales); reutilizar la interfaz interactiva de la vista (descartado por separación MVC y ejecución sin vista).

## Mediciones requeridas

**Decisión**: No fijar cifras ni K predeterminado antes de medir. Ejecutar `py -m cripta --bench --solo linea_tiempo --escala 1` con K=100, 500, 1000 y sin checkpoints. Usar semilla explícita con `random.Random(semilla)` y escoger la cripta de referencia dinámicamente por mayor total de salas.

**Razón**: FR-LIN-014 deja el valor de K a la medición del grupo y FR-LIN-018 fija el objetivo de consulta. La tabla del plan enumera también la alternativa de cambios invertibles y la búsqueda lineal.

**Alternativas consideradas**: elegir K por intuición (sin evidencia y contrario a FR-LIN-014); fijar mediciones en documentación antes de ejecutar (no reproducible).

## Insumos de 001 y 002

- El plan de `specs/001-terreno-cazador/plan.md` indica que `--bench --solo historial` medirá el costo del historial de retroceso con muchos cazadores y que su resultado se informará a 004. El plan consultado no contiene cifras; por tanto no se atribuye ninguna.
- `specs/002-niebla-ir-a/plan.md` y `data-model.md` describen el conocimiento del jugador como estado de partida con nivel por sala y observaciones por salida, plano y reversible. La 004 debe guardar esos datos en checkpoints e incluirlos en las consultas históricas. La codificación y versión binaria corresponden a 004.
- La 002 decidió que los costos de salida forman parte de la proyección persistida. Se incluyen en checkpoints y en el cálculo de memoria del benchmark. Límite conocido: si la memoria resulta excesiva, podrían recalcularse desde el esqueleto.
- La 001 cambió `SalidaVista` (costo), `EnemigoVista` (`es_cazador`), `Partida.vista()` y `_paneles_izquierdos`; el resumen histórico presenta enemigos y vida mediante esas vistas (Depende de 001). El criterio de cripta de referencia (mayor total de salas o `CRIPTA_REFERENCIA`) queda pendiente de unificación con el grupo.
- `docs/ejemplos/partida_cripta-02.log` contiene un pergamino (recoge uno y lo usa para revertir la última acción: quedan 8 acciones vigentes). La prueba de equivalencia FR-LIN-008/SC-LIN-005 usará ese log, lo reproducirá completo y comparará con `historia` tras aplicar el mismo límite t (o el reloj final si t lo excede).
- La 001 y la 002 aún son dependencias de integración en las rutas compartidas. Se marcarán como tales; no se presenta código planeado como existente.

## Verificaciones del código actual

| Hecho | Fuente verificada |
|---|---|
| Retroceso usa closures, hasta cinco intervalos; pergamino quita el último | `cripta/modelo/reversible.py`, `cripta/modelo/historial_retroceso.py`, `cripta/modelo/partida.py::_usar_pergamino` |
| Estado aleatorio guardado en cada intervalo | `cripta/modelo/partida.py::_guardar_contadores` usa `self._azar.getstate()` |
| Estado completo y plano incluye RNG y agenda ordenada | `cripta/modelo/persistencia_modelo.py::crear_estado`, `cripta/infraestructura/estado_guardado.py::EstadoPartida` |
| Formato versionado rechaza incompatibilidad | `cripta/infraestructura/guardado_binario.py::FORMATO_VERSION`, `_leer_encabezado` y `CriptaFormatoIncompatibleError` |
| Replay procesa el log completo hoy | `cripta/servicios/servicio_replay.py::reproducir`, `cripta/__main__.py::_reproducir` |
| El log guarda acciones aceptadas; turnos de enemigo no son acciones de jugador | `cripta/infraestructura/partida_log.py`, confirmado también en `docs/MAPA_CODIGO.md` |
| El movimiento prepara la sala destino antes de confirmar | `cripta/modelo/partida.py::_mover` llama `precarga.preparar_sala` dentro de `sin_registrar`; `cripta/servicios/servicio_precarga.py::preparar_sala` usa contenido cargado/disco o puede activar una solicitud |
| La restauración actual prepara cada sala con contenido | `cripta/modelo/persistencia_modelo.py::restaurar_sala` llama `precarga.preparar_sala`; la reconstrucción histórica usará una vía separada sin esa llamada |

