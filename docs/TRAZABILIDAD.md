# Matriz de trazabilidad de Cripta 2

Lee cada fila de izquierda a derecha para seguir el requisito o criterio desde su escenario citado hasta las tareas y las rutas que estas mencionan.

Las fuentes de cada capacidad son su **spec.md** y su **tasks.md**. El guion indica que las fuentes no citan el vínculo. Los casos agrupados conservan el alcance de la tarea que los cita. Las rutas de pruebas son las escritas como rutas en las tareas, incluidos los directorios de validación citados. Los comandos unittest que solo nombran módulos no agregan rutas a la matriz.

| Capacidad | Requisitos | Con tarea y prueba | Rutas inexistentes |
| --- | ---: | ---: | ---: |
| Terreno y cazador | 24 | 24 | 1 |
| Niebla de guerra e «ir a» | 25 | 25 | 0 |
| Resolubilidad | 24 | 24 | 0 |
| Línea de tiempo | 23 | 23 | 0 |

## Terreno y cazador

Carpeta `specs/001-terreno-cazador/`. Prefijo `FR-TER-`.

| Requisito | Escenario o caso | Tareas | Código | Pruebas |
| --- | --- | --- | --- | --- |
| `FR-TER-001` | US1-1<br>US1-2<br>US4-1 | T001<br>T002<br>T006b<br>T007<br>T017<br>T019 | `cripta/dto/salida_dto.py` | `tests/aceptacion/test_terreno_costos.py`<br>`tests/datos/`<br>`tests/dto/`<br>`tests/dto/__init__.py`<br>`tests/dto/test_salida_dto.py`<br>`tests/modelo/test_cripta_mapa_costos.py` |
| `FR-TER-002` | US1-1<br>US4-1 | T006b<br>T019<br>T021<br>T021b | `cripta/modelo/cripta_mapa.py`<br>`cripta/modelo/partida.py` | `tests/aceptacion/test_terreno_costos.py`<br>`tests/modelo/test_cripta_mapa_costos.py` |
| `FR-TER-003` | US1-1 | T019<br>T021 | `cripta/modelo/partida.py` | `tests/aceptacion/test_terreno_costos.py` |
| `FR-TER-004` | Apéndice B, caso 6<br>US1-3 | T018<br>T019<br>T020<br>T021<br>T025 | `cripta/modelo/partida.py`<br>`cripta/modelo/reloj.py` | `tests/aceptacion/`<br>`tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_terreno_costos.py`<br>`tests/modelo/test_reloj.py` |
| `FR-TER-005` | Apéndice B, caso 7<br>US1-4 | T018<br>T019<br>T020<br>T022<br>T025 | `cripta/modelo/efectos.py`<br>`cripta/modelo/reloj.py` | `tests/aceptacion/`<br>`tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_terreno_costos.py`<br>`tests/modelo/test_reloj.py` |
| `FR-TER-006` | US1-5 | T019<br>T023<br>T024 | `cripta/modelo/partida.py` | `tests/aceptacion/test_terreno_costos.py` |
| `FR-TER-007` | US1-6 | T019<br>T023 | `cripta/modelo/partida.py` | `tests/aceptacion/test_terreno_costos.py` |
| `FR-TER-008` | — | T001<br>T003<br>T008<br>T017<br>T027<br>T030<br>T032 | `cripta/dto/enemigo_dto.py`<br>`cripta/modelo/comportamiento_enemigo.py`<br>`cripta/modelo/enemigo.py`<br>`cripta/modelo/partida.py` | `tests/datos/`<br>`tests/dto/`<br>`tests/dto/__init__.py`<br>`tests/dto/test_enemigo_dto.py`<br>`tests/modelo/test_cazador_decisiones.py` |
| `FR-TER-009` | US2-1 | T027<br>T028<br>T032 | `cripta/modelo/comportamiento_enemigo.py`<br>`cripta/modelo/partida.py` | `tests/aceptacion/test_cazador_persecucion.py`<br>`tests/modelo/test_cazador_decisiones.py` |
| `FR-TER-010` | Apéndice B, caso 3<br>US2-2 | T026<br>T028<br>T028b<br>T029<br>T031<br>T032 | `cripta/estructuras/heap_min.py`<br>`cripta/modelo/buscador_rutas.py`<br>`cripta/modelo/comportamiento_enemigo.py`<br>`cripta/modelo/partida.py` | `tests/aceptacion/test_cazador_persecucion.py`<br>`tests/estructuras/test_heap_min.py`<br>`tests/modelo/test_buscador_rutas.py` |
| `FR-TER-011` | Apéndice B, caso 1<br>Apéndice B, caso 2<br>US3-2<br>US3-3 | T027<br>T028<br>T031<br>T032 | `cripta/modelo/buscador_rutas.py`<br>`cripta/modelo/comportamiento_enemigo.py`<br>`cripta/modelo/partida.py` | `tests/aceptacion/test_cazador_persecucion.py`<br>`tests/modelo/test_cazador_decisiones.py` |
| `FR-TER-012` | Apéndice B, caso 3<br>US2-2<br>US2-3 | T027<br>T028<br>T030<br>T031<br>T032 | `cripta/modelo/buscador_rutas.py`<br>`cripta/modelo/comportamiento_enemigo.py`<br>`cripta/modelo/enemigo.py`<br>`cripta/modelo/partida.py` | `tests/aceptacion/test_cazador_persecucion.py`<br>`tests/modelo/test_cazador_decisiones.py` |
| `FR-TER-013` | Apéndice B, caso 4<br>US3-1 | T026<br>T028<br>T031<br>T032 | `cripta/modelo/buscador_rutas.py`<br>`cripta/modelo/comportamiento_enemigo.py`<br>`cripta/modelo/partida.py` | `tests/aceptacion/test_cazador_persecucion.py`<br>`tests/modelo/test_buscador_rutas.py` |
| `FR-TER-014` | US3-5 | T027<br>T028<br>T031 | `cripta/modelo/buscador_rutas.py` | `tests/aceptacion/test_cazador_persecucion.py`<br>`tests/modelo/test_cazador_decisiones.py` |
| `FR-TER-015` | Apéndice B, caso 5<br>US3-4 | T026<br>T026b<br>T028<br>T028c<br>T031<br>T033 | `cripta/modelo/buscador_rutas.py`<br>`cripta/modelo/efectos.py`<br>`cripta/modelo/partida.py` | `tests/aceptacion/test_cazador_persecucion.py`<br>`tests/modelo/test_buscador_rutas.py`<br>`tests/modelo/test_equivalencia_rutas.py` |
| `FR-TER-016` | US4-1 | T002<br>T005<br>T006b<br>T007<br>T015 | `cripta/dto/salida_dto.py`<br>`cripta/infraestructura/serializacion.py` | `tests/`<br>`tests/dto/test_salida_dto.py`<br>`tests/infraestructura/test_cliente_offline_llaves.py`<br>`tests/modelo/test_cripta_mapa_costos.py` |
| `FR-TER-017` | — | T003<br>T008<br>T015 | `cripta/dto/enemigo_dto.py`<br>`cripta/infraestructura/serializacion.py` | `tests/dto/test_enemigo_dto.py` |
| `FR-TER-018` | — | T001<br>T001b<br>T004<br>T004b<br>T005<br>T009<br>T009b<br>T010<br>T011<br>T012<br>T013<br>T017 | `cripta/dto/llave_ubicacion_dto.py`<br>`cripta/infraestructura/cliente_general.py`<br>`cripta/infraestructura/cliente_http.py`<br>`cripta/infraestructura/cliente_offline.py`<br>`cripta/infraestructura/puertos.py` | `tests/`<br>`tests/cliente_falso.py`<br>`tests/datos/`<br>`tests/dto/`<br>`tests/dto/__init__.py`<br>`tests/dto/test_llave_ubicacion_dto.py`<br>`tests/infraestructura/test_cliente_offline_llaves.py` |
| `FR-TER-019` | — | T006<br>T014<br>T016 | `cripta/infraestructura/cache.py` | `tests/`<br>`tests/datos/`<br>`tests/infraestructura/test_cache_disco.py`<br>`tests/infraestructura/test_cache_llaves.py`<br>`tests/modelo/test_guardado_ida.py`<br>`tests/modelo/test_guardado_vuelta.py`<br>`tests/modelo/test_pergamino.py`<br>`tests/servicios/test_servicio_partida.py` |
| `FR-TER-020` | — | T036<br>T036b<br>T037<br>T038<br>T039<br>T039b<br>T039c | `cripta/bench/cargas_bench.py`<br>`cripta/modelo/partida.py`<br>`cripta/servicios/servicio_bench.py` | `tests/bench/`<br>`tests/modelo/` |
| `FR-TER-021` | — | T035 | `cripta/infraestructura/partida_log.py` | `tests/infraestructura/test_partida_log.py` |
| `FR-TER-022` | — | T020<br>T022<br>T025<br>T028<br>T034 | `cripta/modelo/efectos.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/reloj.py` | `tests/aceptacion/test_cazador_persecucion.py`<br>`tests/modelo/test_reloj.py` |
| `FR-TER-023` | — | T019b<br>T025b | `cripta/modelo/partida.py` | `tests/controlador/test_controlador_errores.py` |
| `FR-TER-024` | — | T034b<br>T034c | `cripta/modelo/partida.py`<br>`cripta/modelo/resultado_partida.py`<br>`cripta/vista/vista_consola.py` | `tests/modelo/test_vista_partida.py`<br>`tests/vista/test_vista_consola.py` |

| Criterio | Escenario o caso | Tareas | Pruebas |
| --- | --- | --- | --- |
| `SC-001` | — | — | — |
| `SC-002` | — | — | — |
| `SC-003` | Escenarios de aceptación del Apéndice B | — | — |
| `SC-004` | — | — | — |
| `SC-005` | — | — | — |

Rutas citadas que no existen. `fixtures/cripta-01/` (prevista).

## Niebla de guerra e «ir a»

Carpeta `specs/002-niebla-ir-a/`. Prefijo `FR-NIE-`.

| Requisito | Escenario o caso | Tareas | Código | Pruebas |
| --- | --- | --- | --- | --- |
| `FR-NIE-001` | Escenario 1.1<br>Escenario 1.3<br>Escenario 1.4 | T001<br>T006<br>T008 | `cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py` | `tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-002` | B-NIE-002<br>Escenario 1.2<br>Escenario 1.5 | T002<br>T006<br>T007<br>T008 | `cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py` | `tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-003` | Escenario 1.1<br>Escenario 1.3<br>Escenario 1.4 | T001<br>T006<br>T008 | `cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py` | `tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-004` | B-NIE-002<br>Escenario 1.2<br>Escenario 1.5<br>Escenario 2.2<br>Escenario 3.17 | T002<br>T004<br>T006<br>T007<br>T008<br>T009 | `cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/efectos.py`<br>`cripta/modelo/partida.py` | `tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-005` | B-NIE-004<br>B-NIE-005<br>Escenario 2.1<br>Escenario 2.2<br>Escenario 3.15<br>Escenario 3.16<br>Escenario 3.17 | T003<br>T004<br>T006<br>T008<br>T012<br>T013 | `cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py` | `tests/`<br>`tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_niebla_ir_a.py`<br>`tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-006` | — | T010<br>T011<br>T038<br>T040 | `cripta/infraestructura/estado_guardado.py`<br>`cripta/modelo/persistencia_modelo.py` | `tests/`<br>`tests/servicios/test_servicio_partida_guardado.py` |
| `FR-NIE-007` | — | T017<br>T019<br>T020<br>T022<br>T023<br>T024<br>T025<br>T027<br>T029<br>T030 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/resultado_partida.py`<br>`cripta/vista/vista_base.py`<br>`cripta/vista/vista_consola.py` | `tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_ir_a.py`<br>`tests/vista/test_vista_consola.py` |
| `FR-NIE-008` | Escenario 1.1<br>Escenario 1.3<br>Escenario 1.4 | T001<br>T006<br>T016<br>T017<br>T019<br>T020<br>T021<br>T022<br>T023<br>T024<br>T025<br>T027<br>T029<br>T030<br>T039 | `cripta/`<br>`cripta/bench/cargas_bench.py`<br>`cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/resultado_partida.py`<br>`cripta/modelo/ruta_conocida.py`<br>`cripta/servicios/servicio_bench.py`<br>`cripta/servicios/servicio_replay.py`<br>`cripta/vista/vista_base.py`<br>`cripta/vista/vista_consola.py` | `tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_conocimiento_jugador.py`<br>`tests/modelo/test_ir_a.py`<br>`tests/vista/test_vista_consola.py` |
| `FR-NIE-009` | B-NIE-001<br>B-NIE-002<br>B-NIE-003<br>B-NIE-006<br>Escenario 3.1<br>Escenario 3.2<br>Escenario 3.9<br>Escenario 3.12<br>Escenario 3.14 | T012<br>T014<br>T015<br>T017<br>T022<br>T029<br>T030 | `cripta/controlador/controlador_cripta.py`<br>`cripta/vista/vista_consola.py` | `tests/`<br>`tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_niebla_ir_a.py`<br>`tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_ir_a.py`<br>`tests/vista/test_vista_consola.py` |
| `FR-NIE-010` | Escenario 3.1<br>Escenario 3.2<br>Escenario 3.9<br>Escenario 3.12<br>Escenario 3.14 | T015<br>T016<br>T021<br>T022<br>T039 | `cripta/`<br>`cripta/bench/cargas_bench.py`<br>`cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/ruta_conocida.py`<br>`cripta/servicios/servicio_bench.py`<br>`cripta/servicios/servicio_replay.py` | `tests/modelo/test_ir_a.py` |
| `FR-NIE-011` | Escenario 3.3–3.8<br>Escenario 3.10<br>Escenario 3.11<br>Escenario 3.13 | T018<br>T021<br>T022<br>T038 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/partida.py` | `tests/`<br>`tests/controlador/test_controlador_cripta.py` |
| `FR-NIE-012` | Escenario 3.3–3.8<br>Escenario 3.10<br>Escenario 3.11<br>Escenario 3.13 | T016<br>T018<br>T021<br>T022 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/ruta_conocida.py` | `tests/controlador/test_controlador_cripta.py` |
| `FR-NIE-013` | B-NIE-001<br>B-NIE-002<br>B-NIE-003<br>B-NIE-006<br>Escenario 3.3–3.8<br>Escenario 3.10<br>Escenario 3.11<br>Escenario 3.13 | T012<br>T014<br>T018<br>T019<br>T020<br>T021<br>T022<br>T025<br>T027<br>T029<br>T030 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/resultado_partida.py`<br>`cripta/vista/vista_base.py`<br>`cripta/vista/vista_consola.py` | `tests/`<br>`tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_niebla_ir_a.py`<br>`tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_ir_a.py`<br>`tests/vista/test_vista_consola.py` |
| `FR-NIE-014` | Escenario 3.1<br>Escenario 3.2<br>Escenario 3.9<br>Escenario 3.12<br>Escenario 3.14 | T015<br>T016<br>T021<br>T022 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/ruta_conocida.py` | `tests/modelo/test_ir_a.py` |
| `FR-NIE-015` | B-NIE-001<br>B-NIE-002<br>B-NIE-003<br>B-NIE-006<br>Escenario 3.3–3.8<br>Escenario 3.10<br>Escenario 3.11<br>Escenario 3.13 | T007<br>T009<br>T012<br>T014<br>T018<br>T021<br>T022 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/efectos.py`<br>`cripta/modelo/partida.py` | `tests/`<br>`tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_niebla_ir_a.py`<br>`tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-016` | — | T026<br>T028 | `cripta/controlador/controlador_cripta.py`<br>`cripta/infraestructura/partida_log.py`<br>`cripta/servicios/servicio_partida.py`<br>`cripta/servicios/servicio_replay.py` | `tests/controlador/test_controlador_cripta.py`<br>`tests/infraestructura/test_partida_log.py` |
| `FR-NIE-017` | B-NIE-001<br>B-NIE-002<br>B-NIE-003<br>B-NIE-006<br>Escenario 3.3–3.8<br>Escenario 3.10<br>Escenario 3.11<br>Escenario 3.13 | T012<br>T014<br>T018<br>T022<br>T038 | `cripta/controlador/controlador_cripta.py` | `tests/`<br>`tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_niebla_ir_a.py`<br>`tests/controlador/test_controlador_cripta.py` |
| `FR-NIE-018` | — | T031<br>T032<br>T033<br>T034<br>T035<br>T036<br>T037<br>T039<br>T041 | `cripta/`<br>`cripta/bench/cargas_bench.py`<br>`cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/ruta_conocida.py`<br>`cripta/servicios/servicio_bench.py`<br>`cripta/servicios/servicio_replay.py` | `tests/servicios/test_servicio_bench.py` |
| `FR-NIE-019` | Escenario 3.1<br>Escenario 3.2<br>Escenario 3.9<br>Escenario 3.12<br>Escenario 3.14 | T015<br>T017<br>T022 | `cripta/controlador/controlador_cripta.py` | `tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_ir_a.py` |
| `FR-NIE-020` | Escenario 3.3–3.8<br>Escenario 3.10<br>Escenario 3.11<br>Escenario 3.13 | T018<br>T022 | `cripta/controlador/controlador_cripta.py` | `tests/controlador/test_controlador_cripta.py` |
| `FR-NIE-021` | Escenario 3.1<br>Escenario 3.2<br>Escenario 3.9<br>Escenario 3.12<br>Escenario 3.14 | T015<br>T017<br>T022 | `cripta/controlador/controlador_cripta.py` | `tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_ir_a.py` |
| `FR-NIE-022` | Escenario 2.1<br>Escenario 3.15<br>Escenario 3.16 | T003<br>T006<br>T008 | `cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py` | `tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-023` | Escenario 2.1<br>Escenario 3.15<br>Escenario 3.16 | T003<br>T006<br>T008 | `cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py` | `tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-024` | B-NIE-004<br>B-NIE-005<br>Escenario 2.2<br>Escenario 3.17 | T004<br>T006<br>T008<br>T012<br>T013 | `cripta/modelo/conocimiento_jugador.py`<br>`cripta/modelo/partida.py` | `tests/`<br>`tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_niebla_ir_a.py`<br>`tests/modelo/test_conocimiento_jugador.py` |
| `FR-NIE-025` | Escenario 3.18 | T005<br>T006 | `cripta/modelo/conocimiento_jugador.py` | `tests/modelo/test_conocimiento_jugador.py` |

| Criterio | Escenario o caso | Tareas | Pruebas |
| --- | --- | --- | --- |
| `SC-NIE-001` | B-NIE-004<br>B-NIE-005<br>Escenario 1.1<br>Escenario 1.2<br>Escenario 1.3<br>Escenario 1.4<br>Escenario 1.5<br>Escenario 2.1<br>Escenario 2.2<br>Escenario 3.15<br>Escenario 3.16<br>Escenario 3.17 | T001<br>T002<br>T003<br>T004<br>T013<br>T029 | `tests/aceptacion/test_niebla_ir_a.py`<br>`tests/modelo/test_conocimiento_jugador.py`<br>`tests/vista/test_vista_consola.py` |
| `SC-NIE-002` | B-NIE-001<br>B-NIE-002<br>B-NIE-003<br>B-NIE-006<br>Escenario 3.1<br>Escenario 3.2<br>Escenario 3.9<br>Escenario 3.12<br>Escenario 3.14 | T014<br>T015<br>T032<br>T033 | `tests/aceptacion/test_niebla_ir_a.py`<br>`tests/modelo/test_ir_a.py`<br>`tests/servicios/test_servicio_bench.py` |
| `SC-NIE-003` | B-NIE-001<br>B-NIE-002<br>B-NIE-003<br>B-NIE-006<br>Escenario 3.3–3.8<br>Escenario 3.10<br>Escenario 3.11<br>Escenario 3.13 | T014<br>T017<br>T018 | `tests/aceptacion/test_niebla_ir_a.py`<br>`tests/controlador/test_controlador_cripta.py` |
| `SC-NIE-004` | — | T032<br>T033<br>T034<br>T035<br>T036<br>T037<br>T041 | `tests/servicios/test_servicio_bench.py` |
| `SC-NIE-005` | B-NIE-004<br>B-NIE-005<br>Escenario 2.2<br>Escenario 3.17 | T004<br>T010<br>T013<br>T038<br>T040 | `tests/`<br>`tests/aceptacion/test_niebla_ir_a.py`<br>`tests/modelo/test_conocimiento_jugador.py`<br>`tests/servicios/test_servicio_partida_guardado.py` |

## Resolubilidad

Carpeta `specs/003-resolubilidad/`. Prefijo `FR-RES-`.

| Requisito | Escenario o caso | Tareas | Código | Pruebas |
| --- | --- | --- | --- | --- |
| `FR-RES-001` | Caso límite de la puerta abierta a la sala de salida sin la llave de salida | T001<br>T002<br>T007 | `cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-002` | Caso límite de la puerta abierta a la sala de salida sin la llave de salida | T001<br>T002<br>T006<br>T007 | `cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/estructuras/ordenamientos.py`<br>`cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-003` | Caso límite de la puerta abierta a la sala de salida sin la llave de salida | T001<br>T002<br>T006<br>T007 | `cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/estructuras/ordenamientos.py`<br>`cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-004` | — | T001<br>T007 | `cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-005` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003<br>T007 | `cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-006` | Caso límite de la puerta abierta a la sala de salida sin la llave de salida | T001<br>T002<br>T007 | `cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-007` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003<br>T005<br>T007 | `cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-008` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003<br>T005<br>T006<br>T007 | `cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/estructuras/ordenamientos.py`<br>`cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-009` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003<br>T005<br>T008 | `cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-010` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003<br>T005<br>T008 | `cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-011` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003<br>T005<br>T008 | `cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-012` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003<br>T005<br>T008 | `cripta/modelo/resolubilidad.py` | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-013` | Apéndice B, inicio regular sobre cripta no resoluble sin `--forzar` aborta sin bucle de simulación | T012<br>T013<br>T014<br>T015 | `cripta/controlador/controlador_cripta.py`<br>`cripta/servicios/servicio_partida.py`<br>`cripta/vista/vista_base.py`<br>`cripta/vista/vista_consola.py` | `tests/controlador/test_controlador_cripta.py`<br>`tests/controlador/test_controlador_resolubilidad.py` |
| `FR-RES-014` | Apéndice B, inicio regular sobre cripta no resoluble sin `--forzar` aborta sin bucle de simulación | T012<br>T013<br>T015<br>T016 | `cripta/__main__.py`<br>`cripta/controlador/controlador_cripta.py`<br>`cripta/vista/vista_base.py`<br>`cripta/vista/vista_consola.py` | `tests/controlador/test_controlador_cripta.py`<br>`tests/controlador/test_controlador_resolubilidad.py` |
| `FR-RES-015` | Apéndice B, inicio regular sobre cripta no resoluble sin `--forzar` aborta sin bucle de simulación | T012<br>T013<br>T015<br>T016 | `cripta/__main__.py`<br>`cripta/controlador/controlador_cripta.py`<br>`cripta/vista/vista_base.py`<br>`cripta/vista/vista_consola.py` | `tests/controlador/test_controlador_cripta.py`<br>`tests/controlador/test_controlador_resolubilidad.py` |
| `FR-RES-016` | Apéndice B, inicio regular sobre cripta no resoluble sin `--forzar` aborta sin bucle de simulación | T012<br>T016 | `cripta/__main__.py` | `tests/controlador/test_controlador_resolubilidad.py` |
| `FR-RES-017` | — | T010<br>T011 | `cripta/servicios/servicio_resolubilidad.py` | `tests/cliente_falso.py`<br>`tests/servicios/test_servicio_resolubilidad.py` |
| `FR-RES-018` | — | T001<br>T004<br>T007<br>T009<br>T019 | `cripta/bench/cargas_bench.py`<br>`cripta/estructuras/cola.py`<br>`cripta/estructuras/heap_min.py`<br>`cripta/modelo/resolubilidad.py` | `tests/bench/test_cargas_bench.py`<br>`tests/modelo/test_resolubilidad.py` |
| `FR-RES-019` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003 | — | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-020` | — | T004<br>T009<br>T017<br>T018<br>T019<br>T020<br>T021 | `cripta/bench/cargas_bench.py`<br>`cripta/modelo/resolubilidad.py` | `tests/bench/test_cargas_bench.py`<br>`tests/modelo/test_resolubilidad.py`<br>`tests/servicios/test_servicio_bench.py` |
| `FR-RES-021` | — | T010<br>T011 | `cripta/servicios/servicio_resolubilidad.py` | `tests/cliente_falso.py`<br>`tests/servicios/test_servicio_resolubilidad.py` |
| `FR-RES-022` | Apéndice B, llave de salida tras su propia puerta<br>Apéndice B, llaves obtenibles del campo `suelta` de cualquier enemigo<br>Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003 | — | `tests/modelo/test_resolubilidad.py` |
| `FR-RES-023` | — | T010<br>T011 | `cripta/servicios/servicio_resolubilidad.py` | `tests/cliente_falso.py`<br>`tests/servicios/test_servicio_resolubilidad.py` |
| `FR-RES-024` | Apéndice B, inicio regular sobre cripta no resoluble sin `--forzar` aborta sin bucle de simulación | T012<br>T016 | `cripta/__main__.py` | `tests/controlador/test_controlador_resolubilidad.py` |

| Criterio | Escenario o caso | Tareas | Pruebas |
| --- | --- | --- | --- |
| `SC-001` | — | T020<br>T021 | `tests/bench/test_cargas_bench.py` |
| `SC-002` | — | T019<br>T020<br>T021 | `tests/bench/test_cargas_bench.py` |
| `SC-003` | Apéndice B, varios órdenes válidos producen misma secuencia | T001<br>T003 | `tests/modelo/test_resolubilidad.py` |
| `SC-004` | Caso límite de la puerta abierta a la sala de salida sin la llave de salida | T001<br>T002<br>T003 | `tests/modelo/test_resolubilidad.py` |
| `SC-005` | Apéndice B, inicio regular sobre cripta no resoluble sin `--forzar` aborta sin bucle de simulación | T012<br>T016 | `tests/controlador/test_controlador_resolubilidad.py` |
| `SC-006` | — | T010<br>T011 | `tests/cliente_falso.py`<br>`tests/servicios/test_servicio_resolubilidad.py` |
| `SC-007` | — | T017<br>T018<br>T019<br>T021 | `tests/bench/test_cargas_bench.py`<br>`tests/servicios/test_servicio_bench.py` |
| `SC-008` | — | T010<br>T011 | `tests/cliente_falso.py`<br>`tests/servicios/test_servicio_resolubilidad.py` |

## Línea de tiempo

Carpeta `specs/004-linea-de-tiempo/`. Prefijo `FR-LIN-`.

| Requisito | Escenario o caso | Tareas | Código | Pruebas |
| --- | --- | --- | --- | --- |
| `FR-LIN-001` | B-LIN-001<br>B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-003<br>Escenarios de las cinco historias (cobertura conjunta) | T006<br>T012<br>T031<br>T034<br>T035<br>T036<br>T037 | `cripta/bench/cargas_bench.py`<br>`cripta/modelo/linea_tiempo.py` | `tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-002` | B-LIN-001<br>B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-003<br>Escenarios de las cinco historias (cobertura conjunta) | T006<br>T012<br>T031<br>T035<br>T036<br>T037 | `cripta/bench/cargas_bench.py`<br>`cripta/modelo/linea_tiempo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-003` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-002<br>Escenarios de las cinco historias (cobertura conjunta) | T001<br>T002<br>T003<br>T007<br>T009<br>T012<br>T020<br>T022<br>T035<br>T036<br>T037 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/vista/vista_consola.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-004` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-004<br>Escenarios de las cinco historias (cobertura conjunta) | T008<br>T012<br>T013<br>T014<br>T021<br>T022<br>T035<br>T036<br>T037<br>T042 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py`<br>`cripta/vista/vista_base.py`<br>`cripta/vista/vista_consola.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/vista/test_vista_consola.py` |
| `FR-LIN-005` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-002<br>B-LIN-004<br>Escenarios de las cinco historias (cobertura conjunta) | T004<br>T005<br>T007<br>T008<br>T010<br>T011<br>T020<br>T022<br>T032<br>T035<br>T036<br>T037<br>T038<br>T042 | `cripta/bench/cargas_bench.py`<br>`cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py`<br>`cripta/vista/vista_consola.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-006` | B-LIN-001<br>B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-003<br>Escenarios de las cinco historias (cobertura conjunta) | T001<br>T002<br>T006<br>T009<br>T012<br>T020<br>T035<br>T036<br>T037 | `cripta/modelo/linea_tiempo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-007` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-002<br>Escenarios de las cinco historias (cobertura conjunta) | T001<br>T003<br>T004<br>T005<br>T007<br>T012<br>T032<br>T035<br>T036<br>T037 | `cripta/bench/cargas_bench.py`<br>`cripta/modelo/linea_tiempo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-008` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-005<br>Escenarios de las cinco historias (cobertura conjunta) | T025<br>T026<br>T035<br>T036<br>T037<br>T038<br>T042 | `cripta/__main__.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py`<br>`cripta/servicios/servicio_replay.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/servicios/test_servicio_replay.py` |
| `FR-LIN-009` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-005<br>Escenarios de las cinco historias (cobertura conjunta) | T025<br>T026<br>T035<br>T036<br>T037 | `cripta/__main__.py`<br>`cripta/servicios/servicio_replay.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/servicios/test_servicio_replay.py` |
| `FR-LIN-010` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenario 4.1<br>Escenarios de las cinco historias (cobertura conjunta) | T015<br>T017<br>T019<br>T035<br>T036<br>T037<br>T042 | `cripta/infraestructura/estado_guardado.py`<br>`cripta/infraestructura/guardado_binario.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/infraestructura/test_guardado_binario.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-011` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-006<br>Escenario 4.2<br>Escenarios de las cinco historias (cobertura conjunta) | T016<br>T019<br>T035<br>T036<br>T037 | `cripta/infraestructura/guardado_binario.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/infraestructura/test_guardado_binario.py` |
| `FR-LIN-012` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-006<br>Escenario 4.2<br>Escenarios de las cinco historias (cobertura conjunta) | T016<br>T019<br>T035<br>T036<br>T037 | `cripta/infraestructura/guardado_binario.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/infraestructura/test_guardado_binario.py` |
| `FR-LIN-013` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenarios de las cinco historias (cobertura conjunta) | T001<br>T002<br>T023<br>T024<br>T033<br>T035<br>T036<br>T037<br>T041<br>T042 | `cripta/__main__.py`<br>`cripta/bench/cargas_bench.py`<br>`cripta/constantes.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py`<br>`cripta/servicios/servicio_partida.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/servicios/test_servicio_bench.py`<br>`tests/servicios/test_servicio_partida.py` |
| `FR-LIN-014` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenarios de las cinco historias (cobertura conjunta) | T001<br>T002<br>T023<br>T024<br>T027<br>T028<br>T029<br>T033<br>T035<br>T036<br>T037<br>T040<br>T041<br>T042 | `cripta/__main__.py`<br>`cripta/bench/cargas_bench.py`<br>`cripta/constantes.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py`<br>`cripta/servicios/servicio_partida.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/servicios/test_servicio_bench.py`<br>`tests/servicios/test_servicio_partida.py` |
| `FR-LIN-015` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenarios de las cinco historias (cobertura conjunta) | T001<br>T002<br>T010<br>T011<br>T030<br>T031<br>T032<br>T035<br>T036<br>T037<br>T038<br>T039<br>T041<br>T042 | `cripta/__main__.py`<br>`cripta/bench/cargas_bench.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/servicios/test_servicio_bench.py` |
| `FR-LIN-016` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenarios de las cinco historias (cobertura conjunta) | T001<br>T029<br>T030<br>T035<br>T036<br>T037<br>T041<br>T042 | `cripta/bench/cargas_bench.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/servicios/test_servicio_bench.py` |
| `FR-LIN-017` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenarios de las cinco historias (cobertura conjunta) | T009<br>T010<br>T015<br>T017<br>T035<br>T036<br>T037<br>T042 | `cripta/infraestructura/estado_guardado.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/infraestructura/test_guardado_binario.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-018` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenarios de las cinco historias (cobertura conjunta) | T027<br>T028<br>T029<br>T031<br>T033<br>T035<br>T036<br>T037<br>T039<br>T040<br>T041<br>T042 | `cripta/__main__.py`<br>`cripta/bench/cargas_bench.py`<br>`cripta/constantes.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/servicios/test_servicio_bench.py` |
| `FR-LIN-019` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-004<br>Escenarios de las cinco historias (cobertura conjunta) | T008<br>T014<br>T018<br>T021<br>T035<br>T036<br>T037<br>T042 | `cripta/infraestructura/estado_guardado.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/vista/test_vista_consola.py` |
| `FR-LIN-020` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-002<br>Escenarios de las cinco historias (cobertura conjunta) | T003<br>T007<br>T035<br>T036<br>T037 | `cripta/modelo/linea_tiempo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-021` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenarios de las cinco historias (cobertura conjunta) | T015<br>T017<br>T018<br>T019<br>T029<br>T035<br>T036<br>T037<br>T042 | `cripta/bench/cargas_bench.py`<br>`cripta/infraestructura/estado_guardado.py`<br>`cripta/infraestructura/guardado_binario.py`<br>`cripta/modelo/partida.py`<br>`cripta/modelo/persistencia_modelo.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/infraestructura/test_guardado_binario.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `FR-LIN-022` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>Escenario 5.1<br>Escenarios de las cinco historias (cobertura conjunta) | T023<br>T024<br>T033<br>T035<br>T036<br>T037 | `cripta/__main__.py`<br>`cripta/constantes.py`<br>`cripta/servicios/servicio_partida.py` | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/servicios/test_servicio_partida.py` |
| `FR-LIN-023` | B-LIN-001<br>B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-003<br>Escenario 1.8<br>Escenarios de las cinco historias (cobertura conjunta) | T006<br>T009<br>T012<br>T020<br>T022<br>T034<br>T035<br>T036<br>T037 | `cripta/controlador/controlador_cripta.py`<br>`cripta/modelo/linea_tiempo.py`<br>`cripta/vista/vista_consola.py` | `tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_linea_tiempo.py`<br>`tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |

| Criterio | Escenario o caso | Tareas | Pruebas |
| --- | --- | --- | --- |
| `SC-LIN-001` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-004<br>siete grupos | T008<br>T021<br>T034<br>T036<br>T037 | `tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/vista/test_vista_consola.py` |
| `SC-LIN-002` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-004<br>estado/log/retroceso intactos | T008<br>T032<br>T036<br>T037<br>T038 | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/modelo/test_partida_linea_tiempo.py` |
| `SC-LIN-003` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>escala y latencia | T027<br>T028<br>T029<br>T031<br>T033<br>T036<br>T037<br>T040<br>T041 | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/servicios/test_servicio_bench.py` |
| `SC-LIN-004` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>memoria | T027<br>T029<br>T030<br>T036<br>T037<br>T041 | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/servicios/test_servicio_bench.py` |
| `SC-LIN-005` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>B-LIN-005<br>replay equivalente | T025<br>T036<br>T037 | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/servicios/test_servicio_replay.py` |
| `SC-LIN-006` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>round-trip y conocimiento | T015<br>T016<br>T018<br>T036<br>T037 | `tests/aceptacion/test_linea_tiempo.py`<br>`tests/infraestructura/test_guardado_binario.py` |
| `SC-LIN-007` | B-LIN-001 a B-LIN-006 (cobertura conjunta)<br>rechazo de consulta y K | T009<br>T020<br>T023<br>T034<br>T036<br>T037 | `tests/aceptacion/__init__.py`<br>`tests/aceptacion/test_linea_tiempo.py`<br>`tests/controlador/test_controlador_cripta.py`<br>`tests/modelo/test_partida_linea_tiempo.py`<br>`tests/servicios/test_servicio_partida.py` |

## Requisitos sin tarea, sin prueba o sin escenario citado

- `FR-TER-008` sin escenario citado.
- `FR-TER-017` sin escenario citado.
- `FR-TER-018` sin escenario citado.
- `FR-TER-019` sin escenario citado.
- `FR-TER-020` sin escenario citado.
- `FR-TER-021` sin escenario citado.
- `FR-TER-022` sin escenario citado.
- `FR-TER-023` sin escenario citado.
- `FR-TER-024` sin escenario citado.
- `FR-NIE-006` sin escenario citado.
- `FR-NIE-007` sin escenario citado.
- `FR-NIE-016` sin escenario citado.
- `FR-NIE-018` sin escenario citado.
- `FR-RES-004` sin escenario citado.
- `FR-RES-017` sin escenario citado.
- `FR-RES-018` sin escenario citado.
- `FR-RES-020` sin escenario citado.
- `FR-RES-021` sin escenario citado.
- `FR-RES-023` sin escenario citado.
