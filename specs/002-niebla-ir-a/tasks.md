# Tareas: Niebla de guerra e «Ir a»

**Entrada**: `specs/002-niebla-ir-a/spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md` y `contracts/`.

Cada tarea cita FR, ruta, estado actual de la ruta, comando de validación y criterio de hecho. Las tareas están acotadas a un cambio revisable de hasta unos 90 minutos. Las pruebas se escriben antes de la implementación correspondiente.

## Fase A: Dominio puro del conocimiento

**Objetivo**: mantener el conocimiento consultable y reversible en el modelo, sin red, disco ni vista.

- [ ] T001 Prueba de estado inicial, explorada/avistada/desconocida y proyección sin filtraciones, cubriendo el escenario de aceptación 1.1; atiende FR-NIE-001, FR-NIE-003, FR-NIE-008; ruta `tests/modelo/test_conocimiento_jugador.py` (Nuevo); validar con `py -m unittest tests.modelo.test_conocimiento_jugador`; hecho cuando comprueba los tres estados y que datos ocultos no aparecen.
- [ ] T002 Prueba de datos de sala explorada y memoria de puerta ante cambio real no observado, cubriendo los escenarios de aceptación 1.2 y 1.5; atiende FR-NIE-002, FR-NIE-004; ruta `tests/modelo/test_conocimiento_jugador.py` (Nuevo); validar con `py -m unittest tests.modelo.test_conocimiento_jugador`; hecho cuando verifica nombre, salidas, costos y última observación desde cualquiera de los extremos.
- [ ] T003 Prueba de revelación por antorcha al entrar, incluyendo salidas cerradas, sin contenido ni activación de amenazas, retención al apagar y sin revelar al solo encender, cubriendo los escenarios 2.1, 3.15 y 3.16; atiende FR-NIE-005, FR-NIE-022, FR-NIE-023; ruta `tests/modelo/test_conocimiento_jugador.py` (Nuevo); validar con `py -m unittest tests.modelo.test_conocimiento_jugador`; hecho cuando verifica esos límites de revelación.
- [ ] T004 Prueba de inversas puntuales de salas y puertas reveladas, cierre observado desde sala vecina y restauración tras pergamino, cubriendo los escenarios 2.2 y 3.17; atiende FR-NIE-004, FR-NIE-005, FR-NIE-024; ruta `tests/modelo/test_conocimiento_jugador.py` (Nuevo); validar con `py -m unittest tests.modelo.test_conocimiento_jugador`; hecho cuando las celdas vuelven a sus valores previos sin copia completa del mapa.
- [ ] T005 Crear `cripta/modelo/conocimiento_jugador.py` (Nuevo) con estados, observaciones, revelación, proyección e inversas por celda usando listas contiguas indexadas por entero y las estructuras reversibles existentes; atiende FR-NIE-001 a FR-NIE-005, FR-NIE-008, FR-NIE-022 a FR-NIE-024; validar con `py -m unittest tests.modelo.test_conocimiento_jugador`; hecho cuando pasan T001–T004 y el módulo no importa red, archivos ni vista.

## Fase B: Integración con la partida

**Objetivo**: integrar el conocimiento con entradas, antorcha, cierres observables, pergamino y proyección lógica.

- [ ] T006 Prueba de entrada ordinaria, observación de puertas y revelación de vecinas, y de cierre automático observado desde una sala conectada; atiende FR-NIE-002, FR-NIE-004, FR-NIE-015; ruta `tests/modelo/test_conocimiento_jugador.py` (Nuevo); validar con `py -m unittest tests.modelo.test_conocimiento_jugador`; hecho cuando la memoria solo cambia al observar desde un extremo.
- [ ] T007 Integrar creación, entradas y antorcha con `ConocimientoJugador` en `cripta/modelo/partida.py` (Modificado); atiende FR-NIE-001 a FR-NIE-005, FR-NIE-022 a FR-NIE-024; validar con `py -m unittest tests.modelo.test_conocimiento_jugador`; hecho cuando entradas observan puertas, la antorcha revela según spec y pergamino revierte la entrada y sus cambios de conocimiento.
- [ ] T008 Exponer la proyección lógica del conocimiento en `EstadoPartida` dentro de `cripta/modelo/partida.py` (Modificado); atiende FR-NIE-006; validar con `py -m unittest tests.modelo.test_conocimiento_jugador`; hecho cuando estados lógicos e historia consultable conservan los valores del conocimiento sin definir codificación binaria.
- [ ] T009 Crear el paquete `tests/aceptacion/__init__.py` (Nuevo); atiende FR-NIE-005, FR-NIE-009, FR-NIE-013, FR-NIE-015, FR-NIE-017, FR-NIE-024; validar con `py -m unittest discover -s tests/aceptacion -t .`; hecho cuando unittest descubre los casos de aceptación.
- [ ] T010 Prueba automatizada de seis casos del Apéndice B: B-NIE-001 destino no explorado, B-NIE-002 puerta recordada abierta que cierra, B-NIE-003 enemigo dormido, B-NIE-004 antorcha sin activar contenido, B-NIE-005 reversión de antorcha y B-NIE-006 pergamino durante viaje; atiende FR-NIE-005, FR-NIE-009, FR-NIE-013, FR-NIE-015, FR-NIE-017, FR-NIE-024; ruta `tests/aceptacion/test_niebla_ir_a.py` (Nuevo); validar con `py -m unittest tests.aceptacion.test_niebla_ir_a`; hecho cuando cada caso tiene una aserción automatizada sobre su resultado descrito.
- [ ] T011 [P] Prueba de proyección lógica del conocimiento e historial, dejando la codificación binaria expresamente bloqueada por decisión de la 004; atiende FR-NIE-006; ruta `tests/servicios/test_servicio_partida_guardado.py` (Modificado); validar con `py -m unittest tests.servicios.test_servicio_partida_guardado`; hecho cuando prueba solo el estado lógico disponible y deja anotado que guardar/cargar binario no se valida aún.

## Fase C: Ruta y viaje

**Objetivo**: calcular rutas únicamente con conocimiento y ejecutar el viaje como movimientos ordinarios paso a paso.

- [ ] T012 [P] Pruebas unitarias de costo mínimo, puertas no observadas/cerradas, desempate por menor id, destino inválido, destino actual y ausencia de ruta inicial, cubriendo escenarios 3.1, 3.2, 3.9, 3.12 y 3.14; atiende FR-NIE-009, FR-NIE-010, FR-NIE-014, FR-NIE-019, FR-NIE-021; ruta `tests/modelo/test_ir_a.py` (Nuevo); validar con `py -m unittest tests.modelo.test_ir_a`; hecho cuando cada caso comprueba primer paso o rechazo sin efectos.
- [ ] T013 Implementar búsqueda de costo mínimo propia con `HeapMinimo` en `cripta/modelo/ruta_conocida.py` (Nuevo), usando listas indexadas y desempate por menor id; **Depende de 001**: requiere `esta_vacio` y `__len__` en `HeapMinimo`; atiende FR-NIE-008, FR-NIE-010, FR-NIE-012, FR-NIE-014; validar con `py -m unittest tests.modelo.test_ir_a`; hecho cuando T012 pasa, la búsqueda solo consulta conocimiento y no abre puertas.
- [ ] T014 Pruebas del ciclo de viaje para acción ordinaria, tiempo/eventos entre pasos, recálculo tras cierre observado, enemigos vivos al entrar, daño y motivos concurrentes en orden fijo, enemigo inicial y sin continuación tras pergamino, cubriendo escenarios 3.3 a 3.8, 3.10, 3.11 y 3.13; atiende FR-NIE-011 a FR-NIE-013, FR-NIE-015, FR-NIE-017, FR-NIE-020; ruta `tests/controlador/test_controlador_cripta.py` (Modificado); validar con `py -m unittest tests.controlador.test_controlador_cripta`; hecho cuando cada condición de detención queda cubierta y los pasos usan la ruta ordinaria del servicio.
- [ ] T015 Implementar validaciones, bucle de viaje, recálculo por paso, motivos de detención ordenados y cancelación al intercalarse otra acción en `cripta/controlador/controlador_cripta.py` (Modificado); atiende FR-NIE-009 a FR-NIE-015, FR-NIE-017, FR-NIE-019 a FR-NIE-021; validar con `py -m unittest tests.controlador.test_controlador_cripta`; hecho cuando las órdenes inválidas no producen pasos/tiempo y los viajes válidos paran según spec.
- [ ] T016 Proyectar conocimiento de partida sin leer datos ocultos y entregar al controlador el paso/motivos de ruta en `cripta/modelo/partida.py` (Modificado); atiende FR-NIE-008, FR-NIE-010 a FR-NIE-015; validar con `py -m unittest tests.modelo.test_ir_a`; hecho cuando el modelo devuelve datos y resultados sin texto de interfaz ni importaciones de red, archivos o vista.

## Fase D: Registro y vista

**Objetivo**: registrar la orden y sus pasos, presentar el mapa conocido y mostrar el motivo de detención.

- [ ] T017 [P] Pruebas de comentario `#` una sola vez antes del primer movimiento, acciones individuales, sin comentario si no hay pasos y replay que omite el comentario; atiende FR-NIE-016; ruta `tests/infraestructura/test_partida_log.py` (Modificado); validar con `py -m unittest tests.infraestructura.test_partida_log`; hecho cuando verifica orden, cantidad y reproducción de registros.
- [ ] T018 Adaptar escritor, lector y replay de `partida.log` para tratar el comentario de viaje como metadato no accionable; rutas `cripta/servicios/servicio_partida.py` (Modificado), `cripta/infraestructura/partida_log.py` (Modificado), `cripta/servicios/servicio_replay.py` (Modificado); atiende FR-NIE-016; validar con `py -m unittest tests.infraestructura.test_partida_log tests.servicios.test_servicio_replay`; hecho cuando el comentario antecede al primer paso una vez y replay reproduce solo acciones.
- [ ] T019 [P] Prueba del comando de mapa conocido y motivo mostrado, sin consumo de tiempo ni registro; atiende FR-NIE-007, FR-NIE-008; ruta `tests/vista/test_vista_consola.py` (Modificado); validar con `py -m unittest tests.vista.test_vista_consola`; hecho cuando la presentación contiene solo la proyección recibida.
- [ ] T020 Implementar presentación del mapa conocido y motivo de detención en `cripta/vista/vista_consola.py` (Modificado); atiende FR-NIE-007, FR-NIE-008, FR-NIE-013; validar con `py -m unittest tests.vista.test_vista_consola`; hecho cuando la vista no consulta mapa real ni calcula rutas.

## Fase E: Mediciones `--bench`

**Objetivo**: medir rutas, revelación y reversión sin instanciar la vista y sin fijar cifras antes de ejecutar el benchmark.

- [ ] T021 Implementar pruebas de equivalencia de resultados entre ruta con heap y selección lineal del harness, incluida elección dinámica del fixture con mayor total de salas; atiende FR-NIE-018, SC-NIE-002, SC-NIE-004; ruta `tests/servicios/test_servicio_bench.py` (Nuevo); validar con `py -m unittest tests.servicios.test_servicio_bench`; hecho cuando compara ambos algoritmos sobre consultas idénticas y no fija id de cripta.
- [ ] T022 Implementar carga `niebla_rutas` con selección lineal, `random.Random(semilla)` propio, revelación incremental y reversión frente a referencias en `cripta/bench/cargas_bench.py` (Modificado); atiende FR-NIE-018, SC-NIE-002, SC-NIE-004; validar con `py -m cripta --bench --solo niebla_rutas --escala 1`; hecho cuando informa medidas observadas y datos del fixture seleccionado por total de salas.
- [ ] T023 Registrar `niebla_rutas` en `cripta/servicios/servicio_bench.py` (Modificado), manteniendo `--bench` sin vista; atiende FR-NIE-018, SC-NIE-004; validar con `py -m cripta --bench --solo niebla_rutas --escala 1`; hecho cuando el comando ejecuta la carga y reporta tiempos medidos sin resultados prefijados.
- [ ] T024 Medir búsqueda, alternativa lineal, revelación e inversas con el comando exacto `py -m cripta --bench --solo niebla_rutas --escala 1`; atiende FR-NIE-018, SC-NIE-002, SC-NIE-004; ruta de evidencia `specs/002-niebla-ir-a/tasks.md` (Modificado); hecho cuando la salida real permite comprobar el umbral de 5 ms, informa entorno, semilla/configuración, número de salas/salidas, mediana y máximo sin escribir cifras anticipadas.

## Fase F: Cierre

**Objetivo**: conservar compatibilidad, auditar límites y documentar decisiones pendientes.

- [ ] T025 Ejecutar la suite de Parte I después de la integración con `py -m unittest discover -s tests -t .`; atiende FR-NIE-006, FR-NIE-011, FR-NIE-017, SC-NIE-005; ruta de validación `tests/` (existente); hecho cuando las pruebas existentes de Parte I terminan correctamente.
- [ ] T026 Auditar importaciones y usos prohibidos en rutas nuevas o modificadas: `cripta/modelo/conocimiento_jugador.py` (Nuevo), `cripta/modelo/ruta_conocida.py` (Nuevo), `cripta/bench/cargas_bench.py` (Modificado), `cripta/servicios/servicio_bench.py` (Modificado); atiende FR-NIE-008, FR-NIE-010, FR-NIE-018; validar con `rg -n 'heapq|bisect|collections|networkx|\.sort\(|sorted\(|\b(set|dict)\b' cripta/modelo/conocimiento_jugador.py cripta/modelo/ruta_conocida.py cripta/bench/cargas_bench.py cripta/servicios/servicio_bench.py`; hecho cuando no hay estructuras o importaciones prohibidas y se verifica que `--replay` y `--bench` no instancian la vista.
- [ ] T027 **Bloqueada por decisión de 004**: completar prueba de guardar/cargar el conocimiento y línea de tiempo cuando se decida quién incorpora el campo y con qué versión; **Depende de 004** (codificación binaria); atiende FR-NIE-006, SC-NIE-005; ruta `tests/servicios/test_servicio_partida_guardado.py` (Modificado); comando previsto `py -m unittest tests.servicios.test_servicio_partida_guardado`; hecho cuando la decisión de 004 está documentada y la prueba confirma restauración del conocimiento, sin definir aquí bytes ni formato.
- [ ] T028 Añadir la sección de decisiones de implementación y resultados medidos a `docs/DECISIONES.md` (Nuevo); atiende FR-NIE-018, SC-NIE-004; validar con `py -m cripta --bench --solo niebla_rutas --escala 1`; hecho cuando registra solo decisiones acordes con los documentos y cifras obtenidas al ejecutar las mediciones.

## Dependencias y orden de ejecución

- Fase A precede a B; B precede a C; C precede a D; D precede a E; E precede al cierre de F.
- En F, la suite de Parte I y la auditoría se ejecutan después de la integración. T027 queda bloqueada hasta resolver la coordinación con 004.
- Las tareas de ruta que usan los métodos pendientes de `HeapMinimo` llevan **Depende de 001**. El punto de corte de este Pull Request es después de Fase E y la revisión del cierre aplicable; no puede fusionarse antes del PR de 001 y de traer sus cambios a esta rama. T027 no bloquea el corte de código mientras siga pendiente la decisión de 004.
- No hay ejecución paralela marcada: las pruebas iniciales y sus implementaciones comparten archivo de prueba, y las fases dependen de la anterior. Solo se marcarán [P] cuando se puedan trabajar tareas en archivos distintos sin dependencia pendiente.

## Estrategia de implementación

Primero completar Fase A y validar el dominio puro; continuar en orden por B, C y D. Fase E compara algoritmos y registra resultados medidos. El alcance mínimo revisable es Fases A–B: conocimiento observable, antorcha e integración lógica reversible. La funcionalidad de viaje requiere completar C–D. El cierre requiere conservar Parte I y revisar mediciones; el guardado binario se mantiene bloqueado por 004.

## Cobertura independiente

- Historia 1 y SC-NIE-001: T001–T004, T019–T020; `py -m unittest tests.modelo.test_conocimiento_jugador tests.vista.test_vista_consola`.
- Historia 2 y SC-NIE-001/005: T003–T011; `py -m unittest tests.modelo.test_conocimiento_jugador tests.aceptacion.test_niebla_ir_a`.
- Historia 3 y SC-NIE-002/003: T009, T012–T018; `py -m unittest tests.modelo.test_ir_a tests.controlador.test_controlador_cripta tests.infraestructura.test_partida_log`.
- SC-NIE-004: T021–T024; `py -m cripta --bench --solo niebla_rutas --escala 1`.
- SC-NIE-005: T004, T008, T011 y T027; la parte de guardar/cargar está bloqueada por la decisión de 004.
