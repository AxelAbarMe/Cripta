| Subsistema | Caso | Tiempo | Nota |
|---|---|---:|---|
| agenda | 100 pendientes: heap (elegida) | 5.79 µs/op |  |
| agenda | 100 pendientes: lista lineal (descartada) | 7.07 µs/op | 1.2x más lenta que el heap |
| agenda | 500 pendientes: heap (elegida) | 5.85 µs/op |  |
| agenda | 500 pendientes: lista lineal (descartada) | 37.67 µs/op | 6.4x más lenta que el heap |
| agenda | 2000 pendientes: heap (elegida) | 9.01 µs/op |  |
| agenda | 2000 pendientes: lista lineal (descartada) | 153.70 µs/op | 17.1x más lenta que el heap |
| agenda | cancelar 1/3 y reprogramar 1/3 (perezoso) | 0.93 µs/op |  |
| historial | registrar acción (6 inversas): operaciones inversas (elegida) | 3.14 µs/op |  |
| historial | registrar acción: copia completa de 200 salas + 60 actores (descartada, prohibida) | 1207.46 µs/op | 384x más lenta y guarda 5 estados enteros |
| historial | deshacer 5 acciones (30 inversas) | 5.58 µs/op |  |
| ciclo | 100 actores activos, peor de 20 ciclos (200 eventos) | 2.058 ms | 2.06 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| ciclo | 300 actores activos, peor de 20 ciclos (600 eventos) | 6.655 ms | 6.65 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| ciclo | 600 actores activos, peor de 20 ciclos (1200 eventos) | 14.199 ms | 14.20 ms  -> CUMPLE el límite de 20 ms (§5.2) |
| partida | 25 salas, 12 enemigos activos al final, 69 acciones x 3 corridas | 2.004 ms | tiempo típico de una acción: 0.44 ms, peor caso: 2.00 ms (peor de cada corrida: 0.97, 2.00, 6.16 ms; se toma el del medio: 2.00) -> CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| partida | 100 salas, 60 enemigos activos al final, 139 acciones x 3 corridas | 31.320 ms | tiempo típico de una acción: 3.00 ms, peor caso: 31.32 ms (peor de cada corrida: 31.32, 11.02, 43.40 ms; se toma el del medio: 31.32) -> NO CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| partida | 400 salas, 252 enemigos activos al final, 429 acciones x 3 corridas | 129.766 ms | tiempo típico de una acción: 8.85 ms, peor caso: 129.77 ms (peor de cada corrida: 101.72, 129.87, 129.77 ms; se toma el del medio: 129.77) -> NO CUMPLE el límite de 20 ms (§5.2, decide la mediana de los peores casos) |
| ruta_cazador | R=600, H=1: ciclo con cálculo compartido (elegida) | 0.442 ms | mediana de 120 ciclos, peor 1.138 ms |
| ruta_cazador | R=600, H=1: compartido, búsqueda sola | 272.43 µs/op | 58 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=1: compartido, consultas de costo_de_conexion | 123.29 µs/op | 3979 consultas (1.86 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=1: ciclo con cálculo individual (descartada) | 0.495 ms | mediana de 120 ciclos, peor 1.737 ms |
| ruta_cazador | R=600, H=1: individual, búsqueda sola | 333.66 µs/op | 60 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=1: individual, consultas de costo_de_conexion | 146.42 µs/op | 4105 consultas (2.14 µs cada una) |
| ruta_cazador | R=600, H=1: razón individual/compartido | razón | razón de tiempo 1.12 y de búsquedas 1.03 |
| ruta_cazador | R=600, H=10: ciclo con cálculo compartido (elegida) | 0.654 ms | mediana de 120 ciclos, peor 133.619 ms |
| ruta_cazador | R=600, H=10: compartido, búsqueda sola | 286.23 µs/op | 58 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=10: compartido, consultas de costo_de_conexion | 184.18 µs/op | 5779 consultas (1.91 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=10: ciclo con cálculo individual (descartada) | 3.356 ms | mediana de 120 ciclos, peor 12.311 ms |
| ruta_cazador | R=600, H=10: individual, búsqueda sola | 3021.23 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=10: individual, consultas de costo_de_conexion | 1336.96 µs/op | 40510 consultas (1.98 µs cada una) |
| ruta_cazador | R=600, H=10: razón individual/compartido | razón | razón de tiempo 5.13 y de búsquedas 10.34 |
| ruta_cazador | R=600, H=30: ciclo con cálculo compartido (elegida) | 1.173 ms | mediana de 120 ciclos, peor 9.519 ms |
| ruta_cazador | R=600, H=30: compartido, búsqueda sola | 276.12 µs/op | 58 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=30: compartido, consultas de costo_de_conexion | 299.20 µs/op | 9779 consultas (1.84 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=600, H=30: ciclo con cálculo individual (descartada) | 9.558 ms | mediana de 120 ciclos, peor 27.543 ms |
| ruta_cazador | R=600, H=30: individual, búsqueda sola | 9125.57 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=600, H=30: individual, consultas de costo_de_conexion | 4043.80 µs/op | 121410 consultas (2.00 µs cada una) |
| ruta_cazador | R=600, H=30: razón individual/compartido | razón | razón de tiempo 8.15 y de búsquedas 31.03 |
| ruta_cazador | R=2400, H=1: ciclo con cálculo compartido (elegida) | 2.946 ms | mediana de 120 ciclos, peor 5.020 ms |
| ruta_cazador | R=2400, H=1: compartido, búsqueda sola | 3143.09 µs/op | 58 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=1: compartido, consultas de costo_de_conexion | 1414.50 µs/op | 39721 consultas (2.14 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=1: ciclo con cálculo individual (descartada) | 3.029 ms | mediana de 120 ciclos, peor 8.173 ms |
| ruta_cazador | R=2400, H=1: individual, búsqueda sola | 3129.97 µs/op | 60 búsquedas para 60 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=1: individual, consultas de costo_de_conexion | 1410.22 µs/op | 40967 consultas (2.07 µs cada una) |
| ruta_cazador | R=2400, H=1: razón individual/compartido | razón | razón de tiempo 1.03 y de búsquedas 1.03 |
| ruta_cazador | R=2400, H=10: ciclo con cálculo compartido (elegida) | 3.547 ms | mediana de 120 ciclos, peor 5.784 ms |
| ruta_cazador | R=2400, H=10: compartido, búsqueda sola | 3045.73 µs/op | 58 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=10: compartido, consultas de costo_de_conexion | 1435.53 µs/op | 41620 consultas (2.07 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=10: ciclo con cálculo individual (descartada) | 30.181 ms | mediana de 120 ciclos, peor 83.632 ms |
| ruta_cazador | R=2400, H=10: individual, búsqueda sola | 33089.03 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=10: individual, consultas de costo_de_conexion | 14961.10 µs/op | 409130 consultas (2.19 µs cada una) |
| ruta_cazador | R=2400, H=10: razón individual/compartido | razón | razón de tiempo 8.51 y de búsquedas 10.34 |
| ruta_cazador | R=2400, H=30: ciclo con cálculo compartido (elegida) | 4.765 ms | mediana de 120 ciclos, peor 8.659 ms |
| ruta_cazador | R=2400, H=30: compartido, búsqueda sola | 4319.90 µs/op | 58 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=30: compartido, consultas de costo_de_conexion | 2264.66 µs/op | 45840 consultas (2.96 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | R=2400, H=30: ciclo con cálculo individual (descartada) | 128.151 ms | mediana de 120 ciclos, peor 331.570 ms |
| ruta_cazador | R=2400, H=30: individual, búsqueda sola | 127704.26 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | R=2400, H=30: individual, consultas de costo_de_conexion | 57802.24 µs/op | 1227270 consultas (2.83 µs cada una) |
| ruta_cazador | R=2400, H=30: razón individual/compartido | razón | razón de tiempo 26.89 y de búsquedas 31.03 |
| ruta_cazador | mixto 25:11, H=10: ciclo con cálculo compartido (elegida) | 5.015 ms | mediana de 120 ciclos, peor 12.325 ms |
| ruta_cazador | mixto 25:11, H=10: compartido, búsqueda sola | 4894.31 µs/op | 116 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=10: compartido, consultas de costo_de_conexion | 2282.99 µs/op | 45262 consultas (3.03 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | mixto 25:11, H=10: ciclo con cálculo individual (descartada) | 15.166 ms | mediana de 120 ciclos, peor 41.905 ms |
| ruta_cazador | mixto 25:11, H=10: individual, búsqueda sola | 17711.72 µs/op | 600 búsquedas para 600 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=10: individual, consultas de costo_de_conexion | 7924.13 µs/op | 151096 consultas (3.15 µs cada una) |
| ruta_cazador | mixto 25:11, H=10: razón individual/compartido | razón | razón de tiempo 3.02 y de búsquedas 5.17 |
| ruta_cazador | mixto 25:11, H=30: ciclo con cálculo compartido (elegida) | 5.777 ms | mediana de 120 ciclos, peor 11.170 ms |
| ruta_cazador | mixto 25:11, H=30: compartido, búsqueda sola | 4086.91 µs/op | 116 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=30: compartido, consultas de costo_de_conexion | 2058.97 µs/op | 49328 consultas (2.50 µs cada una), medidas con envoltura que suma su propio costo |
| ruta_cazador | mixto 25:11, H=30: ciclo con cálculo individual (descartada) | 39.716 ms | mediana de 120 ciclos, peor 133.197 ms |
| ruta_cazador | mixto 25:11, H=30: individual, búsqueda sola | 44157.09 µs/op | 1800 búsquedas para 1800 decisiones, total de la corrida de 60 ciclos, no por ciclo |
| ruta_cazador | mixto 25:11, H=30: individual, consultas de costo_de_conexion | 19845.66 µs/op | 453168 consultas (2.63 µs cada una) |
| ruta_cazador | mixto 25:11, H=30: razón individual/compartido | razón | razón de tiempo 6.87 y de búsquedas 15.52 |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: invalidación selectiva (elegida) | 150.98 µs/op | 1 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 4.200 ms en búsquedas, 0 puertas inestables |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: recalcular siempre (descartada) | 7253.15 µs/op | 140 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 698.959 ms en búsquedas |
| invalidacion | 20 cazadores, 100 ticks, puertas estables: razón recalcular siempre/selectiva | razón | razón de tiempo 48.04 y de búsquedas 140.00 |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: invalidación selectiva (elegida) | 535.27 µs/op | 4 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 33.763 ms en búsquedas, 5 puertas inestables |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: recalcular siempre (descartada) | 6335.84 µs/op | 140 búsquedas para 140 decisiones (total de los 100 ticks, no por ciclo), 618.947 ms en búsquedas |
| invalidacion | 20 cazadores, 100 ticks, 5 puertas con cierre cada 15 ticks: razón recalcular siempre/selectiva | razón | razón de tiempo 11.84 y de búsquedas 35.00 |
| ciclo_referencia | cripta-06, 36 cazadores activos al medir, en persecución por ciclo: promedio 4.3 y máximo 6, 100 ciclos x 3 corridas | 3.133 ms | ciclo típico 1.421 ms, peor caso 3.133 ms (peor de cada corrida: 3.133, 3.103, 19.882 ms) -> CUMPLE el límite de 20 ms |