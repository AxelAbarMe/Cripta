---

description: "Lista de tareas para la implementación de la Verificación de Resolubilidad"
---

# Tareas: Verificación de Resolubilidad (003-resolubilidad)

**Entrada**: Documentos de diseño en `specs/003-resolubilidad/`

**Requisitos previos**: `plan.md` (requerido), `spec.md` (requerido), `research.md`, `data-model.md`, `contracts/contrato_resolubilidad.md`, `quickstart.md`

**Principio**: Las pruebas se escriben **antes** del código que las hace pasar (TDD estricto).
Cada tarea cita el o los `FR-RES-NNN` que atiende, la ruta real del archivo que toca
(marcada **Modificado**), el comando de prueba que la valida y el criterio de "hecho".

**Restricciones que toda tarea respeta**:
- Sin `heapq`, `bisect`, `collections`, `networkx`, `set` ni `dict` como índice/caché/tabla.
- Sin `list.sort()` ni `sorted()`. Solo `list` como almacenamiento contiguo indexado por entero.
- Se reutilizan `Cola` (`cripta/estructuras/cola.py`), `HeapMinimo` (`cripta/estructuras/heap_min.py`),
  `ordenar_auto` / `Ordenamiento.merge_sort` (`cripta/estructuras/ordenamientos.py`) y
  `ordenamiento_selector.py`.
- Errores de programación heredan de `IndexError` o `ValueError`; `CriptaError` solo para fallos externos.
  Se reutilizan `CriptaDatosInvalidosError` y `CriptaLimiteError` sin redefinirlos.
- El modelo no importa red ni archivos; `--verificar` y `--bench` no instancian la vista.
- Sin commits ni push dentro de las tareas.

## Formato: `[ID] [P?] [HistoriaUS?] Descripción con ruta`

- **[P]**: puede ejecutarse en paralelo con otra tarea del mismo bloque (distintos archivos, sin dependencias sin cumplir).
- **[US1]–[US5]**: a qué historia de usuario de `spec.md` pertenece la tarea.
- Orden de dependencias entre fases: **A → B → C**, **A → D** (D puede avanzar en paralelo con B y C) y **E** al final, cuando A, B, C y D estén completas.

---

## Fase A — Dominio puro (modelo + pruebas)

**Propósito**: Implementar y verificar `cripta/modelo/resolubilidad.py` de forma completamente
aislada de red, disco y vista. Las pruebas van primero.

**Punto de corte / PR**: Cuando todas las tareas A estén en ✅ y `py -m unittest tests.modelo.test_resolubilidad` pase sin errores, se cierra el PR de Fase A.

> **⚠️ CRÍTICO**: Las tareas de prueba (T001 a T004) se escriben y deben **fallar** antes de implementar el código (T005 a T009).

---

### Pruebas de dominio — se escriben primero

- [ ] T001 [P] [US1][US2][US3] Crear el esqueleto de `tests/modelo/test_resolubilidad.py` con los fixtures sintéticos reutilizables (cripta lineal simple, cripta con ciclo, cripta con enemigo errante, cripta con varios órdenes válidos); todos los casos de prueba del bloque T002–T004 se colocan en este archivo — **Nuevo**: `tests/modelo/test_resolubilidad.py`
  - Requisitos: FR-RES-001 a FR-RES-012, FR-RES-018, FR-RES-019, FR-RES-022, SC-003, SC-004
  - Comando: `py -m unittest tests.modelo.test_resolubilidad`
  - Hecho: el archivo existe, `discover` lo encuentra, todos los casos fallan con `ImportError` o `AttributeError` (aún no hay implementación).

- [ ] T002 [US1][US2] Escribir casos de prueba del recorrido incremental básico en `tests/modelo/test_resolubilidad.py`: cripta resoluble directa, llaves no consumibles, trampas no bloquean, puerta abierta a sala_salida sin llave_salida = NO resoluble (caso límite de spec.md), cripta desconectada sin puertas, sala inicial sin salidas transitables, llave_salida inmediatamente accesible — **Modificado**: `tests/modelo/test_resolubilidad.py`
  - Requisitos: FR-RES-001, FR-RES-002, FR-RES-003, FR-RES-006, SC-004
  - Comando: `py -m unittest tests.modelo.test_resolubilidad`
  - Hecho: todos los métodos de este bloque existen en el archivo y fallan (implementación ausente).

- [ ] T003 [US3][US4][US5] Escribir casos de prueba de diagnóstico, determinismo y enemigos en `tests/modelo/test_resolubilidad.py`: llave de salida tras su propia puerta (Apéndice B), llaves obtenibles del campo `suelta` de cualquier enemigo (Apéndice B), varios órdenes válidos producen misma secuencia (Apéndice B, SC-003), cadena doble de ciclos independientes, puerta cerrada sin llave, llave exigida sin ubicación (FR-RES-022), puertas bilaterales (FR-RES-019) — **Modificado**: `tests/modelo/test_resolubilidad.py`
  - Requisitos: FR-RES-005, FR-RES-007, FR-RES-008, FR-RES-009, FR-RES-010, FR-RES-011, FR-RES-012, FR-RES-019, FR-RES-022, SC-003, SC-004
  - Comando: `py -m unittest tests.modelo.test_resolubilidad -k ApendiceB`
  - Hecho: métodos nombrados con sufijo `_ApendiceB` existen y fallan.

- [ ] T004 [US1][US3] Escribir casos de prueba del recorrido incremental único (`FR-RES-018`) y de la alternativa ingenua `verificar_ingenuo_reiniciado` en `tests/modelo/test_resolubilidad.py`: ambos métodos producen el mismo `ResultadoResolubilidad.es_resoluble` sobre la misma cripta; `verificar_ingenuo_reiniciado` existe como método separado — **Modificado**: `tests/modelo/test_resolubilidad.py`
  - Requisitos: FR-RES-018, FR-RES-020
  - Comando: `py -m unittest tests.modelo.test_resolubilidad`
  - Hecho: métodos existen y fallan por `AttributeError`.

---

### Implementación del módulo de dominio

- [ ] T005 Implementar entidades de datos inmutables en `cripta/modelo/resolubilidad.py`: `ResultadoResolubilidad` (`frozen=True, slots=True`; atributos: `es_resoluble: bool`, `llaves_obtenidas: tuple[str,...]`, `llaves_no_obtenibles: tuple[str,...]`, `frontera_bloqueada: tuple[FronteraBloqueadaPuerta,...]`, `ubicaciones_llaves: tuple[UbicacionLlaveDiagnostico,...]`, `ciclos_dependencia: tuple[CicloDependenciaLlaves,...]`, `motivo_no_resoluble: str | None`; método `reporte_texto() -> str`), `FronteraBloqueadaPuerta`, `CicloDependenciaLlaves` (método `formato() -> str`), `UbicacionLlaveDiagnostico` (estados `"obtenible"`, `"no_obtenible"`, `"sin_ubicacion"`) — **Nuevo**: `cripta/modelo/resolubilidad.py`
  - Requisitos: FR-RES-007, FR-RES-008, FR-RES-009, FR-RES-010, FR-RES-011, FR-RES-012
  - Comando: `py -m unittest tests.modelo.test_resolubilidad`
  - Hecho: las cuatro clases de datos pueden importarse; los tests de instanciación directa pasan.

- [ ] T006 Implementar catálogo ordenado y búsqueda binaria manual en `cripta/modelo/resolubilidad.py`: función `_busqueda_binaria(catalogo: list[str], clave: str) -> int` (10 líneas, sin `bisect`); función `_construir_catalogo(llaves_salida: str, llaves_puertas: list[str], llaves_ubicaciones: list[str]) -> list[str]` que ordena con `Ordenamiento.merge_sort` de `cripta/estructuras/ordenamientos.py` y deduplica en pasada lineal; tablas contiguas `llave_obtenida`, `puertas_pendientes`, `ubicaciones_por_llave`, `llaves_en_sala`, `visitada` como listas de Python indexadas por entero — **Modificado**: `cripta/modelo/resolubilidad.py`
  - Requisitos: FR-RES-002, FR-RES-003, FR-RES-008 (desempate por menor índice en catálogo ordenado)
  - Comando: `py -m unittest tests.modelo.test_resolubilidad`
  - Hecho: `_busqueda_binaria` y `_construir_catalogo` importables; pruebas de catálogo pasan.

- [ ] T007 Implementar `VerificadorResolubilidad.__init__` y el recorrido incremental único `verificar()` en `cripta/modelo/resolubilidad.py`: recibe `mapa: CriptaMapa`, `sala_inicial: int`, `sala_salida: int`, `llave_salida: str`, `llaves_ubicaciones: tuple[LlaveUbicacionDTO, ...]`; usa `Cola` (`cripta/estructuras/cola.py`) para la cola de salas, `HeapMinimo` (`cripta/estructuras/heap_min.py`) como `candidatas` para elegir la llave de menor identificador al vaciarse la cola; al agotarse candidatas sin cumplir condición de victoria, construye `frontera_bloqueada` y `llaves_no_obtenibles`; bandera `entro_por_llave_salida` según Regla 1 de `data-model.md`; retorna `ResultadoResolubilidad` — **Modificado**: `cripta/modelo/resolubilidad.py`
  - Requisitos: FR-RES-001, FR-RES-002, FR-RES-003, FR-RES-004, FR-RES-005, FR-RES-006, FR-RES-007, FR-RES-008, FR-RES-018
  - Comando: `py -m unittest tests.modelo.test_resolubilidad`
  - Hecho: T002 y T004 pasan; sin uso de `dict`, `set`, `heapq`, `bisect` ni `sort`/`sorted`.

- [ ] T008 Implementar detección de ciclos por DFS tricolor en `cripta/modelo/resolubilidad.py`: función interna `_detectar_ciclos(llaves_no_obtenibles, puertas_pendientes, ubicaciones_por_llave, catalogo)` que (1) hace flood-fill O(V+E) desde frontera bloqueada sobre salas inalcanzables para construir `G_dep` como `list[list[int]]` bipartito (nodos: las llaves no obtenibles y los bloques de salas inalcanzables; aristas bloque→llave exigida por cada puerta que entra al bloque y llave→bloque donde está la llave), (2) ejecuta DFS tricolor con `color: list[int]` del tamaño de ese total de nodos (0=blanco, 1=gris, 2=negro) y `pila_camino: list[int]` como lista contigua sin `deque`, (3) informa cada ciclo solo con llaves (se omiten los bloques) y lo normaliza al menor identificador léxico rotando con índices enteros, (4) ordena ciclos entre grupos por llave menor; retorna `tuple[CicloDependenciaLlaves, ...]` — **Modificado**: `cripta/modelo/resolubilidad.py`
  - Requisitos: FR-RES-009, FR-RES-010, FR-RES-011, FR-RES-012
  - Comando: `py -m unittest tests.modelo.test_resolubilidad`
  - Hecho: T003 pasa (Apéndice B, cadena doble de ciclos, puerta sin llave, llave sin ubicación).

- [ ] T009 Implementar `VerificadorResolubilidad.verificar_ingenuo_reiniciado()` en `cripta/modelo/resolubilidad.py`: alternativa descartada que reinicia un BFS completo desde `sala_inicial` con las llaves disponibles en cada ronda hasta que ninguna pasada descubre llaves nuevas; misma firma de retorno (`ResultadoResolubilidad`) para validación cruzada en `--bench` — **Modificado**: `cripta/modelo/resolubilidad.py`
  - Requisitos: FR-RES-018, FR-RES-020
  - Comando: `py -m unittest tests.modelo.test_resolubilidad`
  - Hecho: T004 pasa; `verificar_ingenuo_reiniciado` produce mismo `es_resoluble` que `verificar` en todos los fixtures.

---

## Fase B — Servicio de aplicación

**Propósito**: Implementar `ServicioResolubilidad`, sus pruebas y la integración con `CacheDisco` y `ContadorSolicitudes`.
Depende de Fase A completa (T001–T009 en ✅).

**Punto de corte / PR**: Cuando `py -m unittest tests.servicios.test_servicio_resolubilidad` pase sin errores, se cierra el PR de Fase B.

---

### Pruebas de servicio — se escriben primero

- [ ] T010 [P] Escribir `tests/servicios/test_servicio_resolubilidad.py` con casos: obtiene llaves por red y persiste en caché, segunda llamada usa caché sin consumir presupuesto, presupuesto agotado antes de llaves lanza `CriptaLimiteError` sin reporte parcial, costos contradictorios en esqueleto lanzan `CriptaDatosInvalidosError`, retorna `ResultadoResolubilidad` completo sobre fixture resoluble — **Nuevo**: `tests/servicios/test_servicio_resolubilidad.py`
  - Requisitos: FR-RES-017, FR-RES-021, FR-RES-023, SC-006, SC-008
  - Comando: `py -m unittest tests.servicios.test_servicio_resolubilidad`
  - Hecho: archivo existe, `discover` lo encuentra, todos los casos fallan por `ImportError`.

---

### Implementación del servicio

- [ ] T011 Implementar `ServicioResolubilidad` en `cripta/servicios/servicio_resolubilidad.py`: recibe `cliente: ClienteCripta`, `contador: ContadorSolicitudes`, `cache_disco: CacheDisco | None = None`; método `verificar(id_cripta: str) -> ResultadoResolubilidad` que (a) obtiene datos generales y esqueleto paginado con `contador`, (b) consulta `cache_disco.leer_llaves` antes de llamar `cliente.obtener_llaves` (clave versionada `cripta.<id>.<ver>.llaves.json`), (c) si presupuesto se agota lanza `CriptaLimiteError`, (d) construye `CriptaMapa` (si lanza `CriptaDatosInvalidosError` propaga sin reporte), (e) instancia `VerificadorResolubilidad` y retorna resultado — **Nuevo**: `cripta/servicios/servicio_resolubilidad.py`
  - Requisitos: FR-RES-017, FR-RES-021, FR-RES-023, SC-006, SC-008
  - Comando: `py -m unittest tests.servicios.test_servicio_resolubilidad`
  - Hecho: T010 pasa; sin importaciones de red en modelo; `ClienteFalso` de `tests/cliente_falso.py` suficiente para los tests.

---

## Fase C — CLI y vista

**Propósito**: Integrar la compuerta en el controlador, el método abstracto en la vista base, la implementación en la vista consola y las banderas `--verificar` / `--forzar` en `__main__.py`.
Depende de Fase B completa.

**Punto de corte / PR**: Cuando `py -m unittest tests.controlador.test_controlador_resolubilidad` pase sin errores, se cierra el PR de Fase C.

---

### Pruebas de controlador — se escriben primero

- [ ] T012 [P] Escribir `tests/controlador/test_controlador_resolubilidad.py` con casos: inicio regular sobre cripta resoluble muestra reporte y arranca partida, inicio regular sobre cripta no resoluble sin `--forzar` aborta sin bucle de simulación (caso del Apéndice B, método con sufijo `_ApendiceB`), el reporte se imprime con el formato del §3 del contrato (métodos con `reporte` en el nombre), inicio regular con `--forzar` muestra advertencia y continúa, `--verificar` llama servicio sin instanciar vista — **Nuevo**: `tests/controlador/test_controlador_resolubilidad.py`
  - Requisitos: FR-RES-013, FR-RES-014, FR-RES-015, FR-RES-016, SC-005
  - Comando: `py -m unittest tests.controlador.test_controlador_resolubilidad`
  - Hecho: archivo existe, todos los casos fallan por `ImportError`.

---

### Implementación de CLI y vista

- [ ] T013 [P] Agregar método abstracto `mostrar_reporte_resolubilidad(resultado: ResultadoResolubilidad, forzada: bool = False) -> None` a `cripta/vista/vista_base.py` — **Modificado**: `cripta/vista/vista_base.py` y las vistas falsas que heredan de `VistaBase` en `tests/controlador/test_controlador_cripta.py` (se les agrega un `mostrar_reporte_resolubilidad` vacío para que sigan instanciándose)
  - Requisitos: FR-RES-013
  - Comando: `py -m unittest discover -s tests -t .`
  - Hecho: `VistaBase` define el método abstracto; `py -c "from cripta.vista.vista_base import VistaBase"` sin error; `py -m unittest discover -s tests -t .` sigue en OK.

- [ ] T014 Implementar `mostrar_reporte_resolubilidad` en `cripta/vista/vista_consola.py`: imprime por `sys.stdout` el reporte formateado según el esquema de `contracts/contrato_resolubilidad.md` §3 (ancho 81 caracteres con `=`, sección de llaves obtenidas o diagnóstico de no resolubilidad, puertas de frontera, ciclos); acepta `forzada: bool` para agregar la advertencia de inicio forzado — **Modificado**: `cripta/vista/vista_consola.py`
  - Requisitos: FR-RES-013, FR-RES-014, FR-RES-015
  - Comando: `py -m unittest tests.controlador.test_controlador_resolubilidad`
  - Hecho: `py -m unittest tests.controlador.test_controlador_resolubilidad -k reporte` pasa y la salida coincide con el formato del §3 del contrato.

- [ ] T015 Integrar verificación en `cripta/servicios/servicio_partida.py`: antes de instanciar `Partida`, invocar `ServicioResolubilidad.verificar(id_cripta)` y adjuntar el `ResultadoResolubilidad` al objeto devuelto al controlador — **Modificado**: `cripta/servicios/servicio_partida.py`
  - Requisitos: FR-RES-013
  - Comando: `py -m unittest tests.controlador.test_controlador_resolubilidad`
  - Hecho: el controlador recibe el resultado sin abrir vista; T012 pasa.

- [ ] T016 Modificar `cripta/controlador/controlador_cripta.py`: aceptar `forzar: bool = False`; en `_iniciar_partida` (o equivalente), obtener `ResultadoResolubilidad` del servicio, llamar `vista.mostrar_reporte_resolubilidad(resultado, forzada=forzar)`; si `not resultado.es_resoluble and not forzar` retornar sin entrar al bucle interactivo — **Modificado**: `cripta/controlador/controlador_cripta.py`
  - Requisitos: FR-RES-013, FR-RES-014, FR-RES-015
  - Comando: `py -m unittest tests.controlador.test_controlador_resolubilidad`
  - Hecho: T012 pasa; las 222 pruebas previas siguen en OK.

- [ ] T017 Agregar banderas `--verificar <id_cripta>` y `--forzar` en `cripta/__main__.py`: si `--verificar` está presente, instanciar `ServicioResolubilidad` con `ClienteOffline` o `ClienteHttp` y `CacheDisco`, llamar `servicio.verificar(id_cripta)`, imprimir `resultado.reporte_texto()` a `sys.stdout`, salir con código `0`/`1`/`2` según contrato §1.1 sin instanciar `VistaConsola`; si no está `--verificar`, pasar `forzar` al controlador — **Modificado**: `cripta/__main__.py`
  - Requisitos: FR-RES-014, FR-RES-015, FR-RES-016, SC-005
  - Comando: `py -m cripta --offline --verificar cripta-02` (sin vista interactiva; requiere que los datos de esa cripta ya estén guardados para --offline, por ejemplo tras descargarla en línea una vez); `py -m unittest tests.controlador.test_controlador_resolubilidad`
  - Hecho: T012 pasa; `--verificar` imprime reporte y sale sin instanciar la vista; `--forzar` pasa la bandera al controlador.

---

## Fase D — Mediciones `--bench`

**Propósito**: Agregar las cargas `resolubilidad` y `resolubilidad_cota` al módulo `cripta/bench/cargas_bench.py`.
Depende de Fase A completa (el verificador ya funciona); puede solaparse con Fase C en la misma rama.

**Punto de corte / PR**: Cuando ambos comandos de bench ejecuten sin error y produzcan salida conforme al formato del plan §5, se cierra el PR de Fase D.

---

- [ ] T018 Implementar generador sintético determinista en `cripta/bench/cargas_bench.py`: función `_generar_cripta_encadenada(k: int, salas_por_segmento: int, semilla: int) -> tuple[CriptaMapa, int, int, str, tuple[LlaveUbicacionDTO,...]]` que construye una cripta de `k` llaves en cadena a través de `k * salas_por_segmento` salas usando `random.Random(semilla)` para ruido aleatorio deterministico (sin `random` global), cada segmento `i` tiene puerta cerrada que requiere llave `k_i` y llave `k_i` en sala lateral; última sala tiene puerta que exige `llave_salida`; sin ningún `dict` ni `set` en la función — **Modificado**: `cripta/bench/cargas_bench.py`
  - Requisitos: FR-RES-020, SC-007
  - Comando: `py -m cripta --bench --solo resolubilidad`
  - Hecho: función importable; generador produce siempre la misma cripta para `SEMILLA_BENCH = 20260928`.

- [ ] T019 Registrar carga `"resolubilidad"` en `CARGAS` dentro de `cripta/bench/cargas_bench.py`: función `bench_resolubilidad(escala: float = 1.0)` que llama `_generar_cripta_encadenada(k, 20, SEMILLA_BENCH)` para al menos tres valores crecientes de `k` (proporcionales a `escala`), ejecuta `VerificadorResolubilidad.verificar()` y `VerificadorResolubilidad.verificar_ingenuo_reiniciado()` cada una 3 veces con `_medir` (así se evidencia el costo aproximadamente lineal, SC-002), reporta con `_comparar` la aceleración sin escribir cifras de rendimiento fijas en el código fuente — **Modificado**: `cripta/bench/cargas_bench.py`
  - Requisitos: FR-RES-018, FR-RES-020, SC-002, SC-007
  - Comando: `py -m cripta --bench --solo resolubilidad`
  - Hecho: salida con formato `=== RESOLUBILIDAD ... ===` y línea `recorrido_ingenuo_reiniciado es N.Nx más lento que recorrido_incremental`.

- [ ] T020 Registrar carga `"resolubilidad_cota"` en `CARGAS` dentro de `cripta/bench/cargas_bench.py`: función `bench_resolubilidad_cota()` que descarga (o lee de `CacheDisco`) la lista de criptas publicadas, elige la de mayor total de salas **sin fijar su id en el código** (Principio IV), ejecuta `VerificadorResolubilidad.verificar()` con `_medir` (se mide solo la verificación, sin contar la descarga de datos) y lo compara contra el límite de 200 ms; imprime `CUMPLE` o `FALLA` — **Modificado**: `cripta/bench/cargas_bench.py`
  - Requisitos: FR-RES-020, SC-001, SC-002
  - Comando: `py -m cripta --bench --solo resolubilidad_cota`
  - Hecho: salida con formato `=== RESOLUBILIDAD_COTA ... ===` indicando `(límite 200.0 ms: CUMPLE)`; el id de cripta se obtiene dinámicamente del catálogo.

---

## Fase E — Cierre y auditoría

**Propósito**: Garantizar compatibilidad retroactiva, auditar importaciones prohibidas y documentar decisiones.
Depende de Fases A–D completas.

**Punto de corte / PR**: Cuando todas las tareas E estén en ✅, la rama está lista para revisión final.

---

- [ ] T021 [P] Ejecutar la suite completa de 222 pruebas de la Parte I y verificar que todas terminan en `OK` — Sin archivos nuevos
  - Requisitos: Principio VIII de la Constitución
  - Comando: `py -m unittest discover -s tests -t .`
  - Hecho: salida `Ran 222+ tests ... OK` (sin errores ni fallos en ninguna prueba preexistente).

- [ ] T022 [P] Auditar importaciones prohibidas con `Select-String` en todos los archivos `.py` de `cripta/` y `tests/`: verificar ausencia de `import heapq`, `import bisect`, `from collections`, `import networkx`, y ausencia de `.sort(` / `sorted(` en módulos evaluados — Sin archivos nuevos
  - Requisitos: Principio I de la Constitución
  - Comando:
    ```powershell
    Select-String -Path (Get-ChildItem cripta,tests -Recurse -Filter *.py).FullName -Pattern "heapq|bisect|collections|networkx|sorted\(|\.sort\("
    ```
  - Hecho: no aparece ninguna importación prohibida; cada `sorted(` o `.sort(` que aparezca se revisa a mano y solo se permite fuera de los ordenamientos evaluados; el uso de `dict` y `set` como índice o caché se revisa en la revisión del Pull Request.

- [ ] T023 Redactar sección `## 003 Verificación de Resolubilidad` en `DECISIONES.md` (en la raíz del repositorio): registrar (a) razón de adoptar recorrido incremental frente a reinicio BFS, (b) razón de búsqueda binaria manual frente a `bisect`, (c) razón de DFS tricolor frente a Tarjan, (d) razón de desempate con `HeapMinimo` propio frente a `sorted()`, (e) límites conocidos (identificadores dispersos, escala de catálogo) según plan §6 — **Modificado**: `DECISIONES.md`
  - Requisitos: Principio VII de la Constitución; plan §6
  - Comando: (ninguno automatizable; revisión manual)
  - Hecho: sección presente, cita las cinco decisiones (a) a (e) y no incluye cifras de rendimiento sin medir.

---

## Dependencias y orden de ejecución

### Dependencias entre fases

```
Fase A (T001–T009)  ──►  Fase B (T010–T011)  ──►  Fase C (T012–T017)
                    │                                        │
                    └──────────────────────────────────────► Fase D (T018–T020)
                                                             │
                                               Fase E (T021–T023)  ◄── requiere A+B+C+D
```

- **Fase A**: Sin dependencias externas — puede iniciar de inmediato.
- **Fase B**: Depende de A completa (necesita `VerificadorResolubilidad` importable).
- **Fase C**: Depende de B completa (necesita `ServicioResolubilidad` y `ResultadoResolubilidad`).
- **Fase D**: Depende de A completa; puede desarrollarse en paralelo con C si hay capacidad.
- **Fase E**: Depende de A, B, C y D completas.

### Dependencias dentro de la Fase A

```
T001 ──► T002 ──► T005 ──► T006 ──► T007 ──► T008 ──► T009
     ──► T003 ──►  │
     ──► T004 ──►  │
                   └── (T005 no depende de T002/T003/T004, solo de T001)
```

> T001–T004 son independientes entre sí una vez T001 existe y se pueden escribir en paralelo [P].
> T005 depende solo de T001 (el archivo debe existir). T006–T009 son secuenciales sobre el mismo archivo.

### Oportunidades de paralelismo

- **[P] dentro de Fase A**: T002, T003 y T004 pueden escribirse simultáneamente (mismo archivo de pruebas, distintos métodos).
- **[P] dentro de Fase B**: T010 puede escribirse mientras se revisan las pruebas de Fase A (distintos archivos).
- **[P] dentro de Fase C**: T012, T013 pueden iniciarse simultáneamente (distintos archivos); T014 espera T013.
- **[P] Fases C y D**: pueden avanzar en paralelo una vez Fase B esté completa.
- **[P] dentro de Fase E**: T021 y T022 pueden ejecutarse simultáneamente.

---

## Ejemplo de ejecución en paralelo — Fase A (pruebas)

```powershell
# Escribir pruebas de distintos bloques en paralelo (distintos desarrolladores / sesiones):
# Sesión 1: T002 — recorrido básico y casos límite
# Sesión 2: T003 — Apéndice B, determinismo, enemigos
# Sesión 3: T004 — verificar_ingenuo_reiniciado

# Validar que todas fallan correctamente (implementación aún ausente):
py -m unittest tests.modelo.test_resolubilidad
# Resultado esperado: FAIL / ERROR en todos los casos (ImportError / AttributeError)
```

---

## Estrategia de implementación

### MVP mínimo viable (Fase A + B)

1. Completar Fase A: modelo puro con pruebas → garantiza el núcleo algorítmico.
2. Completar Fase B: servicio de aplicación → integración con infraestructura existente.
3. **Validar**: `py -m unittest tests.modelo.test_resolubilidad tests.servicios.test_servicio_resolubilidad`

### Entrega incremental

1. **Fase A** → PR: modelo puro funciona de forma totalmente aislada.
2. **Fase B** → PR: servicio integrado con `CacheDisco` y `ContadorSolicitudes`.
3. **Fases C + D** → PR conjunto: CLI, vista y mediciones bench.
4. **Fase E** → PR de cierre: retrocompatibilidad confirmada y decisiones documentadas.

---

## Notas

- `[P]` = tarea puede ejecutarse en paralelo con otra del mismo bloque marcada `[P]`, siempre que toquen archivos distintos.
- Las etiquetas `[US1]`–`[US5]` mapean las historias de usuario de `spec.md` en orden de prioridad.
- Ninguna tarea contiene commits ni push; los hace el humano.
- El registro de este comando en `PROMPTS_LLM.md` se hace fuera de las tareas, según instrucción explícita del usuario.
- Las cifras de rendimiento (`resolubilidad_cota`) se miden y registran en T020 al momento de ejecutar `--bench`; no se fijan en el código fuente.
