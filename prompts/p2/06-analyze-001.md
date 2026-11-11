Analiza la consistencia entre specs/001-terreno-cazador/spec.md, plan.md, tasks.md y la constitución.
Solo lectura: no modifiques ningún archivo. Verifica en particular:
- Cada FR-TER-001 a 023 tiene al menos una tarea y una prueba que lo cita, y ninguna tarea cita un
  requisito inexistente.
- Los siete casos del Apéndice B aparecen como escenarios con prueba.
- plan.md no agrega reglas que no estén en spec.md, y spec.md no nombra estructuras, clases ni módulos.
- Ninguna tarea ni decisión usa heapq, bisect, collections, networkx, set ni dict como índice o caché.
- Cada afirmación de rendimiento cita un comando de --bench o está marcada como hipótesis.
- Las rutas de archivo del plan y de las tareas coinciden (Nuevo / Modificado).
- Las pruebas van antes que el código en cada fase y el orden de dependencias entre fases es coherente.
- El contrato de datos (Fase A) es separable y no depende de B, C, D ni E.
Clasifica cada hallazgo por gravedad y señala el archivo y la línea.