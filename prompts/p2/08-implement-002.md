# Implementación 002, paso 2: conocimiento, integración con la partida y cierres (T006 a T009)

Solo T006, T007, T008 y T009 de specs/002-niebla-ir-a/tasks.md, en ese orden. No sigas con T010.

Reglas generales:
1. Lee spec.md, plan.md, data-model.md, research.md, quickstart.md y contracts/ antes de escribir. La API la fijan las pruebas de T001 a T005 en tests/modelo/test_conocimiento_jugador.py, que son la fuente de verdad de nombres y firmas: ConocimientoJugador(mapa, sala_inicial), estado_de_sala, sala_conocida, observar_puerta, estado_de_puerta, al_entrar, proyectar, SalaConocida y SalidaConocida. Usa exactamente lo que esas pruebas llaman. La clase hereda de Reversible y registra inversas por celda dentro de cada método, como Inventario.
2. Si necesitas un nombre nuevo que ni las pruebas ni los documentos definan, propón el mínimo siguiendo los patrones del código existente, en español, y anótalo en tu resumen con el archivo y el motivo. Solo detente y pregunta si algo cambia lo que el jugador observa o una regla de spec.md.
3. No modifiques las pruebas de T001 a T005. Si una te parece contradictoria con la spec, detente y explícalo.
4. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Listas indexadas por id de sala. Errores de programación heredan de IndexError o ValueError. El modelo no importa red, archivos ni vista.
5. No crees ni cambies de rama y no hagas commit ni push. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios y textos nuevos no uses ";". Comentarios cortos: cabecera de máximo 5 líneas y 1 o 2 líneas por método.
6. Después de cada tarea marca su casilla [X] en tasks.md respetando sus finales de línea.

Puntos de control:
- T006: crea cripta/modelo/conocimiento_jugador.py. Debe pasar py -m unittest tests.modelo.test_conocimiento_jugador completo. Corre también py -m unittest discover -s tests -t . y confirma que todo pasa.
- T007: agrega a tests/modelo/test_conocimiento_jugador.py las pruebas de entrada ordinaria vía Partida (observación de puertas, revelación de vecinas y cierre automático observado desde una sala conectada, caso B-NIE-002), usando mapas sintéticos y los ayudantes existentes de tests/. Deben fallar porque Partida aún no integra el conocimiento. Muestra que fallan por esa razón.
- T008: integra ConocimientoJugador en cripta/modelo/partida.py (creación, entradas, antorcha, conexión del retroceso en _conectar_retroceso como se hace con el inventario). El pergamino debe revertir la entrada y sus cambios de conocimiento. Deben pasar las pruebas de T007.
- T009: cripta/modelo/efectos.py avisa al conocimiento los cierres automáticos solo si son observables. Deben pasar todas las pruebas de T007.
Al terminar, corre py -m unittest discover -s tests -t . y reporta cuántas pasan. Dime qué hiciste por tarea, los nombres nuevos que propusiste y confirma que no cambió ningún archivo fuera de cripta/modelo/, tests/modelo/ y tasks.md.