# Implementación 003, Fase A, paso 3: ciclos y cierre de la Fase A (T008 y T009)

Una ejecución anterior con otro modelo se cortó por falta de cupo después de escribir cripta/modelo/resolubilidad.py. No lo reescribas desde cero. Parte de lo que hay.

Reglas generales:
1. Lee primero .specify/memory/constitution.md. Luego lee spec.md, plan.md, data-model.md, research.md y contracts/ de specs/003-resolubilidad/. La API la fijan las pruebas de tests/modelo/test_resolubilidad.py. No modifiques esas pruebas. Si una te parece contradictoria con la spec, detente y explícalo.
2. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Solo listas indexadas por entero. Reutiliza Cola, HeapMinimo y Ordenamiento.merge_sort. El modelo no importa red, archivos ni vista.
3. No crees ni cambies de rama y no hagas commit ni push. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios y textos nuevos no uses ";". Comentarios cortos.
4. Si necesitas un nombre nuevo que ni las pruebas ni los documentos definan, propón el mínimo en español y anótalo en tu resumen.

Pasos:
- Revisión: lee cripta/modelo/resolubilidad.py completo y compáralo con T005, T006 y T007 de specs/003-resolubilidad/tasks.md y con data-model.md. Corrige lo que no cumpla y dime qué cambiaste. Mueve al inicio del archivo los imports de direccion_opuesta que están dentro de funciones. Marca T005, T006 y T007 en [X] si cumplen.
- T008: implementa _detectar_ciclos tal como lo describe tasks.md, con G_dep bipartito bloques y llaves, DFS tricolor con listas contiguas, ciclos informados solo con llaves y normalizados al menor identificador, y ciclos ordenados por llave menor. Conéctalo en verificar() para llenar ciclos_dependencia. Deben pasar las pruebas de ciclos, incluida test_cadena_doble_ciclos_independientes y test_llave_salida_tras_propia_puerta_ApendiceB.
- Si test_llave_exigida_sin_ubicacion sigue fallando después de T008, diagnostica por qué (estado sin_ubicacion en ubicaciones_llaves) y corrige el código, no la prueba.
- T009: revisa verificar_ingenuo_reiniciado, que ya existe. Debe dar el mismo es_resoluble que verificar en todos los casos de prueba y no usar estructuras prohibidas. Corrige lo que haga falta.
- Marca T008 y T009 en [X] respetando los finales de línea de tasks.md.
Al terminar, corre py -m unittest tests.modelo.test_resolubilidad y py -m unittest discover -s tests -t . y reporta cuántas pasan. Corre este comando y muestra su salida: Select-String -Path cripta\modelo\resolubilidad.py -Pattern "heapq|bisect|collections|networkx|sorted\(|\.sort\(|dict|set\(". Confirma que solo cambiaron cripta/modelo/resolubilidad.py y tasks.md.