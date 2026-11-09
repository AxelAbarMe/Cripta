# MAPA_CODIGO.md — Mapa del código de Cripta (Parte I) · versión completa

> **Propósito:** base para los `plan.md` de la Parte II. Describe **qué existe hoy** en el repositorio, dónde está y qué puntos hay que tocar para las 4 capacidades nuevas.
> **Cómo se generó:** lectura directa del código de `Cripta.zip` (≈ 10 300 líneas de Python, 78 módulos en `cripta/`, 27 archivos de prueba). Las afirmaciones citan archivo y clase/función. Los puntos que antes estaban marcados con ⚠️ ya se verificaron (ver §9, ítems 3, 4 y 13). Lo único que queda sin ejecutar es lo que la P2 aún no define (por ejemplo, el comportamiento de un cazador sin `rango`).
> **Para agentes:** no asumas módulos que no estén aquí. Si necesitas algo que no aparece, búscalo en el repo antes de inventarlo.

---

## 0. Estado verificado (línea base)

| Verificación | Resultado |
|---|---|
| `python -m unittest discover -s tests -t .` (Python 3.12.3) | **222 pruebas, OK** (0,76 s). Requiere `fixtures/` presente |
| `--offline --replay docs/ejemplos/partida_cripta-02/03/04.log` | los tres terminan con código **0** |
| `--bench --solo ciclo` | 100 actores: 1,9 ms · 300: 7,0 ms · 600 actores (1 200 eventos): **15,1 ms** (límite 20 ms) |
| `--bench --solo agenda` | heap vs lista lineal: 1,2× / 4,8× / 8,6× más rápido con 100 / 500 / 2 000 eventos pendientes |
| `--bench --solo historial` | inversas: 2,6 µs/acción; copia completa (descartada): 1 447 µs/acción (556× más lenta) |
| Fixtures | `cripta-01` 6 salas · `-02` 20 · `-03` 40 · `-04` 50 (presupuestos 9 / 23 / 42 / 52). Todas son criptas de la Parte I (sin `costo`, sin cazadores) |

> ⚠️ El margen del ciclo de eventos es **estrecho** (15 ms de 20 ms con 600 actores *sin* búsqueda de rutas). Los cazadores agregarán trabajo por turno: el plan de 001 debe medirlo desde el principio.

---

## 1. Árbol del proyecto

```
Cripta/
├── cripta/
│   ├── __main__.py            arranque, banderas (argparse), cableado de dependencias
│   ├── constantes.py          costos de acciones, RASTRO_ANTIGUEDAD_MAX=400, RETROCESO_MAX_ACCIONES=5,
│   │                          BITACORA_MAX_MENSAJES=20, MAX_ELEMENTOS_POR_LOTE=10, direccion_opuesta()
│   ├── excepciones.py         CriptaError y derivadas (ApiError, Limite, FormatoIncompatible, Bitacora, ...)
│   ├── modelo/                reglas del juego (sin red, sin archivos, sin pantalla)
│   ├── controlador/           controlador_cripta.py
│   ├── vista/                 vista_base.py (contrato) + vista_consola.py (ASCII, 113 columnas)
│   ├── servicios/             une modelo + infraestructura
│   ├── infraestructura/       red, disco, caché, guardado, bitácora, puntajes
│   ├── estructuras/           estructuras de datos y ordenamientos propios
│   ├── dto/                   JSON del API -> objetos inmutables
│   └── bench/                 cargas_bench.py (cargas sintéticas de --bench)
├── tests/                     unittest por capa (+ cliente_falso.py, cripta_artificial.py)
├── docs/                      DecisionesDiseño.md, CONTRATO_PARTIDA.md, FORMATO_OFFLINE.md, Bitacora.md, ejemplos/*.log
├── fixtures/                  respuestas del API guardadas (--offline)
├── scripts/                   generar_fixtures.py, prueba_api.py
├── datos/                     (generado, ignorado por git) cache/, puntajes/, partida.sav, partida.log
├── PROMPTS_LLM.md  README.md  requirements.txt (requests>=2.31)
```

> Nota: en el zip el archivo aparece como `DecisionesDise#U00f1o.md` (artefacto de codificación del zip); en el repo se llama `docs/DecisionesDiseño.md`. La Parte II pide `DECISIONES.md` **en la raíz**.

---

## 2. Capa por capa

### 2.1 `cripta/modelo/` — reglas del juego

| Módulo | Qué contiene |
|---|---|
| `partida.py` (674 líneas) | **`Partida`: el motor.** Acciones del jugador, turnos de enemigos, activación, trampas, puertas, victoria/derrota, guardado/carga, vista. Es la clase más grande y con más acoplamiento (ver §8) |
| `reloj.py` | `RelojEventos` (reloj virtual + agenda sobre `HeapMinimo`), `EventoProgramado`, `calcular_intervalo()`, `calcular_tiempo_reprogramado()` |
| `reversible.py` | Base `Reversible`: intercepta `__setattr__` y registra la inversa (closure) del valor pisado |
| `historial_retroceso.py` | `HistorialRetroceso`: una `Pila` de closures por intervalo; máx. 5 intervalos |
| `actor.py` / `jugador.py` / `enemigo.py` | `Actor(Reversible)`: vida, ataque_base, defensa_base, velocidad, sala_actual, `tiempo_siguiente`, `evento_pendiente`, `veneno_activo`. `Jugador` añade `Inventario`. `Enemigo` añade `instancia_id`, `tipo_catalogo`, `comportamiento`, `suelta`, `activo` |
| `comportamiento_enemigo.py` | `decidir_accion_enemigo()` → `("atacar"\|"mover"\|"esperar", direccion)`; `_decidir_errante`, `_decidir_rastreador` |
| `sala.py` | `EstadoPuertas(Reversible)` (4 booleanos), `Sala(Reversible)`: esqueleto + puertas + contenido + `rastro_ultima_visita` + `enemigos_dormidos/activos` |
| `cripta_mapa.py` | `CriptaMapa`: `VectorOrdenado` de salas por id; `vecinos()`, `puerta_transitable()`, `datos_de_puerta()`, `abrir/cerrar_puerta()`, `sincronizar_puertas()` |
| `efectos.py` | `EfectoVeneno`, `EfectoCambioVelocidad`, `EfectoAntorcha`, `EfectoRegeneracion`, `EfectoTrampa`, `EfectoCierrePuerta` |
| `inventario.py` | `Inventario(Reversible)` sobre `ListaDobleEnlazada` con cursor; `vista_ordenada()` usa `ordenar_auto` |
| `combate.py` | `calcular_daño()` / `atacar()` con `azar.randint(0,4)` |
| `accion.py` | `Accion` (dataclass inmutable). Tipos: `mover, abrir, atacar, esperar, recoger, usar, equipar, soltar, pergamino` |
| `bitacora_mensajes.py` | `BitacoraMensajes` sobre `ColaCircular(20)` |
| `persistencia_modelo.py` | `crear_estado()` / `restaurar_jugador()` / `restaurar_sala()`: modelo ⇄ datos planos |
| `resultado_partida.py` | `VistaPartida`, `SalidaVista`, `EnemigoVista`, `ResultadoAccion`, `ResumenPuntaje` |
| `puntajes.py`, `trampa.py` | tabla de puntajes; `Trampa(Reversible)` (armada/desarmar/rearmar) |

### 2.2 `cripta/servicios/`

| Módulo | Responsabilidad |
|---|---|
| `servicio_partida.py` | `ServicioPartida`: **único que conoce cliente + caché + modelo**. `iniciar_nueva`, `ejecutar` (escribe en bitácora cada acción aceptada), `guardar`, `cargar`, `registrar_puntaje`, `reporte_final`. Consume `/criptas/{id}` y `/catalogo/version` en `_datos_basicos` |
| `servicio_precarga.py` | Esqueleto completo + contenido anticipado por lotes (BFS, radio 2, lotes de 10), hilo trabajador, incorporación determinista en orden de solicitud, población de enemigos dormidos (`preparar_sala`) |
| `servicio_catalogo.py` | Catálogo con caché en memoria (**LRU** sobre `ListaDobleEnlazada` + índice `VectorOrdenado`), recuperación desde disco, lotes de red de 10, fichas en uso protegidas |
| `servicio_replay.py` | `ServicioReplay.reproducir(ruta)` → `ResultadoReplay` |
| `servicio_bench.py` | `ServicioBench`, `ejecutar_bench_cli()`; código de salida 1 si `ciclo` o `partida` no cumplen 20 ms |
| `servicio_presupuesto.py` | reporte final del presupuesto de solicitudes |

### 2.3 `cripta/infraestructura/`

| Módulo | Responsabilidad |
|---|---|
| `puertos.py` | `Protocol`s: **`ClienteCripta`** (7 métodos, **sin `obtener_llaves`**) y `AlmacenDiscoPuerto` |
| `cliente_http.py` | `ClienteHttp`: UUID único por ejecución (`X-Cripta-Client-Id`), timeout 10 s, 429 con `time.sleep` y hasta 5 reintentos; **cada intento cuenta** y se revisa el presupuesto antes (`CriptaLimiteError`) |
| `cliente_offline.py` | `ClienteOffline`: mismo contrato leyendo `fixtures/` |
| `cliente_general.py` | `ClienteGeneral`: envoltorio que **serializa** las llamadas (seguro entre hilos) |
| `contador_solicitudes.py` | `ContadorSolicitudes` (presupuesto máximo, realizadas, restantes) |
| `cache.py` | `CacheDisco`: claves **con la versión dentro** (`catalogo.<ver>.<id>.json`, `cripta.<id>.<ver>.salas.<n>.json`, `…contenido.<sala>.json`); versión distinta = clave inexistente = fallo de caché (no se borra nada) |
| `almacen_disco.py` | `AlmacenDiscoArchivos` (leer/escribir/existe) |
| `guardado_binario.py` | `GuardadoBinario` (formato propio con `struct`), `guardar_json/cargar_json` (solo para comparar en bench) |
| `estado_guardado.py` | Datos planos del guardado: `EstadoPartida`, `JugadorGuardado`, `SalaGuardada`, `EnemigoGuardado`, `EventoGuardado`, `EstadoRNG`; constantes `EV_*` de tipos de evento |
| `partida_log.py` | `EscritorBitacoraPartida` / `LectorBitacoraPartida`, `diferencias_de_version()` |
| `puntajes_disco.py`, `serializacion.py`, `lotes.py` | tabla de puntajes en JSON; DTO→JSON; validación de lotes |

### 2.4 `cripta/dto/`

Un `dataclass(frozen=True, slots=True)` por tipo del API, con `desde_json()`. Relevantes para la P2:

- `SalidaDTO(sala_destino, cerrada, llave, cierre_automatico)` — **sin `costo`**.
- `SalaDTO(id, nombre, norte, sur, este, oeste)` con `salida(direccion)`.
- `EnemigoDTO(id, nombre, clase, vida_max, ataque, defensa, velocidad, comportamiento, suelta)` — **sin `rango`**.
- `entidad_desde_json()` despacha por `clase` (lanza `ValueError` si desconoce la clase).
- No existe DTO de `/llaves` (existe `llave_dto.py`, pero es la **ficha de catálogo** de una llave, no la ubicación).

### 2.5 `cripta/vista/` y `cripta/controlador/`

- `VistaBase` (ABC): `pedir_orden`, `mostrar_estado`, `mostrar_aviso`, `mostrar_error`, `confirmar`, `pedir_texto`, etc.
- `VistaConsola`: `_interpretar(partes)` convierte texto → `Orden(tipo, argumento)`; `_minimapa(vista)` dibuja **solo la sala actual y sus vecinas** (sala `@ id` + `N:id`, `S:id`...). Ancho fijo 113.
- `ControladorCripta`: `_procesar(orden, vista)` despacha (`siguiente/anterior`, `ordenar`, `guardar`, `cargar`, `pergamino`, o `_traducir` → `Accion`). Los números de la pantalla (empiezan en 1) se traducen a `instancia_id` / `ficha_id` / índice de inventario en `_traducir`. `_ERRORES = (CriptaError, FileNotFoundError, RuntimeError, ValueError)` se atrapan en `_intentar`.

---

## 3. Flujo de ejecución

### 3.1 Arranque (`__main__.main`)

1. `argparse` con `parse_known_args`: `--offline`, `--cache-size`, `--replay`, `--bench` (los argumentos restantes de `--bench` los interpreta `ejecutar_bench_cli`).
2. Construye `ContadorSolicitudes` → `ClienteHttp` o `ClienteOffline` → `ClienteGeneral` → `CacheDisco(datos/cache)` → `ServicioPartida`.
3. `--replay` → `ServicioReplay` (sin vista; códigos 0/1/2). `--bench` → sin vista. Otro caso → `ControladorCripta(servicio, VistaConsola(), ...)`.

### 3.2 Nueva partida (`ServicioPartida.iniciar_nueva`)

`obtener_general` (fija el presupuesto) → `obtener_version_catalogo` → `_armar`: crea `CriptaMapa`, `ServicioCatalogo`, `ServicioPrecarga`, `cargar_esqueleto(paginas)` (disco o red) → `Partida(...)` → `Partida.iniciar()` (sala inicial preparada, `marcar_visita(0)`, activa enemigos, programa turno del jugador en t=0).

### 3.3 Una acción del jugador (`Partida.ejecutar_accion`)

```
pergamino?  → _usar_pergamino()  (no abre intervalo, no registra, deshace_ultimo_intervalo)
si no:
  historial.iniciar_intervalo()
  _guardar_contadores()          # registra closure con (acciones, derrotados, antorcha, instancia, turno_listo, azar.getstate())
  _despachar(accion)             # _mover / _abrir / _atacar / _recoger / _soltar / _equipar / _usar / _esperar
      └─ _terminar_accion_jugador(costo)  → programa turno del jugador (calcular_intervalo)
             → _avanzar_hasta_turno_jugador()  # ejecuta eventos del reloj hasta que toque decidir
             → historial.cerrar_intervalo()
  si rechazada → descartar_intervalo_actual()  (sin tiempo, sin log)
```

`ServicioPartida.ejecutar` escribe en `partida.log` solo las acciones **aceptadas** (incluido `pergamino`).

### 3.4 Un turno de enemigo (`Partida._turno_enemigo`)

Si está muerto o la partida terminó → no hace nada (la muerte **no** cancela eventos uno a uno, salvo que `_matar_enemigo` cancele su `evento_pendiente`). Luego `decidir_accion_enemigo(enemigo, sala_jugador, mapa, azar, tiempo)` → ejecuta (`combate.atacar`, `_mover_enemigo`, o espera) y `_programar_turno_enemigo(enemigo, costo)` con **costo fijo** (`COSTO_ATACAR` / `COSTO_MOVER` / `COSTO_ESPERAR`).

### 3.5 Movimiento del jugador (`Partida._mover`)

Valida salida y puerta → `precarga.preparar_sala(destino)` **dentro de `sin_registrar()`** (espera la red si hace falta, sin tocar el reloj virtual) → `marcar_visita` en origen y destino → `jugador.sala_actual = destino` → `_activar_enemigos_de(destino)` → `precargar_desde(destino)` → `_activar_trampas_de(destino)` → victoria si la sala es `sala_salida` y la puerta cruzada exige `llave_salida` → `_terminar_accion_jugador(accion.costo_base)`.

---

## 4. Estructuras de datos propias (qué hay y dónde se usa)

| Estructura | Archivo | Se usa en |
|---|---|---|
| `HeapMinimo` | `estructuras/heap_min.py` | Agenda del `RelojEventos`. **Solo** tiene `insertar` y `eliminar_minimo` (devuelve `None` si está vacío); **no hay** `peek`, ni `__len__`, ni búsqueda/actualización por clave. Compara elementos con `<` (los `EventoProgramado` definen `__lt__` por `(tiempo, secuencia)`) |
| `VectorOrdenado(clave)` | `estructuras/vector.py` | **Índice por clave con búsqueda binaria** (sustituto del dict): `CriptaMapa._salas`, `_solicitadas`, `_pobladas`, `_indice_lote`, índice del catálogo, pendientes. `insertar` es O(n) (desplaza), `buscar/contiene` O(log n). API: `insertar, buscar, contiene, eliminar, elementos, __len__` |
| `ListaDobleEnlazada` | `estructuras/lista_doble_enlazada.py` | LRU del catálogo; orden real del inventario (cursor por nodo). `agregar`, `agregar_inicio`, `eliminar_nodo`, `mover_al_inicio` en O(1) |
| `Pila` | `estructuras/pila.py` | Un intervalo del historial = una `Pila` de closures (`pop()` devuelve `None` si está vacía) |
| `ColaCircular` | `estructuras/cola_circular.py` | Bitácora en pantalla (20 mensajes, sobrescribe el más antiguo) |
| `Cola` | `estructuras/cola.py` | Cola FIFO enlazada: BFS de la precarga, cola de lotes del hilo de red |
| `ListaEnlazada` | `estructuras/lista_enlazada.py` | Existe, sin uso relevante en el motor |
| Ordenamientos | `estructuras/ordenamientos.py` | `Ordenamiento` con insertion, merge, quick, bubble, selection, heap |
| Selector | `estructuras/ordenamiento_selector.py` | `ordenar_auto(lista, comparacion_costosa)`: elige inserción vs merge por `n` y desorden medido; umbrales 32 / 8 / 30 |

**No existe aún:** cola de prioridad indexable, estructura de grafo, algoritmo de rutas, estructura de conjunto, ni estructura de puntos de control.

> Reutilización para la P2: `HeapMinimo` puede servir como cola de prioridad de una búsqueda de rutas **si** se le agrega lo que falta (`__len__`/vacío, quizá `peek`), insertando pares comparables (p. ej. `(costo, sala_id)`); `VectorOrdenado` sirve de mapa `sala_id → dato` (distancias, estado de exploración) con búsqueda O(log n). Todo cambio a estas estructuras debe pasar por spec/plan.

---

## 5. Modelo de datos del juego

### 5.1 Salida, puerta y sala
- La geometría vive en `SalaDTO` (inmutable, del esqueleto). **El estado de las puertas** (abierta/cerrada) vive aparte en `Sala.puertas` (`EstadoPuertas`, 4 booleanos), por **ambos lados**: `CriptaMapa._fijar_puerta` cambia las dos salas; `sincronizar_puertas()` (se llama en `Partida.__init__`) iguala los dos lados.
- La **llave y el cierre automático** pueden venir marcados en un solo lado de la puerta: `CriptaMapa.datos_de_puerta()` mira los dos.
- `CriptaMapa.vecinos(sala_id)` → `((direccion, destino), ...)` en orden N, S, E, O (incluye puertas cerradas). `puerta_transitable(sala, dir)` = existe y no está cerrada.
- `CriptaMapa.obtener(id)` por búsqueda binaria; los ids de sala no tienen por qué ser contiguos.

### 5.2 Enemigos
- Una `Sala` guarda `enemigos_dormidos` (cargados, sin activar) y `enemigos_activos`. Un enemigo activo que se mueve cambia de lista de sala (`_mover_enemigo`). Los enemigos se crean dormidos en `ServicioPrecarga.preparar_sala` ordenados por `instancia_id` con `ordenar_auto`.
- `Enemigo.comportamiento` es un `str` copiado de la ficha; `decidir_accion_enemigo` despacha por ese texto (`"errante"`, `"rastreador"`, otro = guardián).
- El **rastro** es `Sala.rastro_ultima_visita` (`None` si nunca); `rastro_es_fresco(tiempo, 400)`. Lo marcan `Partida._mover/_esperar/_atacar/_recoger/...` en cada acción aceptada del jugador.

### 5.3 Catálogo y caché
- `ServicioCatalogo.obtener(ficha_id)` → memoria → disco (`CacheDisco`, validado por versión en la clave) → red por lotes de 10. `solicitar(ids)` acumula pendientes; `obtener_varias` resuelve juntos.
- Desalojo: LRU protegiendo `fichas_en_uso()` (la pregunta a `Partida.fichas_en_uso()`: inventario, suelo y trampas de la sala actual, enemigos dormidos de la sala actual, enemigos activos vivos de **todas** las salas).

### 5.4 Efectos (todo son eventos del reloj)
`EfectoCambioVelocidad` reescala el evento pendiente del actor con `calcular_tiempo_reprogramado` (cancela el viejo y programa uno nuevo con secuencia nueva). `EfectoTrampa`, `EfectoCierrePuerta`, `EfectoAntorcha` programan su evento con `datos=(EV_*, sujeto, a, b)` para poder guardarse.

---

## 6. Retroceso (pergamino): cómo está hecho

- `Reversible.__setattr__`: si hay `registrador`, antes de asignar guarda **una closure** `lambda: object.__setattr__(self, nombre, anterior)`. Se conectan: `Jugador`, `Inventario`, `Sala`, `EstadoPuertas` (vía `CriptaMapa.conectar_registrador`), y por instancia `Enemigo`, `Trampa` y efectos (`_con_retroceso`).
- `RelojEventos` registra de forma **explícita** (no con `Reversible`): `_deshacer_programar`, `restituir` (cancelar), `_deshacer_ejecutar` (restaura el reloj y reinserta el evento).
- Cambios que no son asignaciones (listas) registran su inversa a mano (`Sala.agregar_objeto/quitar_objeto/activar_enemigos_dormidos`, `_mover_enemigo`, `_matar_enemigo`).
- `Partida._guardar_contadores()` registra por acción un estado con **`self._azar.getstate()`** (tupla de 625 enteros). Tras retroceder se repite la misma acción con el mismo azar.
- `HistorialRetroceso`: `_intervalos: list[Pila]` (máx. 5; `pop(0)` al exceder). `sin_registrar()` pausa el registro (carga de contenido, pergaminos recogidos/soltados, descuento del pergamino usado).
- **Excluidos del alcance:** el cursor del inventario (`_no_reversibles`), la caché, la cantidad de pergaminos.

> ⚠️ **Implicaciones para la línea de tiempo (004):** las inversas son *closures*: no se pueden guardar en disco, ni consultar, ni recorrer por tiempo, y cada acción almacena un `getstate()` de 625 enteros. El historial de 5 intervalos es barato, pero **no sirve tal cual** para 5 000 acciones. La P1 ya resolvió el mismo problema para el guardado usando **datos planos** (`EventoGuardado`, `EV_*`). La línea de tiempo probablemente necesite un registro de cambios en forma de datos, no de closures (decisión del `plan.md` de 004).

---

## 7. Persistencia y bitácoras

### 7.1 `partida.sav` (`guardado_binario.py`)
- Disposición: `[ENCABEZADO 24 B][ÍNDICE n×16 B][BLOQUE GLOBAL][BLOQUE SALA]×n`, little-endian. Magic `b"CRPT"`, **`FORMATO_VERSION = 1`**.
- El índice (id, offset, longitud) se ordena con `ordenar_auto`; `cargar_sala(ruta, id)` hace **búsqueda binaria directamente sobre el archivo** (`seek`+`read` de 16 B).
- Global: versiones, semilla, estado del RNG, reloj, contadores, jugador+inventario, agenda (`EventoGuardado`), mensajes. Por sala: puertas, rastro, suelo, trampas, enemigos.
- Detecta magic/versión/truncado → `CriptaFormatoIncompatibleError`.
- Al cargar, `Partida.desde_estado_guardado` **no** restaura el historial de retroceso (empieza vacío) y reconstruye la agenda a partir de los `EV_*`.
- **No guarda** estado de niebla ni línea de tiempo (no existen aún). Hay que subir `FORMATO_VERSION` para que un guardado de la P1 se detecte como incompatible.

### 7.2 `partida.log`
- Una línea JSON por registro. Línea 1: `{"tipo":"encabezado","id_cripta","version_cripta","version_catalogo","semilla"}`; luego una línea por acción aceptada = `Accion.a_dict()` (p. ej. `{"tipo":"mover","direccion":"N"}`).
- `LectorBitacoraPartida.leer()`: toda línea no vacía debe ser JSON y, salvo la primera, **debe tener `"tipo"`**; `ServicioReplay` convierte cada línea con `Accion.desde_dict()` (que lanza `ValueError` ante un tipo desconocido y el replay lo reporta como «acción inválida»).
- `guardar` copia la bitácora a `partida.sav.log`; `cargar` la restaura (o la marca `parcial` si falta, y entonces `--replay` se niega a reproducirla).

### 7.3 Caché en disco
Claves versionadas (ver §2.3). Un archivo ilegible se trata como fallo de caché, nunca como excepción.

---

## 8. Puntos de extensión para la Parte II (dónde tocar)

### 001 — Terreno y cazador
| Qué | Dónde | Notas |
|---|---|---|
| Leer `costo` de la salida | `dto/salida_dto.py` (`SalidaDTO.desde_json`), `infraestructura/serializacion.py` (`pagina_esqueleto_a_json`), `cripta_mapa.py` | Ausente/`null` ⇒ 100. El cliente offline y la caché reutilizan estos DTO |
| Leer `rango` del cazador | `dto/enemigo_dto.py`, `serializacion.py` (`ficha_a_json`), `modelo/enemigo.py` | `comportamiento` llega como texto; el schema permite `rango` nulo (caso a aclarar) |
| Costo de movimiento variable | `Partida._mover` (hoy `accion.costo_base`=100) y `Partida._turno_enemigo` (hoy `costo = COSTO_MOVER`) | El costo debe salir de la `SalidaDTO` cruzada. `Accion.costo_base` es una tabla fija en `accion.py` |
| Decisión del cazador | `modelo/comportamiento_enemigo.py` (`decidir_accion_enemigo`) | Firma actual `(enemigo, sala_jugador_id, mapa, azar, tiempo_actual)`; necesita rutas sobre el esqueleto + estado actual de puertas (`mapa.puerta_transitable`) |
| Búsqueda de rutas y estructuras auxiliares | `estructuras/` (nuevo) + `modelo/` | Ver §4: no hay cola de prioridad indexable ni grafo. Prohibidos `heapq`, `set`, `dict`, `collections` |
| Invalidación de rutas | eventos que cambian puertas: `CriptaMapa.abrir_puerta/cerrar_puerta` (los llaman `_abrir` y `EfectoCierrePuerta._cerrar`); movimiento del jugador: `_mover`; muerte: `_matar_enemigo`; velocidad: `EfectoCambioVelocidad` | Cada uno es un punto donde invalidar |
| Agenda | `reloj.py` | Con intervalos `max(1, costo*100//velocidad)` y costo 1 el intervalo puede ser 1: revisar el bench de ciclo |
| Bench | `bench/cargas_bench.py` (`CARGAS`), `servicio_bench.py` | Añadir cargas; generar criptas con `tests/cripta_artificial.py` (cuadrícula, sin costos) o un generador nuevo determinista por semilla |
| Vista | `SalidaVista` (sin costo), `EnemigoVista`, `VistaConsola._paneles_*` | Mostrar costos y distinguir cazadores |

### 002 — Niebla de guerra e «ir a»
| Qué | Dónde | Notas |
|---|---|---|
| Estado de conocimiento (explorada/avistada/desconocida + memoria de puertas) | nuevo, en `modelo/`; debe ser **`Reversible`** o registrar inversas | Entra al guardado, al retroceso y a la línea de tiempo |
| Marcar exploración | `Partida.iniciar` (sala inicial) y `Partida._mover` (tras `jugador.sala_actual = ...`) | La antorcha: `Partida._antorcha_encendida` + `EfectoAntorcha`; **hoy la antorcha solo cambia un flag y programa su apagado, no tiene efecto de juego** |
| Observar puertas | al entrar a una sala y al estar en cualquiera de los dos lados | `CriptaMapa.vecinos/puerta_transitable` |
| Qué muestra la vista | `Partida.vista()` y `VistaConsola._minimapa` | Hoy `vista()` usa `mapa.vecinos(sala.id)` (datos reales); debe pasar a derivarse del conocimiento |
| Comando `ir a <sala>` y `mapa` | `VistaConsola._interpretar`, `Orden`, `ControladorCripta._procesar` | `_interpretar` toma `partes[1]` como argumento: «ir a 5» necesita manejar dos palabras. Cada paso debe ser una `Accion("mover", dir)` normal |
| Log | `partida_log.py` | La orden `ir a` se registra «además como comentario»: **hoy el lector exige que cada línea sea JSON con `"tipo"` y el replay rechaza tipos desconocidos**; hay que definir el formato del comentario y hacer que lector/replay lo ignoren |
| Precarga | `servicio_precarga.py` | Puede seguir usando el esqueleto completo (infraestructura) |

### 003 — Resolubilidad
| Qué | Dónde | Notas |
|---|---|---|
| Endpoint `/llaves` | `infraestructura/puertos.py` (`ClienteCripta`), `cliente_http.py`, `cliente_offline.py`, `cliente_general.py`, nuevo DTO en `dto/` | **No existe en ningún cliente.** Cuenta contra el presupuesto; puede persistirse con la versión de la cripta (`cache.py`) |
| Fixtures | `scripts/generar_fixtures.py`, `fixtures/<id>/` y `docs/FORMATO_OFFLINE.md` | Hay que añadir `llaves.json` por cripta y regenerar con las criptas de la P2 |
| Recorrido | nuevo en `servicios/` o `modelo/` | Opera sobre esqueleto + ubicación de llaves, sin vista |
| Banderas | `__main__.py` | `--verificar <cripta>` (sin vista), `--forzar`. Hoy `parse_known_args` pasa lo desconocido solo a `--bench` |
| Integración al inicio | `ServicioPartida.iniciar_nueva` | Punto natural para verificar antes de `Partida(...)`; mostrar reporte vía vista/controlador |

### 004 — Línea de tiempo
| Qué | Dónde | Notas |
|---|---|---|
| Registro de cambios consultable | nuevo; **no** reutilizar closures (§6) | Debe crecer con los cambios + 1 punto de control cada K acciones |
| Punto de control | `persistencia_modelo.crear_estado/restaurar_*` y `EstadoPartida` ya producen/consumen una copia completa **en datos planos, incluyendo el estado del RNG** (`EstadoRNG`) | Es la base natural del punto de control |
| Consulta `historia <t>/#k` | `ControladorCripta`, `VistaConsola`, `Partida` | No debe tocar el historial de retroceso ni el log |
| `--replay --hasta t` | `__main__._reproducir`, `ServicioReplay.reproducir` | Hoy reproduce siempre todo el log; no hay parámetro de corte |
| Recorte al usar pergamino | `Partida._usar_pergamino` | Coordinar con `HistorialRetroceso.deshacer_ultimo_intervalo` |
| Formato binario | `guardado_binario.py` (`FORMATO_VERSION`, `_escribir_global`, `_leer_global`) | Subir versión; escribir la línea de tiempo; **detectar el archivo viejo** (ya existe `CriptaFormatoIncompatibleError`) |
| Bandera | `__main__.py` | `--checkpoint-cada K` |

### Transversal (5.6 — revisión de decisiones de la P1)
- Agenda (`reloj.py`, `bench_agenda`, `bench_ciclo_eventos`) y retroceso (`historial_retroceso.py`, `bench_historial`): repetir mediciones con la carga nueva y documentar antes/después en `DECISIONES.md`.
- El bench `partida` con 400 salas ya supera 20 ms en la P1 (límite documentado, §4.1 de `DecisionesDiseño.md`); revisarlo con cazadores.

---

## 9. Riesgos de acoplamiento y hallazgos

1. **`Partida` (674 líneas) concentra casi todo.** Acciones, turnos, efectos, guardado y vista pasan por ella. Cualquier capacidad la toca: coordinen las modificaciones por funciones concretas para evitar conflictos de Git (§8).
2. **Costos fijos repartidos:** `Accion._TIPOS`/`costo_base`, `COSTO_MOVER` usado en `_turno_enemigo` y en `_activar_enemigos_de(enemigo, COSTO_MOVER)`. Con costo por salida hay que decidir quién calcula el costo del movimiento.
3. **Veneno y regeneración: ✅ verificado, son huecos de la Parte I.** `EfectoVeneno` solo se instancia en `Partida._restaurar_agenda` (`partida.py:189`, al cargar un guardado). Ningún punto del motor lo inicia durante el juego: ni trampas (`_activar_trampas_de`, `partida.py:401`, hace daño fijo), ni enemigos, ni objetos. El antídoto (`_aplicar_uso`, `partida.py:564`) llama `self._jugador.veneno_activo.cancelar()`, y `_motivo_no_usable` (`:545`) lo rechaza si no hay veneno, así que hoy el antídoto nunca se puede usar en una partida real. `EfectoRegeneracion` no se instancia en ningún archivo (grep sobre `cripta/` solo lo encuentra en su definición). Ninguno es parte de la P2, pero el Apéndice B de la P1 los pide; decidan si se arreglan en una tarea aparte (con spec) o se declaran fuera de alcance.
4. **Antorcha sin efecto de juego: ✅ verificado.** `_aplicar_uso` (`partida.py:566-568`) solo pone `_antorcha_encendida = True` y programa `EfectoAntorcha`. Nada lee ese flag salvo `vista()` (`:643`, para mostrar «Antorcha») y `_motivo_no_usable` (`:543`). 002 es quien le da efecto: el punto de enganche es `_mover` (`:368`), después de `jugador.sala_actual = destino.id`.
5. **DTO estrictos hacia adentro, tolerantes hacia afuera:** `desde_json` ignora campos extra (usa `datos[...]`/`.get`), así que `costo`/`rango` no rompen el parseo, pero **se pierden** si no se agregan a DTO, `serializacion.py` (caché) y `cliente_offline`.
6. **Caché de disco versionada por clave:** las criptas nuevas (otra versión) invalidan solas lo persistido; pero **los fixtures son archivos fijos**: hay que regenerarlos (`scripts/generar_fixtures.py`) y los `.log` de `docs/ejemplos/` seguirán sirviendo solo contra las criptas de la P1.
7. **Hilo de red en la precarga + `ClienteGeneral` serializado:** el modelo no debe depender del orden de llegada; la incorporación está ordenada por solicitud (`_incorporar_hasta`). Cualquier consulta nueva de red (`/llaves`) debe respetar presupuesto y orden determinista.
8. **Retroceso por closures** (§6): afecta el diseño de 004 y de la reversión del conocimiento (002).
9. **`VectorOrdenado.insertar` es O(n):** razonable a escala de la P1; con mapas grandes y búsquedas de rutas frecuentes, medirlo antes de usarlo como mapa de distancias.
10. **`HistorialRetroceso._intervalos.pop(0)`** es O(n) sobre una lista de ≤ 6 elementos (irrelevante hoy).
11. **Ejemplos de replay y pruebas dependen de fixtures de la P1**; si se regeneran, mantener las criptas antiguas o ajustar las pruebas.
12. **README desactualizado respecto a la P2** (versión de spec-kit, agente, banderas nuevas) y `DECISIONES.md` aún no está en la raíz.

---

13. **Nuevos hallazgos verificados al cerrar el mapa:**
    - `Partida._activar_enemigos_de` (`partida.py:258`) programa el primer turno con `COSTO_MOVER` (100). Es correcto según P1 §2.4 («acción base de costo 100»): **no debe cambiar** con el costo por salida, aunque tenga el mismo nombre de constante que el costo de movimiento.
    - `Partida._turno_enemigo` (`:273`) decide **antes** de saber cuánto costará: devuelve `(tipo, direccion)` y luego fija `costo = COSTO_MOVER`. Para el cazador la decisión debe devolver también el costo de la salida (o el motor debe consultarlo con `mapa.datos_de_puerta`/esqueleto); el costo hoy no viaja en la decisión.
    - `Partida._mover_enemigo` (`:294`) resuelve el destino con `origen.esqueleto.salida(direccion).sala_destino`: ahí mismo se puede leer el `costo` de la salida.
    - Los fixtures de la P1 **no traen `llaves.json`** (`fixtures/cripta-01/` solo tiene `contenido/`, `general.json`, `salas/`, `version.json`) ni `costo` en las salidas.
    - Los archivos `.py` usan finales de línea **CRLF** (`\r\n`). Los agentes que editen con `str_replace` o parches deben respetarlo o quedará ruido en los `diff` (considerar `.gitattributes`).
    - Los `__pycache__` del zip son de Python 3.14 y el mapa verificó con 3.12: el código corre en ambas.
    - El repo del zip trae un cambio sin confirmar (`docs/DecisionesDiseño.md` borrado y su copia `DecisionesDise#U00f1o.md` sin seguimiento): es un artefacto del zip, no tocar en el repo real.

---

## 11. Índice de líneas de las funciones que la P2 toca

> Números de línea del zip analizado (`HEAD 9865c1f`). Cambiarán al editar: úsenlos para ubicarse, no como contrato.

| Archivo | Función / clase | Línea |
|---|---|---|
| `modelo/partida.py` | `Partida.__init__` / `iniciar` | 61 / 219 |
| | `_guardar_contadores` / `_restaurar_contadores` | 99 / 106 |
| | `a_estado_guardado` / `desde_estado_guardado` / `_restaurar_agenda` | 117 / 133 / 176 |
| | `_terminar_accion_jugador` / `_avanzar_hasta_turno_jugador` | 245 / 239 |
| | `_activar_enemigos_de` / `_programar_turno_enemigo` | 258 / 265 |
| | `_turno_enemigo` / `_mover_enemigo` / `_matar_enemigo` | 273 / 294 / 468 |
| | `ejecutar_accion` / `_despachar` / `_usar_pergamino` | 309 / 328 / 347 |
| | `_mover` / `_abrir` / `_activar_trampas_de` | 368 / 419 / 401 |
| | `_aplicar_uso` / `_apagar_antorcha` | 554 / 571 |
| | `fichas_en_uso` / `vista` | 605 / 626 |
| `modelo/comportamiento_enemigo.py` | `decidir_accion_enemigo` / `_decidir_errante` / `_decidir_rastreador` | 10 / 21 / 31 |
| `modelo/reloj.py` | `calcular_intervalo` / `calcular_tiempo_reprogramado` | 7 / 11 |
| | `RelojEventos.programar / cancelar / reprogramar / ejecutar_siguiente` | 67 / 89 / 96 / 102 |
| | `restituir` / `programar_con_secuencia` | 148 / 159 |
| `modelo/cripta_mapa.py` | `vecinos` / `puerta_transitable` / `datos_de_puerta` | 26 / 40 / 48 |
| | `abrir_puerta` / `cerrar_puerta` / `sincronizar_puertas` | 71 / 74 / 94 |
| `modelo/efectos.py` | `EfectoVeneno` / `EfectoCambioVelocidad` / `EfectoAntorcha` | 29 / 90 / 137 |
| | `EfectoRegeneracion` / `EfectoTrampa` / `EfectoCierrePuerta` | 157 / 186 / 217 |
| `__main__.py` | `main` y sus `add_argument` | 51 / 53-57 |
| `controlador/controlador_cripta.py` | `_procesar` / `_traducir` / `_guardar` / `_cargar` | 127 / 155 / 259 / 264 |
| `vista/vista_consola.py` | `_interpretar` / `mostrar_estado` / `_minimapa` | 171 / 205 / 264 |
| `bench/cargas_bench.py` | `CARGAS` (registro de cargas de `--bench`) | 568 |

---

## 12. Mapa de pruebas existentes

27 archivos bajo `tests/`, un directorio por capa, más dos ayudantes compartidos en la raíz de `tests/`:

| Carpeta | Archivos |
|---|---|
| `tests/` (ayudantes) | `cliente_falso.py` (cliente sin red), `cripta_artificial.py` (cripta en cuadrícula, sin costos ni cazadores) |
| `controlador/` | `test_controlador_cripta`, `test_controlador_errores` |
| `estructuras/` | `test_cola_circular`, `test_heap_min`, `test_lista_doble_enlazada`, `test_lista_enlazada`, `test_ordenamientos`, `test_pila`, `test_vector_ordenado` |
| `infraestructura/` | `test_cache_disco`, `test_cliente_http`, `test_contador_solicitudes`, `test_guardado_binario`, `test_partida_log`, `test_puntajes_disco` |
| `modelo/` | `test_comportamiento_enemigo`, `test_guardado_ida`, `test_guardado_vuelta`, `test_pergamino`, `test_puntajes`, `test_retroceso_ganchos` |
| `servicios/` | `test_servicio_catalogo`, `test_servicio_partida`, `test_servicio_partida_guardado`, `test_servicio_precarga`, `test_servicio_replay` |
| `vista/` | `test_vista_consola` |

Pruebas que se romperán o deberán ampliarse con la P2: `test_comportamiento_enemigo` (cazador), `test_guardado_*` y `test_guardado_binario` (nueva versión de formato), `test_partida_log` y `test_servicio_replay` (comentarios `ir a`, `--hasta`), `test_vista_consola` (mapa conocido, costos), `test_cliente_http` y `test_servicio_partida` (endpoint `/llaves`). **No hay pruebas de `Partida` aisladas, de efectos ni de `reloj`**: se cubren de forma indirecta; 001 y 004 necesitarán pruebas directas nuevas.

---

## 13. Cargas de `--bench` ya disponibles

`CARGAS` (`bench/cargas_bench.py:568`) define 10 cargas, seleccionables con `--solo`: `agenda`, `cache`, `disco`, `inventario`, `historial`, `ordenamiento`, `guardado`, `ciclo`, `partida`, `solicitudes`. Reutilizables como base para P2 §6.3: `_medir` (mejor de 3 corridas), `_comparar` (texto «X veces más lenta/rápida»), `bench_ciclo_eventos` (límite 20 ms), `bench_partida_real` (Partida real sobre cripta artificial), `bench_historial` (inversas vs copia completa) y `estado_sintetico` (estado para guardado). **Faltan** las cargas de P2: ruta del cazador (uno vs muchos, rango, compartido vs individual), invalidación de rutas (puertas estables vs inestables), mapa conocido e «ir a», resolubilidad (incremental vs por llave), línea de tiempo (tres valores de K y sin puntos de control). Las criptas sintéticas deben ser deterministas por semilla (hoy `SEMILLA_BENCH`).

---

## 10. Cómo ejecutar lo que existe (para el agente)

```
py -m unittest discover -s tests -t .                        # 222 pruebas, debe terminar en OK
py -m cripta --offline                                       # juego con fixtures
py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log   # código 0
py -m cripta --bench --solo agenda ciclo historial           # mediciones
```

Una prueba nueva de la P2 debe: usar `unittest`, apoyarse en `tests/cliente_falso.py` y `tests/cripta_artificial.py` (sin red) y **citar el id `FR-XXX-NNN`** del requisito que ejerce.
