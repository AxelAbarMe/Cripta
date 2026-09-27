26/09/2026

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