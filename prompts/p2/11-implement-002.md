# Implementación 002, paso 5: bucle del viaje y consulta del mapa en el controlador (T014, T017, T018 y T022)

Solo T014, T017, T018 y T022 de specs/002-niebla-ir-a/tasks.md, en ese orden. No sigas con T023.

Mismas reglas generales del prompt 10 (puntos 1 a 6): nombres nuevos mínimos y anotados, sin estructuras prohibidas, CRLF, sin sed -i, sin ";" en comentarios, sin commit ni push, pruebas con valor, casillas [X] al terminar cada tarea. No toques cripta/vista/, cripta/servicios/, cripta/infraestructura/, cripta/bench/ ni el modelo salvo que un defecto de T015 a T021 lo exija, y en ese caso detente y explícalo.

Contexto de diseño, ya decidido en plan.md:
- El bucle vive en ControladorCripta. Antes de cada paso pide al modelo el siguiente paso, ejecuta Accion("mover", direccion) con ServicioPartida.ejecutar y evalúa el resultado completo. Solo ejecuta los pasos de su propia orden y no despacha otras acciones entre ellos.
- Estructura el paso para poder aislarlo (una función de un solo paso usada por el bucle), de modo que B-NIE-006 pueda ejecutar el viaje paso a paso desde el servicio e intercalar el pergamino. Tras un pergamino el viaje no continúa.
- Dos órdenes nuevas en Orden: la consulta del mapa y «ir a» con la sala destino como id entero. Actualiza el docstring de Orden.
- El controlador pide a la vista presentar el mapa proyectado y el motivo de detención. VistaBase y VistaConsola son de la Fase D (T025 a T030): no las edites. La vista falsa de las pruebas define esos métodos. Anota sus nombres, porque T027 deberá coincidir con ellos.
- No escribas el comentario # de partida.log ni toques el escritor o el lector: es T028.
- Si el jugador muere en un paso, no se informa el viaje y la partida termina por el flujo normal.

Puntos de control:
- T014: agrega a tests/aceptacion/test_niebla_ir_a.py (ya existe, es Modificado) los casos B-NIE-001 (destino no explorado), B-NIE-002 (puerta recordada abierta que ahora está cerrada), B-NIE-003 (sala con enemigos dormidos que se activan y detienen el viaje) y B-NIE-006 (pergamino durante el viaje). Si necesitas un servicio con mapa sintético y el ayudante existente no lo permite sin tocar archivos no permitidos, detente y explícalo. Renombra la clase PruebasAceptacionNiebla a TestAceptacionNiebla en tests/aceptacion/test_niebla_ir_a.py, para seguir el prefijo Test de las demás clases de prueba, y agrega los casos nuevos de T014 en esa misma clase o en otra con prefijo Test.
- T017: agrega a tests/controlador/test_controlador_cripta.py, con su VistaFalsa y la cripta congelada de tests/datos/, las pruebas de orden inválida, destino actual, ruta inexistente y consulta del mapa: cero tiempo, cero líneas nuevas en partida.log (usa una ruta de bitácora temporal), ningún cambio del historial, y la consulta traduce la orden, pide la proyección al modelo y la entrega a la vista.
- T018: agrega las pruebas del ciclo del viaje: acción ordinaria por paso, eventos entre pasos, recálculo tras un cierre observado, detenciones, motivos en orden fijo, muerte del jugador y pergamino.
- Las pruebas de T014, T017 y T018 deben fallar por la falta de la orden y del bucle, no por errores de sintaxis ni nombres mal escritos. Muestra las razones.
- T022: implementa en cripta/controlador/controlador_cripta.py las validaciones, el bucle, el recálculo por paso, los motivos ordenados, la cancelación por pergamino y la consulta del mapa. Deben pasar T014, T017 y T018. Corre py -m unittest discover -s tests -t . y confirma que todo pasa.
Al terminar, reporta cuántas pruebas pasan, qué hiciste por tarea, los nombres nuevos (incluidos los métodos que el controlador pide a la vista) y confirma que no cambió ningún archivo fuera de cripta/controlador/, tests/controlador/, tests/aceptacion/ y tasks.md.