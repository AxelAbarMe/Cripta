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
- En el DTO, una salida sin costo queda con `costo` en `None` y una con costo conserva su valor entero $\ge 1$. En el mapa, una conexión sin costo en ningún lado vale `100` y una con costo en un solo lado usa ese valor en ambos sentidos.
- Fichas de cazador con rango nulo, ausente, no entero o menor que 1 se cargan sin error, con `rango` en `None`; en el juego ese cazador es pasivo y al activarse aparece un aviso con el ID de la ficha (FR-TER-008).
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
- Un cambio de velocidad después de un movimiento escala el tiempo restante hasta la próxima acción según P1 §2.3.
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
**Objetivo**: Comprobar que no se introdujeron importaciones prohibidas (`heapq`, `bisect`, `collections`, `networkx`) en el código del modelo ni en las estructuras (Principio I).

**Comando**:
```powershell
Select-String -Path (Get-ChildItem cripta -Recurse -Filter *.py).FullName -Pattern "heapq|bisect|collections|networkx|sorted\(|\.sort\("
```
**Resultado Esperado**: Sin importaciones prohibidas. Cada `sorted(` o `.sort(` que aparezca se revisa a mano: solo se permite fuera de los ordenamientos evaluados. El uso de `dict` y `set` como índice o caché se revisa en la revisión del Pull Request, porque una búsqueda de texto no distingue los usos permitidos.

---

### Escenario 5: Rendimiento con `--bench` (Cálculo Compartido e Invalidación)
**Objetivo**: Medir empíricamente el tiempo del ciclo de eventos con decenas de cazadores activos (< 20 ms) y contrastar el cálculo compartido vs individual y la reutilización con invalidación vs recalcular siempre (FR-TER-020).

**Comandos**:
```powershell
py -m cripta --bench --solo ruta_cazador
py -m cripta --bench --solo invalidacion
py -m cripta --bench --solo ciclo
py -m cripta --bench --solo agenda
py -m cripta --bench --solo historial
```
**Resultado Esperado**:
- `ruta_cazador`: hipótesis a confirmar: el cálculo compartido mantiene el ciclo por debajo de 20 ms con 30 cazadores, y el individual crece con el número de cazadores. Incluir un caso de rangos heterogéneos.
- `invalidacion`: hipótesis: con puertas estables, reutilizar la tabla reduce las búsquedas frente a recalcular siempre; con puertas inestables se mide a partir de qué frecuencia de cambios deja de convenir. Se reportan los resultados tal como salgan.
- `ciclo`, `agenda` e `historial`: regresión de la Parte I (sin cazadores). Hipótesis a confirmar: el ciclo sigue por debajo de 20 ms con los costos variables. FR-TER-020 con cazadores se verifica con `ruta_cazador` (`H=30`) mientras no se publique la cripta de referencia.

---

### Escenario 6: Reproducción de Partidas Existentes (--replay)
**Objetivo**: Garantizar compatibilidad hacia atrás con la Parte I (Principio VIII).

**Comando**:
```powershell
py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log
```
**Resultado Esperado**: Termina con código de salida `0`.

**Riesgo**: regenerar fixtures (Escenario 1) puede cambiar la versión de la cripta y volver incompatible este `--replay`. Ejecutar este escenario con las fixtures originales respaldadas antes de regenerar.