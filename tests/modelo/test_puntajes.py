"""Pruebas del orden de la tabla de puntajes (ranking por cripta y puntajes globales)."""
import unittest

from cripta.modelo.puntajes import Puntaje, TablaPuntajes


def puntaje(nombre, victoria, tiempo, enemigos=0, cripta="c1", version="v1"):
    return Puntaje(nombre, cripta, version, 10, enemigos, tiempo, victoria)


def tabla_con(*puntajes):
    tabla = TablaPuntajes()
    for p in puntajes:
        tabla.agregar(p)
    return tabla


def nombres(puntajes):
    return [p.nombre_jugador for p in puntajes]


class PruebaOrdenDePuntajes(unittest.TestCase):
    def test_las_victorias_van_primero_de_menor_a_mayor_tiempo(self):
        tabla = tabla_con(puntaje("D", False, 50, 9), puntaje("V2", True, 900), puntaje("V1", True, 300))
        self.assertEqual(nombres(tabla.ranking("c1", "v1")), ["V1", "V2", "D"])

    def test_las_derrotas_se_ordenan_por_mas_enemigos_derrotados(self):
        tabla = tabla_con(puntaje("A", False, 500, 1), puntaje("B", False, 100, 4), puntaje("C", False, 300, 2))
        self.assertEqual(nombres(tabla.ranking("c1", "v1")), ["B", "C", "A"])

    def test_en_un_empate_de_enemigos_gana_mas_tiempo_vivo(self):
        tabla = tabla_con(puntaje("Corta", False, 100, 3), puntaje("Larga", False, 700, 3))
        self.assertEqual(nombres(tabla.ranking("c1", "v1")), ["Larga", "Corta"])

    def test_un_empate_total_conserva_el_orden_de_registro(self):
        tabla = tabla_con(puntaje("Primero", False, 100, 3), puntaje("Segundo", False, 100, 3))
        self.assertEqual(nombres(tabla.ranking("c1", "v1")), ["Primero", "Segundo"])

    def test_el_ranking_filtra_por_cripta_y_version(self):
        tabla = tabla_con(
            puntaje("Esta", True, 100),
            puntaje("OtraVersion", True, 10, version="v2"),
            puntaje("OtraCripta", True, 10, cripta="c2"),
        )
        self.assertEqual(nombres(tabla.ranking("c1", "v1")), ["Esta"])
        self.assertEqual(nombres(tabla.globales()), ["OtraVersion", "OtraCripta", "Esta"])

    def test_ordenar_no_altera_el_orden_de_registro(self):
        tabla = tabla_con(puntaje("D", False, 50, 9), puntaje("V", True, 300))
        tabla.ranking("c1", "v1")
        tabla.globales()
        self.assertEqual(nombres(tabla.registros()), ["D", "V"])

    def test_una_tabla_vacia_da_un_ranking_vacio(self):
        self.assertEqual(TablaPuntajes().ranking("c1", "v1"), ())
        self.assertEqual(TablaPuntajes().globales(), ())

    def test_con_mas_filas_que_el_umbral_del_selector_el_orden_es_el_mismo(self):
        filas = []
        for i in range(160):
            victoria = i % 3 == 0
            filas.append(puntaje(f"j{i}", victoria, (i * 37) % 101, (i * 7) % 13))
        resultado = tabla_con(*filas).globales()
        # Referencia hecha a mano (inserción estable), sin usar sorted ni list.sort
        esperado = []
        for p in filas:
            clave = (0, p.tiempo_final, 0) if p.victoria else (1, -p.enemigos_derrotados, -p.tiempo_final)
            posicion = len(esperado)
            while posicion > 0 and esperado[posicion - 1][0] > clave:
                posicion -= 1
            esperado.insert(posicion, (clave, p))
        self.assertEqual(list(resultado), [p for _clave, p in esperado])


if __name__ == "__main__":
    unittest.main()