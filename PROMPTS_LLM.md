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