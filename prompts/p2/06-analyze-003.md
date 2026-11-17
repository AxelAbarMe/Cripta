SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad
Contexto: ya estoy en la rama 003-resolubilidad. No crees ni cambies de rama y no hagas commit. Es un análisis de SOLO LECTURA: no crees ni modifiques ningún archivo; entrega el informe únicamente en el chat. Redacta todo en español. Analiza la consistencia entre specs/003-resolubilidad/spec.md, plan.md, research.md, data-model.md, quickstart.md, contracts/, tasks.md y la constitución. Puedes leer cripta/ y tests/ solo para verificar rutas y nombres; no releas el repositorio completo.

Verifica en particular:
1. Cada FR-RES-001 a 023 y cada SC-001 a 008 tiene al menos una tarea y una prueba que lo cita; ninguna tarea cita un requisito inexistente.
2. Los cuatro casos del Apéndice B y cada escenario de aceptación de spec.md tienen una prueba prevista antes del código que los hace pasar.
3. spec.md no nombra estructuras, clases, módulos ni rutas de endpoint, y plan.md no agrega reglas del juego que no estén en spec.md.
4. Ningún documento propone heapq, bisect, collections, networkx, set, dict como índice o caché, ni list.sort() o sorted().
5. Cada cifra de rendimiento cita un comando de --bench o está marcada como hipótesis.
6. Las rutas de archivo y las marcas Nuevo/Modificado coinciden entre plan.md y tasks.md, y existen en el repositorio cuando dicen Modificado.
7. El orden de dependencias entre fases, las marcas [P] y los puntos de corte de los Pull Requests son coherentes.
8. Puntos a vigilar: los códigos de salida 0/1/2 de --verificar son decisión del plan y no vienen de la spec; la herencia de CriptaDatosInvalidosError; la semántica de las aristas del grafo de dependencias; quickstart.md no cita fixtures inexistentes ni exige datos offline sin explicarlo; la carga resolubilidad_cota está registrada en CARGAS; la prueba de --verificar (T012) vive en __main__.py, que se implementa en otra tarea; y cualquier cifra fija del número total de pruebas.

Informe: tabla con ID, gravedad (CRÍTICA, ALTA, MEDIA, BAJA), archivo y línea, problema y corrección sugerida. Máximo 25 hallazgos, los más graves primero, y cierra con una lista de requisitos sin tarea y tareas sin requisito (o "ninguno").