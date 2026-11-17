| Subsistema | Caso | Tiempo | Nota |
|---|---|---:|---|
| agenda | 100 pendientes: heap (elegida) | 3.33 µs/op |  |
| agenda | 100 pendientes: lista lineal (descartada) | 4.92 µs/op | 1.5x más lenta que el heap |
| agenda | 500 pendientes: heap (elegida) | 4.51 µs/op |  |
| agenda | 500 pendientes: lista lineal (descartada) | 24.96 µs/op | 5.5x más lenta que el heap |
| agenda | 2000 pendientes: heap (elegida) | 5.93 µs/op |  |
| agenda | 2000 pendientes: lista lineal (descartada) | 99.49 µs/op | 16.8x más lenta que el heap |
| agenda | cancelar 1/3 y reprogramar 1/3 (perezoso) | 0.48 µs/op |  |
| cache | buscar en 25 fichas: VectorOrdenado (elegida) | 0.42 µs/op |  |
| cache | buscar en 25 fichas: recorrido lineal (descartada) | 0.27 µs/op | el recorrido lineal es 1.5x más rápido que VectorOrdenado |
| cache | marcar uso LRU con 25 fichas: lista doble (elegida) | 0.16 µs/op |  |
| cache | marcar uso LRU con 25 fichas: list.remove+insert (descartada) | 0.12 µs/op | list.remove+insert es 1.3x más rápido que la lista doble |
| cache | buscar en 1000 fichas: VectorOrdenado (elegida) | 1.06 µs/op |  |
| cache | buscar en 1000 fichas: recorrido lineal (descartada) | 9.79 µs/op | el recorrido lineal es 9.2x más lento que VectorOrdenado |
| cache | marcar uso LRU con 1000 fichas: lista doble (elegida) | 0.18 µs/op |  |
| cache | marcar uso LRU con 1000 fichas: list.remove+insert (descartada) | 3.48 µs/op | list.remove+insert es 18.9x más lento que la lista doble |
| disco | recuperar ficha liberada (lectura de disco + parseo) | 49.16 µs/op | referencia del API: ~400 ms por solicitud de red |
| inventario | soltar en medio, n=10: lista doble (elegida) | 0.49 µs/op |  |
| inventario | soltar en medio, n=10: list.pop(i) (descartada) | 0.10 µs/op | list.pop(i) es 4.8x más rápido que la lista doble  <- con inventario_max típico (~10) la diferencia es despreciable |
| inventario | soltar en medio, n=10000: lista doble (elegida) | 0.34 µs/op |  |
| inventario | soltar en medio, n=10000: list.pop(i) (descartada) | 8.99 µs/op | list.pop(i) es 26.7x más lento que la lista doble |
| historial | registrar acción (6 inversas): operaciones inversas (elegida) | 1.90 µs/op |  |
| historial | registrar acción: copia completa de 200 salas + 60 actores (descartada, prohibida) | 784.10 µs/op | 413x más lenta y guarda 5 estados enteros |
| historial | deshacer 5 acciones (30 inversas) | 3.26 µs/op |  |
| ordenamiento | n=10 aleatorio: inserción | 0.003 ms |  |
| ordenamiento | n=10 aleatorio: mergesort | 0.007 ms |  |
| ordenamiento | n=10 aleatorio: burbuja (descartada) | 0.004 ms |  |
| ordenamiento | n=10 aleatorio: AUTOMÁTICO -> insercion | 0.003 ms | 1.01x del mejor de los dos |
| ordenamiento | n=10 casi ordenado (2%): inserción | 0.002 ms |  |
| ordenamiento | n=10 casi ordenado (2%): mergesort | 0.007 ms |  |
| ordenamiento | n=10 casi ordenado (2%): burbuja (descartada) | 0.004 ms |  |
| ordenamiento | n=10 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.002 ms | 1.05x del mejor de los dos |
| ordenamiento | n=10 inverso: inserción | 0.004 ms |  |
| ordenamiento | n=10 inverso: mergesort | 0.007 ms |  |
| ordenamiento | n=10 inverso: burbuja (descartada) | 0.005 ms |  |
| ordenamiento | n=10 inverso: AUTOMÁTICO -> insercion | 0.004 ms | 1.01x del mejor de los dos |
| ordenamiento | n=50 aleatorio: inserción | 0.043 ms |  |
| ordenamiento | n=50 aleatorio: mergesort | 0.054 ms |  |
| ordenamiento | n=50 aleatorio: burbuja (descartada) | 0.209 ms |  |
| ordenamiento | n=50 aleatorio: AUTOMÁTICO -> insercion | 0.041 ms | 0.95x del mejor de los dos |
| ordenamiento | n=50 casi ordenado (2%): inserción | 0.005 ms |  |
| ordenamiento | n=50 casi ordenado (2%): mergesort | 0.040 ms |  |
| ordenamiento | n=50 casi ordenado (2%): burbuja (descartada) | 0.042 ms |  |
| ordenamiento | n=50 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.006 ms | 1.33x del mejor de los dos |
| ordenamiento | n=50 inverso: inserción | 0.068 ms |  |
| ordenamiento | n=50 inverso: mergesort | 0.038 ms |  |
| ordenamiento | n=50 inverso: burbuja (descartada) | 0.098 ms |  |
| ordenamiento | n=50 inverso: AUTOMÁTICO -> merge | 0.046 ms | 1.21x del mejor de los dos |
| ordenamiento | n=200 aleatorio: inserción | 0.735 ms |  |
| ordenamiento | n=200 aleatorio: mergesort | 0.238 ms |  |
| ordenamiento | n=200 aleatorio: burbuja (descartada) | 1.514 ms |  |
| ordenamiento | n=200 aleatorio: AUTOMÁTICO -> merge | 0.301 ms | 1.26x del mejor de los dos |
| ordenamiento | n=200 casi ordenado (2%): inserción | 0.040 ms |  |
| ordenamiento | n=200 casi ordenado (2%): mergesort | 0.184 ms |  |
| ordenamiento | n=200 casi ordenado (2%): burbuja (descartada) | 0.675 ms |  |
| ordenamiento | n=200 casi ordenado (2%): AUTOMÁTICO -> insercion | 0.052 ms | 1.30x del mejor de los dos |
| ordenamiento | n=200 inverso: inserción | 1.274 ms |  |
| ordenamiento | n=200 inverso: mergesort | 0.187 ms |  |
| ordenamiento | n=200 inverso: burbuja (descartada) | 1.728 ms |  |
| ordenamiento | n=200 inverso: AUTOMÁTICO -> merge | 0.226 ms | 1.21x del mejor de los dos |
| ordenamiento | n=1000 aleatorio: inserción | 17.716 ms |  |
| ordenamiento | n=1000 aleatorio: mergesort | 1.448 ms |  |
| ordenamiento | n=1000 aleatorio: AUTOMÁTICO -> merge | 1.473 ms | 1.02x del mejor de los dos |
| ordenamiento | n=1000 casi ordenado (2%): inserción | 1.506 ms |  |
| ordenamiento | n=1000 casi ordenado (2%): mergesort | 1.313 ms |  |
| ordenamiento | n=1000 casi ordenado (2%): AUTOMÁTICO -> merge | 1.358 ms | 1.03x del mejor de los dos |
| ordenamiento | n=1000 inverso: inserción | 33.714 ms |  |
| ordenamiento | n=1000 inverso: mergesort | 1.098 ms |  |
| ordenamiento | n=1000 inverso: AUTOMÁTICO -> merge | 1.240 ms | 1.13x del mejor de los dos |
| ordenamiento | comparaciones n=50 aleatorio | 0.000 ms | inserción=679, merge=222 -> elige merge si comparar es caro |
| ordenamiento | comparaciones n=50 casi ordenado (2%) | 0.000 ms | inserción=108, merge=161 -> elige insercion si comparar es caro |
| ordenamiento | comparaciones n=200 aleatorio | 0.000 ms | inserción=9920, merge=1267 -> elige merge si comparar es caro |
| ordenamiento | comparaciones n=200 casi ordenado (2%) | 0.000 ms | inserción=877, merge=947 -> elige insercion si comparar es caro |
| guardado | 50 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=14066 B, json=34902 B (2.5x el binario) |
| guardado | 50 salas: guardar binario | 1.836 ms |  |
| guardado | 50 salas: guardar JSON | 1.059 ms |  |
| guardado | 50 salas: cargar todo binario | 0.497 ms |  |
| guardado | 50 salas: cargar todo JSON | 0.732 ms | cargar JSON es 1.5x más lento que cargar binario |
| guardado | 50 salas: cargar UNA sala (binario, con índice) | 0.105 ms | 5x más rápido que cargar todo |
| guardado | 500 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=86510 B, json=231764 B (2.7x el binario) |
| guardado | 500 salas: guardar binario | 4.810 ms |  |
| guardado | 500 salas: guardar JSON | 6.346 ms |  |
| guardado | 500 salas: cargar todo binario | 4.124 ms |  |
| guardado | 500 salas: cargar todo JSON | 3.648 ms | cargar JSON es 1.1x más rápido que cargar binario |
| guardado | 500 salas: cargar UNA sala (binario, con índice) | 0.048 ms | 85x más rápido que cargar todo |
| guardado | 5000 salas: TAMAÑO binario vs JSON | 0.000 ms | binario=738814 B, json=2084958 B (2.8x el binario) |
| guardado | 5000 salas: guardar binario | 39.715 ms |  |
| guardado | 5000 salas: guardar JSON | 54.444 ms |  |
| guardado | 5000 salas: cargar todo binario | 41.789 ms |  |
| guardado | 5000 salas: cargar todo JSON | 36.730 ms | cargar JSON es 1.1x más rápido que cargar binario |
| guardado | 5000 salas: cargar UNA sala (binario, con índice) | 0.052 ms | 796x más rápido que cargar todo |
| ciclo | 100 actores activos, peor de 20 ciclos (200 eventos) | 2.126 ms | 2.13 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| ciclo | 300 actores activos, peor de 20 ciclos (600 eventos) | 5.867 ms | 5.87 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| ciclo | 600 actores activos, peor de 20 ciclos (1200 eventos) | 8.266 ms | 8.27 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| partida | 25 salas, 12 enemigos activos al final, 69 acciones x 3 corridas | 0.441 ms | tiempo típico de una acción: 0.20 ms, peor caso: 0.44 ms (peor de cada corrida: 0.32, 0.55, 0.44 ms; se toma el del medio: 0.44) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| partida | 100 salas, 60 enemigos activos al final, 139 acciones x 3 corridas | 2.783 ms | tiempo típico de una acción: 1.23 ms, peor caso: 2.78 ms (peor de cada corrida: 2.63, 2.78, 3.14 ms; se toma el del medio: 2.78) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| partida | 400 salas, 252 enemigos activos al final, 429 acciones x 3 corridas | 13.078 ms | tiempo típico de una acción: 5.58 ms, peor caso: 13.08 ms (peor de cada corrida: 13.08, 43.16, 12.35 ms; se toma el del medio: 13.08) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| solicitudes | 100 salas, 90 visitadas: contenido | 0.000 ms | con precarga en lotes: 10 solicitudes; una por sala visitada (descartada): 90 solicitudes |
| solicitudes | 100 salas, 90 visitadas: catálogo | 0.000 ms | por lotes: 4 solicitudes; una por ficha (descartada): 7 solicitudes |
| solicitudes | 400 salas, 380 visitadas: contenido | 0.000 ms | con precarga en lotes: 40 solicitudes; una por sala visitada (descartada): 380 solicitudes |
| solicitudes | 400 salas, 380 visitadas: catálogo | 0.000 ms | por lotes: 4 solicitudes; una por ficha (descartada): 7 solicitudes |
| ruta_cazador | R=600, H=1: ciclo con cálculo compartido (elegida) | 0.357 ms | mediana de 120 ciclos, peor 1.595 ms |
| ruta_cazador | R=600, H=1: compartido, búsqueda sola | 250.86 µs/op | 58 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=1: compartido, consultas de costo_de_conexion | 113.85 µs/op | 3979 consultas (1.72 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=1: ciclo con cálculo individual (descartada) | 0.357 ms | mediana de 120 ciclos, peor 2.041 ms |
| ruta_cazador | R=600, H=1: individual, búsqueda sola | 241.08 µs/op | 60 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=1: individual, consultas de costo_de_conexion | 111.81 µs/op | 4105 consultas (1.63 µs cada una) |
| ruta_cazador | R=600, H=1: razón individual/compartido | razón | razón de tiempo 1.00 y de búsquedas 1.03 |
| ruta_cazador | R=600, H=10: ciclo con cálculo compartido (elegida) | 0.535 ms | mediana de 120 ciclos, peor 1.691 ms |
| ruta_cazador | R=600, H=10: compartido, búsqueda sola | 238.14 µs/op | 58 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=10: compartido, consultas de costo_de_conexion | 158.22 µs/op | 5779 consultas (1.64 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=10: ciclo con cálculo individual (descartada) | 2.441 ms | mediana de 120 ciclos, peor 8.543 ms |
| ruta_cazador | R=600, H=10: individual, búsqueda sola | 2445.35 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=10: individual, consultas de costo_de_conexion | 1105.07 µs/op | 40510 consultas (1.64 µs cada una) |
| ruta_cazador | R=600, H=10: razón individual/compartido | razón | razón de tiempo 4.57 y de búsquedas 10.34 |
| ruta_cazador | R=600, H=30: ciclo con cálculo compartido (elegida) | 0.916 ms | mediana de 120 ciclos, peor 2.713 ms |
| ruta_cazador | R=600, H=30: compartido, búsqueda sola | 254.22 µs/op | 58 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=30: compartido, consultas de costo_de_conexion | 262.48 µs/op | 9779 consultas (1.61 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=30: ciclo con cálculo individual (descartada) | 7.722 ms | mediana de 120 ciclos, peor 22.610 ms |
| ruta_cazador | R=600, H=30: individual, búsqueda sola | 7255.16 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=30: individual, consultas de costo_de_conexion | 3280.37 µs/op | 121410 consultas (1.62 µs cada una) |
| ruta_cazador | R=600, H=30: razón individual/compartido | razón | razón de tiempo 8.43 y de búsquedas 31.03 |
| ruta_cazador | R=2400, H=1: ciclo con cálculo compartido (elegida) | 2.382 ms | mediana de 120 ciclos, peor 4.810 ms |
| ruta_cazador | R=2400, H=1: compartido, búsqueda sola | 2308.53 µs/op | 58 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=1: compartido, consultas de costo_de_conexion | 1068.84 µs/op | 39721 consultas (1.61 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=1: ciclo con cálculo individual (descartada) | 2.326 ms | mediana de 120 ciclos, peor 6.737 ms |
| ruta_cazador | R=2400, H=1: individual, búsqueda sola | 2432.38 µs/op | 60 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=1: individual, consultas de costo_de_conexion | 1117.12 µs/op | 40967 consultas (1.64 µs cada una) |
| ruta_cazador | R=2400, H=1: razón individual/compartido | razón | razón de tiempo 0.98 y de búsquedas 1.03 |
| ruta_cazador | R=2400, H=10: ciclo con cálculo compartido (elegida) | 2.449 ms | mediana de 120 ciclos, peor 4.745 ms |
| ruta_cazador | R=2400, H=10: compartido, búsqueda sola | 2377.45 µs/op | 58 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=10: compartido, consultas de costo_de_conexion | 1147.00 µs/op | 41620 consultas (1.65 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=10: ciclo con cálculo individual (descartada) | 23.010 ms | mediana de 120 ciclos, peor 65.226 ms |
| ruta_cazador | R=2400, H=10: individual, búsqueda sola | 25214.52 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=10: individual, consultas de costo_de_conexion | 11543.59 µs/op | 409130 consultas (1.69 µs cada una) |
| ruta_cazador | R=2400, H=10: razón individual/compartido | razón | razón de tiempo 9.40 y de búsquedas 10.34 |
| ruta_cazador | R=2400, H=30: ciclo con cálculo compartido (elegida) | 2.968 ms | mediana de 120 ciclos, peor 6.016 ms |
| ruta_cazador | R=2400, H=30: compartido, búsqueda sola | 2352.09 µs/op | 58 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=30: compartido, consultas de costo_de_conexion | 1230.20 µs/op | 45840 consultas (1.61 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=30: ciclo con cálculo individual (descartada) | 68.940 ms | mediana de 120 ciclos, peor 207.195 ms |
| ruta_cazador | R=2400, H=30: individual, búsqueda sola | 76133.91 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=30: individual, consultas de costo_de_conexion | 34797.79 µs/op | 1227270 consultas (1.70 µs cada una) |
| ruta_cazador | R=2400, H=30: razón individual/compartido | razón | razón de tiempo 23.23 y de búsquedas 31.03 |
| ruta_cazador | mixto 25:11, H=10: ciclo con cálculo compartido (elegida) | 2.954 ms | mediana de 120 ciclos, peor 6.214 ms |
| ruta_cazador | mixto 25:11, H=10: compartido, búsqueda sola | 2627.72 µs/op | 116 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=10: compartido, consultas de costo_de_conexion | 1252.32 µs/op | 45262 consultas (1.66 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | mixto 25:11, H=10: ciclo con cálculo individual (descartada) | 8.726 ms | mediana de 120 ciclos, peor 29.866 ms |
| ruta_cazador | mixto 25:11, H=10: individual, búsqueda sola | 9369.80 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=10: individual, consultas de costo_de_conexion | 4270.07 µs/op | 151096 consultas (1.70 µs cada una) |
| ruta_cazador | mixto 25:11, H=10: razón individual/compartido | razón | razón de tiempo 2.95 y de búsquedas 5.17 |
| ruta_cazador | mixto 25:11, H=30: ciclo con cálculo compartido (elegida) | 3.354 ms | mediana de 120 ciclos, peor 6.626 ms |
| ruta_cazador | mixto 25:11, H=30: compartido, búsqueda sola | 2723.95 µs/op | 116 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=30: compartido, consultas de costo_de_conexion | 1393.71 µs/op | 49328 consultas (1.70 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | mixto 25:11, H=30: ciclo con cálculo individual (descartada) | 27.194 ms | mediana de 120 ciclos, peor 78.126 ms |
| ruta_cazador | mixto 25:11, H=30: individual, búsqueda sola | 27917.80 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=30: individual, consultas de costo_de_conexion | 12755.72 µs/op | 453168 consultas (1.69 µs cada una) |
| ruta_cazador | mixto 25:11, H=30: razón individual/compartido | razón | razón de tiempo 8.11 y de búsquedas 15.52 |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: invalidación selectiva (elegida) | 102.38 µs/op | 1 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 2.626 ms en búsquedas, 0 puertas inestables |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: recalcular siempre (descartada) | 4254.67 µs/op | 140 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 414.207 ms en búsquedas |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: razón recalcular siempre/selectiva | razón | razón de tiempo 41.56 y de búsquedas 140.00 |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: invalidación selectiva (elegida) | 174.80 µs/op | 4 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 10.273 ms en búsquedas, 5 puertas inestables |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: recalcular siempre (descartada) | 4089.97 µs/op | 140 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 398.154 ms en búsquedas |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: razón recalcular siempre/selectiva | razón | razón de tiempo 23.40 y de búsquedas 35.00 |
| ciclo_referencia | cripta-06, 36 cazadores activos al medir, en persecución por ciclo: promedio 4.3 y máximo 6, 100 ciclos x 3 corridas | 3.495 ms | ciclo típico 1.195 ms, peor caso 3.495 ms (peor de cada corrida: 3.295, 3.948, 3.495 ms) -> CUMPLE el límite de 20 ms |