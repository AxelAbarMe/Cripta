| Subsistema | Caso | Tiempo | Nota |
|---|---|---:|---|
| agenda | 100 pendientes: heap (elegida) | 2.90 µs/op |  |
| agenda | 100 pendientes: lista lineal (descartada) | 4.54 µs/op | 1.6x más lenta que el heap |
| agenda | 500 pendientes: heap (elegida) | 5.40 µs/op |  |
| agenda | 500 pendientes: lista lineal (descartada) | 25.61 µs/op | 4.7x más lenta que el heap |
| agenda | 2000 pendientes: heap (elegida) | 5.87 µs/op |  |
| agenda | 2000 pendientes: lista lineal (descartada) | 125.17 µs/op | 21.3x más lenta que el heap |
| agenda | cancelar 1/3 y reprogramar 1/3 (perezoso) | 0.60 µs/op |  |
| cache | buscar en 25 fichas: VectorOrdenado (elegida) | 0.45 µs/op |  |
| cache | buscar en 25 fichas: recorrido lineal (descartada) | 0.28 µs/op | el recorrido lineal es 1.6x más rápido que VectorOrdenado |
| cache | marcar uso LRU con 25 fichas: lista doble (elegida) | 0.17 µs/op |  |
| cache | marcar uso LRU con 25 fichas: list.remove+insert (descartada) | 0.14 µs/op | list.remove+insert es 1.2x más rápido que la lista doble |
| cache | buscar en 1000 fichas: VectorOrdenado (elegida) | 1.03 µs/op |  |
| cache | buscar en 1000 fichas: recorrido lineal (descartada) | 9.63 µs/op | el recorrido lineal es 9.3x más lento que VectorOrdenado |
| cache | marcar uso LRU con 1000 fichas: lista doble (elegida) | 0.17 µs/op |  |
| cache | marcar uso LRU con 1000 fichas: list.remove+insert (descartada) | 3.21 µs/op | list.remove+insert es 18.6x más lento que la lista doble |
| disco | recuperar ficha liberada (lectura de disco + parseo) | 54.08 µs/op | referencia del API: ~400 ms por solicitud de red |
| inventario | soltar en medio, n=10: lista doble (elegida) | 0.29 µs/op |  |
| inventario | soltar en medio, n=10: list.pop(i) (descartada) | 0.06 µs/op | list.pop(i) es 4.7x más rápido que la lista doble  <- con inventario_max típico (~10) la diferencia es despreciable |
| inventario | soltar en medio, n=10000: lista doble (elegida) | 0.39 µs/op |  |
| inventario | soltar en medio, n=10000: list.pop(i) (descartada) | 1.02 µs/op | list.pop(i) es 2.6x más lento que la lista doble |
| historial | registrar acción (6 inversas): operaciones inversas (elegida) | 1.69 µs/op |  |
| historial | registrar acción: copia completa de 200 salas + 60 actores (descartada, prohibida) | 767.52 µs/op | 453x más lenta y guarda 5 estados enteros |
| historial | deshacer 5 acciones (30 inversas) | 3.42 µs/op |  |
| ordenamiento | n=10 aleatorio: inserción | 0.003 ms |  |
| ordenamiento | n=10 aleatorio: mergesort | 0.007 ms |  |
| ordenamiento | n=10 aleatorio: burbuja (descartada) | 0.004 ms |  |
| ordenamiento | n=10 aleatorio: AUTOMÁTICO -> insercion | 0.003 ms | 0.99x del mejor de los dos |
| ordenamiento | n=10 casi ordenado (2%): inserción | 0.002 ms |  |
| ordenamiento | n=10 casi ordenado (2%): mergesort | 0.007 ms |  |
| ordenamiento | n=10 casi ordenado (2%): burbuja (descartada) | 0.004 ms |  |
| ordenamiento | n=10 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.002 ms | 1.03x del mejor de los dos |
| ordenamiento | n=10 inverso: inserción | 0.004 ms |  |
| ordenamiento | n=10 inverso: mergesort | 0.007 ms |  |
| ordenamiento | n=10 inverso: burbuja (descartada) | 0.005 ms |  |
| ordenamiento | n=10 inverso: AUTOMÁTICO -> insercion | 0.004 ms | 1.01x del mejor de los dos |
| ordenamiento | n=50 aleatorio: inserción | 0.042 ms |  |
| ordenamiento | n=50 aleatorio: mergesort | 0.053 ms |  |
| ordenamiento | n=50 aleatorio: burbuja (descartada) | 0.100 ms |  |
| ordenamiento | n=50 aleatorio: AUTOMÁTICO -> insercion | 0.050 ms | 1.20x del mejor de los dos |
| ordenamiento | n=50 casi ordenado (2%): inserción | 0.006 ms |  |
| ordenamiento | n=50 casi ordenado (2%): mergesort | 0.055 ms |  |
| ordenamiento | n=50 casi ordenado (2%): burbuja (descartada) | 0.061 ms |  |
| ordenamiento | n=50 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.008 ms | 1.33x del mejor de los dos |
| ordenamiento | n=50 inverso: inserción | 0.095 ms |  |
| ordenamiento | n=50 inverso: mergesort | 0.053 ms |  |
| ordenamiento | n=50 inverso: burbuja (descartada) | 0.085 ms |  |
| ordenamiento | n=50 inverso: AUTOMÁTICO -> merge | 0.038 ms | 0.72x del mejor de los dos |
| ordenamiento | n=200 aleatorio: inserción | 0.630 ms |  |
| ordenamiento | n=200 aleatorio: mergesort | 0.226 ms |  |
| ordenamiento | n=200 aleatorio: burbuja (descartada) | 1.430 ms |  |
| ordenamiento | n=200 aleatorio: AUTOMÁTICO -> merge | 0.253 ms | 1.12x del mejor de los dos |
| ordenamiento | n=200 casi ordenado (2%): inserción | 0.046 ms |  |
| ordenamiento | n=200 casi ordenado (2%): mergesort | 0.212 ms |  |
| ordenamiento | n=200 casi ordenado (2%): burbuja (descartada) | 0.713 ms |  |
| ordenamiento | n=200 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.052 ms | 1.13x del mejor de los dos |
| ordenamiento | n=200 inverso: inserción | 1.233 ms |  |
| ordenamiento | n=200 inverso: mergesort | 0.178 ms |  |
| ordenamiento | n=200 inverso: burbuja (descartada) | 1.633 ms |  |
| ordenamiento | n=200 inverso: AUTOMÁTICO -> merge | 0.207 ms | 1.16x del mejor de los dos |
| ordenamiento | n=1000 aleatorio: inserción | 17.729 ms |  |
| ordenamiento | n=1000 aleatorio: mergesort | 1.660 ms |  |
| ordenamiento | n=1000 aleatorio: AUTOMÁTICO -> merge | 1.700 ms | 1.02x del mejor de los dos |
| ordenamiento | n=1000 casi ordenado (2%): inserción | 1.826 ms |  |
| ordenamiento | n=1000 casi ordenado (2%): mergesort | 1.560 ms |  |
| ordenamiento | n=1000 casi ordenado (2%): AUTOMÁTICO -> merge | 1.347 ms | 0.86x del mejor de los dos |
| ordenamiento | n=1000 inverso: inserción | 33.862 ms |  |
| ordenamiento | n=1000 inverso: mergesort | 1.033 ms |  |
| ordenamiento | n=1000 inverso: AUTOMÁTICO -> merge | 1.118 ms | 1.08x del mejor de los dos |
| ordenamiento | comparaciones n=50 aleatorio | 0.000 ms | inserción=679, merge=222 -> elige merge si comparar es caro |
| ordenamiento | comparaciones n=50 casi ordenado (2%) | 0.000 ms | inserción=108, merge=161 -> elige insercion si comparar es caro |
| ordenamiento | comparaciones n=200 aleatorio | 0.000 ms | inserción=9920, merge=1267 -> elige merge si comparar es caro |
| ordenamiento | comparaciones n=200 casi ordenado (2%) | 0.000 ms | inserción=877, merge=947 -> elige insercion si comparar es caro |
| guardado | 50 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=14066 B, json=34902 B (2.5x el binario) |
| guardado | 50 salas: guardar binario | 1.524 ms |  |
| guardado | 50 salas: guardar JSON | 1.412 ms |  |
| guardado | 50 salas: cargar todo binario | 0.483 ms |  |
| guardado | 50 salas: cargar todo JSON | 0.505 ms | cargar JSON es 1.0x más lento que cargar binario |
| guardado | 50 salas: cargar UNA sala (binario, con índice) | 0.042 ms | 11x más rápido que cargar todo |
| guardado | 500 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=86510 B, json=231764 B (2.7x el binario) |
| guardado | 500 salas: guardar binario | 4.364 ms |  |
| guardado | 500 salas: guardar JSON | 6.080 ms |  |
| guardado | 500 salas: cargar todo binario | 4.343 ms |  |
| guardado | 500 salas: cargar todo JSON | 3.481 ms | cargar JSON es 1.2x más rápido que cargar binario |
| guardado | 500 salas: cargar UNA sala (binario, con índice) | 0.055 ms | 79x más rápido que cargar todo |
| guardado | 5000 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=738814 B, json=2084958 B (2.8x el binario) |
| guardado | 5000 salas: guardar binario | 38.358 ms |  |
| guardado | 5000 salas: guardar JSON | 52.397 ms |  |
| guardado | 5000 salas: cargar todo binario | 40.029 ms |  |
| guardado | 5000 salas: cargar todo JSON | 38.231 ms | cargar JSON es 1.0x más rápido que cargar binario |
| guardado | 5000 salas: cargar UNA sala (binario, con índice) | 0.050 ms | 809x más rápido que cargar todo |
| ciclo | 100 actores activos, peor de 20 ciclos (200 eventos) | 1.654 ms | 1.65 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| ciclo | 300 actores activos, peor de 20 ciclos (600 eventos) | 3.851 ms | 3.85 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| ciclo | 600 actores activos, peor de 20 ciclos (1200 eventos) | 8.509 ms | 8.51 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| partida | 25 salas, 12 enemigos activos al final, 69 acciones x 3 corridas | 0.354 ms | tiempo típico de una acción: 0.21 ms, peor caso: 0.35 ms (peor de cada corrida: 0.29, 0.46, 0.35 ms; se toma el del medio: 0.35) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| partida | 100 salas, 60 enemigos activos al final, 139 acciones x 3 corridas | 2.822 ms | tiempo típico de una acción: 1.21 ms, peor caso: 2.82 ms (peor de cada corrida: 2.82, 3.14, 2.81 ms; se toma el del medio: 2.82) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| partida | 400 salas, 252 enemigos activos al final, 429 acciones x 3 corridas | 12.035 ms | tiempo típico de una acción: 5.18 ms, peor caso: 12.04 ms (peor de cada corrida: 12.04, 17.59, 10.40 ms; se toma el del medio: 12.04) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| solicitudes | 100 salas, 90 visitadas: contenido | 0.000 ms | con precarga en lotes: 10 solicitudes; una por sala visitada (descartada): 90 solicitudes |
| solicitudes | 100 salas, 90 visitadas: catálogo | 0.000 ms | por lotes: 4 solicitudes; una por ficha (descartada): 7 solicitudes |
| solicitudes | 400 salas, 380 visitadas: contenido | 0.000 ms | con precarga en lotes: 40 solicitudes; una por sala visitada (descartada): 380 solicitudes |
| solicitudes | 400 salas, 380 visitadas: catálogo | 0.000 ms | por lotes: 4 solicitudes; una por ficha (descartada): 7 solicitudes |
| ruta_cazador | R=600, H=1: ciclo con cálculo compartido (elegida) | 0.371 ms | mediana de 120 ciclos, peor 0.864 ms |
| ruta_cazador | R=600, H=1: compartido, búsqueda sola | 241.08 µs/op | 58 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=1: compartido, consultas de costo_de_conexion | 112.95 µs/op | 3979 consultas (1.70 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=1: ciclo con cálculo individual (descartada) | 0.369 ms | mediana de 120 ciclos, peor 1.542 ms |
| ruta_cazador | R=600, H=1: individual, búsqueda sola | 265.70 µs/op | 60 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=1: individual, consultas de costo_de_conexion | 121.16 µs/op | 4105 consultas (1.77 µs cada una) |
| ruta_cazador | R=600, H=1: razón individual/compartido | razón | razón de tiempo 0.99 y de búsquedas 1.03 |
| ruta_cazador | R=600, H=10: ciclo con cálculo compartido (elegida) | 0.551 ms | mediana de 120 ciclos, peor 1.593 ms |
| ruta_cazador | R=600, H=10: compartido, búsqueda sola | 230.41 µs/op | 58 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=10: compartido, consultas de costo_de_conexion | 151.78 µs/op | 5779 consultas (1.58 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=10: ciclo con cálculo individual (descartada) | 2.622 ms | mediana de 120 ciclos, peor 8.558 ms |
| ruta_cazador | R=600, H=10: individual, búsqueda sola | 2446.72 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=10: individual, consultas de costo_de_conexion | 1115.56 µs/op | 40510 consultas (1.65 µs cada una) |
| ruta_cazador | R=600, H=10: razón individual/compartido | razón | razón de tiempo 4.76 y de búsquedas 10.34 |
| ruta_cazador | R=600, H=30: ciclo con cálculo compartido (elegida) | 0.976 ms | mediana de 120 ciclos, peor 2.666 ms |
| ruta_cazador | R=600, H=30: compartido, búsqueda sola | 234.22 µs/op | 58 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=30: compartido, consultas de costo_de_conexion | 254.66 µs/op | 9779 consultas (1.56 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=30: ciclo con cálculo individual (descartada) | 7.619 ms | mediana de 120 ciclos, peor 24.305 ms |
| ruta_cazador | R=600, H=30: individual, búsqueda sola | 7273.97 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=30: individual, consultas de costo_de_conexion | 3288.56 µs/op | 121410 consultas (1.63 µs cada una) |
| ruta_cazador | R=600, H=30: razón individual/compartido | razón | razón de tiempo 7.80 y de búsquedas 31.03 |
| ruta_cazador | R=2400, H=1: ciclo con cálculo compartido (elegida) | 2.464 ms | mediana de 120 ciclos, peor 4.330 ms |
| ruta_cazador | R=2400, H=1: compartido, búsqueda sola | 2527.57 µs/op | 58 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=1: compartido, consultas de costo_de_conexion | 1166.04 µs/op | 39721 consultas (1.76 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=1: ciclo con cálculo individual (descartada) | 2.548 ms | mediana de 120 ciclos, peor 7.108 ms |
| ruta_cazador | R=2400, H=1: individual, búsqueda sola | 2621.83 µs/op | 60 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=1: individual, consultas de costo_de_conexion | 1197.97 µs/op | 40967 consultas (1.75 µs cada una) |
| ruta_cazador | R=2400, H=1: razón individual/compartido | razón | razón de tiempo 1.03 y de búsquedas 1.03 |
| ruta_cazador | R=2400, H=10: ciclo con cálculo compartido (elegida) | 2.734 ms | mediana de 120 ciclos, peor 6.403 ms |
| ruta_cazador | R=2400, H=10: compartido, búsqueda sola | 2439.72 µs/op | 58 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=10: compartido, consultas de costo_de_conexion | 1169.49 µs/op | 41620 consultas (1.69 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=10: ciclo con cálculo individual (descartada) | 24.086 ms | mediana de 120 ciclos, peor 67.480 ms |
| ruta_cazador | R=2400, H=10: individual, búsqueda sola | 25520.58 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=10: individual, consultas de costo_de_conexion | 11701.05 µs/op | 409130 consultas (1.72 µs cada una) |
| ruta_cazador | R=2400, H=10: razón individual/compartido | razón | razón de tiempo 8.81 y de búsquedas 10.34 |
| ruta_cazador | R=2400, H=30: ciclo con cálculo compartido (elegida) | 3.136 ms | mediana de 120 ciclos, peor 6.060 ms |
| ruta_cazador | R=2400, H=30: compartido, búsqueda sola | 2427.47 µs/op | 58 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=30: compartido, consultas de costo_de_conexion | 1281.28 µs/op | 45840 consultas (1.68 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=30: ciclo con cálculo individual (descartada) | 72.278 ms | mediana de 120 ciclos, peor 203.891 ms |
| ruta_cazador | R=2400, H=30: individual, búsqueda sola | 75950.16 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=30: individual, consultas de costo_de_conexion | 34792.58 µs/op | 1227270 consultas (1.70 µs cada una) |
| ruta_cazador | R=2400, H=30: razón individual/compartido | razón | razón de tiempo 23.04 y de búsquedas 31.03 |
| ruta_cazador | mixto 25:11, H=10: ciclo con cálculo compartido (elegida) | 2.933 ms | mediana de 120 ciclos, peor 5.180 ms |
| ruta_cazador | mixto 25:11, H=10: compartido, búsqueda sola | 2966.59 µs/op | 116 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=10: compartido, consultas de costo_de_conexion | 1396.97 µs/op | 45262 consultas (1.85 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | mixto 25:11, H=10: ciclo con cálculo individual (descartada) | 9.474 ms | mediana de 120 ciclos, peor 32.865 ms |
| ruta_cazador | mixto 25:11, H=10: individual, búsqueda sola | 9749.44 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=10: individual, consultas de costo_de_conexion | 4445.60 µs/op | 151096 consultas (1.77 µs cada una) |
| ruta_cazador | mixto 25:11, H=10: razón individual/compartido | razón | razón de tiempo 3.23 y de búsquedas 5.17 |
| ruta_cazador | mixto 25:11, H=30: ciclo con cálculo compartido (elegida) | 3.830 ms | mediana de 120 ciclos, peor 6.967 ms |
| ruta_cazador | mixto 25:11, H=30: compartido, búsqueda sola | 3050.90 µs/op | 116 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=30: compartido, consultas de costo_de_conexion | 1553.20 µs/op | 49328 consultas (1.89 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | mixto 25:11, H=30: ciclo con cálculo individual (descartada) | 31.639 ms | mediana de 120 ciclos, peor 91.984 ms |
| ruta_cazador | mixto 25:11, H=30: individual, búsqueda sola | 31616.86 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=30: individual, consultas de costo_de_conexion | 14247.79 µs/op | 453168 consultas (1.89 µs cada una) |
| ruta_cazador | mixto 25:11, H=30: razón individual/compartido | razón | razón de tiempo 8.26 y de búsquedas 15.52 |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: invalidación selectiva (elegida) | 105.10 µs/op | 1 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 3.036 ms en búsquedas, 0 puertas inestables |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: recalcular siempre (descartada) | 4897.05 µs/op | 140 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 477.115 ms en búsquedas |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: razón recalcular siempre/selectiva | razón | razón de tiempo 46.59 y de búsquedas 140.00 |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: invalidación selectiva (elegida) | 217.68 µs/op | 4 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 12.680 ms en búsquedas, 5 puertas inestables |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: recalcular siempre (descartada) | 4309.46 µs/op | 140 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 420.687 ms en búsquedas |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: razón recalcular siempre/selectiva | razón | razón de tiempo 19.80 y de búsquedas 35.00 |
| ciclo_referencia | cripta-06, 36 cazadores activos al medir, en persecución por ciclo: promedio 4.3 y máximo 6, 100 ciclos x 3 corridas | 2.880 ms | ciclo típico 1.342 ms, peor caso 2.880 ms (peor de cada corrida: 2.773, 3.147, 2.880 ms) -> CUMPLE el límite de 20 ms |