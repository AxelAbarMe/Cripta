from dataclasses import dataclass

'''Se define la clase AntidotoDTO, que representa un objeto de tipo Antídoto en el sistema. 
Esta clase es inmutable. Contiene atributos como id, nombre, clase, peso y valor, 
y proporciona un método estático para crear una instancia a partir de un diccionario JSON.
Extraido de GET /catalogo/{catalog_id}

Entidad de catalogo. Es un item que otorga protección contra veneno.
'''
@dataclass(frozen=True, slots=True)
class AntidotoDTO:
    id : str
    nombre : str
    clase : str
    peso : int
    valor : int

    @staticmethod
    def desde_json(datos):
        return AntidotoDTO(
            id=datos["id"],
            nombre=datos["nombre"],
            clase=datos["clase"],
            peso=datos["peso"],
            valor=datos["valor"],
        )