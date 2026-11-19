# Resultados del benchmark 003 (resolubilidad)

Medición en Windows-11-10.0.26200-SP0 (AMD64) con Python 3.14.6, Equipo B (Intel Core Ultra 7).

Fecha: 2026-11-18. Commit: 6114646.

Cada corrida fue un proceso aparte y las tres terminaron con código de salida 0.

La cripta sintética de esta medición pone la puerta de cada segmento en la primera sala del corredor y su llave en una sala lateral al final, así que el ingenuo necesita una pasada por segmento. La primera versión de la carga ponía la llave antes que la puerta y las cifras de esa versión se reemplazaron.

```powershell
py -m cripta --bench --solo resolubilidad resolubilidad_cota
```

## Mediana de las tres corridas

| Escenario | Incremental (ms) | Ingenuo reiniciado (ms) | Razón ingenuo/incremental |
|---|---|---|---|
| 10 llaves, 200 salas | 0.908 | 3.347 | 3.7x |
| 20 llaves, 400 salas | 1.799 | 10.589 | 6.1x |
| 40 llaves, 800 salas | 3.298 | 44.845 | 13.6x |

La razón es la mediana de las tres razones que imprimió cada corrida.

| Cota | Verificación (ms) | Límite (ms) | Resultado |
|---|---|---|---|
| cripta-06, 300 salas | 1.389 | 200.0 | CUMPLE |

## Salas sacadas de la cola

Se contaron las salas que cada método saca de la cola durante una verificación, con un script temporal fuera del repositorio que no se versiona. El conteo no depende del equipo.

| Escenario | Incremental | Ingenuo, cripta anterior | Ingenuo, cripta nueva | Razón nueva |
|---|---|---|---|---|
| 10 llaves, 200 salas | 200 | 400 | 1299 | 6.5x |
| 20 llaves, 400 salas | 400 | 800 | 4599 | 11.5x |
| 40 llaves, 800 salas | 800 | 2080 | 17199 | 21.5x |

## Corrida 1

```text
--bench  (Python 3.14.6, escala=1.0)

=== RESOLUBILIDAD  (0.19 s) ===
  10 llaves encadenadas, 200 salas: recorrido incremental (elegida): 0.671 ms
  10 llaves encadenadas, 200 salas: recorrido ingenuo reiniciado (descartada): 2.974 ms
      -> recorrido_ingenuo_reiniciado es 4.4x más lento que recorrido_incremental
  20 llaves encadenadas, 400 salas: recorrido incremental (elegida): 1.500 ms
  20 llaves encadenadas, 400 salas: recorrido ingenuo reiniciado (descartada): 10.545 ms
      -> recorrido_ingenuo_reiniciado es 7.0x más lento que recorrido_incremental
  40 llaves encadenadas, 800 salas: recorrido incremental (elegida): 2.896 ms
  40 llaves encadenadas, 800 salas: recorrido ingenuo reiniciado (descartada): 39.103 ms
      -> recorrido_ingenuo_reiniciado es 13.5x más lento que recorrido_incremental

=== RESOLUBILIDAD_COTA  (0.01 s) ===
  verificación cripta-06 (300 salas): 1.260 ms
      -> 1.260 ms (límite 200.0 ms: CUMPLE)

Total: 0.21 s
```

## Corrida 2

```text
--bench  (Python 3.14.6, escala=1.0)

=== RESOLUBILIDAD  (0.23 s) ===
  10 llaves encadenadas, 200 salas: recorrido incremental (elegida): 1.018 ms
  10 llaves encadenadas, 200 salas: recorrido ingenuo reiniciado (descartada): 3.639 ms
      -> recorrido_ingenuo_reiniciado es 3.6x más lento que recorrido_incremental
  20 llaves encadenadas, 400 salas: recorrido incremental (elegida): 1.799 ms
  20 llaves encadenadas, 400 salas: recorrido ingenuo reiniciado (descartada): 10.589 ms
      -> recorrido_ingenuo_reiniciado es 5.9x más lento que recorrido_incremental
  40 llaves encadenadas, 800 salas: recorrido incremental (elegida): 3.298 ms
  40 llaves encadenadas, 800 salas: recorrido ingenuo reiniciado (descartada): 44.845 ms
      -> recorrido_ingenuo_reiniciado es 13.6x más lento que recorrido_incremental

=== RESOLUBILIDAD_COTA  (0.01 s) ===
  verificación cripta-06 (300 salas): 1.389 ms
      -> 1.389 ms (límite 200.0 ms: CUMPLE)

Total: 0.25 s
```

## Corrida 3

```text
--bench  (Python 3.14.6, escala=1.0)

=== RESOLUBILIDAD  (0.32 s) ===
  10 llaves encadenadas, 200 salas: recorrido incremental (elegida): 0.908 ms
  10 llaves encadenadas, 200 salas: recorrido ingenuo reiniciado (descartada): 3.347 ms
      -> recorrido_ingenuo_reiniciado es 3.7x más lento que recorrido_incremental
  20 llaves encadenadas, 400 salas: recorrido incremental (elegida): 2.210 ms
  20 llaves encadenadas, 400 salas: recorrido ingenuo reiniciado (descartada): 13.548 ms
      -> recorrido_ingenuo_reiniciado es 6.1x más lento que recorrido_incremental
  40 llaves encadenadas, 800 salas: recorrido incremental (elegida): 3.950 ms
  40 llaves encadenadas, 800 salas: recorrido ingenuo reiniciado (descartada): 58.808 ms
      -> recorrido_ingenuo_reiniciado es 14.9x más lento que recorrido_incremental

=== RESOLUBILIDAD_COTA  (0.02 s) ===
  verificación cripta-06 (300 salas): 2.100 ms
      -> 2.100 ms (límite 200.0 ms: CUMPLE)

Total: 0.34 s
```
