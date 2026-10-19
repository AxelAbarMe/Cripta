# 20/09/2026

Antes de programar nada se hizo una prueba directa al API para ver qué devuelve el servidor de verdad y no solo lo que dice el Swagger. Se creó un script prueba_api.py que consulta las criptas publicadas, los datos generales, el esqueleto por páginas, el contenido de las salas y el catálogo por lotes, imprimiendo el código de estado y el JSON de cada respuesta. Con eso se confirmó la cripta-01 (Osario menor) de 6 salas y se revisaron los casos raros de los datos.

Después se empezaron los DTO con los de la cripta y los del esqueleto. Se usó dataclass con frozen y slots para que los DTO queden inmutables y pesen menos, porque lo que cambia durante la partida es estado del modelo y no del DTO. Cada DTO tiene su método desde_json que es el único lugar donde se toca el diccionario que devuelve respuesta.json(), así el dict solo se usa para leer el JSON como lo permite el enunciado y de ahí para adentro el programa trabaja con objetos.

Los DTO que quedaron hechos son:
* CriptaResumenDTO
* JugadorInicialDTO
* CriptaGeneralDTO
* SalidaDTO
* SalaDTO
* PaginaEsqueletoDTO

Se definió que va una clase por archivo en dto/, igual que como se hace en Java, para que el criterio sea parejo en todos los DTO que falten. También las salidas no se guardan como diccionario sino en cuatro campos fijos norte, sur, este y oeste, porque las direcciones siempre son máximo cuatro y así no se ocupa ninguna estructura de búsqueda.

Lo siguiente que hay que realizar son los DTO que faltan, que son los del contenido de las salas, los del catálogo con una ficha por cada clase y los de versiones, y después el cliente HTTP en infraestructura/ que debe usar un solo UUID por ejecución, revisar el código de estado antes de leer el JSON, esperar y reintentar cuando llega un 429, y llevar la cuenta de las solicitudes para no pasarse del presupuesto.

# 26/09/2026

Ya los DTO se encuentran al 100%, no hay que agregar nada y eso está verificado porque yo hice los DTO basados en el server, donde devuelve cada JSON y todo eso ya se maneja automatico

Ya las estructuras, todas estan implementadas, solo hay que justificarlas, ahora mismo hay:
* Cola simple
* Cola Circular
* Vector Ordenado
* Pila
* Lista enlazada
* Lista Doble enlazada
* Heap Minimo
Todos esos ya deberian de servir para todo lo que vayamos a ocupar, entonces si ocupan cambios son minimos.

Ya las carpetas *bench/*, *controlador/*, *vista/*, *modelo/* tienen todos los archivos o una gran mayoria agregada, la *infraestructura/* le agregue los .py faltantes, pero todos esos ahora mismo estan vacios, solo están agregados, tambien agregue un ___main___.py, excepciones.py y constantes.py en la raiz de *cripta/*.

Lo siguiente que hay que realizar es el *modelo/* porque eso ya es como tal la lógica de todo, hay como 13 archivos de modelo, luego hay que ver, pero varios archivos son herencia *actor.py le hereda a jugador.py y enemigo.py*

# 30/09/2026

Los DTO no se modificaron, se modificaron algunas estructuras como la lista doble para agregar un puntero que apunte al final para O(1)
Se agregaron selector de ordenamientos y cambios mínimos en el resto de estructuras como Pila, Lista, Vector.

Ya las carpetas *bench/*, *infraestructura/*, *servicios/*, *modelo/* tienen archivos con códigos, pero no revisados en su plenitud.
Infraestructura se le fue agregado selector de cliente, la lógica del cache con el almacen y guardado en disco, junto con auxiliares de serialización para el guardado de la información de la partida.

Además, estados de guardado, modificación a puertos.py y agregado código en partida_log.py para --replay

Luego en modelo se cambiaron todos los .py en cada uno se agregó lógica que utiliza constantes.py para información global del juego, actor.py le entrega información tanto a jugador.py como enemigo.py, cripta_mapa.py extrae información de las sala.py para la creación del mapa. Además, se presenta la lógica del reloj que aplica a todo el modelo y es el que efectua todas las acciones de cada sección.

Finalmente se agregaron los servicios, bench y test con información temporal no justificada ni revisada para avanzar en el trabajo del grupo.

Faltante:
* Revisar DTO
* Revisar Estructuras
* Justificar Estructuras en Decisiones.md
* Agregar prompts utilizados para explicación de lógica y creación de código.
* Revisar Infraestructura
* Revisar Modelo
* Revisar Servicios
* Revisar Bench
* Revisar Test/
* Revisar constantes.py y excepciones.py
* Agregar comentarios a todos los archivos .py de todas las carpetas anteriores y revisar indexado, código y comentarios existentes
* Revisar lógica de cada archivo pendiente y realizado, realizar nombres de archivos, import, variables, métodos, clases, etc.
* Crear código para Vista/
* Crear código para Controlador/
* Crear documentación válida de todo el proceso del proyecto por cada carpeta o capa del MVC
* Crear documentación para parte de Vista y Controlador en el caso de Python
* Agregar código restante para el juego completo en caso de que sea necesario modificar, agregar o eliminar archivos.py ya existentes
* Revisar requierements.txt
* Eliminar prueba_apy.py o moverla a pruebas de Test/
* Revisar README.md actualizado con la información actual

Opcional:
* Revisar posibilidad de transformar sistema monolítico actual en una app basada en microservicios
* Revisar disponibilidad para creación de interfaz gráfica para el sistema de la app de Cripta


# 06/10/2026

Se revisó el proyecto completo contra el enunciado: base, estructuras, DTO, infraestructura, modelo, servicios y bench, ejecutando el código en cada capa para confirmar los fallos en vez de suponerlos. El diseño general es correcto, pero había 9 bugs que impedían que varias partes corrieran, y todavía no existe el motor del juego, ni el controlador, la vista, el guardado desde el modelo ni el replay.

Se corrigieron los bugs que bloqueaban al resto:
* Constantes: faltaban CACHE_TAMANO_DEFAULT y MAX_ELEMENTOS_POR_LOTE, así que no se podían importar el servicio de catálogo ni el de precarga.
* Lista doble enlazada: no inicializaba su tamaño, no tenía __len__ y agregar y agregar_inicio no devolvían el nodo. Con eso el inventario no podía recoger objetos y la caché LRU fallaba al desalojar.
* ContenidoSalaDTO tiene el campo id y no sala; se corrigió en cache.py, serializacion.py y servicio_precarga.py.
* Veneno: llamaba a un método que no existe, así que fallaba en su primer pulso.
* VectorOrdenado.insertar reordenaba todo el vector en cada inserción, lo que era cuadrático (unos 3.5 s con 8000 salas) y fallaba con claves repetidas. Ahora busca el punto de inserción con búsqueda binaria y solo compara claves.
* El bench de ciclo llamaba a una función de combate que no existe.

También se separaron constantes.py y excepciones.py en secciones por dueño para evitar conflictos al trabajar en paralelo. Con estos cambios los imports funcionan, la lista doble responde bien y el bench corre sus 8 cargas completas; el ciclo de eventos cumple el límite de 20 ms (6.17 ms con 600 actores, medición sintética).

Lo siguiente que hay que realizar:
* Endurecer el cliente HTTP: errores de red con contexto y tope de reintentos por 429 dentro del presupuesto.
* Generar los fixtures y el formato --offline propio.
* Sincronizar las dos caras de una puerta y validar el reloj y la velocidad de los efectos.
* Escribir el motor del juego, el retroceso completo, el puente con el guardado y el replay.

Más tarde se empezó con la parte de red. El cliente HTTP ahora convierte cada error de red (sin conexión o tiempo agotado) en un error propio del juego que dice qué operación falló, y ante un 429 (el servidor pide esperar porque llegaron demasiadas solicitudes) espera y reintenta como máximo un número fijo de veces; cada reintento cuenta como una solicitud del presupuesto, como lo pide el enunciado. La validación de los lotes (que una solicitud no pida más elementos de los permitidos) quedó en un solo lugar, compartida por el cliente de red y el de archivos, y ClienteGeneral ya no revisa el presupuesto dos veces.

# 07/10/2026

Se escribió el contrato de la API pública de Partida (docs/CONTRATO_PARTIDA.md): construcción, acciones del jugador, resultados, consultas, guardado y replay. Sirve de referencia para el motor, el controlador y el reproductor de replay.

Se reforzó el modelo para poder implementar el retroceso y el guardado:
* Reloj de eventos: ya no acepta eventos en el pasado, cuenta los eventos vigentes (esta_vacia ignora los cancelados) y expone siguiente_secuencia, restaurar, restituir y programar_con_secuencia, que se necesitan para revertir la agenda y reconstruir una partida guardada.
* Efectos: un veneno nuevo reemplaza al anterior y reinicia su duración; el actor guarda su veneno activo para que el antídoto lo pueda cancelar. El cambio de velocidad resta al terminar lo que él mismo sumó, de modo que varios efectos solapados no se pisan, y la velocidad nunca baja de VELOCIDAD_MINIMA.
* Historial de retroceso: registrar sin un intervalo abierto, o abrir un intervalo con otro ya abierto, lanza CriptaHistorialError en lugar de perder cambios en silencio.
* Mapa: las dos caras de una puerta se abren y se cierran juntas, y sincronizar_puertas deja cerradas las dos si una sola lo estaba. Agregar una página repetida se ignora. Se agregó puerta_transitable para el movimiento y el comportamiento de los enemigos.
* Inventario: ir_a_posicion, conteo y consumo de pergaminos, fichas_en_uso para la caché, orden por nombre sin distinguir mayúsculas ni tildes y vistas ordenadas con el selector automático.

Se documentaron en el Documento de Decisiones la agenda de eventos (4.1), el retroceso (4.6) y el inventario (4.5).

Lo siguiente que hay que realizar:
* Enemigos: comportamientos guardián, errante y rastreador, con referencias directas a las salas vecinas.
* Motor Partida: acciones del jugador con sus costos, activación de enemigos, movimiento que espera contenido, trampas, muerte de actores, victoria y derrota.
* Retroceso completo, puente entre el modelo y el guardado, y replay.

En la parte de red, los errores de formato (una respuesta que no tiene la forma esperada) ahora dicen en qué operación ocurrieron, tanto en el cliente de red como en el de archivos, y el mensaje de CriptaApiError ya no muestra un código vacío cuando no hubo respuesta del servidor. El cliente falso de los tests (un cliente que responde sin red, con datos inventados) pasó a usar la misma validación de lotes y a reportar bien el total de salas, y la cripta artificial de los tests ganó una llave de salida para poder probar la victoria. Se escribió el script scripts/generar_fixtures.py, que descarga del API todas las respuestas de una cripta y del catálogo y las guarda en fixtures/ para jugar con --offline; se generaron las de cripta-01 y se documentó el formato en docs/FORMATO_OFFLINE.md.

# 08/10/2026

Se unieron las dos ramas de trabajo en main y se comprobó el proyecto completo: los imports funcionan, el bench corre sus 8 cargas y el ciclo de eventos cumple el límite de 20 ms. Con los datos reales de cripta-01 guardados en fixtures/ se probó el flujo completo (cliente offline, mapa, catálogo y precarga) y los enemigos, las puertas y las fichas se construyen correctamente: un enemigo sin vida declarada nace con su vida máxima, el comportamiento "guardián" llega con tilde y la llave y el cierre automático de una puerta vienen marcados en un solo lado de la salida.

Se agregó al mapa datos_de_puerta, que devuelve la llave y el cierre automático de una puerta mirando sus dos lados.

Se escribió comportamiento_enemigo.py con la decisión del turno de un enemigo (2.8): si comparte sala con el jugador ataca; si no, el guardián espera, el errante elige al azar una salida abierta y el rastreador sigue el rastro fresco más reciente de las salas vecinas, con desempate por menor id. El módulo solo decide; ejecutar la acción lo hará el motor.

Se escribió accion.py con las 9 acciones del jugador definidas en el contrato de Partida, con su validación, su costo base y su conversión a dict para la bitácora de la partida.

Se escribió el primer trozo del motor (partida.py y resultado_partida.py): construcción de la partida con su generador de azar propio, inicio según 2.4, ciclo de eventos hasta el siguiente turno del jugador, turnos de los enemigos (atacar, moverse o esperar), derrota, la consulta vista() con todo lo que debe mostrar la interfaz y la acción esperar. Se probó con la cripta real de fixtures: con la misma semilla dos partidas producen exactamente los mismos mensajes y tiempos, y con otra semilla cambian.

Lo siguiente que hay que realizar:
* Motor Partida, trozo 2: mover y abrir (llave comparada con el id de la ficha y cierre automático), trampas y victoria.
* Motor Partida, trozo 3: atacar, recoger, usar, equipar, soltar y pergamino.
* Retroceso completo y puente entre el modelo y el guardado.
* Replay.

El profesor confirmó que para --offline se guardan los JSON que devuelve el API y que la organización de los archivos queda a criterio del grupo; se anotó en el documento del formato. Se corrigieron detalles de los DTO: el campo cerrada de una salida es siempre booleano (un null del JSON queda como falso), el campo abre de una llave acepta texto o número, el rearme de una trampa puede faltar y entonces se usa el valor por defecto, y el archivo de ContenidoSalaRespuestaDTO se renombró para que tenga el mismo nombre que la clase. Se rehízo la bitácora de la partida para que el replay la pueda leer: un archivo por partida, una primera línea con la cripta, las versiones y la semilla, y luego una línea por acción; si la última línea quedó cortada (por ejemplo, porque el programa se cerró mientras escribía) se ignora con un aviso, y si el encabezado no es válido o las versiones no coinciden, se informa.

# 09/10/2026

Se completó el segundo trozo del motor Partida: mover, abrir, trampas, cierre automático y victoria. El movimiento rechaza una dirección sin salida o con puerta cerrada, espera a tener el contenido de la sala destino antes de confirmarse (la espera real no mueve el reloj virtual), refresca el rastro, activa a los enemigos dormidos de la sala y aplica las trampas armadas antes de procesar el siguiente evento. Abrir comprueba que el jugador tenga la llave comparando el id de la ficha, y busca la llave y el cierre automático en los dos lados de la puerta porque el API solo los marca en uno. El cierre automático cierra ambos lados. Entrar a la sala de salida con vida termina la partida con victoria. Se probó con la cripta real de fixtures: rechazos, trampa, ataques de enemigos, abrir con llave, cierre automático con el jugador al otro lado de la puerta y victoria.

Se dejó pendiente decidir qué hacer con la bitácora de la partida al cargar una partida guardada (seguir en la misma o empezar una nueva).

Se completó el tercer trozo del motor Partida: atacar (el enemigo que muere cancela su evento pendiente, sale de la sala y suelta sus objetos), recoger (con rechazo sin consumir tiempo si el inventario está lleno), soltar, equipar y usar objetos (curar, cambiar la velocidad con reajuste del turno pendiente, cancelar el veneno con un antídoto y encender una antorcha). Se agregó al inventario posicion_actual y a la vista objeto_actual_indice para que la interfaz pueda pedir acciones por posición. Se probó con la cripta real de fixtures y con fichas inventadas para el antídoto y la poción de velocidad, que la cripta publicada no trae.

El pergamino de retroceso queda para cuando se haga el retroceso completo, porque necesita registrar la inversa de cada cambio.

Se corrigió la vista para que los objetos del suelo lleguen con su id de ficha y su nombre, porque la interfaz necesita el id para pedir recoger. Se revisó el modelo en busca de código sin uso: EfectoCierrePuerta cerraba solo un lado de la puerta, lo que contradecía que una salida conecta dos salas, así que se adaptó para cerrar ambos lados y ahora lo usa Partida; Enemigo.etiqueta no se usaba y Partida repetía su lógica, así que ahora la usa; y sincronizar_puertas no lo llamaba nadie, lo que dejaba cruzar una puerta con llave desde el lado sin marcar, así que ahora lo llama Partida al crearse.

Se empezó el retroceso completo con los ganchos de inversa de cada objeto del modelo: una base Reversible que guarda el valor anterior de cada atributo que cambia, inversas explícitas en el reloj, las listas de la sala y el inventario, y un gancho del historial que ignora los cambios fuera de un intervalo y permite pausar el registro. Al probar el inventario se descubrió que reponer un objeto crea un nodo nuevo, así que las inversas buscan por objeto. Al usar la base también en el reloj el ciclo de eventos subió a 17 ms, por lo que el reloj registra de forma explícita. Se agregaron tests unitarios en tests/modelo.

Se completó el retroceso con el pergamino: Partida conecta el registro de inversas a todos los objetos que cambian, abre un intervalo por acción aceptada y lo descarta si la acción se rechaza, y la acción pergamino revierte el último intervalo sin consumir tiempo ni contar como acción. El pergamino usado se descuenta fuera de la reversión y recoger o soltar un pergamino dentro del intervalo no se deshace; el estado del azar también se restaura. Se agregaron tests con la cripta real para los casos del Apéndice B (dos pergaminos seguidos, pergamino recogido en el intervalo, tope de 5 acciones). Con la base Reversible en los actores el ciclo de eventos costó cerca de un 10 % más, sin acercarse al límite de 20 ms.

Lo siguiente que hay que realizar:
* Puente entre el modelo y el guardado.
* Servicio que arma la partida y coordina la bitácora, el puntaje y el reporte final.
* Replay, y decidir qué hacer con la bitácora de la partida al cargar una partida guardada.

Se revisó el guardado binario: los formatos de struct (el módulo de Python que convierte números a bytes) se preparan una sola vez y los campos de cada registro se escriben juntos, antes de escribir se valida que cada valor quepa en su campo y al leer se valida la estructura del archivo, para detectar un archivo dañado en vez de cargar datos incorrectos. En la caché en disco, un archivo dañado ahora cuenta como ausente, así la ficha o la sala se vuelve a pedir una sola vez en lugar de gastar solicitudes de más. En el servicio del catálogo, pedir varias fichas con un id repetido cuenta aciertos y fallos igual que pedirlas una por una.

# 10/10/2026

Se midió el rendimiento del ciclo de eventos en dos series de cinco corridas, la segunda con el recolector de basura desactivado: la mediana fue de 7.1 y 7.5 ms con 600 actores activos, muy por debajo del límite de 20 ms, aunque aparecieron picos aislados (el mayor, 23.3 ms) que desactivar el recolector no eliminó. Se documentó el resultado y su límite en el Documento de Decisiones.

Se empezó el guardado de la partida. Los eventos de la agenda ahora declaran sus datos para poder escribirse en un archivo, y Partida.a_estado_guardado convierte la partida viva a EstadoPartida: reloj, estado del azar, jugador, inventario, salas visitadas con sus enemigos, trampas y puertas, y la agenda pendiente. Se agregó el módulo persistencia_modelo.py y tests con la cripta real: estado inicial, sala con enemigos y trampa, puerta con cierre automático, antorcha, ida y vuelta por el archivo binario (incluida la carga de una sala suelta) y mismo estado con la misma semilla.

Se completó el guardado de la partida con su segunda parte: Partida.desde_estado_guardado reconstruye el modelo desde un EstadoPartida (salas visitadas, enemigos, trampas, puertas, rastro, inventario, jugador, azar, mensajes) y recrea las acciones de la agenda a partir de sus descriptores; cada efecto sabe volver a programar su evento guardado. Al probarlo se encontró y corrigió un fallo de la primera parte: un enemigo activo que caminaba a una sala sin visitar se perdía al guardar. Los tests con la cripta real comparan una partida guardada y cargada contra una que nunca se guardó, incluso pasando por el archivo binario.

Lo siguiente que hay que realizar:
* Servicio que arma la partida y coordina la bitácora, el puntaje, el guardado y el reporte final.
* Decidir qué hacer con la bitácora de la partida al cargar una partida guardada, y el replay.

En la precarga (el servicio que pide en segundo plano el contenido de las salas antes de que el jugador llegue), la espera por un lote quedó limitada a ESPERA_MAXIMA_LOTE_SEGUNDOS y, una vez cerrado el servicio, ya no acepta pedidos nuevos. Al poblar una sala, los enemigos se ordenan con ordenar_auto, el selector de algoritmo de ordenamiento, como lo pide el enunciado. ColaCircular lanza su propio error, ColaCircularVaciaError, en vez de una Exception genérica, y rechaza una capacidad inválida.

# 11/10/2026

Se agregó ServicioPartida, que arma la partida a partir de un cliente (de red o de archivos): obtiene los datos generales, fija el presupuesto con el valor de la cripta, consulta una vez la versión del catálogo, carga el esqueleto, crea el catálogo y la precarga, inicia la partida y escribe en la bitácora cada acción aceptada con su encabezado. También entrega el reporte final de solicitudes, presupuesto y aciertos y fallos de caché. Se conectó la caché del catálogo con el estado del juego mediante Partida.fichas_en_uso, de modo que las fichas del inventario, del suelo y las trampas de la sala actual y de los enemigos vivos no se desalojan. Al probarlo se encontró que una acción que fallaba a mitad de camino por un error de infraestructura dejaba cambios sin deshacer; ahora se revierte el intervalo abierto. Se agregaron tests con la cripta real: solicitudes en frío y con la caché caliente, bitácora, reproducción de una partida desde su bitácora, caché chica y fallos de infraestructura.

Se agregaron al servicio de partida guardar y cargar. Guardar escribe el archivo binario y, junto a él, una copia de la bitácora hasta ese instante; cargar valida las versiones de la cripta y del catálogo, reconstruye la partida y restaura esa bitácora, de modo que la partida sigue en la misma historia sin acciones de una rama abandonada. Si falta la copia, la bitácora nueva queda marcada como parcial. También se agregó el puntaje final con victoria o derrota: se guarda en la tabla local al terminar y el ranking se muestra por cripta y versión, con las victorias primero. Se probó con la cripta real, incluida la reproducción desde cero de la bitácora de una partida cargada, y la carga en frío cuesta las mismas 6 solicitudes que iniciar una partida.

Lo siguiente que hay que realizar:
* Replay (--replay), con revisión de las versiones y rechazo de las bitácoras parciales.
* Medir el ciclo real de una acción contra el límite de 20 ms.
* Controlador y vista, y el programa principal con sus banderas.

La tabla de puntajes se guarda en disco con RepositorioPuntajes, en datos/puntajes, y se ordena con ordenar_auto. En el bench se agregó la carga partida, que mide el ciclo de eventos con el motor real del juego sobre criptas artificiales de varios tamaños, con tres corridas, su tiempo típico y su peor caso, para compararlo con el límite de 20 ms. El bench del inventario dejó de cronometrar la construcción de la lista, para medir solo la operación que compara, y su texto dice explícitamente qué compara.

# 16/10/2026

Se hizo pull de lo último de main y se terminó el bench de solicitudes de red. Esta carga compara, sobre criptas artificiales de 100 y 400 salas, cuántas solicitudes gasta la precarga pidiendo el contenido de las salas por lotes (varias salas en una sola solicitud) contra pedir una sala por solicitud, y lo mismo con las fichas del catálogo. Con lotes se gastan 10 solicitudes contra 90 en 100 salas y 40 contra 380 en 400 salas; en el catálogo, 4 lotes contra 7. Se limpió el código del bench que ya no se usaba y los textos de cada comparación ahora dicen cuál alternativa es más rápida y cuántas veces.

Se reorganizaron las pruebas para que corran todas juntas con `py -m unittest discover -s tests -t .`: cada carpeta de tests lleva un archivo `__init__.py` vacío, que es lo que le indica a Python que esa carpeta es un paquete y que discover debe entrar en ella. Los tests de ServicioPartida pasaron a tests/servicios, para que tests/ tenga la misma estructura que cripta/.

Se agregaron pruebas unitarias de la parte de infraestructura y servicios que aún no tenía:
* ColaCircular: orden de salida, capacidad, vuelta del índice al llegar al final y error al sacar de una cola vacía.
* Bitácora de partida: escribir y leer, una línea final cortada a la mitad, encabezados inválidos y diferencias de versión.
* Guardado binario: ida y vuelta por el archivo, leer una sola sala con el índice, valores que no caben en su campo y archivos dañados.
* Caché en disco: la versión forma parte de la clave, un archivo dañado se trata como ausente y una ficha dañada se vuelve a pedir en el mismo lote que las demás.
* Archivo de puntajes: formato 2, un archivo dañado no se sobrescribe y las filas inválidas se rechazan.
* ServicioCatalogo: estadísticas de aciertos y fallos, pedidos por lotes, desalojo de la ficha usada hace más tiempo y fichas en uso que no se desalojan.
* ServicioPrecarga: mínimo de lotes, espera máxima por un lote, respuesta que llega tarde, cierre del servicio y enemigos ordenados.

Al escribir los tests de la precarga se vio que los enemigos de una sala se ordenaban en cada vuelta del ciclo que los crea; se corrigió para ordenarlos una sola vez al terminar de poblar la sala.

Lo siguiente que hay que realizar:
* Escribir en el Documento de Decisiones las secciones de precarga, catálogo, caché, ordenamiento, guardado binario y bitácora con replay, con sus mediciones.
* README con la instalación, las banderas y los comandos.
* Bitácora y prompts de la parte de red, disco y servicios.


# 17/10/2026

Se corrigió el orden de las derrotas en la tabla de puntajes: ahora gana la que derrotó más enemigos y, en un empate, la que sobrevivió más tiempo. Las victorias siguen yendo primero, de menor a mayor tiempo. La tabla ganó un método de puntajes globales (todas las criptas y versiones, con la misma regla) y el servicio de partida lo expone sin necesitar una partida en curso, de modo que el menú ya no usa el orden antiguo por tiempo. Se quitó un punto y coma sobrante en el módulo de combate y se eliminó del informe del replay una línea suelta que no era parte del informe. La carpeta de datos generados al jugar (caché, puntajes y partidas) salió del seguimiento de git y quedó en el archivo de exclusiones. Se comprobó que el replay reproduce bien una partida jugada sin conexión; sin esa opción usa la red y falla con un mensaje claro. Se agregaron tests del orden de los puntajes (incluida una tabla de 160 filas, sobre el umbral del selector de algoritmo) y de los puntajes globales del servicio; la suite completa pasó con 180 tests.

Una revisión posterior encontró que el método de puntajes globales y el nuevo orden del ranking no habían quedado en la tabla de puntajes, y que faltaba el archivo de tests de ese orden. Se completaron ambos y la suite volvió a pasar completa (180 tests).

Se integró el trabajo de la interfaz y la red: el inventario pasó a ser circular, la victoria exige abrir con la llave de salida la puerta cruzada, el contador de solicitudes se reinicia en cada partida nueva y el programa principal ya admite `--offline`, `--cache-size`, `--bench` y `--replay` sin crear la vista. Se completaron en el documento de decisiones las secciones de agenda de eventos, inventario, retroceso, rastro y bitácora en pantalla, con la medición del rastreador y de la cola circular contra sus alternativas. El rendimiento del ciclo con la partida real, medido con el equipo en reposo (mediana de 5 ejecuciones), cumple el límite de 20 ms con 25, 100 y 225 salas; el caso de 400 salas queda documentado como límite conocido.

Lo siguiente que hay que realizar:
* Medir el costo de guardar los contadores del azar en cada acción.
* Completar las decisiones de diseño pendientes y los textos de límites.
* Revisión final de todo el proyecto.

En la noche se empezaron a escribir en el Documento de Decisiones las secciones de la parte de red y disco: 4.3 (cómo se piden por lotes y se guardan en memoria las fichas del catálogo), 4.4 (la caché, con su regla de desalojo y su copia en disco) y 4.2 (la precarga de salas). Para la evidencia se corrieron las cargas del bench y una prueba de la precarga con 400 ms de latencia simulada (el retraso que se agrega a cada respuesta del servidor): con el jugador moviéndose sin pausas, solo 8 de 89 movimientos tuvieron que esperar el contenido de la sala, 4.48 s en total. Las tres secciones se terminaron pasada la medianoche.

# 18/10/2026

Se hizo pull de lo último de main, con las banderas del programa principal y el replay, y se hicieron arreglos pequeños: el cliente HTTP tenía un import repetido, el número máximo de reintentos ante un 429 pasó a constantes.py junto a los demás valores del juego, se actualizaron comentarios que habían quedado viejos (el formato 2 del archivo de puntajes y lo que guarda el fin de un cambio de velocidad), se quitaron los nombres de personas de los encabezados de los archivos, la carpeta datos/ quedó fuera de git y el script de la primera prueba del API (prueba_api.py) pasó a scripts/, sin el código viejo que tenía comentado. Se quitó de requirements.txt la dependencia pytest, que no se usaba: las pruebas usan unittest, que viene con Python.

Se completaron en el Documento de Decisiones las secciones 4.9, 4.10 y 4.11:
* 4.9 (ordenamiento): cómo ordenar_auto elige el algoritmo según la cantidad de elementos y si ya vienen casi ordenados, con la tabla de tiempos de los algoritmos en 12 casos medidos con el bench, el caso de comparaciones costosas y la regla de orden del ranking de puntajes con sus tests.
* 4.10 (guardado binario): el formato del archivo, con un índice que permite leer una sola sala sin leer el archivo completo (0.048 ms por sala) y un tamaño entre 2.5 y 2.8 veces menor que el mismo estado guardado en JSON.
* 4.11 (bitácora y replay): el formato de la bitácora y cómo el replay la verifica. Como evidencia se reprodujo una partida real con la semilla 2734113286: las 5 acciones se reprodujeron igual y terminó en la misma derrota, en el tiempo 373.

Se escribió el README con la instalación, cómo ejecutar el juego y sus banderas (--offline, --cache-size, --replay y --bench), los comandos de la consola, los archivos que genera el juego en datos/ y cómo correr las pruebas.

Al revisar las pruebas se vio que las carpetas tests/vista y tests/controlador no tenían su archivo __init__.py, así que discover no entraba en ellas y sus 33 tests nunca se ejecutaban. Se agregaron los dos archivos y la suite completa pasó con 213 tests.

Se completó la bitácora de la parte de red, disco y servicios de los días 6 al 17 de octubre, que no se había registrado.

Se hizo pull de los últimos cambios de main. Trajeron pruebas nuevas para el manejo del HTTP 429 (el servidor pide esperar porque llegaron demasiadas solicitudes): el cliente HTTP espera el tiempo indicado por el servidor y reintenta, cada reintento cuenta en el presupuesto, todos los reintentos usan el mismo identificador de cliente, un 429 sin tiempo indicado espera un segundo, un 429 que no se resuelve termina con un error que nombra la operación después de MAX_REINTENTOS_429 reintentos, y con el presupuesto agotado nunca se supera el máximo. Otra prueba comprueba que ese error de red, mostrado desde el controlador, no cierra el juego: se muestra el mensaje y se vuelve al menú. La suite completa pasa con 222 pruebas.

Se hizo una revisión completa de la documentación sobre la versión más reciente del proyecto:
* Documento de Decisiones: no queda ninguna línea marcada como pendiente de revisar y las 11 secciones tienen sus seis partes, incluida la decisión de 4.7. Se corrigió una contradicción en 4.1 sobre la muerte de un enemigo (el motor cancela su evento pendiente y, además, el turno comprueba que siga vivo), se actualizó el texto de límites de 4.6, que decía que había que repetir la medición cuando el motor registrara inversas reales (ya lo hace y esas inversas están incluidas en las mediciones de la partida real de 4.1), se indicó en 4.5 que el recorrido del inventario es circular, se quitó un párrafo repetido en los límites de 4.7, se aclaró en 4.10 que el archivo binario no contiene JSON, se indicó en 4.4 por qué no se usa una tabla hash y se corrigió un formato roto en 4.2.
* PROMPTS_LLM.md: se unificó el nombre de la herramienta, se quitaron nombres de personas y se agruparon en una sola entrada por día las consultas pequeñas.

Se decidió no agregar más alternativas descartadas al bench: el enunciado pide medir al menos una alternativa descartada por sección, y las que quedan sin medir (la lista ordenada en 4.1 y FIFO en 4.4) están declaradas como tales en sus límites conocidos, con la razón de cada descarte.

