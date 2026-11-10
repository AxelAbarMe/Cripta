# Guía Rápida de Validación (Quickstart): Terreno y Cazador

**Rama**: `001-terreno-cazador` | **Fecha**: 2026-11-09 | **Especificación**: [spec.md](spec.md)

Esta guía describe los escenarios ejecutables paso a paso para validar de extremo a extremo que la capacidad de Terreno y Cazador funciona correctamente, cumple con la Constitución y satisface todos los requisitos funcionales.

---

## 1. Requisitos Previos

- Python 3.11+ instalado y activo en el entorno virtual (`.venv`).
- Repositorio limpio y dependencias instaladas:
  ```powershell
  .venv\Scripts\activate
  py -m pip install -r requirements.txt
  ```
- Verificación de línea base de la Parte I:
  ```powershell
  py -m unittest discover -s tests -t .
  ```
  *Resultado esperado*: 222 pruebas terminadas en `OK`.

---

## 2. Escenarios de Validación

### Escenario 1: Regeneración de Fixtures y Validación del Contrato de Datos (Costo, Rango y Llaves)
**Objetivo**: Regenerar fixtures incluyendo los nuevos campos y verificar que los DTOs y adaptadores leen correctamente el campo `costo` en salidas, el campo `rango` en cazadores, y el endpoint `/llaves` en modo offline (FR-TER-001, FR-TER-008, FR-TER-018).

**Comandos**:
```powershell
# 1. Regenerar fixtures con costo, rango y llaves
py -m scripts.generar_fixtures

# 2. Ejecutar pruebas unitarias de DTOs e infraestructura (archivos de prueba Nuevos)
py -m unittest tests.dto.test_salida_dto
py -m unittest tests.dto.test_enemigo_dto
py -m unittest tests.dto.test_llave_ubicacion_dto
py -m unittest tests.infraestructura.test_cliente_offline_llaves
```
**Resultado Esperado**:
- Fixtures actualizados en `fixtures/` con salidas ponderadas, fichas con rango y `llaves.json`.
- Salidas sin costo asignan `100`; salidas con costo conservan su valor entero $\ge 1$.
- Fichas de cazador sin rango o con rango $\le 0$ lanzan `CriptaDatosInvalidosError` (o `CriptaApiError`) indicando el ID de la ficha en el mensaje de error.
- `obtener_llaves()` retorna las tuplas con `(id, sala, enemigo)` correctamente.

---

### Escenario 2: Movimiento de Actores sobre Terreno con Costo
**Objetivo**: Confirmar que el intervalo de movimiento escala según la fórmula $\max(1, \text{costo} \cdot 100 // \text{velocidad})$, que el costo es simétrico y que las acciones sin movimiento conservan costo 100 (FR-TER-001 a FR-TER-006).

**Comandos**:
```powershell
# Archivo de prueba Nuevo
py -m unittest tests.aceptacion.test_terreno_costos
```
**Resultado Esperado**:
- Movimiento sobre salida de costo 250 con velocidad 100 produce intervalo 250 (tanto en ida como en vuelta).
- Movimiento sobre salida de costo 1 con velocidad 200 produce intervalo $\ge 1$ (nunca 0).
- Cambio de velocidad en tránsito escala el tiempo restante según P1 §2.3.
- Esperar y atacar conservan costo 100 sin importar las salidas adyacentes.

---

### Escenario 3: Persecución del Cazador y Desempate Determinista
**Objetivo**: Validar que el cazador avanza por la ruta de menor costo acumulado (aunque tenga más salas), ataca si comparte sala, espera si $d > \text{rango}$ o no hay ruta, y desempata hacia la vecina con menor ID (FR-TER-009 a FR-TER-014).

**Comandos**:
```powershell
# Archivo de prueba Nuevo
py -m unittest tests.aceptacion.test_cazador_persecucion
```
**Resultado Esperado**:
- Entre ruta directa de 1 sala con costo 300 vs ruta de 3 salas con costo acumulado 150, elige la de 150.
- Ante dos salidas con costo mínimo idéntico, elige la vecina con menor ID.
- Si $d > \text{rango}$, espera con costo 100.
- Si una puerta se cierra automáticamente en el camino, su decisión en el siguiente turno equivale a calcular desde cero.

---

### Escenario 4: Auditoría de Prohibiciones y Reglas del Curso
**Objetivo**: Asegurar que no se hayan introducido importaciones ni estructuras prohibidas (`heapq`, `bisect`, `collections`, `networkx`, `set`, `dict` como índice).

**Comando**:
```powershell
# Script auditor propuesto en CONTEXTO_CRIPTA2.md (Nuevo)
py -m scripts.revisar_prohibidos
```
**Resultado Esperado**: Código de salida `0` sin ningún error de importación prohibida.

---

### Escenario 5: Rendimiento con `--bench` (Cálculo Compartido e Invalidación)
**Objetivo**: Medir empíricamente el tiempo del ciclo de eventos con decenas de cazadores activos (< 20 ms) y contrastar el cálculo compartido vs individual y la reutilización con invalidación vs recalcular siempre (FR-TER-020).

**Comandos**:
```powershell
py -m cripta --bench --solo ruta_cazador
py -m cripta --bench --solo invalidacion
py -m cripta --bench --solo ciclo agenda
```
**Resultado Esperado**:
- `ruta_cazador`: confirmar la hipótesis de que el cálculo compartido mantiene el ciclo holgadamente por debajo de 20 ms con 30 cazadores, mientras que el cálculo individual escala linealmente con el número de cazadores.
- `invalidacion`: con puertas estables, reutilizar la tabla produce 0 búsquedas Dijkstra; con puertas inestables, el sobrecosto de invalidación es marginal.
- `ciclo`: el ciclo de eventos permanece $< 20$ ms en la cripta de referencia.

---

### Escenario 6: Reproducción de Partidas Existentes (--replay)
**Objetivo**: Garantizar compatibilidad hacia atrás con la Parte I (Principio VIII).

**Comando**:
```powershell
py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log
```
**Resultado Esperado**: Termina con código de salida `0`.
