# Documento de Decisiones de Diseño — CRIPTA


## Cómo leer este documento


**Términos.** *µs* y *ms* son millonésimas y milésimas de segundo. *Mediana*: el valor del medio de varias corridas (no la afecta una corrida atípica). *Peor caso*: la corrida o el ciclo más lento de un conjunto. *O(...)* describe cómo crece el costo con el tamaño: O(1) no crece, O(log n) crece muy despacio, O(n) crece en proporción. *n* es la cantidad de elementos de la estructura que se está midiendo; las demás letras se definen en cada sección. *Lote*: una sola solicitud al API que lleva hasta 10 elementos. *Alternativa descartada*: la opción que se midió contra la elegida para justificar la decisión.


**Cómo se reproduce.** `python -m cripta --bench` corre todas las cargas; `python -m cripta --bench --solo <carga> --escala <factor>` corre una (cargas: agenda, cache, disco, inventario, historial, historial_cazadores, ordenamiento, guardado, ciclo, partida, solicitudes, ruta_cazador, invalidacion, ciclo_referencia, niebla_rutas, linea_tiempo, resolubilidad, resolubilidad_cota). Los conteos de solicitudes no dependen del equipo; los tiempos sí, por eso se reportan medianas de varias corridas y el equipo usado.


**Equipos de medición.**


| Equipo | Hardware y sistema | Python | Se usó en |
|---|---|---|---|
| A | Ryzen 5 5600GT, 32 GB, Windows | 3.12.10 | 4.1, 5.3 |
| B | Intel Core Ultra 7, 16 GB, Windows | 3.14.6 | 4.1, 4.2, 4.4, 4.9, 4.10, 5.1, 5.2, 5.4, 5.5, 5.6 |
| C | Linux | 3.12 | 4.5, 4.6, 4.7, 4.8 |


Cada sección indica en qué equipo se midió, y las cifras de equipos distintos no se comparan entre sí. Las mediciones del Equipo C que no salen de `--bench` se hicieron con un script propio y se indican como tales en su sección. Los conteos de operaciones por acción ("frecuencia medida") salen de un script que cuenta llamadas sobre la partida real y no dependen del equipo.


Las cifras de la sección 5.3 se midieron en el Equipo A con Python 3.14.7, a diferencia de la versión que figura en su fila.


## 4.1 Qué ocurre a continuación (agenda de eventos)


### Problema


El juego avanza ejecutando siempre el evento pendiente con menor `(tiempo, secuencia)`, y esa operación se repite decenas de miles de veces por partida, con varios cientos de eventos simultáneos. Además hay que poder cancelar eventos (muerte de un actor, antídoto, fin de efecto) y reprogramarlos (cambio de velocidad) sin recorrer la agenda y sin perder el orden determinista.


### Alternativas consideradas


1. **Lista lineal desordenada**: programar es O(1), pero extraer el siguiente exige recorrerla entera. Se descartó porque la extracción es la operación más frecuente; en la medición con `--bench` es 1.5x, 5.7x y 15.6x más lenta que el montículo con 100, 500 y 2000 eventos.
2. **Lista ordenada (inserción ordenada)**: extraer es O(1), pero cada inserción desplaza elementos, O(n), y hay una inserción por cada acción de cada actor. Se descartó por el mismo motivo, con la peor relación en las operaciones que más se repiten. No se midió por separado.
3. **Cancelación activa** (sacar el evento del montículo al cancelar): exigiría localizarlo dentro del montículo, lo que obliga a guardar posiciones. Se descartó por la cancelación (marcar y descartar al salir), que cuesta O(1) y no necesita ese índice; el precio es que los cancelados ocupan espacio hasta salir (ver Límites).


### Decisión


#### Agenda


La agenda es un montículo mínimo (`HeapMinimo`, implementación propia) ordenado por la pareja `(tiempo, secuencia)`. El número de secuencia lo asigna el reloj al programar cada evento, así que el orden es total y determinista aunque haya empates, cancelaciones o reprogramaciones.


Cancelar un evento solo marca `cancelado = True`; el evento se descarta cuando sale del montículo. Reprogramar cancela el evento viejo y agenda uno nuevo con secuencia nueva (2.3). Cuando un enemigo muere, el motor cancela su evento pendiente (ver "Muerte de enemigos y velocidad del jugador" más abajo), así que no hace falta recorrer la agenda; como segunda defensa, el turno de un enemigo comprueba `esta_vivo()` y no hace nada si ya murió. El reloj lleva un contador de eventos vigentes, de modo que `esta_vacia()` no tiene que recorrer la agenda.


#### Efectos


Efectos: un veneno nuevo reemplaza al anterior y reinicia su duración (no se acumula el daño), y el actor guarda cuál es su veneno activo para que el antídoto pueda cancelarlo. Los cambios de velocidad restan al terminar lo que ellos mismos sumaron, así varios efectos solapados no se pisan, y la velocidad nunca baja de `VELOCIDAD_MINIMA` (1).


#### Turno jugador


El turno del jugador es un evento más de la misma agenda: se programa en tiempo 0 al iniciar la partida y, tras cada acción aceptada, se programa el siguiente con `intervalo = max(1, costo * 100 // velocidad)`. Un motor (`Partida`) ejecuta eventos hasta que vuelve a tocar el turno del jugador; así el orden entre jugador y enemigos sale solo de `(tiempo, secuencia)`. Las acciones rechazadas (por ejemplo, una acción aún no permitida) no consumen tiempo ni cambian el estado. Cada enemigo decide en su turno con un módulo aparte (`comportamiento_enemigo.py`) y el motor ejecuta lo decidido y reprograma su siguiente turno con costo 100.


#### Trampas y puertas


Las trampas y el cierre automático de puertas también son eventos de la agenda: al activarse, una trampa desarma y programa su rearme con el intervalo de su ficha (300 si no declara otro), y una puerta con cierre automático programa su cierre al abrirse. El cierre actúa sobre los dos lados de la puerta; quien ya la cruzó se queda en su sala y solo se impide volver a atravesar. El daño de una trampa es fijo: no pasa por la defensa ni consume el generador aleatorio.


#### Muerte de enemigos y velocidad del jugador


Cuando un enemigo muere, el motor cancela su evento pendiente y lo saca de la sala, de modo que sus acciones futuras no ocurren y no hace falta recorrer la agenda. El turno del jugador guarda su propio evento pendiente (que se limpia cuando se ejecuta) para que un efecto de velocidad reescale solo una acción realmente programada (2.3). Las pociones de velocidad se aplican antes de calcular el siguiente turno del jugador.


El cierre automático de una puerta es un efecto (`EfectoCierrePuerta`) que cierra los dos lados de la salida a través del mapa, porque una salida conecta exactamente dos salas (2.1) y el API solo marca la puerta cerrada, la llave y el cierre en uno de sus lados. El motor sincroniza el estado de los dos lados al crear la partida. La regeneración de enemigos (2.10) está implementada como efecto, pero el esquema de enemigo del API no tiene ningún campo para declararla, así que con los datos actuales ningún enemigo la usa; queda como decisión conocida.


### Análisis de complejidad


Programar y extraer el siguiente evento cuestan O(log n) con n eventos en la agenda. Cancelar es O(1) y reprogramar es O(log n). `esta_vacia()` es O(1) gracias al contador de eventos vigentes. Las operaciones más frecuentes del juego, extraer el siguiente evento y programar el siguiente turno del actor, son las que cuestan O(log n).


### Evidencia empírica


Medición con `--bench` (escala 0.3), heap contra lista lineal (alternativa descartada): con 100, 500 y 2000 eventos pendientes la lista lineal es 1.5x, 5.7x y 15.6x más lenta. Con 600 actores activos (1200 eventos) el peor ciclo tomó 6.17 ms, bajo el límite de 20 ms de 5.2 (carga sintética). Cancelar un tercio de los eventos y reprogramar otro tercio, de forma perezosa, cuesta 0.33 µs por operación.


Rendimiento del ciclo (5.2), medido con `--bench --solo ciclo` (escala 0.3, Python 3.12.10, Ryzen 5 5600GT con 32 GB de RAM), con 600 actores activos y 1200 eventos por ciclo. Se reporta el peor de 20 ciclos en cada corrida. Primera serie de 5 corridas: 15.9, 7.1, 6.9, 23.3 y 7.1 ms (mediana 7.1 ms). Segunda serie de 5 corridas, con el recolector de basura desactivado: 6.9, 11.9, 7.5, 13.3 y 7.0 ms (mediana 7.5 ms). De las 10 corridas, 9 quedaron por debajo del límite de 20 ms y una (23.3 ms) lo superó.


Rendimiento con la partida real (5.2), medido con `--bench --solo partida --escala 0.5` (cripta artificial cuadrada recorrida en zigzag, Windows, Python 3.12.10, equipo en reposo, mediana de 5 ejecuciones de 3 corridas cada una): con 25 salas y 12 enemigos activos, la acción típica toma 0.23 ms y el peor caso 0.48 ms; con 100 salas y 60 enemigos, 1.35 ms y 9.19 ms; con 225 salas y 140 enemigos, 3.23 ms y 14.81 ms. Las tres cumplen el límite de 20 ms, y de las 15 corridas con 225 salas la peor tomó 19.02 ms.


### Límites conocidos


La cancelación es perezosa: los eventos cancelados siguen ocupando espacio en el montículo hasta que les toca salir. Con muchas cancelaciones sin consumir eventos, la agenda puede crecer más que el número de eventos vigentes (con 100 000 reprogramaciones, el montículo llegó a 100 001 entradas). Si eso fuera un problema, habría que compactar el montículo cada cierto número de cancelaciones.


No se puede programar un evento en un tiempo anterior al del reloj (se lanza `ValueError`). El retroceso del pergamino restaura el reloj con un método propio (`restaurar`) en vez de programar hacia atrás.


La medición del ciclo tiene picos aislados: desactivar el recolector de basura no los eliminó, por lo que no se deben a él, y no se determinó su causa (puede ser ruido del sistema, pues el equipo de medición no estaba dedicado a la prueba). Como el bench reporta el peor de 20 ciclos, un solo ciclo lento basta para que la corrida supere el límite; por eso la conclusión se apoya en la mediana de varias corridas y no en una sola, y conviene medir con el equipo en reposo y reportar también un percentil.


El límite de 20 ms se cumple hasta 225 salas con 140 enemigos activos y el peor caso crece con el tamaño de la cripta (0.48, 9.19 y 14.81 ms con 25, 100 y 225 salas). El caso de 400 salas, que en la Parte I no cumplía, se revisó con la carga nueva y se documenta en la sección 5.6.


**Frecuencia medida.** Se contaron las operaciones sobre la partida real (cripta artificial cuadrada recorrida en zigzag y 50 esperas). Promedio por cada acción del jugador:


| Salas | Acciones | Eventos extraídos de la agenda | Eventos programados | Decisiones de enemigos |
|---|---|---|---|---|
| 25 | 69 | 19.3 | 19.5 | 18.3 |
| 100 | 139 | 72.4 | 72.8 | 71.3 |
| 225 | 259 | 148.5 | 149.0 | 147.3 |


Extraer el siguiente evento y programar el siguiente turno del actor es, entonces, la operación más repetida, y su cantidad crece con los enemigos activos: con 225 salas son unas 150 extracciones por acción del jugador, es decir cerca de 38 000 en una partida de 259 acciones.


## 4.2 Traer el contenido antes de que haga falta (precarga)
### Problema
Para que el jugador entre a una sala, el programa necesita su contenido (enemigos, objetos, trampas) **antes** de confirmar el movimiento: nunca puede quedar en una sala cuyo contenido no conoce. El esqueleto de la cripta (qué salas hay y cómo se conectan) se descarga completo al iniciar, pero el contenido se pide aparte: cada solicitud tarda unos 400 ms, cuesta lo mismo con 1 sala que con 10 y cuenta contra el presupuesto. Si se pidiera al cruzar cada puerta, el jugador esperaría 400 ms en cada movimiento.


La operación que el programa ejecuta en cada movimiento es **revisar si conviene anticipar** contenido desde la sala nueva; pedir un lote ocurre mucho menos. En un recorrido de 89 movimientos por una cripta de 100 salas se revisó 89 veces y se pidieron 10 lotes. Además, puede haber una respuesta todavía en camino cuando el jugador se mueve: el programa debe esperarla sin caerse y sin que el tiempo real de red afecte el reloj virtual del juego, y las respuestas deben incorporarse siempre en el mismo orden para que la partida sea reproducible.


### Alternativas consideradas
1. **Pedir el contenido de cada sala al entrar** (una solicitud por sala, sin anticipar). Es lo más simple, pero gasta una solicitud por sala visitada y hace esperar ~400 ms en cada puerta. Se descartó; su costo en solicitudes se midió contra lo elegido (ver Evidencia).
2. **Pedir todo el contenido al empezar la partida.** Usa la misma cantidad de solicitudes que lo elegido (una cada 10 salas), pero obliga a esperarlas todas antes de jugar (con 1000 salas serían unos 40 s) y gasta presupuesto en salas que el jugador quizá nunca visite. Se descartó.
3. **Esperar la respuesta en el mismo hilo del juego** contra **pedirla en un hilo de red aparte** (un hilo es una tarea que el programa ejecuta en paralelo). En el mismo hilo, cada lote detiene el juego 400 ms aunque todavía no haga falta. En un hilo aparte, el lote viaja mientras el jugador piensa su siguiente acción. Se eligió el hilo aparte, pero el juego sigue siendo determinista.


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
- `--bench --solo solicitudes` y scripts aparte (cripta artificial, recorrido en zigzag; cuenta las solicitudes, no depende de la máquina):


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
- La anticipación mira 2 pasos a la redonda. Si el jugador se mueve sin pausa y la red es lenta, alcanza al hilo de red y espera (8 de 89 movimientos en la medición). Con una red mucho más lenta que 400 ms convendría mirar más lejos.
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
- Cada id descubierto se anota como **pendiente**: todavía no se pide, queda en espera para viajar en el próximo lote. Los pendientes se guardan en un `VectorOrdenado` (un arreglo ordenado por id, ver 4.4), así no hay repetidos y cada lote se arma siempre en el mismo orden. Se anotan al incorporar el contenido de una sala y al descargar la ficha de un enemigo, porque esa ficha dice qué objetos suelta: así esos objetos se conocen antes de que el enemigo muera.
- Al **consultar** una ficha se busca primero en memoria, después en el disco (con la versión del catálogo dentro del nombre del archivo, ver 4.4) y solo al final en la red. Si hay que ir a la red, la ficha que hace falta viaja junto con hasta 9 pendientes en **una sola solicitud**.
- Para preparar una sala se piden todas sus fichas de una vez, así las que faltan viajan juntas.
- Antes de armar un lote se quitan de los pendientes los ids que ya están en memoria o en el disco con la versión vigente: **un id vigente nunca se pide dos veces**.
- La versión del catálogo se consulta una sola vez por partida. Como el catálogo es global y el nombre del archivo en disco no incluye la cripta, una ficha descargada jugando una cripta sirve para las demás.


### Análisis de complejidad
Letras usadas: **n** = fichas guardadas en memoria (como mucho `--cache-size`, 25 por defecto); **p** = ids pendientes, es decir, descubiertos pero todavía no pedidos; **k** = fichas distintas que necesita la partida completa.
- **Consultar una ficha en memoria** (la operación más frecuente): O(log n), porque el índice es un `VectorOrdenado` y se busca con búsqueda binaria (con 25 fichas son unas 5 comparaciones). Además, mover la ficha al frente de la lista de uso cuesta O(1): no depende de cuántas fichas haya (ver 4.4).
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
- `cripta-01` sin nada en la caché de disco (todo se descarga): 2 lotes de catálogo en total al iniciar la partida (ver 4.4).
- Tests (`tests/servicios/test_servicio_catalogo.py`): tres ids descubiertos viajan en un solo lote; lo que ya está en memoria no genera solicitudes; contar aciertos y fallos da lo mismo pidiendo de a uno o todos juntos. En `tests/infraestructura/test_cache_disco.py`: una ficha dañada en disco se vuelve a pedir **en el mismo lote** que las que faltan.


### Límites conocidos
- La cripta artificial tiene solo 7 tipos de ficha, así que la ganancia medida es pequeña (4 lotes contra 7 solicitudes). Con muchos tipos distintos la diferencia puede llegar a 10 a 1, pero no se ha medido con una cripta de catálogo grande.
- Si los ids se descubrieran uno por uno justo cuando hacen falta, cada uno costaría un lote propio y la estrategia se acercaría a la alternativa descartada. Anotar lo que suelta cada enemigo al descargar su ficha reduce ese caso, pero no lo elimina.
- Insertar un id pendiente obliga a correr los que van detrás en el arreglo ordenado. Si una sola sala trajera cientos de ids nuevos, ese costo empezaría a notarse y convendría otra estructura; con las criptas probadas los pendientes son pocos y no pesa.
- La versión del catálogo cuesta una solicitud por partida, aunque todas las fichas estén en disco.


## 4.4 Reutilización y caché persistente
### Problema
Las fichas de catálogo se consultan todo el tiempo: al mostrar la sala, al preparar una sala nueva y al revisar el inventario. En un recorrido de 89 movimientos por una cripta de 100 salas hubo 185 consultas resueltas en memoria, unas 2 por movimiento (ver 4.3). Por eso **averiguar si una ficha está en memoria es la operación más frecuente** y su costo importa. En memoria solo caben `--cache-size` fichas (25 por defecto): al llegar a ese tope hay que liberar alguna, pero nunca una que esté en uso (un enemigo vivo, un objeto del inventario, un objeto o una trampa de la sala actual). Una ficha liberada no debe volver a costar una solicitud de red: tiene que poder recuperarse del disco. Además, la caché debe sobrevivir al cierre del programa y validarse con la versión del catálogo y de la cripta sin descargar todo otra vez.


### Alternativas consideradas
1. **Para encontrar una ficha: recorrer una lista sin orden** contra **un arreglo ordenado por id con búsqueda binaria** (`VectorOrdenado`). Una tabla hash (el `dict` de Python, que encuentra un elemento sin recorrer nada) no es opción: el enunciado (7) prohíbe usar `dict` como índice o caché, y una tabla hash propia no forma parte de las estructuras vistas en el curso hasta el momento del proyecto. Se midieron las dos (ver Evidencia): con 25 fichas el recorrido es un poco más rápido, pero con 1000 es 8.5 veces más lento. Se descartó el recorrido porque su costo crece con la cantidad de fichas, y esa cantidad la elige el usuario con `--cache-size`.
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
- Cómo leer la tabla: con el tope por defecto, las alternativas simples son algo más rápidas, pero la diferencia es de fracciones de microsegundo por consulta, nada frente al límite de 20 ms por ciclo (5.2). Con 1000 fichas, lo elegido es entre 8 y 19 veces más rápido. Con la lista doble, pasar una ficha al frente cuesta lo mismo con 25 que con 1000 fichas (0.25 y 0.15 µs).
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


El jugador recorre el inventario hacia adelante y hacia atrás desde la posición actual, suelta el objeto que está viendo en cualquier posición, equipa moviendo un objeto al frente y pide vistas ordenadas sin alterar el orden real. Además `inventario_max` limita cuántos objetos caben. La pregunta es qué estructura hace barato soltar y equipar sin depender de la posición del objeto.


**Frecuencia.** Cada acción del jugador ejecuta como máximo una operación sobre el inventario (recoger, soltar, equipar o usar un objeto); recorrerlo con `sig` y `ant` es una operación por comando, y una vista ordenada solo se calcula cuando el jugador la pide. El tamaño nunca supera `inventario_max` (10 en la cripta de pruebas). Por eso el inventario no es una operación repetida del ciclo de eventos.


### Alternativas consideradas


1. **Lista contigua (`list`)**: es la opción más simple y rápida con pocos objetos, pero soltar o mover al frente desplaza los elementos posteriores, O(n). Se descartó porque la posición del objeto no debería importar para el costo; con inventarios típicos la diferencia es despreciable (ver Evidencia), así que es una decisión de escalabilidad y no de velocidad actual.
2. **Lista enlazada simple**: soltar el objeto actual obligaría a conocer el nodo anterior, lo que cuesta un recorrido. Se descartó porque no permite recorrer hacia atrás ni soltar en O(1).
3. **Arreglo con marcas de borrado**: soltar sería O(1), pero el orden real se llenaría de huecos y equipar (mover al frente) exigiría reordenar. Se descartó por la complejidad extra.


### Decisión


El inventario usa una lista doble enlazada con un nodo por objeto. Para soltar el objeto que se está viendo en O(1), el inventario conserva el nodo que devuelve `agregar`, y la lista mantiene su tamaño para aplicar el límite `inventario_max` sin recorrerla.


El jugador recorre el inventario con un cursor sobre los nodos (O(1) por paso), de forma circular: después del último objeto `sig` vuelve al primero y `ant` desde el primero va al último. Para acciones sobre un objeto concreto (usar, equipar, soltar por posición) existe `ir_a_posicion`, que recorre la lista desde el principio: cuesta O(n), pero n está acotado por `inventario_max`, que es pequeño. Los pergaminos se cuentan y se consumen por clase (`cantidad_pergaminos`, `quitar_primero_de_clase`), sin tocar el historial de retroceso (2.11). Las vistas ordenadas trabajan sobre una copia con el selector automático de ordenamiento; el orden por nombre ignora mayúsculas y tildes para que el resultado sea el que espera una persona. `fichas_en_uso` expone los ids de catálogo que el inventario mantiene referenciados, para que la caché no los libere (4.4).


Usar un objeto consumible (poción, antídoto, antorcha) lo saca del inventario sin dejarlo en el suelo. Un antídoto sin veneno activo se rechaza sin consumir tiempo ni el objeto; una segunda antorcha no se puede encender mientras hay una encendida. Los objetos recogidos reciben un id de instancia determinista (un contador de la partida). Las acciones por posición (usar, equipar, soltar) llevan el índice del objeto en el orden real, para que la acción sea reproducible en el replay.


### Análisis de complejidad


Recorrer, recoger, soltar el objeto actual y equipar cuestan O(1). Ir a una posición, contar por clase, quitar el primero de una clase y listar fichas en uso cuestan O(n), con n <= inventario_max. Una vista ordenada cuesta lo que cueste el algoritmo elegido por el selector sobre n elementos.


### Evidencia empírica


Medición con `--bench --solo inventario` (soltar el objeto del medio y volver a agregar, sin contar la construcción de la lista; Linux, Python 3.12, mediana de 5 corridas): con n=10, la lista doble cuesta 0.34 µs por operación y `list.pop(i)` 0.06 µs (6x más rápida); con n=10 000, 0.42 µs y 0.31 µs (1.4x más rápida). Es decir, la alternativa descartada es más rápida a los tamaños con los que se juega. Una medición manual anterior con n=100 000 dio 0.52 µs para la lista doble y 7.73 µs para `list.pop`, que es donde la lista doble empieza a ganar; ese caso no está en el bench.


### Límites conocidos


Con un `inventario_max` típico (unas decenas) la lista doble no es más rápida que una lista contigua: según la medición, `list.pop` es entre 1.4x y 6x más rápida con n entre 10 y 10 000. La lista doble solo gana con inventarios muy grandes (del orden de 100 000 objetos, medición manual), así que esta decisión se justifica por el costo que no depende de la posición y no por velocidad con los datos reales de las criptas.


Las operaciones por posición y por clase recorren la lista; si `inventario_max` creciera mucho, convendría un índice auxiliar.


## 4.6 Pergaminos de retroceso e historial reversible


### Problema


El pergamino de retroceso devuelve el estado de la partida al punto anterior a la última acción del jugador, incluidos todos los eventos que ocurrieron antes de su siguiente decisión, hasta 5 acciones hacia atrás. Hay que hacerlo sin guardar copias completas del estado, y los pergaminos y la caché quedan fuera de lo que se revierte.


**Frecuencia medida** (mismo conteo que en 4.1, con un script que no forma parte de `--bench`). Cada acción del jugador registra, en promedio, 108 operaciones inversas con 25 salas, 414 con 100 y 859 con 225 (con 12, 60 y 140 enemigos activos al final). Deshacer una acción revierte esas operaciones, así que su costo depende de cuántos enemigos actuaron en el intervalo y no del tamaño de la cripta.


### Alternativas consideradas


1. **Copia completa del estado por acción**: es la más simple, pero 4.6 la prohíbe. Se midió igualmente como alternativa descartada: registrar una acción cuesta 1199 µs con copia completa (200 salas y 60 actores) frente a 2.17 µs con operaciones inversas, 553 veces más lenta, además de guardar 5 estados enteros.
2. **Reconstruir desde el inicio reproduciendo la bitácora**: no guarda estado extra, pero deshacer costaría reproducir toda la partida menos una acción, proporcional a su duración. Se descartó sin medir porque su costo crece con la partida y no con el tamaño del cambio.
3. **Registrar el cambio de cada atributo en un solo mecanismo para todo el modelo**: es lo que hace la base `Reversible`, y se adoptó para los actores y las salas. Para el reloj de eventos, la parte más caliente, se descartó y se registran inversas explícitas con un solo `if` (ver Evidencia).


### Decisión


El historial guarda un intervalo por cada acción del jugador. Cada intervalo es una pila de operaciones inversas (funciones que deshacen un cambio), y los intervalos se guardan en una lista acotada a 5 (`RETROCESO_MAX_ACCIONES`); al pasar el límite se descarta el más antiguo. No se guardan copias del estado, solo lo necesario para invertir cada cambio.


Deshacer un intervalo ejecuta sus inversas en orden LIFO, de modo que lo último que ocurrió se revierte primero. El historial es estricto: registrar un cambio sin un intervalo abierto, o abrir un intervalo con otro ya abierto, lanza `CriptaHistorialError`. Así un cambio que no se podría deshacer no pasa desapercibido.


Para que el reloj pueda revertirse, expone `restaurar` (tiempo y contador de secuencia) y `restituir` (devuelve un evento cancelado o ya ejecutado a la agenda con su mismo `(tiempo, secuencia)`).


Cada objeto del modelo que cambia durante la partida sabe deshacer sus propios cambios. Una base común (`Reversible`) intercepta la asignación de atributos y, si el objeto tiene un registrador, guarda solo el valor que pisa; los cambios que no son asignaciones (agregar o quitar de una lista, mover un nodo del inventario, programar o ejecutar un evento) registran su inversa explícita. El historial entrega un gancho (`registrar_cambio`) que ignora los cambios fuera de un intervalo, mientras se revierte y dentro de un bloque `sin_registrar()`, pensado para no deshacer la carga de contenido ni las operaciones con pergaminos. Las inversas del inventario buscan el nodo por su objeto y no por el nodo guardado, porque reponer un objeto crea un nodo nuevo.


El motor abre un intervalo por cada acción del jugador aceptada y lo cierra cuando le vuelve a tocar decidir; una acción rechazada descarta su intervalo, porque no cambia nada. Todo lo que cambia durante el intervalo (reloj, agenda, vida, posición, rastro, puertas, trampas, suelo, inventario, enemigos y los contadores de la partida) registra su inversa; el estado del generador aleatorio también se restaura, de modo que repetir una acción tras retroceder da el mismo resultado y el pergamino no sirve para volver a tirar los dados. La carga de contenido de una sala y las operaciones con pergaminos se hacen dentro de `sin_registrar()`: cargar contenido es infraestructura y no estado del juego, y recoger o soltar un pergamino no se deshace (2.11). Usar un pergamino primero revierte el último intervalo y después descuenta el pergamino, fuera del historial; no consume tiempo ni cuenta como acción. Sin pergamino, o sin intervalos que deshacer, se rechaza sin consumir nada: el historial guarda como máximo 5 intervalos.  


Si la infraestructura falla a mitad de una acción (por ejemplo, se agota el presupuesto al pedir una ficha cuando el jugador ya entró a la sala), el intervalo abierto se revierte con las mismas inversas del retroceso en lugar de descartarse, de modo que la acción no deja cambios a medias y se puede reintentar. Una acción rechazada no cambió nada y su intervalo solo se descarta.


### Análisis de complejidad


Registrar un cambio es O(1) (apilar una operación inversa). Deshacer un intervalo cuesta O(k), con k el número de cambios de ese intervalo, y no depende del tamaño de la cripta ni de la cantidad de actores.


### Evidencia empírica


Medición con `--bench` (escala 0.3), contra la alternativa descartada y prohibida por 4.6 (guardar una copia completa del estado, aquí con 200 salas y 60 actores): registrar una acción con operaciones inversas cuesta 2.17 µs, y con copia completa 1199 µs, o sea 553 veces más lenta, además de guardar 5 estados enteros. Deshacer 5 acciones (30 operaciones inversas) cuesta 3.34 µs por deshacer.


Alternativa descartada, medida con `--bench`: usar la base `Reversible` (que intercepta cada asignación) también en el reloj de eventos subió el ciclo con 600 actores activos de unos 7 ms a 17 ms, cerca del límite de 20 ms de 5.2. Por eso el reloj, que es la parte más caliente, registra sus inversas de forma explícita con un solo `if` por operación, y la mediana del ciclo volvió a 7.5 a 8.7 ms.


Costo de los ganchos medido con `--bench` (600 actores activos, mediana de 6 corridas): con la base `Reversible` en los actores el ciclo tomó unos 8.5 ms y sin ella unos 7.7 ms, es decir, el mecanismo agrega cerca de un 10 %, muy por debajo del límite de 20 ms. Los tests de tests/modelo comprueban los casos del Apéndice B: dos pergaminos seguidos, pergamino recogido o soltado dentro del intervalo y el tope de 5 acciones.


### Límites conocidos


Si una operación inversa falla a mitad de un deshacer, la excepción no se captura: el intervalo ya salió de la pila y el estado puede quedar a medias. Se considera un error de programación, no una condición normal del juego. Una solución más robusta sería aplicar las inversas sobre una copia del estado o poder reanudar el deshacer.


La medición de 2.17 µs contra 1199 µs usa una carga sintética que solo compara el costo de registrar. El costo con las inversas reales del motor (reloj, vida, puertas, trampas, inventario y azar) está incluido en las mediciones del ciclo con la partida real de 4.1, donde cada acción registra entre 108 y 859 inversas y el peor caso cumple los 20 ms hasta 225 salas. Lo que no se midió por separado es el tiempo de ejecutar un pergamino completo sobre la partida real; los tests comprueban que revierte bien, no cuánto tarda.


Cada acción del jugador guarda el estado del generador aleatorio (unos 625 enteros) además de las inversas; con un historial de 5 intervalos es poca memoria, pero sería lo primero a revisar si el límite de retroceso creciera mucho. Los efectos que no existen en los datos del API (el veneno, que ningún objeto ni trampa origina) están preparados para retroceder, pero solo se probaron de forma unitaria.


Los mensajes de la bitácora en pantalla no forman parte del estado reversible: tras retroceder o tras revertir una acción fallida, un mensaje ya mostrado (por ejemplo «Entras a ...») permanece. Tampoco se deshace que una sala figure como cargada, porque es infraestructura.


## 4.7 El rastro del jugador


### Problema


Cada sala guarda el instante de la última visita del jugador (`rastro_ultima_visita`), y el rastro se refresca por cada acción del jugador. La caducidad se detecta al consultar el rastro (`rastro_es_fresco`, antigüedad menor que 400) y no se elimina activamente: no hay que programar eventos de borrado ni recorrer salas, y la consulta es O(1) por sala.


En su turno, un rastreador mira únicamente las salas vecinas conectadas por salidas abiertas (`puerta_transitable`), descarta las de rastro vencido o inexistente, y se mueve hacia la de rastro más reciente; con rastros iguales gana la sala de menor id (2.9). Si ninguna sirve, espera. No conoce el mapa ni busca rutas. La decisión vive en un módulo aparte (`comportamiento_enemigo.py`) que solo decide: ejecutar la acción y reprogramar el turno lo hace el motor.


**Frecuencia medida** (mismo conteo que en 4.1, con un script que no forma parte de `--bench`). Por cada acción del jugador se ejecutan, en promedio, 0.8 decisiones de rastreador con 25 salas, 9.4 con 100 y 28.2 con 225 (de 18.3, 71.3 y 147.3 decisiones de enemigos). Cada una examina como mucho 4 salidas.


### Alternativas consideradas


1. **Eliminar los rastros viejos activamente** (un evento de borrado por sala visitada): obliga a programar un evento por cada visita y a cancelarlo al volver a visitarla, lo que añade carga a la agenda. Se descartó porque detectar la caducidad al consultar es O(1) y no necesita eventos.
2. **Guardar el recorrido del jugador como lista y recorrerla**: la decisión costaría lo que mida el recorrido. Se descartó porque 4.7 lo prohíbe expresamente.
3. **Buscar la ruta hasta el jugador** (como una búsqueda en el mapa): descartada por 2.9, que dice que el rastreador no conoce el mapa completo ni busca rutas.
4. **Referencias directas a las salas vecinas** (en vez de localizar cada vecina con `mapa.obtener`): quitaría el factor logarítmico, pero toca el mapa, el guardado y el retroceso. Se descartó con la medición de Evidencia, porque no es el cuello de botella.


### Decisión
La caducidad del rastro se detecta al consultarlo (`rastro_es_fresco`: antigüedad menor que 400 unidades), sin eventos de borrado ni recorridos. Cada sala guarda solo `rastro_ultima_visita`, que se refresca en cada acción del jugador. El rastreador examina como mucho 4 salidas abiertas, descarta los rastros vencidos y se mueve a la vecina con el rastro más reciente (en un empate, la de menor id de sala); si ninguna sirve, espera. La decisión vive en `comportamiento_enemigo.py`; el motor ejecuta la acción y reprograma el turno.


### Análisis de complejidad


Una decisión del rastreador examina como mucho 4 salidas, así que su costo no depende de la longitud del recorrido del jugador ni de la cantidad de salas visitadas. Con varios rastreadores, el trabajo por ciclo crece linealmente con los enemigos que realmente actúan (cada uno hace una decisión de a lo sumo 4 vecinos). Cada vecino se localiza en el mapa con búsqueda binaria, es decir O(log n) con n salas.


### Evidencia empírica


Se midió la decisión de un rastreador completa (vecinos, puertas, rastro y elección) con el mapa real, un enemigo en el centro de una cripta cuadrada con los rastros de sus vecinas frescos, mediana de 7 series de 20 000 decisiones (Linux, Python 3.12, con un script propio que no forma parte de `--bench`): 4.6 µs con 100 salas, 10.7 µs con 1600 y 11.6 µs con 6400. Con 64 veces más salas el costo se multiplica por 2.5, que es el factor logarítmico de la búsqueda binaria. La alternativa de referencias directas, simulada sin la consulta de puertas (por eso es una cota inferior), costó entre 0.41 y 0.49 µs y no creció con las salas.


Con un perfilador sobre una partida de 225 salas y 140 enemigos activos, la búsqueda binaria en el mapa ocupó cerca del 8 % del tiempo total. El resto está repartido entre el registro de cambios reversibles, la agenda y el montículo, así que quitar ese factor no cambiaría de forma apreciable el cumplimiento de 5.2.


### Límites conocidos


Un comportamiento de enemigo desconocido se trata como guardián (espera), para que un valor nuevo del API no detenga la partida. El errante consume el generador aleatorio solo cuando tiene al menos una salida abierta, y una sola vez, para que el replay sea idéntico.


La decisión del rastreador cuesta O(salidas · log n), no O(salidas) como pide el enunciado en sentido estricto: con 64 veces más salas cuesta 2.5 veces más. Se aceptó por la medición anterior; si una cripta de revisión tuviera un orden de magnitud más salas, la mejora sería guardar referencias a las salas vecinas, a costa de mantenerlas en el guardado y el retroceso.


## 4.8 Bitácora en pantalla


### Problema


La interfaz muestra solo los últimos 20 mensajes del juego. El consumo de memoria de esa bitácora debe ser constante durante toda la partida, y agregar un mensaje no puede implicar desplazar físicamente los 19 anteriores.


**Frecuencia medida**. Se agregan, en promedio, 11.6 mensajes por acción del jugador con 25 salas, 27.9 con 100 y 40.0 con 225, casi todos ataques de enemigos. Es decir, con muchos enemigos activos la bitácora recibe decenas de mensajes por acción, y solo se muestran los últimos 20.


### Alternativas consideradas


1. **Lista que crece** y mostrar los últimos 20 con un recorte: la memoria crece con la partida. Se descartó por el requisito de memoria constante; con 300 000 mensajes retuvo unos 2.5 MB.
2. **Lista de tamaño fijo que borra el primero al pasar de 20** (`del lista[0]`): memoria constante, pero cada mensaje desplaza físicamente los demás, que es lo que 4.8 prohíbe. Se descartó por el requisito, aunque con solo 20 elementos el desplazamiento es barato (ver Evidencia).
3. **Cola circular de capacidad fija** (elegida).


### Decisión


Una cola circular de capacidad fija (`ColaCircular`, 20 posiciones, implementación propia) con un índice al frente y otro al final. Al agregar con la cola llena se sobrescribe el mensaje más antiguo y el frente avanza una posición; no se mueve ningún otro mensaje. `BitacoraMensajes` envuelve la cola y entrega los mensajes del más antiguo al más reciente.


### Análisis de complejidad


Agregar un mensaje es O(1), sin desplazar elementos. Leer los mensajes es O(k) con k ≤ 20, y se hace una vez por pantalla. La memoria es O(20): una lista fija de 20 posiciones.


### Evidencia empírica


Medición propia (Linux, Python 3.12, mediana de 5 corridas de 300 000 mensajes): agregar a la cola circular cuesta 0.116 µs por mensaje; la lista de 20 que borra el primero, 0.046 µs; la lista que crece, 0.018 µs. La memoria pico fue de 0.8 KB con la cola circular, 0.3 KB con la lista de 20 y 2540 KB con la lista que crece. Tras 1000 y tras 100 000 mensajes la cola retiene la misma memoria (1.7 KB), que es el requisito. La cola circular no es la más rápida (con solo 20 elementos desplazar es barato), pero 0.12 µs por mensaje es despreciable frente a los 20 ms por ciclo.


### Límites conocidos


La decisión se justifica por el requisito de 4.8 más que por velocidad: con 20 mensajes, desplazar sería igual de válido en tiempo. Si el tope creciera a miles de mensajes, el desplazamiento dejaría de ser despreciable y la cola circular sería claramente mejor. Sobrescribir el más antiguo descarta mensajes sin avisar; no hay historial completo en pantalla (la bitácora de partida en disco sí lo guarda). Los mensajes no forman parte del estado reversible (ver 4.6).


## 4.9 Ordenamiento


### Problema
El juego ordena en varios lugares, y cada uno tiene tamaños y datos distintos:
- **Enemigos de una sala**, al poblarla (2.4 pide activarlos en orden de id): una vez por cada sala nueva con enemigos; casi siempre son pocos (2 o 3). El id de instancia se compara como texto (ver Límites).
- **Listas auxiliares del catálogo:** no se ordenan con estos algoritmos. Los ids pendientes de pedir viven en un `VectorOrdenado` que se mantiene ordenado al insertar (4.3), y el índice de fichas en memoria también (4.4).
- **Vistas ordenadas del inventario** (por peso, valor o nombre): cuando el jugador las pide; como mucho la capacidad del inventario.
- **Tabla de puntajes** (ranking de la cripta y tabla general): al terminar una partida o al abrir los puntajes; tantos elementos como partidas registradas.
- **Al guardar la partida**: el índice de salas del archivo binario (una entrada por sala de la cripta, cientos si la cripta es grande) y los eventos pendientes de la agenda (decenas). Estos datos suelen llegar **casi ordenados**, porque salen de estructuras que ya guardan un orden parecido.


Es decir, casi siempre se ordenan listas pequeñas o casi ordenadas, pero a veces una grande. El enunciado pide al menos dos algoritmos con características distintas, que el programa elija automáticamente cuál usar según propiedades medibles de los datos, y no usar `list.sort()` ni `sorted()`.


### Alternativas consideradas
Se implementaron seis algoritmos (`estructuras/ordenamientos.py`) y se compararon:
1. **Usar siempre mergesort.** Mergesort divide la lista en mitades, ordena cada una y las mezcla; siempre cuesta lo mismo, sin importar cómo vengan los datos. Pero con listas pequeñas o casi ordenadas pierde frente a inserción, porque copia las mitades en listas nuevas en cada paso. Con 50 elementos casi ordenados fue 9 veces más lento que inserción. Se descartó como única opción.
2. **Usar siempre inserción.** Inserción recorre la lista y mete cada elemento en su lugar entre los anteriores; si la lista ya está casi ordenada, casi no mueve nada. Pero si está muy desordenada, su costo crece con el cuadrado del tamaño: con 1000 elementos en orden inverso fue 29 veces más lenta que mergesort. Se descartó como única opción.
3. **Burbuja.** Es la más simple, pero fue más lenta que la mejor de las otras dos en todos los casos medidos (por ejemplo, con 200 elementos aleatorios 6 veces más lenta que mergesort). Se descartó, y se midió en el bench como alternativa descartada.
4. **Quicksort y heapsort** (también implementados). Quicksort, tal como está (toma el último elemento como pivote), cae en su peor caso con listas ya ordenadas, que aquí son frecuentes. Heapsort no aprovecha que los datos estén casi ordenados. Ninguno aporta algo que no cubra la combinación elegida.


### Decisión
Se combinan **inserción** y **mergesort**, y un selector (`ordenar_auto` en `estructuras/ordenamiento_selector.py`) elige uno en cada llamada midiendo dos propiedades de la lista:
- **n**, el tamaño;
- **el desorden**: la fracción de pares de elementos vecinos que están al revés. Vale 0 si la lista ya está ordenada, alrededor de 0.5 si es aleatoria y 1 si está en orden inverso. Se mide con una sola pasada por la lista.


La regla:
- Si n ≤ 32, inserción (en listas pequeñas, mergesort pierde por lo que gasta en copiar).
- Si n > 32, se calcula n × desorden, que aproxima cuántos elementos están fuera de lugar. Si es 30 o menos (casi ordenada), inserción; si es más, mergesort.


Todos los usos del juego pasan por `ordenar_auto`. Mergesort es **estable**: dos elementos iguales quedan en el mismo orden en que venían. De todos modos, cada uso del juego ordena tuplas que llevan un desempate (un índice o un id único), así que el resultado no depende de eso.


El ranking de la tabla de puntajes ordena con el selector automático una tupla de cuatro valores. Las victorias van primero, de menor a mayor tiempo final. Las derrotas van después: más enemigos derrotados primero y, en un empate, más tiempo vivo primero. El orden de registro desempata y mantiene estable el resultado; como es único, la comparación nunca llega hasta el puntaje. `ranking(cripta_id, version)` incluye solo los puntajes de la cripta y la versión jugadas. `globales()` ordena con la misma regla todos los puntajes guardados, de todas las criptas y versiones, y el menú los obtiene con `ServicioPartida.puntajes_globales()`, que no necesita una partida en curso.


El selector también tiene un modo para **comparaciones costosas**, para cuando comparar dos elementos es lento (por ejemplo, si cada comparación tuviera que calcular algo). En ese caso importa cuántas comparaciones hace cada algoritmo, no el tiempo de copiar: con 8 elementos o menos usa inserción directamente, y con más elige el que, según el desorden medido, haría menos comparaciones.


### Análisis de complejidad
Letras usadas: **n** = elementos a ordenar; **I** = inversiones, es decir, cuántos pares de elementos están en el orden contrario al correcto (0 si ya está ordenada, cerca de n²/2 si está al revés).
- **Medir el desorden:** una pasada, O(n). Es lo que cuesta decidir.
- **Inserción:** O(n + I). Con una lista casi ordenada I es pequeño y el costo queda cerca de O(n); con una lista al revés llega a O(n²). No usa memoria extra.
- **Mergesort:** O(n log n) siempre, sin importar el orden de entrada; usa memoria extra del tamaño de la lista para las copias de las mitades.
- La regla busca usar inserción justo cuando I es pequeño (lista corta o casi ordenada) y mergesort cuando no.


### Evidencia empírica
- `--bench --solo ordenamiento` (Intel Core Ultra 7, 16 GB, Python 3.14.6). "Casi ordenado" significa una lista ordenada en la que se intercambiaron al azar n/50 pares de elementos (al menos uno). Tiempos en milisegundos por ordenamiento:


  | n | Datos | Inserción | Mergesort | Burbuja (descartada) | Elige el selector |
  |---|---|---|---|---|---|
  | 10 | aleatorio | 0.004 | 0.010 | 0.006 | inserción |
  | 10 | casi ordenado | 0.002 | 0.009 | 0.004 | inserción |
  | 10 | inverso | 0.004 | 0.009 | 0.007 | inserción |
  | 50 | aleatorio | 0.057 | 0.062 | 0.116 | inserción |
  | 50 | casi ordenado | 0.006 | 0.054 | 0.060 | inserción |
  | 50 | inverso | 0.092 | 0.054 | 0.130 | mergesort |
  | 200 | aleatorio | 0.849 | 0.282 | 1.758 | mergesort |
  | 200 | casi ordenado | 0.054 | 0.249 | 0.865 | inserción |
  | 200 | inverso | 1.431 | 0.249 | 1.984 | mergesort |
  | 1000 | aleatorio | 33.084 | 2.415 | — | mergesort |
  | 1000 | casi ordenado | 2.686 | 3.098 | — | mergesort |
  | 1000 | inverso | 62.604 | 2.161 | — | mergesort |


  (Con 1000 elementos el bench no incluye burbuja: con 200 ya era la más lenta en todos los casos.)
- Lectura: el selector eligió el algoritmo más rápido en 11 de los 12 casos. El tiempo del selector, que incluye medir el desorden, quedó entre 0.92 y 1.28 veces el del mejor de los dos. Con tiempos tan pequeños esa diferencia es en parte ruido de la medición, por eso hay valores por debajo de 1. El único error fue con 1000 elementos casi ordenados: eligió mergesort (3.1 ms) cuando inserción tardó 2.7 ms.
- Comparado con usar un solo algoritmo: "siempre mergesort" habría sido 9 veces más lento con 50 elementos casi ordenados (0.054 contra 0.006 ms) y 4.6 veces con 200 (0.249 contra 0.054 ms). "Siempre inserción" habría sido 14 veces más lento con 1000 aleatorios (33.1 contra 2.4 ms) y 29 veces con 1000 en orden inverso (62.6 contra 2.2 ms).
- Comparaciones costosas (se cuenta cuántas comparaciones hace cada algoritmo, no el tiempo):


  | n | Datos | Inserción | Mergesort | Elige |
  |---|---|---|---|---|
  | 50 | aleatorio | 679 | 222 | mergesort |
  | 50 | casi ordenado | 108 | 161 | inserción |
  | 200 | aleatorio | 9920 | 1267 | mergesort |
  | 200 | casi ordenado | 877 | 947 | inserción |


  En los cuatro casos eligió el que hace menos comparaciones.
- Tests (`tests/estructuras/test_ordenamientos.py`): cada algoritmo ordena bien listas vacías, de un elemento, ordenadas, inversas, con repetidos, con todos los elementos iguales y aleatorias; inserción y mergesort son estables; la medida de desorden da 0 y 1 en los extremos; el selector elige inserción con listas pequeñas o grandes casi ordenadas y mergesort con listas grandes aleatorias o inversas.
- `tests/modelo/test_puntajes.py` comprueba el orden de victorias y derrotas, el desempate por tiempo vivo, el empate total, el filtro por cripta y versión, la tabla vacía y 160 filas (más de 32, así que ahí el selector ya decide según el desorden). Dos de esos tests fallan si se rompe la regla de las derrotas.


### Límites conocidos
- **Listas pequeñas.** Lo primero que mira el selector es el tamaño: si la lista tiene 32 elementos o menos, usa inserción sin revisar nada más. El bench mide listas de 10 y de 50 elementos: con 10, inserción ganó en los tres casos; con 50, ganó inserción con datos aleatorios y casi ordenados, y mergesort con datos en orden inverso. Eso indica que el tamaño donde conviene empezar a mirar el desorden está entre 10 y 50. Como el bench no mide tamaños intermedios, no confirma que 32 sea exactamente el mejor valor.
- **Listas grandes casi ordenadas.** Si la lista tiene más de 32 elementos, el selector estima cuántos elementos están fuera de su lugar (tamaño × desorden). Si son 30 o menos, usa inserción; si son más, mergesort. Con 1000 elementos casi ordenados la estimación dio cerca de 40, así que eligió mergesort, que tardó un 15 % más que inserción (3.098 contra 2.686 ms). En listas grandes, inserción todavía conviene con algo más de 30 elementos fuera de lugar.
- **Desorden que no se ve entre vecinos.** La medida de desorden solo compara cada elemento con el siguiente. Una lista hecha de dos mitades ordenadas pero intercambiadas (por ejemplo, 51…100 seguido de 1…50) tiene un solo par de vecinos al revés: el selector la vería casi ordenada y elegiría inserción, aunque tiene muchísimas inversiones y la inserción tardaría como en su peor caso. No se comprobó si algún uso del juego produce listas así.
- El modo de comparaciones costosas está implementado y medido, pero ninguna parte del juego lo usa: en todos los usos se comparan tuplas de números o textos, que es barato.
- Mergesort usa memoria extra del tamaño de la lista. Con los tamaños del juego no importa, pero con listas muy grandes sí pesaría.
- Los puntajes globales mezclan criptas distintas, así que comparan tiempos y enemigos derrotados de criptas con distinta dificultad. Esa comparación no es justa entre criptas; solo el ranking por cripta y versión lo es.
- **Id de instancia comparado como texto.** Los enemigos de una sala se activan en orden ascendente de su id de instancia (2.4), comparado como texto. Con ids del mismo largo (`e-201`, `e-202`) coincide con el orden numérico; con `e-9` frente a `e-10` no, porque `"e-10"` queda antes que `"e-9"`. Una cripta cuyos ids tengan largo distinto activaría esos enemigos en otro orden que el numérico (siempre el mismo para la misma cripta, así que el replay no se afecta).


## 4.10 Guardado binario de la partida


### Problema
El jugador puede guardar la partida y cargarla después, y el enunciado pide que el archivo sea **binario con un formato propio**: los datos se escriben como bytes con un tamaño fijo para cada campo (por ejemplo, 4 bytes para un entero), no como texto. Además pide tres cosas concretas: poder **recuperar una sala específica sin leer el archivo completo**, **detectar un archivo de otra versión del formato** en lugar de leerlo mal, y **comparar tamaño en disco y tiempo de carga contra JSON** (texto).


Guardar y cargar ocurren pocas veces por partida (cuando el jugador lo pide), así que no compiten con el límite de 20 ms por acción. Lo que importa es que el archivo sea correcto, compacto y que se pueda leer por partes.


### Alternativas consideradas
1. **JSON** (texto con la estructura de los datos). Es fácil de leer y depurar, pero ocupa más y, para obtener una sala, hay que leer y convertir todo el archivo. Se midió contra el binario (ver Evidencia).
2. **`pickle`** (el formato de Python para guardar objetos tal cual). No es un formato propio y amarra el archivo a cómo están escritas las clases del programa: si una clase cambia, un archivo viejo puede fallar de formas difíciles de explicar. Se descartó.
3. **Binario sin índice** (todas las salas una tras otra). Es más simple, pero para encontrar una sala hay que leer todas las anteriores. Se descartó porque no cumple "recuperar una sala sin leer el archivo completo".


### Decisión
**Formato del archivo** (`infraestructura/guardado_binario.py`, escrito con el módulo `struct`, que convierte números a bytes de tamaño fijo). El archivo tiene cuatro partes, en este orden:


| Parte | Tamaño | Contenido |
|---|---|---|
| Encabezado | 24 bytes | la marca `CRPT` (para reconocer que es un archivo de Cripta), la versión del formato, la cantidad de salas y dónde empieza y cuánto mide el bloque global |
| Índice | 16 bytes por sala | para cada sala: su id, en qué byte del archivo empieza su bloque y cuánto mide; **ordenado por id de sala** (con el selector de 4.9) |
| Bloque global | variable | cripta y versiones, semilla y estado del azar, reloj, jugador e inventario, eventos pendientes de la agenda y mensajes |
| Bloques de sala | variable, uno por sala | puertas, rastro, objetos del suelo, trampas y enemigos de esa sala |


- **Recuperar una sala sin leer todo** (`cargar_sala`): como cada registro del índice mide lo mismo (16 bytes) y están ordenados por id, se hace búsqueda binaria **directamente sobre el archivo**: se salta a la posición del registro del medio, se leen sus 16 bytes, se decide si seguir a la izquierda o a la derecha, y así hasta encontrar la sala. Después se salta a su bloque y se lee solo ese. Nunca se leen las demás salas ni el índice completo.
- **Detectar otra versión:** al abrir el archivo se revisa primero el encabezado. Si no empieza con `CRPT` ("no es un archivo de Cripta") o la versión del formato no es la que el programa entiende, se lanza `CriptaFormatoIncompatibleError` sin leer nada más. También se rechaza un archivo cuyo encabezado indica más salas de las que caben en su tamaño real, o que está cortado.
- **Guardado seguro:** el archivo se arma completo en memoria y se escribe primero con otro nombre (`.tmp`), que después reemplaza al anterior. Si el programa se cierra a la mitad, el guardado anterior queda intacto. Si un valor no cabe en su campo (por ejemplo, un número demasiado grande para 4 bytes), se lanza un error antes de tocar el disco.


**Qué se guarda y cómo se carga:**


La partida viva se convierte a datos planos (`EstadoPartida`) en un módulo del modelo (`persistencia_modelo.py`), que no escribe archivos: eso lo hace `GuardadoBinario`. La agenda del reloj contiene funciones, que no se pueden escribir en disco, así que cada evento declara al programarse un descriptor (tipo, sujeto y dos números) y la agenda se guarda como esos descriptores; un evento sin descriptor produce un error en lugar de perderse en silencio. Solo se guardan como cargadas las salas a las que el jugador llegó: el contenido que solo se precargó es estado de la caché y se vuelve a pedir al cargar. No se guarda el historial de retroceso, de modo que tras cargar el pergamino no deshace acciones anteriores al guardado. Solo se puede guardar con la partida en curso y cuando al jugador le toca decidir, por lo que no hay un evento de turno del jugador pendiente.


Cargar una partida reconstruye el modelo a partir del `EstadoPartida`. Se piden de nuevo el contenido y las fichas de las salas visitadas y el estado guardado manda sobre lo recién creado: suelo, trampas, enemigos (dormidos y activos), puertas, rastro, inventario con su equipo y su cursor, y estadísticas del jugador. Las acciones de la agenda, que son funciones, se recrean a partir de su descriptor con la misma pareja (tiempo, secuencia) con que se guardaron, y el estado del generador aleatorio se repone para que la partida continúe con la misma secuencia de azar. La carga se hace sin registrar inversas, de modo que no hay nada que el pergamino pueda deshacer de ella. Si el id o la versión de la cripta no coinciden con los guardados, se informa la incompatibilidad en lugar de cargar. Un enemigo activo que llegó caminando a una sala que el jugador nunca visitó se guarda con esa sala, porque es estado del juego y no de la caché.


Guardar y cargar pasan por el servicio de partida. Cargar valida primero el archivo, la versión de la cripta y la del catálogo con que se guardó, y solo entonces reemplaza la partida en curso, así un fallo de validación no destruye la partida actual. Las salas visitadas se piden de nuevo a la precarga (del disco si la caché ya las tiene) y después se pisan con el estado guardado. Las salas que solo se precargaron no se guardan como cargadas, porque son estado de la caché.


El archivo binario no contiene JSON: encabezado, índice, bloque global y bloques de sala se escriben campo por campo con `struct`. La función `guardar_json` del mismo módulo existe solo para la comparación de tamaño y tiempos de la Evidencia.


### Análisis de complejidad
Letras usadas: **S** = salas guardadas en el archivo; **B** = tamaño total del archivo en bytes.
- **Guardar:** O(B) para escribir todo, más ordenar el índice de S registros con el selector de 4.9 (suele llegar casi ordenado, así que normalmente es inserción, cerca de O(S)).
- **Cargar todo:** O(B): se lee y se convierte cada campo una vez.
- **Cargar una sala:** O(log S) lecturas de 16 bytes para la búsqueda binaria en el índice, más la lectura de ese único bloque. No depende del tamaño total del archivo.
- **Detectar otra versión:** leer los 24 bytes del encabezado, O(1), antes de cualquier otra cosa.


### Evidencia empírica
- `--bench --solo guardado` (Intel Core Ultra 7, 16 GB, Python 3.14.6). El estado de prueba lo genera el bench: n salas con objetos, enemigos y algunas trampas, un jugador con 8 objetos y hasta 300 eventos pendientes. Tiempos en milisegundos:


  | Salas | Tamaño binario | Tamaño JSON | Guardar binario | Guardar JSON | Cargar todo binario | Cargar todo JSON | Cargar UNA sala (binario) |
  |---|---|---|---|---|---|---|---|
  | 50 | 14 066 B | 34 902 B (2.5×) | 0.884 | 0.909 | 0.637 | 0.418 | 0.048 |
  | 500 | 86 510 B | 231 764 B (2.7×) | 3.812 | 4.892 | 3.380 | 3.178 | 0.049 |
  | 5000 | 738 814 B | 2 084 958 B (2.8×) | 31.604 | 46.032 | 33.340 | 34.816 | 0.049 |


- Lectura:
  - **Tamaño:** el binario ocupa entre 2.5 y 2.8 veces menos que el JSON.
  - **Cargar una sala:** tarda lo mismo con 50 que con 5000 salas (unos 0.05 ms), porque solo lee el encabezado, unos pocos registros del índice y el bloque de esa sala. Es 13 veces más rápido que cargar todo con 50 salas, 69 veces con 500 y 676 veces con 5000.
  - **Guardar:** el binario es más rápido, sobre todo con muchas salas (31.6 contra 46.0 ms con 5000).
  - **Cargar todo:** el JSON es igual o un poco más rápido (1.5 veces con 50 salas, 1.1 veces con 500 y prácticamente igual con 5000). El módulo `json` de Python está escrito en C, mientras que el lector binario convierte cada campo con una llamada desde Python. El binario no gana aquí, y no hace falta que gane: lo que pide el enunciado que JSON no puede dar es recuperar una sala sin leer todo y detectar la versión del formato.
- La prueba de ida y vuelta (`tests/modelo/test_guardado_vuelta.py`) compara una partida que se guardó y se cargó contra otra que nunca se guardó: tras las mismas acciones tienen el mismo estado completo, la misma vista y los mismos mensajes. Cubre trampas, antorcha, puerta con cierre automático, veneno, cambio de velocidad, un enemigo en una sala sin visitar y el paso por el archivo binario.
- Cargar un guardado sin nada en la caché de disco, con 3 salas visitadas en la cripta de pruebas (presupuesto 9), costó 6 solicitudes (datos generales, versión del catálogo, esqueleto, un lote de contenido y dos de catálogo), igual que iniciar una partida nueva. La partida cargada y la que nunca se guardó dan el mismo estado antes y después de seguir jugando (`tests/servicios/test_servicio_partida_guardado.py`).
- Tests del formato (`tests/infraestructura/test_guardado_binario.py`): el índice queda ordenado aunque las salas se guarden desordenadas; se recupera bien la primera, una del medio y la última sala del índice, y una que no existe da `None`; un valor que no cabe da error sin tocar el guardado anterior; un archivo con otra marca, otra versión, una cantidad de salas imposible o cortado a la mitad se rechaza.
- Guardar el mismo estado en JSON y cargarlo reconstruye exactamente el mismo estado que el binario, así que la comparación de tamaño y de tiempos de la tabla anterior es justa.


### Límites conocidos
- **El juego no usa todavía la carga de una sola sala.** `cargar_sala` cumple el requisito, está medida y probada, pero al cargar una partida el juego lee el archivo completo, porque necesita todo el estado para continuar. Sería útil si en el futuro se cargaran las salas a medida que el jugador las visita.
- **Cargar todo no es más rápido que JSON**, y con archivos pequeños es más lento (1.5 veces con 50 salas). Si solo importara la carga completa, JSON bastaría.
- El pergamino de retroceso no puede deshacer acciones anteriores a una partida cargada, porque el historial (solo inversas, nunca copias del estado) no se guarda. Guardar solo es posible con la partida en curso.
- Cargar vuelve a pedir el contenido de las salas visitadas: si no están en la caché de disco, cuesta hasta un lote por cada diez salas visitadas, más los lotes de fichas. No se midió en una cripta grande.
- El contador de ids de los objetos recogidos no forma parte del archivo: al cargar se retoma después del mayor id que queda en el inventario, de modo que nunca se repite un id existente, pero puede diferir del que habría tenido una partida que nunca se guardó. Esos ids no se muestran ni intervienen en ninguna acción.
- Los efectos del veneno y del cambio de velocidad se probaron con efectos creados a mano, porque la cripta publicada no trae nada que los origine.
- Cada campo tiene un tamaño fijo (por ejemplo, las cantidades de objetos o mensajes caben en 2 bytes, hasta 65 535). Un valor más grande no se puede guardar: da error en lugar de corromper el archivo.


## 4.11 Bitácora de partida y reproducción
### Problema
Cada acción del jugador debe quedar registrada en un archivo de texto al que solo se le agregan líneas al final, nunca se reescribe. El archivo empieza con un encabezado con, como mínimo, el id y la versión de la cripta, la versión del catálogo y la semilla del azar. Con `--replay partida.log` el programa debe repetir la partida completa sin que nadie la juegue. Si la versión que dice el log ya no está disponible, debe decir que no puede garantizar una reproducción fiel, en lugar de reproducir en silencio contra datos distintos. El profesor usará esta función para reportar y repetir errores durante la evaluación.


Escribir en el log pasa en **cada acción aceptada**, así que tiene que ser barato. Leerlo pasa solo al reproducir.


### Alternativas consideradas
1. **Guardar el estado completo después de cada acción** en lugar de la acción. No hace falta: el juego es determinista (la misma semilla y las mismas acciones dan la misma partida, ver 4.2 y 4.6), así que basta con las acciones, que ocupan muchísimo menos. Se descartó.
2. **Un solo documento JSON con la lista de todas las acciones.** Para agregar una acción habría que reescribir el archivo completo, y si el programa se cierra a la mitad el archivo queda inválido entero. Se descartó.
3. **Un archivo binario.** Ocuparía algo menos, pero no se podría leer ni revisar a mano, y para reportar un error es útil poder abrir el log y ver qué hizo el jugador. Se descartó.
4. **Lo elegido: una línea JSON por registro** (el formato llamado "JSON Lines"). Cada línea es un objeto JSON completo e independiente; agregar una acción es escribir una línea más al final, y si el programa se cierra a la mitad, como mucho se pierde la última línea.


### Decisión
**Formato del archivo** (`infraestructura/partida_log.py`):
- **Línea 1, el encabezado:** `{"tipo": "encabezado", "id_cripta": ..., "version_cripta": ..., "version_catalogo": ..., "semilla": ...}`. Puede llevar además `"parcial": true` (ver más abajo).
- **Una línea por acción aceptada**, tal como la da `Accion.a_dict()`. Por ejemplo `{"tipo": "mover", "direccion": "N"}` o `{"tipo": "atacar", "instancia": "e-201"}`.
- **Escribir:** cada acción abre el archivo en modo "agregar al final", escribe la línea completa y lo cierra. Lo ya escrito nunca se toca. Una partida nueva en la misma ruta empieza un archivo nuevo en lugar de mezclarse con la anterior. Un encabezado sin alguno de los cuatro campos obligatorios es un error de programación y se rechaza al crear el escritor.
- **Leer:** se revisa que la primera línea sea un encabezado con los cuatro campos y que cada acción tenga su `tipo`. Solo la **última** línea puede venir cortada (el programa se cerró mientras la escribía): se ignora y se avisa. Una línea inválida en medio del archivo es un error (`CriptaBitacoraError`), porque significa que el archivo se dañó.


**Quién escribe y qué pasa al guardar:**


`ServicioPartida` escribe la bitácora: tras ejecutar una acción, si el modelo la acepta, la anota (incluido el pergamino, que cambia el estado y debe repetirse en el replay); las rechazadas no cambian el estado y no se anotan. El encabezado se escribe cuando la partida ya inició sin errores, con el id y la versión de la cripta, la versión del catálogo y la semilla; si no se da semilla se genera con un generador del sistema y queda en el encabezado. Sin ruta de bitácora (replay y bench) no se escribe nada.


El guardado lleva consigo una copia de la bitácora hasta el instante de guardar (archivo del guardado más `.log`). Cargar la restaura como bitácora activa y la partida sigue anexando en ella. Se descartó recortar la bitácora original por el número de acciones del jugador, porque el log también anota el pergamino y las acciones que luego se deshicieron, así que no coincide con ese contador; guardar el número de líneas habría exigido cambiar el formato del guardado, y poner marcas dentro del log habría obligado al lector a distinguirlas de las acciones. Con la copia, la bitácora de una partida cargada es exactamente la historia que llevó a ese estado y se puede reproducir desde cero. Si la copia no existe, la bitácora nueva lleva `"parcial": true` en el encabezado y no es reproducible.


**Reproducción** (`servicios/servicio_replay.py`, con `--replay`, sin crear la vista):
1. Lee el log. Si es parcial, informa que no se puede garantizar una reproducción fiel y no reproduce.
2. Inicia la partida con la cripta y la **semilla del encabezado**, sin escribir una bitácora nueva ni registrar puntaje.
3. Compara la versión de la cripta y la del catálogo del log con las disponibles (`diferencias_de_version`). Si alguna no coincide, dice cuál y **no reproduce**.
4. Repite cada acción por el mismo camino que usa el juego (`ServicioPartida.ejecutar`) y muestra cada paso: la acción, la sala, la vida, el tiempo y los mensajes.
5. Si una acción no se acepta o no es válida, se detiene e informa **la línea del log y el motivo** (una divergencia: la partida reproducida se separó de la original).
6. Al final muestra el desenlace, el puntaje y el reporte de solicitudes y caché. Termina con código 0 si la reproducción fue fiel, 1 si no lo fue y 2 si no se pudo leer el log o falló la red.


### Análisis de complejidad
Letra usada: **A** = acciones anotadas en el log.
- **Anotar una acción:** O(1). Se agrega una línea corta al final (unos 35 bytes para un movimiento) sin leer ni reescribir lo anterior. Abrir y cerrar el archivo en cada acción cuesta un poco más que dejarlo abierto, pero garantiza que cada línea quede completa en disco.
- **Leer el log:** O(A), una pasada.
- **Reproducir:** A acciones, cada una con el mismo costo que tuvo en el juego (5.2), más mostrar cada paso.
- **Comparar versiones:** O(1), dos comparaciones de texto.


### Evidencia empírica
- Reproducción real (`py -m cripta --offline --replay datos/partida.log`, sobre una partida jugada en la consola con `cripta-01`, semilla 2734113286): el log tenía 5 acciones (recoger la antorcha, esperar, encenderla, entrar a la sala de las ratas y atacar) y el replay reprodujo las 5 sin divergencias, sin abrir la vista y sin intervención. Mostró cada paso con sus mensajes, incluidos el daño de la trampa y los ataques de las ratas, que dependen del azar, y terminó igual que la partida jugada: derrota en el tiempo 373, con 5 acciones del jugador. Un comando escrito después de morir no quedó en el log, porque solo se anotan las acciones aceptadas.
- Formato del log (`tests/infraestructura/test_partida_log.py`): lo escrito se lee igual; una partida nueva en la misma ruta reemplaza la anterior; la última línea cortada se ignora y se avisa, y un archivo sano no avisa nada; una línea rota en medio, un archivo vacío o uno sin encabezado son errores; un encabezado incompleto se rechaza al escribir; `diferencias_de_version` informa cada versión distinta.
- Reproducción (`tests/servicios/test_servicio_replay.py`): reproducir da la misma partida; se muestra un paso por acción con sus mensajes; reproducir no modifica el log; con otra versión o con un log parcial no se reproduce; una acción que no se acepta o que no es válida informa su línea; la última línea cortada se avisa y lo demás se reproduce; un log que no existe es un error.
- `tests/servicios/test_servicio_partida.py` reproduce la bitácora de una partida en una partida nueva con la semilla del encabezado y compara el estado guardado, la vista y el puntaje: son iguales.
- `tests/servicios/test_servicio_partida_guardado.py` guarda una partida, sigue jugando, carga el guardado y comprueba que la bitácora restaurada contiene solo las acciones hasta el guardado; después reproduce esa bitácora desde cero y obtiene el mismo estado que la partida cargada.


### Límites conocidos
- Los mensajes de una acción rechazada quedan en la bitácora en pantalla pero no en el log, por lo que una partida reproducida puede diferir de la original solo en esos mensajes; el estado, la vista y el puntaje coinciden.
- Solo se comprueba que el encabezado de la copia coincida con el del guardado; no se puede verificar que la copia tenga exactamente las acciones que llevaron a ese estado. Una bitácora parcial no se puede reproducir.
- Si la versión del log ya no es la que entrega el servidor, el replay no reproduce, aunque el contenido de esa versión vieja siga en la caché de disco. Es la opción más segura, pero también la más estricta: el enunciado permitiría usar una copia local compatible. Para reproducir sin red, el log tiene que ser de la misma versión que los datos de `--offline`.
- Para comparar las versiones, primero hay que iniciar la partida, lo que gasta las solicitudes del arranque aunque al final no se reproduzca.
- El costo de escribir el log en cada acción no está separado en el bench: la medición de la partida real (5.2) se hace sin bitácora.


## 5.1 La ruta más barata del cazador


Especificación: [spec.md](specs/001-terreno-cazador/spec.md). Plan: [plan.md](specs/001-terreno-cazador/plan.md). Investigación: [research.md](specs/001-terreno-cazador/research.md).


**Coincidencia con el plan original.** La decisión coincide con la del plan en lo esencial: Dijkstra con `HeapMinimo`, tabla plana por id, una sola búsqueda desde la sala del jugador y poda por rango. La medición no obligó a cambiar nada. Hay una diferencia de implementación que no motivó una medición y se explica en Límites conocidos: el plan calcula la tabla con el rango máximo de todos los cazadores activos y el código la calcula con el rango del cazador que consulta y la amplía si llega uno de mayor rango.


### Problema


Cada cazador activo, en su turno, debe moverse por la ruta de menor costo acumulado hacia la sala del jugador, usando solo salidas abiertas en ese instante. Los costos de las salidas no son uniformes (de 1 en adelante, 100 por defecto) y el cazador solo persigue si la distancia no supera su rango (600 y 2400 en los valores publicados por el servidor). El costo de la búsqueda debe depender de la región que cae dentro del rango y no del tamaño de la cripta. Puede haber decenas de cazadores persiguiendo al mismo jugador a la vez, así que importa cuántas búsquedas hacen falta. Ante rutas de igual costo gana siempre la vecina de menor id.


**Frecuencia.** La operación repetida es decidir el paso de un cazador, una vez por cada turno de cada cazador activo. La búsqueda completa solo hace falta cuando cambia el objetivo o el grafo (5.2).


### Alternativas consideradas


Las razones de descarte vienen de [research.md](specs/001-terreno-cazador/research.md), secciones 1 a 3.


1. **Búsqueda lineal del mínimo sobre una lista contigua.** Extraer el mínimo cuesta O(V), con lo que la búsqueda completa llega a O(V² + E). Se descartó por el plan y por research.md como hipótesis de que con cientos de salas y varios cazadores pondría en riesgo el límite de 20 ms. No se midió por separado, así que esa razón sigue siendo una hipótesis.
2. **A\* con heurística.** La cripta es un grafo de salas conectadas por N, S, E y O sin coordenadas garantizadas, así que no hay una heurística admisible conocida. Una heurística no admisible rompería la optimalidad y la equivalencia observable de FR-TER-015. Además, un A\* por cazador impide compartir la búsqueda. No se midió.
3. **Todas las parejas (Floyd-Warshall).** Memoria O(V²) y tiempo O(V³), y cualquier cambio de puerta obliga a recalcular todo. No se midió.
4. **Cálculo individual por cazador** (Dijkstra desde cada cazador hacia el jugador). Es la única alternativa que sí se midió contra lo elegido, con la carga `ruta_cazador` (ver Evidencia).


También se descartó, para la tabla de distancias, un `VectorOrdenado` por id (insertar cuesta O(V), O(V²) para construir la tabla) y una tabla hash propia (complejidad innecesaria con ids enteros densos).


### Decisión


Se calcula **una sola vez** un Dijkstra desde la sala del jugador sobre las salidas abiertas, con `HeapMinimo` como cola de prioridad de pares `(distancia, sala)`. Las distancias y los nodos cerrados viven en dos listas planas indexadas por id de sala, sin `dict` ni `set`. La búsqueda se detiene al extraer un nodo con distancia mayor que el rango pedido. Como todos los costos son enteros de 1 en adelante, ninguna sala posterior puede quedar dentro del rango.


La tabla la comparten todos los cazadores. Cada uno, en su sala `u`, mira sus salidas abiertas, calcula `costo(u, v) + dist(v)` para cada vecina `v` y elige entre las que alcanzan el mínimo la de menor id. Si su sala no fue alcanzada o la distancia supera su rango, espera.


**El desempate por menor id es exacto** porque la tabla se calcula desde la sala del jugador. Por la simetría de costos y puertas (FR-TER-002), `dist(u, jugador)` es igual a `dist(jugador, u)`, así que la distancia de cada vecina al jugador es única y el conjunto de vecinas óptimas es el mismo que daría un cálculo desde cada cazador. El desempate no depende del orden de extracción del montículo.


### Análisis de complejidad


Letras usadas: **V_R** y **E_R** = salas y salidas dentro del rango, **H** = cazadores que deciden en el ciclo, **n** = salas del mapa.
- **Búsqueda compartida:** O((V_R + E_R) log V_R) con el montículo, más una consulta de costo por salida relajada. No depende del tamaño de la cripta sino de la región dentro del rango.
- **Decisión de un cazador:** examina como mucho 4 salidas. El plan la anota como O(1), pero cada salida consulta `costo_de_conexion`, que cuesta O(log n), así que en rigor es O(log n).
- **Ciclo con H cazadores:** una búsqueda más H decisiones, en lugar de H búsquedas con el cálculo individual.
- **Memoria:** O(V) por las dos listas planas.


### Evidencia empírica


Medido con `py -m cripta --bench --solo ruta_cazador` en el Equipo B (Intel Core Ultra 7, Python 3.14.6). Se reporta la **mediana de tres corridas** (resultados en `docs/bench/resultados_001_a.md`, `_b.md` y `_c.md`). Cripta sintética de 400 salas con costos entre 20 y 490 y semilla fija, 60 ciclos por escenario. Cada ciclo es un ciclo completo de `Partida` entre dos decisiones del jugador, sin red ni vista. El jugador se mueve en casi todos los ciclos.


| Escenario | Ciclo compartido (ms) | Ciclo individual (ms) | Razón de tiempo | Búsquedas compartido | Búsquedas individual | Razón de búsquedas |
|---|---|---|---|---|---|---|
| R=600, H=1 | 0.357 | 0.357 | 1.00 | 58 | 60 | 1.03 |
| R=600, H=10 | 0.551 | 2.524 | 4.58 | 58 | 600 | 10.34 |
| R=600, H=30 | 0.950 | 7.619 | 7.91 | 58 | 1800 | 31.03 |
| R=2400, H=1 | 2.384 | 2.424 | 1.02 | 58 | 60 | 1.03 |
| R=2400, H=10 | 2.594 | 23.481 | 9.05 | 58 | 600 | 10.34 |
| R=2400, H=30 | 2.972 | 70.175 | 23.23 | 58 | 1800 | 31.03 |
| Mixto 25:11, H=10 | 2.954 | 8.811 | 2.95 | 116 | 600 | 5.17 |
| Mixto 25:11, H=30 | 3.354 | 27.194 | 8.11 | 116 | 1800 | 15.52 |


Los conteos de búsquedas son idénticos en las tres corridas, porque no dependen del equipo. El escenario mixto usa la proporción de cripta-06 (25 cazadores de rango 600 por cada 11 de rango 2400).


- **Cuántas búsquedas hacen falta.** Con H=30 hay 1800 decisiones en los 60 ciclos y el cálculo compartido hizo 58 búsquedas. Esto es consistente con una búsqueda por cada ciclo en que el jugador cambió de sala y ninguna en los otros dos, aunque no se contó por separado cuántos ciclos tuvieron cambio de sala. El cálculo individual hizo 1800, una por decisión. El compartido hace 31.03 veces menos búsquedas.
- **Con H=1 da casi igual.** La razón de tiempo es 1.00 con R=600 y 1.02 con R=2400, dentro del ruido entre corridas (en las seis razones sueltas de H=1 va de 0.98 a 1.03). El jugador se mueve en casi cada ciclo, así que casi cada decisión necesita una búsqueda nueva con cualquiera de los dos métodos (58 contra 60).
- **La ventaja crece con H.** Con R=2400 el ciclo compartido pasa de 2.384 a 2.972 ms al subir H de 1 a 30, mientras que el individual pasa de 2.424 a 70.175 ms. Con rango corto (R=600) la ventaja es menor pero igual crece (1.00, 4.58 y 7.91). No se encontró ninguna condición en que el cálculo individual ganara de forma clara. El plan sospechaba que podría convenir con pocos cazadores o con rangos muy dispares y no se observó: con H=1 empatan y en el mixto con H=10 el compartido sigue siendo 2.95 veces más rápido.
- **Límite de 20 ms.** Con cálculo compartido ningún ciclo superó 6.967 ms en ninguno de los escenarios de las tres corridas (es el peor de los 120 ciclos del escenario mixto con H=30, corrida b). Con el individual, R=2400 y H=30, la mediana del ciclo es 70.175 ms y el peor ciclo llegó a 207.195 ms. Esta carga no verifica FR-TER-020, eso lo hace `ciclo_referencia` (ver 5.6).
- **Costo de consultar `costo_de_conexion`.** Con R=2400 y H=1, la búsqueda sola tardó una mediana de 2423.53 µs y las consultas de costo dentro de ella 1116.72 µs (39 721 consultas de unos 1.69 µs), es decir cerca de 46 % del tiempo de una búsqueda, casi la mitad. La medición usa una envoltura que suma su propio costo, así que la fracción puede estar algo sobrestimada.


**Alternativa no implementada.** La consulta cuesta O(log n) porque `CriptaMapa` localiza cada conexión con búsqueda binaria. Se mantuvo así porque el ciclo ya cumple el límite con holgura (5.6). Si hiciera falta recortar tiempo, se podrían precalcular los costos en una tabla plana al construir el mapa, con O(1) por consulta. No se implementó ni se midió. La consulta de salas por id, en cambio, ya es O(1) desde la 004 (ver 5.5).


### Límites conocidos


- **El rango de la tabla no es el máximo de los cazadores activos.** El plan dice que la búsqueda se acota con el rango máximo de todos los cazadores activos. El código calcula la tabla con el rango del primer cazador que consulta y la recalcula si luego consulta uno de mayor rango (`calcular_o_reutilizar` en `buscador_rutas.py`). Las decisiones no cambian, porque los cazadores de mayor rango siempre disparan el recálculo y la equivalencia con el cálculo desde cero está probada. El costo se ve en el escenario mixto: 116 búsquedas en 60 ciclos, el doble que las 58 de los escenarios con un solo rango. Esa cifra es consistente con dos búsquedas por ciclo, pero no se aisló la causa con un conteo aparte. El compartido sigue siendo mucho mejor que el individual (15.52 veces menos búsquedas con H=30).
- Un cazador con un rango mucho mayor que los demás obliga a expandir la búsqueda hasta ese rango. El plan lo anotaba como límite y la medición mixta no muestra que el individual compense.
- La tabla plana asume ids de sala densos. Con ids muy grandes y dispersos desperdiciaría memoria y habría que indexar por posición.
- El diseño supone un único objetivo común (el jugador).
- El tiempo de las cargas depende del equipo. Las razones y los conteos de búsquedas son más estables que los milisegundos.


## 5.2 Rutas que dejan de ser válidas


Especificación: [spec.md](specs/001-terreno-cazador/spec.md). Plan: [plan.md](specs/001-terreno-cazador/plan.md). Investigación: [research.md](specs/001-terreno-cazador/research.md), sección 4.


**Coincidencia con el plan original.** La decisión coincide con la del plan en el mecanismo (invalidación selectiva por eventos), con una diferencia en el sexto evento: el plan invalidaba al activar un cazador cuyo rango superara el rango calculado y el código invalida al activar cualquier cazador. La diferencia no la motivó una medición y se justifica abajo.


### Problema


La tabla de 5.1 vale mientras no cambie el objetivo (la sala del jugador) ni el grafo (qué salidas están abiertas). La decisión de cada cazador debe ser idéntica a la que daría un cálculo desde cero en ese instante (FR-TER-015). Hay que saber qué eventos invalidan la tabla, cuándo es válido reutilizarla y cuánto se gana frente a recalcular siempre. Se evalúa la validez en cada turno de cada cazador, mientras que los eventos que invalidan son mucho menos frecuentes.


### Alternativas consideradas


1. **Recalcular siempre**, una búsqueda por cada turno de cada cazador. Es la más simple y siempre correcta, pero repite el mismo cálculo aunque nada haya cambiado. Se midió contra lo elegido (ver Evidencia).
2. **Actualización incremental de caminos más cortos (por ejemplo D\* Lite).** Se descartó por la complejidad de implementarla a mano frente a un Dijkstra estático en grafos de este tamaño. No se midió.


### Decisión


La tabla se invalida con estos eventos:
1. el jugador se mueve (cambia el origen de la búsqueda)
2. se abre una puerta (aparece una salida transitable)
3. se cierra una puerta por cierre automático (desaparece una salida)
4. se usa un pergamino de retroceso (se restaura un estado anterior)
5. se carga una partida guardada
6. se activa un cazador


Se conserva ante los turnos y movimientos de los cazadores, la muerte de enemigos y los cambios de velocidad, porque ninguno cambia la sala del jugador ni qué salidas están abiertas, y el costo de una ruta es una suma de costos de salida que no depende de la velocidad.


**Cuándo se reutiliza.** Solo si la tabla es válida, es de la misma sala del jugador y el rango pedido no supera el rango con que se calculó. Si falta cualquiera de las tres condiciones, se recalcula.


**La invalidación al activar un cazador es conservadora.** Un cazador se activa cuando el jugador entra a su sala, y entrar a una sala ya invalida la tabla por el movimiento (evento 1), así que la invalidación del evento 6 casi nunca hace trabajo que no se hiciera ya. El caso que el plan quería cubrir con ese evento, un cazador de rango mayor que el calculado, lo resuelve por sí sola la comparación de rangos de la condición de reutilización. La invalidación puede sobrar pero no faltar, y cuesta muy poco porque solo apaga una bandera.


**Prueba de equivalencia (P2 §5.2).** Una prueba recorre secuencias deterministas por semilla de movimientos, aperturas y cierres de puertas, activaciones y muertes, y en cada turno de cada cazador compara la decisión con reutilización contra la de un buscador nuevo calculando desde cero (`tests/modelo/test_equivalencia_rutas.py`).


### Análisis de complejidad


Comprobar si la tabla sirve es O(1): una bandera y dos comparaciones. Una invalidación es O(1) (apagar la bandera) y el costo se paga en la búsqueda siguiente, que es la de 5.1. Con la invalidación selectiva el número de búsquedas depende de cuántos eventos invalidantes ocurren y no de cuántos turnos de cazador hay.


### Evidencia empírica


Medido con `py -m cripta --bench --solo invalidacion` en el Equipo B, mediana de tres corridas (`docs/bench/resultados_001_a.md`, `_b.md` y `_c.md`). Hay 20 cazadores y 100 ticks en los que el jugador espera sin cambiar de sala. En el régimen de puertas inestables se cierran 5 puertas cada 15 ticks. Una operación de la tabla es un tick.


| Régimen | Estrategia | Tiempo por tick (µs) | Búsquedas para 140 decisiones | Tiempo en búsquedas (ms) |
|---|---|---|---|---|
| Puertas estables | Invalidación selectiva (elegida) | 102.38 | 1 | 2.823 |
| Puertas estables | Recalcular siempre (descartada) | 4279.48 | 140 | 418.351 |
| 5 puertas inestables | Invalidación selectiva (elegida) | 205.52 | 4 | 11.720 |
| 5 puertas inestables | Recalcular siempre (descartada) | 4162.78 | 140 | 407.049 |


- **Puertas estables:** recalcular siempre es 42.37 veces más lento y hace 140 veces más búsquedas (140 contra 1).
- **Puertas inestables:** recalcular siempre es 20.25 veces más lento y hace 35 veces más búsquedas (140 contra 4). Con puertas que cambian, la invalidación selectiva cuesta el doble por tick que con puertas estables (205.52 contra 102.38 µs) porque invalida y recalcula más, pero sigue ganando.
- Los conteos de búsquedas son iguales en las tres corridas. La razón de tiempo con puertas inestables fue 20.25, 19.80 y 23.40 en cada corrida, y con puertas estables 42.37, 46.59 y 41.56.


### Límites conocidos


- El plan se proponía medir a partir de qué frecuencia de cambios de puertas deja de convenir reutilizar. Solo se midió un punto (5 puertas cada 15 ticks) y en él conviene con claridad. No se encontró el punto de cruce.
- La carga cierra y abre las puertas directamente sobre el mapa y apaga la bandera de la tabla a mano. No mide la ruta real de `EfectoCierrePuerta` hacia la invalidación. Esa conexión se comprueba con las pruebas de la capacidad y no con esta medición.
- La carga es sintética (400 salas, 20 cazadores de rango 2400, el jugador sin moverse). Con un jugador que se mueve en cada ciclo la tabla se invalida cada vez y la ventaja desaparece, como muestra el caso H=1 de 5.1.


## 5.3 Niebla de guerra e «ir a»


Especificación: [spec.md](specs/002-niebla-ir-a/spec.md). Plan: [plan.md](specs/002-niebla-ir-a/plan.md). Investigación: [research.md](specs/002-niebla-ir-a/research.md).


**Coincidencia con el plan original.** La decisión final coincide con la del plan: conocimiento en listas por id, revelación incremental, reversión mediante inversas puntuales, búsqueda propia con `HeapMinimo` desde el destino y costos guardados en el conocimiento. La medición confirmó la elección del heap: con las 300 salas conectadas de cripta-06, la selección lineal fue más lenta, así que la hipótesis de `research.md` de que podría ganar en mapas pequeños no se cumplió en el tamaño medido.


### Problema


Cada entrada a una sala observa sus puertas y revela las salas vecinas si la antorcha está encendida. Cada paso de «ir a» calcula un primer paso usando solo el conocimiento del jugador, pues una puerta no observada no cuenta como abierta. El pergamino revierte la entrada y también los cambios de conocimiento que produjo. La decisión debe limitar el costo de esa revelación y de cada consulta frecuente de ruta, cumplir FR-NIE-018 bajo 5 ms y mantener el mapa conocido separado del mapa real (SC-NIE-002 y SC-NIE-004).


### Alternativas consideradas


1. **Representar el conocimiento con listas contiguas por id (elegida).** Consultas directas de sala, puerta y costo. Frente a **recalcular desde el mapa real en cada consulta**, que se descarta porque el mapa real contiene datos que el jugador aún no conoce y repetiría el trabajo.
2. **Revelación incremental (elegida).** Visita las salidas de la sala de entrada y las vecinas que se revelan. Frente a una **pasada completa por el mapa** en cada entrada, que no escala con lo que cambió.
3. **Reversión con inversas puntuales por celda (elegida).** Registra solo los valores que cambian. Frente a una **copia completa del conocimiento** en cada acción, que duplica estado aunque solo cambien unas celdas.
4. **Búsqueda propia con `HeapMinimo` desde el destino (elegida).** Calcula sobre salas exploradas, puertas recordadas abiertas y costos conocidos. Frente a **selección lineal manual**, cuya complejidad es cuadrática, y a reutilizar `BuscadorRutas` de la 001, descartada porque calcula sobre el mapa real, poda por rango de cazadores y conserva una caché pensada para sus eventos.
5. **Costo de salida guardado en el conocimiento (elegido).** Frente a consultar `CriptaMapa.costo_de_conexion` durante la búsqueda, lo que consulta la representación real en cada relajación.


### Decisión


Se mantienen las decisiones del plan. Cada entrada actualiza solo las celdas afectadas y registra sus inversas. La búsqueda de producción recalcula desde el destino con heap antes de cada paso, usando los costos guardados en el conocimiento. La carga abre las 28 puertas cerradas de su instancia del mapa para probar el peor caso conectado, selecciona al azar 12 pares de salas con ruta usando semilla 20261118 y mide tres cálculos por alternativa y consulta. La cripta de referencia se selecciona por el mayor total de salas del listado, sin fijar su id en el código. Para la medición resultó ser cripta-06, de 300 salas y 760 salidas.


### Análisis de complejidad


Consultar sala, puerta y costo es O(1). Revelar R salas cuesta O(R), pues el grado está acotado por cuatro. La búsqueda con heap cuesta O((V+E) log V). La selección lineal cuesta O(V²+E). La reversión ejecuta una operación inversa por cada celda modificada.


### Evidencia empírica


Comando `py -m cripta --bench --solo niebla_rutas --escala 1`. Equipo A, Python 3.14.7. Las medianas de las tablas son medianas de tres corridas y cada máximo es el mayor de los máximos de esas corridas. Se hicieron tres cálculos por consulta de ruta y 12 consultas con ruta. La primera versión de la carga usaba pares de salas vecinas con las puertas cerradas, que separaban el mapa en regiones diminutas. Se corrigió abriendo las puertas del harness y eligiendo al azar pares que sí tuvieran ruta, para medir el peor caso conectado. Resultados completos: [corrida A](docs/bench/resultados_002_a.md), [corrida B](docs/bench/resultados_002_b.md) y [corrida C](docs/bench/resultados_002_c.md).


| Alternativa | Mediana (ms) | Máximo (ms) |
|---|---:|---:|
| Ruta de producción con costos guardados | 3.095 | 4.834 |
| Selección lineal manual | 4.799 | 7.142 |
| Heap del harness con costos guardados | 3.069 | 4.503 |
| Heap del harness consultando `CriptaMapa.costo_de_conexion` | 4.217 | 7.101 |


La producción cumplió FR-NIE-018 en las tres corridas: los máximos fueron 4.834, 3.799 y 4.599 ms. El peor máximo fue 4.834 ms, con 0.166 ms de margen al límite. La selección lineal no ganó en este mapa conectado y tuvo máximo superior a 5 ms. Consultar el mapa durante el heap también tuvo máximo superior a 5 ms.


| Revelación | Incremental mediana / máximo (ms) | Pasada ingenua mediana / máximo (ms) | Razón de medianas |
|---|---:|---:|---:|
| R=10 | 0.032 / 0.057 | 0.360 / 0.504 | 11.25x |
| R=50 | 0.028 / 0.073 | 0.362 / 0.571 | 12.93x |
| R=200 | 0.016 / 0.081 | 0.366 / 0.645 | 22.88x |


| Reversión | Mediana / máximo (ms) | Razón de medianas |
|---|---:|---:|
| Inversas puntuales, 409 operaciones | 0.800 / 1.059 | — |
| Copia completa | 1.185 / 1.270 | 1.48x más lenta |


Las equivalencias de las alternativas fueron verdaderas en las tres corridas. Los máximos que superaron 5 ms fueron la selección lineal y el heap consultando `CriptaMapa.costo_de_conexion`; la ruta de producción y las mediciones de revelación y reversión quedaron por debajo.


### Límites conocidos


- El margen de producción al límite de 5 ms es estrecho: el peor máximo observado fue 4.834 ms. La función de producción proyecta el conocimiento y reconstruye las aristas entrantes en cada llamada (`cripta/modelo/ruta_conocida.py`); que esa preparación domine el tiempo es una hipótesis que no se midió por separado.
- En la revelación, R es la cantidad de entradas aleatorias con reemplazo, no R salas nuevas. Solo se midió un tamaño de mapa, cripta-06. Se midió el cálculo del primer paso y no un viaje completo dentro de una partida real.
- El guardado binario del conocimiento dependía de la 004 (ya fusionada en main); T040 está completa y la carga desde archivo conserva el mapa explorado correctamente.
- Al entrar a una sala se observan todas sus puertas. Por eso, en la sala actual no hay puertas sin observar y `Partida.vista()` presenta cada una según su estado observado, abierta o cerrada.
- El grupo decidió considerar abierta al explorar su sala una salida que no tenga puerta cerrable. Esta decisión está pendiente de confirmación con el profesor.
- Los costos de las salidas conocidas ocupan memoria proporcional a las salidas representadas.


## 5.4 Resolubilidad


Especificación: [spec.md](specs/003-resolubilidad/spec.md). Plan: [plan.md](specs/003-resolubilidad/plan.md). Investigación: [research.md](specs/003-resolubilidad/research.md). Mediciones completas: [resultados_003.md](docs/bench/resultados_003.md).


**Coincidencia con el plan original.** La decisión final coincide con la del plan (sección 3.1): recorrido incremental único con cola propia, catálogo ordenado con búsqueda binaria manual, tablas contiguas por entero, montículo para desempatar llaves y DFS tricolor para los ciclos. La carga sintética tuvo que corregirse para que el ingenuo mostrara su costo, como se explica en la evidencia.


**Términos de esta sección.** *K* es la cantidad de llaves distintas de la cripta. *V* es la cantidad de salas. *E* es la cantidad de salidas entre salas (como mucho 4 por sala, así que E es a lo sumo 4V). *Recorrido incremental*: un único recorrido por anchura que, al conseguir una llave, sigue desde donde estaba sin volver a empezar. *Recorrido por anchura* (BFS): visitar primero las salas más cercanas y después las más lejanas, usando una cola. *Ciclo de dependencia*: un grupo de llaves donde cada una está encerrada tras una puerta que exige otra del mismo grupo, de modo que ninguna se puede conseguir. *DFS tricolor*: una búsqueda en profundidad que marca cada nodo como sin ver, en curso o terminado, y detecta un ciclo cuando llega a un nodo que está en curso.


### Problema


Antes de jugar hay que saber si la cripta se puede completar: obtener la llave de salida y llegar a la sala de salida por una puerta que la exija, suponiendo que las llaves no se consumen y que todo enemigo se puede derrotar (FR-RES-001 a FR-RES-006). Si no se puede, el reporte debe decir qué llaves no se consiguen, qué puertas forman la frontera bloqueada y qué llaves se bloquean entre sí (FR-RES-012). La verificación corre una vez por cripta (con `--verificar` o al elegir la cripta) y debe tardar menos de 200 ms en la cripta publicada más grande (SC-001). Las llaves se identifican con texto y el enunciado prohíbe usar `dict` o `set` como índice, así que cada id de llave hay que convertirlo a un entero por otro camino.


### Alternativas consideradas


1. **Recorrido incremental único (elegida).** Cuando el recorrido encuentra una puerta cerrada cuya llave aún no tiene, anota la puerta como pendiente de esa llave y sigue. Al vaciarse la cola, toma la llave disponible de menor id y libera sus puertas pendientes. Frente a **repetir el recorrido completo cada vez que se consigue una llave** (`verificar_ingenuo_reiniciado`, descartada), que repite visitas a salas ya exploradas. El plan estimó su costo en O(K · (V + E log V)).
2. **Catálogo ordenado con búsqueda binaria manual (elegida).** Los ids de llaves se ordenan con merge sort propio, se deduplican en una pasada y cada id se convierte en su posición. Frente a **búsqueda lineal sobre la lista de ids**, que costaría O(E · K) comparaciones de texto, y a **una tabla hash hecha a mano**, que agrega colisiones y redimensionamiento para un conjunto fijo y pequeño.
3. **Detección de ciclos con DFS tricolor sobre un grafo reducido (elegida).** Solo se ejecuta si la cripta no es resoluble. Agrupa las salas inalcanzables en bloques unidos por puertas abiertas y reporta un ciclo por grupo, empezando por la llave de menor id. Frente a **enumerar todos los ciclos** (Johnson o Tarjan), que puede crecer de forma exponencial y contradice FR-RES-012, y a **una búsqueda plana con un solo arreglo de visitados**, que confunde ciclos reales con ramas ya procesadas.
4. **Desempate con `HeapMinimo` (elegida).** Las llaves disponibles entran una sola vez al montículo y la de menor id sale en O(log K). Frente a **reordenar la lista de candidatas en cada ronda**, que costaría hasta O(K² log K), y a `sorted()` o `list.sort()`, prohibidos.
5. **Rutas mínimas (Dijkstra o Bellman-Ford), descartada.** La resolubilidad es una propiedad de conectividad y no de costo, así que un montículo de rutas solo agrega trabajo.


### Decisión


Se mantienen las decisiones del plan. `VerificadorResolubilidad.verificar` hace un solo recorrido por anchura sobre listas contiguas indexadas por entero (`visitada`, `llave_obtenida`, `puertas_pendientes`, `llaves_en_sala`). Cuando la cola se vacía y hay llaves candidatas, extrae la de menor id del montículo y encola las salas destino de sus puertas pendientes. La cripta es resoluble solo si se obtuvo la llave de salida y se cruzó, hacia la sala de salida, una puerta que la exige. Si no lo es, calcula la frontera bloqueada, la ubicación de cada llave no obtenida y los ciclos de dependencia. La frontera y los ciclos se ordenan con un merge sort propio sobre sus campos, sin `sorted()`. El modelo no toca red, archivos ni vista. La entrada por la llave de salida se cuenta aunque la sala de salida ya haya sido alcanzada por otra ruta.


### Análisis de complejidad


El plan da O(E log V + K log K) para el recorrido incremental, con memoria O(V + E + K). El término E log V viene de que cada salida examinada consulta `CriptaMapa.obtener`, que es una búsqueda binaria entre las V salas. El catálogo cuesta O(K log K). La detección de ciclos corre solo si la cripta no es resoluble y recorre una sola vez las salas inalcanzables, con costo O(V + E + K) más el DFS sobre el grafo reducido. La alternativa descartada tiene costo O(K · (V + E log V)) en el peor caso, porque cada reinicio repite un recorrido completo.


### Evidencia empírica


Comando `py -m cripta --bench --solo resolubilidad resolubilidad_cota`. Equipo B (Intel Core Ultra 7, Windows, Python 3.14.6), tres corridas, cada una en un proceso aparte, commit 6114646. Las cifras se midieron con el código de ese commit, que ya incluye las correcciones del verificador y la cripta sintética nueva, y el archivo docs/bench/resultados_003.md se guardó en el commit 21996d9. Las cifras son medianas de las tres corridas tomadas de [resultados_003.md](docs/bench/resultados_003.md). La razón es la mediana de las tres razones impresas por cada corrida.


La cripta sintética pone la puerta de cada segmento en la primera sala del corredor y su llave en una sala lateral al final, es decir, cada llave queda después de su puerta. Así el recorrido llega a la puerta sin tener la llave y el ingenuo necesita volver a empezar para cruzarla. La primera versión de la carga ponía la llave antes que la puerta, que es el mejor caso del ingenuo, y por eso se cambió (ver más abajo).


| Escenario | Incremental (ms) | Ingenuo reiniciado (ms) | Razón ingenuo/incremental |
|---|---:|---:|---:|
| 10 llaves, 200 salas | 0.908 | 3.347 | 3.7x |
| 20 llaves, 400 salas | 1.799 | 10.589 | 6.1x |
| 40 llaves, 800 salas | 3.298 | 44.845 | 13.6x |


| Cota | Verificación (ms) | Límite (ms) | Resultado |
|---|---:|---:|---|
| cripta-06, 300 salas | 1.389 | 200.0 | CUMPLE |


La verificación de la cripta de referencia, elegida por el mayor total de salas del listado sin fijar su id en el código, tomó 1.389 ms contra un límite de 200 ms, unas 144 veces por debajo.


Salas sacadas de la cola en una verificación (también en [resultados_003.md](docs/bench/resultados_003.md)). Se contaron con un script temporal fuera del repositorio que no se versiona, y el conteo no depende del equipo.


| Escenario | Incremental | Ingenuo, primera cripta | Ingenuo, cripta nueva | Razón nueva |
|---|---:|---:|---:|---:|
| 10 llaves, 200 salas | 200 | 400 | 1299 | 6.5x |
| 20 llaves, 400 salas | 400 | 800 | 4599 | 11.5x |
| 40 llaves, 800 salas | 800 | 2080 | 17199 | 21.5x |


**Por qué se cambió la cripta sintética.** La primera versión de la carga colgaba la sala lateral de la llave de una sala al azar del corredor y ponía la puerta al final del corredor. El recorrido por anchura visitaba la lateral antes que la puerta, así que al llegar a la puerta ya tenía la llave. Con eso el ingenuo casi no necesitaba reiniciar: sacó de la cola 400, 800 y 2080 salas, es decir 2.0, 2.0 y 2.6 veces V (algo más de 2 pasadas), y la razón de tiempos fue de 1.6 a 2.0 veces. Esas cifras se midieron con el código del commit d2b340d y están en `docs/bench/resultados_003.md` del commit b3474b0. Era el mejor caso del ingenuo y no mostraba lo que el plan quería mostrar, por eso se cambió la carga y se repitió la medición.

**Lo que el plan esperaba y lo que se midió.** El plan (sección 2, alternativa A.1) estimaba para K = 50 y V = 1000 unas 25 000 visitas redundantes y una diferencia del orden de K veces. Con la cripta nueva:

- **Medido (conteo de salas):** el incremental saca cada sala una sola vez (200, 400 y 800) y el ingenuo saca 1299, 4599 y 17199, es decir 6.5, 11.5 y 21.5 veces lo que el incremental. El trabajo del ingenuo crece con K, como decía el plan. Con K = 40 y V = 800 son unas 16 400 visitas por encima de las 800 necesarias, el mismo orden que las 25 000 estimadas para K = 50 y V = 1000.
- **Medido (tiempo):** el ingenuo es 3.7, 6.1 y 13.6 veces más lento, y la razón crece con K.
- **Medido (código y conteo):** el ingenuo repite el recorrido mientras la pasada anterior haya conseguido alguna llave nueva, así que siempre hace al menos 2 pasadas, y con la cripta nueva el conteo muestra que hace muchas más.
- **Hipótesis, no confirmada:** que el número de visitas del ingenuo sea cercano a (K + 1) / 2 veces V, porque cada reinicio vuelve a recorrer los segmentos anteriores. Es una cuenta aritmética que concuerda con el conteo (por ejemplo 800 · 41 / 2 = 16 400 contra 17 199 medidas), pero no se contó pasada por pasada.
- **Hipótesis, no confirmada:** que parte de la diferencia se diluya por trabajo fijo. Ambos métodos hacen lo mismo antes de recorrer: revisar todas las salas y salidas para juntar los ids de llaves, ordenarlos y deduplicarlos con merge sort, y armar las tablas. Ese trabajo no depende del número de pasadas y se suma a los dos tiempos. Es coherente con que la razón de tiempos (3.7, 6.1 y 13.6) sea menor que la razón de salas sacadas de la cola (6.5, 11.5 y 21.5), pero no se midió por separado cuánto pesa ese trabajo.

La decisión no cambia y la evidencia la refuerza: el incremental fue más rápido en las tres escalas y es el único cuyo costo no depende de cuántas llaves haya que conseguir en cadena.


### Límites conocidos


- Solo se midió una cripta sintética de cadena, con 20 salas por segmento y una llave por segmento, y está construida para que el ingenuo necesite reiniciar en cada segmento. Con otra forma la ventaja puede ser mucho menor, como mostró la primera versión de la carga (razón de 1.6 a 2.0). Las criptas publicadas no se midieron con el ingenuo.
- Cada cifra es la mediana de tres corridas en un solo equipo (Equipo B), y las medianas de tiempo no se comparan con las de los equipos A o C. Las razones sí son más estables, pero tampoco se midieron en otro equipo.
- La cota de 200 ms se midió solo en cripta-06 (300 salas). No se midió con una cripta más grande ni en red viva, y la medición no incluye el tiempo de leer fixtures ni de construir el mapa.
- La detección de ciclos no está medida: las criptas de `--bench` son resolubles, así que ese camino no corre en las cargas. Su costo es el del plan, sin evidencia propia. El caso del Apéndice B con la llave de salida dentro de la sala de salida (ciclo itm_llave_salida -> itm_llave_salida) sí está cubierto por pruebas en tests/modelo/test_resolubilidad.py (las de sufijo _ApendiceB).
- Riesgos del plan (sección 6). Los arreglos `visitada` y `llaves_en_sala` miden `max_sala_id + 1`, así que ids de sala muy dispersos gastarían memoria innecesaria (el API numera las salas desde 1 de forma correlativa, y el diseño asume V hasta unas 1000). Con más de 100 000 llaves distintas el ordenamiento inicial O(K log K) tendría un costo que solo `--bench` podría confirmar y que no se midió. El algoritmo reporta un solo ciclo representativo por grupo de llaves, como pide FR-RES-012, y no todos los ciclos posibles.
- Además, la búsqueda binaria de `CriptaMapa.obtener` agrega el factor log V a cada salida examinada. El plan (sección 7) mantiene `CriptaMapa` sin cambios y no se midió el efecto de reemplazarla por referencias directas.


## 5.5 La línea de tiempo


Especificación: [spec.md](specs/004-linea-de-tiempo/spec.md). Plan: [plan.md](specs/004-linea-de-tiempo/plan.md). Investigación: [research.md](specs/004-linea-de-tiempo/research.md).


**Coincidencia con el plan original.** La decisión coincide con el plan en sus cuatro elecciones de diseño: re-simular desde el punto de control más cercano, buscar con búsqueda binaria manual, recortar desde el final al usar un pergamino y restaurar el estado ya materializado sin preparar salas. Las mediciones de la carga `linea_tiempo` confirmaron las cuatro y ninguna se cambió. Hay tres diferencias respecto del plan, cada una motivada por una medición:
1. **Índice plano por id en `CriptaMapa.obtener`.** El plan no lo contemplaba. Lo motivó un perfil de la consulta, donde `obtener` era el 40 % del tiempo total (ver "Cambios motivados por mediciones").
2. **Puntos de control reducidos (T042).** El plan guardaba el estado completo en cada punto. Lo motivó la memoria de la línea base, 34494.7 KiB con K=50.
3. **K=50 como valor predeterminado (T033).** El plan no fijaba K y exigía medirlo. Lo fijaron las mediciones de la tabla de esta sección.


### Problema


La partida debe poder mostrar su estado en un instante pasado (`historia <t>`) o justo antes de una acción numerada (`historia #k`) sin alterar la partida viva (FR-LIN-005). Una consulta debe aplicar o deshacer los cambios de no más de K acciones (FR-LIN-015), tardar menos de 50 ms con 5 000 acciones (FR-LIN-018) y la memoria debe crecer con los cambios y los puntos de control y no con acciones por tamaño del estado (FR-LIN-016). El pergamino recorta la línea y las acciones revertidas dejan de existir para la consulta (FR-LIN-007). La línea debe sobrevivir al guardado y a la carga (FR-LIN-010).


**Frecuencia.** Registrar una acción ocurre en cada acción del jugador. Consultar ocurre pocas veces por partida, pero su costo es el que limita el valor de K. El recorte ocurre una vez por pergamino.


### Alternativas consideradas


Las razones de descarte vienen de [research.md](specs/004-linea-de-tiempo/research.md). Todas se midieron con `py -m cripta --bench --solo linea_tiempo --escala 1`. Las cifras de esta lista salen de `docs/bench/resultados_004_puntos_reducidos.md` y la de la restauración también de la línea base (`resultados_004_linea_base.md`).


1. **Reconstruir hacia atrás con cambios serializables** frente a **re-simular desde el punto de control** (elegida). Con puntos cada 100 acciones y 13 consultas, la reconstrucción hacia atrás tardó una mediana de 0.843 ms y un máximo de 1.173 ms. Re-simular tardó 28.929 ms y 52.927 ms. Registrar costó 14.9 µs por acción hacia atrás y 6.7 µs re-simulando. La memoria fue 9193.6 KiB y 11885.9 KiB. **Hacia atrás es mucho más rápida al consultar y se descartó igual**, por tres razones. Primero, la medición es un modelo de cota inferior que solo registra los 9 campos visibles (sala, vida, estadísticas, inventario, efectos y enemigos de la sala) y no el azar, la agenda ni el mapa conocido, así que no reconstruye el estado completo que exige FR-LIN-017. Segundo, cada mutación del motor tendría que quedar cubierta de forma explícita, y una que falte cambia en silencio lo que muestra la historia. Tercero, su costo crece con las acciones que faltan hasta el final y no con K. El modelo coincidió con la re-simulación en 13 de 13 consultas.
2. **Búsqueda lineal frente a binaria** (elegida) en dos lugares. Para pasar de un instante a una acción con 5000 elementos y 400 consultas, la binaria tardó 1.16 µs con 12.3 inspecciones en promedio y la lineal 106.13 µs con 2627.7, es decir 91.7 veces más lenta (en la línea base 76.1 veces). Para hallar el punto de control anterior con 50 elementos, la binaria tardó 0.54 µs con 5.8 inspecciones y la lineal 0.96 µs con 25.2, 1.8 veces más lenta. La comparación favorece algo a la lineal, porque la binaria cuenta la llamada al método y la lineal es un bucle directo.
3. **Recorte desde el final frente a escanear y filtrar** (elegida la primera). Con 5000 acciones y 30 repeticiones, recortar desde el final tardó 3.18 µs y procesó 2 registros. Filtrar tardó 405.12 µs y examinó 5050 registros, 127.5 veces más lento (en la línea base 1.80 µs contra 388.34 µs, 215.3 veces).
4. **Restaurar un punto con el estado ya materializado frente a preparar cada sala** (elegida la primera). Con 75 salas con contenido y 5 repeticiones, la vía materializada tardó 3.584 ms y 0.0 llamadas al cliente por consulta. Preparar las salas tardó 12.702 ms con 16.0 llamadas al cliente por consulta (75 llamadas a `preparar_sala`), 3.5 veces más lento. Cada llamada al cliente de fixtures lee un archivo, que es la E/S de la consulta. Con la red real, cada una sería además una solicitud contra el presupuesto.
5. **Frecuencia de los puntos de control (K)**: 50, 100, 500, 1000 y ninguno. Se comparan en la tabla de Evidencia empírica.


También se descartó reutilizar las inversas del historial de retroceso como registro histórico, porque son closures (no se pueden consultar ni guardar) y solo conservan cinco intervalos. Esa razón viene de research.md y no se midió.


### Decisión


La línea de tiempo (`LineaTiempo`, `cripta/modelo/linea_tiempo.py`) es un registro puro, sin red, archivos ni vista, hecho con listas contiguas. Guarda las acciones vigentes con su instante (dos listas paralelas), los puntos de control (`PuntoControl`, un número de acciones y un estado) y los ajustes de inventario del pergamino (una posición y las instancias afectadas). `Partida` (`cripta/modelo/partida.py`) la alimenta y la consulta.


- **Qué es un punto de control.** `Partida._capturar` arma con `crear_estado` un estado plano que incluye el generador aleatorio, el reloj con su agenda, el jugador, el mapa, el conocimiento del jugador y el contador de instancias. Hay una base, capturada al iniciar la partida, que conserva todas las salas. Los puntos periódicos se crean tras registrar una acción cuando el número de acciones es múltiplo de K, siempre que haya turno listo y la partida siga en curso, y omiten las salas que se pueden reconstruir desde el esqueleto (T042).
- **Consulta por acción** (`consultar_accion(k)`). Busca con búsqueda binaria el último punto con número de acciones menor o igual que k menos 1, o parte de la base si no hay ninguno, y re-simula las acciones que faltan hasta justo antes de la acción k.
- **Consulta por instante** (`consultar_instante(t)`). Valida que t sea entero, no negativo, no posterior al reloj y no anterior al inicio de la línea. Con dos búsquedas binarias cuenta las acciones con instante menor que t y las de instante menor o igual que t. Si hay una decisión en t, o t es el reloj actual, reconstruye el estado tras las acciones anteriores a t, que es el estado justo antes de esa decisión (FR-LIN-002). Si no hay decisión en t, reconstruye hasta la acción previa y ejecuta además los eventos de la acción siguiente con tiempo menor o igual que t (FR-LIN-001).
- **Reconstrucción aislada.** `_crear_aislada` copia el mapa estático (`copiar_mapa_estatico`) y arma una `Partida` nueva marcada como aislada y silenciosa, con una `PrecargaMaterializada` que sirve el contenido inicial de las salas y las fichas del catálogo. Restaura el punto con el azar y la agenda, apaga el registro de retroceso y re-simula con la misma lógica de las acciones. Aplica los ajustes de inventario en su posición. Si una acción re-simulada no se acepta, lanza `RuntimeError`. La copia no escribe bitácora, no emite mensajes ni toca la partida viva, y el resumen sale de ella.
- **Contenido estático.** La primera vez que se prepara una sala viva, `_marcar_preparada_viva` guarda su contenido inicial en una tabla propia de la partida (`_contenido_inicial`). La reconstrucción lee de ahí y no llama a `preparar_sala`, así que no hay E/S del contenido de las salas ni solicitudes contra el presupuesto. Esto difiere en el detalle del plan, que proponía tomar el contenido de las salas ya materializadas, y el resultado observable es el mismo.
- **Pergamino.** El pergamino revierte la última acción. `_recortar_linea_por_pergamino` trunca la línea en una acción menos, quita los puntos de control con número de acciones mayor que el nuevo largo y conserva el del borde. Anota un ajuste de inventario en esa posición con la diferencia entre el inventario previo a la acción revertida y el inventario vivo. El pergamino no se numera, y si ya había ajustes posteriores a la nueva posición se acumulan en ella.
- **Guardado.** La línea completa, el contenido inicial de las salas y la base se guardan en el formato binario, que sube de versión una sola vez y rechaza los archivos de la Parte I (FR-LIN-011).
- **K predeterminado.** K=50 (`CHECKPOINT_CADA_DEFECTO`), con `--checkpoint-cada K` para cambiarlo.


**Por qué K=50.** Es el único valor de los medidos cuyo máximo observado de consulta queda por debajo de los 50 ms de FR-LIN-018: 24.457 ms con K=50 contra 51.072 ms con K=100, el siguiente. La mediana de K=100 (32.976 ms) sí cumple, pero el máximo no. Con K=50 el registro medio es 9.2 µs por acción y el peor ciclo 1.933 ms, ambos lejos de los 20 ms. El precio es memoria: la estimación del bench para K=50 es 22873.6 KiB contra 11885.9 KiB para K=100, es decir 1.92 veces más, y el archivo guardado de una partida de 5000 acciones pesa 1288.5 KiB (ver "Tamaño del archivo de guardado"). El criterio es el máximo de 21 consultas comunes y no una garantía para toda consulta posible (ver Límites conocidos).


### Análisis de complejidad


Letras usadas: **N** = acciones vigentes, **C** = puntos de control (cerca de N/K), **K** = frecuencia de los puntos, **S** = tamaño del estado completo, **r** = registros descartados por un pergamino.
- **Pasar de un instante a una acción:** O(log N), con búsqueda binaria manual.
- **Hallar el punto de control anterior:** O(log C).
- **Reconstruir:** crear la copia aislada (copiar el mapa estático y restaurar el punto) cuesta en proporción al número de salas y al tamaño del estado, y re-simular cuesta como máximo K acciones, cada una con el costo normal de un ciclo de eventos. Una consulta no depende de N salvo por las búsquedas logarítmicas.
- **Obtener una sala por id durante la reconstrucción:** O(1) con el índice plano de `CriptaMapa` (antes O(log n)).
- **Registrar una acción:** O(1) por la acción y O(S) por cada punto de control, que ocurre una vez cada K acciones.
- **Recortar por pergamino:** O(r), con r los registros que se descartan desde el final. En la medición r fue 2.
- **Memoria:** O(N + C·S), con C = N/K. No crece como N·S (FR-LIN-016).


### Evidencia empírica


Medido con `py -m cripta --bench --solo linea_tiempo --escala 1` en el Equipo B (Intel Core Ultra 7, Windows 11, Python 3.14.6). La salida íntegra de cada corrida está en `docs/bench/resultados_004_linea_base.md` y `docs/bench/resultados_004_puntos_reducidos.md`. Cripta de referencia elegida por el mayor total de salas entre los fixtures (cripta-06, 300 salas y 760 salidas), semilla 20261117, 5000 acciones, vida máxima fijada antes de iniciar y 21 consultas comunes por escenario, incluidos los estados inmediatamente anteriores a un punto de control. Cada escenario es una partida independiente con la misma carga. La mediana y el máximo son de esas 21 consultas.


| K | Puntos | Memoria estimada (KiB) | Mediana de consulta (ms) | Máximo observado (ms) | Registro medio (µs por acción) | Peor ciclo (ms) | Máximo bajo 50 ms |
|---|---|---|---|---|---|---|---|
| 50 | 100 | 22873.6 | 11.935 | 24.457 | 9.2 | 1.933 | Sí |
| 100 | 50 | 11885.9 | 32.976 | 51.072 | 7.1 | 4.349 | No |
| 500 | 10 | 3093.4 | 119.972 | 247.549 | 2.7 | 2.667 | No |
| 1000 | 5 | 1992.5 | 210.444 | 481.429 | 2.5 | 2.745 | No |
| Sin puntos | 0 | 882.7 | 793.650 | 2232.532 | 1.8 | 2.655 | No |


Los cinco escenarios cumplen el límite de 20 ms del ciclo. La memoria estimada es la suma de `sys.getsizeof` de cada objeto que se alcanza desde la línea, sin descontar lo que comparten. **Es una cota superior** y no la memoria real, que es menor. Con K=50 la parte de las acciones es 882.6 KiB y la de los puntos 21990.9 KiB.


Lo que muestra la tabla:
- **El tiempo de consulta crece con K y la memoria baja con K.** Pasar de K=50 a K=1000 multiplica la mediana por 17.6 (de 11.935 a 210.444 ms) y divide la memoria estimada por 11.5 (de 22873.6 a 1992.5 KiB).
- **Sin puntos periódicos es inviable.** La mediana es 793.650 ms y el máximo 2232.532 ms, porque cada consulta re-simula desde el inicio.
- **El costo de registrar es bajo en todos los casos.** El peor ciclo nunca pasó de 4.349 ms.


### Cambios motivados por mediciones


**a. Índice plano por id en `CriptaMapa.obtener`.** No estaba en el plan. Un perfil de la consulta mostró que el 83 % del tiempo era re-simular y que `obtener` ocupaba el 40 % del tiempo total, porque la reconstrucción pide muchas veces la sala por id y cada pedido era una búsqueda binaria de O(log n). Se reemplazó por una lista indexada por id de sala (`_indice`), que da O(1). Es el cambio de una decisión de la Parte I (ver 5.1 y 5.6).


Medición en el mismo equipo, mediana y máximo de consulta en ms. «Antes» sale de `docs/bench/resultados_004_antes_indice.md`, medido en el commit anterior al índice. «Después» sale de `docs/bench/resultados_004_linea_base.md`, con el índice ya aplicado.


**Los dos archivos no usan exactamente la misma carga.** El de «antes» es la versión vieja de la carga: no tiene el escenario K=50, hace 16 consultas por escenario y no 21, y juega una sola partida con K=100 de la que los otros K reutilizan sus puntos de control. La carga nueva juega una partida independiente por escenario. Por eso la tabla compara solo los escenarios que existen en los dos archivos (K=100, 500, 1000 y sin puntos) y el máximo, que depende del conjunto de consultas, es el valor menos comparable. La memoria estimada de la línea es idéntica en los dos archivos para esos escenarios (por ejemplo 17690.4 KiB con K=100), así que el índice no la cambió.


| K | Antes del índice (mediana, máximo) | Después del índice (mediana, máximo) | Razón de la mediana |
|---|---|---|---|
| 100 | 59.438, 101.570 | 31.490, 53.273 | 1.89 |
| 500 | 227.926, 521.301 | 115.495, 249.615 | 1.97 |
| 1000 | 458.146, 1089.326 | 205.440, 467.162 | 2.23 |
| Sin puntos | 1901.980, 4291.973 | 856.935, 2222.919 | 2.22 |


La consulta se hizo entre 1.9 y 2.2 veces más rápida en la mediana en los cuatro escenarios. Con K=100 el máximo pasó de 101.570 a 53.273 ms. En una corrida posterior al índice, K=100 dio una mediana de 31.8 ms y un máximo de 54.6 ms, en línea con la fila anterior. `ciclo_referencia` pasó de 3.144 ms (`resultados_001_a.md`) a 2.541 ms. Las razones de la mediana son más fiables que las de los máximos, y la diferencia de carga entre los dos archivos puede explicar parte de ellas.


**b. Puntos de control reducidos (T042).** No estaba en el plan. En los puntos periódicos se omiten las salas nunca preparadas cuando sus puertas, rastro y enemigos activos permiten reconstruirlas desde el esqueleto. Solo cambia el contenido de los puntos periódicos, y no el punto inicial ni la correspondencia con la historia, el replay o el guardado. Comparación de la memoria estimada entre la línea base y la medición reducida (`resultados_004_puntos_reducidos.md`):


| K | Antes (KiB) | Después (KiB) | Ahorro |
|---|---|---|---|
| 50 | 34494.7 | 22873.6 | 33.7 % |
| 100 | 17690.4 | 11885.9 | 32.8 % |
| 500 | 4245.8 | 3093.4 | 27.1 % |
| 1000 | 2565.4 | 1992.5 | 22.3 % |
| Sin puntos | 882.7 | 882.7 | 0.0 % |


Los tiempos quedaron dentro del ruido entre corridas. La mediana con K=50 pasó de 12.616 a 11.935 ms y con K=100 de 31.490 a 32.976 ms. El máximo con K=100 pasó de 53.273 a 51.072 ms y siguió sobre los 50 ms. Con K=50 el máximo bajó de 24.817 a 24.457 ms. El ahorro es menor con K más grandes porque los puntos pesan menos en el total.


### Tamaño del archivo de guardado


Se midió el tamaño real en disco de `partida.sav` con K=50, tras jugar la partida con el mismo ayudante del bench (`_jugar_linea` de `cripta/bench/cargas_bench.py`, misma cripta de referencia y misma semilla) y guardar con `ServicioPartida.guardar`. Script propio, que se corre desde la raíz del proyecto:


```text
cliente = ClienteOffline(str(cb.DIRECTORIO_FIXTURES_BENCH))
referencia = min(cliente.listar_criptas(), key=lambda c: (-c.salas, c.id))
with cb._jugar_linea(acciones, 50, referencia.id) as corrida:
    corrida.servicio.guardar(ruta)
    tamano = os.path.getsize(ruta)
```


| Acciones | Puntos de control | Archivo (bytes) | Archivo (KiB) |
|---|---|---|---|
| 1000 | 20 | 281459 | 274.9 |
| 5000 | 100 | 1319470 | 1288.5 |


El archivo crece casi en proporción a las acciones (4.7 veces con 5 veces más acciones). **La memoria del bench y el archivo no son la misma cantidad.** La memoria del bench (22873.6 KiB con K=50 y 5000 acciones) es una cota superior, porque suma los objetos compartidos más de una vez y mide objetos de Python, y solo cuenta la línea. El archivo es el tamaño real en disco, en binario compacto, y contiene además el resto del estado de la partida. Por eso no se pueden restar entre sí. Con 5000 acciones y K=50 el archivo pesa unas 18 veces menos que la cota del bench. Una sola corrida, sin medir el tiempo de guardar ni de cargar.


### Límites conocidos


- **El estado cambiado a mano fuera de las acciones no se puede reconstruir.** La consulta re-simula acciones registradas, así que un cambio hecho directamente sobre el estado (por ejemplo subir la vida del jugador en una prueba) solo aparece si se hizo antes de iniciar la línea. Las pruebas de aceptación lo resuelven recapturando el estado base después del cambio.
- **Una ficha desalojada de la caché puede obligar a leer disco o red.** La reconstrucción no prepara salas, pero si una ficha del catálogo ya no está en memoria, pedirla puede leer disco y, sin caché de disco, gastar solicitudes del presupuesto. No se midió con la red real.
- **Una partida cargada conserva el K con que se guardó.** `--checkpoint-cada` no cambia la frecuencia de una partida ya guardada, y los puntos ya creados no se recalculan.
- **`PuntoControlGuardado.siguiente_instancia` repite el valor de su estado.** Es un dato duplicado en el formato, que ocupa espacio sin aportar información nueva.
- **La cripta de referencia ya no está fijada en el código.** Las cargas con partida real (`ciclo_referencia`, `historial_cazadores` y `linea_tiempo`) eligen la misma cripta con una función común, la de más salas entre los fixtures con desempate por menor id (cripta-06 con estos fixtures). Se eliminó la constante `CRIPTA_REFERENCIA`, que fijaba el id de una cripta concreta. Si el grupo prefiere otro criterio, solo cambia esa función.
- **El máximo observado no es una garantía.** El valor de K se eligió con el máximo de 21 consultas comunes en una máquina y una cripta. Una consulta lejos de un punto de control, en otro equipo o con otra partida, podría pasar de 50 ms.
- **La historia es una sola línea vigente.** El pergamino descarta la rama revertida (FR-LIN-007) y el inventario de instantes anteriores al pergamino se reconstruye con las acciones vigentes. Esta regla es una decisión del grupo pendiente de confirmar con el profesor.


## 5.6 Revisión de decisiones de la Parte I


Especificación: [spec.md](specs/001-terreno-cazador/spec.md). Plan: [plan.md](specs/001-terreno-cazador/plan.md), sección «Revisión de Decisiones de la Parte I», punto 3.


**Coincidencia con el plan original.** La decisión final coincide con la del plan: llamar a `gc.freeze()` al terminar `Partida.ejecutar_accion`. El plan ya la proponía a partir de las medidas de la Parte I y esta sección documenta el antes y el después con la carga nueva (P2 §7.1). Las demás decisiones de la Parte I que el plan marcó para revisar, la agenda y el historial de retroceso, se mantienen.


### Problema


Con la carga nueva hay que repetir las mediciones de la Parte I y cambiar toda decisión que deje de ser adecuada (P2 §5.6). La carga `partida` de la Parte I superaba los 20 ms con 400 salas y el límite de 4.1 lo dejaba documentado con la causa sin aislar. Con `--bench` completo, el programa terminaba con código de salida 1 y la carga `partida` con 400 salas aparecía como NO CUMPLE.


### Alternativas consideradas


Las alternativas vienen del plan, punto 3.
1. **Apagar el recolector de basura.** Deja de recoger basura cíclica nueva. Se descartó.
2. **Limpiar con `gc.collect()` en el tiempo ocioso tras cada acción.** Cada limpieza cuesta de 35 a 72 ms con 400 salas, más que el límite. Se descartó.
3. **Subir el umbral de la generación 2.** El recolector de Python 3.14 trabaja distinto y la solución no es portable. Se descartó.
4. **Mantener la decisión de la Parte I** (documentarlo como límite conocido, sin cambiar nada). Es lo que se hizo en 4.1 y deja el código de salida de `--bench` en 1.


### Decisión


Llamar a `gc.freeze()` al final de `Partida.ejecutar_accion` (`cripta/modelo/partida.py`). Ese punto cubre el juego, `--replay` y `--bench`, porque las cargas llaman a `Partida` directamente. Según el plan, la causa son las pausas del recolector. En una partida de 400 salas con 1287 acciones, una limpieza completa encuentra 0 objetos de basura cíclica y la memoria es igual con o sin limpiezas (8.5 MB), así que las pausas recorren objetos vivos, sobre todo el historial de retroceso, sin recuperar nada. Congelar los objetos vivos evita que el recolector los vuelva a recorrer.


El mecanismo se cubre con una prueba que comprueba que tras `ejecutar_accion` hay objetos congelados (T039b) y otra que ejecuta cada carga registrada a escala mínima (T039c).


### Análisis de complejidad


`gc.freeze()` mueve los objetos vivos a una generación permanente que el recolector no recorre. El plan midió unos 0.01 ms por llamada. No cambia la complejidad de ninguna operación del juego. Lo que cambia es el trabajo del recolector, que deja de recorrer los objetos congelados en cada limpieza de las generaciones mayores.


### Evidencia empírica


Equipo B (Intel Core Ultra 7, Python 3.14.6). Las cifras de «después» son la **mediana de las tres corridas** (`docs/bench/resultados_001_a.md`, `_b.md` y `_c.md`). Las de «antes» salen de `docs/bench/resultados_001_antes_gc_freeze.md`. Cada celda de la carga `partida` es la mediana de los peores casos de 3 corridas dentro del mismo archivo.


**Antes y después, carga `partida` (peor caso):**


| Salas | Antes (sin `gc.freeze`) | Después (mediana de 3 corridas) | Veredicto después |
|---|---|---|---|
| 25 | 2.004 ms | 0.354 ms | CUMPLE |
| 100 | 31.320 ms (NO CUMPLE) | 2.822 ms | CUMPLE |
| 400 | 129.766 ms (NO CUMPLE) | 13.078 ms | CUMPLE |


Con 400 salas, el tiempo típico de una acción fue 8.85 ms antes y 5.42 ms después (mediana). En las tres corridas nuevas el peor de cada repetición con 400 salas fue 13.21, 23.33 y 12.05 ms (corrida a), 12.04, 17.59 y 10.40 ms (corrida b) y 13.08, 43.16 y 12.35 ms (corrida c). El **código de salida de `--bench` completo** fue 1 antes y es 0 ahora.


**Advertencia sobre la comparación.** El archivo de «antes» se midió en peores condiciones del equipo. La carga `ciclo` con 600 actores, que es sintética y no pasa por `Partida.ejecutar_accion`, dio 14.199 ms antes contra 8.509 ms de mediana después. Por eso la diferencia entre 129.77 y 13.08 ms mezcla el efecto del arreglo con el ruido del equipo. La comparación controlada es la siguiente.


**Comparación controlada** (mismo equipo, código actual, desactivando `gc.freeze` solo para esa corrida, en las mismas condiciones y con otras aplicaciones abiertas). Carga `partida` con 400 salas, peor de cada corrida:


| Variante | Corrida 1 | Corrida 2 | Corrida 3 | Mediana | Veredicto |
|---|---|---|---|---|---|
| Con `gc.freeze` | 14.91 ms | 19.29 ms | 24.52 ms | 19.29 ms | CUMPLE |
| Sin `gc.freeze` | 32.20 ms | 42.79 ms | 51.89 ms | 42.79 ms | NO CUMPLE |


- Con 100 salas, en esa misma corrida controlada, los peores de cada repetición fueron 2.51, 1.74 y 1.80 ms con `gc.freeze` (mediana 1.80 ms, CUMPLE) y 8.62, 2.54 y 33.00 ms sin `gc.freeze` (mediana 8.62 ms, CUMPLE, con un pico de 33.00 ms en una repetición).
- El tiempo típico de una acción fue parecido (6.06 ms con `gc.freeze` y 5.20 ms sin él), así que el arreglo quita los picos y no cambia el trabajo.
- Con `gc.freeze` la mediana (19.29 ms) queda justo bajo el límite y una de las tres corridas (24.52 ms) lo supera. Estas corridas se hicieron con otras aplicaciones abiertas, por lo que son más exigentes que las de la tabla anterior.
- Un diagnóstico que registró al recolector durante el `--bench` completo encontró que, en la acción más lenta de cada repetición de 400 salas, el recolector usó menos de 3 ms y solo en la generación 0.
- **Los picos aislados que quedan no vienen del recolector, y su causa no se aisló.** Por ejemplo 23.33 ms en la corrida a y 43.16 ms en la corrida c, cada uno en una de las tres repeticiones. Por eso la carga decide con la mediana de los peores casos y no con el peor de una repetición.


**Verificación de FR-TER-020 con la carga nueva** (`py -m cripta --bench --solo ciclo_referencia`: cripta-06, 300 salas, 36 cazadores activos, en persecución por ciclo un promedio de 4.3 y un máximo de 6, 100 ciclos por 3 corridas). Peor caso 3.144 ms (mediana de las tres corridas, que dieron 3.144, 2.880 y 3.495 ms), ciclo típico 1.195 ms (mediana). El peor ciclo individual de las nueve repeticiones fue 3.948 ms. **CUMPLE** el límite de 20 ms. En la corrida de antes de `gc.freeze` una repetición había llegado a 19.882 ms.


**Cargas de la Parte I repetidas con la carga nueva** (mediana de las tres corridas, `agenda` e `historial` se miden sin cazadores):


| Carga | Parte I (4.1 y 4.6) | Ahora |
|---|---|---|
| Agenda, lista lineal contra heap con 100, 500 y 2000 eventos | 1.5x, 5.7x y 15.6x más lenta | 1.6x, 5.5x y 19.1x más lenta |
| Agenda, heap con 2000 eventos | — | 5.87 µs por operación |
| Agenda, cancelar un tercio y reprogramar un tercio | 0.33 µs por operación | 0.48 µs por operación |
| Historial, registrar una acción con inversas | 2.17 µs | 1.90 µs |
| Historial, copia completa (descartada) | 1199 µs, 553x más lenta | 767.52 µs, 413x más lenta |
| Historial, deshacer 5 acciones | 3.34 µs | 3.34 µs |
| Ciclo con 600 actores, peor de 20 ciclos | 6.17 ms | 8.509 ms |


La agenda y el historial mantienen su ventaja sobre las alternativas descartadas, con razones parecidas a las de la Parte I, y el ciclo sin cazadores sigue bajo el límite de 20 ms (1.654, 4.130 y 8.509 ms con 100, 300 y 600 actores). Las diferencias en microsegundos entre la Parte I y ahora vienen en buena parte de que se midieron en otro equipo y otro Python, así que no se interpretan como un cambio real. Se conservan las decisiones de la Parte I para la agenda y el historial.


**Revisión repetida en la 004 (T039).** Con la línea de tiempo integrada se corrió `py -m cripta --bench --solo agenda historial ciclo partida ciclo_referencia` (Windows 11, Python 3.14.6, una sola corrida) y se comparó con `docs/bench/resultados_001_a.md`. No se encontró una regresión. Las diferencias son del orden del ruido entre corridas y van en ambos sentidos, y no se fijó un umbral de regresión.


| Carga | `resultados_001_a.md` | T039 |
|---|---|---|
| Agenda, heap con 100, 500 y 2000 pendientes | 2.79, 3.80 y 5.09 µs por operación | 2.83, 3.95 y 5.41 µs por operación |
| Agenda, cancelar y reprogramar | 0.47 µs por operación | 0.40 µs por operación |
| Historial, registrar con 6 inversas | 1.90 µs | 1.59 µs |
| Historial, deshacer 5 acciones | 3.34 µs | 2.68 µs |
| Ciclo con 100, 300 y 600 actores | 1.16, 4.13 y 8.64 ms | 0.80, 4.15 y 7.12 ms |
| Partida con 25, 100 y 400 salas (mediana de los peores casos) | 0.29, 3.12 y 13.21 ms | 0.34, 2.26 y 9.80 ms |
| `ciclo_referencia` (cripta-06, 36 cazadores) | 3.144 ms | 2.675 ms |


Todos los casos de `ciclo`, `partida` y `ciclo_referencia` cumplen el límite de 20 ms. Se conservan las decisiones de la Parte I para la agenda (montículo con orden `(tiempo, secuencia)`) y el historial de retroceso (inversas por cambio). **Una decisión de la Parte I sí cambió: la consulta de salas por id de `CriptaMapa`.** Pasó de búsqueda binaria a un índice plano por id con costo O(1), porque un perfil de la consulta histórica mostró que `obtener` ocupaba el 40 % del tiempo total (en 4.7 la búsqueda binaria del mapa había ocupado cerca del 8 % en otra carga). Con el índice, `ciclo_referencia` pasó de 3.144 ms a 2.541 ms en la medición de la sección 5.5. La carga `historial` sigue siendo sintética y sin cazadores. El costo del retroceso con cazadores se midió con la carga nueva `historial_cazadores`, descrita más abajo en esta sección.


**Cuidado con la carga `historial`.** Es la misma carga sintética de la Parte I (6 inversas por acción, 200 salas y 60 actores) y **no tiene cazadores**. No mide el costo del historial con decenas de cazadores moviéndose entre dos acciones, que era el riesgo que el plan anotaba para el responsable de la capacidad 004. Ese riesgo se midió después con una carga propia, `historial_cazadores`, con `py -m cripta --bench --solo ciclo_referencia historial historial_cazadores` a escala 1 en el Equipo B y en una sola corrida. Sobre la cripta de referencia (cripta-06 con estos fixtures), con 36 cazadores activos al medir, cada una de 500 acciones se ejecutó, se revirtió con la acción pergamino real y se volvió a ejecutar. El intervalo de una acción registró una mediana de 200 operaciones inversas, un máximo de 637 y un mínimo de 21, frente a las 6 de la carga sintética. Revertir tardó una mediana de 267.5 µs y un máximo de 1435.9 µs por acción, con 1.37 µs por inversa en promedio. La carga sintética dio en esa misma corrida 5.44 µs por acción y 0.91 µs por inversa (la corrida de `historial` del mismo comando dio 4.04 µs por acción). Con cazadores, la mediana de revertir fue 49.2 veces la sintética. Casi todo ese aumento viene de la cantidad de inversas (200 contra 6, unas 33 veces más) y poco del costo de cada una (1.5 veces). El máximo de 1435.9 µs queda muy por debajo de los 20 ms del ciclo, que se usa aquí solo como referencia.


Límites de esa medición. Es una sola corrida. El tiempo es el de la acción pergamino completa, que incluye invalidar las rutas, quitar el pergamino y recortar la línea. Los 36 cazadores se activan desde el inicio, igual que en `ciclo_referencia`, así que cada acción tiene más trabajo que en una partida normal. El costo de registrar las inversas no se midió por separado, solo cuántas son. En esa misma corrida `ciclo_referencia` dio un peor caso de 4.526 ms (peores de cada corrida 14.007, 4.526 y 4.502 ms) y cumple el límite de 20 ms por la mediana de los peores casos.


### Límites conocidos


- **La basura cíclica entre objetos congelados no se recupera.** Tras `gc.freeze()` los objetos vivos de ese momento dejan de revisarse, así que si más tarde quedan formando ciclos que ya nadie usa, el recolector no los libera. En la partida de 400 salas se midió 0 objetos de basura cíclica, pero con partidas mucho más largas o con otros patrones podría acumularse memoria. No se midió.
- El recolector se sigue ejecutando sobre los objetos nuevos, así que la basura cíclica creada después de cada congelación sí se recoge.
- Quedan picos aislados que superan los 20 ms en repeticiones sueltas (23.33, 43.16 y 24.52 ms en algunas corridas). No vienen del recolector según el diagnóstico y su causa no se aisló. La decisión de cumplimiento se apoya en la mediana de los peores casos, como en la Parte I.
- La comparación «antes» de la tabla se hizo en condiciones del equipo distintas a las de «después» (ver la advertencia). La evidencia más sólida del efecto es la comparación controlada de 400 salas, con 19.29 ms con `gc.freeze` y 42.79 ms sin él.
