# Línea base del benchmark 004

Medición en Windows-11-10.0.26200-SP0 (AMD64) con Python 3.14.6.

El comando terminó con código de salida 0.

```powershell
py -m cripta --bench --solo linea_tiempo --escala 1
```

```text
--bench  (Python 3.14.6, escala=1.0)

=== LINEA_TIEMPO  (43.79 s) ===
  cripta-06, semilla 20261117, 5000 acciones, 300 salas, 760 salidas: 2294.047 ms totales, 458.81 µs/op (5000 ops)
      -> tiempo acumulado de ciclos de K=50. Cinco partidas independientes con la misma semilla y carga. Vida máxima 1000000000 fijada antes de iniciar. 21 consultas comunes por acción e instante, incluidos estados inmediatamente anteriores a puntos de control
  K=50: 5000 acciones, 100 puntos periódicos, 21 consultas: 295.705 ms totales, 14081.20 µs/op (21 ops)
      -> memoria de la línea 34494.7 KiB (acciones 882.6, ajustes 0.1, puntos 33612.0). registro medio 12.8 µs/acción, incluida la captura cuando toca. Consulta: mediana 12.616 ms, máximo observado 24.817 ms -> CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 11.885 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  K=100: 5000 acciones, 50 puntos periódicos, 21 consultas: 701.783 ms totales, 33418.25 µs/op (21 ops)
      -> memoria de la línea 17690.4 KiB (acciones 882.6, ajustes 0.1, puntos 16807.7). registro medio 8.3 µs/acción, incluida la captura cuando toca. Consulta: mediana 31.490 ms, máximo observado 53.273 ms -> NO CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 3.668 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  K=500: 5000 acciones, 10 puntos periódicos, 21 consultas: 2592.561 ms totales, 123455.27 µs/op (21 ops)
      -> memoria de la línea 4245.8 KiB (acciones 882.6, ajustes 0.1, puntos 3363.1). registro medio 2.9 µs/acción, incluida la captura cuando toca. Consulta: mediana 115.495 ms, máximo observado 249.615 ms -> NO CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 3.214 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  K=1000: 5000 acciones, 5 puntos periódicos, 21 consultas: 4628.236 ms totales, 220392.18 µs/op (21 ops)
      -> memoria de la línea 2565.4 KiB (acciones 882.6, ajustes 0.1, puntos 1682.7). registro medio 2.5 µs/acción, incluida la captura cuando toca. Consulta: mediana 205.440 ms, máximo observado 467.162 ms -> NO CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 2.130 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  sin puntos periódicos: 5000 acciones, 0 puntos periódicos, 21 consultas: 17818.684 ms totales, 848508.76 µs/op (21 ops)
      -> memoria de la línea 882.7 KiB (acciones 882.6, ajustes 0.1, puntos 0.1). registro medio 1.6 µs/acción, incluida la captura cuando toca. Consulta: mediana 856.935 ms, máximo observado 2222.919 ms -> NO CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 2.413 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  re-simular desde checkpoint (elegida): 5000 acciones, 13 consultas por acción: 31.178 ms totales, 2398.33 µs/op (13 ops)
      -> registrar 8.8 µs por acción (incluye crear los checkpoints), memoria 17690.4 KiB, consulta mediana 31.178 ms y máximo 50.537 ms. Reconstruye el estado completo, con azar y agenda
  reconstruir hacia atrás con cambios serializables (descartada): 5000 acciones, 13 consultas por acción: 0.881 ms totales, 67.78 µs/op (13 ops)
      -> registrar 14.8 µs por acción, memoria 9193.6 KiB, consulta mediana 0.881 ms y máximo 1.618 ms (deshace desde el final, así que el costo crece con las acciones que faltan). Modelo de cota inferior: solo registra los 9 campos visibles (sala, vida, estadísticas, inventario, efectos y enemigos de la sala), no el azar, la agenda ni el mapa conocido. Coincide con la re-simulación en 13 de 13 consultas. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  búsqueda límite temporal a acción: binaria manual (elegida) frente a lineal (descartada), 5000 elementos, 400 consultas: 0.556 ms totales, 1.39 µs/op (400 ops)
      -> binaria 1.39 µs por consulta con 12.3 inspecciones en promedio; lineal 105.78 µs con 2627.7; lineal es 76.1x más lento que binaria; mismo resultado en las consultas. La binaria cuenta la llamada al método y la lineal es un bucle directo sobre la lista
  búsqueda checkpoint anterior: binaria manual (elegida) frente a lineal (descartada), 50 elementos, 400 consultas: 0.211 ms totales, 0.53 µs/op (400 ops)
      -> binaria 0.53 µs por consulta con 5.8 inspecciones en promedio; lineal 0.92 µs con 25.2; lineal es 1.8x más lento que binaria; mismo resultado en las consultas. La binaria cuenta la llamada al método y la lineal es un bucle directo sobre la lista
  recorte por pergamino: desde el final (elegida) frente a escaneo y filtrado (descartada), 5000 acciones, 30 repeticiones: 0.054 ms totales, 1.80 µs/op (30 ops)
      -> desde el final 1.80 µs y 2 registros procesados por recorte; escaneo y filtrado 388.34 µs y 5050 registros examinados; el filtrado es 215.3x más lento que el recorte desde el final
  restauración de un checkpoint: vía materializada (elegida) frente a preparar salas (descartada), 75 salas con contenido, 5 repeticiones: 4.126 ms totales, 825.12 µs/op (5 ops)
      -> materializada 4.126 ms y 0.0 llamadas al cliente por consulta; con preparar_sala 14.383 ms y 16.0 llamadas (75 llamadas a preparar_sala); preparar salas es 3.5x más lento que la vía materializada. Cada llamada al cliente de fixtures lee un archivo: es la E/S de la consulta

Total: 43.79 s
```
