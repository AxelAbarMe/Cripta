# Prompt para `/speckit-specify` — 004 Línea de tiempo

```text
Capacidad: línea de tiempo (consulta del pasado de la partida) con puntos de control.

Estado en el instante t: el estado después de ejecutar todos los eventos con tiempo <= t; si a t le
corresponde una decisión del jugador, es el estado justo antes de tomarla.
"historia <t>" o "historia #k" (estado justo antes de la acción k del jugador) muestra como mínimo:
reloj, sala del jugador, vida y estadísticas, inventario, efectos activos, enemigos de esa sala con
su vida y el mapa conocido en ese momento. No consume tiempo, no se registra como acción, no
altera estado del juego ni del historial de retroceso.
"--replay partida.log --hasta <t>" reproduce hasta t e imprime el mismo resumen sin vista.
Los pergaminos recortan la línea: las acciones revertidas dejan de existir. Consultar un instante
posterior al reloj actual se rechaza.
Memoria: se permiten copias completas del estado (puntos de control) pero no más de una cada K
acciones del jugador; K se configura con --checkpoint-cada K (el valor por defecto lo justifica el
grupo con mediciones). Una consulta nunca requiere aplicar o deshacer cambios de más de K acciones.
Fuera de los puntos de control solo se guarda la información necesaria para reconstruir cambios; la
memoria crece con los cambios ocurridos más un punto de control cada K, nunca con acciones×tamaño
del estado. Si se reconstruye re-simulando, el punto de control incluye el estado del generador
aleatorio.
Persistencia: guardar y cargar conserva la línea completa; el formato binario cambia y un archivo
de la Parte I se detecta como incompatible (o se migra explícitamente), nunca se carga en silencio.
Rendimiento: consulta < 50 ms en partida de >= 5 000 acciones con K por defecto.

Coordinación con otras capacidades (no redefine sus reglas): el mapa conocido de la historia es el
conocimiento del jugador de la capacidad de niebla de guerra, que forma parte del estado de la
partida y se revierte con el pergamino; cada paso de un viaje «ir a» es una acción ordinaria del
jugador. Esta capacidad es dueña de la versión del formato binario de guardado, que debe incluir
el estado que declaren las demás capacidades.

Escenarios del Apéndice B:
- historia <t> con t mayor que el reloj actual: se rechaza
- historia tras un pergamino: no muestra las acciones revertidas
- varios eventos en el mismo t: muestra el estado después de todos
- historia no consume tiempo, no va a partida.log, no modifica el historial de retroceso
- --replay --hasta t posterior al final: muestra el estado final e indica que terminó antes
- carga de archivo de la Parte I: incompatibilidad reportada o migración explícita

Prefijo: FR-LIN-NNN. Sin estructuras, clases ni módulos.
```