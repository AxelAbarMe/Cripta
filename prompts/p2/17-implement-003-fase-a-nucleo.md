# Implementación 003, Fase A, paso 2: núcleo del verificador (T005 a T007)

Solo T005, T006 y T007 de specs/003-resolubilidad/tasks.md, en ese orden. No sigas con T008.

Reglas generales:
1. Lee primero .specify/memory/constitution.md. Luego lee spec.md, plan.md, data-model.md, research.md, quickstart.md y contracts/ de specs/003-resolubilidad/ antes de escribir. La API la fijan las pruebas de tests/modelo/test_resolubilidad.py, que son la fuente de verdad de nombres y firmas. Usa exactamente lo que esas pruebas llaman.
2. Si necesitas un nombre nuevo que ni las pruebas ni los documentos definan, propón el mínimo siguiendo los patrones del código existente, en español, y anótalo en tu resumen con el archivo y el motivo. Solo detente y pregunta si algo cambia una regla de spec.md.
3. No modifiques tests/modelo/test_resolubilidad.py. Si una prueba te parece contradictoria con la spec o con data-model.md, detente y explícalo.
4. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Solo listas indexadas por entero. Reutiliza Cola (cripta/estructuras/cola.py), HeapMinimo (cripta/estructuras/heap_min.py) y Ordenamiento.merge_sort (cripta/estructuras/ordenamientos.py). Errores de programación heredan de IndexError o ValueError. El modelo no importa red, archivos ni vista.
5. No crees ni cambies de rama y no hagas commit ni push. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios y textos nuevos no uses ";". Comentarios cortos: cabecera de máximo 5 líneas y 1 o 2 líneas por método.
6. Después de cada tarea marca su casilla [X] en tasks.md respetando sus finales de línea.

Puntos de control:
- T005: crea cripta/modelo/resolubilidad.py (Nuevo, comprueba con Test-Path que no exista) con las cuatro clases de datos inmutables y reporte_texto() y formato() según data-model.md y contracts/.
- T006: agrega _busqueda_binaria y _construir_catalogo (merge_sort propio, deduplicación lineal) y las tablas contiguas.
- T007: agrega VerificadorResolubilidad.__init__ y verificar() con Cola, HeapMinimo, la regla de entro_por_llave_salida de data-model.md y la frontera bloqueada. Hasta T008, ciclos_dependencia puede devolver una tupla vacía provisional, anótalo.
- Las pruebas que dependen de la detección de ciclos (T008) o de verificar_ingenuo_reiniciado (T009) seguirán fallando. Dime cuáles pasan, cuáles fallan, y confirma que las que fallan lo hacen solo por eso.
Al terminar, corre py -m unittest tests.modelo.test_resolubilidad y py -m unittest discover -s tests -t . y reporta cuántas pasan. Dime qué hiciste por tarea, los nombres nuevos que propusiste y confirma que solo cambiaron cripta/modelo/resolubilidad.py y tasks.md.