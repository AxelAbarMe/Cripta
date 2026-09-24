from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class VersionCriptaDTO:
    id: str
    version: str

    @staticmethod
    def desde_json(datos):
        return VersionCriptaDTO(
            id=datos["id"],
            version=datos["version"]
        )   

@dataclass(frozen=True, slots=True)
class VersionCatalogoDTO:
    version: str

    @staticmethod
    def desde_json(datos):
        return VersionCatalogoDTO(
            version=datos["version"]
        )   