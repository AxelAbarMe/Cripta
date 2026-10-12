# Contrato de `Partida` (API pública del motor)

Archivo de referencia entre quien implementa el modelo y quien implementa el controlador, el replay y el bench.
Si algo de aquí cambia, se avisa antes (interfaz congelada).

Módulos nuevos (en `cripta/modelo/`): `accion.py` (la acción del jugador) y `partida.py` (el motor).
Convención: todos los nombres de métodos, atributos y clases nuevos van **en español**, igual que el resto del modelo. Los métodos especiales que exige Python (`__init__`, `__len__`) se mantienen.

---

## 1. Principios
1. `Partida` **no conoce HTTP, archivos ni la vista**. Recibe sus dependencias ya construidas.
2. Toda la aleatoriedad sale de **una sola** `random.Random(semilla)` propia de la partida.
3. Nunca usa la hora del sistema. La espera real por una respuesta de red **no mueve el reloj virtual**.
4. Funciona igual en el juego interactivo, en `--replay` y en `--bench`: no necesita vista.
5. Las acciones inválidas **no lanzan excepción**: se devuelven como rechazadas, sin consumir tiempo.
6. Solo se propagan excepciones por errores de infraestructura (CriptaApiError, CriptaLimiteError, CriptaDatosNoEncontradosError, CriptaError si la precarga ya se cerró) y por mal uso (RuntimeError: ejecutar antes de iniciar(), iniciar dos veces, guardar una partida terminada). Si la infraestructura falla a mitad de una acción, Partida deshace lo ya cambiado: la partida queda como estaba y la acción se puede reintentar (los mensajes ya mostrados no se retiran).

---

## 2. Construcción

```python
Partida(datos_generales, mapa, servicio_catalogo, servicio_precarga, semilla)
```

| Parámetro | Qué es |
|---|---|
| `datos_generales` | `CriptaGeneralDTO` de la cripta (sala inicial, sala de salida, llave de salida, estadísticas del jugador, `inventario_max`) |
| `mapa` | `CriptaMapa` ya construido con el esqueleto completo |
| `servicio_catalogo` | `ServicioCatalogo` (fichas) |
| `servicio_precarga` | `ServicioPrecarga` (contenido de salas) |
| `semilla` | entero con el que se crea `random.Random` |

Quien construye todo esto es ServicioPartida (§11); el __main__ solo le entrega el cliente, el contador y la caché de disco.

`partida.iniciar()` hace lo de §2.4 del enunciado: asegura el contenido de la sala inicial, le pone rastro en tiempo 0, activa sus enemigos en orden de id de instancia y programa la primera acción del jugador en tiempo 0.

---

## 3. La acción del jugador (`accion.py`)

`Accion` es un objeto inmutable con un `tipo` y, según el tipo, un argumento. Se convierte a `dict` para el log y se reconstruye desde él.

| `tipo` | Argumento | Costo base | Notas |
|---|---|---|---|
| `"mover"` | `direccion`: `"N"`, `"S"`, `"E"`, `"O"` | 100 | |
| `"abrir"` | `direccion` | 50 | Rechazada si falta la llave |
| `"atacar"` | `instancia`: id de instancia del enemigo | 100 | Debe estar en la sala actual |
| `"esperar"` | (ninguno) | 100 | |
| `"recoger"` | `ficha_id`: objeto del suelo | 25 | Rechazada con inventario lleno |
| `"usar"` | `indice`: posición en el orden real del inventario | 50 | |
| `"equipar"` | `indice` | 50 | |
| `"soltar"` | `indice` | 25 | |
| `"pergamino"` | (ninguno) | **0** | No consume tiempo y no entra al historial de retroceso (§2.11) |

Decisión: `usar`, `equipar` y `soltar` llevan el `indice` explícito, y `Partida` coloca el cursor del inventario ahí antes de ejecutar. Así una acción por sí sola es reproducible; si dependiera de dónde quedó el cursor, el replay no podría reconstruirla.

Formato en el log (un `dict` por línea, tal como lo escribe `EscritorBitacoraPartida.registrar_accion`):
```python
{"tipo": "mover", "direccion": "N"}
{"tipo": "atacar", "instancia": "e-201"}
{"tipo": "equipar", "indice": 2}
{"tipo": "esperar"}
```
Métodos: `accion.a_dict()` y `Accion.desde_dict(datos)`. `desde_dict` lanza `ValueError` con un mensaje claro si el `tipo` es desconocido o falta un argumento.

**Qué se registra en el log:** toda acción **aceptada**, incluida `"pergamino"` (aunque no sea una acción del jugador para el historial, sí cambia el estado y el replay tiene que repetirla). Las rechazadas no se registran: no cambian el estado. Lo escribe ServicioPartida.ejecutar, no el controlador.

---

## 4. Ejecutar una acción

```python
resultado = partida.ejecutar_accion(accion)
```

1. Si la acción no es válida → devuelve un `ResultadoAccion` con `aceptada=False` y el motivo; no consume tiempo ni toca el estado.
2. Si es válida: la ejecuta, programa la siguiente acción del jugador y **procesa todos los eventos** (enemigos, efectos, cierres de puerta) hasta el siguiente instante en que el jugador decide.
3. Si el movimiento entra a una sala cuyo contenido aún no llegó, **espera** (bloquea) hasta tenerlo; el reloj virtual no avanza durante esa espera. (hasta 60 s; si no llega, CriptaApiError)

`ResultadoAccion` (inmutable):

| Campo | Tipo | Significado |
|---|---|---|
| `aceptada` | `bool` | Si se ejecutó |
| `motivo_rechazo` | `str` o `None` | Texto para mostrar al jugador cuando no se ejecutó |
| `mensajes` | `tuple[str, ...]` | Mensajes nuevos generados (también quedan en la bitácora de 20) |
| `desenlace` | `str` | `"en_curso"`, `"victoria"` o `"derrota"` |
| `tiempo` | `int` | Reloj virtual al terminar |

Motivos de rechazo cubiertos (Apéndice B): inventario lleno, puerta sin llave, no hay salida en esa dirección, puerta cerrada, enemigo que no está en la sala, índice de inventario inexistente, objeto del suelo que no está. sin pergamino, sin acción que deshacer, puerta ya abierta, puerta sin cerradura, objeto que no se puede equipar o usar.

Cuando `desenlace` deja de ser `"en_curso"`, `ejecutar_accion` ya no acepta más acciones (las rechaza con el motivo "La partida ya terminó.").

---

## 5. Consultas (solo lectura, no consumen tiempo ni tocan el azar)

| Método | Devuelve |
|---|---|
| `partida.vista()` | `VistaPartida` inmutable con lo que muestra la interfaz (ver abajo) |
| `partida.desenlace()` | `"en_curso"`, `"victoria"` o `"derrota"` |
| `partida.mensajes()` | Los últimos 20 mensajes, del más antiguo al más reciente |
| `partida.inventario_siguiente()` / `inventario_anterior()` | Mueven el cursor y devuelven el objeto actual (sin tiempo) |
| `partida.inventario_ordenado(criterio)` | Vista ordenada por `"peso"`, `"valor"` o `"nombre"` sin alterar el orden real |
| `partida.puntaje()` | Datos para la tabla de puntajes: acciones ejecutadas, enemigos derrotados, tiempo final. ResumenPuntaje; el nombre y la versión de la cripta los agrega ServicioPartida. |
| `partida.fichas_en_uso()` | ids de ficha que la caché no puede liberar (inventario, suelo y trampas de la sala actual, enemigos vivos); se la pasa ServicioPartida al catálogo.

`VistaPartida` incluye: sala actual (id y nombre), salidas (dirección, destino, si está cerrada), enemigos presentes (etiqueta como “Rata gigante [e-201]”, instancia, vida y vida máxima), objetos del suelo (ficha_id y nombre), trampas (nombre y si está armada), estadísticas del jugador (vida, vida máxima, ataque y defensa con el equipo puesto, velocidad), efectos activos, inventario (objeto actual y su posición, cantidad, capacidad, arma y armadura equipadas), pergaminos y retrocesos_posibles, tiempo virtual y desenlace.

---

## 6. Guardado y carga

```python
estado = partida.a_estado_guardado(version_catalogo)
partida = Partida.desde_estado_guardado(estado, datos_generales, mapa, servicio_catalogo, servicio_precarga)
```

- `a_estado_guardado()` produce el `EstadoPartida` que ya sabe escribir `GuardadoBinario`. Incluye la semilla y el estado del generador aleatorio.
- `version_catalogo` la aporta quien arma la partida (`servicio_partida`), porque `Partida` no conoce esa versión.
- `desde_estado_guardado()` reconstruye el modelo y **recrea las acciones del reloj** (hoy son closures) a partir de `EventoGuardado`.
- Este puente vive en `modelo/persistencia_modelo.py`; `Partida` solo expone los dos métodos.
- a_estado_guardado lanza RuntimeError si la partida no se inició o ya terminó.
- desde_estado_guardado lanza CriptaFormatoIncompatibleError si el id o la versión de la cripta no coinciden, y el historial de retroceso empieza vacío.

El contrato con infraestructura: `EstadoPartida` y `GuardadoBinario` están congelados (si cambian, se avisa).

---

## 7. Cómo lo usa cada parte

| Quién | Qué hace con `Partida` |
|---|---|
| **Controlador** | Traduce el teclado a `Accion`, llama a `ejecutar_accion`, pide `vista()` a la vista y llama a `servicio.ejecutar(accion)`, que ejecuta y registra en la bitácora; para consultar usa `servicio.partida.vista()`. `registrar_accion(accion.a_dict())` |
| **Replay** | Lee el log con `LectorBitacoraPartida`, valida versiones, lama a `servicio.iniciar_nueva(cripta, semilla)` sin ruta de bitácora con la semilla del encabezado y llama `ejecutar_accion(Accion.desde_dict(d))` por cada línea. No necesita vista |
| **Bench** | Puede crear una `Partida` con una cripta artificial (`tests/cripta_artificial.py`) y medir el ciclo de §5.2 |
| **Guardado** | Llama a `a_estado_guardado()` / `desde_estado_guardado()` y le pasa el estado a `GuardadoBinario` |

---

## 8. Garantía de determinismo (la prueba del contrato)

Dos `Partida` creadas con la **misma cripta, la misma semilla y la misma secuencia de acciones** deben producir exactamente el `mismo vista()`, el mismo `puntaje()` y el mismo estado guardado. Los mensajes solo pueden diferir en los de acciones rechazadas, que no se anotan en el log. Esta es la prueba que valida el replay de punta a punta.

---

## 9. Fuera del contrato (decisiones que se anotan en el Documento de Decisiones)
- Qué origina el veneno y si se acumula o se reinicia.
- Significado de `modificador_velocidad`.
- Si el daño de trampa pasa por la defensa.
- Qué hacer con la regeneración (el esquema `Enemy` no la declara).

---

## 10. Estado de implementación
Este archivo define la interfaz **antes** de implementarla. Se marca cada punto cuando exista:

- [x] `accion.py`: `Accion`, `a_dict`, `desde_dict`
- [x] `partida.py`: construcción e `iniciar()`
- [x] `ejecutar_accion` con las 9 acciones
- [x] consultas (`vista`, `mensajes`, `inventario_*`, `puntaje`)
- [x] `a_estado_guardado` / `desde_estado_guardado`
- [x] prueba de determinismo (sección 8)

## 11. `ServicioPartida` (lo que usan el controlador y el replay)
Archivo: `cripta/servicios/servicio_partida.py`. Construcción: `ServicioPartida(cliente, contador, cache_disco=None, tamano_cache=25, asincrono=True, repositorio_puntajes=None)`, con `cliente` = `ClienteGeneral(...)` y `contador` el mismo que usa el cliente.

| Miembro | Qué hace |
|---|---|
| `listar_criptas()` | `GET /criptas` (cuenta como una solicitud) |
| `iniciar_nueva(cripta_id, semilla=None, ruta_bitacora=None)` | Fija el presupuesto de la cripta, consulta la versión del catálogo, carga el esqueleto, arma todo e inicia. Sin `semilla` genera una. Sin `ruta_bitacora` no escribe log |
| `ejecutar(accion)` → `ResultadoAccion` | Ejecuta y, si se acepta, anota en la bitácora (incluido el pergamino) |
| `partida` | Solo consultas: `vista()`, `mensajes()`, `desenlace()`, `inventario_*`, `puntaje()` |
| `reporte_final()` | Solicitudes, presupuesto, aciertos y fallos de caché (§5.1) |
| `cerrar()` | Detiene la precarga. Llamarlo siempre al terminar |
| `datos_generales`, `version_catalogo`, `semilla` | Datos de la partida en curso |

Cualquier error de infraestructura hereda de `CriptaError` y puede salir de `ejecutar` **y también de `vista()`** (que consulta el catálogo): el controlador captura `CriptaError`, muestra el mensaje y sigue; la partida no quedó a medias.

| Miembro | Qué hace |
|---|---|
| `guardar(ruta)` | Guarda la partida y una copia de la bitácora en `ruta.log`. `RuntimeError` si la partida terminó |
| `cargar(ruta, ruta_bitacora=None)` | Reemplaza la partida en curso. `FileNotFoundError` o `CriptaFormatoIncompatibleError` si el archivo falta o no es compatible, y entonces la partida en curso no se toca |
| `registrar_puntaje(nombre)` | Solo con la partida terminada y una vez por partida. Devuelve el ranking de la cripta |
| `ranking()` | Puntajes de la cripta y versión de la partida en curso |
| `bitacora_completa` | `False` si se cargó un guardado sin su copia de la bitácora |

