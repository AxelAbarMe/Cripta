Corrige solo documentos de specs/001-terreno-cazador/ (spec.md, plan.md, quickstart.md y tasks.md), sin tocar código ni fixtures. El grupo acordó lo siguiente tras revisar el servidor:
- cripta-01 ya no existe en el servidor. Hay dos criptas nuevas: cripta-05 "Cripta sellada" (24 salas) y cripta-06 "Cripta de referencia" (300 salas). La versión del catálogo cambió de be68d322d2f5 a 4b9e75a42be5.
- cripta-01 se mueve con el catálogo anterior y criptas.json a tests/datos/ como datos de prueba congelados. Las 4 pruebas que usan ClienteOffline("fixtures") (test_guardado_ida, test_guardado_vuelta, test_pergamino, test_servicio_partida) pasan a usar ClienteOffline("tests/datos"), y se actualiza su docstring.
- fixtures/ queda igual al servidor actual: cripta-02 a cripta-06 con llaves.json, costo, rango y el catálogo nuevo.
- Los tres ejemplos de docs/ejemplos/ ya no se reproducen porque guardan el catálogo anterior. Se reemplazan por ejemplos nuevos que muestren terreno y cazador, en la Fase E.
- La cripta de referencia de FR-TER-020 y SC-001 es cripta-06. La carga sintética de 400 salas se mantiene para comparar alternativas, pero la verificación de FR-TER-020 se hace con cripta-06 desde fixtures/.

Cambios concretos:
1. spec.md: actualiza el supuesto de la cripta de referencia y agrega una sesión de clarificaciones "Sesión 2026-11-10 (estado del servidor)" con estos hechos.
2. plan.md: actualiza la línea de mediciones de FR-TER-020 y el Límite Conocido 5.
3. quickstart.md: actualiza la medición de FR-TER-020 y el comando de replay de ejemplo.
4. tasks.md: reescribe T016 (el respaldo es el commit e6d52ac y se mueve cripta-01 a tests/datos/ con las 4 pruebas), T017 (regenera cripta-02 a cripta-06 con llaves.json y actualiza docs/FORMATO_OFFLINE.md y la sección de fixtures del README), T039 (mide con cripta-06) y T042 (graba ejemplos nuevos, reemplaza los de docs/ejemplos/ y actualiza la tabla del README). Conserva los ids y el formato de las tareas.

No marques casillas. Respeta los finales de línea de cada archivo. No uses sed -i. Al terminar, dime qué cambiaste en cada archivo.

Seguimiento, en la misma sesión:

Sí falta una tarea: cargas_bench.py solo tiene cargas sintéticas. Agrega en la Fase D una tarea T036b, antes de T039: modificar cripta/bench/cargas_bench.py para registrar la carga ciclo_referencia, que carga cripta-06 desde fixtures/ con ClienteOffline (sin red ni vista), arma la partida y mide el ciclo de eventos entre dos decisiones del jugador con decenas de cazadores activos. Si cripta-06 no trae suficientes cazadores, la carga activa más instancias de cazador con una semilla fija, y se documenta cuántas. Cita FR-TER-020. Haz que T038 también habilite ciclo_referencia en servicio_bench.py y que T039 use ciclo_referencia. Actualiza la sección de dependencias de tasks.md. Solo tasks.md, no marques casillas, no uses sed -i.
