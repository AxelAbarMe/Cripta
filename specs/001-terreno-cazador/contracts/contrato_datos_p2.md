# Contrato de Interfaces y Datos: Terreno, Cazador y Llaves

**Rama**: `001-terreno-cazador` | **Fecha**: 2026-11-09 | **Especificación**: [spec.md](../spec.md)

Este documento define formalmente los contratos externos e internos para la Parte II introducidos en esta funcionalidad.

---

## 1. Contratos Externos (API REST v1.1.0)

### 1.1 `GET /criptas/{id}/llaves`
- **Propósito**: Obtener la ubicación inicial de las llaves de una cripta para verificación y juego.
- **Cabeceras obligatorias**:
  - `X-Cripta-Client-Id`: UUID v4 generado una vez por ejecución.
- **Presupuesto de Red**: Cada solicitud HTTP cuenta como una en `presupuesto_solicitudes`, reintentos por 429 incluidos (cada reintento es otra solicitud). Sin reintentos, la consulta usa exactamente una.
- **Respuestas**:
  - `200 OK`:
    ```json
    {
      "llaves": [
        {
          "id": "itm_llave_bronce",
          "sala": 2,
          "enemigo": null
        },
        {
          "id": "itm_llave_plata",
          "sala": 5,
          "enemigo": "mst_guardian_01"
        }
      ]
    }
    ```
  - `404 Not Found`: Si la cripta no existe.
  - `429 Too Many Requests`: `{"error": "...", "reintentar_en": n}`. Debe esperarse y reintentarse respetando presupuesto.
- **Esquema formal**: Definido en [contrato_servicio_llaves.json](contrato_servicio_llaves.json).

---

### 1.2 Extensión de Salidas en `GET /criptas/{id}/salas?pagina=n`
- Las salidas pueden incluir opcionalmente el campo `costo`:
  ```json
  {
    "N": {
      "sala": 2,
      "costo": 250
    },
    "E": {
      "sala": 3,
      "cerrada": true,
      "llave": "itm_llave_bronce",
      "costo": 50
    }
  }
  ```
- **Regla**: Si está presente, `costo` debe ser un entero $\ge 1$. El costo de una conexión es el declarado en cualquiera de sus dos lados; si ningún lado lo declara (ausente o `null`), vale `100`. Si los dos lados declaran costos distintos, el dato es inválido.

---

### 1.3 Extensión de Fichas de Catálogo en `GET /catalogo`
- Ficha de cazador:
  ```json
  {
    "id": "mst_cazador_cripta",
    "nombre": "Cazador de las sombras",
    "clase": "enemigo",
    "vida_max": 40,
    "ataque": 12,
    "defensa": 4,
    "velocidad": 120,
    "comportamiento": "cazador",
    "rango": 300,
    "suelta": ["itm_pocion_vida"]
  }
  ```
- **Regla**: Si `comportamiento == "cazador"`, `rango` debe ser un entero $\ge 1$. Si el rango es nulo, falta, no es entero o es menor que 1, no se lanza excepción: `rango` queda en `None` y el cazador se trata de forma pasiva (ataca si comparte sala con el jugador y si no espera con costo 100; nunca persigue), con un aviso a la bitácora de mensajes al activarse (FR-TER-008).

---

## 2. Contratos Internos (Código Python)

### 2.1 Interfaz `ClienteCripta` (`cripta/infraestructura/puertos.py`)

```python
class ClienteCripta(Protocol):
    def obtener_general(self, id_cripta: str) -> GeneralDTO: ...
    def obtener_version(self, id_cripta: str) -> str: ...
    def obtener_pagina_esqueleto(self, id_cripta: str, pagina: int) -> PaginaEsqueletoDTO: ...
    def obtener_contenido_lote(self, id_cripta: str, salas_ids: tuple[int, ...]) -> ContenidoLoteDTO: ...
    def obtener_catalogo_lote(self, ids: tuple[str, ...]) -> CatalogoDTO: ...
    def obtener_version_catalogo(self) -> str: ...
    def obtener_lista_criptas(self) -> tuple[CriptaResumenDTO, ...]: ...
    # Método nuevo de la Parte II:
    def obtener_llaves(self, id_cripta: str) -> tuple[LlaveUbicacionDTO, ...]: ...
```

---

### 2.2 DTOs (`cripta/dto/` — `llave_ubicacion_dto.py` es Nuevo)

```python
@dataclass(frozen=True, slots=True)
class SalidaDTO:
    sala_destino: int
    cerrada: bool = False
    llave: str | None = None
    cierre_automatico: int | None = None
    costo: int | None = None  # None si este lado no declara costo. CriptaMapa resuelve el de la conexión (100 si ningún lado lo declara)

@dataclass(frozen=True, slots=True)
class LlaveUbicacionDTO:
    id: str
    sala: int
    enemigo: str | None = None

    @classmethod
    def desde_json(cls, datos: dict) -> "LlaveUbicacionDTO":
        # Ante datos externos inválidos lanza ValueError con el dato afectado. El cliente lo convierte.
        if "id" not in datos or "sala" not in datos:
            raise ValueError(f"ubicación de llave sin 'id' o 'sala': {datos}")
        if not str(datos["id"]) or not isinstance(datos["sala"], int) or datos["sala"] < 1:
            raise ValueError(f"ubicación de llave con 'id' vacío o 'sala' menor que 1: {datos}")
        return cls(
            id=str(datos["id"]),
            sala=datos["sala"],
            enemigo=str(datos["enemigo"]) if datos.get("enemigo") else None
        )
```

---

### 2.3 Contrato de `BuscadorRutas` (`cripta/modelo/buscador_rutas.py` — Nuevo)

```python
class BuscadorRutas:
    def invalidar(self) -> None:
        """Marca la caché de distancias como inválida."""
        ...

    def calcular_o_reutilizar(self, mapa: CriptaMapa, sala_jugador_id: int, rango_max: int) -> None:
        """Calcula Dijkstra desde sala_jugador_id si está invalidado o si rango_max excede el previo."""
        ...

    def distancia(self, sala_id: int) -> int | None:
        """Devuelve la distancia mínima hacia la sala del jugador, o None si inalcanzable dentro del rango."""
        ...

    def decidir_paso(self, cazador: Enemigo, sala_jugador_id: int, mapa: CriptaMapa) -> tuple[str, str | None, int]:
        """Devuelve (accion, direccion, costo) con accion 'mover' o 'esperar'. El ataque se decide antes, en _decidir_cazador."""
        ...
```
