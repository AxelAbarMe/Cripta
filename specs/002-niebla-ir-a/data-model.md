# Modelo de datos: conocimiento del jugador

## Conocimiento del jugador

Estado nuevo propiedad de la partida y fuente única para representar el mapa y las adyacencias a la vista y al viaje «ir a».

| Campo lógico | Dominio | Significado |
|---|---|---|
| Estado por sala | `desconocida`, `avistada`, `explorada` | Nivel de información del jugador. La sala inicial comienza explorada. |
| Última observación por salida | `no_observada`, `abierta`, `cerrada` | Memoria de la puerta por dirección cardinal; sobrevive a cambios reales hasta una observación nueva. |

Los datos viven en listas contiguas indexadas por id entero. No se usa tabla hash. La proyección persistida contiene valores, no closures ni referencias al modelo vivo.

## Transiciones especificadas

- Inicio: sala inicial → explorada.
- Al explorar una sala: sus destinos no explorados → avistados; se revelan nombre, salidas, costos y observaciones conforme a spec.
- Al entrar con antorcha encendida: vecinas → exploradas; se revela la puerta entre cada vecina y la sala de entrada, no contenido ni otras puertas.
- Apagar antorcha: no elimina conocimiento.
- Encender antorcha sin entrar: no cambia vecinas.
- Observar una puerta: su memoria pasa a abierta o cerrada según el estado real observado.
- Cambio real con el jugador en uno de los dos extremos (incluido un cierre automático): su memoria se actualiza de inmediato.
- Pergamino: restaura en orden inverso las celdas cambiadas en la acción que deshace.

## Viaje

El viaje no es un estado persistido separado. Antes de cada paso se deriva una ruta del conocimiento vigente: destino explorado, solo salas exploradas y puertas recordadas abiertas. El avance vive durante la orden en el controlador; cada paso confirmado es una acción ordinaria. La detención devuelve motivos ordenados según `spec.md`.

## Integración con persistencia

El estado lógico de partida agrega valores por sala y observaciones por puerta. `EstadoPartida` y la proyección/restauración se coordinan con la capacidad 004. Este documento no define nombres de campos binarios, codificación, versión, checkpoints ni migración.
