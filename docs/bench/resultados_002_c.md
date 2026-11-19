# Resultados de niebla_rutas, corrida C

Comando: `py -m cripta --bench --solo niebla_rutas --escala 1`. Fecha: 2026-11-18. Salida completa tal como la imprimió `--bench`:

```text
--bench  (Python 3.14.7, escala=1.0)

=== NIEBLA_RUTAS  (1.19 s) ===
  ruta de producción, 12 consultas con ruta: 3.095 ms
      -> mediana por cálculo 3.095 ms, máximo por cálculo 4.599 ms. CUMPLE el límite de 5 ms. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  selección lineal manual, mismas consultas: 4.758 ms
      -> mediana por cálculo 4.758 ms, máximo por cálculo 5.284 ms. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  costos guardados frente a costo_de_conexion: 3.062 ms
      -> costos guardados: mediana 3.062 ms y máximo 3.398 ms. Consulta al mapa: mediana 4.194 ms y máximo 7.101 ms. Equivalencia con ruta real: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=10: 0.033 ms
      -> incremental: mediana 0.033 ms y máximo 0.053 ms. Pasada ingenua: mediana 0.360 ms y máximo 0.504 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=50: 0.028 ms
      -> incremental: mediana 0.028 ms y máximo 0.052 ms. Pasada ingenua: mediana 0.362 ms y máximo 0.563 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=200: 0.016 ms
      -> incremental: mediana 0.016 ms y máximo 0.061 ms. Pasada ingenua: mediana 0.368 ms y máximo 0.569 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  reversión por inversas frente a copia completa: 0.870 ms totales, 2.13 µs/op (409 ops)
      -> registrar y revertir por inversas: mediana 0.870 ms y máximo 1.059 ms. Copiar y restaurar: mediana 1.186 ms y máximo 1.197 ms. inversas=409. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7

Total: 1.19 s
```
