# Contrato de CLI: línea de tiempo

## Consultar historia durante una partida

- Forma: `historia <t>` o `historia #<k>`.
- `<t>` es un instante del reloj virtual. Se rechaza si supera el reloj actual.
- `#k` identifica el estado justo antes de la acción vigente k, numerada desde 1.
- Se presenta como mínimo: reloj, sala, vida y estadísticas, inventario, efectos activos, enemigos de la sala y su vida, y mapa conocido.
- Una consulta válida o rechazada no consume tiempo, no se registra, no altera el estado ni cambia el historial de retroceso.
- Si se rechaza, se informa el motivo.

## Configurar checkpoints

- Forma: `py -m cripta [opciones] --checkpoint-cada K`.
- K debe ser entero mayor o igual que 1. Cero, negativos y texto inválido impiden iniciar e informan el motivo.
- El default se elige y justifica con mediciones; no queda fijado por este contrato.

## Reproducir hasta un instante

- Forma: `py -m cripta --replay partida.log --hasta <t>`.
- Reproduce el prefijo temporal conforme a las reglas de FR-LIN-001 y FR-LIN-002 e imprime el mismo resumen histórico.
- Si la partida termina antes de `<t>`, imprime el estado final e indica el final anticipado.
- No inicia la vista interactiva.

## Guardar y cargar

- El guardado nuevo conserva toda la línea vigente y los campos persistentes declarados por otras capacidades.
- Un archivo P1 se rechaza como incompatible por versión, permanece intacto y no se ofrece migración.

