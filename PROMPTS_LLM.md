### 2026-09-20 — Claude (Opus 5, app de escritorio de Claude)
**Prompt (resumido):** Se compartió el PDF del enunciado, el openapi.json y
el esqueleto inicial del repo. Se preguntó cómo se organiza la arquitectura
MVC + adaptadores que pide §6 y si el enunciado exige una estructura de
carpetas específica. Luego se pidió, paso a paso y con explicación, probar
el API con un script (prueba_api.py) e interpretar sus respuestas reales, y
construir los primeros DTO de la cripta y del esqueleto (CriptaResumenDTO,
JugadorInicialDTO, CriptaGeneralDTO, SalidaDTO, SalaDTO y
PaginaEsqueletoDTO).

**Para qué se usó:** Entender la arquitectura exigida, verificar el acceso al
API y la forma de sus respuestas, y crear los primeros DTO.

### 2026-09-21 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se compartió el contexto acumulado del proyecto, el PDF del
enunciado, el openapi.json y el estado actual del repo (zip). Se pidió: revisar si
la estructura de carpetas actual cumple la arquitectura MVC + adaptadores exigida
en §6; explicar el funcionamiento de --bench/--offline/--replay y del servicio HTTP
(esqueleto, contenido, catálogo, presupuesto de red); aclarar la diferencia entre
guardar la partida y la prohibición de copiar el estado completo para el pergamino
de retroceso; resolver si el juego necesita reiniciarse para jugar de nuevo; y
proponer una lista inicial de próximos archivos .py a implementar por carpeta.

**Para qué se usó:** Planificar la arquitectura, entender las reglas de red/retroceso
del enunciado y ordenar el trabajo antes de escribir código de estructuras.

### 2026-09-23 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se compartió el contexto acumulado del proyecto
(CONTEXTO_CRIPTA_PARA_CLAUDE.md), el PDF del enunciado, el openapi.json y
el estado del repo (Cripta.zip). Se pidió construir el esqueleto markdown
de la Sección 8 (Documento de Decisiones) para los 11 problemas de §4;
revisar si la estructura de carpetas del zip cumple la arquitectura MVC +
adaptadores de §6 (bench/, docs/, fixtures/, tests/); explicar el
funcionamiento de --bench/--offline/--replay y del servicio HTTP
(esqueleto, contenido, catálogo, presupuesto de red, modo offline);
aclarar la diferencia entre guardar la partida y la prohibición de copiar
el estado completo para el pergamino de retroceso; resolver si el juego
necesita reiniciarse para jugar de nuevo; señalar qué faltaba en el repo
(requirements.txt vacío, PROMPTS_LLM.md ausente, import duplicado en
prueba_api.py); y proponer una lista inicial de próximos archivos .py por
carpeta, fusionada con la tabla de tareas ya existente del grupo.

**Para qué se usó:** Sentar la arquitectura completa del proyecto, entender
las reglas de red/retroceso/presupuesto del enunciado, y organizar el
trabajo pendiente antes de escribir código de estructuras o DTO.

### 2026-09-23 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se pidió revisar los 6 DTO ya existentes contra el
openapi.json e implementar los que faltaban para cubrir cada GET del
contrato de la API: contenido de salas, las 9 clases de entidad del
catálogo discriminadas por "clase", versiones de cripta/catálogo, y
errores 4xx/429. Se explicó para cada uno de dónde vienen los datos, por
qué se diseñó así, y dónde se usará en el modelo y los servicios.
Posteriormente se reorganizaron en archivos de una sola clase cada uno,
siguiendo el estilo ya establecido en el repo (una clase por archivo).

**Para qué se usó:** Completar la capa de DTO del proyecto antes de
construir el cliente HTTP real.

### 2026-09-23 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se pidió continuar con el siguiente conjunto de
archivos .py después de los DTO. Se implementaron cripta/excepciones.py,
infraestructura/puertos.py (interfaces con typing.Protocol),
infraestructura/contador_solicitudes.py, e infraestructura/cliente_http.py
(cliente real con manejo de 429, timeout, validación de lotes y conteo de
solicitudes), verificando que todo compilara e importara correctamente.

**Para qué se usó:** Construir la capa de infraestructura de red que
consumirán los servicios y el modelo, cumpliendo las reglas del PDF sobre
identificador de cliente, manejo de errores/429 y presupuesto de
solicitudes.


### 2026-10-04 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se compartió el zip del proyecto, el PDF del enunciado, el
openapi.json y el contexto acumulado. Se pidió revisar el proyecto completo por
secciones (base, estructuras, DTO, infraestructura, modelo, servicios y bench),
contrastarlo con el enunciado, ejecutar el código para confirmar los fallos y
cerrar con un veredicto de qué falta antes de seguir con el resto del proyecto.

**Para qué se usó:** Detectar y confirmar bugs, ver qué falta contra el enunciado
y ordenar el trabajo pendiente.

### 2026-10-06 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se pidió seguir paso a paso la corrección de los bugs
bloqueantes (constantes faltantes, lista doble enlazada, campo id del contenido
de sala, método del veneno, inserción en VectorOrdenado y llamada del bench),
indicando solo las partes a cambiar y el archivo donde pegarlas.

**Para qué se usó:** Corregir los bugs que impedían importar y ejecutar los
servicios, el inventario, la caché y el bench.


### 2026-10-07 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se pidió definir el contrato de la API pública del motor
Partida y después seguir paso a paso, por etapas con commits pequeños, la mejora
del modelo para poder implementar retroceso y guardado (reloj de eventos, efectos
de veneno y velocidad, historial de retroceso, puertas del mapa e inventario),
indicando solo las partes a cambiar, el archivo donde pegarlas y las pruebas.

**Para qué se usó:** Diseñar la interfaz de Partida y corregir y ampliar el
modelo (reloj, efectos, historial, mapa e inventario), junto con el texto de las
decisiones de diseño correspondientes.


### 2026-10-08 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se compartió el proyecto actualizado con el trabajo de ambos
y se pidió revisar lo relevante, probar el flujo con los datos reales de cripta-01
guardados en fixtures/, y continuar paso a paso con el modelo: un método del mapa
para la llave y el cierre automático de una puerta y el comportamiento de los
enemigos (guardián, errante y rastreador). Después se pidió el motor Partida por 
trozos y la acción del jugador.

**Para qué se usó:** Verificar la integración, escribir la decisión del turno de
los enemigos, la acción del jugador y el primer trozo del motor Partida, y
redactar el texto de las decisiones de diseño del rastro y de la agenda.


### 2026-10-09 — Claude (Sonnet 5, claude.ai)
**Prompt (resumido):** Se pidió continuar el motor Partida con el segundo trozo
(movimiento entre salas, abrir puertas con llave, trampas, cierre automático y
victoria), probándolo con la cripta real guardada en fixtures/. Después se pidió 
el tercer trozo (atacar, recoger, soltar, equipar y usar objetos). Después se pidió 
corregir objetos_suelo en la vista y revisar el código sin uso del modelo. Después 
se pidió el retroceso completo (pergamino), empezando por los ganchos de inversa de 
los objetos del modelo. Después se pidió conectar el retroceso a Partida y la 
acción del pergamino.

**Para qué se usó:** Escribir y verificar el movimiento, las puertas y las
trampas del motor, y redactar las decisiones de diseño correspondientes.