# Contrato de Interfaces y Reporte: Verificación de Resolubilidad

**Rama**: `003-resolubilidad` | **Fecha**: 2026-11-11 | **Especificación**: [spec.md](../spec.md)

Este documento define formalmente los contratos externos e internos para la capacidad de Verificación de Resolubilidad, abarcando interfaces de Python, contratos de línea de comandos (CLI) y el formato estructurado del reporte de diagnóstico.

---

## 1. Contratos de Línea de Comandos (CLI)

### 1.1 Invocación con `--verificar <cripta>` (FR-RES-016, SC-005)
- **Sintaxis**:
  ```powershell
  python -m cripta [--offline] --verificar <id_cripta>
  ```
- **Comportamiento**:
  - Descarga u obtiene del almacenamiento local los datos generales de la cripta, todas las páginas del esqueleto y la consulta `/llaves`.
  - Ejecuta la verificación de resolubilidad de dominio.
  - Imprime el reporte formateado exclusivamente por `sys.stdout`.
  - **No instancia componentes de vista ni controlador interactivo** (cumplimiento del Principio III de la Constitución).
  - **Códigos de salida**:
    - `0`: Verificación completada con éxito (sea la cripta resoluble o no resoluble).
    - `1`: Error de datos inválidos en el esqueleto (`CriptaDatosInvalidosError`, por ejemplo costos contradictorios).
    - `2`: Error externo de infraestructura (`CriptaLimiteError` por presupuesto agotado, `ApiError` de red, o archivo dañado irrecuperable).

---

### 1.2 Inicio de Partida Regular y Opción `--forzar` (FR-RES-013, FR-RES-014, FR-RES-015)
- **Sintaxis**:
  ```powershell
  python -m cripta [--offline] [--forzar]
  ```
- **Comportamiento al Elegir una Cripta**:
  - Se ejecuta la verificación de resolubilidad automáticamente.
  - El reporte resultante se presenta al usuario a través de la interfaz de usuario (`VistaConsola.mostrar_reporte_resolubilidad()`).
  - **Si la cripta es RESOLUBLE**: La partida arranca normalmente ingresando al bucle interactivo de simulación.
  - **Si la cripta es NO RESOLUBLE**:
    - **Sin `--forzar`**: Se muestra el reporte indicando que la cripta no puede ganarse, se cancela el inicio del juego y se retorna al menú principal sin entrar a la simulación.
    - **Con `--forzar`**: Se muestra el reporte con una advertencia visible de inicio forzado y se procede a iniciar la partida normalmente.

---

### 1.3 Invocación de Medición en `--bench` (FR-RES-020, SC-007)
- **Sintaxis**:
  ```powershell
  python -m cripta --bench --solo resolubilidad
  ```
- **Salida esperada**:
  - Ejecución de la carga sintética determinista basada en `SEMILLA_BENCH`.
  - Reporte comparativo de tiempo: `recorrido_ingenuo_reiniciado es X.Xx más lento que recorrido_incremental`.

---

## 2. Contratos de Interfaces en Python (Código Fuente)

### 2.1 Módulo de Dominio: `VerificadorResolubilidad` (`cripta/modelo/resolubilidad.py`)

Clase pura de dominio, sin importaciones de red, disco ni vista.

```python
class VerificadorResolubilidad:
    """Ejecuta el análisis de resolubilidad y diagnóstico causal sobre el grafo de la cripta."""

    def __init__(self, mapa: CriptaMapa, sala_inicial: int, sala_salida: int,
                 llave_salida: str, llaves_ubicaciones: tuple[LlaveUbicacionDTO, ...]):
        ...

    def verificar(self) -> ResultadoResolubilidad:
        """Ejecuta el recorrido incremental único en O(V + E + K log K) y retorna el resultado."""
        ...

    def verificar_ingenuo_reiniciado(self) -> ResultadoResolubilidad:
        """Alternativa descartada para --bench: reinicia BFS completo por cada llave descubierta."""
        ...
```

---

### 2.2 Módulo de Servicios: `ServicioResolubilidad` (`cripta/servicios/servicio_resolubilidad.py`)

Orquestador de infraestructura, presupuesto y dominio.

```python
class ServicioResolubilidad:
    """Coordina la obtención de datos, gestión de caché, presupuesto y verificación."""

    def __init__(self, cliente: ClienteCripta, contador: ContadorSolicitudes,
                 cache_disco: CacheDisco | None = None):
        ...

    def verificar(self, id_cripta: str) -> ResultadoResolubilidad:
        """Descarga/lee esqueleto y llaves, arma CriptaMapa, verifica y retorna el diagnóstico."""
        ...
```

---

### 2.3 Contrato de Presentación: `VistaBase` (`cripta/vista/vista_base.py`)

Extensión del contrato abstracto de la vista para presentar el reporte.

```python
class VistaBase(ABC):
    ...
    @abstractmethod
    def mostrar_reporte_resolubilidad(self, resultado: ResultadoResolubilidad, forzada: bool = False) -> None:
        """Presenta en pantalla el reporte de resolubilidad al iniciar una partida interactiva."""
        ...
```

---

## 3. Esquema y Formato del Reporte de Diagnóstico

### 3.1 Cripta Resoluble
```text
=================================================================================
REPORTE DE RESOLUBILIDAD: Cripta del Olvido (cripta-02)
Estado: RESOLUBLE
=================================================================================
La cripta es completable. Es posible obtener la llave de salida ('itm_llave_oro')
y acceder a la sala de salida (sala 20) a traves de una puerta que la requiere.

Secuencia causal de obtencion de llaves:
  1. itm_llave_bronce (obtenible en sala 3)
  2. itm_llave_plata  (obtenible en sala 8, portada por mst_guardian_01)
  3. itm_llave_oro    (obtenible en sala 14)
=================================================================================
```

---

### 3.2 Cripta No Resoluble con Bloqueo y Ciclo de Dependencia
```text
=================================================================================
REPORTE DE RESOLUBILIDAD: Cripta Imposible (cripta-sintetica-01)
Estado: NO RESOLUBLE
=================================================================================
ADVERTENCIA: La cripta no puede completarse bajo las reglas del juego.
Motivo: No es posible alcanzar la llave de salida ('itm_llave_salida') ni acceder
        a la sala de salida (sala 10).

Llaves no obtenibles (3):
  - itm_llave_azul   (sala 4)
  - itm_llave_roja   (sala 7, portada por ent_errante_01)
  - itm_llave_salida (sala 10)

Frontera bloqueada (2 puertas):
  - Sala 2 -> E -> Sala 4 (requiere 'itm_llave_roja')
  - Sala 5 -> N -> Sala 6 (requiere 'itm_llave_azul')

Dependencias circulares detectadas (1 ciclo representativo):
  - Ciclo 1: itm_llave_azul -> itm_llave_roja -> itm_llave_azul
    (La llave 'itm_llave_azul' requiere franquear la puerta de 'itm_llave_roja',
     pero 'itm_llave_roja' reside tras la puerta de 'itm_llave_azul').
=================================================================================
```
