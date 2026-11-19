# Resultados del benchmark 003 (resolubilidad)

Medición en Windows-11-10.0.26200-SP0 (AMD64) con Python 3.14.6, Equipo B (Intel Core Ultra 7).

Fecha: 2026-11-18. Commit: d2b340d.

Cada corrida fue un proceso aparte y las tres terminaron con código de salida 0.

```powershell
py -m cripta --bench --solo resolubilidad resolubilidad_cota
```

## Mediana de las tres corridas

| Escenario | Incremental (ms) | Ingenuo reiniciado (ms) | Razón ingenuo/incremental |
|---|---|---|---|
| 10 llaves, 200 salas | 0.728 | 1.146 | 1.6x |
| 20 llaves, 400 salas | 1.394 | 2.271 | 1.7x |
| 40 llaves, 800 salas | 2.886 | 5.743 | 2.0x |

La razón es la mediana de las tres razones que imprimió cada corrida.

| Cota | Verificación (ms) | Límite (ms) | Resultado |
|---|---|---|---|
| cripta-06, 300 salas | 1.289 | 200.0 | CUMPLE |

## Corrida 1

```text
--bench  (Python 3.14.6, escala=1.0)

=== RESOLUBILIDAD  (0.06 s) ===
  10 llaves encadenadas, 200 salas: recorrido incremental (elegida): 0.705 ms
  10 llaves encadenadas, 200 salas: recorrido ingenuo reiniciado (descartada): 1.146 ms
      -> recorrido_ingenuo_reiniciado es 1.6x más lento que recorrido_incremental
  20 llaves encadenadas, 400 salas: recorrido incremental (elegida): 1.338 ms
  20 llaves encadenadas, 400 salas: recorrido ingenuo reiniciado (descartada): 2.271 ms
      -> recorrido_ingenuo_reiniciado es 1.7x más lento que recorrido_incremental
  40 llaves encadenadas, 800 salas: recorrido incremental (elegida): 2.949 ms
  40 llaves encadenadas, 800 salas: recorrido ingenuo reiniciado (descartada): 6.026 ms
      -> recorrido_ingenuo_reiniciado es 2.0x más lento que recorrido_incremental

=== RESOLUBILIDAD_COTA  (0.01 s) ===
  verificación cripta-06 (300 salas): 1.164 ms
      -> 1.164 ms (límite 200.0 ms: CUMPLE)

Total: 0.08 s
```

## Corrida 2

```text
--bench  (Python 3.14.6, escala=1.0)

=== RESOLUBILIDAD  (0.06 s) ===
  10 llaves encadenadas, 200 salas: recorrido incremental (elegida): 0.728 ms
  10 llaves encadenadas, 200 salas: recorrido ingenuo reiniciado (descartada): 1.143 ms
      -> recorrido_ingenuo_reiniciado es 1.6x más lento que recorrido_incremental
  20 llaves encadenadas, 400 salas: recorrido incremental (elegida): 1.544 ms
  20 llaves encadenadas, 400 salas: recorrido ingenuo reiniciado (descartada): 2.261 ms
      -> recorrido_ingenuo_reiniciado es 1.5x más lento que recorrido_incremental
  40 llaves encadenadas, 800 salas: recorrido incremental (elegida): 2.876 ms
  40 llaves encadenadas, 800 salas: recorrido ingenuo reiniciado (descartada): 5.743 ms
      -> recorrido_ingenuo_reiniciado es 2.0x más lento que recorrido_incremental

=== RESOLUBILIDAD_COTA  (0.01 s) ===
  verificación cripta-06 (300 salas): 1.364 ms
      -> 1.364 ms (límite 200.0 ms: CUMPLE)

Total: 0.07 s
```

## Corrida 3

```text
--bench  (Python 3.14.6, escala=1.0)

=== RESOLUBILIDAD  (0.06 s) ===
  10 llaves encadenadas, 200 salas: recorrido incremental (elegida): 0.743 ms
  10 llaves encadenadas, 200 salas: recorrido ingenuo reiniciado (descartada): 1.157 ms
      -> recorrido_ingenuo_reiniciado es 1.6x más lento que recorrido_incremental
  20 llaves encadenadas, 400 salas: recorrido incremental (elegida): 1.394 ms
  20 llaves encadenadas, 400 salas: recorrido ingenuo reiniciado (descartada): 2.306 ms
      -> recorrido_ingenuo_reiniciado es 1.7x más lento que recorrido_incremental
  40 llaves encadenadas, 800 salas: recorrido incremental (elegida): 2.886 ms
  40 llaves encadenadas, 800 salas: recorrido ingenuo reiniciado (descartada): 5.447 ms
      -> recorrido_ingenuo_reiniciado es 1.9x más lento que recorrido_incremental

=== RESOLUBILIDAD_COTA  (0.01 s) ===
  verificación cripta-06 (300 salas): 1.289 ms
      -> 1.289 ms (límite 200.0 ms: CUMPLE)

Total: 0.07 s
```
