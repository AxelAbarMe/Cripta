# Tareas: Terreno y Cazador

**Entrada**: Documentos de diseño en `specs/001-terreno-cazador/`

**Requisitos previos**: `plan.md` (requerido), `spec.md` (requerido), `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Organización**: Las tareas están agrupadas por fase temática y las fases se ejecutan en orden secuencial A, B, C, D, E.

## Formato: `[ID] [P?] [Story?] Descripción`

- **[P]**: Puede ejecutarse en paralelo con otras tareas de su mismo bloque (archivos distintos, sin dependencias sin completar)
- **[US1–US4]**: Historia de usuario a la que pertenece la tarea
- Se incluyen rutas exactas de archivo; se indica `(Nuevo)` cuando el archivo no existe y `(Modificado)` cuando ya existe

## Pull Requests previstos

1. **PR de documentación**: spec, clarificaciones, plan y tasks. Se abre cuando el análisis de consistencia quede limpio.
2. **PR de la Fase A** (contrato de datos): rama nueva desde `main`, después de fusionar el PR de documentación.
3. **PR de las Fases B a E**: rama nueva desde `main`, después de fusionar el PR de la Fase A.

---

## Fase A: Contrato de Datos — Bloque separable para el primer Pull Request de código

> [!IMPORTANT]
> Este bloque es el **punto de corte del primer Pull Request de código**.
> Las capacidades 002, 003 y 004 dependen del contrato de datos definido aquí (`SalidaDTO` con `costo`, `EnemigoDTO` con `rango`, `LlaveUbicacionDTO`, `obtener_llaves` en puertos y clientes, caché versionada, serialización y fixtures). Debe fusionarse antes de que esas capacidades comiencen.

**Objetivo**: Implementar y verificar todos los cambios al contrato de datos de la Parte II de forma autónoma, incluyendo sus pruebas, antes de cualquier lógica de terreno o cazador.

**Prueba independiente**: `py -m unittest tests.dto.test_salida_dto tests.dto.test_enemigo_dto tests.dto.test_llave_ubicacion_dto tests.infraestructura.test_cliente_offline_llaves tests.infraestructura.test_cache_llaves tests.modelo.test_cripta_mapa_costos`

### A.0 — Infraestructura de pruebas de la Fase A

- [X] T001 [US4] Crear `tests/dto/__init__.py` (Nuevo) para habilitar el descubrimiento de pruebas `unittest` en la carpeta `tests/dto/` (FR-TER-001, FR-TER-008, FR-TER-018)
- [X] T001b [US4] Modificar `tests/cliente_falso.py` (Modificado): implementar `obtener_llaves(id_cripta)` para cumplir el protocolo `ClienteCripta` ampliado en T010, devolviendo una tupla de `LlaveUbicacionDTO` configurable en el constructor y registrando la llamada como una solicitud, para que T005 pueda comprobar el presupuesto (FR-TER-018)

### A.1 — Pruebas del contrato de datos (escribir antes que el código)

> [!NOTE]
> Estas pruebas se escriben primero y se confirma que fallan antes de implementar los DTOs.

- [X] T002 [P] [US4] Crear `tests/dto/test_salida_dto.py` (Nuevo): prueba que salidas sin campo `costo` o con `costo` nulo en JSON quedan con `costo` en `None` (no declarado); prueba que `costo >= 1` se conserva; prueba que `costo < 1` o no entero lanza `ValueError` con la salida afectada en el mensaje, y que al construir la sala el mensaje incluye la sala y la dirección (FR-TER-001, FR-TER-016)
- [X] T003 [P] [US4] Crear `tests/dto/test_enemigo_dto.py` (Nuevo): prueba que ficha con `comportamiento == "cazador"` y `rango` nulo, ausente, no entero o menor que 1 se construye sin lanzar excepción y con `rango` en `None`; prueba que `rango >= 1` se almacena; prueba que ficha no cazadora tolera `rango` nulo (FR-TER-008, FR-TER-017)
- [X] T004 [P] [US4] Crear `tests/dto/test_llave_ubicacion_dto.py` (Nuevo): prueba que `LlaveUbicacionDTO.desde_json` construye correctamente el DTO con `enemigo` nulo o presente; prueba que campos `id` o `sala` ausentes, `id` vacío o `sala` menor que 1 lanzan `ValueError` con el dato afectado en el mensaje; prueba que `enemigo` nulo implica llave en el suelo (FR-TER-018)
- [X] T004b [P] [US4] Ampliar `tests/dto/test_llave_ubicacion_dto.py` (Modificado): prueba que un campo `enemigo` igual a cadena vacía lanza `ValueError` con el dato afectado en el mensaje, y que solo `enemigo` nulo o ausente se interpreta como llave en el suelo (FR-TER-018)
- [X] T005 [P] [US4] Crear `tests/infraestructura/test_cliente_offline_llaves.py` (Nuevo): prueba, con una carpeta de fixtures temporal creada por la propia prueba (no los fixtures reales, que se regeneran en T017), que `ClienteOffline.obtener_llaves()` lee `<carpeta>/<id>/llaves.json` y retorna una tupla de `LlaveUbicacionDTO`; prueba que `costo` en salidas del esqueleto se lee desde fixtures; prueba, con el cliente falso de `tests/`, que la consulta de llaves cuenta como una solicitud del presupuesto (FR-TER-016, FR-TER-018)
- [X] T006 [P] [US4] Crear `tests/infraestructura/test_cache_llaves.py` (Nuevo): prueba que la ubicación de llaves, el esqueleto y el contenido persistidos con una versión de cripta distinta, y las fichas de catálogo persistidas con una versión de catálogo distinta, se tratan como ausentes sin borrar archivos; prueba que los datos con la versión correcta se recuperan; si las pruebas de la Parte I (`tests/infraestructura/test_cache_disco.py`) ya cubren esqueleto, contenido o catálogo, se citan aquí en lugar de duplicarlas (FR-TER-019)
- [X] T006b [P] [US4] Crear `tests/modelo/test_cripta_mapa_costos.py` (Nuevo): con un esqueleto armado en la prueba, verificar que una conexión sin costo en ningún lado vale 100, que una con costo en un solo lado (por ejemplo 250 y nada) vale 250 en ambos sentidos, y que dos costos distintos lanzan `CriptaDatosInvalidosError` con las salas de la conexión en el mensaje; cubre el escenario US4-1 (FR-TER-001, FR-TER-002, FR-TER-016)

### A.2 — Implementación del contrato de datos

- [X] T007 [P] [US4] Modificar `cripta/dto/salida_dto.py` (Modificado): agregar campo `costo: int | None = None`; en `desde_json`, si `"costo"` está ausente o es nulo dejar `None` (no declarado en este lado; el 100 por defecto lo aplica `CriptaMapa`, T021b); si está presente validar entero `>= 1`, lanzando `ValueError` con la salida afectada en el mensaje ante dato inválido; `SalaDTO.desde_json` agrega la sala y la dirección. El cliente lo convierte, como en la Parte I (FR-TER-001, FR-TER-016)
- [X] T008 [P] [US4] Modificar `cripta/dto/enemigo_dto.py` (Modificado): agregar campo `rango: int | None = None`; en `desde_json`, si `comportamiento == "cazador"` conservar `rango` si es un entero `>= 1` y dejarlo en `None` si es nulo, ausente o no válido, sin lanzar excepción (el tratamiento pasivo es de T032, FR-TER-008); para otros comportamientos tolerarlo nulo (FR-TER-008, FR-TER-017)
- [X] T009 [P] [US4] Crear `cripta/dto/llave_ubicacion_dto.py` (Nuevo): dataclass `frozen=True, slots=True` con campos `id: str`, `sala: int`, `enemigo: str | None = None` y método de clase `desde_json` que lanza `ValueError` con el dato afectado si faltan `id` o `sala`, si `id` es vacío o si `sala` es menor que 1 (el cliente lo convierte, como en la Parte I); si `enemigo` es nulo o ausente, se asigna `None` (FR-TER-018)
- [X] T009b [US4] Modificar `cripta/dto/llave_ubicacion_dto.py` (Modificado): ajustar `desde_json` para rechazar un `enemigo` igual a cadena vacía con `ValueError` y el dato afectado, dejando `None` solo para `enemigo` nulo o ausente. El cliente lo convierte como siempre. Debe pasar T004b (FR-TER-018)
- [X] T010 [US4] Modificar `cripta/infraestructura/puertos.py` (Modificado): añadir `obtener_llaves(self, id_cripta: str) -> tuple[LlaveUbicacionDTO, ...]` al protocolo `ClienteCripta`, importando `LlaveUbicacionDTO` desde `cripta/dto/llave_ubicacion_dto.py` (FR-TER-018)
- [X] T011 [US4] Modificar `cripta/infraestructura/cliente_http.py` (Modificado): implementar `obtener_llaves` con `GET /criptas/{id}/llaves`, cabecera `X-Cripta-Client-Id`, conteo de la solicitud en el presupuesto, tiempo de espera explícito y reintento ante HTTP 429 respetando `reintentar_en`, contando cada reintento; retornar tupla de `LlaveUbicacionDTO` (FR-TER-018)
- [X] T012 [US4] Modificar `cripta/infraestructura/cliente_offline.py` (Modificado): implementar `obtener_llaves` leyendo `fixtures/<id>/llaves.json` y construyendo la tupla con `LlaveUbicacionDTO.desde_json` (FR-TER-018)
- [X] T013 [US4] Modificar `cripta/infraestructura/cliente_general.py` (Modificado): añadir delegación sincronizada de `obtener_llaves` hacia el cliente subyacente (FR-TER-018)
- [X] T014 [P] [US4] Modificar `cripta/infraestructura/cache.py` (Modificado): agregar persistencia y recuperación de las llaves bajo una clave que incluya la versión de la cripta, siguiendo el esquema de claves versionadas existente; si la versión de cripta o de catálogo no coincide, tratarlo como fallo de caché sin borrado manual de archivos (FR-TER-019)
- [X] T015 [P] [US4] Modificar `cripta/infraestructura/serializacion.py` (Modificado): incluir el campo `costo` al serializar salidas del esqueleto y el campo `rango` al serializar fichas del catálogo (FR-TER-016, FR-TER-017)
- [X] T021b [US4] Modificar `cripta/modelo/cripta_mapa.py` (Modificado): resolver el costo de cada conexión desde ambos lados, como `datos_de_puerta` hace con la llave y el cierre automático; si ningún lado declara costo, la conexión vale 100; si solo un lado lo declara, rige para ambos sentidos; si los dos lados declaran costos distintos, lanzar `CriptaDatosInvalidosError` con operación «construir el mapa», ruta «esqueleto de la cripta» y las salas de la conexión en el detalle; `_mover` (T021) y `_turno_enemigo` (T023) obtienen el costo desde aquí; corregir hasta que pase T006b. Va en la Fase A porque `CriptaMapa` no depende de las Fases B a E y las capacidades 002 a 004 necesitan el costo ya resuelto (FR-TER-002)

### A.3 — Fixtures y documentación de ejemplos

- [X] T016 [US4] Respaldar y reubicar los datos anteriores al servidor actual (FR-TER-019; Límite Conocido 5 del plan): el respaldo de los fixtures actuales es el commit e6d52ac. Mover `fixtures/cripta-01/`, el catálogo anterior (`fixtures/catalogo/`) y `fixtures/criptas.json` a `tests/datos/` como datos de prueba congelados, y cambiar `ClienteOffline("fixtures")` por `ClienteOffline("tests/datos")` en `tests/modelo/test_guardado_ida.py`, `tests/modelo/test_guardado_vuelta.py`, `tests/modelo/test_pergamino.py` y `tests/servicios/test_servicio_partida.py`, actualizando el docstring de cada una. Confirmar que esas pruebas siguen en `OK`
- [X] T017 [US4] Modificar `scripts/generar_fixtures.py` (Modificado): regenerar `fixtures/` para que quede igual al servidor actual (cripta-02 a cripta-06, con `costo` en salidas, `rango` en fichas de catálogo, `llaves.json` consultando `/llaves` y el catálogo 4b9e75a42be5); verificar que los fixtures generados pasan las pruebas de los DTOs; actualizar `docs/FORMATO_OFFLINE.md` y la sección de fixtures del `README.md` (criptas incluidas y ubicación de los datos congelados en `tests/datos/`) (FR-TER-001, FR-TER-008, FR-TER-018)

**Punto de corte del primer Pull Request de código**: Fase A completada y verificada → abrir PR a `main`.

---

## Fase B: Terreno — Costos de movimiento y reprogramación

> [!NOTE]
> Depende de que la Fase A esté fusionada en `main` (`SalidaDTO.costo` disponible). Se trabaja en una rama nueva desde `main`.

**Objetivo**: Que el intervalo de tiempo virtual escale con el costo de la salida, que el cambio de velocidad reprograme correctamente y que un desplazamiento rechazado no consuma tiempo. Aplica a jugador, errantes y rastreadores.

**Prueba independiente**: `py -m unittest tests.aceptacion.test_terreno_costos tests.modelo.test_reloj tests.controlador.test_controlador_errores`

### B.0 — Infraestructura de pruebas de la Fase B

- [X] T018 [US1] Crear `tests/aceptacion/__init__.py` (Nuevo) para habilitar el descubrimiento `unittest` en la carpeta `tests/aceptacion/` (FR-TER-004, FR-TER-005)

### B.1 — Pruebas de terreno (escribir antes que el código)

> [!NOTE]
> Las pruebas siguientes se escriben primero y se confirma que fallan antes de modificar el motor.

- [X] T019 [US1] Crear `tests/aceptacion/test_terreno_costos.py` (Nuevo) con los escenarios de aceptación de US1 y los casos del Apéndice B correspondientes a terreno:
  - US1-1: actor de velocidad 100, salida de costo 250 → intervalo 250 en ida y vuelta (FR-TER-001, FR-TER-002, FR-TER-003)
  - US1-2: actor de velocidad 100, salida sin costo → intervalo 100 (FR-TER-001)
  - US1-3 / Apéndice B caso 6: actor de velocidad 200, salida de costo 1 → intervalo `>= 1` (FR-TER-004)
  - US1-4 / Apéndice B caso 7: actor de velocidad 100 inicia cruce de salida de costo 400 en t=0, la velocidad cambia a 200 en t=100 → reprogramación a t=250 (FR-TER-005)
  - US1-5: esperar y atacar conservan costo 100 sin importar las salidas adyacentes (FR-TER-006)
  - US1-6: errante y rastreador usan el costo de la salida que cruzan (FR-TER-007)
  - Simetría: el costo de una salida es igual en ambos sentidos; si ningún lado declara costo, la conexión vale 100; si el costo se declara en un solo lado de la conexión (por ejemplo 250 de un lado y nada del otro), rige para ambos sentidos; si los dos lados declaran costos distintos, construir el mapa lanza `CriptaDatosInvalidosError` con las salas de la conexión en el mensaje (FR-TER-002; Límite Conocido 4 del plan)
- [X] T019b [US1] Ampliar `tests/controlador/test_controlador_errores.py` (Modificado) con la prueba de FR-TER-023: ante un desplazamiento rechazado (puerta cerrada o dirección sin salida), (a) se emite un mensaje descriptivo de rechazo observable, (b) el reloj virtual no avanza, (c) no cambian el estado del juego ni el historial de retroceso y (d) no se escribe ninguna línea en `partida.log`; la prueba cita FR-TER-023 (FR-TER-023)
- [X] T020 [P] [US1] Crear `tests/modelo/test_reloj.py` (Nuevo): prueba que `calcular_intervalo` con costo 1 y velocidad alta produce `>= 1`; prueba que `calcular_tiempo_reprogramado` escala el tiempo restante (se reutiliza la función existente de `cripta/modelo/reloj.py`, P1 §2.3, sin fórmula nueva); prueba el desempate por menor número de secuencia para dos eventos en el mismo instante en `RelojEventos` (FR-TER-004, FR-TER-005, FR-TER-022)

### B.2 — Implementación de terreno

- [X] T021 [US1] Modificar `cripta/modelo/partida.py` (Modificado) → `_mover`: en lugar de `accion.costo_base`, pasar a `_terminar_accion_jugador` el `costo` de la salida cruzada, de modo que el intervalo siga saliendo de `calcular_intervalo` (P1 §2.3); verificar que el regreso por la misma salida usa el mismo costo (FR-TER-002, FR-TER-003, FR-TER-004)
- [X] T022 [US1] Verificar `cripta/modelo/efectos.py` (Modificado si hace falta) → `EfectoCambioVelocidad`: confirmar que reescala el evento pendiente con `calcular_tiempo_reprogramado` y lo reprograma con número de secuencia nuevo mediante `RelojEventos.reprogramar`; corregir solo si la prueba T019 falla (FR-TER-005, FR-TER-022)
- [X] T023 [US1] Modificar `cripta/modelo/partida.py` (Modificado) → `_turno_enemigo`: para errantes y rastreadores, programar el turno con el costo de la salida que cruzan (consultado con `CriptaMapa.datos_de_puerta` o el esqueleto) en lugar de `COSTO_MOVER`, conservando su selección de destino. No cambiar `_activar_enemigos_de`, cuyo primer turno sigue siendo costo 100 según P1 §2.4 (FR-TER-006, FR-TER-007)
- [X] T024 [US1] Verificar `cripta/modelo/partida.py` (Modificado si hace falta) → acciones sin movimiento (atacar, esperar, usar, equipar, recoger, soltar, abrir): confirmar con las pruebas de T019 que conservan costo 100 sin importar las salidas adyacentes (FR-TER-006)
- [X] T025 [US1] Verificar `cripta/modelo/reloj.py` (Modificado si hace falta): `calcular_intervalo` aplica `max(1, ...)` y `RelojEventos` asigna número de secuencia al programar y reprogramar para un desempate total; corregir solo si T020 falla (FR-TER-004, FR-TER-005, FR-TER-022)
- [X] T025b [US1] Verificar `cripta/modelo/partida.py` (Modificado si hace falta) → `_despachar` y `_mover`: confirmar con T019b que un desplazamiento rechazado emite el mensaje, no consume tiempo, no altera el estado ni el historial y no llega a `partida.log`; corregir solo si T019b falla (FR-TER-023)

**Punto de verificación Fase B**: `py -m unittest tests.aceptacion.test_terreno_costos tests.modelo.test_reloj tests.controlador.test_controlador_errores` → todos en `OK`.

---

## Fase C: Cazador — Búsqueda de ruta y decisiones del enemigo

> [!IMPORTANT]
> Depende de la Fase A fusionada (`EnemigoDTO.rango`) y de la Fase B completa (costos en movimiento). La Fase D depende de que la Fase C esté completa.

**Objetivo**: Implementar el comportamiento del enemigo cazador: búsqueda de ruta compartida con estructuras propias, decisiones (ataque, movimiento, espera), desempate determinista, límite por rango, invalidación por eventos y ausencia de entradas de cazadores en `partida.log`.

**Prueba independiente**: `py -m unittest tests.aceptacion.test_cazador_persecucion tests.modelo.test_buscador_rutas tests.modelo.test_equivalencia_rutas tests.modelo.test_cazador_decisiones tests.infraestructura.test_partida_log`

### C.1 — Pruebas del cazador (escribir antes que el código)

- [X] T026 [P] [US2] [US3] Crear `tests/modelo/test_buscador_rutas.py` (Nuevo): prueba la búsqueda sobre un grafo simple de 5 salas con costos heterogéneos; prueba la poda por `rango_max` (ninguna sala con distancia `<= rango_max` se pierde; las demás pueden quedar en `None` o con una distancia tentativa mayor); prueba que si dos vecinas tienen el mismo `costo(u,v) + dist(v, S_J)` se elige la de menor `id`; prueba que la tabla se reutiliza sin recalcular si no fue invalidada; prueba que `invalidar()` fuerza el recálculo en la siguiente consulta; prueba que una activación con rango mayor al calculado recalcula (FR-TER-010, FR-TER-013, FR-TER-015)
- [X] T026b [P] [US2] [US3] Crear `tests/modelo/test_equivalencia_rutas.py` (Nuevo): sobre secuencias deterministas por semilla de movimientos del jugador, aperturas y cierres de puertas, activaciones y muertes de cazadores, comparar en cada turno de cada cazador la decisión del `BuscadorRutas` con reutilización contra la de un buscador nuevo que calcula desde cero; ninguna decisión puede diferir. Es la evidencia de equivalencia que exige P2 §5.2 (FR-TER-015)
- [X] T027 [P] [US2] [US3] Crear `tests/modelo/test_cazador_decisiones.py` (Nuevo): prueba que el cazador en la misma sala ataca con costo 100 (FR-TER-009); que con ruta abierta y `d <= rango` se mueve con el costo de la salida (FR-TER-012); que sin ruta abierta espera con costo 100 (FR-TER-011); que con `d > rango` espera con costo 100 (FR-TER-011); que no le afecta la niebla (FR-TER-014); que un cazador con `rango` en `None` no persigue: ataca si comparte sala y si no espera con costo 100, y que al activarse se agrega a la bitácora de mensajes un aviso con el id de la ficha (FR-TER-008)
- [X] T028 [P] [US2] [US3] Crear `tests/aceptacion/test_cazador_persecucion.py` (Nuevo) con los escenarios de aceptación de US2 y US3 y los casos del Apéndice B:
  - US2-1: cazador comparte sala → ataca, costo 100 (FR-TER-009)
  - US2-2 / Apéndice B caso 3: ruta directa de costo 300 contra ruta de 3 salas de costo 150 → elige la de 150, primer paso de costo 50 (FR-TER-010, FR-TER-012)
  - US2-3: el costo de la acción de moverse es el de la salida atravesada (FR-TER-012)
  - US3-1 / Apéndice B caso 4: dos vecinas con el mismo costo mínimo → va a la de menor id (FR-TER-013)
  - US3-2 / Apéndice B caso 1: sin ruta abierta → espera con costo 100 (FR-TER-011)
  - US3-3 / Apéndice B caso 2: ruta abierta pero `d > rango` → espera con costo 100 (FR-TER-011)
  - US3-4 / Apéndice B caso 5: una puerta de la ruta se cierra entre dos turnos → decide como desde cero (FR-TER-015)
  - US3-5: el cazador no abre puertas y no le afecta la niebla (FR-TER-014)
  - Activaciones simultáneas al entrar a una sala: sus primeros turnos se programan en orden ascendente de identificador de instancia (FR-TER-022)
  - Cazador en una sala que el jugador no ha visitado: permanece dormido y no persigue hasta que el jugador entra a su sala (supuesto de activación de la spec, P1 §2.4)
  - `d == rango`: el cazador se mueve, porque la espera exige `d > rango` (FR-TER-011, FR-TER-012)
  - Cazador que muere con su próximo turno programado: ese turno no produce ninguna acción (FR-TER-015)
  - Cazador en la misma sala que el jugador aunque la distancia por el mapa supere su rango: ataca (FR-TER-009)

- [X] T028c [US3] Ampliar `tests/aceptacion/test_cazador_persecucion.py` (Modificado) con escenarios que comprueban, a través de `Partida`, que la tabla del cazador se invalida en cada evento de T033 que hoy no tiene prueba propia:
  - El jugador abre una puerta con llave que acorta la ruta (FR-TER-015)
  - El jugador usa el pergamino de retroceso y vuelve a una sala anterior (FR-TER-015)
  - Se activa un cazador con un rango mayor que el calculado (FR-TER-015)
  - Se carga una partida guardada (FR-TER-015)
  - En cada caso la decisión del cazador debe ser la misma que calcular desde cero (FR-TER-015)

- [X] T028b [P] [US2] Ampliar `tests/estructuras/test_heap_min.py` (Modificado): prueba que `esta_vacio()` es verdadero en un montículo nuevo y falso tras insertar, y que `__len__` sigue las inserciones y extracciones (FR-TER-010)
- [X] T035 [P] [US3] Ampliar `tests/infraestructura/test_partida_log.py` (Modificado): tras turnos completos de un cazador, un errante y un rastreador (movimiento, espera y ataque) no se escribe ninguna línea en `partida.log`; `cripta/infraestructura/partida_log.py` no debería requerir cambios (FR-TER-021)

### C.2 — Estructuras auxiliares

- [X] T029 [P] [US2] Modificar `cripta/estructuras/heap_min.py` (Modificado): añadir `esta_vacio(self) -> bool` y `__len__(self) -> int` sobre la estructura interna existente, sin `heapq` ni otras bibliotecas prohibidas; hoy `HeapMinimo` solo tiene `insertar` y `eliminar_minimo` (FR-TER-010)
- [X] T030 [P] [US2] Modificar `cripta/modelo/enemigo.py` (Modificado): exponer la propiedad `rango` tomada de la ficha del catálogo, para uso de la decisión del cazador (FR-TER-008, FR-TER-012)

### C.3 — BuscadorRutas

- [ ] T031 [US2] Crear `cripta/modelo/buscador_rutas.py` (Nuevo): clase `BuscadorRutas` con `_distancias: list[int | None]`, `_cerrados: list[bool]`, `_sala_objetivo`, `_rango_max_calculado` y `_valido`; implementar `invalidar()`, `calcular_o_reutilizar(mapa, sala_jugador_id, rango_max)` con búsqueda de costo mínimo desde la sala del jugador usando `HeapMinimo` y tabla plana indexada por `sala_id` (sin `heapq`, `bisect`, `collections`, `dict` ni `set`), con poda al extraer un nodo de distancia `> rango_max`, solo por salidas abiertas en ese instante; implementar `distancia(sala_id)` y `decidir_paso(cazador, sala_jugador_id, mapa)`, que devuelve acción, dirección y costo de la salida, con desempate por `min(v.id)` (FR-TER-010, FR-TER-011, FR-TER-012, FR-TER-013, FR-TER-014, FR-TER-015)

### C.4 — Comportamiento del cazador en el motor

- [ ] T032 [US2] Modificar `cripta/modelo/comportamiento_enemigo.py` y `cripta/modelo/partida.py` → `_activar_enemigos_de` (Modificado): añadir `_decidir_cazador` que (1) ataca si comparte sala con el jugador, (2) consulta `BuscadorRutas.decidir_paso` si no, (3) espera si no hay ruta o `d > rango`; enlazarlo en `decidir_accion_enemigo` para el comportamiento `"cazador"`. Como hoy la decisión devuelve solo `(tipo, direccion)`, la decisión del cazador debe devolver también el costo, sin alterar el resultado de errantes y rastreadores. Un cazador con `rango` en `None` no consulta `BuscadorRutas`: ataca si comparte sala y si no espera con costo 100; el aviso a la bitácora de mensajes se agrega al activarlo, en `Partida._activar_enemigos_de` (solo el aviso: el primer turno sigue programándose con costo 100, ver T023) (FR-TER-008, FR-TER-009, FR-TER-010, FR-TER-011, FR-TER-012, FR-TER-013)
- [ ] T033 [US2] [US3] Modificar `cripta/modelo/partida.py` y `cripta/modelo/efectos.py` (Modificado): instanciar `BuscadorRutas` y usarlo en el turno del cazador; invalidar la tabla en `_mover` (el jugador cambia de sala), `_abrir` (puerta abierta), `EfectoCierrePuerta` (puerta cerrada), `_usar_pergamino` (retroceso), la activación de un cazador con `rango > _rango_max_calculado` y la carga de una partida guardada; conservar la tabla ante turnos de cazadores, muerte de enemigos y cambios de velocidad (FR-TER-015)
- [ ] T034 [US3] Verificar `cripta/modelo/partida.py` (Modificado si hace falta) → `_activar_enemigos_de`: confirmar con la prueba de T028 que las activaciones simultáneas programan sus primeros turnos en orden ascendente de identificador de instancia (FR-TER-022)

**Punto de verificación Fase C**: `py -m unittest tests.modelo.test_buscador_rutas tests.modelo.test_equivalencia_rutas tests.modelo.test_cazador_decisiones tests.aceptacion.test_cazador_persecucion tests.infraestructura.test_partida_log` → todos en `OK`.

---

## Fase D: Mediciones `--bench`

> [!NOTE]
> Depende de que las Fases B y C estén completas.

**Objetivo**: Implementar las cargas sintéticas `ruta_cazador` e `invalidacion` con sus alternativas descartadas, la carga `ciclo_referencia` sobre cripta-06, medir las cargas de regresión `ciclo`, `agenda` e `historial` y documentar los resultados tal como salgan.

### D.1 — Cargas nuevas

- [ ] T036 [US2] Modificar `cripta/bench/cargas_bench.py` (Modificado): registrar la carga `ruta_cazador`, que mide ciclos completos de `Partida` entre dos decisiones del jugador (agenda, turnos de enemigos, búsqueda e invalidación), sin red ni vista, como `bench_partida_real` de la Parte I, y reporta aparte el tiempo de la búsqueda sola y el tiempo dedicado a consultar costos con `costo_de_conexion` (Límite Conocido 6 del plan); usa una cripta sintética determinista de 400 salas (una muestra de la escala de diseño de hasta 1 000 salas) generada con `random.Random(42)`, costos de salida entre 20 y 490, escenarios `H=1, 10, 30` y rangos `R=600` y `R=2400` (valores reales del servidor), más el caso de rangos heterogéneos con la proporción de cripta-06 (25 de rango 600 y 11 de rango 2400, escalada a `H`, Límite Conocido 2 del plan); implementar también la alternativa descartada (cálculo individual desde cada cazador) en la misma carga (FR-TER-020)

  Comando exacto: `py -m cripta --bench --solo ruta_cazador`

- [ ] T036b [US2] Modificar `cripta/bench/cargas_bench.py` (Modificado): registrar la carga `ciclo_referencia`, que carga cripta-06 desde `fixtures/` con `ClienteOffline` (sin red ni vista), arma la partida y mide el ciclo de eventos completo entre dos decisiones del jugador con decenas de cazadores activos persiguiendo al mismo objetivo; si cripta-06 no trae suficientes cazadores, la carga activa más instancias de cazador con una semilla fija (`random.Random(42)`) y reporta cuántas agregó; ninguna cifra de cripta-06 se escribe en el código, todo sale de los fixtures (FR-TER-020)

  Comando exacto: `py -m cripta --bench --solo ciclo_referencia`

- [ ] T037 [US2] [US3] Modificar `cripta/bench/cargas_bench.py` (Modificado): registrar la carga `invalidacion` con 20 cazadores durante 100 ticks en dos escenarios, puertas estables y 5 puertas con cierre automático cada 15 ticks; implementar también la alternativa descartada (recalcular siempre en cada turno de cazador) (FR-TER-020)

  Comando exacto: `py -m cripta --bench --solo invalidacion`

- [ ] T038 [US2] Modificar `cripta/servicios/servicio_bench.py` (Modificado): habilitar las cargas `ruta_cazador`, `invalidacion` y `ciclo_referencia` y reportar las métricas del plan (tiempo por ciclo, número de búsquedas, razón individual/compartido) (FR-TER-020)

### D.2 — Cargas de regresión de la Parte I

- [ ] T039 Ejecutar las mediciones de regresión de la Parte I (sin cazadores) y verificar FR-TER-020 con la carga `ciclo_referencia` (cripta-06, 300 salas, desde `fixtures/`, con decenas de cazadores activos), comparándola con el límite de 20 ms. La carga sintética de 400 salas y `ruta_cazador` (`H=30`) se mantienen solo para comparar alternativas. Anotar los resultados tal como salgan, sin afirmar cifras no medidas (FR-TER-020):

  ```powershell
  py -m cripta --bench --solo ciclo_referencia
  py -m cripta --bench --solo ciclo
  py -m cripta --bench --solo agenda
  py -m cripta --bench --solo historial
  ```
  Si algún límite se supera, documentarlo como límite conocido, revisar la decisión e informar al responsable de la capacidad 004 sobre el resultado de `historial`.

**Punto de verificación Fase D**: Las cargas nuevas y de regresión terminan sin errores y los resultados quedan anotados para T043.

---

## Fase E: Cierre y Verificación Final

> [!NOTE]
> Depende de que las Fases A a D estén completas. T040 y T041 no dependen entre sí.

**Objetivo**: Garantizar la compatibilidad con la Parte I, auditar importaciones prohibidas, verificar `--replay` y dejar documentadas la decisión y las invocaciones.

- [ ] T040 [P] Ejecutar la suite completa y confirmar que las 222 pruebas de la Parte I terminan en `OK` junto con las nuevas (Principio VIII):

  Comando exacto: `py -m unittest discover -s tests -t .`

- [ ] T041 [P] Auditar importaciones prohibidas (Principio I):

  ```powershell
  Select-String -Path (Get-ChildItem cripta -Recurse -Filter *.py).FullName -Pattern "heapq|bisect|collections|networkx|sorted\(|\.sort\("
  ```
  Resultado esperado: sin importaciones prohibidas; cada `sorted(` o `.sort(` se revisa a mano y solo se permite fuera de los ordenamientos evaluados. Los usos de `dict` y `set` como índice o caché se revisan a mano en el Pull Request, porque la búsqueda de texto no distingue los usos permitidos.

- [ ] T042 Grabar ejemplos nuevos que muestren terreno con costo y cazadores (con los fixtures regenerados en T017), reemplazar los tres de `docs/ejemplos/` (que guardan el catálogo anterior y ya no se reproducen), actualizar la tabla de bitácoras de ejemplo del `README.md` y reproducir cada uno con `--replay` (Principio VIII):

  Comando exacto: `py -m cripta --offline --replay docs/ejemplos/partida_cripta-06.log`

  Resultado esperado: código de salida `0` para cada ejemplo nuevo, sin ejemplos con el catálogo be68d322d2f5.

- [ ] T043 Ampliar `DECISIONES.md` (raíz) con la sección de la capacidad 001: problema, alternativas y razón de descarte, decisión, complejidad, resultados de `--bench` de T036, T036b, T037 y T039 con el comando exacto, el tiempo de consulta de costos medido en T036 y, si pesa, la alternativa de precalcular los costos en una tabla plana al construir el mapa (O(1) por consulta, frente a O(log n) de la consulta actual), límites conocidos y enlaces a `spec.md` y `plan.md` (Principio VI)
- [ ] T044 Registrar en `PROMPTS_LLM.md` las invocaciones de la implementación (por ejemplo `/speckit-implement`), con fecha, herramienta, prompt textual y para qué se usó (Flujo de Trabajo de la Constitución)

---

## Dependencias y Orden de Ejecución

### Dependencias entre fases

```
Fase A ──► Fase B ──► Fase C ──► Fase D ──► Fase E
```

- **Fase A** (contrato de datos): inicia tras fusionar el PR de documentación. Es el primer Pull Request de código y desbloquea las capacidades 002, 003 y 004.
- **Fase B** (terreno): depende de la Fase A fusionada en `main`.
- **Fase C** (cazador): depende de la Fase A fusionada y de la Fase B completa. T004b y T009b (rechazo de `enemigo` vacío en `LlaveUbicacionDTO`) se hacen antes de la Fase C.
- **Fase D** (`--bench`): depende de las Fases B y C completas.
- **Fase E** (cierre): depende de las Fases A a D completas.

### Dependencias entre historias de usuario

| Historia | Prioridad | Puede iniciar tras... |
|---|---|---|
| US4 — Contrato de datos | P2 | El PR de documentación fusionado (es la Fase A) |
| US1 — Movimiento y costos | P1 | Fase A fusionada |
| US2 — Cazador (persecución) | P1 | Fase A fusionada y Fase B completa |
| US3 — Cazador (desempates y puertas) | P2 | Fase C implementada (US2) |

### Dependencias dentro de cada fase

- Fase A: T001 → T001b → T002–T006, T004b y T006b (pruebas en paralelo) → T007, T008, T009, T014, T015 y T021b (en paralelo) → T009b (tras T004b, antes de la Fase C) → T010 → T011 y T012 → T013 → T016 → T017
- Fase B: T018 → T019, T019b, T020 (pruebas) → T021 → T022 → T023 → T024 → T025 → T025b
- Fase C: T026, T026b, T027, T028, T028b y T035 (pruebas en paralelo) → T028c (tras T028, mismo archivo, antes de C.4) → T029–T030 (en paralelo) → T031 → T032 → T033 → T034
- Fase D: T036 → T036b → T037 (mismo archivo) → T038 → T039
- Fase E: T040–T041 (en paralelo) → T042 → T043 → T044

### Oportunidades de paralelización

```text
Fase A, pruebas (archivos distintos): T002, T003, T004, T004b, T005, T006, T006b
Fase A, implementación: T007, T008, T009, T014, T015, T021b (T010 a T013 van en orden después de T009, porque usan `LlaveUbicacionDTO`)
Fase C, pruebas: T026, T026b, T027, T028, T028b, T035
Fase C, auxiliares: T029, T030
Fase E, auditoría y suite: T040, T041
```

---

## Estrategia de Implementación

> [!IMPORTANT]
> El código se entrega en dos Pull Requests posteriores al de documentación, cada uno desde una rama nueva creada desde `main` actualizado. No se acumulan fases sin fusionar el Pull Request anterior.

### Pull Request de documentación

1. Spec, clarificaciones, plan y tasks, con `/speckit-analyze` limpio.
2. Revisión por otro integrante y fusión con merge commit, sin squash.

### Pull Request de la Fase A

3. Rama nueva desde `main`. Completar la Fase A: infraestructura de pruebas → pruebas → implementación → fixtures.
4. Revisión y fusión. Las capacidades 002, 003 y 004 pueden comenzar tras esta fusión.

### Pull Request de las Fases B a E

5. Rama nueva desde `main` con la Fase A ya fusionada.
6. Completar en orden Fase B, Fase C, Fase D y Fase E, verificando al final de cada una su punto de verificación.
7. Abrir el Pull Request con las Fases B a E.

---

## Notas

- Las tareas **[P]** tocan archivos distintos y no dependen entre sí dentro de su bloque.
- Ninguna tarea incluye `git commit` ni `git push`. Los hacen las personas.
- Las prohibiciones de la Constitución aplican a toda tarea: sin `heapq`, `bisect`, `collections`, `networkx`, `set` ni `dict` como índice o caché, y sin `list.sort()` ni `sorted()` en los ordenamientos evaluados.
- Los errores de programación interna heredan de `IndexError` o `ValueError` en su propio módulo. Los DTO lanzan `ValueError` ante datos externos inválidos y los clientes lo convierten (`ClienteOffline` en `CriptaDatosInvalidosError`, `ClienteHttp` en `CriptaApiError`), como en la Parte I. Solo `CriptaMapa` lanza `CriptaDatosInvalidosError` directamente.
- Las carpetas nuevas de pruebas (`tests/dto/`, `tests/aceptacion/`) requieren un `__init__.py` explícito (T001, T018).
- La invocación de `/speckit-tasks` y sus correcciones se registran en `PROMPTS_LLM.md` al ejecutarlas, fuera de esta lista.