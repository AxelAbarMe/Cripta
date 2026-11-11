# Guía de Validación Rápida: Verificación de Resolubilidad (Fase 1)

**Rama**: `003-resolubilidad` | **Fecha**: 2026-11-11 | **Especificación**: [spec.md](spec.md)

Esta guía detalla los comandos y escenarios ejecutables paso a paso para validar la funcionalidad de Verificación de Resolubilidad de punta a punta, asegurando el cumplimiento de todos los requisitos (`FR-RES-001` a `FR-RES-023`), criterios de éxito (`SC-001` a `SC-008`) y escenarios del Apéndice B.

---

## 1. Requisitos Previos

- Python 3.11+ instalado y activo en la terminal.
- Repositorio situado en la raíz del proyecto.
- Fixtures locales disponibles en el directorio `fixtures/`.

---

## 2. Escenarios de Validación

### Escenario 1: Ejecución de la Suite Completa de Pruebas Unitarias
Verifica que las pruebas preexistentes y las nuevas pruebas de resolubilidad pasen en su totalidad.

```powershell
python -m unittest discover -s tests -t .
```
- **Resultado esperado**: Todas las pruebas terminan en `OK` sin errores ni fallos. Las pruebas de resolubilidad en `tests/modelo/test_resolubilidad.py` y `tests/servicios/test_servicio_resolubilidad.py` cubren el 100% de los requisitos citando sus identificadores `FR-RES-NNN`.

---

### Escenario 2: Verificación Independiente por Consola (`--verificar`)
Comprueba la auditoría automatizada sin instanciar la interfaz interactiva (FR-RES-016, SC-005).

#### 2.1 Cripta Resoluble en Modo Offline
```powershell
python -m cripta --offline --verificar cripta-02
```
- **Resultado esperado**: Código de salida `0`. Emite en `sys.stdout` el reporte con `Estado: RESOLUBLE` y la secuencia determinista de llaves obtenibles. No se abre interfaz ni se solicita entrada al usuario.

#### 2.2 Cripta No Resoluble
```powershell
python -m cripta --offline --verificar cripta-no-resoluble
```
- **Resultado esperado**: Código de salida `0`. Emite el reporte con `Estado: NO RESOLUBLE`, detallando llaves inalcanzables, puertas de la frontera bloqueada y ciclos de dependencia encontrados.

---

### Escenario 3: Inicio de Partida Regular y Control con `--forzar`
Valida la compuerta de seguridad al arrancar una partida interactiva (FR-RES-013, FR-RES-014, FR-RES-015).

#### 3.1 Cripta No Resoluble sin `--forzar`
```powershell
python -m cripta --offline
```
- **Acción del usuario**: Elegir una cripta no resoluble desde el menú.
- **Resultado esperado**: La vista presenta el reporte de advertencia indicando que la cripta es imposible de ganar; la partida **no inicia** y el sistema retorna inmediatamente al menú principal sin entrar a la simulación.

#### 3.2 Cripta No Resoluble con `--forzar`
```powershell
python -m cripta --offline --forzar
```
- **Acción del usuario**: Elegir una cripta no resoluble.
- **Resultado esperado**: La vista muestra el reporte de advertencia informando el inicio forzado y arranca la partida normalmente.

---

### Escenario 4: Medición Comparativa en `--bench` (Incremental vs Alternativa Ingenua)
Evalúa el rendimiento empírico del recorrido incremental frente a la alternativa descartada de repetir el recorrido por llave (FR-RES-020, SC-007).

```powershell
python -m cripta --bench --solo resolubilidad
```
- **Resultado esperado**:
  - Salida con código `0`.
  - Muestra la comparación determinista basada en `SEMILLA_BENCH` sobre criptas sintéticas de muchas llaves encadenadas.
  - Reporta que `recorrido_ingenuo_reiniciado` es significativamente más lento que `recorrido_incremental` (evidencia empírica de aceleración).

---

### Escenario 5: Cota de Rendimiento de 200 ms sobre la Mayor Cripta Publicada
Verifica que el tiempo cronológico en el entorno de referencia sea estrictamente inferior a 200 ms (SC-001).

```powershell
python -m cripta --bench --solo resolubilidad_cota
```
- **Resultado esperado**: La verificación de resolubilidad sobre la cripta publicada de mayor tamaño (`cripta-04`, 50 salas) se ejecuta en un tiempo $< 200\text{ ms}$ (típicamente $< 5\text{ ms}$).

---

### Escenario 6: Validación de Casos Específicos del Apéndice B
Ejecutar la suite focalizada en los escenarios del enunciado:

```powershell
python -m unittest tests/modelo/test_resolubilidad.py -k ApendiceB
```
- **Casos cubiertos**:
  1. Llave de salida tras la única puerta que ella misma abre: clasificada como no resoluble; reporte señala el ciclo de dependencia circular exacto (`itm_llave_salida -> itm_llave_salida`).
  2. Llave en campo `suelta` de un enemigo errante: ubicada y obtenible en la sala inicial del enemigo.
  3. Varios órdenes válidos de recolección: dos ejecuciones consecutivas bajo las mismas entradas producen exactamente la misma secuencia ordenada con desempate léxico en orden ascendente (SC-003).

---

### Escenario 7: Casos Límite de Datos e Infraestructura
1. **Costos contradictorios en esqueleto (FR-RES-021)**:
   - Al verificar una cripta con costos incoherentes en los extremos de una conexión, el comando termina informando `CriptaDatosInvalidosError` con código de salida `1` sin emitir reporte de resolubilidad.
2. **Presupuesto de solicitudes agotado (FR-RES-023, SC-008)**:
   - Con el presupuesto en cero y sin datos en caché, el sistema aborta informando `CriptaLimiteError` con código de salida `2` sin emitir reportes parciales.
3. **Puertas cerradas sin llave (FR-RES-022)**:
   - Clasificadas como barreras permanentemente infranqueables e incluidas en la frontera bloqueada con `llave=None`.
