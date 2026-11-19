# Fase C de la 003: interfaz de resolubilidad (T012 a T016)

Implementa solo T012 a T016 de specs/003-resolubilidad/tasks.md. Lee antes .specify/memory/constitution.md, spec.md, contracts/, data-model.md, quickstart.md y la sección de la Fase C de tasks.md. Si algo contradice spec.md, detente y explícalo.

Alcance de escritura: solo cripta/vista/, cripta/controlador/, cripta/servicios/servicio_partida.py, cripta/__main__.py, tests/controlador/, tests/vista/ y tasks.md (marca [X] solo T012 a T016). No toques resolubilidad.py, servicio_resolubilidad.py, cripta/bench/, docs/, PROMPTS_LLM.md ni DECISIONES.md.

Orden sugerido: como T012 (--verificar, códigos de salida 0, 1 y 2) depende de __main__.py (T016), haz primero lo que no dependa y deja T012 con su conexión a __main__ al final, respetando los números de tarea.

Reglas generales: respeta la constitución y las restricciones de estructuras de datos propias que ya aplican al resto de cripta/ (sin librerías de colecciones prohibidas). Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios y textos nuevos no uses ";". Los errores de datos heredan de CriptaError y los de programación de IndexError o ValueError. No crees ni cambies de rama y no hagas commit ni push.

Pruebas: agrega pruebas unittest para cada tarea en tests/controlador/ y tests/vista/. Al terminar corre py -m unittest discover -s tests -t . y reporta cuántas pasan. Confirma con git status --short que solo cambiaron archivos del alcance permitido y lista cuáles.