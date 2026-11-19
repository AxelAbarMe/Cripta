# Especificación de funcionalidad: Línea de tiempo

**Rama de funcionalidad**: `004-linea-de-tiempo`

**Creada**: 2026-11-15

**Estado**: Borrador

**Entrada**: Prompt de usuario: `prompts/p2/02-specify-004.md`

## Aclaraciones

### Sesión 2026-11-16

- P: ¿Cómo debe numerarse k en historia #k y qué debe ocurrir si k es cero o no corresponde a una acción existente? → R: La primera acción es 1. Cero y cualquier valor sin acción correspondiente se rechazan. «Acción correspondiente» significa una acción que ya ocurrió y sigue vigente (no revertida por pergamino); el valor siguiente a la última acción vigente se rechaza, igual que t mayor que el reloj.
- P: ¿Una orden del jugador que se rechaza debe contar al numerar las acciones de historia #k? → R: Solo cuentan las acciones ejecutadas y registradas en partida.log; las órdenes rechazadas, las consultas de historia y del mapa, y las líneas de comentario de la bitácora no cuentan. Cada paso de un viaje «ir a» cuenta como una acción.
- P: ¿El uso de un pergamino recibe número en «historia #k» y cómo continúa la numeración después del recorte? → R: El pergamino no es una acción numerada; recorta la línea vigente y la numeración continúa desde la última acción vigente.
- P: Si `t` coincide con el momento de una decisión del jugador, ¿qué estado debe mostrar `historia t`? → R: Se incluyen todos los eventos con tiempo menor que t y los eventos de t que la agenda de la Parte I ejecuta antes de la decisión del jugador; se muestra el estado justo antes de esa decisión. La decisión misma y los eventos de t posteriores a ella no se incluyen. Si en t no hay decisión del jugador, se aplica FR-LIN-001: estado después de todos los eventos de t.
- P: Después de un pergamino que revierte eventos, ¿cómo debe tratarse `historia t` para un instante que pertenecía a esos eventos revertidos? → R: Tras un pergamino el reloj queda en el valor restaurado, así que un `t` posterior a ese reloj se rechaza igual que cualquier `t` mayor que el reloj actual; un `t` menor o igual se acepta y muestra el estado de la línea vigente en ese instante, sin las acciones revertidas. Para `historia #k`, #k se refiere solo a la línea vigente: las acciones revertidas dejan de tener número y k se rechaza si es cero o mayor que la cantidad de acciones vigentes.
- P: Al cargar un archivo guardado de la Parte I, ¿debe el sistema reportar incompatibilidad o permitir una migración explícita? → R: Al cargar un archivo de la Parte I se reporta la incompatibilidad por versión y no se carga; nunca se carga en silencio ni se modifica o borra el archivo (la invalidación es por versión, como pide la capacidad de terreno y cazador). No se ofrece migración.
- P: ¿Qué valores acepta --checkpoint-cada K y qué ocurre con un valor inválido? → R: K debe ser un entero mayor o igual que 1. Un valor inválido (cero, negativo o no numérico) se rechaza al iniciar, informando el motivo, y la partida no inicia.
- P: ¿Qué ocurre con una consulta de historia rechazada? → R: Toda consulta de historia rechazada (instante posterior al reloj, «#k» inválido o argumento mal formado) informa el motivo del rechazo y no produce ningún efecto: no consume tiempo, no se registra ni cambia el estado o el historial de retroceso.

## Escenarios de usuario y pruebas

### Historia de usuario 1: Consultar un estado pasado (Prioridad: P1)

Como jugador, quiero consultar el estado de la partida en un instante anterior para entender qué ocurría entonces sin alterar la partida actual.

**Prioridad**: Es la función central de la línea de tiempo y permite inspeccionar el pasado durante una partida.

**Prueba independiente**: Consultar un instante válido y comparar el resumen mostrado con el estado correspondiente de la partida.

**Escenarios de aceptación**:

1. **Dado** que el reloj actual de la partida es `r`, **cuando** se consulta `historia t` con `t > r`, **entonces** la consulta se rechaza.
2. **Dado** que ocurrieron varios eventos en el instante `t` y no hay una decisión del jugador en `t`, **cuando** se consulta `historia t`, **entonces** se muestra el estado después de todos los eventos con tiempo menor o igual que `t`.
3. **Dado** que a `t` le corresponde una decisión del jugador, **cuando** se consulta `historia t`, **entonces** se incluyen los eventos con tiempo menor que `t` y los eventos de `t` que la agenda de la Parte I ejecuta antes de esa decisión, y se muestra el estado justo antes de ella; la decisión y los eventos posteriores de `t` no se incluyen.
4. **Dado** un instante válido, **cuando** se consulta `historia t`, **entonces** el resumen incluye como mínimo reloj, sala del jugador, vida y estadísticas, inventario, efectos activos, enemigos de esa sala con su vida y mapa conocido en ese momento.
5. **Dado** un estado válido de la partida, **cuando** se consulta `historia t`, **entonces** la consulta no consume tiempo, no se registra como acción y no altera el estado actual ni el historial de retroceso.
6. **Dado** que el jugador usó un pergamino y revirtió acciones, **cuando** consulta `historia`, **entonces** no se muestran las acciones revertidas.
7. **Dado** un estado válido de la partida, **cuando** se consulta `historia t`, **entonces** la consulta no se registra en `partida.log`.
8. **Dado** una consulta de historia con instante posterior al reloj, «#k» inválido o argumento mal formado, **cuando** se realiza la consulta, **entonces** se informa el motivo del rechazo y no se consume tiempo, no se registra ni cambia el estado o el historial de retroceso. (FR-LIN-023)

### Historia de usuario 2: Consultar antes de una acción (Prioridad: P1)

Como jugador, quiero localizar un estado justo antes de una acción numerada para revisar la partida por su secuencia de decisiones.

**Prioridad**: Permite consultar la historia por la referencia de acción que define el prompt.

**Prueba independiente**: Consultar `historia #k` y verificar que el resumen representa el estado justo antes de la acción `k`.

**Escenarios de aceptación**:

1. **Dado** que existe una acción vigente del jugador numerada `k` desde 1, **cuando** se consulta `historia #k`, **entonces** se muestra el estado justo antes de esa acción.
2. **Dado** que existe una acción vigente `k`, **cuando** se consulta `historia #k` con cero, un valor sin acción vigente correspondiente o el valor siguiente a la última acción vigente, **entonces** la consulta se rechaza.
3. **Dado** que se numeran las acciones, **cuando** se consulta `historia #k`, **entonces** solo cuentan las acciones ejecutadas y registradas, salvo el uso de pergamino, que recorta la línea y no se numera; tampoco cuentan las órdenes rechazadas, las consultas de historia y del mapa ni las líneas de comentario de la bitácora.
4. **Dado** un viaje «ir a», **cuando** se numeran las acciones, **entonces** cada paso cuenta como una acción.

### Historia de usuario 3: Reproducir hasta un instante sin vista (Prioridad: P2)

Como persona que revisa una partida, quiero reproducir su bitácora hasta un instante y obtener el mismo resumen histórico sin iniciar la vista interactiva.

**Prioridad**: Ofrece la misma consulta histórica durante una reproducción automatizada.

**Prueba independiente**: Ejecutar la reproducción de una bitácora hasta un instante y comparar el resumen con `historia` para ese instante.

**Escenarios de aceptación**:

1. **Dado** una bitácora reproducible, **cuando** se ejecuta `--replay partida.log --hasta t`, **entonces** se reproduce la bitácora completa para construir la misma línea vigente que la partida viva y se consulta con el mismo componente que `historia <t>`, sin vista.
2. **Dado** que la partida termina antes de `t`, **cuando** se ejecuta `--replay partida.log --hasta t`, **entonces** se muestra el estado final y se indica que la partida terminó antes de `t`.

### Historia de usuario 4: Guardar y cargar la línea de tiempo (Prioridad: P2)

Como jugador, quiero que la línea de tiempo se conserve al guardar y cargar una partida y que se identifiquen explícitamente los archivos guardados de la Parte I.

**Prioridad**: Garantiza que lo consultable en el pasado sobreviva al guardado y que ningún archivo antiguo se cargue sin avisar.

**Prueba independiente**: Guardar y cargar una partida con historia y comparar `historia t` antes y después; cargar un archivo de la Parte I y verificar el resultado.

**Escenarios de aceptación**:

1. **Dado** una partida con una línea de tiempo, **cuando** se guarda y se carga, **entonces** se conserva la línea completa. (FR-LIN-010)
2. **Dado** un archivo guardado de la Parte I, **cuando** se intenta cargar, **entonces** se reporta la incompatibilidad por versión, no se carga, no se modifica ni se borra el archivo y no se ofrece una migración. (FR-LIN-011, FR-LIN-012)

### Historia de usuario 5: Configurar los puntos de control (Prioridad: P2)

Como jugador, quiero indicar cada cuántas acciones se guardan puntos de control para configurar la consulta de la línea de tiempo.

**Prioridad**: Permite configurar la frecuencia máxima de los puntos de control.

**Prueba independiente**: Iniciar con valores válidos e inválidos de `--checkpoint-cada K` y verificar que un valor inválido impide iniciar la partida e informa el motivo.

**Escenarios de aceptación**:

1. **Dado** un valor cero, negativo o no numérico para `K`, **cuando** se inicia con `--checkpoint-cada K`, **entonces** se rechaza al iniciar, se informa el motivo y la partida no inicia. (FR-LIN-022)

### Casos límite

- Una consulta a un instante posterior al reloj actual se rechaza.
- Cuando varios eventos tienen el mismo instante, la consulta incluye todos ellos si no hay una decisión del jugador en ese instante; si la hay, incluye solo los eventos anteriores a la decisión según la agenda de la Parte I.
- Después de usar un pergamino, el reloj queda en el valor restaurado y las acciones revertidas ya no forman parte de la línea consultable. Un `t` posterior a ese reloj se rechaza; un `t` menor o igual se acepta y muestra el estado de la línea vigente, sin las acciones revertidas. #k se refiere solo a la línea vigente: las acciones revertidas dejan de tener número y k se rechaza si es cero o mayor que la cantidad de acciones vigentes.
- Una consulta histórica no debe modificar la partida ni el historial de retroceso.
- Si `--hasta t` queda después del final de la partida reproducida, se muestra el estado final y se indica que terminó antes.
- Un archivo guardado de la Parte I se rechaza por incompatibilidad de versión sin cargarlo, modificarlo ni borrarlo; no se ofrece migración.

## Requisitos

### Requisitos funcionales

- **FR-LIN-001**: Si en el instante `t` no corresponde una decisión del jugador, el sistema DEBE definir el estado como el estado después de ejecutar todos los eventos con tiempo menor o igual que `t`.
- **FR-LIN-002**: Si en `t` corresponde una decisión del jugador, la consulta DEBE incluir todos los eventos con tiempo menor que `t` y los eventos de `t` que la agenda de la Parte I ejecuta antes de esa decisión. DEBE mostrar el estado justo antes de tomarla, sin incluir la decisión ni los eventos de `t` posteriores a ella.
- **FR-LIN-003**: El sistema DEBE permitir consultar el pasado mediante `historia <t>` y `historia #k`, donde `#k` identifica el estado justo antes de la acción vigente `k` del jugador. Las acciones se numeran desde 1; solo cuentan las acciones ejecutadas y registradas, salvo el uso de pergamino, que recorta la línea vigente y no se numera. Las órdenes rechazadas, las consultas de historia y del mapa, y las líneas de comentario de la bitácora NO DEBEN contar; cada paso de un viaje «ir a» DEBE contar como una acción. Cero, cualquier valor sin acción vigente correspondiente y el valor siguiente a la última acción vigente DEBEN rechazarse.
- **FR-LIN-004**: La consulta DEBE mostrar como mínimo el reloj, la sala del jugador, su vida y estadísticas, el inventario, los efectos activos, los enemigos de la sala consultada con su vida y el mapa conocido en ese momento.
- **FR-LIN-005**: La consulta histórica NO DEBE consumir tiempo, registrarse como acción, aparecer en `partida.log`, alterar el estado de la partida ni modificar el historial de retroceso.
- **FR-LIN-006**: El sistema DEBE rechazar la consulta de un instante posterior al reloj actual, incluido el reloj restaurado por un pergamino. Un instante menor o igual que ese reloj DEBE mostrar el estado de la línea vigente en ese instante.
- **FR-LIN-007**: Las acciones revertidas por pergaminos DEBEN dejar de existir en la línea de tiempo consultable. #k se refiere solo a la línea vigente: las acciones revertidas dejan de tener número y k se rechaza si es cero o mayor que la cantidad de acciones vigentes. Una consulta temporal DEBE mostrar solo el estado de la línea vigente, sin incluir acciones revertidas.
- **FR-LIN-008**: `--replay partida.log --hasta <t>` DEBE reproducir la bitácora completa para construir la misma línea vigente que la partida viva y consultar con el mismo componente que `historia <t>`, sin instanciar la vista. Si `t` supera el reloj final, DEBE limitar la consulta a ese reloj e indicar el final anticipado conforme a FR-LIN-009.
- **FR-LIN-009**: Si la partida reproducida termina antes de `<t>`, la reproducción DEBE mostrar el estado final e indicar que terminó antes.
- **FR-LIN-010**: Guardar y cargar una partida DEBE conservar la línea de tiempo completa.
- **FR-LIN-011**: El formato binario de guardado DEBE cambiar respecto de la Parte I. Al intentar cargar un archivo de la Parte I, el sistema DEBE reportar incompatibilidad por versión y NO DEBE cargarlo en silencio, modificarlo ni borrarlo.
- **FR-LIN-012**: El sistema NO DEBE ofrecer migración de archivos de la Parte I.
- **FR-LIN-013**: El sistema DEBE permitir configurar con `--checkpoint-cada K` la frecuencia máxima de puntos de control completos, con no más de un punto de control por cada `K` acciones del jugador.
- **FR-LIN-014**: El valor predeterminado de `K` DEBE ser justificado por el grupo mediante mediciones; esta especificación no fija un número.
- **FR-LIN-015**: Una consulta DEBE requerir aplicar o deshacer cambios de no más de `K` acciones del jugador.
- **FR-LIN-016**: Fuera de los puntos de control, el sistema DEBE guardar solo la información necesaria para reconstruir los cambios. La memoria DEBE crecer con los cambios ocurridos más los puntos de control, no con el producto del número de acciones por el tamaño del estado.
- **FR-LIN-017**: Si la reconstrucción re-simula la partida, cada punto de control DEBE incluir el estado del generador aleatorio.
- **FR-LIN-018**: La consulta DEBE tardar menos de 50 ms en una partida de al menos 5 000 acciones con el valor predeterminado de `K`.
- **FR-LIN-019**: El mapa conocido mostrado en una consulta DEBE corresponder al conocimiento del jugador en ese momento, según la capacidad de niebla de guerra.
- **FR-LIN-020**: Cada paso de un viaje «ir a» DEBE contar como una acción ordinaria del jugador para la línea de tiempo.
- **FR-LIN-021**: El formato binario de guardado de esta capacidad DEBE incluir el estado que declaren las demás capacidades.
- **FR-LIN-022**: `K` en `--checkpoint-cada K` DEBE ser un entero mayor o igual que 1. Un valor inválido DEBE rechazarse al iniciar, informando el motivo, y la partida NO DEBE iniciar.
- **FR-LIN-023**: Toda consulta de historia rechazada por instante posterior al reloj, «#k» inválido o argumento mal formado DEBE informar el motivo del rechazo y NO DEBE producir efecto alguno: no consumir tiempo, no registrarse ni cambiar el estado o el historial de retroceso.

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
- **SC-LIN-005**: La reproducción de la bitácora completa produce la misma línea vigente y el mismo resumen histórico que `historia <t>`; si `t` supera el reloj final, consulta ese reloj e indica el final anticipado. La prueba incluye una bitácora con pergamino.
- **SC-LIN-006**: Guardar y cargar conserva la línea de tiempo completa y un archivo de la Parte I nunca se carga en silencio.
- **SC-LIN-007**: Un valor inválido de `K` y una consulta de historia rechazada informan su motivo y no producen efecto alguno.

## Supuestos

- El reloj de la partida es el tiempo virtual definido por el juego.
- El conocimiento del mapa forma parte del estado de la partida y se consulta conforme a las reglas de la capacidad de niebla de guerra.
- La selección del valor predeterminado de `K` se documentará tras las mediciones del grupo; no se fija en esta especificación.
- Los archivos guardados de la Parte I se rechazan por incompatibilidad de versión, sin cargarlos, modificarlos ni borrarlos, y no se ofrece migración.
- Decisiones del grupo tomadas en las sesiones de aclaraciones, pendientes de confirmar con el profesor porque el enunciado no las fija expresamente:
  - Las acciones se numeran desde 1 en «historia #k»; solo cuentan las acciones ejecutadas y registradas, y los valores sin acción vigente correspondiente se rechazan.
  - El uso de pergamino no se numera: recorta la línea y la numeración continúa desde la última acción vigente.
  - Los archivos guardados de la Parte I se rechazan por versión y no se ofrece migración (el enunciado permite también migrarlos explícitamente).
  - `--checkpoint-cada K` exige un entero mayor o igual que 1; un valor inválido se rechaza al iniciar informando el motivo y la partida no inicia.
  - Como los pergaminos quedan fuera de la reversión (Parte I §2.11), `historia` de instantes anteriores al uso de un pergamino reconstruye el inventario a partir de las acciones vigentes, y el efecto del pergamino se aplica desde su posición en adelante.
  