# Investigación: línea de tiempo

## Registro consultable

**Decisión**: Mantener acciones aceptadas y puntos de control en una línea de tiempo propia. No reutilizar el registro de closures del pergamino.

**Razón**: `cripta/modelo/reversible.py` registra closures de inversión. `cripta/modelo/historial_retroceso.py` conserva solo cinco intervalos y los ejecuta en LIFO; no representa tiempos ni se puede guardar como datos. `Partida._guardar_contadores` guarda además `random.Random.getstate()` en cada intervalo. El registro aparte permite consultar y persistir sin alterar el mecanismo de pergamino.

**Alternativas consideradas**: usar closures del historial (descartado por no ser consultable ni serializable y por su límite de cinco intervalos); emitir un registro plano de cada mutación (apto para invertir, pero exige cobertura explícita de cada campo y coordinación con 001/002). Se medirá esta segunda alternativa contra re-simulación antes de descartar su factibilidad.

## Reconstrucción de una consulta

**Decisión**: Partir del checkpoint más cercano anterior al objetivo y re-simular las acciones necesarias en un contexto aislado, con estado RNG restaurado.

**Razón**: `cripta/modelo/persistencia_modelo.py::crear_estado` produce `EstadoPartida` con datos planos y `EstadoRNG`. Así se limita el trabajo a K acciones (FR-LIN-015) y la consulta no toca la partida activa (FR-LIN-005).

**Alternativas consideradas**: invertir mutaciones serializables hasta el objetivo (requiere cubrir todas las mutaciones del motor); reconstruir desde el inicio sin checkpoints (simple, pero no satisface el límite K). El benchmark `linea_tiempo` compara la primera alternativa y el caso sin checkpoints.

## Orden temporal

**Decisión**: Reproducir con el mismo orden determinista que la agenda existente y respetar el corte antes de la siguiente decisión del jugador.

**Razón**: `cripta/modelo/reloj.py::EventoProgramado.__lt__` compara `(tiempo, secuencia)`. `RelojEventos.ejecutar_siguiente` extrae el mínimo vigente, fija el reloj al tiempo del evento y ejecuta la acción. `reprogramar` crea un evento con secuencia nueva. D.3 del contexto confirma secuencia creciente como desempate. Este es el orden relevante para FR-LIN-002.

**Alternativas consideradas**: agrupar eventos solo por tiempo e ignorar la secuencia (descartado porque puede cambiar el estado observable); reproducir todas las acciones del mismo instante antes de devolver el control al jugador (descartado porque contradice el límite predecisión de FR-LIN-002).

## Localización y recorte

**Decisión**: Guardar checkpoints en una secuencia contigua ordenada por acción, localizar el previo con búsqueda binaria manual y recortar la línea vigente desde el final al aceptar pergamino.

**Razón**: Los checkpoints se insertan en orden. La búsqueda binaria reduce la localización a O(log C); truncar la secuencia y quitar checkpoints posteriores evita recorrer el historial completo. Las operaciones son compatibles con el uso de `list` como almacenamiento contiguo y no requieren `bisect`, `dict` ni `set`.

**Alternativas consideradas**: escaneo lineal de checkpoints (más simple, O(C) por consulta); filtrar todos los registros por tiempo al usar pergamino (O(N), innecesario dado que la línea vigente tiene un límite de longitud).

## Persistencia y compatibilidad

**Decisión**: Extender `EstadoPartida` y el formato binario existente, incrementar su versión y rechazar explícitamente archivos P1.

**Razón**: `cripta/infraestructura/guardado_binario.py` declara `FORMATO_VERSION = 1` y ya lanza `CriptaFormatoIncompatibleError` cuando magic o versión no coinciden. `EstadoPartida` y sus clases auxiliares son el canal de datos planos.

**Alternativas consideradas**: cargar P1 en silencio (prohibido por FR-LIN-011); ofrecer migración (prohibido por FR-LIN-012); guardar la línea en archivo lateral (puede desincronizarse del guardado principal y no cumple el guardado completo atómico a nivel lógico).

## Replay y CLI

**Decisión**: Agregar `--hasta t` al servicio de replay y los comandos/configuración de historia y checkpoints a la CLI, sin instanciar la vista interactiva en replay o bench.

**Razón**: `ServicioReplay.reproducir(ruta)` itera toda la bitácora y `cripta/__main__.py::_reproducir` imprime el resultado completo. La ruta de replay ya se ejecuta antes de crear `ControladorCripta` y `VistaConsola`.

**Alternativas consideradas**: filtrar o truncar el archivo log para simular un corte (descartado porque altera la fuente y no respeta eventos temporales); reutilizar la interfaz interactiva de la vista (descartado por separación MVC y ejecución sin vista).

## Mediciones requeridas

**Decisión**: No fijar cifras ni K predeterminado antes de medir. Ejecutar `py -m cripta --bench --solo linea_tiempo --escala 1` con K=100, 500, 1000 y sin checkpoints. Usar semilla explícita con `random.Random(semilla)` y escoger la cripta de referencia dinámicamente por mayor total de salas.

**Razón**: FR-LIN-014 deja el valor de K a la medición del grupo y FR-LIN-018 fija el objetivo de consulta. La tabla del plan enumera también la alternativa de cambios invertibles y la búsqueda lineal.

**Alternativas consideradas**: elegir K por intuición (sin evidencia y contrario a FR-LIN-014); fijar mediciones en documentación antes de ejecutar (no reproducible).

## Insumos de 001 y 002

- El plan de `specs/001-terreno-cazador/plan.md` indica que `--bench --solo historial` medirá el costo del historial de retroceso con muchos cazadores y que su resultado se informará a 004. El plan consultado no contiene cifras; por tanto no se atribuye ninguna.
- `specs/002-niebla-ir-a/plan.md` y `data-model.md` describen el conocimiento del jugador como estado de partida con nivel por sala y observaciones por salida, plano y reversible. La 004 debe guardar esos datos en checkpoints e incluirlos en las consultas históricas. La codificación y versión binaria corresponden a 004.
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

