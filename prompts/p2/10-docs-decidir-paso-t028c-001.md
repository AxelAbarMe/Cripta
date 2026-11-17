Corrige solo documentos de specs/001-terreno-cazador/ (contracts/contrato_datos_p2.md y tasks.md), sin tocar código ni pruebas.

1. En contracts/contrato_datos_p2.md, en el docstring de BuscadorRutas.decidir_paso, aclara que llama internamente a calcular_o_reutilizar(mapa, sala_jugador_id, cazador.rango), así que no hace falta calcular antes, y que la tabla se reutiliza si sigue válida y el rango del cazador no supera el rango con que se calculó.

2. En tasks.md agrega T028c justo después de T028, sin marcar: ampliar tests/aceptacion/test_cazador_persecucion.py con escenarios que comprueben, a través de Partida, que la tabla del cazador se invalida en cada evento de T033 que hoy no tiene prueba propia: el jugador abre una puerta con llave que acorta la ruta, el jugador usa el pergamino de retroceso y vuelve a una sala anterior, se activa un cazador con un rango mayor que el calculado, y se carga una partida guardada. En cada caso la decisión del cazador debe ser la misma que calcular desde cero (FR-TER-015). Actualiza las dependencias para que T028c vaya antes de C.4.

Conserva ids, formato y finales de línea. No marques casillas. No uses sed -i. En textos nuevos no uses ";". Al terminar, dime qué cambiaste.
