# Modelo de datos: línea de tiempo

Los nombres siguientes describen datos lógicos, no nombres obligatorios de clases. Las representaciones físicas deben ser planas y no usar `dict` o `set` como índice.

## Acción vigente del jugador

| Campo | Significado |
|---|---|
| Posición ordinal | Número de acción desde 1, sin contar órdenes rechazadas, comentarios ni consultas. |
| Datos de acción | Tipo y argumentos suficientes para volver a ejecutar la acción aceptada. |
| Límite temporal | Instante virtual asociado a la posición para consultas por tiempo y orden de eventos. |

Las acciones posteriores al límite vigente se descartan al usar pergamino. Cada paso de «ir a» es una acción individual; el comentario que acompaña el viaje no cuenta. El pergamino tampoco recibe número: `partida.log` conserva su línea y las líneas de acciones revertidas, pero #k se refiere solo a la línea vigente: las acciones revertidas dejan de tener número y k se rechaza si es cero o mayor que la cantidad de acciones vigentes. Tras el recorte, la numeración continúa desde la última acción vigente. (FR-LIN-003, FR-LIN-007, FR-LIN-020)

## Ajuste de inventario

Entrada de línea sin número ni costo para K, anexada al aceptar un pergamino. Contiene las instancias de pergamino afectadas: el consumido y el recogido dentro del intervalo revertido que no vuelve al suelo. La reconstrucción aplica el ajuste al llegar a su posición. Si un pergamino posterior trunca por detrás de este ajuste, los ajustes afectados se acumulan en el nuevo final de la línea para preservar el inventario que mantiene la partida viva. (FR-LIN-005, FR-LIN-007)

## Punto de control

| Campo lógico | Significado |
|---|---|
| Número de acciones | Posición de la última acción incluida en el estado. |
| Estado de partida | Proyección plana completa equivalente a `EstadoPartida`. |
| Estado aleatorio | Estado de `random.Random` para continuar la secuencia idéntica. |
| Conocimiento del mapa | Nivel por sala y cuatro observaciones de puerta que declare la capacidad 002. |
| Costos conocidos de salida | Costos que forman parte de la proyección persistida de conocimiento declarada por 002. |

Se crea como máximo un checkpoint por cada K acciones. El punto de control es el estado en el punto de decisión del jugador que sigue a la acción múltiplo de K, después de ejecutar los eventos hasta esa decisión. Coincide con la definición de estado de Parte II §3.6 para `historia #(k+1)`. Tras pergamino se descartan todos los checkpoints cuyo número de acciones supera la longitud vigente; el checkpoint exactamente en el borde se conserva. (FR-LIN-013, FR-LIN-017, FR-LIN-019, FR-LIN-021)

## Cambio histórico

La secuencia entre checkpoints conserva solo datos necesarios para reconstruir, no una copia completa por acción. La estrategia elegida aplica acciones aceptadas desde el checkpoint. El diseño alternativo medido puede codificar mutaciones serializables para invertirlas; las closures existentes del pergamino no forman parte de este registro.

## Línea vigente

| Campo lógico | Significado |
|---|---|
| Acciones y ajustes | Secuencia ordenada de acciones aceptadas y ajustes de inventario todavía vigentes. Solo las acciones reciben número y cuentan para K. |
| Puntos de control | Estados completos ordenados por número de acción, separados por no más de K acciones. |
| Límite vigente | Longitud de la secuencia actual; al retroceder se trunca sin recorrer prefijos. |
| Frecuencia K | Entero mayor o igual a 1, configurable al iniciar; el default se justifica con benchmark. |

Las acciones revertidas no se pueden consultar por número ni tiempo. Una consulta temporal valida primero que `t` no exceda el reloj vigente. El cursor del inventario pertenece a la interfaz (`_no_reversibles`); el resumen histórico no depende de su posición. (FR-LIN-006, FR-LIN-007, FR-LIN-014, FR-LIN-022)

## Resultado histórico

Proyección de solo lectura con reloj, sala, vida y estadísticas del jugador, inventario, efectos activos, enemigos de la sala consultada con vida y mapa conocido para el instante solicitado. La proyección se obtiene en contexto aislado y no conserva referencias mutables al juego activo. (FR-LIN-004, FR-LIN-005, FR-LIN-019)

## Estado de persistencia

El estado guardado integra línea vigente, checkpoints, acciones entre checkpoints y estados declarados por las demás capacidades, incluidos los costos conocidos de salida definidos por 002. 004 realiza el único cambio de versión binaria del grupo; los campos y su proyección de conocimiento los define 002. La carga de un formato P1 falla explícitamente y no ofrece migración. Los costos se incluyen en la medición de memoria; si resulta excesiva, podrían recalcularse desde el esqueleto (límite conocido, no decisión). (FR-LIN-010, FR-LIN-011, FR-LIN-012, FR-LIN-021)

## Reglas de transición

1. Acción aceptada: anexar la acción y su límite temporal; al llegar al múltiplo K, capturar el estado completo y RNG.
2. Acción rechazada/consulta: no anexa ni modifica la línea.
3. Consulta temporal: elegir el límite temporal por la regla de FR-LIN-001/002 y reconstruir desde el checkpoint anterior más cercano.
4. Consulta `#k`: validar acción vigente y devolver estado inmediatamente anterior a esa acción.
5. Pergamino: truncar acciones hasta el final de la acción revertida y quitar checkpoints con número de acciones mayor que la longitud vigente resultante. Anexar en la posición del pergamino un ajuste de inventario con instancias afectadas, sin número ni cuenta para K. Si un pergamino posterior trunca por detrás del ajuste, acumular los ajustes afectados en el nuevo final. Esto refleja que P1 no restaura el consumido ni devuelve al suelo el pergamino recogido en el intervalo revertido (`Partida._usar_pergamino`, `Inventario._deshacer_recoger`). El cursor excluido de las inversas (`Inventario._no_reversibles`) no interviene en el resumen histórico.
6. Carga: restaurar tanto el estado actual como la línea vigente, sin restaurar closures del pergamino.

## Reconstrucción aislada

La reconstrucción mantiene `HistorialRetroceso.sin_registrar()` activo, no tiene bitácora asociada y no genera mensajes. Tanto el movimiento como la restauración actual pueden preparar salas mediante `precarga.preparar_sala`; en particular, `persistencia_modelo.restaurar_sala` lo llama por cada sala con contenido cargado, provocando E/S por consulta y posible red. La reconstrucción toma el contenido estático (esqueleto, fichas, tipos de enemigos y trampas) de las salas ya materializadas en la partida viva o cargada y aplica encima solo el estado dinámico del checkpoint, mediante una vía de restauración que no llama a `precarga.preparar_sala`. No se usa fixture como sustituto de la partida guardada. `historia` y `--replay --hasta` comparten el mismo componente que transforma el estado reconstruido en resumen. Replay completa la bitácora para formar la línea vigente, luego consulta t limitado al reloj final; si t supera ese reloj indica el final anticipado. La prueba de equivalencia usa una bitácora con pergamino, porque `docs/ejemplos/partida_cripta-02.log` no lo contiene (FR-LIN-008, FR-LIN-009, SC-LIN-005).

## Coordinación con otras capacidades

La 001 cambió las vistas de salidas y enemigos (`SalidaVista`, `EnemigoVista`), `Partida.vista()` y `_paneles_izquierdos`. El resumen histórico muestra enemigos de la sala con su vida mediante esas vistas (Depende de 001). El criterio de cripta de referencia —mayor total de salas o constante `CRIPTA_REFERENCIA` de 001— se unificará con el grupo y permanece sin decisión.

La 002 define los campos de conocimiento y su proyección persistida; 004 guarda esos datos, incluidos los costos, en checkpoints y realiza el único cambio de versión binaria del grupo.

