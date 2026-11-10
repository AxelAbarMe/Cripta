# Tareas: Terreno y Cazador

**Entrada**: Documentos de diseño en `specs/001-terreno-cazador/`

**Requisitos previos**: `plan.md` (requerido), `spec.md` (requerido), `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Organización**: Las tareas están agrupadas por fase temática para permitir la implementación y verificación independientes de cada bloque.

## Formato: `[ID] [P?] [Story?] Descripción`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias sin completar)
- **[US1–US4]**: Historia de usuario a la que pertenece la tarea
- Se incluyen rutas exactas de archivo y se indica `(Nuevo)` cuando el archivo no existe aún

---

## Fase A: Contrato de Datos — Bloque separable para el primer Pull Request

> [!IMPORTANT]
> Este bloque es el **punto de corte del primer Pull Request** a `main`.  
> Las capacidades 002, 003 y 004 dependen del contrato de datos definido aquí (SalidaDTO con `costo`, EnemigoDTO con `rango`, LlaveUbicacionDTO, `obtener_llaves` en puertos y clientes, caché versionada, serialización y fixtures). Debe fusionarse antes de que esas capacidades comiencen.

**Objetivo**: Implementar y verificar todos los cambios al contrato de datos de la Parte II de forma autónoma, incluyendo sus pruebas, antes de cualquier lógica de terreno o cazador.

**Prueba independiente**: `py -m unittest tests.dto.test_salida_dto tests.dto.test_enemigo_dto tests.dto.test_llave_ubicacion_dto tests.infraestructura.test_cliente_offline_llaves tests.infraestructura.test_cache_llaves`

### A.0 — Infraestructura de pruebas de la Fase A

- [ ] T001 [US4] Crear `tests/dto/__init__.py` (Nuevo) para habilitar el descubrimiento de pruebas `unittest` en la carpeta `tests/dto/` (FR-TER-001, FR-TER-008, FR-TER-018)

### A.1 — Pruebas del contrato de datos (escribir antes que el código)

> [!NOTE]
> Estas pruebas deben escribirse primero y confirmarse que fallan antes de implementar los DTOs.

- [ ] T002 [P] [US4] Crear `tests/dto/test_salida_dto.py` (Nuevo): prueba que salidas sin campo `costo` o con `costo` nulo en JSON asignan `100`; prueba que `costo >= 1` se conserva; prueba que `costo < 1` lanza `CriptaDatosInvalidosError` o `CriptaApiError` con el id de ficha en el mensaje (FR-TER-001, FR-TER-016)
- [ ] T003 [P] [US4] Crear `tests/dto/test_enemigo_dto.py` (Nuevo): prueba que ficha con `comportamiento == "cazador"` y `rango` nulo o ausente lanza `CriptaDatosInvalidosError` (en `--offline`) o `CriptaApiError` (en HTTP) con el `id` de la ficha en el mensaje; prueba que `rango >= 1` se almacena; prueba que ficha no cazadora tolera `rango` nulo (FR-TER-008, FR-TER-017)
- [ ] T004 [P] [US4] Crear `tests/dto/test_llave_ubicacion_dto.py` (Nuevo): prueba que `LlaveUbicacionDTO.desde_json` construye correctamente el DTO con `enemigo` nulo o presente; prueba que campos `id` o `sala` ausentes lanzan `CriptaDatosInvalidosError`; prueba que `enemigo` nulo implica llave en suelo (FR-TER-018)
- [ ] T005 [P] [US4] Crear `tests/infraestructura/test_cliente_offline_llaves.py` (Nuevo): prueba que `ClienteOffline.obtener_llaves()` lee `fixtures/<id>/llaves.json` y retorna una tupla de `LlaveUbicacionDTO`; prueba que la llamada descuenta el presupuesto en 1; prueba que `costo` en salidas del esqueleto se lee desde fixtures (FR-TER-016, FR-TER-018)
- [ ] T006 [P] [US4] Crear `tests/infraestructura/test_cache_llaves.py` (Nuevo): prueba que datos persistidos con versión de cripta distinta son detectados como incompatibles y rechazados sin borrar archivos; prueba que datos con versión correcta se recuperan; prueba que un archivo de la Parte I se rechaza formalmente (FR-TER-019)

### A.2 — Implementación del contrato de datos

- [ ] T007 [P] [US4] Modificar `cripta/dto/salida_dto.py`: agregar campo `costo: int = 100`; en `desde_json`, si `"costo"` está ausente o es nulo asignar `100`; si está presente validar entero `>= 1`, lanzando la excepción externa apropiada con el id de ficha en el mensaje ante dato inválido (FR-TER-001, FR-TER-016)
- [ ] T008 [P] [US4] Modificar `cripta/dto/enemigo_dto.py`: agregar campo `rango: int | None = None`; en `desde_json`, si `comportamiento == "cazador"` exigir `rango` entero `>= 1`, lanzando `CriptaDatosInvalidosError` (en `--offline`) o `CriptaApiError` (en HTTP) con el `id` de la ficha en el mensaje si es nulo o ausente; para otros comportamientos tolerarlo nulo (FR-TER-008, FR-TER-017)
- [ ] T009 [P] [US4] Crear `cripta/dto/llave_ubicacion_dto.py` (Nuevo): dataclass `frozen=True, slots=True` con campos `id: str`, `sala: int`, `enemigo: str | None = None` y método de clase `desde_json` que lanza `CriptaDatosInvalidosError` si faltan `id` o `sala`; si `enemigo` es nulo o ausente, se asigna `None` (FR-TER-018)
- [ ] T010 [US4] Modificar `cripta/infraestructura/puertos.py`: añadir método abstracto `obtener_llaves(self, id_cripta: str) -> tuple[LlaveUbicacionDTO, ...]` al protocolo `ClienteCripta`, importando `LlaveUbicacionDTO` desde `cripta/dto/llave_ubicacion_dto.py` (FR-TER-018)
- [ ] T011 [P] [US4] Modificar `cripta/infraestructura/cliente_http.py`: implementar `obtener_llaves` realizando `GET /criptas/{id}/llaves` con cabecera `X-Cripta-Client-Id`, descuento de presupuesto, timeout explícito y reintento ante HTTP 429 respetando `reintentar_en`; retornar tupla de `LlaveUbicacionDTO` (FR-TER-018)
- [ ] T012 [P] [US4] Modificar `cripta/infraestructura/cliente_offline.py`: implementar `obtener_llaves` leyendo `fixtures/<id>/llaves.json` y construyendo la tupla de `LlaveUbicacionDTO` con `desde_json`; descuenta el presupuesto en 1 (FR-TER-018)
- [ ] T013 [US4] Modificar `cripta/infraestructura/cliente_general.py`: añadir delegación sincronizada a `obtener_llaves` hacia el cliente subyacente (FR-TER-018)
- [ ] T014 [P] [US4] Modificar `cripta/infraestructura/cache.py`: agregar persistencia y recuperación de `llaves.json` bajo clave versionada `cripta.<id>.<version>.llaves.json`; invalidar automáticamente si la versión de cripta o catálogo no coincide, sin requerir borrado manual (FR-TER-019)
- [ ] T015 [P] [US4] Modificar `cripta/infraestructura/serializacion.py`: incluir campo `costo` al serializar salidas del esqueleto a JSON y campo `rango` al serializar fichas del catálogo (FR-TER-016, FR-TER-017)

### A.3 — Fixtures y documentación de ejemplos

- [ ] T016 [US4] Respaldar los fixtures actuales de `fixtures/` antes de regenerarlos; revisar qué registros de `docs/ejemplos/` quedarían incompatibles con `--replay` si cambia la versión de la cripta (FR-TER-019; ver Límite Conocido 5 del plan)
- [ ] T017 [US4] Modificar `scripts/generar_fixtures.py`: añadir regeneración de fixtures con campo `costo` en salidas, campo `rango` en fichas de catálogo y `llaves.json` consultando el endpoint `/llaves`; verificar que los fixtures generados superan las pruebas de los DTOs (FR-TER-001, FR-TER-008, FR-TER-018)

**Punto de corte del primer Pull Request**: Fase A completada y verificada → abrir PR a `main`.

---

## Fase B: Terreno — Costos de movimiento y reprogramación

> [!NOTE]
> Depende de que Fase A esté fusionada (SalidaDTO con `costo` disponible). Puede iniciarse en paralelo con Fase C si Fase A ya está en `main`.

**Objetivo**: Extender el motor de movimiento para que el intervalo de tiempo virtual escale con el costo de la salida, y reprogramar correctamente ante cambios de velocidad. Aplica a jugador, errantes y rastreadores.

**Prueba independiente**: `py -m unittest tests.aceptacion.test_terreno_costos`

### B.0 — Infraestructura de pruebas de la Fase B

- [ ] T018 [US1] Crear `tests/aceptacion/__init__.py` (Nuevo) para habilitar el descubrimiento `unittest` en la carpeta `tests/aceptacion/` (FR-TER-004, FR-TER-005)

### B.1 — Pruebas de terreno (escribir antes que el código)

> [!NOTE]
> Las pruebas siguientes deben fallar antes de modificar el código del motor.

- [ ] T019 [US1] Crear `tests/aceptacion/test_terreno_costos.py` (Nuevo) con los escenarios de aceptación de US1 y los casos del Apéndice B correspondientes a terreno:
  - Escenario US1-1: actor velocidad 100, salida costo 250 → intervalo 250 en ida y vuelta (FR-TER-001, FR-TER-002, FR-TER-003)
  - Escenario US1-2: actor velocidad 100, salida sin costo → intervalo 100 (FR-TER-001)
  - Escenario US1-3 / Apéndice B caso 6: actor velocidad 200, salida costo 1 → intervalo `>= 1` (FR-TER-004)
  - Escenario US1-4 / Apéndice B caso 7: actor velocidad 100 inicia cruce de salida costo 400 en t=0, velocidad cambia a 200 en t=100 → reprogramación a t=250 (FR-TER-005)
  - Escenario US1-5: esperar y atacar conservan costo 100 sin importar salidas adyacentes (FR-TER-006)
  - Escenario US1-6: errante y rastreador usan el costo de la salida elegida para su movimiento (FR-TER-007)
- [ ] T020 [P] [US1] Crear `tests/modelo/test_reloj.py` (Nuevo): prueba `calcular_intervalo(costo, velocidad)` para costo 1 y velocidad alta produce `>= 1`; prueba `reprogramar` escala correctamente el tiempo restante con la fórmula `max(1, restante * v_ant // v_nueva)`; prueba desempate por menor número de secuencia en la agenda para dos eventos en el mismo instante (FR-TER-004, FR-TER-005, FR-TER-022)

### B.2 — Implementación de terreno

- [ ] T021 [US1] Modificar `cripta/modelo/partida.py` → función `_mover`: usar `salida.costo` para calcular `intervalo = max(1, costo * 100 // velocidad)` en lugar del costo base fijo; verificar que el movimiento hacia atrás por la misma salida usa el mismo `costo` (FR-TER-002, FR-TER-003, FR-TER-004)
- [ ] T022 [US1] Modificar `cripta/modelo/partida.py` → lógica de reprogramación ante cambio de velocidad: aplicar `max(1, (t_siguiente - t) * velocidad_anterior // velocidad_nueva)` y actualizar el evento en la agenda con un número de secuencia nuevo (FR-TER-005)
- [ ] T023 [US1] Modificar `cripta/modelo/partida.py` → `_turno_enemigo` para errantes y rastreadores: pasar `salida.costo` al cálculo del intervalo de movimiento, conservando su lógica de selección de destino (FR-TER-007)
- [ ] T024 [US1] Modificar `cripta/modelo/partida.py` → acciones sin movimiento (atacar, esperar, usar, equipar, recoger, soltar, abrir): confirmar que sus costos de acción no se ven afectados por costos de salidas; añadir prueba de regresión en `test_terreno_costos.py` si no existe aún (FR-TER-006)
- [ ] T025 [US1] Verificar `cripta/modelo/reloj.py` → funciones `calcular_intervalo` y `calcular_tiempo_reprogramado`: ajustar o añadir la cláusula `max(1, ...)` si no existe ya; añadir el nuevo número de secuencia en `ReprogramarEvento` para garantizar desempate total en la agenda (FR-TER-004, FR-TER-005, FR-TER-022)

**Punto de verificación Fase B**: `py -m unittest tests.aceptacion.test_terreno_costos tests.modelo.test_reloj` → todos en OK.

---

## Fase C: Cazador — Búsqueda de ruta y decisiones del enemigo

> [!IMPORTANT]
> Depende de Fase A fusionada (EnemigoDTO con `rango`) y Fase B completada (costos en movimiento). Fase C puede ejecutarse en paralelo con Fase D una vez que Fase A y B estén listas.

**Objetivo**: Implementar el comportamiento del enemigo cazador: búsqueda de ruta compartida por Dijkstra con estructuras propias, decisiones (ataque, movimiento, espera), desempate determinista, límite por rango, invalidación de caché por eventos e impacto en `partida.log`.

**Prueba independiente**: `py -m unittest tests.aceptacion.test_cazador_persecucion tests.modelo.test_buscador_rutas tests.modelo.test_cazador_decisiones`

### C.1 — Pruebas del cazador (escribir antes que el código)

- [ ] T026 [P] [US2] [US3] Crear `tests/modelo/test_buscador_rutas.py` (Nuevo): prueba Dijkstra sobre grafo simple de 5 salas con costos heterogéneos; prueba poda por `rango_max` (salas fuera de rango retornan `None`); prueba desempate: cuando dos vecinas tienen el mismo `costo(u,v) + dist(v, S_J)`, se elige la de menor `id`; prueba que la tabla se reutiliza sin recalcular si no fue invalidada; prueba que `invalidar()` fuerza recálculo en la siguiente consulta (FR-TER-010, FR-TER-013, FR-TER-015)
- [ ] T027 [P] [US2] [US3] Crear `tests/modelo/test_cazador_decisiones.py` (Nuevo): prueba cazador comparte sala → ataca con costo 100 (FR-TER-009); prueba cazador en sala distinta con ruta abierta `d <= rango` → se mueve con costo de la salida (FR-TER-012); prueba cazador sin ruta abierta → espera costo 100 (FR-TER-011); prueba cazador con `d > rango` → espera costo 100 (FR-TER-011); prueba cazador no afectado por niebla de guerra (FR-TER-014); prueba que movimientos del cazador no generan líneas en `partida.log` (FR-TER-021)
- [ ] T028 [P] [US2] [US3] Ampliar `tests/aceptacion/test_cazador_persecucion.py` (Nuevo) con los escenarios de aceptación de US2, US3 y los siete casos del Apéndice B:
  - US2-1: cazador comparte sala → ataca, costo 100 (FR-TER-009)
  - US2-2 / Apéndice B caso 3: ruta directa costo 300 vs ruta 3 salas costo 150 → elige la de 150, primer paso costo 50 (FR-TER-010, FR-TER-012)
  - US2-3: costo de acción del cazador al moverse = costo de la salida atravesada (FR-TER-012)
  - US3-1 / Apéndice B caso 4: dos vecinas con mismo costo mínimo → va a la de menor id (FR-TER-013)
  - US3-2 / Apéndice B caso 1: sin ruta abierta → espera costo 100 (FR-TER-011)
  - US3-3 / Apéndice B caso 2: ruta abierta pero `d > rango` → espera costo 100 (FR-TER-011)
  - US3-4 / Apéndice B caso 5: puerta de la ruta se cierra entre dos turnos → decide como desde cero (FR-TER-015)
  - US3-5: cazador no abre puertas, no le afecta niebla de guerra (FR-TER-014)

### C.2 — Estructuras auxiliares

- [ ] T029 [P] [US2] Modificar `cripta/estructuras/heap_min.py`: añadir métodos `esta_vacio(self) -> bool` y `__len__(self) -> int` sobre la lista interna existente, sin usar `heapq` ni otras bibliotecas prohibidas (FR-TER-010; plan §1 y §5)
- [ ] T030 [P] [US2] Modificar `cripta/modelo/enemigo.py`: exponer propiedad `rango` que retorna `self._ficha.rango` (entero); usar únicamente en la decisión del cazador (FR-TER-008, FR-TER-012)

### C.3 — BuscadorRutas (Dijkstra compartido)

- [ ] T031 [US2] Crear `cripta/modelo/buscador_rutas.py` (Nuevo): clase `BuscadorRutas` con atributos internos `_distancias: list[int | None]`, `_sala_objetivo: int | None`, `_rango_max_calculado: int`, `_valido: bool`; implementar `invalidar()`, `calcular_o_reutilizar(mapa, sala_jugador_id, rango_max)` con Dijkstra usando `HeapMinimo` y tabla plana `list` indexada por `sala_id` (prohibidos `heapq`, `bisect`, `collections`, `dict` y `set`), con poda al extraer nodo con distancia `> rango_max`; implementar `distancia(sala_id)` y `decidir_paso(cazador, sala_jugador_id, mapa)` con desempate por `min(v.id)` (FR-TER-010, FR-TER-011, FR-TER-012, FR-TER-013, FR-TER-014, FR-TER-015)

### C.4 — Comportamiento del cazador en el motor

- [ ] T032 [US2] Modificar `cripta/modelo/comportamiento_enemigo.py`: añadir función `_decidir_cazador(cazador, sala_jugador_id, buscador, mapa)` que (1) ataca si comparten sala con costo 100, (2) consulta `buscador.decidir_paso` si no comparten sala, (3) espera con costo 100 si no hay ruta o `d > rango`; enlazar en `decidir_accion_enemigo` para comportamiento `"cazador"` (FR-TER-009, FR-TER-010, FR-TER-011, FR-TER-012, FR-TER-013)
- [ ] T033 [US2] [US3] Modificar `cripta/modelo/partida.py`: instanciar `BuscadorRutas` y pasarlo al turno del cazador; invalidar la tabla en los eventos: `_mover` (jugador cambia sala), `_abrir` (puerta abierta), cierre automático de puerta, `_usar_pergamino` (retroceso), activación de cazador con `rango > _rango_max_calculado`, carga de partida guardada; conservar la tabla ante: turnos de cazadores, muerte de enemigos, cambios de velocidad (FR-TER-015)
- [ ] T034 [US3] Verificar `cripta/modelo/partida.py` → desempate de agenda: confirmar que eventos reprogramados reciben un número de secuencia nuevo incremental para garantizar desempate total por menor número de secuencia (FR-TER-022)
- [ ] T035 [US3] Verificar `cripta/infraestructura/partida_log.py`: confirmar que los movimientos, esperas y ataques de los cazadores no generan ninguna línea en `partida.log`; añadir prueba de regresión en `test_cazador_decisiones.py` que verifique el log tras un turno completo del cazador (FR-TER-021, FR-TER-023)

**Punto de verificación Fase C**: `py -m unittest tests.modelo.test_buscador_rutas tests.modelo.test_cazador_decisiones tests.aceptacion.test_cazador_persecucion` → todos en OK.

---

## Fase D: Mediciones `--bench`

> [!NOTE]
> Depende de que Fase B y Fase C estén completas. Puede iniciarse en paralelo con Fase E si las cargas ya están registradas y el motor responde.

**Objetivo**: Implementar las cargas sintéticas `ruta_cazador` e `invalidacion` con sus alternativas descartadas; medir las cargas de regresión `ciclo`, `agenda` e `historial`; documentar los resultados.

### D.1 — Cargas nuevas

- [ ] T036 [P] [US2] Modificar `cripta/bench/cargas_bench.py`: registrar carga `ruta_cazador` con cripta sintética determinista de 400 salas generada por `random.Random(42)`, costos de salidas entre 10 y 250, escenarios `H=1,10,30` cazadores y rangos `R=100` y `R=500`; implementar también el **Alternativa Descartada** (cálculo individual desde cada cazador) para medir en el mismo benchmark (FR-TER-020; plan §1 y §3)

  Comando exacto: `py -m cripta --bench --solo ruta_cazador`

- [ ] T037 [P] [US2] [US3] Modificar `cripta/bench/cargas_bench.py`: registrar carga `invalidacion` con 20 cazadores durante 100 ticks, escenario puertas estables y escenario 5 puertas con cierre automático cada 15 ticks; implementar también la **Alternativa Descartada** (recalcular siempre en cada turno de cazador) (FR-TER-020; plan §4)

  Comando exacto: `py -m cripta --bench --solo invalidacion`

- [ ] T038 [US2] Modificar `cripta/servicios/servicio_bench.py`: habilitar la ejecución de las cargas `ruta_cazador` e `invalidacion` y reportar las métricas definidas en el plan (tiempo por ciclo, número de ejecuciones de Dijkstra, razón compartido/individual) (FR-TER-020)

### D.2 — Cargas de regresión de la Parte I

- [ ] T039 [P] Ejecutar y documentar las mediciones de regresión de la Parte I con las nuevas cargas activas:

  Comandos exactos:
  ```powershell
  py -m cripta --bench --solo ciclo
  py -m cripta --bench --solo agenda
  py -m cripta --bench --solo historial
  ```
  Registrar los resultados en `docs/DECISIONES.md` indicando si se mantienen dentro de los límites (ciclo `< 20 ms`, agenda, historial); si algún límite se supera, documentar como límite conocido y notificar al responsable de la capacidad 004 (FR-TER-020; plan §3 de bench)

**Punto de verificación Fase D**: Las tres cargas de regresión terminan sin errores y los resultados quedan documentados.

---

## Fase E: Cierre y Verificación Final

> [!NOTE]
> Depende de que todas las Fases A–D estén completas. Puede iniciarse parcialmente en paralelo (T040 y T041 no dependen entre sí).

**Objetivo**: Garantizar retrocompatibilidad con la Parte I, auditar importaciones prohibidas, verificar reproducción con `--replay` y registrar la invocación en `PROMPTS_LLM.md`.

- [ ] T040 [P] Ejecutar la suite completa de la Parte I y confirmar que las 222 pruebas terminan en `OK`:

  Comando exacto: `py -m unittest discover -s tests -t .`

  Si alguna prueba falla, corregir la regresión antes de avanzar (Principio VIII de la Constitución; plan §"Restricciones")

- [ ] T041 [P] Ejecutar la auditoría de importaciones prohibidas en el modelo y estructuras:

  Comando exacto:
  ```powershell
  Select-String -Path cripta\modelo\*.py, cripta\estructuras\*.py -Pattern "heapq|bisect|collections|networkx"
  ```
  Resultado esperado: sin coincidencias. Revisar manualmente los usos de `dict` y `set` en la revisión del Pull Request, ya que la búsqueda de texto no distingue usos permitidos (Principio I de la Constitución; quickstart §4)

- [ ] T042 Ejecutar reproducción de partida de ejemplo con `--replay` para verificar compatibilidad hacia atrás (Principio VIII):

  Comando exacto: `py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log`

  Resultado esperado: código de salida `0`. **Prerequisito**: ejecutar con los fixtures originales respaldados (T016) si se regeneraron en T017 (quickstart §6)

- [ ] T043 Registrar en `PROMPTS_LLM.md` la invocación del comando `/speckit-tasks` para esta funcionalidad, incluyendo fecha, herramienta, prompt textual y propósito de uso (Flujo de Trabajo — Bitácora de Prompts de la Constitución)

---

## Dependencias y Orden de Ejecución

### Dependencias entre fases

```
Fase A ──► Fase B ──► Fase C ──► Fase D ──► Fase E
│                                             │
└─────────────────────────────────────────────┘
  (Fase A también desbloquea cap. 002, 003, 004)
```

- **Fase A** (contrato de datos): Sin dependencias previas — puede iniciarse de inmediato. Es el primer Pull Request.
- **Fase B** (terreno): Depende de que Fase A esté fusionada en `main` (`SalidaDTO.costo` disponible).
- **Fase C** (cazador): Depende de Fase A fusionada (`EnemigoDTO.rango`) y Fase B completada (costos en movimiento).
- **Fase D** (`--bench`): Depende de Fase B y C completas (el motor debe estar operativo con cazadores y costos).
- **Fase E** (cierre): Depende de Fase A–D completas.

### Dependencias entre historias de usuario

| Historia | Prioridad | Puede iniciar tras... |
|---|---|---|
| US4 — Contrato de datos | P2 | Nada (es la Fase A) |
| US1 — Movimiento y costos | P1 | Fase A fusionada |
| US2 — Cazador (persecución) | P1 | Fase A fusionada + Fase B completa |
| US3 — Cazador (desempates y puertas) | P2 | Fase C implementada (US2) |

### Dependencias dentro de cada fase

- En Fase A: T001 → T002–T006 (pruebas en paralelo) → T007–T015 (implementación, algunos en paralelo) → T016 → T017
- En Fase B: T018 → T019–T020 (en paralelo) → T021–T025 (en secuencia lógica)
- En Fase C: T026–T028 (pruebas en paralelo) → T029–T030 (en paralelo) → T031 → T032 → T033 → T034–T035
- En Fase D: T036–T037 (en paralelo) → T038 → T039
- En Fase E: T040–T041 (en paralelo) → T042 → T043

### Oportunidades de paralelización

```powershell
# Fase A — pruebas de DTOs (en paralelo, archivos distintos):
# T002: tests/dto/test_salida_dto.py
# T003: tests/dto/test_enemigo_dto.py
# T004: tests/dto/test_llave_ubicacion_dto.py
# T005: tests/infraestructura/test_cliente_offline_llaves.py
# T006: tests/infraestructura/test_cache_llaves.py

# Fase A — implementación de DTOs e infraestructura (en paralelo):
# T007: cripta/dto/salida_dto.py
# T008: cripta/dto/enemigo_dto.py
# T009: cripta/dto/llave_ubicacion_dto.py
# T011: cripta/infraestructura/cliente_http.py
# T012: cripta/infraestructura/cliente_offline.py
# T014: cripta/infraestructura/cache.py
# T015: cripta/infraestructura/serializacion.py

# Fase C — pruebas del cazador (en paralelo):
# T026: tests/modelo/test_buscador_rutas.py
# T027: tests/modelo/test_cazador_decisiones.py
# T028: tests/aceptacion/test_cazador_persecucion.py

# Fase D — cargas bench (en paralelo):
# T036: carga ruta_cazador
# T037: carga invalidacion

# Fase E — auditoría y suite Parte I (en paralelo):
# T040: py -m unittest discover
# T041: Select-String prohibiciones
```

---

## Estrategia de Implementación

### Primer Pull Request (Fase A únicamente)

1. Completar Fase A: infraestructura de pruebas → pruebas de DTOs e infraestructura → implementación → fixtures
2. **Punto de corte**: Fase A aprobada en revisión → abrir PR a `main` y fusionar
3. Las capacidades 002, 003 y 004 pueden comenzar en paralelo tras la fusión

### Incremento principal (Fases B y C)

4. Completar Fase B (terreno) sobre la rama actual
5. Completar Fase C (cazador) encadenada
6. Validar con `py -m unittest discover -s tests -t .` → 222 + nuevas pruebas en OK

### Validación de rendimiento y cierre (Fases D y E)

7. Completar Fase D: cargas `--bench` y resultados documentados
8. Completar Fase E: auditoría, `--replay` y `PROMPTS_LLM.md`
9. Abrir segundo Pull Request con Fases B–E

---

## Notas

- Las tareas marcadas **[P]** tocan archivos distintos y no dependen entre sí dentro de su bloque: pueden asignarse a colaboradores diferentes o ejecutarse en paralelo en la misma sesión de trabajo.
- Ninguna tarea incluye `git commit`, `git push` ni mensajes de commit con identificadores de tarea ni nombres de personas.
- Las prohibiciones de la Constitución aplican a toda tarea: sin `heapq`, `bisect`, `collections`, `networkx`, `set` ni `dict` como índice o caché, y sin `list.sort()` ni `sorted()` en las estructuras evaluadas.
- Los errores de programación interna heredan de `IndexError` o `ValueError` en su propio módulo; `CriptaDatosInvalidosError` y `CriptaApiError` se reservan para datos externos.
- Todas las carpetas nuevas de pruebas (`tests/dto/`, `tests/aceptacion/`) requieren un `__init__.py` explícito (T001, T018).
