# Instrucciones para agentes — Cripta 2
1. Lee primero docs/CONTEXTO_CRIPTA2.md (PARTE D) y .specify/memory/constitution.md.
2. Antes de planificar, lee docs/MAPA_CODIGO.md. No inventes módulos que no existan.
3. PROHIBIDO en los problemas evaluados: heapq, bisect, collections (deque, OrderedDict,
   defaultdict, Counter), networkx, bibliotecas de grafos/rutas, list.sort()/sorted() donde el
   enunciado lo prohíbe, dict o set como índice/caché/tabla de búsqueda. Implementa a mano.
4. spec.md = QUÉ y POR QUÉ (sin estructuras, clases ni módulos). plan.md = CÓMO.
5. Determinismo: random.Random(semilla) propia; nunca hora del sistema ni orden de red.
6. MVC: modelo sin red/archivos/UI; --replay y --bench no instancian la vista.
7. Ningún dato de una cripta concreta en el código.
8. Cada tarea cita su requisito (FR-XXX-NNN); cada prueba cita el requisito que cubre.
9. Si falta información, pregunta; no asumas. Si la spec está mal, corrige la spec PRIMERO.
10. No hagas commits ni push. Los hace el humano. Registra el trabajo en tasks.md (casillas).
11. Si te quedas sin contexto/tokens: deja tasks.md actualizado y escribe docs/HANDOFF.md.
12. Convenciones de la Parte I (siguen vigentes):
    - Clases, métodos y atributos nuevos en español. Los métodos especiales (__len__...) quedan igual.
    - Comentarios: cabecera de máximo 5 líneas por archivo y 1-2 líneas por método. Nunca ";"
      dentro de un comentario. Las justificaciones van a docs/ o DECISIONES.md, no al código.
    - Sin nombres de personas en código, comentarios, commits ni documentos para el profesor.
    - Un error de programación hereda de IndexError o ValueError en su propio módulo. CriptaError
      (excepciones.py) es solo para errores externos (red, disco, archivos).
    - Pruebas con unittest en tests/, misma estructura que cripta/, y cada carpeta con su
      __init__.py (si falta, discover no la ve).
    - Respeta los finales de línea CRLF de los archivos existentes.
    - No crees ni modifiques un .py que la tarea no pida sin preguntar antes.