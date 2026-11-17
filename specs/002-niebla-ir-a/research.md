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

- **Decisión**: búsqueda de costo mínimo propia del jugador en `cripta/modelo/ruta_conocida.py`, con `HeapMinimo` propio, calculada desde el destino sobre el subgrafo conocido y recalculada antes de cada paso. No se comparte el estado ni la caché del cazador.
- **Razón**: costos ponderados, subgrafo parcial, puertas recordadas abiertas y conocimiento que puede cambiar entre pasos.
- **Alternativas**: reutilizar `BuscadorRutas` previsto por la 001, descartada porque calcula sobre el mapa real, poda por rango de cazadores, guarda una caché pensada para sus eventos y no recibe destino; selección lineal manual, alternativa experimental obligatoria con costo O(V²+E).
- **Costo por salida**: al revelar una sala, guardar el costo de cada salida en listas propias indexadas por id para consulta O(1); `ruta_conocida.py` usa esos valores y no consulta `CriptaMapa.costo_de_conexion`. Se descarta consultar el esqueleto en cada relajación porque accede a la representación real en vez de la proyección conocida. `--bench` medirá ambas alternativas, sin cifras previas.
- **Dependencia**: `HeapMinimo.esta_vacio` y `__len__` los añade la 001. La búsqueda del cazador se cita únicamente como prevista en `specs/001-terreno-cazador/plan.md`; no existe como código en esta rama.

### Orquestación y bitácora

- **Decisión**: bucle de viaje en `ControladorCripta`; cada paso se envía mediante `ServicioPartida.ejecutar` como movimiento ordinario. El servicio escribe un comentario único antes del primer paso y registra cada movimiento por la vía actual.
- **Razón**: conserva acciones, eventos, retroceso y registro individual. La vista presenta la proyección y el motivo; el modelo no conoce UI ni disco.
- **Alternativas**: bucle en el modelo, descartado por mezclar coordinación/presentación; bucle en la vista, descartado porque no debe controlar reglas ni ejecutar acciones.
- **Regla asociada**: los turnos de enemigos no se escriben en log; está descrito como previsto por 001 en su plan, no como código existente.

### Persistencia

- **Decisión**: agregar al estado lógico los tres estados por sala y cuatro observaciones por sala como datos planos.
- **Razón**: FR-NIE-006 y SC-NIE-005 requieren guardar/cargar e historia.
- **Alternativa**: inferir al cargar solo desde la posición actual, descartada porque pierde visitas anteriores y últimas observaciones.
- **Alcance**: esta capacidad define los campos lógicos y su proyección. La 004 es dueña del formato binario y su versión y realizará un solo cambio de versión.
- **Costos**: forman parte de la proyección persistida y se restauran desde ella, sin recalcularse desde el esqueleto.
- **Dependencia**: la prueba de guardar y cargar depende de 004 (codificación binaria); no hay decisión de propiedad pendiente.

## Contexto verificado

- `docs/MAPA_CODIGO.md` identifica motor, reversibilidad, historial, mapa, servicio, controlador, vista, log y harness `--bench`.
- `CriptaMapa.datos_de_puerta()` expone llave y cierre automático, mientras `EstadoPuertas` conserva el estado mutable cerrado/abierto; se puede distinguir una salida sin esos mecanismos de cierre para FR-NIE-025.
- `cripta/modelo/buscador_rutas.py` no está en esta rama. La previsión de 001 aparece en `specs/001-terreno-cazador/plan.md`.
- `fixtures/cripta-06/` existe en esta rama. La selección de la cripta de referencia (mayor total de salas o `CRIPTA_REFERENCIA` prevista por 001) se unificará con el grupo; el benchmark verificará versión e integridad.
- El índice de conocimiento, la búsqueda de ruta y las pruebas descritas aquí son decisiones de planificación; no se afirma que estén implementadas.

## Hipótesis por comprobar

1. Las listas directas por id usan memoria aceptable para el mayor id de la referencia.
2. La búsqueda propia con `HeapMinimo` queda bajo 5 ms con el mapa conocido completo de la cripta de referencia.
3. La selección lineal puede ganar en mapas pequeños por su menor constante, aunque empeora cuadráticamente.
4. Las inversas por celda mantienen buen desempeño cuando la antorcha revela varias vecinas.

No se asignan cifras previas: se medirán con `py -m cripta --bench --solo niebla_rutas --escala 1`.
