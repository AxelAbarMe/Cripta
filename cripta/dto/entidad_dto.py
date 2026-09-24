from ctypes import Union

from cripta.dto.antidoto_dto import AntidotoDTO
from cripta.dto.antorcha_dto import AntorchaDTO
from cripta.dto.arma_dto import ArmaDTO
from cripta.dto.armadura_dto import ArmaduraDTO
from cripta.dto.enemigo_dto import EnemigoDTO
from cripta.dto.llave_dto import LlaveDTO
from cripta.dto.pergamino_dto import PergaminoDTO
from cripta.dto.pocion_dto import PocionDTO
from cripta.dto.trampa_dto import TrampaDTO

EntidadCatalogoDTO = Union[
    EnemigoDTO, ArmaDTO, ArmaduraDTO, PocionDTO, AntidotoDTO, LlaveDTO, AntorchaDTO, PergaminoDTO, TrampaDTO,
]

@staticmethod
def entidad_desde_json(datos):
    if datos["clase"] == "enemigo":
        return EnemigoDTO.desde_json(datos)
    if datos["clase"] == "arma":
        return ArmaDTO.desde_json(datos)
    if datos["clase"] == "armadura":
        return ArmaduraDTO.desde_json(datos)
    if datos["clase"] == "pocion":
        return PocionDTO.desde_json(datos)
    if datos["clase"] == "antidoto":
        return AntidotoDTO.desde_json(datos)
    if datos["clase"] == "llave":
        return LlaveDTO.desde_json(datos)
    if datos["clase"] == "antorcha":
        return AntorchaDTO.desde_json(datos)
    if datos["clase"] == "pergamino":
        return PergaminoDTO.desde_json(datos)
    if datos["clase"] == "trampa":
        return TrampaDTO.desde_json(datos)
    raise ValueError(f"Clase desconocida: {datos['clase']}")