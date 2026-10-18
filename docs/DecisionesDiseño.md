# Documento de Decisiones de Diseño — CRIPTA

## 4.1 Qué ocurre a continuación (agenda de eventos)
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión


### Decisión
Pendiente — completar en reunión (revisar para eliminar esta linea)

La agenda es un montículo mínimo (`HeapMinimo`, implementación propia) ordenado por la pareja `(tiempo, secuencia)`. El número de secuencia lo asigna el reloj al programar cada evento, así que el orden es total y determinista aunque haya empates, cancelaciones o reprogramaciones.

Cancelar un evento solo marca `cancelado = True`; el evento se descarta cuando sale del montículo. Reprogramar cancela el evento viejo y agenda uno nuevo con secuencia nueva (§2.3). La muerte de un actor no cancela sus eventos uno por uno: el turno comprueba `esta_vivo()` y no hace nada si ya murió. El reloj lleva un contador de eventos vigentes, de modo que `esta_vacia()` no tiene que recorrer la agenda.

Efectos: un veneno nuevo reemplaza al anterior y reinicia su duración (no se acumula el daño), y el actor guarda cuál es su veneno activo para que el antídoto pueda cancelarlo. Los cambios de velocidad restan al terminar lo que ellos mismos sumaron, así varios efectos solapados no se pisan, y la velocidad nunca baja de `VELOCIDAD_MINIMA` (1).

El turno del jugador es un evento más de la misma agenda: se programa en tiempo 0 al iniciar la partida y, tras cada acción aceptada, se programa el siguiente con `intervalo = max(1, costo * 100 // velocidad)`. Un motor (`Partida`) ejecuta eventos hasta que vuelve a tocar el turno del jugador; así el orden entre jugador y enemigos sale solo de `(tiempo, secuencia)`. Las acciones rechazadas (por ejemplo, una acción aún no permitida) no consumen tiempo ni cambian el estado. Cada enemigo decide en su turno con un módulo aparte (`comportamiento_enemigo.py`) y el motor ejecuta lo decidido y reprograma su siguiente turno con costo 100.

Las trampas y el cierre automático de puertas también son eventos de la agenda: al activarse, una trampa desarma y programa su rearme con el intervalo de su ficha (300 si no declara otro), y una puerta con cierre automático programa su cierre al abrirse. El cierre actúa sobre los dos lados de la puerta; quien ya la cruzó se queda en su sala y solo se impide volver a atravesar. El daño de una trampa es fijo: no pasa por la defensa ni consume el generador aleatorio.

Cuando un enemigo muere, el motor cancela su evento pendiente y lo saca de la sala, de modo que sus acciones futuras no ocurren y no hace falta recorrer la agenda. El turno del jugador guarda su propio evento pendiente (que se limpia cuando se ejecuta) para que un efecto de velocidad reescale solo una acción realmente programada (§2.3). Las pociones de velocidad se aplican antes de calcular el siguiente turno del jugador.

El cierre automático de una puerta es un efecto (`EfectoCierrePuerta`) que cierra los dos lados de la salida a través del mapa, porque una salida conecta exactamente dos salas (§2.1) y el API solo marca la puerta cerrada, la llave y el cierre en uno de sus lados. El motor sincroniza el estado de los dos lados al crear la partida. La regeneración de enemigos (§2.10) está implementada como efecto, pero el esquema de enemigo del API no tiene ningún campo para declararla, así que con los datos actuales ningún enemigo la usa; queda como decisión conocida.


### Análisis de complejidad
Pendiente — completar en reunión (revisar para eliminar esta linea)

Programar y extraer el siguiente evento cuestan O(log n) con n eventos en la agenda. Cancelar es O(1) y reprogramar es O(log n). `esta_vacia()` es O(1) gracias al contador de eventos vigentes. Las operaciones más frecuentes del juego, extraer el siguiente evento y programar el siguiente turno del actor, son las que cuestan O(log n).



### Evidencia empírica
Pendiente — completar en reunión (revisar para eliminar esta linea)

Medición con `--bench` (escala 0.3), heap contra lista lineal (alternativa descartada): con 100, 500 y 2000 eventos pendientes la lista lineal es 1.5x, 5.7x y 15.6x más lenta. Con 600 actores activos (1200 eventos) el peor ciclo tomó 6.17 ms, bajo el límite de 20 ms de §5.2 (carga sintética). Cancelar un tercio de los eventos y reprogramar otro tercio, de forma perezosa, cuesta 0.33 µs por operación.

Rendimiento del ciclo (§5.2), medido con `--bench --solo ciclo` (escala 0.3, Python 3.12.10, Ryzen 5 5600GT con 32 GB de RAM), con 600 actores activos y 1200 eventos por ciclo. Se reporta el peor de 20 ciclos en cada corrida. Primera serie de 5 corridas: 15.9, 7.1, 6.9, 23.3 y 7.1 ms (mediana 7.1 ms). Segunda serie de 5 corridas, con el recolector de basura desactivado: 6.9, 11.9, 7.5, 13.3 y 7.0 ms (mediana 7.5 ms). De las 10 corridas, 9 quedaron por debajo del límite de 20 ms y una (23.3 ms) lo superó.


### Límites conocidos
Pendiente — completar en reunión (revisar para eliminar esta linea)

La cancelación es perezosa: los eventos cancelados siguen ocupando espacio en el montículo hasta que les toca salir. Con muchas cancelaciones sin consumir eventos, la agenda puede crecer más que el número de eventos vigentes (con 100 000 reprogramaciones, el montículo llegó a 100 001 entradas). Si eso fuera un problema, habría que compactar el montículo cada cierto número de cancelaciones.

No se puede programar un evento en un tiempo anterior al del reloj (se lanza `ValueError`). El retroceso del pergamino restaura el reloj con un método propio (`restaurar`) en vez de programar hacia atrás.

La medición del ciclo tiene picos aislados: desactivar el recolector de basura no los eliminó, por lo que no se deben a él, y no se determinó su causa (puede ser ruido del sistema, pues el equipo de medición no estaba dedicado a la prueba). Como el bench reporta el peor de 20 ciclos, un solo ciclo lento basta para que la corrida supere el límite; por eso la conclusión se apoya en la mediana de varias corridas y no en una sola, y conviene medir con el equipo en reposo y reportar también un percentil.


## 4.2 Traer el contenido antes de que haga falta (precarga)
### Problema
Para que el jugador entre a una sala, el programa necesita su contenido (enemigos, objetos, trampas) **antes** de confirmar el movimiento: nunca puede quedar en una sala cuyo contenido no conoce. El esqueleto de la cripta (qué salas hay y cómo se conectan) se descarga completo al iniciar, pero el contenido se pide aparte: cada solicitud tarda unos 400 ms, cuesta lo mismo con 1 sala que con 10 y cuenta contra el presupuesto. Si se pidiera al cruzar cada puerta, el jugador esperaría 400 ms en cada movimiento.

La operación que el programa ejecuta en cada movimiento es **revisar si conviene anticipar** contenido desde la sala nueva; pedir un lote ocurre mucho menos. En un recorrido de 89 movimientos por una cripta de 100 salas se revisó 89 veces y se pidieron 10 lotes. Además, puede haber una respuesta todavía en camino cuando el jugador se mueve: el programa debe esperarla sin caerse y sin que el tiempo real de red afecte el reloj virtual del juego, y las respuestas deben incorporarse siempre en el mismo orden para que la partida sea reproducible.

### Alternativas consideradas
1. **Pedir el contenido de cada sala al entrar** (una solicitud por sala, sin anticipar). Es lo más simple, pero gasta una solicitud por sala visitada y hace esperar ~400 ms en cada puerta. Se descartó; su costo en solicitudes se midió contra lo elegido (ver Evidencia).
2. **Pedir todo el contenido al empezar la partida.** Usa la misma cantidad de solicitudes que lo elegido (una cada 10 salas), pero obliga a esperarlas todas antes de jugar (con 1000 salas serían unos 40 s) y gasta presupuesto en salas que el jugador quizá nunca visite. Se descartó.
3. **Esperar la respuesta en el mismo hilo del juego** contra **pedirla en un hilo de red aparte** (un hilo es una tarea que el programa ejecuta en paralelo). En el mismo hilo, cada lote detiene el juego 400 ms aunque todavía no haga falta. En un hilo aparte, el lote viaja mientras el jugador piensa su siguiente acción. Se eligió el hilo aparte, pero el juego sigue siendo determinista (ver Decisión).

### Decisión
- **Anticipar por cercanía:** al entrar a una sala se recorre el esqueleto en anchura desde ella (primero las salas a 1 paso, después las de 2, y así), en orden N, S, E, O. Si alguna sala a 2 pasos o menos todavía no se pidió, se pide **un lote** con las 10 salas no pedidas más cercanas. Si todo lo cercano ya se pidió, no se hace nada.
- **Nunca pedir dos veces:** cada sala pedida, recibida o leída del disco se anota en un `VectorOrdenado` (arreglo ordenado por id) en el momento de **pedirla**, no al recibirla. Así lo que se decide no depende de cuándo llegue una respuesta. Una sala guardada en disco con la versión vigente de la cripta se carga sin red y no ocupa lugar en el lote.
- **Hilo de red:** los lotes se ponen en una cola y un solo hilo de red los envía en el orden en que se pidieron (primero en entrar, primero en salir). La cola está protegida para que el juego y el hilo no la usen al mismo tiempo.
- **Determinismo:** lo que llega por red no entra al juego en cuanto llega. Solo se incorpora cuando el jugador necesita una sala y siempre en el orden en que se pidieron los lotes. Si la respuesta todavía no llegó, se espera en tiempo real, sin tocar el reloj virtual del juego. Así, aunque la red tarde distinto en cada partida, el juego ve lo mismo y en el mismo orden.
- **Fallos:** si un lote falla, sus salas vuelven a quedar "sin pedir" y el error llega solo a quien necesitaba esa sala; la partida sigue y puede reintentar. Un lote se espera como mucho 60 s (`ESPERA_MAXIMA_LOTE_SEGUNDOS`): si no llega se da por fallido, y si la respuesta llega después se ignora. Después de cerrar la precarga no se pide nada más: pedir una sala nueva falla de inmediato en lugar de esperar a un hilo que ya terminó.

### Análisis de complejidad
Letras usadas: **S** = salas de la cripta; **a** = salas a 2 pasos o menos de la sala actual (con 4 salidas por sala, unas pocas decenas como mucho).
- **Revisar si conviene anticipar** (en cada movimiento): si ya se pidieron todas las salas, O(1), una sola comparación. Si no, se recorren solo las salas cercanas, O(a log S), porque cada una se busca con búsqueda binaria entre las ya pedidas.
- **Armar un lote:** recorre en anchura hasta encontrar 10 salas sin pedir; en el peor caso (todo lo cercano ya pedido) puede recorrer casi toda la cripta, O(S log S). Solo pasa cuando de verdad se pide un lote.
- **Asegurar el contenido de una sala al entrar:** buscar en qué lote viene, O(log S), más esperar ese lote si todavía no llegó.
- **Solicitudes de red:** como cada lote lleva 10 salas que nunca se pidieron, el total de solicitudes de contenido nunca pasa de ⌈S/10⌉ (S dividido entre 10, redondeado hacia arriba).

### Evidencia empírica
- `--bench --solo solicitudes` (cripta artificial, recorrido en zigzag; cuenta las solicitudes, no depende de la máquina):

  | Cripta | Salas visitadas | Precarga por lotes (elegida) | Una solicitud por sala (descartada) |
  |---|---|---|---|
  | 100 salas | 90 | 10 | 90 |
  | 400 salas | 380 | 40 | 380 |

  En los dos casos el total es exactamente ⌈S/10⌉, el mínimo posible.
- Espera del jugador (medición aparte, con un script de prueba: cripta artificial de 100 salas, cliente falso con 400 ms de latencia por solicitud, hilo de red activo; Intel Core Ultra 7, 16 GB, Python 3.14.6):
  - Jugador que se mueve sin pausa (89 movimientos seguidos, el peor caso): solo 8 movimientos tuvieron que esperar, 4.48 s en total. Pidiendo cada sala al entrar habrían sido unos 89 × 0.4 = 36 s.
  - Jugador que piensa 1 s entre acciones (30 movimientos): solo 2 movimientos esperaron, 0.87 s en total. El resto del contenido llegó mientras el jugador pensaba.
- Tests (`tests/servicios/test_servicio_precarga.py`): recorrer las 25 salas de una cripta artificial usa exactamente 3 lotes; si una respuesta no llega a tiempo hay un error en lugar de una espera eterna; una respuesta que llega tarde se ignora y la sala se puede volver a pedir; después de cerrar, pedir una sala falla de inmediato.

### Límites conocidos
- La anticipación mira 2 pasos a la redonda. Si el jugador se mueve sin pausa y la red es lenta, alcanza al hilo de red y espera (7 de 89 movimientos en la medición). Con una red mucho más lenta que 400 ms convendría mirar más lejos.
- El recorrido en anchura no distingue puertas cerradas: puede anticipar salas detrás de una puerta que el jugador nunca abra. No supera el máximo de ⌈S/10⌉ solicitudes, pero puede gastar algunas en salas que no se visitan.
- Hay un solo hilo de red y los lotes salen de uno en uno. Si el API permitiera solicitudes simultáneas, varios hilos acortarían la espera, pero complicarían el orden determinista.
- La espera máxima de 60 s es larga para un jugador; se eligió así para no dar por fallida una respuesta lenta pero válida.
- La medición de espera usa un cliente falso con latencia fija; no se midió contra el API real.

## 4.3 Resolución de referencias del catálogo
### Problema
El contenido de una sala no trae las entidades completas: trae ids de tipo (`ent_rata_gigante`, `itm_antorcha`, `trp_dardos`) que hay que convertir en fichas de catálogo antes de mostrar o simular la sala. Los ids aparecen en un orden que el programa no controla (según por dónde camine el jugador y qué contenido llegue en cada lote), se repiten mucho entre salas y algunos solo se descubren de forma indirecta: la ficha de un enemigo dice qué objetos suelta. Cada solicitud cuenta contra el presupuesto, y el catálogo acepta hasta 10 ids por solicitud.

Las operaciones que el programa ejecuta de verdad son dos. La primera es **consultar una ficha** (`obtener`), en cada vista de la sala, al preparar una sala y al revisar el inventario. Es muy frecuente: en un recorrido de 89 movimientos por una cripta de 100 salas hubo 185 consultas resueltas en memoria, unas 2 por movimiento. La segunda es **descubrir ids** (`solicitar`), cada vez que se incorpora el contenido de una sala o se descarga la ficha de un enemigo. Es mucho menos frecuente y casi siempre trae ids repetidos.

### Alternativas consideradas
1. **Pedir cada id en el momento en que hace falta** (una solicitud por ficha). Es lo más simple, pero gasta una solicitud por cada tipo distinto, aunque el lote admitiría 10 por el mismo costo. Se descartó por presupuesto; se midió contra lo elegido (ver Evidencia).
2. **Esperar a juntar 10 ids antes de pedir.** Aprovecha cada lote al máximo, pero no sirve cuando una ficha hace falta ya (el jugador entra a una sala y hay que mostrarla): no se puede esperar a que aparezcan más ids. Se descartó.
3. **Descargar todo el catálogo al empezar.** El API solo entrega fichas por id y los ids solo se conocen al descubrirlos, así que no hay forma de pedir "todo"; además se gastarían solicitudes en tipos que el jugador nunca ve. Se descartó.

### Decisión
Lo elegido combina "pedir cuando hace falta" con "aprovechar el lote" (un lote es una sola solicitud al catálogo con hasta 10 ids):
- Cada id descubierto se anota como **pendiente**: todavía no se pide, queda en espera para viajar en el próximo lote. Los pendientes se guardan en un `VectorOrdenado` (un arreglo ordenado por id, ver §4.4), así no hay repetidos y cada lote se arma siempre en el mismo orden. Se anotan al incorporar el contenido de una sala y al descargar la ficha de un enemigo, porque esa ficha dice qué objetos suelta: así esos objetos se conocen antes de que el enemigo muera.
- Al **consultar** una ficha se busca primero en memoria, después en el disco (con la versión del catálogo dentro del nombre del archivo, ver §4.4) y solo al final en la red. Si hay que ir a la red, la ficha que hace falta viaja junto con hasta 9 pendientes en **una sola solicitud**.
- Para preparar una sala se piden todas sus fichas de una vez, así las que faltan viajan juntas.
- Antes de armar un lote se quitan de los pendientes los ids que ya están en memoria o en el disco con la versión vigente: **un id vigente nunca se pide dos veces**.
- La versión del catálogo se consulta una sola vez por partida. Como el catálogo es global y el nombre del archivo en disco no incluye la cripta, una ficha descargada jugando una cripta sirve para las demás.

### Análisis de complejidad
Letras usadas: **n** = fichas guardadas en memoria (como mucho `--cache-size`, 25 por defecto); **p** = ids pendientes, es decir, descubiertos pero todavía no pedidos; **k** = fichas distintas que necesita la partida completa.
- **Consultar una ficha en memoria** (la operación más frecuente): O(log n), porque el índice es un `VectorOrdenado` y se busca con búsqueda binaria (con 25 fichas son unas 5 comparaciones). Además, mover la ficha al frente de la lista de uso cuesta O(1): no depende de cuántas fichas haya (ver §4.4).
- **Anotar un id descubierto:** comprobar si ya está en memoria o en los pendientes es O(log n + log p), con búsqueda binaria. Si es nuevo, insertarlo en su lugar cuesta O(p), porque al meterlo en el arreglo ordenado hay que correr una posición a los que van detrás. Es poco: en las partidas medidas p se queda en unos pocos ids.
- **Armar un lote:** recorrer como mucho 10 pendientes, un costo fijo.
- **Solicitudes de red:** en el mejor caso, ⌈k/10⌉ lotes (todas las fichas agrupadas de 10 en 10). En el peor caso, una solicitud por ficha: pasaría si cada id se descubriera justo en el momento en que ya hace falta, y sería igual que la alternativa descartada.

### Evidencia empírica
- `--bench --solo solicitudes` (cripta artificial, recorrido en zigzag, conteo de llamadas del cliente; los conteos no dependen de la máquina):

  | Cripta | Lotes de catálogo (elegido) | Una solicitud por ficha (descartada) |
  |---|---|---|
  | 100 salas, 90 visitadas | 4 | 7 |
  | 400 salas, 380 visitadas | 4 | 7 |

  En las dos partidas se enviaron 7 ids en total y los 7 eran distintos: ninguno se pidió dos veces. El primer lote llevó 4 fichas juntas; los otros 3 llevaron una ficha que apareció más tarde (lo que suelta la rata y tipos de salas lejanas).
- `cripta-01` sin nada en la caché de disco (todo se descarga): 2 lotes de catálogo en total al iniciar la partida (ver §4.4).
- Tests (`tests/servicios/test_servicio_catalogo.py`): tres ids descubiertos viajan en un solo lote; lo que ya está en memoria no genera solicitudes; contar aciertos y fallos da lo mismo pidiendo de a uno o todos juntos. En `tests/infraestructura/test_cache_disco.py`: una ficha dañada en disco se vuelve a pedir **en el mismo lote** que las que faltan.

### Límites conocidos
- La cripta artificial tiene solo 7 tipos de ficha, así que la ganancia medida es pequeña (4 lotes contra 7 solicitudes). Con muchos tipos distintos la diferencia puede llegar a 10 a 1, pero no se ha medido con una cripta de catálogo grande.
- Si los ids se descubrieran uno por uno justo cuando hacen falta, cada uno costaría un lote propio y la estrategia se acercaría a la alternativa descartada. Anotar lo que suelta cada enemigo al descargar su ficha reduce ese caso, pero no lo elimina.
- Insertar un id pendiente obliga a correr los que van detrás en el arreglo ordenado. Si una sola sala trajera cientos de ids nuevos, ese costo empezaría a notarse y convendría otra estructura; con las criptas probadas los pendientes son pocos y no pesa.
- La versión del catálogo cuesta una solicitud por partida, aunque todas las fichas estén en disco.

## 4.4 Reutilización y caché persistente
### Problema
Las fichas de catálogo se consultan todo el tiempo: al mostrar la sala, al preparar una sala nueva y al revisar el inventario. En un recorrido de 89 movimientos por una cripta de 100 salas hubo 185 consultas resueltas en memoria, unas 2 por movimiento (ver §4.3). Por eso **averiguar si una ficha está en memoria es la operación más frecuente** y su costo importa. En memoria solo caben `--cache-size` fichas (25 por defecto): al llegar a ese tope hay que liberar alguna, pero nunca una que esté en uso (un enemigo vivo, un objeto del inventario, un objeto o una trampa de la sala actual). Una ficha liberada no debe volver a costar una solicitud de red: tiene que poder recuperarse del disco. Además, la caché debe sobrevivir al cierre del programa y validarse con la versión del catálogo y de la cripta sin descargar todo otra vez.

### Alternativas consideradas
1. **Para encontrar una ficha: recorrer una lista sin orden** contra **un arreglo ordenado por id con búsqueda binaria** (`VectorOrdenado`). Una tabla hash (el `dict` de Python, que encuentra un elemento sin recorrer nada) no es opción, porque §7 prohíbe usar `dict` como índice o caché. Se midieron las dos (ver Evidencia): con 25 fichas el recorrido es un poco más rápido, pero con 1000 es 8.5 veces más lento. Se descartó el recorrido porque su costo crece con la cantidad de fichas, y esa cantidad la elige el usuario con `--cache-size`.
2. **Para llevar el orden de uso: una lista de Python** (quitar la ficha con `list.remove` y volver a meterla al frente con `insert`) contra **una lista doblemente enlazada**, en la que cada elemento (nodo) apunta al anterior y al siguiente. Con la lista de Python hay que buscar la ficha y correr todos los elementos de lugar; con la lista doble basta desconectar el nodo y conectarlo al frente. Se midieron las dos: con 25 fichas la lista de Python es un poco más rápida, con 1000 es 19 veces más lenta. Se descartó por la misma razón.
3. **Qué ficha liberar: FIFO** (*first in, first out*: se libera la que entró primero) contra **LRU** (*least recently used*: se libera la que lleva más tiempo sin usarse). FIFO es más simple, pero puede liberar una ficha que se usa todo el tiempo (por ejemplo la de la rata, que aparece en muchas salas) solo porque llegó temprano. Se eligió LRU porque el jugador vuelve a salas cercanas y los mismos tipos se repiten. Esta comparación no se midió (ver Límites).
4. **Para guardar en disco: un solo archivo con todo el catálogo** contra **un archivo por ficha con la versión en el nombre**. El archivo único obliga a leerlo y reescribirlo completo para recuperar o agregar una ficha, y al cambiar la versión habría que invalidarlo entero. Se eligió un archivo por ficha.

### Decisión
La caché en memoria usa dos estructuras, cada una con un trabajo:
- **Índice (para encontrar una ficha):** las fichas en memoria se guardan en un `VectorOrdenado` ordenado por id. Saber si una ficha está en memoria es una búsqueda binaria en ese arreglo, como buscar en el índice de un libro en lugar de recorrer todas las páginas.
- **Orden de uso (para saber cuál liberar):** una `ListaDobleEnlazada` con las fichas de la más usada recientemente (al frente) a la menos usada (al final). Cada entrada del índice guarda su nodo de esta lista, así que al consultar una ficha se la pasa al frente sin buscarla otra vez.

Las reglas:
- **Cuál se libera (LRU):** cuando hay más fichas que el tope, se revisa la lista desde el final (la que lleva más tiempo sin usarse) y se libera la primera que no esté en uso. La ficha que acaba de entrar nunca se libera. Si todas están en uso, la caché se queda temporalmente con más fichas que el tope, porque el enunciado prohíbe soltar una ficha en uso.
- **Fichas en uso:** se obtienen del estado de la partida. `Partida.fichas_en_uso()` junta los ids del inventario, del suelo y las trampas de la sala actual y de los enemigos vivos, y `ServicioPartida` se la entrega al catálogo como una función que solo se consulta al liberar, no en cada acceso. El catálogo se crea antes que la partida, por eso recibe la función y no la partida. Al liberar, cada ficha en uso se marca, se elige cuál sale y las marcas se quitan enseguida.
- **Disco (`CacheDisco`):** un archivo por ficha, con la versión del catálogo dentro del nombre (`catalogo.<versión>.<id>.json`). El esqueleto y el contenido de las salas se guardan igual, con la versión de la cripta. Si la versión del servidor cambió, el archivo con el nombre nuevo simplemente no existe y la ficha se pide a la red; los archivos viejos no molestan y no hace falta recorrer el disco para invalidar nada. Un archivo dañado (que ya no es JSON válido) cuenta como "no está": se vuelve a pedir en lugar de detener la partida.
- La versión del catálogo se consulta una sola vez al iniciar (hace falta para el encabezado de la bitácora y para validar el disco) y se entrega ya conocida al catálogo.

### Análisis de complejidad
Letras usadas: **n** = fichas en memoria (como mucho `--cache-size`, salvo cuando todas están en uso); **u** = fichas en uso en el momento de liberar; **s** = salas de la cripta.
- **Consultar una ficha que está en memoria** (la operación más frecuente): O(log n) por la búsqueda binaria en el índice (con 25 fichas, unas 5 comparaciones), más O(1) para pasarla al frente de la lista de uso. O(1) significa que cuesta lo mismo sin importar cuántas fichas haya.
- **Agregar una ficha nueva** (solo después de que no estaba): O(n), porque al meterla en su lugar del arreglo ordenado hay que correr una posición a las que van detrás. Pasa una vez por ficha descargada o recuperada, no en cada consulta.
- **Liberar una ficha:** marcar las fichas en uso cuesta O(u log n) (una búsqueda binaria por cada una), y buscar cuál liberar desde el final de la lista cuesta O(n) en el peor caso (si casi todas están en uso). Obtener la lista de fichas en uso cuesta O(s), porque recorre las salas buscando enemigos vivos. Todo esto solo ocurre cuando se supera el tope.
- **Recuperar una ficha liberada:** leer un archivo pequeño y convertirlo desde JSON. No depende de cuántas fichas haya en disco.

### Evidencia empírica
- `--bench --solo cache disco` (Intel Core Ultra 7, 16 GB, Python 3.14.6; 20 000 operaciones por caso; µs = microsegundos, millonésimas de segundo):

  | Operación | Fichas | Elegida | Descartada | Resultado |
  |---|---|---|---|---|
  | Buscar una ficha | 25 | `VectorOrdenado`: 0.86 µs | recorrido lineal: 0.53 µs | el recorrido es 1.6 veces más rápido |
  | Buscar una ficha | 1000 | `VectorOrdenado`: 1.24 µs | recorrido lineal: 10.57 µs | el recorrido es 8.5 veces más lento |
  | Pasar una ficha al frente (LRU) | 25 | lista doble: 0.25 µs | `list.remove` + `insert`: 0.16 µs | la lista de Python es 1.5 veces más rápida |
  | Pasar una ficha al frente (LRU) | 1000 | lista doble: 0.15 µs | `list.remove` + `insert`: 2.86 µs | la lista de Python es 19 veces más lenta |

  Recuperar una ficha liberada desde disco (leer el archivo y convertirlo desde JSON): **50.68 µs**, contra ~400 ms (400 000 µs) de una solicitud de red: unas 8000 veces menos.
- Cómo leer la tabla: con el tope por defecto, las alternativas simples son algo más rápidas, pero la diferencia es de fracciones de microsegundo por consulta, nada frente al límite de 20 ms por ciclo (§5.2). Con 1000 fichas, lo elegido es entre 8 y 19 veces más rápido. Con la lista doble, pasar una ficha al frente cuesta lo mismo con 25 que con 1000 fichas (0.25 y 0.15 µs).
- Solicitudes de red al iniciar una partida en la cripta de pruebas (6 salas, presupuesto 9), contando cada llamada del cliente de archivos como una solicitud. Sin nada en la caché de disco: 6 (datos generales, versión del catálogo, una página de esqueleto, un lote de contenido y dos lotes de catálogo). Con la caché de disco llena: 2 (datos generales y versión del catálogo), y todo lo demás sale del disco. Con un tope de 3 fichas en memoria y disco, una partida de 7 acciones liberó 11 fichas, recuperó 3 del disco y no hizo ninguna solicitud extra; sin disco, con ese mismo tope, se agotó el presupuesto de 9 al volver a descargar fichas liberadas (`tests/servicios/test_servicio_partida.py`).
- Tests de la política y del disco:
  - `tests/servicios/test_servicio_catalogo.py`: sale la que lleva más tiempo sin usarse; usar una ficha la salva; una ficha en uso no sale; si todas están en uso se supera el tope; la marca de "en uso" no queda puesta después de liberar.
  - `tests/infraestructura/test_cache_disco.py`: otra versión del catálogo no ve lo guardado; un archivo dañado cuenta como ausente.

### Límites conocidos
- Con el tope por defecto (25), un recorrido lineal y una lista de Python serían algo más rápidos que lo elegido. Se mantiene lo elegido porque el tope lo decide el usuario con `--cache-size` y su costo casi no crece; si el tope fuera siempre pequeño, la alternativa simple bastaría.
- Sin caché en disco, un tope menor que las fichas distintas que necesita la partida hace que cada ficha liberada que se vuelve a necesitar cueste una solicitud: la caché en disco es lo que hace viable un tope pequeño.
- Un enemigo cuya ficha se liberó mientras dormía conserva su propia referencia y no la necesita de la caché.
- `fichas_en_uso` recorre las salas para encontrar enemigos vivos, así que cada liberación cuesta O(s). Es aceptable porque solo ocurre al superar el tope; si la cripta tuviera miles de salas, lo primero a mejorar sería llevar una lista de enemigos activos.
- No se midió cuántas veces más encuentra la ficha en memoria LRU frente a FIFO: la elección se apoya en que el jugador se mueve entre salas cercanas y los tipos se repiten, no en una medición.
- Si todas las fichas en memoria están en uso, la caché se queda por encima del tope hasta que alguna deja de estarlo.
- Los archivos de versiones viejas del catálogo no se borran: no estorban, pero ocupan disco.


## 4.5 Inventario
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión


### Decisión
Pendiente — completar en reunión (revisar para eliminar esta linea)

El inventario usa una lista doble enlazada con un nodo por objeto. Para soltar el objeto que se está viendo en O(1), el inventario conserva el nodo que devuelve `agregar`, y la lista mantiene su tamaño para aplicar el límite `inventario_max` sin recorrerla.

El jugador recorre el inventario con un cursor sobre los nodos (O(1) por paso). Para acciones sobre un objeto concreto (usar, equipar, soltar por posición) existe `ir_a_posicion`, que recorre la lista desde el principio: cuesta O(n), pero n está acotado por `inventario_max`, que es pequeño. Los pergaminos se cuentan y se consumen por clase (`cantidad_pergaminos`, `quitar_primero_de_clase`), sin tocar el historial de retroceso (§2.11). Las vistas ordenadas trabajan sobre una copia con el selector automático de ordenamiento; el orden por nombre ignora mayúsculas y tildes para que el resultado sea el que espera una persona. `fichas_en_uso` expone los ids de catálogo que el inventario mantiene referenciados, para que la caché no los libere (§4.4).

Usar un objeto consumible (poción, antídoto, antorcha) lo saca del inventario sin dejarlo en el suelo. Un antídoto sin veneno activo se rechaza sin consumir tiempo ni el objeto; una segunda antorcha no se puede encender mientras hay una encendida. Los objetos recogidos reciben un id de instancia determinista (un contador de la partida). Las acciones por posición (usar, equipar, soltar) llevan el índice del objeto en el orden real, para que la acción sea reproducible en el replay.


### Análisis de complejidad
Pendiente — completar en reunión

Recorrer, recoger, soltar el objeto actual y equipar cuestan O(1). Ir a una posición, contar por clase, quitar el primero de una clase y listar fichas en uso cuestan O(n), con n <= inventario_max. Una vista ordenada cuesta lo que cueste el algoritmo elegido por el selector sobre n elementos.


### Evidencia empírica
Pendiente — completar en reunión


### Límites conocidos
Pendiente — completar en reunión

Con un inventario pequeño (`inventario_max` típico de unas decenas) una lista contigua (`list`) competiría con la lista doble: en el bench, soltar en el medio con n=10 cuesta 0.40 µs con la lista doble y 0.08 µs con `list.pop`. La ventaja de la lista doble solo aparece con inventarios muy grandes, donde `list.pop` mueve muchos elementos; una medición propia sin contar la construcción dio, soltando en el medio, 0.50 µs (lista doble) contra 0.39 µs (`list.pop`) con n=10 000, y 0.52 contra 7.73 µs con n=100 000. Esa medición habrá que repetirla con el bench corregido, porque el actual incluye la construcción de la lista dentro del tiempo medido (por eso con n=10 000 el bench actual muestra a la lista doble como más lenta).

Las operaciones por posición y por clase recorren la lista; si `inventario_max` creciera mucho, convendría un índice auxiliar.



## 4.6 Pergaminos de retroceso e historial reversible
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión


### Decisión
Pendiente — completar en reunión (revisar para eliminar esta linea)

El historial guarda un intervalo por cada acción del jugador. Cada intervalo es una pila de operaciones inversas (funciones que deshacen un cambio), y los intervalos se guardan en una lista acotada a 5 (`RETROCESO_MAX_ACCIONES`); al pasar el límite se descarta el más antiguo. No se guardan copias del estado, solo lo necesario para invertir cada cambio.

Deshacer un intervalo ejecuta sus inversas en orden LIFO, de modo que lo último que ocurrió se revierte primero. El historial es estricto: registrar un cambio sin un intervalo abierto, o abrir un intervalo con otro ya abierto, lanza `CriptaHistorialError`. Así un cambio que no se podría deshacer no pasa desapercibido.

Para que el reloj pueda revertirse, expone `restaurar` (tiempo y contador de secuencia) y `restituir` (devuelve un evento cancelado o ya ejecutado a la agenda con su mismo `(tiempo, secuencia)`).

Cada objeto del modelo que cambia durante la partida sabe deshacer sus propios cambios. Una base común (`Reversible`) intercepta la asignación de atributos y, si el objeto tiene un registrador, guarda solo el valor que pisa; los cambios que no son asignaciones (agregar o quitar de una lista, mover un nodo del inventario, programar o ejecutar un evento) registran su inversa explícita. El historial entrega un gancho (`registrar_cambio`) que ignora los cambios fuera de un intervalo, mientras se revierte y dentro de un bloque `sin_registrar()`, pensado para no deshacer la carga de contenido ni las operaciones con pergaminos. Las inversas del inventario buscan el nodo por su objeto y no por el nodo guardado, porque reponer un objeto crea un nodo nuevo.

El motor abre un intervalo por cada acción del jugador aceptada y lo cierra cuando le vuelve a tocar decidir; una acción rechazada descarta su intervalo, porque no cambia nada. Todo lo que cambia durante el intervalo (reloj, agenda, vida, posición, rastro, puertas, trampas, suelo, inventario, enemigos y los contadores de la partida) registra su inversa; el estado del generador aleatorio también se restaura, de modo que repetir una acción tras retroceder da el mismo resultado y el pergamino no sirve para volver a tirar los dados. La carga de contenido de una sala y las operaciones con pergaminos se hacen dentro de `sin_registrar()`: cargar contenido es infraestructura y no estado del juego, y recoger o soltar un pergamino no se deshace (§2.11). Usar un pergamino primero revierte el último intervalo y después descuenta el pergamino, fuera del historial; no consume tiempo ni cuenta como acción. Sin pergamino, o sin intervalos que deshacer, se rechaza sin consumir nada; el historial guarda como máximo 5 intervalos.  

Si la infraestructura falla a mitad de una acción (por ejemplo, se agota el presupuesto al pedir una ficha cuando el jugador ya entró a la sala), el intervalo abierto se revierte con las mismas inversas del retroceso en lugar de descartarse, de modo que la acción no deja cambios a medias y se puede reintentar. Una acción rechazada no cambió nada y su intervalo solo se descarta.


### Análisis de complejidad
Pendiente — completar en reunión (revisar para eliminar esta linea)

Registrar un cambio es O(1) (apilar una operación inversa). Deshacer un intervalo cuesta O(k), con k el número de cambios de ese intervalo, y no depende del tamaño de la cripta ni de la cantidad de actores.


### Evidencia empírica
Pendiente — completar en reunión (revisar para eliminar esta linea)

Medición con `--bench` (escala 0.3), contra la alternativa descartada y prohibida por §4.6 (guardar una copia completa del estado, aquí con 200 salas y 60 actores): registrar una acción con operaciones inversas cuesta 2.17 µs, y con copia completa 1199 µs, o sea 553 veces más lenta, además de guardar 5 estados enteros. Deshacer 5 acciones (30 operaciones inversas) cuesta 3.34 µs por deshacer.

Alternativa descartada, medida con `--bench`: usar la base `Reversible` (que intercepta cada asignación) también en el reloj de eventos subió el ciclo con 600 actores activos de unos 7 ms a 17 ms, cerca del límite de 20 ms de §5.2. Por eso el reloj, que es la parte más caliente, registra sus inversas de forma explícita con un solo `if` por operación, y el ciclo volvió a 7.5 a 8.7 ms.

Costo de los ganchos medido con `--bench` (600 actores activos, mediana de 6 corridas): con la base `Reversible` en los actores el ciclo tomó unos 8.5 ms y sin ella unos 7.7 ms, es decir, el mecanismo agrega cerca de un 10 %, muy por debajo del límite de 20 ms. Los tests de tests/modelo comprueban los casos del Apéndice B: dos pergaminos seguidos, pergamino recogido o soltado dentro del intervalo y el tope de 5 acciones.


### Límites conocidos
Pendiente — completar en reunión (revisar para eliminar esta linea)

Si una operación inversa falla a mitad de un deshacer, la excepción no se captura: el intervalo ya salió de la pila y el estado puede quedar a medias. Se considera un error de programación, no una condición normal del juego. Una solución más robusta sería aplicar las inversas sobre una copia del estado o poder reanudar el deshacer.

La medición compara el costo de registrar, no un retroceso completo del juego: esta evidencia habrá que repetirla cuando el motor registre inversas reales de reloj, vida, puertas y trampas.

Cada acción del jugador guarda el estado del generador aleatorio (unos 625 enteros) además de las inversas; con un historial de 5 intervalos es poca memoria, pero sería lo primero a revisar si el límite de retroceso creciera mucho. Los efectos que no existen en los datos del API (el veneno, que ningún objeto ni trampa origina) están preparados para retroceder, pero solo se probaron de forma unitaria.

Los mensajes de la bitácora en pantalla no forman parte del estado reversible: tras retroceder o tras revertir una acción fallida, un mensaje ya mostrado (por ejemplo «Entras a ...») permanece. Tampoco se deshace que una sala figure como cargada, porque es infraestructura.


## 4.7 El rastro del jugador
### Problema
Pendiente — completar en reunión (revisar para eliminar esta linea)

Cada sala guarda el instante de la última visita del jugador (`rastro_ultima_visita`), y el rastro se refresca por cada acción del jugador. La caducidad se detecta al consultar el rastro (`rastro_es_fresco`, antigüedad menor que 400) y no se elimina activamente: no hay que programar eventos de borrado ni recorrer salas, y la consulta es O(1) por sala.

En su turno, un rastreador mira únicamente las salas vecinas conectadas por salidas abiertas (`puerta_transitable`), descarta las de rastro vencido o inexistente, y se mueve hacia la de rastro más reciente; con rastros iguales gana la sala de menor id (§2.9). Si ninguna sirve, espera. No conoce el mapa ni busca rutas. La decisión vive en un módulo aparte (`comportamiento_enemigo.py`) que solo decide: ejecutar la acción y reprogramar el turno lo hace el motor.


### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión (revisar para eliminar esta linea)

Una decisión del rastreador examina como mucho 4 salidas, así que su costo no depende de la longitud del recorrido del jugador ni de la cantidad de salas visitadas. Con varios rastreadores, el trabajo por ciclo crece linealmente con los enemigos que realmente actúan (cada uno hace una decisión de a lo sumo 4 vecinos). Cada vecino se localiza en el mapa con búsqueda binaria, es decir O(log n) con n salas.


### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión (revisar para eliminar esta linea)

Estrictamente, §4.7 pide costo proporcional al número de salidas; localizar cada vecino con búsqueda binaria agrega un factor O(log n) en el tamaño de la cripta. Si esto pesara con criptas muy grandes, la mejora es que cada sala guarde referencias directas a sus salas vecinas. Un comportamiento de enemigo desconocido se trata como guardián (espera), para que un valor nuevo del API no detenga la partida. El errante consume el generador aleatorio solo cuando tiene al menos una salida abierta, y una sola vez, para que el replay sea idéntico.



## 4.8 Bitácora en pantalla
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.9 Ordenamiento
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión

### Decisión
Pendiente — completar en reunión (revisar para eliminar esta linea)

El ranking de la tabla de puntajes ordena con el selector automático una tupla (grupo, tiempo, orden de registro): primero las victorias y luego las derrotas, menor tiempo primero, y el orden de registro desempata para que el resultado sea estable. Solo incluye los puntajes de la cripta y la versión jugadas.


### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.10 Guardado binario de la partida
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión
### Decisión
Pendiente — completar en reunión (revisar para eliminar esta linea)

La partida viva se convierte a datos planos (`EstadoPartida`) en un módulo del modelo (`persistencia_modelo.py`), que no escribe archivos: eso lo hace `GuardadoBinario`. La agenda del reloj contiene funciones, que no se pueden escribir en disco, así que cada evento declara al programarse un descriptor (tipo, sujeto y dos números) y la agenda se guarda como esos descriptores; un evento sin descriptor produce un error en lugar de perderse en silencio. Solo se guardan como cargadas las salas a las que el jugador llegó: el contenido que solo se precargó es estado de la caché y se vuelve a pedir al cargar. No se guarda el historial de retroceso, de modo que tras cargar el pergamino no deshace acciones anteriores al guardado. Solo se puede guardar con la partida en curso y cuando al jugador le toca decidir, por lo que no hay un evento de turno del jugador pendiente.

Cargar una partida reconstruye el modelo a partir del `EstadoPartida`. Se piden de nuevo el contenido y las fichas de las salas visitadas y el estado guardado manda sobre lo recién creado: suelo, trampas, enemigos (dormidos y activos), puertas, rastro, inventario con su equipo y su cursor, y estadísticas del jugador. Las acciones de la agenda, que son funciones, se recrean a partir de su descriptor con la misma pareja (tiempo, secuencia) con que se guardaron, y el estado del generador aleatorio se repone para que la partida continúe con la misma secuencia de azar. La carga se hace sin registrar inversas, de modo que no hay nada que el pergamino pueda deshacer de ella. Si el id o la versión de la cripta no coinciden con los guardados, se informa la incompatibilidad en lugar de cargar. Un enemigo activo que llegó caminando a una sala que el jugador nunca visitó se guarda con esa sala, porque es estado del juego y no de la caché.

Guardar y cargar pasan por el servicio de partida. Cargar valida primero el archivo, la versión de la cripta y la del catálogo con que se guardó, y solo entonces reemplaza la partida en curso, así un fallo de validación no destruye la partida actual. Las salas visitadas se piden de nuevo a la precarga (de disco si la caché está caliente) y después se pisan con el estado guardado. Las salas que solo se precargaron no se guardan como cargadas, porque son estado de la caché.


### Análisis de complejidad
Pendiente — completar en reunión

### Evidencia empírica
Pendiente — completar en reunión (revisar para eliminar esta linea)

La prueba de ida y vuelta (tests/modelo/test_guardado_vuelta.py) compara una partida que se guardó y se cargó contra otra que nunca se guardó: tras las mismas acciones tienen el mismo estado completo, la misma vista y los mismos mensajes. Cubre trampas, antorcha, puerta con cierre automático, veneno, cambio de velocidad, un enemigo en una sala sin visitar y el paso por el archivo binario.

Cargar un guardado en frío, sin caché de disco, con 3 salas visitadas en la cripta de pruebas (presupuesto 9), costó 6 solicitudes (datos generales, versión del catálogo, esqueleto, un lote de contenido y dos de catálogo), igual que iniciar una partida nueva. La partida cargada y la que nunca se guardó dan el mismo estado antes y después de seguir jugando (tests/servicios/test_servicio_partida_guardado.py).


### Límites conocidos
Pendiente — completar en reunión (revisar para eliminar esta linea)

El pergamino de retroceso no puede deshacer acciones anteriores a una partida cargada, porque el historial (solo inversas, nunca copias del estado) no se guarda. Guardar solo es posible con la partida en curso.

El contador de ids de los objetos recogidos no forma parte del archivo de guardado: al cargar se retoma después del mayor id que queda en el inventario, de modo que nunca se repite un id existente, pero puede diferir del que habría tenido una partida que nunca se guardó. Cargar vuelve a pedir el contenido de las salas visitadas, lo que consume solicitudes si no están en el disco. Los efectos del veneno y del cambio de velocidad se probaron con efectos creados a mano, porque la cripta publicada no trae nada que los origine.

Al cargar se vuelve a pedir el contenido de las salas visitadas: con la caché de disco vacía cuesta hasta un lote por cada diez salas visitadas, más los lotes de fichas, y no se midió en una cripta grande. Los identificadores de instancia de los objetos recogidos después de cargar pueden diferir de los de una partida continua; no se muestran ni intervienen en ninguna acción.


## 4.11 Bitácora de partida y reproducción
### Problema
Pendiente — completar en reunión
### Alternativas consideradas
Pendiente — completar en reunión

### Decisión
Pendiente — completar en reunión (revisar para eliminar esta linea)

`ServicioPartida` escribe la bitácora: tras ejecutar una acción, si el modelo la acepta, la anota (incluido el pergamino, que cambia el estado y debe repetirse en el replay); las rechazadas no cambian el estado y no se anotan. El encabezado se escribe cuando la partida ya inició sin errores, con el id y la versión de la cripta, la versión del catálogo y la semilla; si no se da semilla se genera con un generador del sistema y queda en el encabezado. Sin ruta de bitácora (replay y bench) no se escribe nada.

El guardado lleva consigo una copia de la bitácora hasta el instante de guardar (archivo del guardado más `.log`). Cargar la restaura como bitácora activa y la partida sigue anexando en ella. Se descartó recortar la bitácora original por el número de acciones del jugador, porque el log también anota el pergamino y las acciones que luego se deshicieron, así que no coincide con ese contador; guardar el número de líneas habría exigido cambiar el formato del guardado, y poner marcas dentro del log habría obligado al lector a distinguirlas de las acciones. Con la copia, la bitácora de una partida cargada es exactamente la historia que llevó a ese estado y se puede reproducir desde cero. Si la copia no existe, la bitácora nueva lleva `"parcial": true` en el encabezado y no es reproducible.


### Análisis de complejidad
Pendiente — completar en reunión

### Evidencia empírica
Pendiente — completar en reunión (revisar para eliminar esta linea)

tests/servicios/test_servicio_partida.py reproduce la bitácora de una partida en una partida nueva con la semilla del encabezado y compara el estado guardado, la vista y el puntaje: son iguales.

tests/servicios/test_servicio_partida_guardado.py guarda una partida, sigue jugando, carga el guardado y comprueba que la bitácora restaurada contiene solo las acciones hasta el guardado; después reproduce esa bitácora desde cero y obtiene el mismo estado que la partida cargada.


### Límites conocidos
Pendiente — completar en reunión (revisar para eliminar esta linea)

Los mensajes de una acción rechazada quedan en la bitácora en pantalla pero no en el log, por lo que una partida reproducida puede diferir de la original solo en esos mensajes; el estado, la vista y el puntaje coinciden.

Solo se comprueba que el encabezado de la copia coincida con el del guardado; no se puede verificar que la copia tenga exactamente las acciones que llevaron a ese estado. Una bitácora parcial no se puede reproducir.
