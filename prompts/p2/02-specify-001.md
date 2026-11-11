Capacidad: terreno y cazador de Cripta Parte II.

Terreno: cada salida puede declarar un costo entero >= 1; si no lo declara vale 100; es igual
en ambos sentidos. Moverse a través de una salida cuesta el costo de esa salida; el intervalo
sigue siendo max(1, costo_salida * 100 // velocidad). Aplica a todos los actores. Atacar, esperar
y demás acciones no cambian. Errantes y rastreadores conservan su comportamiento.

Cazador: cuarto comportamiento de enemigo; su ficha incluye "rango" (entero en unidades de costo). En su turno: (1) si comparte sala con el jugador, ataca; (2) si no, considera el costo mínimo d de llegar a la sala actual del jugador sumando costos de salidas recorridas y usando solo salidas abiertas en ese instante; (3) si no hay ruta o d > rango, espera con costo 100; (4) si hay, se mueve un paso por una ruta de costo d, y el costo de esa acción es el de la salida que cruza.
Desempate: entre las vecinas v con costo(u,v)+dist(v,jugador)=d va a la de menor id. El cazador
conoce el esqueleto completo y el estado actual de todas las puertas; no le afecta la niebla; no
abre puertas; su decisión nunca depende de si el contenido de una sala se descargó.
Equivalencia observable: la decisión de cada turno debe ser idéntica a calcular desde cero en ese
instante, aunque cambien puertas, el jugador se mueva o mueran actores.

Servicio: el esqueleto trae "costo" por salida; el catálogo trae "comportamiento: cazador" y
"rango"; además, GET /criptas/{id}/llaves entrega la ubicación de las llaves (válida mientras
coincida la versión de la cripta). Los datos persistidos de la Parte I deben invalidarse por
versión, no borrando archivos.

Rendimiento: ciclo de eventos < 20 ms con decenas de cazadores activos que persiguen al mismo
objetivo (cripta de referencia, sin red ni renderizado).

Incluye como escenarios de aceptación todos estos casos del Apéndice B:
- cazador sin ruta abierta: espera con costo 100
- ruta más barata mayor que el rango: espera con costo 100
- ruta de menos salas pero mayor costo vs más salas y menor costo: sigue la de menor costo
- dos vecinas con rutas de costo mínimo: va a la de menor id
- una puerta de la ruta se cierra entre dos turnos: decide como desde cero
- actor de velocidad alta cruza salida de costo 1: intervalo >= 1
- cambia la velocidad de un actor que cruza una salida costosa: tiempo restante escalado (P1 §2.3)

Prefijo de requisitos: FR-TER-NNN. No menciones estructuras de datos, clases ni módulos.
