# Documento de Decisiones de Diseño — CRIPTA

## 4.1 Qué ocurre a continuación (agenda de eventos)
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión (revisar para eliminar esta linea)

Medición con `--bench` (escala 0.3), heap contra lista lineal (alternativa descartada): con 100, 500 y 2000 eventos pendientes la lista lineal es 1.5x, 5.7x y 15.6x más lenta. Con 600 actores activos (1200 eventos) el peor ciclo tomó 6.17 ms, bajo el límite de 20 ms de §5.2 (carga sintética). Cancelar un tercio de los eventos y reprogramar otro tercio, de forma perezosa, cuesta 0.33 µs por operación.

### Límites conocidos
Pendiente — completar en reunión

## 4.2 Traer el contenido antes de que haga falta (precarga)
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.3 Resolución de referencias del catálogo
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.4 Reutilización y caché persistente
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.5 Inventario
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión (revisar para eliminar esta linea)

El inventario usa una lista doble enlazada con un nodo por objeto. Para soltar el objeto que se está viendo en O(1), el inventario conserva el nodo que devuelve `agregar`, y la lista mantiene su tamaño para aplicar el límite `inventario_max` sin recorrerla.

### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.6 Pergaminos de retroceso e historial reversible
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.7 El rastro del jugador
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.8 Bitácora en pantalla
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.9 Ordenamiento
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.10 Guardado binario de la partida
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.11 Bitácora de partida y reproducción
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión
