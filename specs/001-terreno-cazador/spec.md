# Feature Specification: Terreno y Cazador

**Feature Branch**: `001-terreno-cazador`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "Capacidad: terreno y cazador de Cripta Parte II.

Terreno: cada salida puede declarar un costo entero >= 1; si no lo declara vale 100; es igual en ambos sentidos. Moverse a través de una salida cuesta el costo de esa salida; el intervalo sigue siendo max(1, costo_salida * 100 // velocidad). Aplica a todos los actores. Atacar, esperar y demás acciones no cambian. Errantes y rastreadores conservan su comportamiento.

Cazador: cuarto comportamiento de enemigo; su ficha incluye "rango" (entero en unidades de costo). En su turno: (1) si comparte sala con el jugador, ataca; (2) si no, considera el costo mínimo d de llegar a la sala actual del jugador sumando costos de salidas recorridas y usando solo salidas abiertas en ese instante; (3) si no hay ruta o d > rango, espera con costo 100; (4) si hay, se mueve un paso por una ruta de costo d, y el costo de esa acción es el de la salida que cruza.
Desempate: entre las vecinas v con costo(u,v)+dist(v,jugador)=d va a la de menor id. El cazador conoce el esqueleto completo y el estado actual de todas las puertas; no le afecta la niebla; no abre puertas; su decisión nunca depende de si el contenido de una sala se descargó.
Equivalencia observable: la decisión de cada turno debe ser idéntica a calcular desde cero en ese instante, aunque cambien puertas, el jugador se mueva o mueran actores.

Servicio: el esqueleto trae "costo" por salida; el catálogo trae "comportamiento: cazador" y "rango"; además, GET /criptas/{id}/llaves entrega la ubicación de las llaves (válida mientras coincida la versión de la cripta). Los datos persistidos de la Parte I deben invalidarse por versión, no borrando archivos.

Rendimiento: ciclo de eventos < 20 ms con decenas de cazadores activos que persiguen al mismo objetivo (cripta de referencia, sin red ni renderizado).

Incluye como escenarios de aceptación todos estos casos del Apéndice B:
- cazador sin ruta abierta: espera con costo 100
- ruta más barata mayor que el rango: espera con costo 100
- ruta de menos salas pero mayor costo vs más salas y menor costo: sigue la de menor costo
- dos vecinas con rutas de costo mínimo: va a la de menor id
- una puerta de la ruta se cierra entre dos turnos: decide como desde cero
- actor de velocidad alta cruza salida de costo 1: intervalo >= 1
- cambia la velocidad de un actor que cruza una salida costosa: tiempo restante escalado (P1 §2.3)

Prefijo de requisitos: FR-TER-NNN. No menciones estructuras de datos, clases ni módulos."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Movimiento y costos variables del terreno para actores (Priority: P1)

Como jugador o entidad del juego (actor), al desplazarme entre salas conectadas a través de una salida abierta, el tiempo virtual que consume mi movimiento debe reflejar la dificultad del terreno determinada por el costo específico de esa salida (o el costo base estándar de 100 si no se especifica), aplicando el costo de forma idéntica en ambos sentidos de la conexión y garantizando que el intervalo de tiempo virtual nunca sea inferior a 1 unidad temporal.

**Why this priority**: El costo de terreno es el fundamento de la dinámica espacial de la Parte II: afecta a jugadores y a todos los tipos de enemigos en su consumo temporal y en la agenda del reloj de eventos.

**Independent Test**: Puede verificarse de manera aislada cargando un laberinto con salidas de costo variado y comprobando que el jugador y enemigos convencionales consumen exactamente los intervalos temporales prescritos según su velocidad y el costo de la salida atravesada, tanto en ida como en vuelta.

**Acceptance Scenarios**:

1. **Given** un actor con velocidad 100 en una sala, y una salida abierta hacia una sala vecina con costo declarado de 250, **When** el actor se desplaza a través de dicha salida, **Then** la acción consume un costo de 250 unidades, el intervalo de tiempo virtual programado es de 250 unidades, y al regresar por la misma salida abierta en sentido opuesto el costo es también de 250 unidades.
2. **Given** un actor con velocidad 100 en una sala, y una salida abierta hacia una sala vecina que no declara costo, **When** el actor se desplaza a través de dicha salida, **Then** la acción asume un costo por defecto de 100 unidades y programa un intervalo temporal de 100 unidades.
3. **Given** un actor con velocidad elevada de 200 en una sala, y una salida abierta hacia una vecina con costo 1, **When** el actor se desplaza a través de dicha salida, **Then** el cálculo del intervalo produce un tiempo virtual de al menos 1 unidad temporal, evitando valores nulos o negativos.
4. **Given** un actor con velocidad inicial 100 que inicia el cruce de una salida con costo 400 en el instante t = 0 (con tiempo de llegada previsto en t = 400), **When** en el instante t = 100 su velocidad cambia a 200 por efecto de una poción de velocidad, **Then** el tiempo restante se escala proporcionalmente a 150 unidades adicionales, reprogramando su llegada en el instante virtual t = 250.
5. **Given** un actor en una sala contigua a salidas de costos variables, **When** el actor ejecuta una acción de esperar o atacar, **Then** el costo de dicha acción permanece inalterado en su valor base de 100 unidades, sin verse modificado por los costos de las salidas circundantes.
6. **Given** un enemigo errante o rastreador activo en una sala con salidas abiertas de costos heterogéneos, **When** llega su turno de acción, **Then** el errante selecciona al azar una salida abierta y el rastreador selecciona la salida hacia la sala accesible con rastro más fresco menor a 400 unidades, utilizando en ambos casos el costo de la salida seleccionada para determinar el costo y la duración del movimiento.

---

### User Story 2 - Persecución táctica del enemigo Cazador por costo mínimo (Priority: P1)

Como enemigo con comportamiento de Cazador, en cada turno de mi ciclo de vida debo evaluar el estado actual del laberinto para perseguir al jugador por la ruta de menor costo total acumulado a través de salidas actualmente abiertas, o atacarlo directamente si ya me encuentro en la misma sala, asegurando que mis movimientos siempre elijan la opción más económica en costo total aunque implique atravesar un mayor número de salas intermedias.

**Why this priority**: El cazador es la principal amenaza inteligente introducida en la Parte II; su persecución óptima y letal es el núcleo del desafío del jugador y de la simulación.

**Independent Test**: Puede verificarse en un entorno controlado situando a un cazador y al jugador en salas separadas con múltiples caminos alternativos de diferente número de salas y costos, confirmando que el cazador avanza por la ruta de menor costo acumulado y ataca al compartir sala.

**Acceptance Scenarios**:

1. **Given** un cazador y el jugador que se encuentran en la misma sala, **When** llega el turno de acción del cazador, **Then** el cazador ataca al jugador con costo base de 100 unidades y no realiza desplazamiento de sala.
2. **Given** un cazador en la sala A y el jugador en la sala B, existiendo un camino directo de 1 salida abierta de costo 300, y un camino alternativo de 3 salidas abiertas de costo 50 cada una (costo total acumulado de 150), **When** llega el turno de acción del cazador (con rango mayor o igual a 150), **Then** el cazador opta por la ruta de menor costo acumulado (150 frente a 300) y se mueve un paso hacia la primera sala intermedia de dicho camino, teniendo dicha acción un costo de 50 unidades.
3. **Given** un cazador que determina una ruta óptima de costo mínimo d hacia el jugador cuya primera salida abierta tiene costo C, **When** el cazador ejecuta su turno de desplazamiento, **Then** se mueve a la sala vecina inmediata de esa ruta y el costo de su acción corresponde exactamente a C unidades, programando su siguiente turno según dicho costo y su velocidad.

---

### User Story 3 - Decisiones del Cazador ante desempates, bloqueos, límites de rango y puertas dinámicas (Priority: P2)

Como enemigo Cazador, debo resolver situaciones de ambigüedad y contingencias de forma estrictamente determinista: si dos salas vecinas conducen a rutas de costo mínimo idéntico, elegiré la vecina de menor identificador; si no hay ruta abierta o la ruta óptima excede mi rango de percepción, esperaré; y si las puertas del laberinto cambian entre turnos, mi decisión siempre equivaldrá a calcular desde cero con el estado presente del laberinto.

**Why this priority**: Garantiza el determinismo matemático, la auditabilidad de las partidas y la robustez de la toma de decisiones ante un entorno dinámico donde las puertas se abren o cierran y los actores se desplazan.

**Independent Test**: Puede comprobarse mediante escenarios con simetría de costos para evaluar desempates por identificador, puertas con cierres automáticos que alteran la conectividad entre turnos, y distancias superiores al rango asignado.

**Acceptance Scenarios**:

1. **Given** un cazador en una sala conectada a dos salas vecinas v1 (identificador 4) y v2 (identificador 8), donde ambas ofrecen rutas de salidas abiertas hacia el jugador con el mismo costo mínimo total d, **When** llega el turno de acción del cazador, **Then** el cazador desempata a favor de la sala con menor identificador y se desplaza hacia la sala con identificador 4.
2. **Given** un cazador y el jugador separados por puertas cerradas de modo que no existe ningún camino compuesto exclusivamente por salidas abiertas entre sus salas, **When** llega el turno de acción del cazador, **Then** el cazador decide esperar, consumiendo un costo de acción de 100 unidades.
3. **Given** un cazador con atributo de rango de 150 unidades, y una ruta abierta de costo mínimo hacia el jugador cuyo costo total acumulado es de 200 unidades, **When** llega el turno de acción del cazador, **Then** al superar el costo mínimo (200) su rango (150), el cazador decide esperar, consumiendo un costo de acción de 100 unidades.
4. **Given** un cazador que en su turno previo avanzó por una ruta de costo mínimo, y durante el intervalo una puerta de dicha ruta se cierra automáticamente, **When** llega el siguiente turno del cazador, **Then** la decisión tomada es idéntica a evaluar desde cero el estado actual del laberinto: si existe otra ruta abierta dentro de su rango la toma, y si no existe o excede su rango, espera con costo 100.
5. **Given** un cazador persiguiendo al jugador a través de salas que el jugador no ha explorado o cuyo contenido detallado no ha sido descargado por el sistema, **When** el cazador toma su decisión de movimiento, **Then** el cazador utiliza el conocimiento completo de las salidas y puertas del laberinto sin ser afectado por la niebla de guerra ni por la ausencia de descarga de entidades de salas remotas, y no abre puertas cerradas bajo ninguna circunstancia.

---

### User Story 4 - Contrato de datos de terreno, cazadores y ubicación de llaves con control de versión (Priority: P2)

Como sistema de juego, al consultar los datos del laberinto desde el servicio externo (o réplica fuera de línea), debo recibir los costos específicos en las salidas del esqueleto, reconocer fichas de enemigos cazadores con su atributo de rango, consultar la ubicación de las llaves de la cripta, e invalidar de forma automática cualquier dato previamente persistido que pertenezca a versiones incompatibles o de la Parte I sin requerir el borrado manual de archivos.

**Why this priority**: Asegura la compatibilidad con el nuevo contrato de datos de la Parte II y previene corrupciones o lecturas inconsistentes de partidas o cachés locales.

**Independent Test**: Se verifica solicitando la información de un laberinto y comprobando que los costos de salida y las fichas de cazador se registran correctamente, que la consulta de llaves refleja las salas o portadores correctos, y que archivos generados con la versión de la Parte I son detectados y declarados incompatibles.

**Acceptance Scenarios**:

1. **Given** una respuesta de páginas de esqueleto del laberinto proveniente del servicio con salidas que declaran costo entero y salidas que omiten dicho campo, **When** el sistema incorpora las salas y salidas, **Then** las salidas con costo mantienen su valor entero positivo y las que omiten el campo reciben el costo por defecto de 100.
2. **Given** una respuesta del catálogo del servicio que incluye una ficha de enemigo con comportamiento "cazador" y atributo "rango", **When** el sistema incorpora la ficha, **Then** registra el comportamiento como cazador y almacena su rango en unidades de costo para ser utilizado por sus instancias.
3. **Given** una cripta identificada con una versión específica, **When** se consulta el servicio para obtener la ubicación de sus llaves, **Then** se obtiene la lista de llaves indicando para cada una su sala correspondiente y si la porta un enemigo, siendo dicha información válida exclusivamente mientras la versión de la cripta coincida.
4. **Given** un archivo de datos persistidos generado en la primera parte o correspondiente a una versión de cripta o catálogo diferente, **When** el sistema intenta cargar o validar dichos datos persistidos, **Then** el sistema detecta formalmente la incompatibilidad por versión y los invalida o rechaza sin requerir el borrado manual de archivos del disco.

---

### Edge Cases

- ¿Qué ocurre si un cazador tiene dos salidas abiertas hacia salas vecinas con diferente identificador pero que forman parte de la misma ruta o rutas de igual costo mínimo total hacia el jugador? Se desempata estrictamente eligiendo la vecina con menor identificador numérico de sala.
- ¿Qué ocurre si el jugador se desplaza a la misma sala donde se encuentra el cazador mientras éste esperaba o estaba en tránsito? Al llegar el siguiente turno del cazador, éste observa que comparte sala con el jugador y ataca inmediatamente en lugar de moverse.
- ¿Qué ocurre si un enemigo cazador muere mientras esperaba o se movía? Deja de ejecutar eventos y cualquier acción futura programada queda sin efecto en el reloj virtual.
- ¿Qué ocurre si todos los caminos hacia el jugador están bloqueados por puertas cerradas? El cazador no abre puertas bajo ninguna circunstancia y procede a esperar consumiendo un costo de 100 unidades.
- ¿Qué ocurre si el rango del cazador es exactamente igual al costo mínimo d de la ruta abierta (d == rango)? El cazador se mueve normalmente por la ruta óptima, pues la condición de espera es estrictamente d > rango.
- ¿Qué ocurre si el cazador y el jugador están en la misma sala pero la distancia teórica a través del mapa fuera mayor que el rango? Al compartir sala, la condición de ataque prioritario prevalece y el cazador ataca sin evaluar distancias ni rango.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-TER-001**: Toda salida entre dos salas contiguas del laberinto puede declarar un costo entero mayor o igual a 1. Si dicho costo no se declara o es nulo en los datos recibidos, su valor por defecto debe ser 100.
- **FR-TER-002**: El costo de una salida debe ser estrictamente simétrico, teniendo exactamente el mismo valor al ser atravesada en cualquiera de los dos sentidos de la conexión.
- **FR-TER-003**: Toda acción de desplazamiento de un actor (sea el jugador o cualquier tipo de enemigo) a través de una salida abierta debe tener un costo de acción igual al costo declarado de dicha salida.
- **FR-TER-004**: El intervalo de tiempo virtual consumido por una acción de movimiento a través de una salida debe calcularse exactamente mediante la expresión matemática `max(1, costo_salida * 100 // velocidad)`, garantizando que el intervalo resultante sea siempre mayor o igual a 1 unidad de tiempo virtual.
- **FR-TER-005**: Si la velocidad de un actor cambia mientras se encuentra en tránsito cruzando una salida, el tiempo restante para completar el cruce debe escalarse en el instante virtual t del cambio según la fórmula `restante_nuevo = max(1, (t_siguiente - t) * velocidad_anterior // velocidad_nueva)`, actualizando el tiempo de finalización del evento a `t + restante_nuevo`.
- **FR-TER-006**: Los costos de las acciones que no constituyen desplazamiento espacial (tales como atacar, esperar, usar objetos, equipar, recoger, soltar y abrir puertas con llave) no deben verse afectados por los costos de las salidas del laberinto.
- **FR-TER-007**: Los enemigos con comportamientos errante y rastreador deben conservar su lógica de selección de destino (el errante selecciona al azar una salida abierta; el rastreador selecciona la salida hacia la sala accesible con rastro más reciente menor a 400 unidades, desempatando por menor identificador de sala), consumiendo para su desplazamiento el costo específico de la salida seleccionada.
- **FR-TER-008**: El sistema debe incorporar el comportamiento de enemigo "cazador" como cuarto comportamiento disponible en el catálogo de entidades, requiriendo que su ficha incluya un atributo de rango expresado como un número entero positivo en unidades de costo.
- **FR-TER-009**: En su turno de acción, si el cazador comparte sala con el jugador, debe atacar prioritariamente al jugador con el costo base estándar de ataque (100 unidades).
- **FR-TER-010**: En su turno de acción, si el cazador no comparte sala con el jugador, debe evaluar el costo mínimo d para alcanzar la sala actual del jugador sumando exclusivamente los costos de las salidas que se encuentren abiertas en ese instante.
- **FR-TER-011**: Si no existe ninguna ruta compuesta por salidas abiertas hacia la sala actual del jugador, o si el costo mínimo d es estrictamente mayor que el rango del cazador (d > rango), el cazador debe esperar consumiendo un costo de acción de 100 unidades.
- **FR-TER-012**: Si existe al menos una ruta de salidas abiertas hacia el jugador con costo mínimo d menor o igual a su rango (d <= rango), el cazador debe desplazarse un paso hacia una sala vecina perteneciente a dicha ruta de costo d, teniendo la acción de movimiento un costo igual al de la salida atravesada.
- **FR-TER-013**: Cuando existan dos o más salas vecinas v conectadas por salidas abiertas que permitan alcanzar al jugador con el mismo costo mínimo total d (cumpliendo `costo(u, v) + dist(v, jugador) == d`), el cazador debe desempatar obligatoriamente seleccionando la sala vecina con el menor identificador numérico.
- **FR-TER-014**: El cazador debe conocer el esqueleto completo del laberinto y el estado actual de todas sus puertas, no verse afectado por la niebla de guerra, no abrir puertas cerradas bajo ninguna circunstancia, y su toma de decisión no debe depender de si el contenido detallado de una sala ha sido descargado.
- **FR-TER-015**: La decisión de cada turno del cazador debe presentar equivalencia observable idéntica a calcular la ruta desde cero en ese instante, reflejando fielmente cualquier cambio en puertas, movimiento de actores o fallecimiento de entidades.
- **FR-TER-016**: El sistema debe interpretar el atributo de costo en las salidas del esqueleto del laberinto provistas por el servicio externo o modo fuera de línea, asignando 100 si no se encuentra presente.
- **FR-TER-017**: El sistema debe interpretar el comportamiento "cazador" y su atributo "rango" en las fichas del catálogo de entidades provistas por el servicio externo o modo fuera de línea.
- **FR-TER-018**: El sistema debe proveer una consulta para obtener la ubicación de cada llave de la cripta (indicando sala y si está en posesión de un enemigo), contabilizando dicha consulta en el presupuesto de solicitudes y manteniéndola válida únicamente mientras la versión de la cripta coincida.
- **FR-TER-019**: La persistencia de datos debe invalidar formalmente cualquier archivo o registro previo si no coincide la versión de la cripta o del catálogo, o si corresponde al formato de la primera parte, prohibiéndose requerir el borrado manual de archivos como mecanismo de control.
- **FR-TER-020**: El ciclo de eventos de la simulación entre dos decisiones consecutivas del jugador debe completarse en menos de 20 milisegundos en la cripta de referencia, aun en presencia de decenas de cazadores activos persiguiendo al mismo objetivo, medido en el entorno local sin red ni renderizado gráfico.

### Key Entities *(include if feature involves data)*

- **Salida / Conexión**: Vía de paso bidireccional entre dos salas contiguas del laberinto. Atributos conceptuales: sala de origen, sala de destino, estado de puerta (abierta o cerrada con llave), costo de paso (entero >= 1, por defecto 100).
- **Actor**: Entidad con presencia física en una sala y participación activa en la línea de tiempo virtual. Atributos conceptuales: identificador de instancia, sala actual, puntos de vida, ataque, defensa, velocidad, tiempo siguiente de acción programada.
- **Cazador**: Tipo específico de actor enemigo con comportamiento de persecución guiada por costo mínimo. Atributos adicionales: ficha de catálogo asociada, comportamiento cazador, rango de persecución (entero >= 1 en unidades de costo).
- **Ubicación de Llave**: Información provista por el servicio sobre la procedencia de una llave en la cripta. Atributos conceptuales: identificador de la llave, identificador de la sala donde se ubica, e identificador opcional del enemigo que la suelta al ser derrotado (o indicación de encontrarse en el suelo de la sala).
- **Versión de Cripta y Catálogo**: Identificadores de versión provistos por el servicio que gobiernan la validez de los datos del laberinto y el catálogo, empleados para invalidar de forma automática cualquier estado persistido obsoleto.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El ciclo de eventos de la simulación entre dos acciones consecutivas del jugador se ejecuta en menos de 20 milisegundos en la cripta de referencia con al menos 30 cazadores activos en persecución simultánea.
- **SC-002**: El 100% de las decisiones de movimiento y persecución del cazador coinciden exactamente con la ruta de costo mínimo teórico y la regla de desempate por menor identificador de sala.
- **SC-003**: El 100% de los escenarios de aceptación especificados a partir del Apéndice B para terreno y cazador son reproducibles y verificables mediante pruebas automatizadas.
- **SC-004**: Ninguna acción de desplazamiento a través de salidas con costo produce intervalos de tiempo virtual inferiores a 1 unidad temporal, considerando el espectro de velocidades de actores entre 1 y 500.
- **SC-005**: El 100% de los archivos o datos persistidos generados bajo versiones previas o formatos de la primera parte son detectados formalmente como incompatibles sin requerir intervención manual sobre el sistema de archivos.

## Assumptions

- Toda ficha de enemigo con comportamiento "cazador" provista por un catálogo válido incluye un valor de rango entero positivo. En caso de recibir un catálogo con rango nulo o ausente para un cazador, se asumirá por defecto un rango ilimitado (persigue a cualquier distancia mientras exista ruta de salidas abiertas).
- Los costos de salida suministrados por el servicio son números enteros mayores o iguales a 1. Si un valor no se declara o es nulo, asume el valor por defecto de 100.
- La consulta de ubicación de llaves consume exactamente una solicitud del presupuesto de solicitudes de la cripta y su resultado permanece vigente mientras no se altere la versión de la cripta.
- Los actores conservan sus atributos de combate, fórmulas de daño y reglas de turno de la primera parte; la incorporación de salidas con costo variable modifica exclusivamente la duración y el costo del desplazamiento entre salas.
