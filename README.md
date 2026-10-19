# Cripta

Juego de mazmorra por turnos, hecho en Python para el curso Estructuras de Datos (II ciclo 2026). La mazmorra (la "cripta") no viene dentro del programa: se descarga de un **API REST** (un servidor web que entrega los datos en formato JSON) con un **presupuesto** limitado de solicitudes por partida. El juego avanza con un **reloj virtual**: un contador de tiempo propio del juego, que no depende de la hora real.

El proyecto usa estructuras de datos propias (montículo para la agenda de eventos, listas enlazadas, pila, cola circular, vector ordenado) y sigue la arquitectura **MVC** (modelo, vista y controlador separados). Las decisiones de diseño y sus mediciones están en `docs/DecisionesDiseño.md`.

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
| `py -m cripta --replay datos/partida.log` | Reproduce una partida guardada, sin interfaz (sección 5). |
| `py -m cripta --bench` | Corre las mediciones de rendimiento, sin interfaz (sección 6). |
| `py -m cripta --help` | Muestra la ayuda de las banderas. |

Las banderas se pueden combinar, por ejemplo `py -m cripta --offline --cache-size 10`.

**Términos:**

- **Catálogo:** la lista de "fichas" del juego (cada tipo de objeto, enemigo o trampa, con sus estadísticas). El juego las pide al API por lotes y las guarda en una **caché**: una copia local para no volver a pedirlas.
- **Fixtures:** archivos JSON con respuestas reales del API, guardados tal como llegaron, para jugar y probar sin red. Incluyen las cuatro criptas publicadas: `cripta-01` ("Osario menor", 6 salas), `cripta-02` (20 salas), `cripta-03` (40 salas) y `cripta-04` (50 salas). El formato está en `docs/FORMATO_OFFLINE.md`; para regenerar una cripta con internet: `py -m scripts.generar_fixtures cripta-02` (cambiando el id).
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
| `guardar` | Guarda la partida en `datos/partida.sav`. |
| `cargar` | Reemplaza la partida actual por la guardada (pide confirmación). Se usa desde dentro de una partida. |
| `salir` | Vuelve al menú principal (pide confirmación; lo no guardado se pierde). |

`Ctrl+C` o fin de entrada (`Ctrl+Z` y Enter en Windows, `Ctrl+D` en Linux) equivalen a salir.

Cada acción tiene un costo de tiempo (mover, atacar y esperar cuestan más que recoger o soltar) y los enemigos actúan según ese mismo reloj. La pantalla muestra la sala, sus salidas, los enemigos, los objetos del suelo, la vida, los efectos activos, el inventario, un minimapa y los últimos 20 mensajes. Al terminar (victoria o derrota) se puede escribir un nombre para la tabla de puntajes.

## 5. Reproducir una partida (`--replay`)

Cada partida escribe una **bitácora** en `datos/partida.log`: un archivo de texto con una línea por acción aceptada y, en la primera línea, la cripta, su versión, la versión del catálogo y la **semilla** (el número que fija el azar del combate; con la misma semilla y las mismas acciones el resultado es idéntico).

```
py -m cripta --replay datos/partida.log
py -m cripta --offline --replay datos/partida.log
```

El replay vuelve a ejecutar las acciones, sin interfaz ni preguntas, e imprime cada paso y el desenlace. Usa la red, salvo que se agregue `--offline` (que solo sirve si la partida fue en una cripta guardada en `fixtures/`). Si la versión de la cripta o del catálogo cambió desde que se jugó, o la bitácora está marcada como parcial, no la reproduce y explica por qué: con otros datos el resultado ya no sería el mismo.

Al guardar, el juego también copia la bitácora en `datos/partida.sav.log`, de modo que una partida cargada se puede seguir reproduciendo desde el principio.

**Bitácoras de ejemplo.** En `docs/ejemplos/` hay tres partidas ya jugadas que se reproducen sin red, sin necesidad de jugar antes:

```
py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log
py -m cripta --offline --replay docs/ejemplos/partida_cripta-03.log
py -m cripta --offline --replay docs/ejemplos/partida_cripta-04.log
```

| Archivo | Qué muestra |
|---|---|
| `partida_cripta-02.log` | Combate con una rata: el daño tiene una parte al azar, y el replay lo repite igual porque usa la misma semilla. |
| `partida_cripta-03.log` | Uso del pergamino de retroceso: deshace el último movimiento y el tiempo vuelve atrás. |
| `partida_cripta-04.log` | Puerta abierta con llave, recorrido por las cámaras ocultas y cierre automático de la puerta. |

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

- `--solo` corre solo las cargas nombradas: `agenda`, `cache`, `disco`, `inventario`, `historial`, `ordenamiento`, `guardado`, `ciclo`, `partida`, `solicitudes`.
- `--escala X` multiplica el tamaño de las cargas (por defecto 1; con 5 las mediciones son más finas pero tardan más).
- `--markdown ARCHIVO` además escribe la tabla de resultados en ese archivo.

**Código de salida:** `0` todo cumple el límite de 20 ms por ciclo de eventos · `1` alguna medición de `ciclo` o `partida` dice NO CUMPLE · `2` se pidió una carga que no existe.

> Con la escala por defecto, la carga `partida` incluye una cripta artificial de 400 salas, que supera los 20 ms y por eso `--bench` completo termina con código 1. Es un límite conocido y documentado (§4.1 del Documento de Decisiones): las criptas reales son mucho más pequeñas y cumplen.

## 7. Archivos que genera el juego

Todo se escribe en la carpeta `datos/`, que se crea sola y **no se sube a git**:

| Ruta | Contenido |
|---|---|
| `datos/cache/` | Copia en disco de las fichas del catálogo y del contenido de las salas, para no volver a descargarlos. |
| `datos/puntajes/` | Tabla de puntajes (`puntajes.json`) con los resultados de todas las criptas. |
| `datos/partida.sav` | Partida guardada, en formato binario propio. |
| `datos/partida.sav.log` | Bitácora de la partida guardada (la que se usa al cargarla). |
| `datos/partida.log` | Bitácora de la partida en curso (la que lee `--replay`). |

Borrar `datos/` deja el juego como recién instalado: se pierden los puntajes y la partida guardada, y la caché se vuelve a llenar en la siguiente partida.

## 8. Pruebas

Las pruebas usan `unittest`, que viene con Python (no hace falta instalar nada más):

```
py -m unittest discover -s tests -t .
```

- `discover` busca todos los archivos `test_*.py`; `-s tests` indica la carpeta donde buscar y `-t .` que la raíz del proyecto es la carpeta actual (así funcionan los `import cripta...`).
- Al final debe aparecer `OK`. Ninguna prueba usa la red: usan clientes falsos y criptas generadas (`tests/cliente_falso.py`, `tests/cripta_artificial.py`).
- Una sola carpeta o un solo archivo: `py -m unittest discover -s tests/estructuras -t .` o `py -m unittest tests.servicios.test_servicio_replay -v` (`-v` muestra el nombre de cada prueba).

## 9. Estructura del proyecto

```
cripta/
├── __main__.py        arranque y banderas
├── constantes.py      números del juego y de la red en un solo lugar
├── excepciones.py     errores propios
├── modelo/            reglas del juego (sin red, sin pantalla)
├── controlador/       traduce comandos en acciones
├── vista/             pantalla de consola
├── servicios/         une modelo e infraestructura: partida, catálogo, precarga, replay, bench
├── infraestructura/   cliente HTTP y offline, contador de solicitudes, caché, guardado, bitácora, puntajes
├── estructuras/       estructuras de datos y ordenamientos propios
├── dto/               conversión de las respuestas JSON del API a objetos
└── bench/             cargas sintéticas de --bench
fixtures/              respuestas del API guardadas para --offline (las 4 criptas publicadas)
scripts/               generar_fixtures.py y prueba_api.py (prueba rápida del API)
tests/                 pruebas, por capa
docs/                  Documento de Decisiones, bitácora, contrato de la partida, formato offline
└── ejemplos/          bitácoras de ejemplo para --replay
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