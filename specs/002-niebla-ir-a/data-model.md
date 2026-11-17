# Modelo de datos: conocimiento del jugador

## Conocimiento del jugador

Estado nuevo propiedad de la partida y fuente única para representar el mapa y las adyacencias a la vista y al viaje «ir a».

| Campo lógico | Dominio | Significado |
|---|---|---|
| Estado por sala | `desconocida`, `avistada`, `explorada` | Nivel de información del jugador. La sala inicial comienza explorada. |
| Última observación por salida | `no_observada`, `abierta`, `cerrada` | Memoria de la puerta por dirección cardinal; sobrevive a cambios reales hasta una observación nueva. |
| Costo conocido por salida | entero positivo por dirección cardinal | Costo revelado al explorar la sala, en lista propia indexada por id para consulta O(1). |

Estados, observaciones y costos viven en listas propias contiguas indexadas por id entero. No se usa tabla hash. La proyección persistida contiene valores, no closures ni referencias al modelo vivo; incluye costos revelados y los restaura sin recalcularlos desde el esqueleto.

## Transiciones especificadas

- Inicio: sala inicial → explorada.
- Al explorar una sala: sus destinos no explorados → avistados; se revelan nombre, salidas y costos y se inicializan los costos en la lista propia por id. Las salidas sin puerta cerrable quedan abiertas conforme a FR-NIE-025.
- Al entrar con antorcha encendida: vecinas → exploradas; se revela la puerta entre cada vecina y la sala de entrada, no contenido ni otras puertas.
- Apagar antorcha: no elimina conocimiento.
- Encender antorcha sin entrar: no cambia vecinas.
- Observar una puerta: su memoria pasa a abierta o cerrada según el estado real observado.
- Cambio real con el jugador en uno de los dos extremos (incluido un cierre automático): su memoria se actualiza de inmediato.
- Pergamino: restaura en orden inverso las celdas cambiadas en la acción que deshace.

## Viaje

El viaje no es un estado persistido separado. Antes de cada paso se deriva una ruta del conocimiento vigente: destino explorado, solo salas exploradas y puertas recordadas abiertas. El avance vive durante la orden en el controlador; cada paso confirmado es una acción ordinaria. La detención devuelve motivos ordenados según `spec.md`.

## Integración con persistencia

El estado lógico agrega estados por sala, observaciones por puerta y costos conocidos por salida. Esta capacidad define esos campos y su proyección. La 004 es dueña del formato binario y su versión y realizará un único cambio de versión. Los costos forman parte de la proyección persistida y se restauran desde ella. Este documento no define bytes, checkpoints ni migración.
