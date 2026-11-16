# Especificación de funcionalidad: Línea de tiempo

**Rama de funcionalidad**: `004-linea-de-tiempo`

**Creada**: 2026-11-15

**Estado**: Borrador

**Entrada**: Prompt de usuario: `prompts/p2/02-specify-004.md`

## Escenarios de usuario y pruebas

### Historia de usuario 1: Consultar un estado pasado (Prioridad: P1)

Como jugador, quiero consultar el estado de la partida en un instante anterior para entender qué ocurría entonces sin alterar la partida actual.

**Prioridad**: Es la función central de la línea de tiempo y permite inspeccionar el pasado durante una partida.

**Prueba independiente**: Consultar un instante válido y comparar el resumen mostrado con el estado correspondiente de la partida.

**Escenarios de aceptación**:

1. **Dado** que el reloj actual de la partida es `r`, **cuando** se consulta `historia t` con `t > r`, **entonces** la consulta se rechaza.
2. **Dado** que ocurrieron varios eventos en el instante `t`, **cuando** se consulta `historia t`, **entonces** se muestra el estado después de todos los eventos con tiempo menor o igual que `t`.
3. **Dado** que a `t` le corresponde una decisión del jugador, **cuando** se consulta `historia t`, **entonces** se muestra el estado justo antes de esa decisión.
4. **Dado** un instante válido, **cuando** se consulta `historia t`, **entonces** el resumen incluye como mínimo reloj, sala del jugador, vida y estadísticas, inventario, efectos activos, enemigos de esa sala con su vida y mapa conocido en ese momento.
5. **Dado** un estado válido de la partida, **cuando** se consulta `historia t`, **entonces** la consulta no consume tiempo, no se registra como acción y no altera el estado actual ni el historial de retroceso.

### Historia de usuario 2: Consultar antes de una acción (Prioridad: P1)

Como jugador, quiero localizar un estado justo antes de una acción numerada para revisar la partida por su secuencia de decisiones.

**Prioridad**: Permite consultar la historia por la referencia de acción que define el prompt.

**Prueba independiente**: Consultar `historia #k` y verificar que el resumen representa el estado justo antes de la acción `k`.

**Escenarios de aceptación**:

1. **Dado** que existe una acción del jugador identificada como `k`, **cuando** se consulta `historia #k`, **entonces** se muestra el estado justo antes de esa acción.

### Historia de usuario 3: Reproducir hasta un instante sin vista (Prioridad: P2)

Como persona que revisa una partida, quiero reproducir su bitácora hasta un instante y obtener el mismo resumen histórico sin iniciar la vista interactiva.

**Prioridad**: Ofrece la misma consulta histórica durante una reproducción automatizada.

**Prueba independiente**: Ejecutar la reproducción de una bitácora hasta un instante y comparar el resumen con `historia` para ese instante.

**Escenarios de aceptación**:

1. **Dado** una bitácora reproducible, **cuando** se ejecuta `--replay partida.log --hasta t`, **entonces** se imprime el mismo resumen definido para `historia t` sin vista.
2. **Dado** que la partida termina antes de `t`, **cuando** se ejecuta `--replay partida.log --hasta t`, **entonces** se muestra el estado final y se indica que la partida terminó antes de `t`.

### Casos límite

- Una consulta a un instante posterior al reloj actual se rechaza.
- Cuando varios eventos tienen el mismo instante, la consulta incluye todos ellos.
- Después de usar un pergamino, las acciones revertidas ya no forman parte de la línea consultable.
- Una consulta histórica no debe modificar la partida ni el historial de retroceso.
- Si `--hasta t` queda después del final de la partida reproducida, se muestra el estado final y se indica que terminó antes.
- Para archivos de la Parte I queda pendiente aclarar si se reporta incompatibilidad o se realiza una migración explícita; el enunciado permite ambas alternativas.

## Requisitos

### Requisitos funcionales

- **FR-LIN-001**: El sistema DEBE definir el estado en el instante `t` como el estado después de ejecutar todos los eventos con tiempo menor o igual que `t`.
- **FR-LIN-002**: Si en `t` corresponde una decisión del jugador, la consulta DEBE mostrar el estado justo antes de tomarla.
- **FR-LIN-003**: El sistema DEBE permitir consultar el pasado mediante `historia <t>` y `historia #k`, donde `#k` identifica el estado justo antes de la acción `k` del jugador.
- **FR-LIN-004**: La consulta DEBE mostrar como mínimo el reloj, la sala del jugador, su vida y estadísticas, el inventario, los efectos activos, los enemigos de la sala consultada con su vida y el mapa conocido en ese momento.
- **FR-LIN-005**: La consulta histórica NO DEBE consumir tiempo, registrarse como acción, alterar el estado de la partida ni modificar el historial de retroceso.
- **FR-LIN-006**: El sistema DEBE rechazar la consulta de un instante posterior al reloj actual.
- **FR-LIN-007**: Las acciones revertidas por pergaminos DEBEN dejar de existir en la línea de tiempo consultable.
- **FR-LIN-008**: `--replay partida.log --hasta <t>` DEBE reproducir hasta `t` e imprimir el mismo resumen que la consulta histórica, sin instanciar la vista.
- **FR-LIN-009**: Si la partida reproducida termina antes de `<t>`, la reproducción DEBE mostrar el estado final e indicar que terminó antes.
- **FR-LIN-010**: Guardar y cargar una partida DEBE conservar la línea de tiempo completa.
- **FR-LIN-011**: El formato binario de guardado DEBE cambiar respecto de la Parte I y el sistema NO DEBE cargar en silencio un archivo de la Parte I. El tratamiento concreto del archivo queda sujeto a la aclaración pendiente de FR-LIN-012.
- **FR-LIN-012**: **[NEEDS CLARIFICATION: ¿Se reportará incompatibilidad para un archivo de la Parte I o se ofrecerá una migración explícita?]**
- **FR-LIN-013**: El sistema DEBE permitir configurar con `--checkpoint-cada K` la frecuencia máxima de puntos de control completos, con no más de un punto de control por cada `K` acciones del jugador.
- **FR-LIN-014**: El valor predeterminado de `K` DEBE ser justificado por el grupo mediante mediciones; esta especificación no fija un número.
- **FR-LIN-015**: Una consulta DEBE requerir aplicar o deshacer cambios de no más de `K` acciones del jugador.
- **FR-LIN-016**: Fuera de los puntos de control, el sistema DEBE guardar solo la información necesaria para reconstruir los cambios. La memoria DEBE crecer con los cambios ocurridos más los puntos de control, no con el producto del número de acciones por el tamaño del estado.
- **FR-LIN-017**: Si la reconstrucción re-simula la partida, cada punto de control DEBE incluir el estado del generador aleatorio.
- **FR-LIN-018**: La consulta DEBE tardar menos de 50 ms en una partida de al menos 5 000 acciones con el valor predeterminado de `K`.
- **FR-LIN-019**: El mapa conocido mostrado en una consulta DEBE corresponder al conocimiento del jugador en ese momento, según la capacidad de niebla de guerra.
- **FR-LIN-020**: Cada paso de un viaje «ir a» DEBE contar como una acción ordinaria del jugador para la línea de tiempo.
- **FR-LIN-021**: El formato binario de guardado de esta capacidad DEBE incluir el estado que declaren las demás capacidades.

### Entidades clave

- **Estado histórico**: situación de la partida correspondiente a un instante o al momento inmediatamente anterior a una acción del jugador.
- **Acción del jugador**: decisión registrada en la partida, incluida cada acción individual que compone un viaje «ir a».
- **Punto de control**: estado completo de la partida asociado a una posición de la línea de tiempo.
- **Cambio histórico**: información necesaria para reconstruir las variaciones de estado ocurridas entre puntos de control.
- **Línea de tiempo**: secuencia consultable de los estados y cambios de la partida, recortada cuando se revierten acciones con un pergamino.

## Criterios de éxito

### Resultados medibles

- **SC-LIN-001**: En todas las consultas válidas, el resumen contiene los siete grupos mínimos de información exigidos: reloj, sala, vida y estadísticas, inventario, efectos activos, enemigos de la sala con su vida y mapa conocido.
- **SC-LIN-002**: Una consulta válida no cambia el reloj, el estado de la partida, el registro de acciones ni el historial de retroceso.
- **SC-LIN-003**: En una partida de al menos 5 000 acciones, la consulta tarda menos de 50 ms con el valor predeterminado de `K` justificado por mediciones del grupo.
- **SC-LIN-004**: La memoria de la línea de tiempo crece con los cambios registrados y los puntos de control, sin crecer como acciones por tamaño del estado.
- **SC-LIN-005**: La reproducción hasta un instante produce el mismo resumen histórico, o el estado final con indicación de final anticipado cuando corresponda.

## Supuestos

- El reloj de la partida es el tiempo virtual definido por el juego.
- El conocimiento del mapa forma parte del estado de la partida y se consulta conforme a las reglas de la capacidad de niebla de guerra.
- La selección del valor predeterminado de `K` se documentará tras las mediciones del grupo; no se fija en esta especificación.
- La política para tratar archivos guardados de la Parte I se resolverá mediante `/speckit-clarify`, dentro de las alternativas permitidas por el enunciado.
