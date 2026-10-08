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


# 08/10/2026

Se unieron las dos ramas de trabajo en main y se comprobó el proyecto completo: los imports funcionan, el bench corre sus 8 cargas y el ciclo de eventos cumple el límite de 20 ms. Con los datos reales de cripta-01 guardados en fixtures/ se probó el flujo completo (cliente offline, mapa, catálogo y precarga) y los enemigos, las puertas y las fichas se construyen correctamente: un enemigo sin vida declarada nace con su vida máxima, el comportamiento "guardián" llega con tilde y la llave y el cierre automático de una puerta vienen marcados en un solo lado de la salida.

Se agregó al mapa datos_de_puerta, que devuelve la llave y el cierre automático de una puerta mirando sus dos lados.

Se escribió comportamiento_enemigo.py con la decisión del turno de un enemigo (§2.8): si comparte sala con el jugador ataca; si no, el guardián espera, el errante elige al azar una salida abierta y el rastreador sigue el rastro fresco más reciente de las salas vecinas, con desempate por menor id. El módulo solo decide; ejecutar la acción lo hará el motor.

Se escribió accion.py con las 9 acciones del jugador definidas en el contrato de Partida, con su validación, su costo base y su conversión a dict para la bitácora de la partida.

Se escribió el primer trozo del motor (partida.py y resultado_partida.py): construcción de la partida con su generador de azar propio, inicio según §2.4, ciclo de eventos hasta el siguiente turno del jugador, turnos de los enemigos (atacar, moverse o esperar), derrota, la consulta vista() con todo lo que debe mostrar la interfaz y la acción esperar. Se probó con la cripta real de fixtures: con la misma semilla dos partidas producen exactamente los mismos mensajes y tiempos, y con otra semilla cambian.

Lo siguiente que hay que realizar:
* Motor Partida, trozo 2: mover y abrir (llave comparada con el id de la ficha y cierre automático), trampas y victoria.
* Motor Partida, trozo 3: atacar, recoger, usar, equipar, soltar y pergamino.
* Retroceso completo y puente entre el modelo y el guardado.
* Replay.