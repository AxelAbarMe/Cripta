"""Prueba de la revisión de P2 §5.6 (FR-TER-020), ejecutar_accion congela la memoria viva.
Se ejecuta desde la raíz del proyecto con:  py -m unittest tests.modelo.test_congelar_memoria -v
"""
import gc
import unittest

from cripta.modelo.accion import Accion as A
from tests.cripta_cazadores import armar_partida, grafo


class TestCongelarMemoria(unittest.TestCase):
    def test_ejecutar_accion_deja_objetos_congelados(self):
        """P2 §5.6 y FR-TER-020: tras Partida.ejecutar_accion gc.get_freeze_count() es mayor que 0."""
        gc.unfreeze()
        self.addCleanup(gc.unfreeze)
        partida, _ = armar_partida(grafo([(1, "N", 2, 10)]), [])
        partida.ejecutar_accion(A("mover", "N"))
        self.assertGreater(gc.get_freeze_count(), 0)


if __name__ == "__main__":
    unittest.main()
