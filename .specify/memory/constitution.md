<!--
INFORME DE IMPACTO DE SINCRONIZACIÓN (SYNC IMPACT REPORT)
- Cambio de versión: plantilla inicial (sin versión) → 1.0.0
- Principios modificados / establecidos:
  * [PRINCIPLE_1_NAME] → I. Estructuras de datos implementadas por el grupo
  * [PRINCIPLE_2_NAME] → II. Determinismo
  * [PRINCIPLE_3_NAME] → III. Separación MVC y adaptadores
  * [PRINCIPLE_4_NAME] → IV. Ningún dato de una cripta concreta en el código
  * [PRINCIPLE_5_NAME] → V. Presupuesto de red
  * (Nuevo) → VI. Rendimiento respaldado con --bench
  * (Nuevo) → VII. La especificación precede al código
  * (Nuevo) → VIII. Compatibilidad con la primera parte
- Secciones agregadas:
  * [SECTION_2_NAME] → Restricciones del Proyecto
  * [SECTION_3_NAME] → Flujo de Trabajo
  * Gobernanza (completada con reglas específicas de Cripta 2)
- Secciones eliminadas: Ninguna.
- Tareas pendientes (TODOs): Ninguna. Todos los marcadores han sido definidos.
-->

# Constitución del Proyecto Cripta — Segunda Parte

## Principios Fundamentales

### I. Estructuras de datos implementadas por el grupo
- Las estructuras de datos utilizadas para resolver los problemas evaluados (Parte 1 §4 y Parte 2 §5) DEBEN implementarse a mano por el grupo en `cripta/estructuras/` o junto al módulo que las consume.
- En los problemas evaluados queda terminantemente PROHIBIDO el uso de `dict` como índice, caché, tabla de búsqueda o estructura propia.
- En los problemas evaluados queda terminantemente PROHIBIDO el uso de `set` como índice, caché, tabla de búsqueda o estructura propia.
- En los problemas evaluados queda terminantemente PROHIBIDO el uso de `heapq`, `bisect`, `collections` (`deque`, `OrderedDict`, `defaultdict`, `Counter`), `networkx` y cualquier biblioteca externa de grafos o cálculo de rutas.
- En los ordenamientos evaluados queda terminantemente PROHIBIDO el uso de `list.sort()` y `sorted()`.
- Queda PERMITIDO el uso de `list` únicamente como almacenamiento contiguo indexado por posición entera.
- Queda PERMITIDO el uso de módulos estándar `struct`, `json`, `requests` y bibliotecas de interfaz de usuario.
- Queda PERMITIDO el uso de objetos `dict` producidos exclusivamente por `respuesta.json()`, con el único fin de leer datos JSON provenientes del servicio externo.
- Toda propuesta en un documento `plan.md` que contenga una dependencia o estructura prohibida DEBE ser rechazada de inmediato en revisión sin pasar a fase de implementación.
- *Justificación*: El objetivo académico y evaluativo central del curso es el diseño, implementación manual y análisis riguroso de estructuras de datos fundamentales, vetando cualquier solución delegada a bibliotecas nativas u optimizadas externamente.

### II. Determinismo
> *Definición*: El **determinismo** es la propiedad por la cual una ejecución del juego, ante las mismas entradas y configuración inicial, produce de manera exacta la misma secuencia de estados, eventos y resultados en cualquier entorno.
- A igualdad de versión de la cripta, semilla pseudoaleatoria y secuencia de acciones del jugador, el sistema DEBE reproducir exactamente la misma partida, incluyendo la secuencia idéntica de invocaciones y valores del generador aleatorio.
- Toda generación de números o decisiones aleatorias DEBE emplear una instancia local e independiente de `random.Random(semilla)`, prohibiéndose el uso del generador global (`random.random()`, `random.randint()`, etc.).
- El resultado de la simulación y de cualquier regla de juego NUNCA debe depender de la hora del sistema, de mediciones de reloj en tiempo real ni del orden de recepción de respuestas HTTP en la red.
- Todo escenario de empate entre opciones equivalentes DEBE resolverse aplicando taxativamente el criterio de desempate prescrito por la especificación (por ejemplo, menor identificador numérico de sala).
- *Justificación*: El determinismo estricto garantiza la auditabilidad de las bitácoras de juego, la reproducibilidad de casos de prueba y la validez científica de las mediciones de rendimiento comparativas.

### III. Separación MVC y adaptadores
> *Definiciones*:
> - **MVC (Modelo-Vista-Controlador)**: patrón de diseño arquitectónico que aísla los datos y las reglas del dominio del juego (Modelo) de la presentación en pantalla o terminal (Vista) y de la captura y despacho de comandos del usuario (Controlador).
> - **--bench**: opción de línea de comandos para la ejecución de pruebas de rendimiento comparativo (*benchmarks*) automatizadas sobre el modelo sin interacción visual.
- La capa del Modelo NO DEBE contener importaciones ni referencias directas a llamadas HTTP, operaciones de sistema de archivos ni componentes de interfaz gráfica o de consola.
- Las operaciones de red y de almacenamiento en disco DEBEN encapsularse detrás de interfaces de adaptación; la opción `--offline` DEBE reemplazar la fuente de datos mediante la inyección del adaptador correspondiente, sin incorporar bifurcaciones condicionales (`if`) dispersas en el Modelo.
- Las modalidades de ejecución de prueba y verificación `--replay`, `--bench` y `--verificar` DEBEN ejecutarse íntegramente sin instanciar la Vista ni componentes de presentación interactiva.
- *Justificación*: La separación arquitectónica permite someter la lógica pura del juego a pruebas automatizadas de regresión, análisis de rendimiento y verificación sin interferencias ni efectos secundarios de entrada/salida.

### IV. Ningún dato de una cripta concreta en el código
- El código fuente NO DEBE incluir valores fijos (*hardcoded*) de números de sala, identificadores de entidades, total de páginas, presupuestos de solicitudes ni parámetros estadísticos pertenecientes a una cripta particular.
- Todos los datos de configuración de salas, laberintos, llaves, catálogos y entidades DEBEN obtenerse dinámicamente desde el API remoto o desde los archivos serializados consumidos por la modalidad `--offline`.
- *Justificación*: El motor del juego debe ser enteramente agnóstico a las instancias particulares de criptas, garantizando su capacidad de operar de forma general sobre cualquier laberinto generado conforme a la especificación.

### V. Presupuesto de red
- El consumo de solicitudes DEBE respetar estrictamente el límite estipulado por `presupuesto_solicitudes` de cada cripta durante la partida.
- Toda petición HTTP emitida hacia el API DEBE contabilizarse en el presupuesto, computando reintentos motivados por respuestas HTTP 429 y consultas al endpoint de llaves (`/llaves`).
- Toda solicitud HTTP DEBE establecer un tiempo de espera (*timeout*) explícito; en caso de fallo de conexión, el error DEBE registrarse identificando con precisión la operación fallida.
- El tiempo cronológico real transcurrido en llamadas de red NUNCA debe incrementar ni alterar el reloj de tiempo virtual del simulador.
- Los datos persistidos en almacenamiento local DEBEN invalidarse y validarse formalmente por número de versión de la cripta y versión de catálogo, PROHIBIÉNDOSE requerir el borrado manual de archivos como mecanismo de control.
- *Justificación*: El límite de solicitudes es una restricción operativa calificable del entorno que exige una gestión óptima de caché y predescarga sin distorsionar la línea temporal del juego.

### VI. Rendimiento respaldado con --bench
- Toda aseveración relativa a la eficiencia temporal o espacial en documentos `plan.md`, `DECISIONES.md` o en la defensa oral DEBE sustentar su afirmación con una medición obtenida mediante `--bench`, incluyendo el comando exacto para reproducirla.
- Toda carga de datos sintética ejecutada por `--bench` DEBE ser determinista y reproducible a partir de una semilla especificada.
- Cada elección de estructura de datos o algoritmo en `plan.md` DEBE evaluarse y contrastarse frente a al menos una alternativa implementada y medida empíricamente.
- El tiempo de ejecución medido NO DEBE exceder los límites máximos establecidos: ciclo de eventos hasta 20 ms, verificación de resolubilidad hasta 200 ms, consulta de historia hasta 50 ms y paso del comando «ir a» hasta 5 ms (salvo enmienda oficial del docente).
- *Justificación*: El diseño de software de alto rendimiento exige comprobación empírica cuantificable frente a alternativas, erradicando conjeturas no demostradas en la defensa de decisiones técnicas.

### VII. La especificación precede al código
> *Definición*: Un **requisito FR** (*Functional Requirement* o Requisito Funcional) es una cláusula normativa con identificador estructurado (`FR-XXX-NNN`) que define sin ambigüedad una conducta observable, regla de juego o capacidad técnica requerida del sistema.
- Cada capacidad DEBE desarrollarse siguiendo estrictamente la secuencia de etapas: `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`.
- El documento `spec.md` DEBE describir exclusivamente el QUÉ y el POR QUÉ (reglas del juego, historias de usuario, escenarios de aceptación y requisitos funcionales numerados), y NO DEBE mencionar estructuras de datos, nombres de clases ni nombres de módulos de código.
- El documento `plan.md` DEBE describir el CÓMO técnico y NO DEBE introducir reglas de juego que no figuren en `spec.md`.
- Cada requisito funcional DEBE poseer un identificador formal estable con prefijo `FR-XXX-NNN`; cada tarea en `tasks.md` DEBE citar el o los requisitos específicos que implementa.
- Cada escenario de aceptación DEBE contar con al menos una prueba automatizada con `unittest` o un archivo `partida.log` de reproducción verificable, citando explícitamente en el código de prueba el identificador del requisito cubierto.
- Todos los casos de prueba enunciados en el Apéndice B del enunciado oficial de la segunda parte DEBEN figurar explícitamente como escenarios de aceptación en alguna especificación de capacidad.
- En el historial de Git, el commit con la especificación formal de una funcionalidad DEBE anteceder cronológicamente al commit de su código fuente de implementación; si se detecta un error de especificación durante la codificación, este DEBE corregirse primero en un commit independiente de documentación antes de modificar el código.
- *Justificación*: La metodología de desarrollo guiado por especificación (SDD) exige rigor documental y trazabilidad bidireccional continua, impidiendo la aparición de código huérfano o divergencias entre la especificación y el producto final.

### VIII. Compatibilidad con la primera parte
- El conjunto completo de pruebas unitarias desarrolladas en la primera parte DEBE continuar ejecutándose exitosamente mediante el comando `py -m unittest discover -s tests -t .`.
- El mecanismo de retroceso temporal NO DEBE almacenar copias profundas completas de la totalidad del estado del juego en cada evento; las copias completas de estado se reservan con exclusividad para puntos de control de la línea de tiempo con la periodicidad que dicte su especificación.
- El nuevo formato binario de persistencia DEBE detectar explícitamente si un archivo cargado pertenece a la primera parte como incompatible o bien ejecutar una migración transparente notificada, quedando terminantemente PROHIBIDO cargarlo de forma silente o corrupta.
- Cualquier modificación sobre una decisión de diseño tomada en la primera parte DEBE acompañarse obligatoriamente de una medición comparativa de rendimiento que justifique el antes y el después.
- *Justificación*: El sistema constituye una evolución incremental que debe preservar la corrección de las bases operativas consolidadas en la entrega anterior y salvaguardar la huella de memoria.

## Restricciones del Proyecto
- **Entorno y ejecución**: Python 3.11 o superior.
- **Pruebas automatizadas**: Implementadas con el módulo estándar `unittest` en `tests/`, conservando una estructura de carpetas idéntica a `cripta/` y requiriendo un archivo `__init__.py` en cada carpeta para garantizar el correcto descubrimiento de pruebas.
- **Convención de nomenclatura**: Clases, métodos, funciones y atributos nuevos DEBEN escribirse en español. Los métodos especiales o mágicos de Python (`__len__`, `__iter__`, etc.) conservan su denominación estándar.
- **Estándar de comentarios**: Encabezado de archivo de máximo 5 líneas y comentarios de método de 1 a 2 líneas, quedando PROHIBIDO el uso de punto y coma (`;`) dentro de cualquier comentario. Las justificaciones de arquitectura y diseño deben alojarse en `DECISIONES.md` o en la carpeta `docs/`.
- **Manejo de errores**: Todo error de programación DEBE heredar de `IndexError` o `ValueError` dentro de su propio módulo. La excepción `CriptaError` (en `cripta.excepciones`) queda reservada exclusivamente para fallos de origen externo (red, disco o archivos).
- **Anonimato**: Queda terminantemente PROHIBIDO incorporar nombres de personas en código, comentarios, mensajes de commit o entregables académicos.
- **Idioma de documentación**: Toda la documentación técnica, especificaciones y bitácoras deben redactarse en español.

## Flujo de Trabajo
- **Rol de agentes de IA**: Los agentes no realizan `git commit` ni `git push`. La confirmación e integración de cambios es responsabilidad exclusiva de los integrantes humanos, sin aprobación automática.
- **Mensajes de confirmación (Git)**: Redactados en español, acotados a un único tema por commit, y sin incluir identificadores de tarea ni nombres de personas.
- **Integración continua**: Todo cambio ingresa a `main` mediante Pull Request revisado por al menos otro compañero y se fusiona mediante *merge commit* (PROHIBIDO el *squash merge*) para preservar la precedencia histórica de especificaciones sobre el código.
- **Bitácora de prompts**: Toda invocación de un comando de `spec-kit` con texto propio DEBE registrarse en `PROMPTS_LLM.md` indicando fecha, herramienta, prompt textual y propósito de uso.

## Gobernanza
- **Supremacía**: Esta constitución prevalece sobre `plan.md`, `tasks.md` y cualquier recomendación o sugerencia emitida por un agente. Si surge discrepancia, el artefacto subordinado se corrige antes de implementar código.
- **Cumplimiento**: El comando `/speckit-analyze` y la revisión por pares en cada Pull Request validan el cumplimiento obligatorio de estos principios.
- **Procedimiento de enmienda**: Cualquier reforma a esta constitución requiere un Pull Request exclusivo que argumente el cambio y obtenga la aprobación unánime de los tres integrantes del equipo.
- **Versionado semántico**:
  - Incremento **MAJOR**: Eliminación o redefinición sustancial de principios existentes.
  - Incremento **MINOR**: Adición de nuevos principios o ampliación material de las normas del proyecto.
  - Incremento **PATCH**: Correcciones ortográficas, de estilo o aclaraciones menores que no alteren las reglas.
  - Versión inicial: 1.0.0, formalmente ratificada el 2026-11-09.

**Versión**: 1.0.0 | **Ratificada**: 2026-11-09 | **Última enmienda**: 2026-11-09
