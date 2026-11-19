# Cripta

Juego de mazmorra por turnos, hecho en Python para el curso Estructuras de Datos (II ciclo 2026). La mazmorra (la "cripta") no viene dentro del programa: se descarga de un **API REST** (un servidor web que entrega los datos en formato JSON) con un **presupuesto** limitado de solicitudes por partida. El juego avanza con un **reloj virtual**: un contador de tiempo propio del juego, que no depende de la hora real.

El proyecto usa estructuras de datos propias (montículo para la agenda de eventos, listas enlazadas, pila, cola circular, vector ordenado) y sigue la arquitectura **MVC** (modelo, vista y controlador separados). Las decisiones de diseño y sus mediciones están en `DECISIONES.md`.

---

## Proceso de desarrollo con Spec Kit

El desarrollo de la Parte II se realizó siguiendo la metodología dirigida por especificaciones con **Spec Kit v1.2.3**.

### Agentes utilizados

- **Codex CLI** (0.167.2, 0.169.0 y 0.170.0) con GPT-6 Luna y GPT-6.2 Sol.
- **Antigravity CLI** (1.5.3 y 1.5.4) con Gemini, Gemini 3.8 Flash, Claude Sonnet 4.6 y Claude Sonnet 4.6 Thinking.
- **Claude Code** con Sonnet 5.5.
- **Claude en la web y en las apps** con Sonnet 5 y Sonnet 5.5 en la web, y Opus 5 y Opus 5.5 en las apps.

### Flujo de trabajo

El ciclo de desarrollo de cada capacidad siguió las fases de Spec Kit:
1. **specify**: especificación de requisitos funcionales y criterios de éxito en lenguaje natural
2. **clarify**: aclaración de ambigüedades y resolución de dudas sobre el enunciado
3. **plan**: diseño de arquitectura, contratos de interfaces y decisiones técnicas
4. **tasks**: desglose ordenado de tareas con dependencias y fases de implementación
5. **analyze**: verificación de consistencia entre especificación, plan y tareas
6. **implement**: implementación del código y pruebas asociadas guiada por tareas

### Capacidades desarrolladas

Cada capacidad cuenta con su carpeta propia dentro de `specs/`:
- `specs/001-terreno-cazador/`: 001 terreno y cazador
- `specs/002-niebla-ir-a/`: 002 niebla de guerra e ir a
- `specs/003-resolubilidad/`: 003 resolubilidad
- `specs/004-linea-de-tiempo/`: 004 línea de tiempo

### Ubicación de artefactos

- `specs/NNN-.../`: especificación (`spec.md`), plan (`plan.md`) y lista de tareas (`tasks.md`) de cada capacidad
- `prompts/p2/`: prompts preparados para cada corrida y fase del proyecto
- `PROMPTS_LLM.md`: bitácora completa de los prompts utilizados con los asistentes de IA
- `DECISIONES.md`: justificación de diseño de cada estructura y algoritmo con sus mediciones empíricas
- `.specify/memory/constitution.md`: principios de gobernanza, prohibiciones y reglas del proyecto
- [docs/TRAZABILIDAD.md](docs/TRAZABILIDAD.md): matriz que vincula cada requisito con su escenario, tarea, código y prueba

---

## 1. Requisitos

- **Python 3.11 o más reciente.** Se probó con 3.12 y 3.14.
- **Internet**, solo para jugar en línea. Con `--offline` el juego funciona sin conexión (ver la sección 3).
- **Una consola de al menos 113 columnas de ancho.** La pantalla del juego se dibuja con texto y mide exactamente eso; si la ventana es más angosta, las líneas se parten y el dibujo se desordena.

## 2. Instalación

Desde la carpeta raíz del proyecto (la que contiene `cripta/` y `requirements.txt`):

```
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

- Las dos primeras líneas crean y activan un **entorno virtual** (una copia aislada de Python para este proyecto). Son opcionales, pero evitan mezclar paquetes con otros proyectos. En Linux o macOS la activación es `source .venv/bin/activate`.
- La única dependencia que usa el programa es `requests`, la librería que hace las solicitudes HTTP. Se necesita instalada también para jugar con `--offline`.

> **`py` o `python`:** En Windows el comando `py` abre el Python instalado. En Linux y macOS se usa `python3` (o `python`, según la instalación). Todos los comandos de este documento funcionan igual cambiando `py` por el que corresponda.

## 3. Cómo ejecutar

Todos los comandos se escriben **desde la carpeta raíz del proyecto**. `-m cripta` le dice a Python que ejecute el paquete `cripta` como programa.

| Comando | Qué hace |
|---|---|
| `py -m cripta` | Juega en línea: descarga la cripta del API. |
| `py -m cripta --offline` | Juega sin conexión, con las respuestas del API guardadas en `fixtures/`. |
| `py -m cripta --cache-size 50` | Cambia cuántas fichas del catálogo se guardan en memoria (por defecto 25; debe ser un entero mayor o igual a 1). |
| `py -m cripta --checkpoint-cada 50` | Cada cuántas acciones se guarda un punto de control de la línea de tiempo (por defecto 50, debe ser un entero mayor o igual a 1). Un valor inválido se rechaza al iniciar, con su motivo, y la partida no inicia. |
| `py -m cripta --replay datos/partida.log` | Reproduce una partida guardada, sin interfaz (sección 5). |
| `py -m cripta --replay datos/partida.log --hasta 150` | Reproduce la bitácora completa y además muestra el estado de la partida en el instante 150 (sección 5). |
| `py -m cripta --verificar cripta-02` | Verifica si la cripta se puede ganar, sin iniciar una partida y sin interfaz (sección 4.1). |
| `py -m cripta --forzar` | Permite iniciar una partida aunque la cripta elegida no sea resoluble (sección 4.1). |
| `py -m cripta --bench` | Corre las mediciones de rendimiento, sin interfaz (sección 6). |
| `py -m cripta --help` | Muestra la ayuda de las banderas. |

Las banderas se pueden combinar, por ejemplo `py -m cripta --offline --cache-size 10`.

**Términos:**

- **Catálogo:** la lista de "fichas" del juego (cada tipo de objeto, enemigo o trampa, con sus estadísticas). El juego las pide al API por lotes y las guarda en una **caché**: una copia local para no volver a pedirlas.
- **Fixtures:** archivos JSON con respuestas reales del API, guardados tal como llegaron, para jugar y probar sin red. `fixtures/` tiene de `cripta-02` a `cripta-06` del servidor actual; `cripta-01` ("Osario menor", 6 salas) queda congelada con el catálogo anterior en `tests/datos/` y no se regenera. El formato está en `docs/FORMATO_OFFLINE.md`; para regenerar una cripta con internet: `py -m scripts.generar_fixtures cripta-02` (cambiando el id).
- Al salir del juego se imprime un **reporte final**: solicitudes usadas contra el presupuesto, aciertos y fallos de la caché del catálogo, y cuántas salas se trajeron por red o desde disco.

## 4. Cómo se juega

### Menú principal

`1` iniciar partida · `2` créditos · `3` ver puntajes · `4` salir (también se puede escribir la palabra). Al iniciar se elige la cripta por su número; `0` vuelve al menú.

### Comandos dentro de la partida

Se escribe el comando y se pulsa Enter. Mayúsculas y minúsculas dan igual. Los números (`#`) son la posición que muestra la pantalla, **empezando en 1**.

| Comando | Qué hace |
|---|---|
| `n`, `s`, `e`, `o` (o `mover n`) | Moverse al norte, sur, este u oeste. |
| `abrir <dir>` | Abrir la puerta en esa dirección (algunas piden una llave en el inventario). |
| `atacar <#>` | Atacar al enemigo número `#` de la sala. |
| `esperar` | Dejar pasar el tiempo sin hacer nada. |
| `recoger <#>` | Recoger el objeto número `#` del suelo. |
| `sig` / `ant` | Mover el **cursor** del inventario al objeto siguiente o anterior. No gasta tiempo. |
| `usar`, `equipar`, `soltar` | Actúan sobre el objeto que marca el cursor. |
| `ordenar peso` / `valor` / `nombre` | Muestra el inventario ordenado por ese criterio. No cambia el orden real del inventario. |
| `pergamino [1-5]` | Deshace las últimas acciones: cada pergamino deshace una (por defecto 1, máximo 5). Requiere tener pergaminos en el inventario. |
| `mapa` | Muestra el mapa conocido con las salas exploradas y sus conexiones visibles. No gasta tiempo. |
| `ir a <sala>` | Viaja automáticamente a una sala conocida siguiendo la ruta más corta por territorio ya explorado. |
| `historia <t>` | Muestra el estado de la partida en el instante `t` del reloj (por ejemplo `historia 150`). Si en `t` el jugador debía decidir, muestra el estado justo antes de esa decisión. No gasta tiempo, no se anota en la bitácora y no cambia la partida. |
| `historia #<k>` | Muestra el estado justo antes de la acción número `k` (por ejemplo `historia #3`). Solo cuentan las acciones ejecutadas y vigentes, desde 1, y el pergamino no se numera. No gasta tiempo ni cambia la partida. |
| `guardar` | Guarda la partida en `datos/partida.sav`. |
| `cargar` | Reemplaza la partida actual por la guardada (pide confirmación). Se usa desde dentro de una partida. |
| `salir` | Vuelve al menú principal (pide confirmación; lo no guardado se pierde). |

`Ctrl+C` o fin de entrada (`Ctrl+Z` y Enter en Windows, `Ctrl+D` en Linux) equivalen a salir.

`historia` muestra siete grupos de datos: el reloj, la sala, la vida y las estadísticas, el inventario, los efectos activos, los enemigos de la sala con su vida y el mapa conocido en ese momento. Se rechaza, con su motivo y sin ningún efecto, un instante posterior al reloj actual, un número de acción que no existe (cero, o mayor que la cantidad de acciones vigentes) o un argumento mal escrito. Después de usar un pergamino, las acciones que revirtió ya no se pueden consultar.

Cada acción tiene un costo de tiempo (mover, atacar y esperar cuestan más que recoger o soltar) y los enemigos actúan según ese mismo reloj. La pantalla muestra la sala, sus salidas, los enemigos, los objetos del suelo, la vida, los efectos activos, el inventario, un minimapa y los últimos 20 mensajes. Al terminar (victoria o derrota) se puede escribir un nombre para la tabla de puntajes.

### 4.1 Resolubilidad de la cripta (`--verificar` y `--forzar`)

Una cripta es **resoluble** cuando se puede obtener la llave de la salida y llegar a la sala de salida respetando las puertas que piden llave. El programa lo comprueba antes de jugar.

**Al iniciar una partida** se muestra el reporte de resolubilidad de la cripta elegida, dentro de un recuadro:

- Si es **resoluble**: indica `Estado: RESOLUBLE` y la secuencia en que se obtienen las llaves. Después la partida arranca con normalidad.
- Si **no es resoluble**: indica `Estado: NO RESOLUBLE`, el motivo, las llaves no obtenibles, las puertas bloqueadas (sala de origen, dirección, sala de destino y la llave que piden) y, si las hay, las dependencias circulares entre llaves. Sin `--forzar` la partida no inicia y se vuelve al menú. Con `--forzar` se agrega al reporte la línea `ADVERTENCIA: el inicio de la partida fue forzado.` y la partida inicia.

**Verificar sin jugar.** `--verificar` recibe el id de la cripta, imprime el mismo reporte y termina, sin crear la interfaz del juego. Se puede combinar con `--offline`:

```
py -m cripta --verificar cripta-02
py -m cripta --offline --verificar cripta-02
```

**Código de salida de `--verificar`:** `0` la verificación terminó (la cripta puede ser resoluble o no, el reporte lo dice) · `1` los datos de la cripta son inválidos (se explica el motivo) · `2` error externo (red, presupuesto de solicitudes agotado, archivo dañado, etc.).

## 5. Reproducir una partida (`--replay`)

Cada partida escribe una **bitácora** en `datos/partida.log`: un archivo de texto con una línea por acción aceptada y, en la primera línea, la cripta, su versión, la versión del catálogo y la **semilla** (el número que fija el azar del combate; con la misma semilla y las mismas acciones el resultado es idéntico).

```
py -m cripta --replay datos/partida.log
py -m cripta --offline --replay datos/partida.log
```

El replay vuelve a ejecutar las acciones, sin interfaz ni preguntas, e imprime cada paso y el desenlace. Usa la red, salvo que se agregue `--offline` (que solo sirve si la partida fue en una cripta guardada en `fixtures/`). Si la versión de la cripta o del catálogo cambió desde que se jugó, o la bitácora está marcada como parcial, no la reproduce y explica por qué: con otros datos el resultado ya no sería el mismo.

Al guardar, el juego también copia la bitácora en `datos/partida.sav.log`, de modo que una partida cargada se puede seguir reproduciendo desde el principio.

**Consultar un instante con `--hasta`.** Con `--hasta t` el replay reproduce la bitácora completa, sin interfaz, y después muestra el estado en el instante `t` con el mismo componente que el comando `historia <t>` del juego. `t` es un entero mayor o igual a 0 y `--hasta` solo se acepta junto con `--replay`. Si la partida termina antes de `t`, muestra el estado final e indica que terminó antes.

```
py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log --hasta 150
py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log --hasta 999999
```

La primera muestra la sección `Historia t=150` con los siete grupos de datos. La segunda muestra el estado final e indica `terminó antes de t=999999`. Esa bitácora incluye un pergamino, así que la consulta ya no ve la acción que el pergamino revirtió.

**Bitácoras de ejemplo.** En `docs/ejemplos/` hay tres partidas ya jugadas que se reproducen sin red, sin necesidad de jugar antes:

```
py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log
py -m cripta --offline --replay docs/ejemplos/partida_cripta-04.log
py -m cripta --offline --replay docs/ejemplos/partida_cripta-06.log
```

| Archivo | Qué muestra |
|---|---|
| `partida_cripta-02.log` | Salidas con costos distintos (60, 100, 150, 80, 250): cada movimiento hace avanzar el tiempo según el costo de la salida. Una rata ataca al pasar, y al final el pergamino de retroceso deshace un movimiento de costo 120 y el tiempo vuelve atrás. |
| `partida_cripta-04.log` | Puerta abierta con llave, recorrido por las cámaras ocultas y cierre automático de la puerta. |
| `partida_cripta-06.log` | Cazador: el jugador despierta a un espectro acechador, se aleja una sala y el espectro lo sigue por la ruta de costo mínimo. También muestra una salida de costo 200 que cuesta el doble de tiempo que una de 100. |

Las tres terminan con código de salida `0` (reproducción fiel).

**Código de salida** (el número que el programa devuelve al sistema al terminar; sirve para scripts):
`0` la reproducción fue fiel · `1` no fue fiel (se explica el motivo) · `2` error externo (archivo inexistente, red, etc.).

## 6. Mediciones (`--bench`)

```
py -m cripta --bench
py -m cripta --bench --solo cache ordenamiento
py -m cripta --bench --escala 5 --markdown resultados.md
```

Corre **cargas sintéticas** (datos generados con una semilla fija, sin red ni interfaz) que miden cada subsistema y, cuando corresponde, también la alternativa descartada, para comparar. Son la evidencia citada en el Documento de Decisiones.

- `--solo` corre solo las cargas nombradas: `agenda`, `cache`, `disco`, `inventario`, `historial`, `historial_cazadores`, `ordenamiento`, `guardado`, `ciclo`, `partida`, `solicitudes`, `ruta_cazador`, `invalidacion`, `ciclo_referencia`, `niebla_rutas`, `linea_tiempo`, `resolubilidad`, `resolubilidad_cota`.
- `--escala X` multiplica el tamaño de las cargas (por defecto 1; con 5 las mediciones son más finas pero tardan más).
- `--markdown ARCHIVO` además escribe la tabla de resultados en ese archivo.

**Código de salida:** `0` todo cumple el límite de 20 ms por ciclo de eventos · `1` alguna medición de `ciclo`, `partida` o `ciclo_referencia` dice NO CUMPLE · `2` se pidió una carga que no existe.

> La carga `partida` incluye una cripta artificial de 400 salas. En la Parte I superaba los 20 ms por las pasadas completas del recolector de memoria de Python, y `--bench` completo terminaba con código 1. Desde la Parte II el juego congela la memoria viva después de cada acción (`gc.freeze()`) y esa carga cumple, así que `--bench` completo termina con código 0. Las mediciones de antes y después están en `docs/bench/` y se explican en la sección de la capacidad 001 de `DECISIONES.md`.

## 7. Archivos que genera el juego

Todo se escribe en la carpeta `datos/`, que se crea sola y **no se sube a git**:

| Ruta | Contenido |
|---|---|
| `datos/cache/` | Copia en disco de las fichas del catálogo y del contenido de las salas, para no volver a descargarlos. |
| `datos/puntajes/` | Tabla de puntajes (`puntajes.json`) con los resultados de todas las criptas. |
| `datos/partida.sav` | Partida guardada, en formato binario propio. Usa la versión 2 del formato, que guarda también la línea de tiempo. Un archivo guardado de la Parte I (versión 1) se rechaza al cargar con un error claro de versión, sin modificarlo ni borrarlo, y no se migra. |
| `datos/partida.sav.log` | Bitácora de la partida guardada (la que se usa al cargarla). |
| `datos/partida.log` | Bitácora de la partida en curso (la que lee `--replay`). |

Borrar `datos/` deja el juego como recién instalado: se pierden los puntajes y la partida guardada, y la caché se vuelve a llenar en la siguiente partida.

## 8. Pruebas

Las pruebas usan `unittest`, que viene con Python (no hace falta instalar nada más).

Para correr la suite completa de pruebas unitarias y de integración:

```
py -m unittest discover -s tests -t .
```

Para correr únicamente la suite de pruebas de aceptación:

```
py -m unittest discover -s tests/aceptacion -t .
```

- `discover` busca todos los archivos `test_*.py`; `-s tests` indica la carpeta donde buscar y `-t .` que la raíz del proyecto es la carpeta actual (así funcionan los `import cripta...`).
- Al final debe aparecer `OK`. Ninguna prueba usa la red: usan clientes falsos y criptas generadas (`tests/cliente_falso.py`, `tests/cripta_artificial.py`).
- Una sola carpeta o un solo archivo: `py -m unittest discover -s tests/estructuras -t .` o `py -m unittest tests.servicios.test_servicio_replay -v` (`-v` muestra el nombre de cada prueba).
- Las pruebas de rendimiento no se ejecutan con `unittest` sino mediante el comando `py -m cripta --bench` (sección 6).

## 9. Estructura del proyecto

```
cripta/
├── __main__.py        arranque y banderas
├── constantes.py      números del juego y de la red en un solo lugar
├── excepciones.py     errores propios
├── modelo/            reglas del juego (sin red, sin pantalla)
│   ├── linea_tiempo.py          línea de tiempo con puntos de control y consultas históricas
│   ├── conocimiento_jugador.py  mapa conocido y niebla de guerra por exploración
│   └── ruta_conocida.py         búsqueda de rutas sobre territorio explorado para ir a
├── controlador/       traduce comandos en acciones
├── vista/             pantalla de consola
├── servicios/         une modelo e infraestructura: partida, catálogo, precarga, replay, bench
├── infraestructura/   cliente HTTP y offline, contador de solicitudes, caché, guardado, bitácora, puntajes
├── estructuras/       estructuras de datos y ordenamientos propios
├── dto/               conversión de las respuestas JSON del API a objetos
└── bench/             cargas sintéticas de --bench
fixtures/              respuestas del API para --offline (cripta-02 a cripta-06). tests/datos/ tiene cripta-01 congelada
scripts/               generar_fixtures.py, prueba_api.py y revisar_prohibidos.py (auditoría de estructuras prohibidas, se corre con py -m scripts.revisar_prohibidos)
tests/                 pruebas, por capa (incluye tests/aceptacion/ para pruebas de aceptación)
docs/                  contrato de la partida, formato offline, bitácora, mapa de código, documentación del API, mediciones, ejemplos y enunciados
├── bench/             mediciones y reportes de rendimiento
└── ejemplos/          bitácoras de ejemplo para --replay
specs/                 especificaciones, planes y tareas de cada capacidad (001 a 004)
prompts/               prompts ejecutados en cada etapa del desarrollo
DECISIONES.md          decisiones de diseño y mediciones
PROMPTS_LLM.md         prompts usados con asistentes de IA
```

## 10. Problemas comunes

| Problema | Causa y solución |
|---|---|
| `No module named cripta` | El comando no se ejecutó desde la carpeta raíz del proyecto. |
| `No module named requests` | Falta `py -m pip install -r requirements.txt` (o el entorno virtual no está activado). |
| La pantalla sale desordenada | La consola tiene menos de 113 columnas: ensanchar la ventana o reducir la letra. |
| Error de conexión al iniciar | Sin internet o el API no responde: usar `--offline`. |
| `--replay` dice que no es fiel | La versión de la cripta o del catálogo cambió desde que se jugó, la bitácora es parcial o alguna acción ya no se acepta; el informe dice cuál. |
