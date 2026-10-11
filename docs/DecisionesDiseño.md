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



### Límites conocidos
Pendiente — completar en reunión (revisar para eliminar esta linea)

La cancelación es perezosa: los eventos cancelados siguen ocupando espacio en el montículo hasta que les toca salir. Con muchas cancelaciones sin consumir eventos, la agenda puede crecer más que el número de eventos vigentes (con 100 000 reprogramaciones, el montículo llegó a 100 001 entradas). Si eso fuera un problema, habría que compactar el montículo cada cierto número de cancelaciones.

No se puede programar un evento en un tiempo anterior al del reloj (se lanza `ValueError`). El retroceso del pergamino restaura el reloj con un método propio (`restaurar`) en vez de programar hacia atrás.



## 4.2 Traer el contenido antes de que haga falta (precarga)
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

## 4.3 Resolución de referencias del catálogo
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

## 4.4 Reutilización y caché persistente
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
Pendiente — completar en reunión
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
Pendiente — completar en reunión
### Análisis de complejidad
Pendiente — completar en reunión
### Evidencia empírica
Pendiente — completar en reunión
### Límites conocidos
Pendiente — completar en reunión

## 4.11 Bitácora de partida y reproducción
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
