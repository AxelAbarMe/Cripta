# Implementación 003, Fase A, paso 1: pruebas de dominio (T001 a T004)

Solo T001, T002, T003 y T004 de specs/003-resolubilidad/tasks.md, en ese orden. No sigas con T005.

Reglas generales:
1. Lee primero .specify/memory/constitution.md. Luego lee spec.md, plan.md, data-model.md, research.md, quickstart.md y contracts/ de specs/003-resolubilidad/ antes de escribir. La API que las pruebas deben usar la fijan data-model.md y las tareas T005 a T009: módulo cripta/modelo/resolubilidad.py con ResultadoResolubilidad, FronteraBloqueadaPuerta, CicloDependenciaLlaves, UbicacionLlaveDiagnostico y VerificadorResolubilidad(mapa, sala_inicial, sala_salida, llave_salida, llaves_ubicaciones) con los métodos verificar() y verificar_ingenuo_reiniciado(). Usa exactamente esos nombres y firmas.
2. Para armar criptas sintéticas reutiliza los ayudantes existentes de tests/ (por ejemplo tests/cripta_artificial.py y tests/cripta_cazadores.py) y mira cómo los usan las pruebas actuales. No dupliques lo que ya exista.
3. Si necesitas un nombre nuevo que ni los documentos ni las tareas definan, propón el mínimo siguiendo los patrones del código existente, en español, y anótalo en tu resumen con el archivo y el motivo. Solo detente y pregunta si algo contradice una regla de spec.md.
4. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Errores de programación heredan de IndexError o ValueError. El modelo no importa red, archivos ni vista.
5. No crees ni cambies de rama y no hagas commit ni push. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios y textos nuevos no uses ";". Comentarios cortos: cabecera de máximo 5 líneas y 1 o 2 líneas por método.
6. Después de cada tarea marca su casilla [X] en tasks.md respetando sus finales de línea.

Puntos de control:
- T001: crea tests/modelo/test_resolubilidad.py (Nuevo, comprueba con Test-Path que no exista) con el esqueleto y los fixtures sintéticos.
- T002, T003, T004: agrega los casos que describe cada tarea, con los sufijos de nombre que piden (por ejemplo _ApendiceB).
- Todos los casos deben fallar porque resolubilidad.py aún no existe. NO crees cripta/modelo/resolubilidad.py.
Al terminar, corre py -m unittest tests.modelo.test_resolubilidad y muestra que falla por ImportError o AttributeError. Corre también py -m unittest discover -s tests -t . y confirma que los únicos fallos son del archivo nuevo. Dime qué hiciste por tarea, los nombres nuevos que propusiste y confirma que solo cambiaron tests/modelo/test_resolubilidad.py y tasks.md.