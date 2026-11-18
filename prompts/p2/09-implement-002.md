# Implementación 002, paso 3: estado lógico y casos de aceptación (T010 a T013)

Solo T010, T011, T012 y T013 de specs/002-niebla-ir-a/tasks.md, en ese orden. No sigas con T014.

Mismas reglas generales del prompt 08 (puntos 1 a 6): nombres nuevos mínimos y anotados, sin estructuras prohibidas, CRLF, sin sed -i, sin ";" en comentarios, sin commit ni push, casillas [X] al terminar cada tarea.

Puntos de control:
- T010: agrega a tests/servicios/test_servicio_partida_guardado.py la prueba de proyección y restauración lógica del conocimiento y su historial, sin validar bytes. Debe fallar porque EstadoPartida aún no trae el campo. Muestra la razón.
- T011: agrega el campo lógico del conocimiento a EstadoPartida en cripta/infraestructura/estado_guardado.py y su proyección y restauración en cripta/modelo/persistencia_modelo.py. No toques guardado_binario.py ni definas bytes: la 004 es dueña del formato y del cambio de versión. Si añadir el campo obliga a cambiar la codificación binaria o rompe pruebas de guardado existentes, detente y explícalo. Debe pasar T010 y toda la suite.
- T012: tests/aceptacion/__init__.py ya existe porque lo creó la 001. Compruébalo con Test-Path, no lo toques, marca T012 en [X] y dime que ya existía.
- T013: crea tests/aceptacion/test_niebla_ir_a.py (Nuevo, comprueba con Test-Path que no exista) con los casos B-NIE-004 (antorcha sin activar enemigos ni trampas) y B-NIE-005 (pergamino revierte una entrada con antorcha), vía Partida con mapas sintéticos. Deben pasar con lo ya implementado. Si alguno falla, es un defecto de T006 a T011: detente y explícalo en vez de cambiar la prueba.
Al terminar, corre py -m unittest discover -s tests -t . y reporta cuántas pasan. Dime qué hiciste por tarea, los nombres nuevos y los archivos tocados.