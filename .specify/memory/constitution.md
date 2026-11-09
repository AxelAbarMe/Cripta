# Constitución del Proyecto Cripta — Segunda Parte

## Principios Fundamentales

### I. Estructuras de datos implementadas por el grupo
- Las estructuras de datos utilizadas para resolver los problemas evaluados (Parte 1 §4 y Parte 2 §5) DEBEN implementarse a mano por el grupo en `cripta/estructuras/` o junto al módulo que las consume.
- En los problemas evaluados queda PROHIBIDO el uso de `dict` como índice, caché, tabla de búsqueda o estructura propia.
- En los problemas evaluados queda PROHIBIDO el uso de `set` como índice, caché, tabla de búsqueda o estructura propia.
- En los problemas evaluados queda PROHIBIDO el uso de `heapq`, `bisect`, `collections` (`deque`, `OrderedDict`, `defaultdict`, `Counter`), `networkx` y cualquier biblioteca externa de grafos o cálculo de rutas.
- En los ordenamientos evaluados queda PROHIBIDO el uso de `list.sort()` y `sorted()`.
- Queda PERMITIDO el uso de `list` únicamente como almacenamiento contiguo indexado por posición entera.
- Queda PERMITIDO el uso de los módulos `struct` y `json`, de la biblioteca `requests` y de bibliotecas de interfaz de usuario.
- Queda PERMITIDO el uso de objetos `dict` producidos exclusivamente por `respuesta.json()`, con el único fin de leer datos JSON provenientes del servicio externo.
- Toda propuesta en un documento `plan.md` que contenga una dependencia o estructura prohibida DEBE ser rechazada de inmediato en revisión sin pasar a fase de implementación.
- *Justificación*: El objetivo académico y evaluativo central del curso es el diseño, implementación manual y análisis riguroso de estructuras de datos fundamentales, por lo que esas estructuras no pueden sustituirse por implementaciones equivalentes de bibliotecas.

### II. Determinismo
> *Definición*: El **determinismo** es la propiedad por la cual una ejecución del juego, ante las mismas entradas y configuración inicial, produce de manera exacta la misma secuencia de estados, eventos y resultados en cualquier entorno.
- A igualdad de versión de la cripta, semilla pseudoaleatoria y secuencia de acciones del jugador, el sistema DEBE reproducir exactamente la misma partida, incluyendo la secuencia idéntica de invocaciones y valores del generador aleatorio.
- Toda generación de números o decisiones aleatorias DEBE emplear una instancia local e independiente de `random.Random(semilla)`, prohibiéndose el uso del generador global (`random.random()`, `random.randint()`, etc.).
- El resultado de la simulación y de cualquier regla de juego NUNCA DEBE depender de la hora del sistema, de mediciones de reloj en tiempo real ni del orden de recepción de respuestas HTTP en la red.
- Todo escenario de empate entre opciones equivalentes DEBE resolverse aplicando el criterio de desempate prescrito por la especificación (por ejemplo, menor identificador numérico de sala).
- *Justificación*: El determinismo estricto garantiza la auditabilidad de las bitácoras de juego, la reproducibilidad de casos de prueba y la validez científica de las mediciones de rendimiento comparativas.

### III. Separación MVC y adaptadores
> *Definición*:
> - **MVC (Modelo-Vista-Controlador)**: patrón de diseño arquitectónico que aísla los datos y las reglas del dominio del juego (Modelo) de la presentación en pantalla o terminal (Vista) y de la captura y despacho de comandos del usuario (Controlador).
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
- Toda solicitud HTTP DEBE establecer un tiempo de espera (*timeout*) explícito. Todo error de red o código HTTP inesperado DEBE reportarse con un mensaje comprensible que identifique la operación que falló, sin terminar el programa con una excepción sin contexto. Una respuesta HTTP 429 DEBE esperarse y reintentarse sin que el programa se caiga.
- El tiempo cronológico real transcurrido en llamadas de red NUNCA DEBE incrementar ni alterar el reloj de tiempo virtual del simulador.
- Los datos persistidos en almacenamiento local DEBEN invalidarse y validarse formalmente por número de versión de la cripta y versión de catálogo, PROHIBIÉNDOSE requerir el borrado manual de archivos como mecanismo de control.
- *Justificación*: El límite de solicitudes es una restricción operativa calificable del entorno que exige una gestión óptima de caché y predescarga sin distorsionar la línea temporal del juego.

### VI. Rendimiento respaldado con --bench
> *Definición*: **--bench** es la opción de línea de comandos que ejecuta cargas sintéticas de medición (*benchmarks*) sobre el modelo, sin instanciar la vista, y reporta tiempos por subsistema.
- Toda aseveración relativa a la eficiencia temporal o espacial en documentos `plan.md`, `DECISIONES.md` o en la defensa oral DEBE sustentar su afirmación con una medición obtenida mediante `--bench`, incluyendo el comando exacto para reproducirla.
- Toda carga de datos sintética ejecutada por `--bench` DEBE ser determinista y reproducible a partir de una semilla especificada.
- Cada elección de estructura de datos o algoritmo en `plan.md` DEBE contrastarse con al menos una alternativa considerada. Las alternativas que el enunciado exige medir (P2 §5 y §6.3) DEBEN implementarse y medirse con `--bench`.
- En las condiciones que fija P2 §6.1, el tiempo medido NO DEBE exceder: ciclo de eventos entre dos decisiones del jugador 20 ms (con decenas de cazadores activos), verificación de resolubilidad 200 ms (cripta publicada más grande), consulta de historia 50 ms (partida de al menos 5 000 acciones, K por defecto) y cálculo de un paso de «ir a» 5 ms (mapa conocido completo). Estos valores pueden cambiar por enmienda oficial del docente.
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
- El pergamino de retroceso NO DEBE implementarse guardando copias completas del estado del juego: solo registra la información necesaria para invertir los cambios. Las copias completas del estado solo se permiten como puntos de control de la línea de tiempo, con la frecuencia máxima que fije su especificación.
- El nuevo formato binario de persistencia DEBE detectar explícitamente si un archivo cargado pertenece a la primera parte como incompatible o bien migrarlo de forma explícita, quedando PROHIBIDO cargarlo en silencio.
- Cualquier modificación sobre una decisión de diseño tomada en la primera parte DEBE acompañarse obligatoriamente de una medición comparativa de rendimiento que justifique el antes y el después.
- *Justificación*: El sistema constituye una evolución incremental que debe preservar la corrección de las bases operativas consolidadas en la entrega anterior y salvaguardar la huella de memoria.

## Restricciones del Proyecto
- **Entorno y ejecución**: Python 3.11 o superior.
- **Pruebas automatizadas**: Implementadas con el módulo estándar `unittest` en `tests/`, conservando una estructura de carpetas idéntica a `cripta/` y requiriendo un archivo `__init__.py` en cada carpeta para garantizar el correcto descubrimiento de pruebas.
- **Convención de nomenclatura**: Clases, métodos, funciones y atributos nuevos DEBEN escribirse en español. Los métodos especiales o mágicos de Python (`__len__`, `__iter__`, etc.) conservan su denominación estándar.
- **Estándar de comentarios**: Encabezado de archivo de máximo 5 líneas y comentarios de método de 1 a 2 líneas, quedando PROHIBIDO el uso de punto y coma (`;`) dentro de cualquier comentario. Las justificaciones de arquitectura y diseño deben alojarse en `DECISIONES.md` o en la carpeta `docs/`.
- **Manejo de errores**: Todo error de programación DEBE heredar de `IndexError` o `ValueError` dentro de su propio módulo. La excepción `CriptaError` (en `cripta.excepciones`) queda reservada exclusivamente para fallos de origen externo (red, disco o archivos).
- **Anonimato**: Queda PROHIBIDO incorporar nombres de personas en código, comentarios, mensajes de commit o documentos para el profesor. La única excepción es la pantalla de créditos del juego.
- **Idioma de documentación**: Toda la documentación técnica, especificaciones y bitácoras deben redactarse en español.

## Flujo de Trabajo
- **Rol de agentes de IA**: Los agentes no realizan `git commit` ni `git push`. La confirmación e integración de cambios es responsabilidad exclusiva de los integrantes humanos, sin aprobación automática.
- **Mensajes de confirmación (Git)**: Redactados en español, acotados a un único tema por commit, y sin incluir identificadores de tarea ni nombres de personas.
- **Integración a `main`**: Todo cambio ingresa a `main` mediante Pull Request revisado por al menos otro compañero y se fusiona mediante *merge commit* (PROHIBIDO el *squash merge*) para preservar la precedencia histórica de especificaciones sobre el código.
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