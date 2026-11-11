# Especificación de la funcionalidad: Verificación de Resolubilidad

**Rama de la funcionalidad**: `003-resolubilidad`

**Creado**: 2026-11-10

**Estado**: Borrador

**Entrada**: Descripción de usuario: "Capacidad: verificación de resolubilidad de una cripta antes de jugar. Supuestos: el jugador atraviesa cualquier salida abierta y cualquier cerrada cuya llave ya obtuvo; las llaves no se consumen; todo enemigo puede derrotarse; una llave que suelta un enemigo se considera obtenible en la sala donde ese enemigo inicia (incluye enemigos errantes); trampas y cierres automáticos no bloquean. Resoluble: partiendo de la sala inicial, el jugador puede obtener la llave de salida y llegar a la sala de salida a través de una puerta que la requiere. Resultado si es resoluble: un orden de obtención de llaves donde cada llave aparece después de todas las necesarias para alcanzarla; determinista (dos ejecuciones, mismo orden). Resultado si no lo es: llaves que no pueden obtenerse; puertas de la frontera bloqueada (cerradas, adyacentes a la región alcanzable) con la llave que exige cada una; dónde está cada una de esas llaves; y, si una llave está tras puertas que solo ella abre (directamente o por cadena), el ciclo concreto de dependencia. Sin --forzar, una cripta no resoluble no inicia y se muestra el reporte. --verificar <cripta> ejecuta solo la verificación, sin vista. El reporte se muestra al iniciar una partida. Usa los datos del esqueleto y la información de llaves bajo el contrato de datos de la capacidad 001. Rendimiento: < 200 ms en la cripta publicada más grande; costo total aproximadamente lineal en salas, salidas y llaves; el reporte sale del mismo recorrido (sin recorridos adicionales por llave). Escenarios del Apéndice B: llave de salida tras la única puerta que ella misma abre: no resoluble; el reporte señala el ciclo; llave en el campo suelta de un enemigo errante: se ubica en la sala inicial del enemigo; varios órdenes válidos: dos ejecuciones producen el mismo orden; cripta no resoluble sin --forzar: la partida no inicia y se muestra el reporte. Prefijo: FR-RES-NNN. Sin estructuras, clases ni módulos."

## Aclaraciones

### Sesión 2026-11-11

- P: ¿El orden de obtención de llaves en una cripta resoluble debe incluir todas las llaves obtenibles o solo las necesarias para llegar a llave_salida? → R: Todas las llaves obtenibles. El reporte debe incluir la secuencia causal de todas las llaves que el jugador puede llegar a obtener en la región alcanzable, no solo las indispensables para llegar a la salida.
- P: Cuando hay varios ciclos de dependencia, ¿el reporte muestra uno o todos? → R: Un ciclo concreto representativo por cada grupo de llaves que se bloquean entre sí (no todos los ciclos posibles de la cripta). Los ciclos se eligen de forma determinista y se ordenan en el reporte por el menor identificador de llave de cada uno, manteniendo un costo aproximadamente lineal.
- P: Datos incoherentes: una puerta cerrada sin llave, ¿es infranqueable o dato inválido? Una llave exigida por una puerta que no aparece en la consulta de llaves, ¿se reporta como "llave sin ubicación"? → R: Una puerta cerrada que no especifica llave se considera permanentemente infranqueable (barrera no franqueable con ninguna llave, no es dato inválido). Una llave exigida por una puerta pero ausente en los datos de la consulta de llaves se clasifica y reporta como "llave sin ubicación".
- P: Presupuesto de solicitudes: ¿Se aplica el presupuesto igual que en una partida y qué hace el sistema si se agota (con o sin datos de llaves persistidos)? → R: Se aplica el mismo presupuesto y contabilidad de solicitudes que en una partida regular (contando datos generales, páginas del esqueleto y consulta de llaves). Si el presupuesto se agota antes de disponer de todos los datos necesarios y estos no están completamente almacenados en caché persistente para la versión actual, el sistema aborta informando el error de presupuesto de solicitudes agotado, sin emitir reporte de resolubilidad.

## Escenarios de usuario y pruebas

### Historia de usuario 1 - Verificación previa al iniciar partida y control de acceso (Prioridad: P1)

Como jugador que inicia una partida en una cripta, deseo que el sistema verifique de antemano si la cripta tiene solución antes de permitirme jugar, para evitar invertir tiempo en un laberinto imposible de completar a menos que decida forzar el inicio explícitamente.

**Por qué esta prioridad**: Es la funcionalidad central de cara al usuario que previene frustración al garantizar que toda partida iniciada sea completable bajo las reglas del juego, actuando como compuerta de seguridad al arrancar.

**Prueba independiente**: Puede probarse de manera aislada intentando iniciar una partida regular sobre una cripta no resoluble sin parámetros adicionales, comprobando que el juego no arranca y emite el reporte diagnóstico.

**Escenarios de aceptación**:

1. **Dado** una cripta configurada como no resoluble, **Cuando** el usuario ejecuta el inicio de partida regular sin el parámetro `--forzar`, **Entonces** la partida no inicia, el entorno de juego no se ejecuta y se presenta en pantalla el reporte detallado de no resolubilidad.
2. **Dado** una cripta configurada como no resoluble, **Cuando** el usuario ejecuta el inicio de partida incluyendo el parámetro `--forzar`, **Entonces** el sistema presenta el reporte de advertencia de no resolubilidad y procede a iniciar la partida normalmente.
3. **Dado** una cripta resoluble, **Cuando** el usuario ejecuta el inicio de partida regular, **Entonces** el sistema presenta el reporte de resolubilidad confirmando que es posible ganar y arranca la partida normalmente.

---

### Historia de usuario 2 - Verificación diagnóstica independiente vía CLI (Prioridad: P1)

Como evaluador o administrador del sistema, deseo ejecutar la verificación de resolubilidad de una cripta mediante el comando `--verificar <cripta>` sin que se instancie la interfaz gráfica ni la simulación interactiva, para obtener un diagnóstico rápido y automatizable por consola.

**Por qué esta prioridad**: Permite la auditoría automatizada, pruebas por lotes y validaciones en canalizaciones continuas o defensas de curso, cumpliendo con la separación arquitectónica sin interfaz.

**Prueba independiente**: Puede probarse ejecutando `cripta --verificar <id_cripta>` desde la consola y constatando que se imprime el reporte diagnóstico y el proceso termina sin abrir vistas interactivas ni requerir interacción humana.

**Escenarios de aceptación**:

1. **Dado** el identificador de una cripta resoluble, **Cuando** se ejecuta el comando `--verificar <id_cripta>`, **Entonces** el sistema emite el reporte indicando que es resoluble junto con la secuencia determinista de llaves, sin iniciar ninguna vista interactiva.
2. **Dado** el identificador de una cripta no resoluble, **Cuando** se ejecuta el comando `--verificar <id_cripta>`, **Entonces** el sistema emite el reporte detallando las llaves inalcanzables, puertas bloqueadas y ciclos detectados, retornando el control a la terminal sin iniciar la vista interactiva.

---

### Historia de usuario 3 - Detección y diagnóstico de bloqueos y ciclos de dependencia (Prioridad: P2)

Como jugador o analista de laberintos, cuando una cripta no es resoluble deseo ver un reporte exhaustivo que señale exactamente qué llaves no pueden obtenerse, qué puertas forman la frontera bloqueada y, si existe un ciclo donde una llave está encerrada por puertas que dependen de ella misma, se detalle el ciclo concreto.

**Por qué esta prioridad**: Proporciona el valor analítico y explicativo esencial de la capacidad, transformando un rechazo opaco en una justificación transparente del diseño del laberinto.

**Prueba independiente**: Puede probarse aislando un laberinto donde la llave de salida se ubica tras la única puerta que dicha llave abre, verificando que el reporte emitido resalta de manera explícita la dependencia circular.

**Escenarios de aceptación**:

1. **Dado** una cripta donde la llave de salida está situada tras la única puerta cerrada que ella misma abre (caso Apéndice B), **Cuando** se evalúa su resolubilidad, **Entonces** el resultado es no resoluble y el reporte señala explícitamente el ciclo concreto de dependencia circular.
2. **Dado** una cripta no resoluble con varias puertas cerradas adyacentes a las salas alcanzables, **Cuando** se evalúa su resolubilidad, **Entonces** el reporte enumera cada una de las puertas de la frontera bloqueada indicando la llave requerida por cada una y la ubicación donde reside dicha llave (sala o enemigo).

---

### Historia de usuario 4 - Determinismo en el reporte de resolubilidad (Prioridad: P2)

Como usuario o auditor del motor del juego, cuando se realiza la verificación de resolubilidad de una cripta, deseo que todo el reporte generado (secuencia de llaves, orden de puertas de la frontera bloqueada y ciclos de dependencia) sea 100% determinista e idéntico entre ejecuciones sucesivas, resolviendo cualquier ambigüedad u orden alternativo por menor identificador en orden ascendente.

**Por qué esta prioridad**: Asegura la reproducibilidad de bitácoras, pruebas de regresión y cumplimiento estricto del principio de determinismo exigido por el proyecto.

**Prueba independiente**: Puede probarse ejecutando la verificación dos o más veces consecutivas sobre una misma cripta con múltiples ramas de recolección de llaves, fronteras o ciclos, y comparando los reportes generados para verificar que sean exactamente idénticos carácter por carácter.

**Escenarios de aceptación**:

1. **Dado** una cripta resoluble que admite múltiples órdenes válidos de obtención de llaves (caso Apéndice B), **Cuando** se ejecuta la verificación de resolubilidad en dos ocasiones independientes bajo la misma configuración, **Entonces** ambas ejecuciones producen exactamente la misma secuencia ordenada de llaves, desempatando por menor identificador en orden ascendente.
2. **Dado** una cripta no resoluble con múltiples puertas en la frontera bloqueada o múltiples ciclos, **Cuando** se ejecuta la verificación en dos ocasiones independientes, **Entonces** el reporte lista las puertas de la frontera y los ciclos exactamente en el mismo orden determinista, aplicando orden ascendente por identificador.

---

### Historia de usuario 5 - Ubicación y recolección de llaves portadas por enemigos (Prioridad: P3)

Como jugador, deseo que el análisis de resolubilidad considere que las llaves que sueltan los enemigos (cualquier enemigo: errantes, rastreadores y cazadores) se pueden obtener en la sala donde dicho enemigo inicia su recorrido, asumiendo que todo enemigo puede ser vencido.

**Por qué esta prioridad**: Establece el contrato de disponibilidad de llaves móviles o custodiadas, evitando falsos negativos en criptas donde las llaves no están en el suelo sino en inventario de enemigos.

**Prueba independiente**: Puede probarse sobre una cripta donde una llave indispensable para progresar es portada por un enemigo errante, rastreador o cazador, verificando que la llave se asume recolectable al alcanzar la sala inicial de ese enemigo.

**Escenarios de aceptación**:

1. **Dado** una cripta donde una llave requerida figura en el campo de objetos que suelta un enemigo de cualquier tipo (errante, rastreador o cazador; caso Apéndice B), **Cuando** se evalúa la resolubilidad, **Entonces** el sistema asigna la ubicación de dicha llave a la sala donde ese enemigo inicia su recorrido y la considera obtenida tan pronto el jugador alcanza dicha sala inicial.
2. **Dado** un enemigo portador de llave ubicado en una sala inalcanzable desde la región accesible, **Cuando** se evalúa la resolubilidad, **Entonces** la llave portada por dicho enemigo se clasifica como no obtenible y se reporta como causa de bloqueo si alguna puerta de la frontera la requiere.

---

### Casos límite

- **Laberinto desconectado sin puertas**: La sala inicial y la sala de salida se encuentran en componentes no conectados sin que existan puertas cerradas intermedias. El sistema debe clasificar la cripta como no resoluble y reportar que no existe conexión hacia la salida.
- **Sala inicial sin salidas transitables**: La sala de inicio no posee salidas abiertas o sus únicas salidas están cerradas con llaves no presentes en la sala inicial. El sistema reporta no resolubilidad con frontera bloqueada en las salidas de la sala de origen.
- **Llave de salida inmediatamente accesible**: La llave de salida y la puerta final están al alcance directo desde la sala de inicio sin requerir llaves intermedias. El sistema reporta resoluble de forma inmediata con una secuencia que contiene la llave de salida.
- **Cadena de dependencias circulares múltiples**: Existen dos o más grupos de llaves bloqueadas entre sí (por ejemplo, llave A tras puerta B y llave B tras puerta A, junto a otro grupo independiente C y D). El sistema debe identificar un ciclo concreto representativo por cada grupo de llaves en bloqueo mutuo (no todos los ciclos posibles de la cripta), ordenándolos en el reporte por el menor identificador de llave de cada ciclo de manera determinista.
- **Trampas y puertas de cierre automático en la ruta**: La ruta hacia una llave contiene salas con trampas o mecanismos que cierran puertas automáticamente tras pasar. Por los supuestos establecidos, estos factores no deben bloquear el análisis de resolubilidad.
- **Presupuesto de solicitudes de red agotado o limitado**: La verificación consume presupuesto para la consulta de datos generales, páginas del esqueleto y llaves. Si el presupuesto de solicitudes se agota antes de obtener todos los datos necesarios y estos no se encuentran almacenados localmente para la versión actual de la cripta, el sistema aborta informando el error de presupuesto agotado, sin emitir ningún reporte de resolubilidad.
- **Acceso a la sala de salida por puerta abierta**: Llegar a la sala de salida atravesando una puerta abierta no cuenta como resolución de la cripta; las reglas exigen que el jugador debe ingresar a la sala de salida a través de una puerta que requiera explícitamente `llave_salida`.
  - **Dado** una cripta donde la sala de salida es alcanzable directamente desde la sala inicial a través de una puerta abierta, pero no se obtiene la llave de salida o no se cruza una puerta que la requiera para acceder a dicha sala de salida, **Cuando** se evalúa la resolubilidad, **Entonces** el sistema clasifica la cripta como no resoluble y emite el reporte indicando que no se cumplió la condición de entrada con `llave_salida`.
- **Puertas cerradas sin llave y llaves ausentes en la consulta**: Una puerta cerrada no especifica llave requerida, o bien una puerta cerrada exige una llave que no figura en ninguna sala ni enemigo en la consulta de llaves.
  - **Dado** una cripta con una puerta cerrada sin llave asociada o una puerta cerrada cuya llave exigida no figura en la consulta de llaves, **Cuando** se ejecuta la verificación de resolubilidad y dichas puertas o llaves se encuentran en la frontera alcanzable, **Entonces** el sistema clasifica la cripta como no resoluble, incluye la puerta sin llave en la frontera bloqueada indicando que no tiene llave, y reporta la llave ausente como "llave sin ubicación" contabilizándola como no obtenible.

---

## Requisitos

### Requisitos funcionales

- **FR-RES-001**: El sistema DEBE evaluar si una cripta es resoluble partiendo de su sala inicial, verificando si es posible obtener la llave de salida y alcanzar la sala de salida atravesando una puerta que la requiera.
- **FR-RES-002**: El análisis de resolubilidad DEBE asumir que el jugador puede franquear cualquier salida que se encuentre abierta, así como cualquier salida cerrada cuya llave ya haya sido recolectada durante la exploración.
- **FR-RES-003**: El análisis de resolubilidad DEBE asumir que las llaves obtenidas no se consumen al abrir una puerta y pueden reutilizarse indefinidamente para abrir cualquier otra puerta que requiera esa misma llave.
- **FR-RES-004**: El análisis de resolubilidad DEBE asumir que todo enemigo presente en la cripta puede ser derrotado por el jugador al alcanzar su posición.
- **FR-RES-005**: El análisis de resolubilidad DEBE considerar que una llave portada o soltada por un enemigo es obtenible en la sala inicial donde dicho enemigo comienza la partida, aplicando esta regla a cualquier enemigo (errantes, rastreadores y cazadores).
- **FR-RES-006**: El análisis de resolubilidad DEBE asumir que las trampas, peligros ambientales y mecanismos automáticos de cierre de puertas no bloquean ni impiden el paso del jugador.
- **FR-RES-007**: Cuando una cripta resulte ser resoluble, el sistema DEBE generar un reporte que incluya la secuencia válida y ordenada de todas las llaves obtenibles en la cripta, en la que cada llave aparezca después de todas las llaves necesarias para alcanzar la sala donde se encuentra (sin limitarse a las indispensables para llegar a la salida).
- **FR-RES-008**: Todo el reporte emitido por la verificación DEBE ser determinista (misma cripta, mismo reporte). El orden de obtención de las llaves, el orden de las puertas de la frontera bloqueada, y el orden e identificación de los ciclos de dependencia DEBEN ser deterministas entre ejecuciones, aplicando desempate por menor identificador en orden ascendente ante elementos equivalentes.
- **FR-RES-009**: Cuando una cripta no sea resoluble, el sistema DEBE identificar y listar en el reporte el conjunto de todas las llaves que no pueden ser obtenidas desde la región alcanzable.
- **FR-RES-010**: Cuando una cripta no sea resoluble, el sistema DEBE identificar y detallar en el reporte todas las puertas pertenecientes a la frontera bloqueada (puertas cerradas adyacentes a la región alcanzable final, después de usar todas las llaves obtenibles) indicando la llave exigida por cada una de ellas.
- **FR-RES-011**: Cuando una cripta no sea resoluble, el sistema DEBE indicar en el reporte la ubicación conocida (identificador de sala y enemigo asociado si aplica) de cada una de las llaves requeridas por la frontera bloqueada o que no puedan ser obtenidas.
- **FR-RES-012**: Cuando existan dependencias circulares de llaves no obtenibles tras puertas que se bloquean mutuamente (directa o indirectamente), el sistema DEBE aislar e indicar en el reporte un ciclo concreto representativo por cada grupo de llaves que se bloquean entre sí (no todos los ciclos posibles de la cripta). El ciclo de cada grupo debe seleccionarse de forma determinista, y los ciclos de los distintos grupos deben ordenarse en el reporte por el menor identificador de llave en orden ascendente, manteniendo el costo de cómputo aproximadamente lineal.
- **FR-RES-013**: Al iniciar una partida regular, el sistema DEBE ejecutar automáticamente la verificación de resolubilidad y mostrar en pantalla el reporte resultante al usuario.
- **FR-RES-014**: Si una cripta es evaluada como no resoluble al momento de iniciar una partida regular y no se suministra el argumento `--forzar`, el sistema DEBE cancelar el inicio del juego, impedir la entrada al bucle de simulación y mostrar el reporte de no resolubilidad.
- **FR-RES-015**: Si se especifica el argumento de línea de comandos `--forzar` al iniciar una partida sobre una cripta no resoluble, el sistema DEBE emitir el reporte de advertencia y permitir que la partida comience normalmente.
- **FR-RES-016**: La opción de línea de comandos `--verificar <cripta>` DEBE ejecutar exclusivamente la verificación de resolubilidad sobre la cripta indicada, emitiendo el reporte por consola sin instanciar componentes de la vista ni iniciar partidas o simulaciones.
- **FR-RES-017**: La verificación de resolubilidad DEBE obtener los datos requeridos utilizando el esqueleto de la cripta y la información de llaves bajo el contrato de datos de la capacidad 001 (`specs/001-terreno-cazador/contracts/contrato_datos_p2.md`), contabilizando dicha consulta dentro del presupuesto de solicitudes de la cripta y permitiendo su persistencia asociada a la versión de la cripta.
- **FR-RES-018**: El análisis de resolubilidad, la detección de la frontera bloqueada y la identificación de ciclos de dependencia DEBEN calcularse a partir de un único recorrido de exploración integrada de la cripta, sin realizar exploraciones completas adicionales independientes por cada llave.
- **FR-RES-019**: Si una conexión entre dos salas adyacentes es declarada como cerrada en cualquiera de sus dos lados en los datos de la cripta, el sistema DEBE considerarla como cerrada en ambos sentidos, y la llave exigida para franquearla DEBE ser la declarada en cualquiera de los dos lados.
- **FR-RES-020**: La opción de línea de comandos `--bench` DEBE comparar el tiempo del recorrido incremental contra la alternativa ingenua de repetir el recorrido completo por cada llave, utilizando criptas sintéticas con muchas llaves encadenadas generadas de forma determinista mediante una semilla.
- **FR-RES-021**: Si los datos del esqueleto de la cripta presentan costos contradictorios en una misma conexión entre dos salas, la verificación (tanto con `--verificar` como al iniciar una partida) DEBE informar el error de datos inválidos y terminar inmediatamente su ejecución, sin emitir ningún reporte de resolubilidad.
- **FR-RES-022**: Si una conexión entre dos salas está declarada como cerrada pero no especifica llave requerida, el sistema DEBE tratarla como permanentemente infranqueable e incluirla en la frontera bloqueada indicando que no tiene llave. Si una puerta cerrada exige una llave que no aparece en la consulta de llaves, el sistema DEBE clasificarla y reportarla como "llave sin ubicación", contabilizándola como no obtenible dentro del reporte de resolubilidad.
- **FR-RES-023**: La verificación de resolubilidad (tanto en `--verificar` como al inicio de una partida) DEBE aplicar las mismas reglas de contabilidad y límite de presupuesto de solicitudes que una partida regular, consumiendo presupuesto por la consulta de datos generales, cada página del esqueleto y la consulta de llaves. Si el presupuesto se agota antes de disponer de todos los datos necesarios y estos no se encuentran almacenados localmente para la versión activa de la cripta, el sistema DEBE abortar la ejecución informando el error de presupuesto agotado, sin emitir ningún reporte de resolubilidad. Las lecturas desde almacenamiento local y las realizadas con `--offline` no consumen presupuesto de solicitudes.

---

### Entidades clave

- **Cripta**: Estructura del laberinto compuesta por salas interconectadas mediante salidas transitables, con una sala inicial designada para el ingreso del jugador, una sala de salida de escape y una llave de salida obligatoria.
- **Salida / Puerta**: Conexión entre dos salas adyacentes (en este proyecto toda salida conecta dos salas). Posee un estado (abierta o cerrada). Cuando está cerrada, especifica el identificador de la llave obligatoria requerida para desbloquearla. Si cualquiera de sus dos lados la declara cerrada, se considera cerrada en ambos sentidos con la llave declarada en cualquiera de ellos.
- **Llave**: Objeto identificado por un código único necesario para abrir una o más puertas cerradas coincidentes. Puede hallarse depositada en el suelo de una sala específica o ser portada por un enemigo cuya sala inicial está definida.
- **Región Alcanzable**: Conjunto de salas de la cripta a las que el jugador puede acceder desde la sala inicial atravesando únicamente salidas abiertas o salidas cerradas cuyas llaves ya han sido obtenidas previamente en la exploración.
- **Frontera Bloqueada**: Conjunto de salidas cerradas inmediatamente contiguas a la región alcanzable final cuyas llaves asociadas no han sido obtenidas por el jugador tras agotar todas las llaves obtenibles, marcando el límite del avance posible.
- **Ciclo de Dependencia**: Situación de bloqueo mutuo donde el acceso a una llave requiere franquear una o varias puertas cerradas cuyas llaves, a su vez, solo pueden alcanzarse cruzando una puerta que depende de la primera. El reporte aísla un ciclo concreto representativo por cada grupo de llaves que se bloquean entre sí, seleccionado de forma determinista y manteniendo un costo aproximadamente lineal.
- **Reporte de Resolubilidad**: Documento diagnóstico estructurado generado por la verificación, que dictamina si la cripta es o no resoluble. Si es resoluble, incluye la secuencia determinista de recolección de todas las llaves obtenibles en la cripta. Si no lo es, detalla las llaves inalcanzables, las puertas de la frontera bloqueada con sus llaves exigidas, la ubicación de cada llave y los ciclos de dependencia encontrados.

---

## Criterios de éxito

### Resultados medibles

- **SC-001**: La verificación de resolubilidad completa sobre la cripta publicada de mayor tamaño disponible debe ejecutarse en un tiempo cronológico menor a 200 ms en el entorno local de referencia.
- **SC-002**: El costo total de tiempo de la verificación debe ser aproximadamente lineal en relación con la suma del número de salas, salidas transitables y llaves presentes en la cripta analizada.
- **SC-003**: En el 100% de las pruebas ejecutadas sobre criptas resolubles con múltiples caminos válidos de obtención de llaves, dos ejecuciones consecutivas bajo las mismas entradas deben producir exactamente la misma secuencia ordenada de llaves, con desempate determinista por menor identificador en orden ascendente.
- **SC-004**: En el 100% de los casos en que se evalúe una cripta no resoluble, el sistema emite el reporte detallando las llaves no obtenibles y las puertas de la frontera bloqueada sin interrupciones abruptas ni excepciones no controladas.
- **SC-005**: La invocación con el argumento `--verificar <cripta>` debe completar su ejecución emitiendo el reporte por salida estándar sin instanciar elementos de la vista de juego ni esperar entradas interactivas del usuario.
- **SC-006**: La consulta remota para obtener la información de llaves debe consumir una solicitud, más los reintentos por 429 si los hay, dentro del presupuesto de solicitudes de la cripta cuando los datos no estén previamente almacenados en caché persistente.
- **SC-007**: La ejecución de `--bench` debe evidenciar y reportar la diferencia de tiempo entre el recorrido incremental y la alternativa ingenua sobre criptas sintéticas con múltiples llaves encadenadas, produciendo resultados reproducibles basados en semilla.
- **SC-008**: Si el presupuesto de solicitudes de la cripta se agota durante la obtención de datos para la verificación y los datos no están disponibles en la caché persistente local, el proceso debe finalizar inmediatamente indicando el error de presupuesto agotado sin emitir un reporte incompleto ni provocar fallos no controlados.

---

## Supuestos

- Se asume que los datos del esqueleto de la cripta y el catálogo de llaves suministrados por el servicio web son íntegros y corresponden a la versión activa de la cripta analizada.
- Se asume que las llaves nunca se consumen ni se pierden al abrir una puerta cerrada, permaneciendo disponibles durante el resto de la sesión de juego.
- Se asume que para efectos de resolubilidad estática, todo enemigo puede ser vencido por el jugador, por lo que su presencia no constituye una barrera infranqueable si su sala de inicio es alcanzable.
- Se asume que la posición de recolección de una llave portada por cualquier enemigo (errante, rastreador o cazador) corresponde exactamente a la sala donde ese enemigo inicia la partida, con independencia de su patrón de movimiento posterior durante la simulación.
- Se asume que los mecanismos dinámicos de juego (activación y rearme de trampas, cierre periódico o automático de puertas) no alteran las conexiones fundamentales para la alcanzabilidad de la cripta.
- Se asume que la bandera `--forzar` actúa como una decisión de política de ejecución a nivel de interfaz de usuario y no altera el dictamen técnico emitido por el algoritmo de resolubilidad.
