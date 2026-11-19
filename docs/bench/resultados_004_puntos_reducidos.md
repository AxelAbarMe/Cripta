# Benchmark 004 con puntos periódicos reducidos

Medición en Windows-11-10.0.26200-SP0 (AMD64) con Python 3.14.6. El comando terminó con código de salida 0.

```powershell
py -m cripta --bench --solo linea_tiempo --escala 1
```

Se repitió la [línea base](resultados_004_linea_base.md) con el mismo fixture, semilla 20261117, 5 000 acciones, 300 salas, 760 salidas y 21 consultas comunes por escenario. Cada celda compara la línea base con la nueva medición.

| Escenario | Puntos periódicos | Memoria estimada de la línea (KiB) | Mediana de consulta (ms) | Máximo observado de consulta (ms) | Peor ciclo (ms) |
|---|---:|---:|---:|---:|---:|
| K=50 | 100 | 34494.7 → 22873.6 (-33.7 %) | 12.616 → 11.935 | 24.817 → 24.457 | 11.885 → 1.933 |
| K=100 | 50 | 17690.4 → 11885.9 (-32.8 %) | 31.490 → 32.976 | 53.273 → 51.072 | 3.668 → 4.349 |
| K=500 | 10 | 4245.8 → 3093.4 (-27.1 %) | 115.495 → 119.972 | 249.615 → 247.549 | 3.214 → 2.667 |
| K=1000 | 5 | 2565.4 → 1992.5 (-22.3 %) | 205.440 → 210.444 | 467.162 → 481.429 | 2.130 → 2.745 |
| sin puntos periódicos | 0 | 882.7 → 882.7 (0.0 %) | 856.935 → 793.650 | 2222.919 → 2232.532 | 2.413 → 2.655 |

La memoria estimada bajó en los cuatro escenarios con puntos periódicos. La métrica suma los tamaños de objetos alcanzables desde las acciones, los ajustes y los puntos periódicos. Quedan fuera de esa suma el punto inicial y la proyección de puertas iniciales de la partida. Los tiempos corresponden a los valores observados en cada corrida.

Con K=100, la memoria estimada bajó un 32.8 %. El máximo observado de consulta bajó a 51.072 ms y sigue por encima de 50 ms. K=50 fue el único escenario con máximo inferior a 50 ms. El peor ciclo de cada escenario quedó por debajo de 20 ms. K=100 sigue provisional y T033 queda abierta para revisar las mediciones.

La suite completa `py -m unittest discover -s tests -t .` terminó en OK con 628 pruebas.

## Salida íntegra

```text
--bench  (Python 3.14.6, escala=1.0)

=== LINEA_TIEMPO  (43.58 s) ===
  cripta-06, semilla 20261117, 5000 acciones, 300 salas, 760 salidas: 2282.310 ms totales, 456.46 µs/op (5000 ops)
      -> tiempo acumulado de ciclos de K=50. Cinco partidas independientes con la misma semilla y carga. Vida máxima 1000000000 fijada antes de iniciar. 21 consultas comunes por acción e instante, incluidos estados inmediatamente anteriores a puntos de control
  K=50: 5000 acciones, 100 puntos periódicos, 21 consultas: 294.847 ms totales, 14040.35 µs/op (21 ops)
      -> memoria de la línea 22873.6 KiB (acciones 882.6, ajustes 0.1, puntos 21990.9). registro medio 9.2 µs/acción, incluida la captura cuando toca. Consulta: mediana 11.935 ms, máximo observado 24.457 ms -> CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 1.933 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  K=100: 5000 acciones, 50 puntos periódicos, 21 consultas: 675.801 ms totales, 32180.98 µs/op (21 ops)
      -> memoria de la línea 11885.9 KiB (acciones 882.6, ajustes 0.1, puntos 11003.2). registro medio 7.1 µs/acción, incluida la captura cuando toca. Consulta: mediana 32.976 ms, máximo observado 51.072 ms -> NO CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 4.349 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  K=500: 5000 acciones, 10 puntos periódicos, 21 consultas: 2717.330 ms totales, 129396.68 µs/op (21 ops)
      -> memoria de la línea 3093.4 KiB (acciones 882.6, ajustes 0.1, puntos 2210.7). registro medio 2.7 µs/acción, incluida la captura cuando toca. Consulta: mediana 119.972 ms, máximo observado 247.549 ms -> NO CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 2.667 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  K=1000: 5000 acciones, 5 puntos periódicos, 21 consultas: 4650.633 ms totales, 221458.71 µs/op (21 ops)
      -> memoria de la línea 1992.5 KiB (acciones 882.6, ajustes 0.1, puntos 1109.8). registro medio 2.5 µs/acción, incluida la captura cuando toca. Consulta: mediana 210.444 ms, máximo observado 481.429 ms -> NO CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 2.745 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  sin puntos periódicos: 5000 acciones, 0 puntos periódicos, 21 consultas: 17243.665 ms totales, 821126.90 µs/op (21 ops)
      -> memoria de la línea 882.7 KiB (acciones 882.6, ajustes 0.1, puntos 0.1). registro medio 1.8 µs/acción, incluida la captura cuando toca. Consulta: mediana 793.650 ms, máximo observado 2232.532 ms -> NO CUMPLE el límite de 50 ms (P2 §6.1). peor ciclo 2.655 ms -> CUMPLE el límite de 20 ms. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  re-simular desde checkpoint (elegida): 5000 acciones, 13 consultas por acción: 28.929 ms totales, 2225.27 µs/op (13 ops)
      -> registrar 6.7 µs por acción (incluye crear los checkpoints), memoria 11885.9 KiB, consulta mediana 28.929 ms y máximo 52.927 ms. Reconstruye el estado completo, con azar y agenda
  reconstruir hacia atrás con cambios serializables (descartada): 5000 acciones, 13 consultas por acción: 0.843 ms totales, 64.82 µs/op (13 ops)
      -> registrar 14.9 µs por acción, memoria 9193.6 KiB, consulta mediana 0.843 ms y máximo 1.173 ms (deshace desde el final, así que el costo crece con las acciones que faltan). Modelo de cota inferior: solo registra los 9 campos visibles (sala, vida, estadísticas, inventario, efectos y enemigos de la sala), no el azar, la agenda ni el mapa conocido. Coincide con la re-simulación en 13 de 13 consultas. estimación de memoria: suma de sys.getsizeof de cada objeto que se alcanza desde la línea, sin descontar lo que comparten (cota superior)
  búsqueda límite temporal a acción: binaria manual (elegida) frente a lineal (descartada), 5000 elementos, 400 consultas: 0.463 ms totales, 1.16 µs/op (400 ops)
      -> binaria 1.16 µs por consulta con 12.3 inspecciones en promedio; lineal 106.13 µs con 2627.7; lineal es 91.7x más lento que binaria; mismo resultado en las consultas. La binaria cuenta la llamada al método y la lineal es un bucle directo sobre la lista
  búsqueda checkpoint anterior: binaria manual (elegida) frente a lineal (descartada), 50 elementos, 400 consultas: 0.214 ms totales, 0.54 µs/op (400 ops)
      -> binaria 0.54 µs por consulta con 5.8 inspecciones en promedio; lineal 0.96 µs con 25.2; lineal es 1.8x más lento que binaria; mismo resultado en las consultas. La binaria cuenta la llamada al método y la lineal es un bucle directo sobre la lista
  recorte por pergamino: desde el final (elegida) frente a escaneo y filtrado (descartada), 5000 acciones, 30 repeticiones: 0.095 ms totales, 3.18 µs/op (30 ops)
      -> desde el final 3.18 µs y 2 registros procesados por recorte; escaneo y filtrado 405.12 µs y 5050 registros examinados; el filtrado es 127.5x más lento que el recorte desde el final
  restauración de un checkpoint: vía materializada (elegida) frente a preparar salas (descartada), 75 salas con contenido, 5 repeticiones: 3.584 ms totales, 716.82 µs/op (5 ops)
      -> materializada 3.584 ms y 0.0 llamadas al cliente por consulta; con preparar_sala 12.702 ms y 16.0 llamadas (75 llamadas a preparar_sala); preparar salas es 3.5x más lento que la vía materializada. Cada llamada al cliente de fixtures lee un archivo: es la E/S de la consulta

Total: 43.58 s
```
