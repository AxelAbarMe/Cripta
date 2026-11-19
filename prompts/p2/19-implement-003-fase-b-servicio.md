# Implementación 003, Fase B: servicio de resolubilidad (T010 y T011)

Solo T010 y T011 de specs/003-resolubilidad/tasks.md, en ese orden. No sigas con T012.

Reglas generales:
1. Lee primero .specify/memory/constitution.md. Luego lee spec.md, plan.md, data-model.md, research.md y contracts/ de specs/003-resolubilidad/. Mira cómo cripta/servicios/servicio_partida.py y servicio_precarga.py obtienen datos generales y esqueleto paginado con ContadorSolicitudes y CacheDisco, y reutiliza esos patrones. Usa tests/cliente_falso.py (ClienteFalso) en las pruebas, sin red.
2. cripta/modelo/resolubilidad.py ya está completo y probado. No lo modifiques. Importa VerificadorResolubilidad y ResultadoResolubilidad desde ahí.
3. Si necesitas un nombre nuevo que ni los documentos ni las tareas definan, propón el mínimo en español y anótalo en tu resumen. Solo detente y pregunta si algo contradice una regla de spec.md.
4. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Reutiliza CriptaLimiteError y CriptaDatosInvalidosError de cripta/excepciones.py sin redefinirlos. El modelo no importa red ni archivos.
5. No crees ni cambies de rama y no hagas commit ni push. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios y textos nuevos no uses ";". Comentarios cortos.
6. Después de cada tarea marca su casilla [X] en tasks.md respetando sus finales de línea.

Puntos de control:
- T010: crea tests/servicios/test_servicio_resolubilidad.py (Nuevo, comprueba con Test-Path que no exista) con los casos que pide la tarea. Deben fallar por ImportError porque el servicio aún no existe. Muestra que fallan por esa razón.
- T011: crea cripta/servicios/servicio_resolubilidad.py (Nuevo) con ServicioResolubilidad. El presupuesto agotado debe lanzar CriptaLimiteError sin reporte parcial. Los datos contradictorios deben propagar CriptaDatosInvalidosError. Si CacheDisco no encaja con lo que pide la tarea, detente y explícalo, no modifiques cache.py.
Al terminar, corre py -m unittest tests.servicios.test_servicio_resolubilidad y py -m unittest discover -s tests -t . y reporta cuántas pasan. Corre Select-String -Path cripta\servicios\servicio_resolubilidad.py -Pattern "heapq|bisect|collections|networkx|sorted\(|\.sort\(|dict|set\(" y muestra la salida. Confirma que solo cambiaron tests/servicios/test_servicio_resolubilidad.py, cripta/servicios/servicio_resolubilidad.py y tasks.md.