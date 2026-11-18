# Implementación 002, paso 1: pruebas del dominio del conocimiento (T001 a T005)

Solo tareas T001, T002, T003, T004 y T005 de specs/002-niebla-ir-a/tasks.md. Son solo pruebas, sin código en cripta/.

Reglas:
1. Lee spec.md, plan.md, data-model.md, research.md, quickstart.md y contracts/ de specs/002-niebla-ir-a/ antes de escribir. Usa exactamente los nombres de clases, métodos y atributos que definen esos documentos. Si algún nombre que necesitan las pruebas no está definido, detente y pregunta en vez de inventarlo.
2. Crea tests/modelo/test_conocimiento_jugador.py (Nuevo, comprueba con Test-Path que no exista) con clases de prefijo Test. T001 a T005 van en ese mismo archivo, en ese orden.
3. Cada prueba cita en su docstring o comentario el FR-NIE y el escenario de aceptación que cubre (1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 3.15, 3.16, 3.17 y 3.18) y los SC-NIE de la tarea.
4. Usa criptas y mapas sintéticos armados dentro de las pruebas o con los ayudantes existentes de tests/. No uses fixtures/ ni red.
5. Las pruebas deben fallar porque cripta/modelo/conocimiento_jugador.py aún no existe. Córrelas con py -m unittest tests.modelo.test_conocimiento_jugador, muéstrame que fallan por esa razón y no por otra, como un error de sintaxis o un nombre mal escrito en la prueba.
6. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted().
7. No toques cripta/ ni ningún otro archivo salvo el de pruebas y tasks.md. No crees ni cambies de rama, y no hagas commit ni push.
8. Marca T001 a T005 como [X] en tasks.md, respetando sus finales de línea.
9. Los .py van en CRLF. Para editar usa tu herramienta de edición, no sed -i. En comentarios y textos nuevos no uses ";".

Al terminar, corre py -m unittest discover -s tests -t . y dime cuántas pruebas fallan y por qué. Dime qué hiciste y qué nombres de la API usaste, con el documento de donde los tomaste.