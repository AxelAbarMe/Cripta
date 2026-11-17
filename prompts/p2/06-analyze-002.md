# Prompt para `/speckit-analyze` — 002 Niebla de guerra e «Ir a»

```text
Analiza la consistencia entre specs/002-niebla-ir-a/spec.md, plan.md, research.md, data-model.md,
quickstart.md, contracts/, tasks.md y la constitución. Solo lectura: no modifiques ningún archivo.
Verifica en particular: cada FR-NIE-001 a 024 tiene al menos una tarea y una prueba que lo cita, y
ninguna tarea cita un requisito inexistente; cada escenario de aceptación de spec.md (historias 1,
2 y 3), los seis casos B-NIE-001 a 006 y SC-NIE-001 a 005 tienen una tarea de prueba; plan.md no
agrega reglas que no estén en spec.md y spec.md no nombra estructuras, clases ni módulos; ninguna
tarea ni decisión usa heapq, bisect, collections, networkx, set ni dict como índice o caché, ni
list.sort() o sorted(); cada afirmación de rendimiento cita el comando de --bench o está marcada
como hipótesis; las rutas de archivo del plan, del quickstart y de las tareas coinciden y su
estado (Nuevo / Modificado) es correcto según el repositorio; las pruebas van antes que el código
en cada fase, la numeración de tareas es consecutiva y el orden de dependencias entre fases es
coherente; las etiquetas Depende de 001 y Depende de 004 están donde corresponde y ninguna tarea
presenta como existente código que solo está previsto por la 001 (BuscadorRutas, esta_vacio,
__len__, costo en el movimiento); el quickstart, el contrato y el modelo de datos no contradicen
al plan (por ejemplo, alternativas de búsqueda descartadas); la cripta de referencia se elige sin
fijar su id en el código; los errores de programación heredan de IndexError o ValueError; el punto
de corte del Pull Request y su dependencia con la 001 están explícitos. Clasifica cada hallazgo
por gravedad y señala el archivo y la línea.
```