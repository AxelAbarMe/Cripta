# Modelo de datos: línea de tiempo

Los nombres siguientes describen datos lógicos, no nombres obligatorios de clases. Las representaciones físicas deben ser planas y no usar `dict` o `set` como índice.

## Acción vigente del jugador

| Campo | Significado |
|---|---|
| Posición ordinal | Número de acción desde 1, sin contar órdenes rechazadas, comentarios ni consultas. |
| Datos de acción | Tipo y argumentos suficientes para volver a ejecutar la acción aceptada. |
| Límite temporal | Instante virtual asociado a la posición para consultas por tiempo y orden de eventos. |

Las acciones posteriores al límite vigente se descartan al usar pergamino. Cada paso de «ir a» es una acción individual; el comentario que acompaña el viaje no cuenta. (FR-LIN-003, FR-LIN-007, FR-LIN-020)

## Punto de control

| Campo lógico | Significado |
|---|---|
| Número de acciones | Posición de la última acción incluida en el estado. |
| Estado de partida | Proyección plana completa equivalente a `EstadoPartida`. |
| Estado aleatorio | Estado de `random.Random` para continuar la secuencia idéntica. |
| Conocimiento del mapa | Nivel por sala y cuatro observaciones de puerta que declare la capacidad 002. |

Se crea como máximo un checkpoint por cada K acciones. Un checkpoint representa el estado al límite definido por la línea vigente. (FR-LIN-013, FR-LIN-017, FR-LIN-019, FR-LIN-021)

## Cambio histórico

La secuencia entre checkpoints conserva solo datos necesarios para reconstruir, no una copia completa por acción. La estrategia elegida aplica acciones aceptadas desde el checkpoint. El diseño alternativo medido puede codificar mutaciones serializables para invertirlas; las closures existentes del pergamino no forman parte de este registro.

## Línea vigente

| Campo lógico | Significado |
|---|---|
| Acciones | Secuencia ordenada de acciones aceptadas todavía vigentes. |
| Puntos de control | Estados completos ordenados por número de acción, separados por no más de K acciones. |
| Límite vigente | Longitud de la secuencia actual; al retroceder se trunca sin recorrer prefijos. |
| Frecuencia K | Entero mayor o igual a 1, configurable al iniciar; el default se justifica con benchmark. |

Las acciones revertidas no se pueden consultar por número ni tiempo. Una consulta temporal valida primero que `t` no exceda el reloj vigente. (FR-LIN-006, FR-LIN-007, FR-LIN-014, FR-LIN-022)

## Resultado histórico

Proyección de solo lectura con reloj, sala, vida y estadísticas del jugador, inventario, efectos activos, enemigos de la sala consultada con vida y mapa conocido para el instante solicitado. La proyección se obtiene en contexto aislado y no conserva referencias mutables al juego activo. (FR-LIN-004, FR-LIN-005, FR-LIN-019)

## Estado de persistencia

El estado guardado integra línea vigente, checkpoints, acciones entre checkpoints y estados declarados por las demás capacidades. El formato incrementa su versión. La carga de un formato P1 falla explícitamente y no ofrece migración. (FR-LIN-010, FR-LIN-011, FR-LIN-012, FR-LIN-021)

## Reglas de transición

1. Acción aceptada: anexar la acción y su límite temporal; al llegar al múltiplo K, capturar el estado completo y RNG.
2. Acción rechazada/consulta: no anexa ni modifica la línea.
3. Consulta temporal: elegir el límite temporal por la regla de FR-LIN-001/002 y reconstruir desde el checkpoint anterior más cercano.
4. Consulta `#k`: validar acción vigente y devolver estado inmediatamente anterior a esa acción.
5. Pergamino: truncar acciones hasta el final del intervalo revertido y quitar checkpoints posteriores.
6. Carga: restaurar tanto el estado actual como la línea vigente, sin restaurar closures del pergamino.

