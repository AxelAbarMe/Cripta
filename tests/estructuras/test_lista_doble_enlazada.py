"""Pruebas de ListaDobleEnlazada: recorrido en ambos sentidos y O(1) por nodo conocido.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.estructuras.test_lista_doble_enlazada -v
"""
import unittest

from cripta.estructuras.lista_doble_enlazada import ListaDobleEnlazada


def adelante(lista):
    valores, nodo = [], lista.head
    while nodo:
        valores.append(nodo.data)
        nodo = nodo.next
    return valores


def atras(lista):
    valores, nodo = [], lista.tail
    while nodo:
        valores.append(nodo.data)
        nodo = nodo.prev
    return valores


def armar(*valores):
    lista = ListaDobleEnlazada()
    nodos = [lista.agregar(v) for v in valores]
    return lista, nodos


class TestListaDobleEnlazada(unittest.TestCase):
    def assertConsistente(self, lista, esperado):
        # Hacia adelante y hacia atrás deben ser la misma secuencia, y len() debe coincidir
        self.assertEqual(adelante(lista), esperado)
        self.assertEqual(atras(lista), esperado[::-1])
        self.assertEqual(len(lista), len(esperado))

    def test_vacia(self):
        lista = ListaDobleEnlazada()
        self.assertConsistente(lista, [])
        self.assertIsNone(lista.head)
        self.assertIsNone(lista.tail)

    def test_agregar_y_agregar_inicio(self):
        lista, _ = armar(2, 3)
        lista.agregar_inicio(1)
        lista.agregar(4)
        self.assertConsistente(lista, [1, 2, 3, 4])

    def test_agregar_inicio_en_lista_vacia_fija_head_y_tail(self):
        lista = ListaDobleEnlazada()
        nodo = lista.agregar_inicio("a")
        self.assertIs(lista.head, nodo)
        self.assertIs(lista.tail, nodo)

    def test_eliminar_por_valor_cabeza_medio_cola_y_ausente(self):
        lista, _ = armar(1, 2, 3, 4)
        lista.eliminar(1)
        self.assertConsistente(lista, [2, 3, 4])
        lista.eliminar(3)
        self.assertConsistente(lista, [2, 4])
        lista.eliminar(4)
        self.assertConsistente(lista, [2])
        lista.eliminar(99)
        self.assertConsistente(lista, [2])
        lista.eliminar(2)
        self.assertConsistente(lista, [])

    def test_eliminar_en_lista_vacia_no_falla(self):
        lista = ListaDobleEnlazada()
        lista.eliminar(1)
        self.assertEqual(len(lista), 0)

    def test_buscar(self):
        lista, _ = armar("a", "b")
        self.assertTrue(lista.buscar("b"))
        self.assertFalse(lista.buscar("z"))

    def test_eliminar_nodo_en_cualquier_posicion(self):
        for posicion in range(5):
            lista, nodos = armar(0, 1, 2, 3, 4)
            lista.eliminar_nodo(nodos[posicion])
            esperado = [v for v in range(5) if v != posicion]
            self.assertConsistente(lista, esperado)

    def test_eliminar_nodo_unico_deja_la_lista_vacia(self):
        lista, nodos = armar("x")
        lista.eliminar_nodo(nodos[0])
        self.assertConsistente(lista, [])
        self.assertIsNone(lista.head)
        self.assertIsNone(lista.tail)

    def test_mover_al_inicio_desde_cada_posicion(self):
        for posicion in range(4):
            lista, nodos = armar("a", "b", "c", "d")
            lista.mover_al_inicio(nodos[posicion])
            valor = "abcd"[posicion]
            resto = [v for v in "abcd" if v != valor]
            self.assertConsistente(lista, [valor] + resto)

    def test_mover_al_inicio_de_la_cabeza_o_del_unico_no_cambia_nada(self):
        lista, nodos = armar("a", "b")
        lista.mover_al_inicio(nodos[0])
        self.assertConsistente(lista, ["a", "b"])
        unica, nodo = armar("z")
        unica.mover_al_inicio(nodo[0])
        self.assertConsistente(unica, ["z"])

    def test_mover_la_cola_actualiza_tail(self):
        lista, nodos = armar(1, 2, 3)
        lista.mover_al_inicio(nodos[2])
        self.assertEqual(lista.tail.data, 2)
        lista.agregar(9)
        self.assertConsistente(lista, [3, 1, 2, 9])

    def test_secuencia_mixta_mantiene_la_consistencia(self):
        lista, nodos = armar(1, 2, 3, 4, 5)
        lista.mover_al_inicio(nodos[3])      # 4 1 2 3 5
        lista.eliminar_nodo(nodos[0])        # 4 2 3 5
        lista.agregar_inicio(0)              # 0 4 2 3 5
        lista.eliminar(3)                    # 0 4 2 5
        self.assertConsistente(lista, [0, 4, 2, 5])


if __name__ == "__main__":
    unittest.main()