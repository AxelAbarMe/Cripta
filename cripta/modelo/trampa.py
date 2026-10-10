"""Trampa: estado de una trampa colocada en una sala."""
from cripta.modelo.reversible import Reversible

class Trampa(Reversible):
    def __init__(self, instancia_id: str, tipo_catalogo: str):
        self.instancia_id = instancia_id
        self.tipo_catalogo = tipo_catalogo
        self.armada = True  # toda trampa empieza armada al cargar el contenido

    def desarmar(self) -> None:
        self.armada = False

    def rearmar(self) -> None:
        self.armada = True

    def __repr__(self) -> str:
        estado = "armada" if self.armada else "desarmada"
        return f"Trampa({self.instancia_id}, {self.tipo_catalogo}, {estado})"
