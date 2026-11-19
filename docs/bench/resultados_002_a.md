# Resultados de niebla_rutas, corrida A

Comando: `py -m cripta --bench --solo niebla_rutas --escala 1`. Fecha: 2026-11-18. Salida completa tal como la imprimió `--bench`:

```text
--bench  (Python 3.14.7, escala=1.0)

=== NIEBLA_RUTAS  (1.22 s) ===
  ruta de producción, 12 consultas con ruta: 3.100 ms
      -> mediana por cálculo 3.100 ms, máximo por cálculo 4.834 ms. CUMPLE el límite de 5 ms. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  selección lineal manual, mismas consultas: 5.013 ms
      -> mediana por cálculo 5.013 ms, máximo por cálculo 7.142 ms. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  costos guardados frente a costo_de_conexion: 3.205 ms
      -> costos guardados: mediana 3.205 ms y máximo 4.503 ms. Consulta al mapa: mediana 4.287 ms y máximo 5.398 ms. Equivalencia con ruta real: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=10: 0.030 ms
      -> incremental: mediana 0.030 ms y máximo 0.053 ms. Pasada ingenua: mediana 0.357 ms y máximo 0.372 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=50: 0.028 ms
      -> incremental: mediana 0.028 ms y máximo 0.051 ms. Pasada ingenua: mediana 0.359 ms y máximo 0.453 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=200: 0.015 ms
      -> incremental: mediana 0.015 ms y máximo 0.081 ms. Pasada ingenua: mediana 0.363 ms y máximo 0.645 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  reversión por inversas frente a copia completa: 0.800 ms totales, 1.96 µs/op (409 ops)
      -> registrar y revertir por inversas: mediana 0.800 ms y máximo 0.878 ms. Copiar y restaurar: mediana 1.178 ms y máximo 1.270 ms. inversas=409. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7

Total: 1.22 s
```
