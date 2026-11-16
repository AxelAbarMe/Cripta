| Subsistema | Caso | Tiempo | Nota |
|---|---|---:|---|
| agenda | 100 pendientes: heap (elegida) | 2.79 µs/op |  |
| agenda | 100 pendientes: lista lineal (descartada) | 4.38 µs/op | 1.6x más lenta que el heap |
| agenda | 500 pendientes: heap (elegida) | 3.80 µs/op |  |
| agenda | 500 pendientes: lista lineal (descartada) | 21.53 µs/op | 5.7x más lenta que el heap |
| agenda | 2000 pendientes: heap (elegida) | 5.09 µs/op |  |
| agenda | 2000 pendientes: lista lineal (descartada) | 97.36 µs/op | 19.1x más lenta que el heap |
| agenda | cancelar 1/3 y reprogramar 1/3 (perezoso) | 0.47 µs/op |  |
| cache | buscar en 25 fichas: VectorOrdenado (elegida) | 0.41 µs/op |  |
| cache | buscar en 25 fichas: recorrido lineal (descartada) | 0.27 µs/op | el recorrido lineal es 1.5x más rápido que VectorOrdenado |
| cache | marcar uso LRU con 25 fichas: lista doble (elegida) | 0.16 µs/op |  |
| cache | marcar uso LRU con 25 fichas: list.remove+insert (descartada) | 0.13 µs/op | list.remove+insert es 1.2x más rápido que la lista doble |
| cache | buscar en 1000 fichas: VectorOrdenado (elegida) | 0.96 µs/op |  |
| cache | buscar en 1000 fichas: recorrido lineal (descartada) | 9.15 µs/op | el recorrido lineal es 9.5x más lento que VectorOrdenado |
| cache | marcar uso LRU con 1000 fichas: lista doble (elegida) | 0.17 µs/op |  |
| cache | marcar uso LRU con 1000 fichas: list.remove+insert (descartada) | 3.33 µs/op | list.remove+insert es 19.8x más lento que la lista doble |
| disco | recuperar ficha liberada (lectura de disco + parseo) | 51.30 µs/op | referencia del API: ~400 ms por solicitud de red |
| inventario | soltar en medio, n=10: lista doble (elegida) | 0.30 µs/op |  |
| inventario | soltar en medio, n=10: list.pop(i) (descartada) | 0.07 µs/op | list.pop(i) es 4.6x más rápido que la lista doble  <- con inventario_max típico (~10) la diferencia es despreciable |
| inventario | soltar en medio, n=10000: lista doble (elegida) | 0.33 µs/op |  |
| inventario | soltar en medio, n=10000: list.pop(i) (descartada) | 8.24 µs/op | list.pop(i) es 24.6x más lento que la lista doble |
| historial | registrar acción (6 inversas): operaciones inversas (elegida) | 1.90 µs/op |  |
| historial | registrar acción: copia completa de 200 salas + 60 actores (descartada, prohibida) | 757.61 µs/op | 400x más lenta y guarda 5 estados enteros |
| historial | deshacer 5 acciones (30 inversas) | 3.34 µs/op |  |
| ordenamiento | n=10 aleatorio: inserción | 0.003 ms |  |
| ordenamiento | n=10 aleatorio: mergesort | 0.007 ms |  |
| ordenamiento | n=10 aleatorio: burbuja (descartada) | 0.004 ms |  |
| ordenamiento | n=10 aleatorio: AUTOMÁTICO -> insercion | 0.003 ms | 0.98x del mejor de los dos |
| ordenamiento | n=10 casi ordenado (2%): inserción | 0.002 ms |  |
| ordenamiento | n=10 casi ordenado (2%): mergesort | 0.007 ms |  |
| ordenamiento | n=10 casi ordenado (2%): burbuja (descartada) | 0.003 ms |  |
| ordenamiento | n=10 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.002 ms | 1.07x del mejor de los dos |
| ordenamiento | n=10 inverso: inserción | 0.004 ms |  |
| ordenamiento | n=10 inverso: mergesort | 0.007 ms |  |
| ordenamiento | n=10 inverso: burbuja (descartada) | 0.005 ms |  |
| ordenamiento | n=10 inverso: AUTOMÁTICO -> insercion | 0.004 ms | 0.96x del mejor de los dos |
| ordenamiento | n=50 aleatorio: inserción | 0.041 ms |  |
| ordenamiento | n=50 aleatorio: mergesort | 0.051 ms |  |
| ordenamiento | n=50 aleatorio: burbuja (descartada) | 0.096 ms |  |
| ordenamiento | n=50 aleatorio: AUTOMÁTICO -> insercion | 0.047 ms | 1.15x del mejor de los dos |
| ordenamiento | n=50 casi ordenado (2%): inserción | 0.004 ms |  |
| ordenamiento | n=50 casi ordenado (2%): mergesort | 0.041 ms |  |
| ordenamiento | n=50 casi ordenado (2%): burbuja (descartada) | 0.068 ms |  |
| ordenamiento | n=50 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.009 ms | 2.22x del mejor de los dos |
| ordenamiento | n=50 inverso: inserción | 0.104 ms |  |
| ordenamiento | n=50 inverso: mergesort | 0.062 ms |  |
| ordenamiento | n=50 inverso: burbuja (descartada) | 0.144 ms |  |
| ordenamiento | n=50 inverso: AUTOMÁTICO -> merge | 0.062 ms | 1.00x del mejor de los dos |
| ordenamiento | n=200 aleatorio: inserción | 0.922 ms |  |
| ordenamiento | n=200 aleatorio: mergesort | 0.308 ms |  |
| ordenamiento | n=200 aleatorio: burbuja (descartada) | 1.659 ms |  |
| ordenamiento | n=200 aleatorio: AUTOMÁTICO -> merge | 0.228 ms | 0.74x del mejor de los dos |
| ordenamiento | n=200 casi ordenado (2%): inserción | 0.043 ms |  |
| ordenamiento | n=200 casi ordenado (2%): mergesort | 0.209 ms |  |
| ordenamiento | n=200 casi ordenado (2%): burbuja (descartada) | 1.047 ms |  |
| ordenamiento | n=200 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.070 ms | 1.63x del mejor de los dos |
| ordenamiento | n=200 inverso: inserción | 1.358 ms |  |
| ordenamiento | n=200 inverso: mergesort | 0.276 ms |  |
| ordenamiento | n=200 inverso: burbuja (descartada) | 2.387 ms |  |
| ordenamiento | n=200 inverso: AUTOMÁTICO -> merge | 0.286 ms | 1.04x del mejor de los dos |
| ordenamiento | n=1000 aleatorio: inserción | 22.014 ms |  |
| ordenamiento | n=1000 aleatorio: mergesort | 1.705 ms |  |
| ordenamiento | n=1000 aleatorio: AUTOMÁTICO -> merge | 1.965 ms | 1.15x del mejor de los dos |
| ordenamiento | n=1000 casi ordenado (2%): inserción | 1.564 ms |  |
| ordenamiento | n=1000 casi ordenado (2%): mergesort | 1.232 ms |  |
| ordenamiento | n=1000 casi ordenado (2%): AUTOMÁTICO -> merge | 1.356 ms | 1.10x del mejor de los dos |
| ordenamiento | n=1000 inverso: inserción | 36.187 ms |  |
| ordenamiento | n=1000 inverso: mergesort | 1.266 ms |  |
| ordenamiento | n=1000 inverso: AUTOMÁTICO -> merge | 1.351 ms | 1.07x del mejor de los dos |
| ordenamiento | comparaciones n=50 aleatorio | 0.000 ms | inserción=679, merge=222 -> elige merge si comparar es caro |
| ordenamiento | comparaciones n=50 casi ordenado (2%) | 0.000 ms | inserción=108, merge=161 -> elige insercion si comparar es caro |
| ordenamiento | comparaciones n=200 aleatorio | 0.000 ms | inserción=9920, merge=1267 -> elige merge si comparar es caro |
| ordenamiento | comparaciones n=200 casi ordenado (2%) | 0.000 ms | inserción=877, merge=947 -> elige insercion si comparar es caro |
| guardado | 50 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=14066 B, json=34902 B (2.5x el binario) |
| guardado | 50 salas: guardar binario | 1.511 ms |  |
| guardado | 50 salas: guardar JSON | 1.266 ms |  |
| guardado | 50 salas: cargar todo binario | 0.907 ms |  |
| guardado | 50 salas: cargar todo JSON | 0.847 ms | cargar JSON es 1.1x más rápido que cargar binario |
| guardado | 50 salas: cargar UNA sala (binario, con índice) | 0.113 ms | 8x más rápido que cargar todo |
| guardado | 500 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=86510 B, json=231764 B (2.7x el binario) |
| guardado | 500 salas: guardar binario | 4.268 ms |  |
| guardado | 500 salas: guardar JSON | 5.877 ms |  |
| guardado | 500 salas: cargar todo binario | 4.242 ms |  |
| guardado | 500 salas: cargar todo JSON | 3.084 ms | cargar JSON es 1.4x más rápido que cargar binario |
| guardado | 500 salas: cargar UNA sala (binario, con índice) | 0.054 ms | 79x más rápido que cargar todo |
| guardado | 5000 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=738814 B, json=2084958 B (2.8x el binario) |
| guardado | 5000 salas: guardar binario | 41.373 ms |  |
| guardado | 5000 salas: guardar JSON | 53.747 ms |  |
| guardado | 5000 salas: cargar todo binario | 40.840 ms |  |
| guardado | 5000 salas: cargar todo JSON | 40.713 ms | cargar JSON es 1.0x más rápido que cargar binario |
| guardado | 5000 salas: cargar UNA sala (binario, con índice) | 0.049 ms | 828x más rápido que cargar todo |
| ciclo | 100 actores activos, peor de 20 ciclos (200 eventos) | 1.160 ms | 1.16 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| ciclo | 300 actores activos, peor de 20 ciclos (600 eventos) | 4.130 ms | 4.13 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| ciclo | 600 actores activos, peor de 20 ciclos (1200 eventos) | 8.643 ms | 8.64 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| partida | 25 salas, 12 enemigos activos al final, 69 acciones x 3 corridas | 0.288 ms | tiempo típico de una acción: 0.20 ms, peor caso: 0.29 ms (peor de cada corrida: 0.29, 0.29, 0.28 ms; se toma el del medio: 0.29) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| partida | 100 salas, 60 enemigos activos al final, 139 acciones x 3 corridas | 3.115 ms | tiempo típico de una acción: 1.14 ms, peor caso: 3.12 ms (peor de cada corrida: 3.28, 3.12, 3.03 ms; se toma el del medio: 3.12) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| partida | 400 salas, 252 enemigos activos al final, 429 acciones x 3 corridas | 13.213 ms | tiempo típico de una acción: 5.42 ms, peor caso: 13.21 ms (peor de cada corrida: 13.21, 23.33, 12.05 ms; se toma el del medio: 13.21) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| solicitudes | 100 salas, 90 visitadas: contenido | 0.000 ms | con precarga en lotes: 10 solicitudes; una por sala visitada (descartada): 90 solicitudes |
| solicitudes | 100 salas, 90 visitadas: catálogo | 0.000 ms | por lotes: 4 solicitudes; una por ficha (descartada): 7 solicitudes |
| solicitudes | 400 salas, 380 visitadas: contenido | 0.000 ms | con precarga en lotes: 40 solicitudes; una por sala visitada (descartada): 380 solicitudes |
| solicitudes | 400 salas, 380 visitadas: catálogo | 0.000 ms | por lotes: 4 solicitudes; una por ficha (descartada): 7 solicitudes |
| ruta_cazador | R=600, H=1: ciclo con cálculo compartido (elegida) | 0.353 ms | mediana de 120 ciclos, peor 1.300 ms |
| ruta_cazador | R=600, H=1: compartido, búsqueda sola | 224.03 µs/op | 58 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=1: compartido, consultas de costo_de_conexion | 102.06 µs/op | 3979 consultas (1.54 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=1: ciclo con cálculo individual (descartada) | 0.355 ms | mediana de 120 ciclos, peor 1.542 ms |
| ruta_cazador | R=600, H=1: individual, búsqueda sola | 238.81 µs/op | 60 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=1: individual, consultas de costo_de_conexion | 108.62 µs/op | 4105 consultas (1.59 µs cada una) |
| ruta_cazador | R=600, H=1: razón individual/compartido | razón | razón de tiempo 1.01 y de búsquedas 1.03 |
| ruta_cazador | R=600, H=10: ciclo con cálculo compartido (elegida) | 0.551 ms | mediana de 120 ciclos, peor 1.120 ms |
| ruta_cazador | R=600, H=10: compartido, búsqueda sola | 239.34 µs/op | 58 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=10: compartido, consultas de costo_de_conexion | 155.39 µs/op | 5779 consultas (1.61 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=10: ciclo con cálculo individual (descartada) | 2.524 ms | mediana de 120 ciclos, peor 7.485 ms |
| ruta_cazador | R=600, H=10: individual, búsqueda sola | 2461.64 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=10: individual, consultas de costo_de_conexion | 1117.53 µs/op | 40510 consultas (1.66 µs cada una) |
| ruta_cazador | R=600, H=10: razón individual/compartido | razón | razón de tiempo 4.58 y de búsquedas 10.34 |
| ruta_cazador | R=600, H=30: ciclo con cálculo compartido (elegida) | 0.950 ms | mediana de 120 ciclos, peor 2.575 ms |
| ruta_cazador | R=600, H=30: compartido, búsqueda sola | 243.18 µs/op | 58 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=30: compartido, consultas de costo_de_conexion | 269.17 µs/op | 9779 consultas (1.65 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=30: ciclo con cálculo individual (descartada) | 7.514 ms | mediana de 120 ciclos, peor 22.972 ms |
| ruta_cazador | R=600, H=30: individual, búsqueda sola | 7225.28 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=30: individual, consultas de costo_de_conexion | 3283.78 µs/op | 121410 consultas (1.62 µs cada una) |
| ruta_cazador | R=600, H=30: razón individual/compartido | razón | razón de tiempo 7.91 y de búsquedas 31.03 |
| ruta_cazador | R=2400, H=1: ciclo con cálculo compartido (elegida) | 2.384 ms | mediana de 120 ciclos, peor 5.200 ms |
| ruta_cazador | R=2400, H=1: compartido, búsqueda sola | 2423.53 µs/op | 58 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=1: compartido, consultas de costo_de_conexion | 1116.72 µs/op | 39721 consultas (1.69 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=1: ciclo con cálculo individual (descartada) | 2.424 ms | mediana de 120 ciclos, peor 6.428 ms |
| ruta_cazador | R=2400, H=1: individual, búsqueda sola | 2776.13 µs/op | 60 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=1: individual, consultas de costo_de_conexion | 1227.48 µs/op | 40967 consultas (1.80 µs cada una) |
| ruta_cazador | R=2400, H=1: razón individual/compartido | razón | razón de tiempo 1.02 y de búsquedas 1.03 |
| ruta_cazador | R=2400, H=10: ciclo con cálculo compartido (elegida) | 2.594 ms | mediana de 120 ciclos, peor 4.451 ms |
| ruta_cazador | R=2400, H=10: compartido, búsqueda sola | 2414.19 µs/op | 58 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=10: compartido, consultas de costo_de_conexion | 1175.26 µs/op | 41620 consultas (1.69 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=10: ciclo con cálculo individual (descartada) | 23.481 ms | mediana de 120 ciclos, peor 70.588 ms |
| ruta_cazador | R=2400, H=10: individual, búsqueda sola | 25094.99 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=10: individual, consultas de costo_de_conexion | 11536.79 µs/op | 409130 consultas (1.69 µs cada una) |
| ruta_cazador | R=2400, H=10: razón individual/compartido | razón | razón de tiempo 9.05 y de búsquedas 10.34 |
| ruta_cazador | R=2400, H=30: ciclo con cálculo compartido (elegida) | 2.972 ms | mediana de 120 ciclos, peor 5.062 ms |
| ruta_cazador | R=2400, H=30: compartido, búsqueda sola | 2453.37 µs/op | 58 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=30: compartido, consultas de costo_de_conexion | 1289.55 µs/op | 45840 consultas (1.69 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=30: ciclo con cálculo individual (descartada) | 70.175 ms | mediana de 120 ciclos, peor 198.198 ms |
| ruta_cazador | R=2400, H=30: individual, búsqueda sola | 75759.29 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=30: individual, consultas de costo_de_conexion | 34774.57 µs/op | 1227270 consultas (1.70 µs cada una) |
| ruta_cazador | R=2400, H=30: razón individual/compartido | razón | razón de tiempo 23.61 y de búsquedas 31.03 |
| ruta_cazador | mixto 25:11, H=10: ciclo con cálculo compartido (elegida) | 3.067 ms | mediana de 120 ciclos, peor 5.256 ms |
| ruta_cazador | mixto 25:11, H=10: compartido, búsqueda sola | 2721.68 µs/op | 116 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=10: compartido, consultas de costo_de_conexion | 1294.13 µs/op | 45262 consultas (1.72 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | mixto 25:11, H=10: ciclo con cálculo individual (descartada) | 8.811 ms | mediana de 120 ciclos, peor 29.424 ms |
| ruta_cazador | mixto 25:11, H=10: individual, búsqueda sola | 9162.03 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=10: individual, consultas de costo_de_conexion | 4162.02 µs/op | 151096 consultas (1.65 µs cada una) |
| ruta_cazador | mixto 25:11, H=10: razón individual/compartido | razón | razón de tiempo 2.87 y de búsquedas 5.17 |
| ruta_cazador | mixto 25:11, H=30: ciclo con cálculo compartido (elegida) | 3.280 ms | mediana de 120 ciclos, peor 4.851 ms |
| ruta_cazador | mixto 25:11, H=30: compartido, búsqueda sola | 2718.02 µs/op | 116 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=30: compartido, consultas de costo_de_conexion | 1386.22 µs/op | 49328 consultas (1.69 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | mixto 25:11, H=30: ciclo con cálculo individual (descartada) | 26.553 ms | mediana de 120 ciclos, peor 76.924 ms |
| ruta_cazador | mixto 25:11, H=30: individual, búsqueda sola | 28271.31 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=30: individual, consultas de costo_de_conexion | 12932.48 µs/op | 453168 consultas (1.71 µs cada una) |
| ruta_cazador | mixto 25:11, H=30: razón individual/compartido | razón | razón de tiempo 8.10 y de búsquedas 15.52 |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: invalidación selectiva (elegida) | 100.99 µs/op | 1 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 2.823 ms en búsquedas, 0 puertas inestables |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: recalcular siempre (descartada) | 4279.48 µs/op | 140 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 418.351 ms en búsquedas |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: razón recalcular siempre/selectiva | razón | razón de tiempo 42.37 y de búsquedas 140.00 |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: invalidación selectiva (elegida) | 205.52 µs/op | 4 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 11.720 ms en búsquedas, 5 puertas inestables |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: recalcular siempre (descartada) | 4162.78 µs/op | 140 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 407.049 ms en búsquedas |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: razón recalcular siempre/selectiva | razón | razón de tiempo 20.25 y de búsquedas 35.00 |
| ciclo_referencia | cripta-06, 36 cazadores activos al medir, en persecución por ciclo: promedio 4.3 y máximo 6, 100 ciclos x 3 corridas | 3.144 ms | ciclo típico 1.182 ms, peor caso 3.144 ms (peor de cada corrida: 3.233, 3.144, 2.168 ms) -> CUMPLE el límite de 20 ms |