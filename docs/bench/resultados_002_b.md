# Resultados de niebla_rutas, corrida B

Comando: `py -m cripta --bench --solo niebla_rutas --escala 1`. Fecha: 2026-11-18. Salida completa tal como la imprimió `--bench`:

```text
--bench  (Python 3.14.7, escala=1.0)

=== NIEBLA_RUTAS  (1.18 s) ===
  ruta de producción, 12 consultas con ruta: 3.038 ms
      -> mediana por cálculo 3.038 ms, máximo por cálculo 3.799 ms. CUMPLE el límite de 5 ms. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  selección lineal manual, mismas consultas: 4.799 ms
      -> mediana por cálculo 4.799 ms, máximo por cálculo 6.122 ms. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  costos guardados frente a costo_de_conexion: 3.069 ms
      -> costos guardados: mediana 3.069 ms y máximo 3.709 ms. Consulta al mapa: mediana 4.217 ms y máximo 4.906 ms. Equivalencia con ruta real: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=10: 0.032 ms
      -> incremental: mediana 0.032 ms y máximo 0.057 ms. Pasada ingenua: mediana 0.363 ms y máximo 0.417 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=50: 0.029 ms
      -> incremental: mediana 0.029 ms y máximo 0.073 ms. Pasada ingenua: mediana 0.367 ms y máximo 0.571 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  revelación, R=200: 0.016 ms
      -> incremental: mediana 0.016 ms y máximo 0.068 ms. Pasada ingenua: mediana 0.366 ms y máximo 0.577 ms. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7
  reversión por inversas frente a copia completa: 0.793 ms totales, 1.94 µs/op (409 ops)
      -> registrar y revertir por inversas: mediana 0.793 ms y máximo 0.869 ms. Copiar y restaurar: mediana 1.185 ms y máximo 1.190 ms. inversas=409. Equivalencia: True. fixture=cripta-06, salas=300, salidas=760, puertas abiertas=28, pares probados=12, pares con ruta=12, semilla=20261118, Python=3.14.7

Total: 1.18 s
```
