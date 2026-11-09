Establece la constitución del proyecto Cripta, segunda parte. Escríbela completa en español,
incluidos los títulos de las secciones de la plantilla. Cada principio debe tener reglas
verificables (que una revisión pueda decir "se cumple" o "no se cumple") y una línea con su
justificación. Explica brevemente, la primera vez que aparezcan, los términos MVC, determinismo,
requisito FR y --bench. Modifica solo .specify/memory/constitution.md.

Contexto: Cripta es un juego de mazmorra por eventos en Python 3.11+ cuyo objetivo es elegir
estructuras de datos y defenderlas con mediciones. La segunda parte continúa el código de la
primera y se desarrolla con spec-kit. Fuentes: docs/enunciados/ (gana ante cualquier duda),
docs/CONTEXTO_CRIPTA2.md y docs/MAPA_CODIGO.md.

PRINCIPIOS

I. Estructuras de datos implementadas por el grupo
- Las estructuras que resuelven los problemas evaluados (P1 §4 y P2 §5) se implementan a mano en
  cripta/estructuras/ o junto al módulo que las usa.
- Prohibido para esos problemas: dict como índice, caché, tabla de búsqueda o estructura propia;
  set en las mismas condiciones; heapq; bisect; collections (deque, OrderedDict, defaultdict,
  Counter); networkx y cualquier biblioteca de grafos o búsqueda de rutas; list.sort() y sorted()
  en los ordenamientos evaluados.
- Permitido: list como almacenamiento contiguo; struct, json, requests y bibliotecas de interfaz;
  los dict que devuelve respuesta.json(), solo para leer JSON.
- Un plan.md que proponga una dependencia prohibida se rechaza antes de implementar.

II. Determinismo
- Misma versión de cripta, misma semilla y mismas acciones producen la misma partida, incluida la
  misma secuencia de llamadas al generador aleatorio.
- Toda aleatoriedad usa una instancia propia random.Random(semilla), nunca el generador global.
- Nunca deciden el resultado la hora del sistema ni el orden de llegada de respuestas HTTP.
- Los empates siguen el desempate que fija la especificación (por ejemplo, menor id de sala).

III. Separación MVC y adaptadores
- El modelo no conoce HTTP, archivos ni la interfaz concreta.
- Red y disco van detrás de interfaces. --offline sustituye la fuente de datos sin if repartidos
  por el modelo.
- --replay, --bench y --verificar se ejecutan sin instanciar la vista.

IV. Ningún dato de una cripta concreta en el código
- Sin números de sala, ids de entidades, cantidad de páginas, presupuestos ni estadísticas de una
  cripta específica. Todo sale del API o de los archivos de --offline.

V. Presupuesto de red
- Se respeta presupuesto_solicitudes de cada cripta. Toda solicitud HTTP cuenta, incluidos los
  reintentos tras HTTP 429 y la consulta de llaves.
- Toda solicitud usa un tiempo de espera explícito y los errores de red se reportan con la
  operación que falló. El tiempo real de red nunca avanza el reloj virtual.
- Lo persistido se valida por versión de cripta y de catálogo, no borrando archivos a mano.

VI. Rendimiento respaldado con --bench
- Toda afirmación de rendimiento en un plan.md, en DECISIONES.md o en la defensa cita una medición
  de --bench, con el comando exacto que la produce.
- Las cargas sintéticas de --bench son deterministas por semilla.
- Cada decisión de estructura se compara con al menos una alternativa medida.
- Límites vigentes (P1 §5.2 y P2 §6.1, ajustables por enmienda del profesor): ciclo de eventos
  20 ms, verificación de resolubilidad 200 ms, consulta historia 50 ms, paso de «ir a» 5 ms.

VII. La especificación precede al código
- Cada capacidad sigue el flujo specify, clarify, plan, tasks, analyze, implement.
- spec.md describe qué y por qué: reglas, escenarios y requisitos numerados. No nombra
  estructuras, clases ni módulos.
- plan.md describe cómo y no agrega reglas que no estén en spec.md.
- Cada requisito tiene un identificador estable FR-XXX-NNN. Cada tarea de tasks.md cita los
  requisitos que atiende. Cada escenario de aceptación tiene al menos una prueba automatizada o un
  partida.log de reproducción, y la prueba cita el requisito.
- Cada caso del Apéndice B del enunciado de la segunda parte aparece como escenario en alguna
  especificación.
- En Git, la especificación de una capacidad se confirma antes que su código. Si la
  especificación estaba mal, se corrige primero, en un commit separado, y después el código.

VIII. Compatibilidad con la primera parte
- Las pruebas de la primera parte siguen pasando con py -m unittest discover -s tests -t .
- El retroceso no guarda copias completas del estado. Las copias completas solo se permiten como
  puntos de control de la línea de tiempo, en la frecuencia que fije su especificación.
- El formato binario nuevo detecta un archivo de la primera parte como incompatible o lo migra de
  forma explícita. Nunca lo carga en silencio.
- Una decisión de la primera parte solo se cambia con medición del antes y el después.

RESTRICCIONES DEL PROYECTO
- Python 3.11 o superior. Pruebas con unittest en tests/, con la misma estructura de carpetas que
  cripta/ y un __init__.py en cada carpeta.
- Clases, métodos y atributos nuevos en español. Los métodos especiales (__len__...) quedan igual.
- Comentarios: cabecera de máximo 5 líneas por archivo y 1 o 2 líneas por método, sin punto y
  coma dentro del comentario. Las justificaciones van a DECISIONES.md o a docs/.
- Un error de programación hereda de IndexError o ValueError en su propio módulo. CriptaError es
  solo para errores externos (red, disco, archivos).
- Sin nombres de personas en código, comentarios, commits ni documentos para el profesor.
- Documentación en español.

FLUJO DE TRABAJO
- Los agentes no hacen commit ni push. Los hacen las personas, sin aprobación automática.
- Commits en español, un tema por commit, sin códigos de tarea ni nombres de personas.
- Todo cambio entra a main por Pull Request revisado por al menos otro integrante y se fusiona con
  merge commit (sin squash), para conservar el historial que muestra cada especificación antes
  que su código.
- Toda invocación de un comando de spec-kit con texto propio se registra en PROMPTS_LLM.md con
  fecha, herramienta, prompt textual y para qué se usó.

GOBERNANZA
- Esta constitución prevalece sobre plan.md, tasks.md y cualquier sugerencia de un agente. Si un
  plan o una tarea la contradice, el error es del grupo y se corrige antes de implementar.
- /speckit-analyze y la revisión de cada Pull Request verifican el cumplimiento.
- Una enmienda se propone en un Pull Request que solo cambia la constitución, explica el motivo y
  requiere el acuerdo de los tres integrantes.
- Versión semántica: MAJOR si se quita o redefine un principio, MINOR si se agrega uno, PATCH si
  solo cambia la redacción. Versión inicial 1.0.0, ratificada el 2026-11-09.