# Feature Specification: Verificación de Resolubilidad

**Feature Branch**: `003-resolubilidad`

**Created**: 2026-11-10

**Status**: Draft

**Input**: User description: "Capacidad: verificación de resolubilidad de una cripta antes de jugar. Supuestos: el jugador atraviesa cualquier salida abierta y cualquier cerrada cuya llave ya obtuvo; las llaves no se consumen; todo enemigo puede derrotarse; una llave que suelta un enemigo se considera obtenible en la sala donde ese enemigo inicia (incluye enemigos errantes); trampas y cierres automáticos no bloquean. Resoluble: partiendo de la sala inicial, el jugador puede obtener la llave de salida y llegar a la sala de salida a través de una puerta que la requiere. Resultado si es resoluble: un orden de obtención de llaves donde cada llave aparece después de todas las necesarias para alcanzarla; determinista (dos ejecuciones, mismo orden). Resultado si no lo es: llaves que no pueden obtenerse; puertas de la frontera bloqueada (cerradas, adyacentes a la región alcanzable) con la llave que exige cada una; dónde está cada una de esas llaves; y, si una llave está tras puertas que solo ella abre (directamente o por cadena), el ciclo concreto de dependencia. Sin --forzar, una cripta no resoluble no inicia y se muestra el reporte. --verificar <cripta> ejecuta solo la verificación, sin vista. El reporte se muestra al iniciar una partida. Usa los datos del esqueleto y la ubicación de llaves del servicio (nueva consulta que cuenta dentro del presupuesto de solicitudes y puede persistirse con la versión de la cripta). Rendimiento: < 200 ms en la cripta publicada más grande; costo total aproximadamente lineal en salas, salidas y llaves; el reporte sale del mismo recorrido (sin recorridos adicionales por llave). Escenarios del Apéndice B: llave de salida tras la única puerta que ella misma abre: no resoluble; el reporte señala el ciclo; llave en el campo suelta de un enemigo errante: se ubica en la sala inicial del enemigo; varios órdenes válidos: dos ejecuciones producen el mismo orden; cripta no resoluble sin --forzar: la partida no inicia y se muestra el reporte. Prefijo: FR-RES-NNN. Sin estructuras, clases ni módulos."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verificación previa al iniciar partida y control de acceso (Priority: P1)

Como jugador que inicia una partida en una cripta, deseo que el sistema verifique de antemano si la cripta tiene solución antes de permitirme jugar, para evitar invertir tiempo en un laberinto imposible de completar a menos que decida forzar el inicio explícitamente.

**Why this priority**: Es la funcionalidad central de cara al usuario que previene frustración al garantizar que toda partida iniciada sea completable bajo las reglas del juego, actuando como compuerta de seguridad al arrancar.

**Independent Test**: Puede probarse de manera aislada intentando iniciar una partida regular sobre una cripta no resoluble sin parámetros adicionales, comprobando que el juego no arranca y emite el reporte diagnóstico.

**Acceptance Scenarios**:

1. **Given** una cripta configurada como no resoluble, **When** el usuario ejecuta el inicio de partida regular sin el parámetro `--forzar`, **Then** la partida no inicia, el entorno de juego no se ejecuta y se presenta en pantalla el reporte detallado de no resolubilidad.
2. **Given** una cripta configurada como no resoluble, **When** el usuario ejecuta el inicio de partida incluyendo el parámetro `--forzar`, **Then** el sistema presenta el reporte de advertencia de no resolubilidad y procede a iniciar la partida normalmente.
3. **Given** una cripta resoluble, **When** el usuario ejecuta el inicio de partida regular, **Then** el sistema presenta el reporte de resolubilidad confirmando que es posible ganar y arranca la partida normalmente.

---

### User Story 2 - Verificación diagnóstica independiente vía CLI (Priority: P1)

Como evaluador o administrador del sistema, deseo ejecutar la verificación de resolubilidad de una cripta mediante el comando `--verificar <cripta>` sin que se instancie la interfaz gráfica ni la simulación interactiva, para obtener un diagnóstico rápido y automatizable por consola.

**Why this priority**: Permite la auditoría automatizada, pruebas por lotes y validaciones en canalizaciones continuas o defensas de curso, cumpliendo con la separación arquitectónica sin interfaz.

**Independent Test**: Puede probarse ejecutando `cripta --verificar <id_cripta>` desde la consola y constatando que se imprime el reporte diagnóstico y el proceso termina sin abrir vistas interactivas ni requerir interacción humana.

**Acceptance Scenarios**:

1. **Given** el identificador de una cripta resoluble, **When** se ejecuta el comando `--verificar <id_cripta>`, **Then** el sistema emite el reporte indicando que es resoluble junto con la secuencia determinista de llaves, sin iniciar ninguna vista interactiva.
2. **Given** el identificador de una cripta no resoluble, **When** se ejecuta el comando `--verificar <id_cripta>`, **Then** el sistema emite el reporte detallando las llaves inalcanzables, puertas bloqueadas y ciclos detectados, retornando el control a la terminal sin iniciar la vista interactiva.

---

### User Story 3 - Detección y diagnóstico de bloqueos y ciclos de dependencia (Priority: P2)

Como jugador o analista de laberintos, cuando una cripta no es resoluble deseo ver un reporte exhaustivo que señale exactamente qué llaves no pueden obtenerse, qué puertas forman la frontera bloqueada y, si existe un ciclo donde una llave está encerrada por puertas que dependen de ella misma, se detalle el ciclo concreto.

**Why this priority**: Proporciona el valor analítico y explicativo esencial de la capacidad, transformando un rechazo opaco en una justificación transparente del diseño del laberinto.

**Independent Test**: Puede probarse aislando un laberinto donde la llave de salida se ubica tras la única puerta que dicha llave abre, verificando que el reporte emitido resalta de manera explícita la dependencia circular.

**Acceptance Scenarios**:

1. **Given** una cripta donde la llave de salida está situada tras la única puerta cerrada que ella misma abre (caso Apéndice B), **When** se evalúa su resolubilidad, **Then** el resultado es no resoluble y el reporte señala explícitamente el ciclo concreto de dependencia circular.
2. **Given** una cripta no resoluble con varias puertas cerradas adyacentes a las salas alcanzables, **When** se evalúa su resolubilidad, **Then** el reporte enumera cada una de las puertas de la frontera bloqueada indicando la llave requerida por cada una y la ubicación donde reside dicha llave (sala o enemigo).

---

### User Story 4 - Determinismo en la secuencia de obtención de llaves (Priority: P2)

Como usuario o auditor del motor del juego, cuando una cripta es resoluble y admite múltiples secuencias u órdenes válidos para recolectar las llaves, deseo que el orden reportado sea 100% determinista e idéntico entre ejecuciones sucesivas.

**Why this priority**: Asegura la reproducibilidad de bitácoras, pruebas de regresión y cumplimiento estricto del principio de determinismo exigido por el proyecto.

**Independent Test**: Puede probarse ejecutando la verificación dos o más veces consecutivas sobre una misma cripta con múltiples ramas de recolección de llaves y comparando las secuencias de llaves generadas para verificar que sean exactamente idénticas.

**Acceptance Scenarios**:

1. **Given** una cripta resoluble que admite múltiples órdenes válidos de obtención de llaves (caso Apéndice B), **When** se ejecuta la verificación de resolubilidad en dos ocasiones independientes bajo la misma configuración, **Then** ambas ejecuciones producen exactamente la misma secuencia ordenada de llaves.

---

### User Story 5 - Ubicación y recolección de llaves portadas por enemigos (Priority: P3)

Como jugador, deseo que el análisis de resolubilidad considere que las llaves que sueltan los enemigos (estáticos o errantes) se pueden obtener en la sala donde dicho enemigo inicia su recorrido, asumiendo que todo enemigo puede ser vencido.

**Why this priority**: Establece el contrato de disponibilidad de llaves móviles o custodiadas, evitando falsos negativos en criptas donde las llaves no están en el suelo sino en inventario de enemigos.

**Independent Test**: Puede probarse sobre una cripta donde una llave indispensable para progresar es portada por un enemigo errante, verificando que la llave se asume recolectable al alcanzar la sala inicial de ese enemigo.

**Acceptance Scenarios**:

1. **Given** una cripta donde una llave requerida figura en el campo de objetos que suelta un enemigo de comportamiento errante (caso Apéndice B), **When** se evalúa la resolubilidad, **Then** el sistema asigna la ubicación de dicha llave a la sala donde ese enemigo inicia su recorrido y la considera obtenida tan pronto el jugador alcanza dicha sala inicial.
2. **Given** un enemigo portador de llave ubicado en una sala inalcanzable desde la región accesible, **When** se evalúa la resolubilidad, **Then** la llave portada por dicho enemigo se clasifica como no obtenible y se reporta como causa de bloqueo si alguna puerta de la frontera la requiere.

---

### Edge Cases

- **Laberinto desconectado sin puertas**: La sala inicial y la sala de salida se encuentran en componentes no conectados sin que existan puertas cerradas intermedias. El sistema debe clasificar la cripta como no resoluble y reportar que no existe conexión hacia la salida.
- **Sala inicial sin salidas transitables**: La sala de inicio no posee salidas abiertas o sus únicas salidas están cerradas con llaves no presentes en la sala inicial. El sistema reporta no resolubilidad con frontera bloqueada en las salidas de la sala de origen.
- **Llave de salida inmediatamente accesible**: La llave de salida y la puerta final están al alcance directo desde la sala de inicio sin requerir llaves intermedias. El sistema reporta resoluble de forma inmediata con una secuencia que contiene la llave de salida.
- **Cadena de dependencias circulares múltiples**: Existen dos o más ciclos cerrados independientes donde la llave A está tras la puerta B y la llave B tras la puerta A. El reporte debe identificar los ciclos de dependencia involucrados.
- **Trampas y puertas de cierre automático en la ruta**: La ruta hacia una llave contiene salas con trampas o mecanismos que cierran puertas automáticamente tras pasar. Por los supuestos establecidos, estos factores no deben bloquear el análisis de resolubilidad.
- **Presupuesto de solicitudes de red agotado o limitado**: La consulta de ubicación de llaves debe respetar el presupuesto disponible de la cripta y aprovechar el almacenamiento local si ya fue descargada para la misma versión.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-RES-001**: El sistema DEBE evaluar si una cripta es resoluble partiendo de su sala inicial, verificando si es posible obtener la llave de salida y alcanzar la sala de salida atravesando una puerta que la requiera.
- **FR-RES-002**: El análisis de resolubilidad DEBE asumir que el jugador puede franquear cualquier salida que se encuentre abierta, así como cualquier salida cerrada cuya llave ya haya sido recolectada durante la exploración.
- **FR-RES-003**: El análisis de resolubilidad DEBE asumir que las llaves obtenidas no se consumen al abrir una puerta y pueden reutilizarse indefinidamente para abrir cualquier otra puerta que requiera esa misma llave.
- **FR-RES-004**: El análisis de resolubilidad DEBE asumir que todo enemigo presente en la cripta puede ser derrotado por el jugador al alcanzar su posición.
- **FR-RES-005**: El análisis de resolubilidad DEBE considerar que una llave portada o soltada por un enemigo es obtenible en la sala inicial donde dicho enemigo comienza la partida, aplicando esta regla tanto a enemigos estáticos como a enemigos errantes o cazadores.
- **FR-RES-006**: El análisis de resolubilidad DEBE asumir que las trampas, peligros ambientales y mecanismos automáticos de cierre de puertas no bloquean ni impiden el paso del jugador.
- **FR-RES-007**: Cuando una cripta resulte ser resoluble, el sistema DEBE generar un reporte que incluya una secuencia válida de obtención de llaves en la que cada llave aparezca después de todas las llaves necesarias para alcanzar la sala donde se encuentra.
- **FR-RES-008**: La generación de la secuencia de llaves de una cripta resoluble DEBE ser determinista, produciendo de manera estricta el mismo orden en cualquier ejecución ante los mismos datos de la cripta.
- **FR-RES-009**: Cuando una cripta no sea resoluble, el sistema DEBE identificar y listar en el reporte el conjunto de todas las llaves que no pueden ser obtenidas desde la región alcanzable.
- **FR-RES-010**: Cuando una cripta no sea resoluble, el sistema DEBE identificar y detallar en el reporte todas las puertas pertenecientes a la frontera bloqueada (puertas cerradas adyacentes a la región actualmente alcanzable) indicando la llave exigida por cada una de ellas.
- **FR-RES-011**: Cuando una cripta no sea resoluble, el sistema DEBE indicar en el reporte la ubicación conocida (identificador de sala y enemigo asociado si aplica) de cada una de las llaves requeridas por la frontera bloqueada o que no puedan ser obtenidas.
- **FR-RES-012**: Si una llave no obtenible se encuentra tras puertas que solo ella misma permite abrir (ya sea de manera directa o mediante una cadena indirecta de dependencias), el sistema DEBE aislar e indicar en el reporte el ciclo concreto de dependencias circulares.
- **FR-RES-013**: Al iniciar una partida regular, el sistema DEBE ejecutar automáticamente la verificación de resolubilidad y mostrar en pantalla el reporte resultante al usuario.
- **FR-RES-014**: Si una cripta es evaluada como no resoluble al momento de iniciar una partida regular y no se suministra el argumento `--forzar`, el sistema DEBE cancelar el inicio del juego, impedir la entrada al bucle de simulación y mostrar el reporte de no resolubilidad.
- **FR-RES-015**: Si se especifica el argumento de línea de comandos `--forzar` al iniciar una partida sobre una cripta no resoluble, el sistema DEBE emitir el reporte de advertencia y permitir que la partida comience normalmente.
- **FR-RES-016**: La opción de línea de comandos `--verificar <cripta>` DEBE ejecutar exclusivamente la verificación de resolubilidad sobre la cripta indicada, emitiendo el reporte por consola sin instanciar componentes de la vista ni iniciar partidas o simulaciones.
- **FR-RES-017**: La verificación de resolubilidad DEBE obtener los datos requeridos consultando el esqueleto de la cripta y el servicio de ubicación de llaves de la cripta (`GET /criptas/{id}/llaves`), contabilizando dicha consulta dentro del presupuesto de solicitudes de la cripta y permitiendo su persistencia asociada a la versión de la cripta.
- **FR-RES-018**: El análisis de resolubilidad, la detección de la frontera bloqueada y la identificación de ciclos de dependencia DEBEN calcularse a partir de un único recorrido de exploración integrada de la cripta, sin realizar exploraciones completas adicionales independientes por cada llave.

---

### Key Entities *(include if feature involves data)*

- **Cripta**: Estructura del laberinto compuesta por salas interconectadas mediante salidas transitables, con una sala inicial designada para el ingreso del jugador, una sala de salida de escape y una llave de salida obligatoria.
- **Salida / Puerta**: Conexión bidireccional o unidireccional entre dos salas adyacentes. Posee un estado (abierta o cerrada). Cuando está cerrada, especifica el identificador de la llave obligatoria requerida para desbloquearla.
- **Llave**: Objeto identificado por un código único necesario para abrir una o más puertas cerradas coincidentes. Puede hallarse depositada en el suelo de una sala específica o ser portada por un enemigo cuya sala inicial está definida.
- **Región Alcanzable**: Conjunto de salas de la cripta a las que el jugador puede acceder desde la sala inicial atravesando únicamente salidas abiertas o salidas cerradas cuyas llaves ya han sido obtenidas previamente en la exploración.
- **Frontera Bloqueada**: Conjunto de salidas cerradas inmediatamente contiguas a la región alcanzable cuyas llaves asociadas aún no han sido obtenidas por el jugador, marcando el límite del avance actual.
- **Ciclo de Dependencia**: Situación de bloqueo mutuo donde el acceso a una llave requiere franquear una o varias puertas cerradas cuyas llaves, a su vez, solo pueden alcanzarse cruzando una puerta que depende de la primera.
- **Reporte de Resolubilidad**: Documento diagnóstico estructurado generado por la verificación, que dictamina si la cripta es o no resoluble. Si es resoluble, incluye la secuencia determinista de recolección de llaves. Si no lo es, detalla las llaves inalcanzables, las puertas de la frontera bloqueada con sus llaves exigidas, la ubicación de cada llave y los ciclos de dependencia encontrados.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: La verificación de resolubilidad completa sobre la cripta publicada de mayor tamaño disponible debe ejecutarse en un tiempo cronológico menor a 200 ms en el entorno local de referencia.
- **SC-002**: El costo total de tiempo de la verificación debe ser aproximadamente lineal en relación con la suma del número de salas, salidas transitables y llaves presentes en la cripta analizada.
- **SC-003**: En el 100% de las pruebas ejecutadas sobre criptas resolubles con múltiples caminos válidos de obtención de llaves, dos ejecuciones consecutivas bajo las mismas entradas deben producir exactamente la misma secuencia ordenada de llaves.
- **SC-004**: En el 100% de los casos en que se evalúe una cripta no resoluble, el sistema emite el reporte detallando las llaves no obtenibles y las puertas de la frontera bloqueada sin interrupciones abruptas ni excepciones no controladas.
- **SC-005**: La invocación con el argumento `--verificar <cripta>` debe completar su ejecución emitiendo el reporte por salida estándar sin instanciar elementos de la vista de juego ni esperar entradas interactivas del usuario.
- **SC-006**: La consulta remota al endpoint de llaves (`GET /criptas/{id}/llaves`) debe consumir como máximo una unidad del presupuesto de solicitudes de la cripta cuando los datos no estén previamente almacenados en caché persistente.

---

## Assumptions

- Se asume que los datos del esqueleto de la cripta y el catálogo de llaves suministrados por el servicio web son íntegros y corresponden a la versión activa de la cripta analizada.
- Se asume que las llaves nunca se consumen ni se pierden al abrir una puerta cerrada, permaneciendo disponibles durante el resto de la sesión de juego.
- Se asume que para efectos de resolubilidad estática, todo enemigo puede ser vencido por el jugador, por lo que su presencia no constituye una barrera infranqueable si su sala de inicio es alcanzable.
- Se asume que la posición de recolección de una llave portada por un enemigo corresponde exactamente a la sala donde ese enemigo inicia la partida, con independencia de su patrón de movimiento posterior durante la simulación.
- Se asume que los mecanismos dinámicos de juego (activación y rearme de trampas, cierre periódico o automático de puertas) no alteran las conexiones fundamentales para la alcanzabilidad de la cripta.
- Se asume que la bandera `--forzar` actúa como una decisión de política de ejecución a nivel de interfaz de usuario y no altera el dictamen técnico emitido por el algoritmo de resolubilidad.
