# Investigación de diseño: niebla de guerra e «ir a»

## Decisiones

### Índice del conocimiento

- **Decisión**: listas contiguas indexadas por id de sala y por las cuatro direcciones; estados de sala y puerta con tres valores.
- **Razón**: P2 §5.3 exige consultas frecuentes baratas y exploración proporcional a lo revelado. La lista permite consulta/cambio O(1) y revelación O(R) con grado cardinal fijo. `dict` y `set` están prohibidos.
- **Alternativas**: `VectorOrdenado` existente, descartado para consultas frecuentes por O(log V) y para revelación por O(R log V); tabla hash, prohibida.
- **Límite**: espacio O(max_id), que se medirá para ids dispersos.

### Registro reversible

- **Decisión**: cada cambio registra una closure inversa con `Reversible._registrar_inversa` y `HistorialRetroceso.registrar_cambio`.
- **Razón**: `cripta/modelo/reversible.py` conserva el valor anterior al pisarlo; `cripta/modelo/historial_retroceso.py` aplica inversas LIFO por intervalo. La antorcha registra solo celdas reveladas o modificadas.
- **Alternativas**: copia completa por acción, prohibida; segundo sistema de deltas, descartado por duplicación.
- **Medición**: actualización por antorcha y reversión comparadas con copia completa solo como referencia de `--bench`.

### Ruta del jugador

- **Decisión**: Dijkstra con `HeapMinimo` propio; evaluar reutilizar el núcleo previsto por la 001 con proveedor de adyacencias conocidas. No compartir el estado/caché del cazador. Recalcular antes de cada paso.
- **Razón**: costos ponderados, subgrafo parcial, puertas recordadas abiertas y conocimiento que puede cambiar entre pasos.
- **Alternativas**: duplicar Dijkstra, descartado provisionalmente por duplicación y riesgo de discrepancia; selección lineal manual, alternativa experimental obligatoria con costo O(V²+E).
- **Condición**: conservar reutilización solo si la interfaz de 001 admite vecinos inyectados y la medición confirma <5 ms. La ruta de cazador se cita únicamente como prevista en `specs/001-terreno-cazador/plan.md`; no existe como código en esta rama.

### Orquestación y bitácora

- **Decisión**: bucle de viaje en `ControladorCripta`; cada paso se envía mediante `ServicioPartida.ejecutar` como movimiento ordinario. El servicio escribe un comentario único antes del primer paso y registra cada movimiento por la vía actual.
- **Razón**: conserva acciones, eventos, retroceso y registro individual. La vista presenta la proyección y el motivo; el modelo no conoce UI ni disco.
- **Alternativas**: bucle en el modelo, descartado por mezclar coordinación/presentación; bucle en la vista, descartado porque no debe controlar reglas ni ejecutar acciones.
- **Regla asociada**: los turnos de enemigos no se escriben en log; está descrito como previsto por 001 en su plan, no como código existente.

### Persistencia

- **Decisión**: agregar al estado lógico los tres estados por sala y cuatro observaciones por sala como datos planos.
- **Razón**: FR-NIE-006 y SC-NIE-005 requieren guardar/cargar e historia.
- **Alternativa**: inferir al cargar solo desde la posición actual, descartada porque pierde visitas anteriores y últimas observaciones.
- **Alcance**: 004 define formato binario, versión y compatibilidad; este diseño no los fija.

## Contexto verificado

- `docs/MAPA_CODIGO.md` identifica motor, reversibilidad, historial, mapa, servicio, controlador, vista, log y harness `--bench`.
- `cripta/modelo/buscador_rutas.py` no está en esta rama. La previsión de 001 aparece en `specs/001-terreno-cazador/plan.md`.
- `fixtures/cripta-06/` existe en esta rama y será fuente de referencia, sujeta a verificar versión e integridad en el benchmark.
- El índice de conocimiento, la búsqueda de ruta y las pruebas descritas aquí son decisiones de planificación; no se afirma que estén implementadas.

## Hipótesis por comprobar

1. Las listas directas por id usan memoria aceptable para el mayor id de la referencia.
2. El núcleo Dijkstra compartido tiene costo comparable a una copia especializada y ambos quedan bajo 5 ms.
3. La selección lineal puede ganar en mapas pequeños por su menor constante, aunque empeora cuadráticamente.
4. Las inversas por celda mantienen buen desempeño cuando la antorcha revela varias vecinas.

No se asignan cifras previas: se medirán con `py -m cripta --bench --solo niebla_rutas --escala 1`.
