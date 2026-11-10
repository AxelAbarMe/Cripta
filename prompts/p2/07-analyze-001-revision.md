Analiza la consistencia entre specs/001-terreno-cazador/spec.md, plan.md, tasks.md, research.md,
data-model.md, quickstart.md, contracts/ y la constitución, después de las correcciones de la
revisión del Pull Request (sesión de aclaraciones del 2026-11-10).
Solo lectura: no modifiques ningún archivo. Verifica en particular:
- Cada FR-TER-001 a 023 tiene al menos una tarea y una prueba que lo cita, y ninguna tarea cita un
  requisito inexistente. Las tareas nuevas T021b y T026b citan requisitos existentes.
- Los siete casos del Apéndice B aparecen como escenarios con prueba.
- plan.md no agrega reglas que no estén en spec.md, y spec.md no nombra estructuras, clases ni módulos.
- Las decisiones de la sesión del 2026-11-10 se aplican igual en todos los documentos:
  el costo declarado en un solo lado de la conexión rige para ambos sentidos y dos costos distintos
  son un dato inválido (FR-TER-002); un cazador sin rango válido es pasivo y genera un aviso, sin
  excepción (FR-TER-008 y FR-TER-017); los datos externos inválidos usan CriptaDatosInvalidosError
  con cualquier fuente; los turnos de enemigos no escriben en partida.log (FR-TER-021).
- Ningún documento conserva las decisiones reemplazadas (cazador sin rango rechazado con excepción,
  excepción distinta según la fuente, actor «en tránsito»), salvo como historial en la sesión del
  2026-11-09.
- Ninguna tarea ni decisión usa heapq, bisect, collections, networkx, set ni dict como índice o caché.
- Cada afirmación de rendimiento cita un comando de --bench o está marcada como hipótesis.
- Las rutas de archivo del plan y de las tareas coinciden (Nuevo / Modificado).
- Las pruebas van antes que el código en cada fase y el orden de dependencias entre fases es coherente.
- El contrato de datos (Fase A) es separable y no depende de B, C, D ni E.
Clasifica cada hallazgo por gravedad y señala el archivo y la línea.
