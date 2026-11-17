Corrige solo documentos de specs/001-terreno-cazador/ (plan.md y tasks.md), sin tocar código. Es una revisión de una decisión de la Parte I (P2 §5.6) descubierta al medir la Fase D.

Hechos medidos:
- El peor caso de la carga partida de la Parte I supera 20 ms con 400 salas (29.5, 43.8 y 48.2 ms en Windows con Python 3.14), y la Parte I lo había documentado con la causa sin aislar.
- La causa son las pausas del recolector de memoria de Python. Con el recolector apagado el peor caso baja a unos 15 ms y la mediana no cambia. En una partida de 400 salas con 1287 acciones, una limpieza completa encuentra 0 objetos de basura cíclica y la memoria es igual con o sin limpiezas (8.5 MB), así que esas pausas recorren objetos vivos, sobre todo el historial de retroceso, sin recuperar nada.
- Llamar a gc.freeze() al terminar cada acción del jugador deja el peor caso en 11.1, 15.7 y 17.4 ms en Windows con Python 3.14 (en Linux con Python 3.10 baja de 55-66 ms a 14-15.6 ms), con la mediana igual y un costo de unos 0.01 ms por llamada.
- Alternativas evaluadas: apagar el recolector (descartada porque deja de recoger basura cíclica nueva), limpiar con gc.collect() en el tiempo ocioso tras cada acción (descartada porque cada limpieza cuesta 35 a 72 ms con 400 salas), subir el umbral de la generación 2 (descartada porque el recolector de Python 3.14 trabaja distinto y no es portable).
- Riesgo: la basura cíclica entre objetos congelados no se recoge. Se midió 0, y se documenta como límite conocido.

1. plan.md: en la sección "Revisión de Decisiones de la Parte I que esta Carga pueda Invalidar", agrega esta revisión con problema, evidencia, alternativas, decisión (gc.freeze() al final de Partida.ejecutar_accion, que cubre el juego, --replay y el bench, porque las cargas del cazador llaman a Partida directamente sin pasar por ServicioPartida) y riesgo.
2. tasks.md: en la Fase D agrega, sin marcar:
   - T039b: prueba en tests/modelo/ que, después de Partida.ejecutar_accion, gc.get_freeze_count() es mayor que 0, con limpieza (gc.unfreeze) al final de la prueba, y luego el cambio en cripta/modelo/partida.py que llama a gc.freeze() al terminar ejecutar_accion (P2 §5.6, FR-TER-020).
   - T039c: prueba en tests/bench/ (con __init__.py) que ejecuta cada carga registrada en CARGAS a una escala mínima y comprueba que devuelve resultados sin lanzar excepciones (Principio VIII). Motivo: un cambio de la Fase C rompió la carga ciclo sin que ninguna prueba lo detectara.
   - Ajusta T039 para que las mediciones definitivas se tomen después de T039b, y que T043 documente el antes y el después de esta revisión.
   Actualiza las dependencias de la Fase D.

Respeta los finales de línea de cada archivo, no uses sed -i y en textos nuevos no uses ";". Al terminar, dime qué cambiaste.
