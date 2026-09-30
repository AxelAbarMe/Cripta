"""Selector automático de algoritmo de ordenamiento (§4.9).

El enunciado pide escoger el algoritmo "de acuerdo con propiedades medibles de
los datos". Aquí se miden dos: el tamaño `n` y el desorden (fracción de pares
adyacentes fuera de orden, una sola pasada O(n)). Los umbrales NO son
arbitrarios: salen de las mediciones de bench/cargas_bench.py (insertion_sort
vs merge_sort de estructuras/ordenamientos.py):

  - n <= 32: inserción gana siempre (menos sobrecarga; merge_sort crea listas
    auxiliares y objetos por cada división recursiva).
  - n > 32: el costo de inserción crece como n * (1 + inversiones/n) y en las
    mediciones inversiones/n ≈ 0.35 * n * desorden; merge_sort cuesta ≈ n log n
    con constante mayor. El cruce observado cae cerca de n * desorden ≈ 30:
    por debajo, inserción (datos casi ordenados: 1-5 % de elementos movidos);
    por encima, merge_sort (aleatorio, inverso, mucho desorden).
  - Comparaciones costosas (el orden se decide con una función lenta): lo que
    importa es el NÚMERO de comparaciones, no la sobrecarga de Python.
    Inserción hace ≈ n + inversiones; merge ≈ n log2 n. Entonces inserción solo
    conviene si 0.35 * n * desorden < log2(n) - 1, y el atajo de n pequeño baja a 8.
"""
import math

from cripta.estructuras.ordenamientos import Ordenamiento

UMBRAL_PEQUENO = 32
UMBRAL_PEQUENO_COSTOSA = 8
PRODUCTO_MAX_INSERCION = 30
FACTOR_INVERSIONES = 0.35


def medir_desorden(lista) -> float:
    """Fracción de pares adyacentes fuera de orden: 0.0 ordenada, ~0.5 aleatoria,
    1.0 en orden inverso. Una sola pasada, O(n)."""
    n = len(lista)
    if n < 2:
        return 0.0
    descensos = 0
    for i in range(n - 1):
        if lista[i + 1] < lista[i]:
            descensos += 1
    return descensos / (n - 1)


def elegir_algoritmo(lista, comparacion_costosa: bool = False) -> str:
    """Devuelve "insercion" o "merge" según las propiedades medidas de `lista`."""
    n = len(lista)
    if n <= (UMBRAL_PEQUENO_COSTOSA if comparacion_costosa else UMBRAL_PEQUENO):
        return "insercion"
    producto = n * medir_desorden(lista)
    if comparacion_costosa:
        limite = (math.log2(n) - 1) / FACTOR_INVERSIONES
    else:
        limite = PRODUCTO_MAX_INSERCION
    return "insercion" if producto <= limite else "merge"


def ordenar_auto(lista, comparacion_costosa: bool = False) -> str:
    """Ordena `lista` in situ con el algoritmo elegido y devuelve su nombre."""
    algoritmo = elegir_algoritmo(lista, comparacion_costosa)
    ordenador = Ordenamiento(lista)
    if algoritmo == "insercion":
        ordenador.insertion_sort()
    else:
        ordenador.merge_sort()
    return algoritmo