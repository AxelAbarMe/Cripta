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