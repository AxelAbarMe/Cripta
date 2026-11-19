# Bitácora de prompts a modelos de lenguaje (LLM)

Cada entrada tiene la fecha, la herramienta o modelo, **Prompt** (lo que se pidió, en primera persona; está redactado de forma compacta y puede estar reinterpretado, pero es fiel a lo pedido), **Prompt (resumido)** (qué se pidió, en una o dos frases) y **Para qué se usó** (qué se hizo con la respuesta). Se registran los prompts que aportaron al avance del proyecto; las consultas pequeñas de un mismo día se agrupan en una sola entrada. Cuando junto al prompt se pegó una salida de consola, un archivo o un zip, no se copia. No se incluyen credenciales ni datos personales. Todo el código y el texto generado con ayuda de un LLM fue revisado y es responsabilidad del grupo.



### 2026-09-20 — Claude Opus 5 (app de escritorio de Claude)
**Prompt:** "Te paso el PDF del enunciado, el openapi.json y el esqueleto inicial del repo. Cómo se organiza la arquitectura que pide §6, el MVC más los adaptadores de red y disco? El enunciado exige una estructura de carpetas específica? Después, paso a paso y explicándome, hagamos un script para probar el API y ver qué responde de verdad, y empecemos los primeros DTO de la cripta y del esqueleto."

**Prompt (resumido):** Se preguntó cómo organizar la arquitectura de §6 (MVC más los adaptadores de red y disco) y se pidió ayuda para probar el API con un script y crear los primeros DTO.

**Para qué se usó:** Entender la arquitectura exigida y si hay una estructura de carpetas obligatoria, crear prueba_api.py para verificar el acceso al API e interpretar sus respuestas reales, y construir los primeros DTO de la cripta y del esqueleto (CriptaResumenDTO, JugadorInicialDTO, CriptaGeneralDTO, SalidaDTO, SalaDTO y PaginaEsqueletoDTO).

### 2026-09-21 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Te paso el contexto del proyecto, el PDF del enunciado, el openapi.json y el zip del repo. Revisa si la estructura de carpetas cumple la arquitectura MVC con adaptadores que pide §6. Explícame cómo funcionan --bench, --offline y --replay, y el servicio HTTP (esqueleto, contenido, catálogo y presupuesto de red). Aclárame la diferencia entre guardar la partida y la prohibición de copiar el estado completo para el pergamino, y si el juego necesita reiniciarse para jugar de nuevo. Al final, proponme una lista de los próximos .py a implementar por carpeta."

**Prompt (resumido):** Se pidió revisar la estructura contra §6, explicar las banderas, el servicio HTTP y el retroceso, y proponer los próximos archivos.

**Para qué se usó:** Planificar la arquitectura, entender las reglas de red/retroceso del enunciado y ordenar el trabajo antes de escribir código de estructuras.

### 2026-09-23 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Te paso el contexto del proyecto (CONTEXTO_CRIPTA_PARA_CLAUDE.md), el PDF del enunciado, el openapi.json y el Cripta.zip. Arma el esqueleto en markdown de la Sección 8, el Documento de Decisiones, para los 11 problemas de §4. Revisa si las carpetas del zip cumplen la arquitectura de §6 (bench/, docs/, fixtures/, tests/). Explícame --bench, --offline y --replay y el servicio HTTP, incluido el modo offline; la diferencia entre guardar la partida y no copiar el estado completo para el pergamino; y si el juego necesita reiniciarse para jugar de nuevo. Dime qué falta en el repo y proponme los próximos .py por carpeta, unidos con nuestra tabla de tareas."

**Prompt (resumido):** Se pidió el esqueleto del Documento de Decisiones, revisar la estructura contra §6, explicar las banderas y el servicio HTTP, y señalar lo que faltaba en el repo.

**Para qué se usó:** Sentar la arquitectura completa del proyecto, entender las reglas de red/retroceso/presupuesto del enunciado, y organizar el trabajo pendiente antes de escribir código de estructuras o DTO.

### 2026-09-23 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Revisa los 6 DTO que ya tenemos contra el openapi.json e implementa los que faltan para cubrir cada GET de la API: el contenido de las salas, las 9 clases de entidad del catálogo según su campo 'clase', las versiones de cripta y catálogo, y los errores 4xx y 429. Para cada uno explícame de dónde salen los datos, por qué se diseña así y dónde se va a usar. Después sepáralos en archivos de una sola clase, como el resto del repo."

**Prompt (resumido):** Se pidió revisar los DTO existentes, implementar los que faltaban y separarlos en un archivo por clase.

**Para qué se usó:** Completar la capa de DTO del proyecto antes de construir el cliente HTTP real.

### 2026-09-23 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Sigamos con los siguientes .py después de los DTO: excepciones.py, puertos.py con las interfaces, contador_solicitudes.py y cliente_http.py, con el manejo del 429, el timeout, la validación de lotes y el conteo de solicitudes. Verifica que todo compile e importe bien."

**Prompt (resumido):** Se pidieron las excepciones, las interfaces, el contador de solicitudes y el cliente HTTP.

**Para qué se usó:** Construir la capa de infraestructura de red que consumirán los servicios y el modelo, cumpliendo las reglas del PDF sobre identificador de cliente, manejo de errores/429 y presupuesto de solicitudes.

### 2026-10-04 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Te paso el zip del proyecto, el PDF del enunciado, el openapi.json y el contexto. Revisa el proyecto completo por secciones (base, estructuras, DTO, infraestructura, modelo, servicios y bench), compáralo con el enunciado, ejecuta el código para confirmar los fallos en vez de suponerlos y al final dame un veredicto de qué falta antes de seguir."

**Prompt (resumido):** Se pidió revisar todo el proyecto contra el enunciado, confirmando los fallos al ejecutar el código.

**Para qué se usó:** Detectar y confirmar bugs, ver qué falta contra el enunciado y ordenar el trabajo pendiente.

### 2026-10-06 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Vamos paso a paso con la corrección de los bugs que bloquean: las constantes que faltan, la lista doble enlazada, el campo id del contenido de sala, el método del veneno, la inserción en VectorOrdenado y la llamada del bench. Dime solo las partes a cambiar y en qué archivo pegarlas."

**Prompt (resumido):** Se pidió corregir paso a paso los bugs que bloqueaban el proyecto.

**Para qué se usó:** Corregir los bugs que impedían importar y ejecutar los servicios, el inventario, la caché y el bench.

### 2026-10-06 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** Contesta la pregunta, para empezar con el controlador y vista, hace falta algo del backend (DTO, Infra, Estruc, Servicios, Modelo) y además, algo del contexto de los md entregados es necesario que se implemente para proceder con lo que mencione?

Fuera de esas dos preguntas, adicionalmente, se necesita algo que no se haya mencionado para empezar la vista y controlador? (Quiero ir implementando primero la vista en consola y al mismo tiempo hacerlo gráfico, ten eso en cuenta). Lo digo de está forma debido a que somos 3, un compañero se está encargando de Infra, Estruc y otro de Servicios, Modelo y DTO. Bench y Test no se cambiará por ahora, ya ellos arreglaron los errores más evidentes y andan trabajando para efectuar todos los cambios de esos 3 MD por lo que yo decidi implementar controlador y vista, contesta todas esas preguntes y no generes código, solo dame una mini guia si ocupo instalar o buscar algo en especifico, además de que expliques un poco como funcionaria MVC para Python y en especifico para Cripta y como funciona la herramienta recomendada para la parte gráfica (con Pygame/Arcade).

**Prompt (resumido):** Se preguntó qué del backend y de los 3 md de revisión es necesario
antes de empezar controlador y vista (consola y gráfica en paralelo), qué falta no mencionado,
y se pidió una mini guía de instalación, cómo funciona MVC en Python y en Cripta, y cómo
funciona Pygame frente a Arcade. Se verificó que los 4 archivos de vista/ y controlador/ están vacíos.

**Para qué se usó:** Definir qué acordar con los compañeros (contrato de `Partida`, acciones,
estado visible) y elegir Pygame antes de escribir Vista y Controlador.

### 2026-10-06 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** "Te paso el zip actualizado. Empecemos con el cliente HTTP: que dé errores de red con contexto, que tenga un tope de reintentos cuando llega un 429 y que cada intento cuente en el presupuesto. Después, que la validación de lotes esté en un solo lugar para los dos clientes y que ClienteGeneral no revise el presupuesto dos veces. Explícame paso a paso y dame una prueba para correrla yo."

**Prompt (resumido):** Se pidió ayuda para mejorar el cliente HTTP (errores de red, reintentos ante un 429 y presupuesto) y validar los lotes en un solo lugar.

**Para qué se usó:** Endurecer el cliente HTTP (errores, 429 y presupuesto) y unificar la validación de lotes.

### 2026-10-07 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** Partida tiene un servicio que luego le envia a otra Partida modelo? Para mantener la división de capas, además ahí están las reglas creadas, comparalas contra las que pide el pdf, ahora ten en cuenta que todo el contexto se repartio en ese otro md enviado, quitando lo de Partida y vista y controlador que hare yo, ahora tomando eso en cuenta, comentame si es posible lo de vista-controlador-servicio-modelo-(DTO,Infra,Estruc) en ese orden de progresión para implementar ambas clases de Partida y empezar con un pequeño segmento de código pequeño sin métodos, solo la definición de clase básica. Ten en cuenta este nuevo zip para el contexto añadido hasta el momento, solo mira los cambios que necesites, en general es el trabajo de los otros dos compañeros definidos en el 2do MD de repartición y correción de tareas, va en proceso, puedes suponer todos los cambios implementados de esa parte a menos que luego lo especifique, ya que eso lo estarán trabajando, quiero que solamente hagas las explicaciones que te pedi breves, voy a usar pygame

**Prompt (resumido):** Se compartió el nuevo zip, el contrato de `Partida` y el reparto de trabajo
entre dos integrantes. Se preguntó si `Partida` necesita un servicio que la envíe a otra clase
`Partida` del modelo, se pidió comparar el contrato con el PDF, confirmar si es viable el orden
vista → controlador → servicio → modelo → (DTO, infra, estructuras) y obtener el esqueleto de
ambas clases sin métodos. El usuario usará Pygame.

**Para qué se usó:** Separar `Partida` (modelo) de `ServicioPartida` (servicios), detectar
discrepancias del contrato con el PDF (nombre del DTO, rechazos, bloqueo con Pygame) y arrancar
la implementación por capas.

### 2026-10-07 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Definamos el contrato de la API pública del motor Partida. Después sigamos paso a paso, por etapas con commits pequeños, mejorando el modelo para poder hacer el retroceso y el guardado: el reloj de eventos, los efectos de veneno y velocidad, el historial de retroceso, las puertas del mapa y el inventario. Dime solo qué cambiar, en qué archivo y cómo probarlo."

**Prompt (resumido):** Se pidió definir el contrato de Partida y mejorar el modelo para el retroceso y el guardado.

**Para qué se usó:** Diseñar la interfaz de Partida y corregir y ampliar el modelo (reloj, efectos, historial, mapa e inventario), junto con el texto de las decisiones de diseño correspondientes.

### 2026-10-07 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** "Sigamos con los errores de formato: que digan en qué operación pasaron, en el cliente de red y en el offline. Luego el cliente falso de los tests con la misma validación de lotes y la cripta artificial con llave de salida. Y un script que descargue del API una cripta y el catálogo para guardarlos en fixtures/ y usarlos con --offline, con la documentación del formato."

**Prompt (resumido):** Se pidió ayuda para que los errores de formato indiquen la operación, para ajustar el cliente falso y la cripta artificial de los tests, y para crear un script que genere los fixtures de --offline.

**Para qué se usó:** Mensajes de error con contexto, ajustar los dobles de prueba y crear los fixtures de cripta-01 con su formato.

### 2026-10-08 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Te paso el proyecto actualizado con el trabajo de los dos. Revisa lo relevante y prueba el flujo con los datos reales de cripta-01 de fixtures/. Después sigamos paso a paso con el modelo: un método del mapa para la llave y el cierre automático de una puerta, y el comportamiento de los enemigos (guardián, errante y rastreador). Luego hagamos el motor Partida por trozos y la acción del jugador."

**Prompt (resumido):** Se pidió probar la integración con cripta-01 y seguir con las puertas, los enemigos y el primer trozo del motor.

**Para qué se usó:** Verificar la integración, escribir la decisión del turno de los enemigos, la acción del jugador y el primer trozo del motor Partida, y redactar el texto de las decisiones de diseño del rastro y de la agenda.

### 2026-10-08 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** "El profe confirmó que para --offline se guardan los JSON del API y que la organización queda a nuestro criterio. Cómo lo anoto en el documento del formato? Después corrijamos los detalles de los DTO (cerrada booleana, tipos de abre y rearme, nombre del archivo de ContenidoSalaRespuestaDTO), y hagamos que la bitácora de la partida la pueda leer el replay, con una partida por archivo, la última línea cortada y la validación del encabezado y las versiones."

**Prompt (resumido):** Se pidió anotar la confirmación del profesor sobre --offline, además de ayuda para corregir detalles de los DTO y adaptar la bitácora de la partida para el replay.

**Para qué se usó:** Documentar la confirmación del profesor, corregir los DTO y rehacer la bitácora de la partida para el replay.

### 2026-10-09 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Sigamos con el segundo trozo del motor Partida: moverse entre salas, abrir puertas con llave, trampas, cierre automático y victoria, probándolo con la cripta real de fixtures/. Después el tercer trozo: atacar, recoger, soltar, equipar y usar objetos. Luego corrige objetos_suelo en la vista y revisa el código sin uso del modelo. Después empecemos el retroceso completo con los ganchos de inversa de los objetos del modelo y conectémoslo a Partida con la acción del pergamino."

**Prompt (resumido):** Se pidió completar el motor (movimiento, puertas, trampas y objetos) y el retroceso con el pergamino.

**Para qué se usó:** Escribir y verificar el movimiento, las puertas y las trampas del motor, y redactar las decisiones de diseño correspondientes.

### 2026-10-09 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** Tengo una idea, quiero que la pantalla de juego se base en 3 pantallas, la primera sera la de elegir jugar, salir, creditos, etc. Cuando toque creditos solo muestra un pequeño bloque de texto con nuestra información de autores y salir, salir lo regresa al menu principal, salir en el menu principal acaba con el ejecutable.
Jugar lo envia a otra pantalla donde se observe las criptas a elegir (Como puedo saber el total de criptas a elegir? o el max de criptas disponibles?) y cuando se elija una, se coloca la información del jugador e inicia la partida, en la partida ya se dibuja normal la sala y todo lo que ya hablamos de dicha interfaz y se juega normalmente, talvez en una esquina se muestran los controles.
Cuando muera o gane, se muestra un aviso y pasa a otra pantalla con los puntuajes. En ese punto dime que deberia de ocurrir despues, que se cierre el ejecutable ya para salir o un jugar de nuevo que lo envie de vuelta a elegir criptas?
Que tan factible es está idea tanto para consola como gráfica.

**Prompt (resumido):** Se compartió el zip actualizado y se pidió preparar la
Vista (consola y Pygame) y el controlador: cómo obtener la lista de sprites,
tamaños, salas y minimapa, qué pedir a los compañeros y si lo actualizado
cumple reglas, contrato y enunciado. Después se propuso un flujo de pantallas
(menú, créditos, elección de cripta, partida, aviso de fin y puntajes) y se
preguntó cómo saber el total de criptas, qué hacer tras los puntajes y la
factibilidad en consola y gráfica.

**Para qué se usó:** Diseñar la máquina de estados del controlador y el
contrato de la Vista, definir la lista y el tamaño de sprites, revisar el
cumplimiento del zip actualizado y listar lo que falta pedir al resto del equipo.

### 2026-10-09 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** Entonces ahora haz el tutorial o que debo hacer para implementar TODA la vista completa y que debo de hacer para cada sprite, que les debo de pedir a los compañeros que implementen para poder avanzar con eso, como uso pygame y dime como se codea todo lo relacionado a eso, los sprites de que tamaño deben ser y que tantos genericos deberia de hacer, como hago para las salas que se creen en base a un mismo sprite cuadrado de una sala donde moverse en el mapa, etc etc. Dime todo, además dime como saber cuantas criptas hay, saber todo lo que existe ahora mismo y buscar cada una con todas las posibles criptas, como avanzar y codear toda esa área

Toma eso como contexto, solo ignora el prompt de arriba y dime como debo de avanzar para ir realizando cada Sprite correspondiente, para irlo realizando tanto en forma de consola y grafica.

**Prompt (resumido):** Se compartió el zip actualizado y se pidió una guía para implementar la vista (consola y pygame con sprites de Aseprite): qué sprites se necesitan, tamaños, cómo saber las criptas y el catálogo, qué pedir a los compañeros, y si lo actual cumple contrato, reglas y PDF.

**Para qué se usó:** Revisar el estado del proyecto, detectar qué le falta a VistaPartida y al motor, y planificar el inventario de sprites y el orden de trabajo de la vista y el controlador.

### 2026-10-09 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** "Revisa el guardado binario (struct precompilados, campos agrupados y validación de valores y del archivo) y que la caché en disco trate un archivo dañado como ausente para no gastar solicitudes de más. Luego, en ServicioCatalogo, que obtener_varias cuente aciertos y fallos igual que obtener cuando un id se repite."

**Prompt (resumido):** Se pidió ayuda para revisar el guardado binario, tratar los archivos dañados de la caché como ausentes y corregir el conteo de aciertos y fallos con ids repetidos.

**Para qué se usó:** Reforzar el guardado binario y la caché en disco, y corregir el conteo de aciertos y fallos del catálogo.

### 2026-10-10 — Claude (Sonnet 5, claude.ai)
**Prompt:** "Te paso el proyecto actualizado (versión 4). Haz una revisión general y sigamos con el puente de guardado: primero convertir la partida viva a EstadoPartida, con sus tests sobre la cripta real. Revisa también la medición del rendimiento del ciclo de eventos y cómo documentarla. Después hagamos la vuelta: reconstruir la partida desde un estado guardado."

**Prompt (resumido):** Se pidió el guardado de la partida en sus dos sentidos y revisar la medición del ciclo de eventos.

**Para qué se usó:** Escribir la conversión de la partida a datos planos y sus tests, y redactar el texto de las decisiones de diseño del guardado y de la evidencia de rendimiento.

### 2026-10-10 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** Quiero validar con pruebas manuales los últimos cambios de infraestructura y servicios (la espera máxima y el cierre de la precarga, el orden de los enemigos al poblar una sala, el desalojo del catálogo con fichas en uso y la ColaCircular con su error propio) y decidir dónde debe vivir el error de la cola vacía, antes de cada commit.

**Prompt (resumido):** Se pidió validar con pruebas manuales la precarga, el orden de los enemigos, el desalojo con fichas en uso y la ColaCircular, y decidir dónde definir el error de la cola vacía.

**Para qué se usó:** Confirmar la espera máxima de la precarga y el cierre del servicio, que preparar_sala ordena los enemigos con ordenar_auto y que el desalojo respeta las fichas en uso, y decidir que ColaCircularVaciaError vive junto a la estructura y hereda de IndexError, porque es un error de programación y no externo.

### 2026-10-11 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** "Te paso el proyecto actualizado (versión 4) con el contrato de la partida. Empecemos el servicio que arma la partida: construcción, bitácora de acciones y reporte final, y revisa el contrato. ¿Qué necesita la parte de la interfaz para empezar los controladores?" Después: "Te paso la versión 5 con lo que hizo un compañero en la tabla de puntajes. Revisa si eso cambia lo pendiente y sigamos con la segunda parte del servicio de partida: guardar y cargar, puntaje final y ranking. Decidamos también qué hacer con la bitácora al cargar."

**Prompt (resumido):** Se pidió el servicio de partida en dos partes: armarla con su bitácora y reporte, y después guardar, cargar, puntaje y ranking.

**Para qué se usó:** Escribir ServicioPartida y Partida.fichas_en_uso con sus tests, corregir la reversión de una acción que falla a mitad de camino y redactar las decisiones de diseño y la actualización del contrato. Adicionalmente, se usó para revisar la tabla de puntajes y su repositorio, decidir cómo se restaura la bitácora al cargar, escribir guardar, cargar, puntaje y ranking con sus tests y redactar las decisiones de diseño.

### 2026-10-11 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** Quiero la opción más sencilla, pero con sentido, para ordenar el ranking de puntajes, y validar con pruebas manuales el repositorio de puntajes en disco (archivo inexistente, varios registros, archivo dañado que no se sobrescribe y campos inválidos) antes del commit.

**Prompt (resumido):** Se pidió elegir la opción más sencilla y razonable para el ranking y validar el repositorio de puntajes en disco.

**Para qué se usó:** Elegir la propuesta de ranking que se llevó al equipo (victorias primero y separado por cripta) y validar RepositorioPuntajes antes del commit.

### 2026-10-11 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** "Te paso el zip nuevo. Agrega al bench una carga que mida el ciclo de eventos con la Partida real sobre una cripta artificial, con varias corridas, tiempo típico y peor caso, contra los 20 ms. Y que el bench del inventario no cronometre la construcción de la lista y diga qué compara."

**Prompt (resumido):** Se pidió ayuda para agregar al bench una medición del ciclo de eventos con la partida real y corregir lo que mide el bench del inventario.

**Para qué se usó:** Medir el ciclo de eventos con el motor real y corregir el bench del inventario.

### 2026-10-16 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** "Hice merge de main en mi rama. Terminemos el bench con una carga de solicitudes con lotes y sin lotes para la precarga y el catálogo, y limpia el código del bench que no se usa. Después, que los tests corran todos juntos con discover y escribamos los tests de ColaCircular, la bitácora de partida, el guardado binario, la caché en disco, el archivo de puntajes, ServicioCatalogo y ServicioPrecarga, uno por uno. Al final movamos los tests de ServicioPartida a tests/servicios con el cambio mínimo."

**Prompt (resumido):** Se pidió ayuda para terminar el bench de solicitudes con y sin lotes, hacer que los tests corran juntos con discover y escribir las pruebas de infraestructura y servicios. Durante el trabajo también se pidió que los comentarios no atribuyeran código a personas, porque son para el profesor.

**Para qué se usó:** Completar el bench de solicitudes, escribir las pruebas unitarias de infraestructura y servicios, y corregir el orden de los enemigos en preparar_sala.


### 2026-10-17 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** Te paso la puesta al día del proyecto (v6), el enunciado, el openapi y los 01 a 04. Empecemos con la Fase 1 del plan, puntos 1 a 3: haz que el ranking ordene las derrotas por más enemigos derrotados y, en un empate, por más tiempo vivo, agrega unos puntajes globales en el servicio que reemplacen el lambda del `__main__`, y quita la línea suelta `--replay` del informe. Dime qué buscar y por qué cambiarlo en cada archivo, con sus tests. Después, como nos faltó actualizar la documentación de esos cambios, empecemos por ahí, con su commit.

**Prompt (resumido):** Se compartió el estado del proyecto (versión 6) con su documento de puesta al día y se pidió ejecutar la primera fase del plan: ordenar las derrotas del ranking por enemigos derrotados y tiempo vivo, exponer los puntajes globales en el servicio de partida y limpiar una línea del informe del replay. Luego se pidió actualizar la documentación de esos cambios.

**Para qué se usó:** Escribir y probar el nuevo orden del ranking y los puntajes globales con sus tests, y redactar las decisiones de diseño, la bitácora y el contrato de esta fase.

### 2026-10-17 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** Con el 04 de la auditoría y el zip más reciente, dime qué hallazgos siguen abiertos y cuáles ya están resueltos, y propón en qué orden cerrar los que son del modelo. Revisa de paso que lo del puntaje esté bien aplicado, porque hay un test que falla.

**Prompt (resumido):** Se pidió contrastar la auditoría del proyecto con el código actual, clasificar los hallazgos y proponer el orden para cerrar los del modelo. En la revisión apareció una parte del orden de los puntajes sin aplicar.

**Para qué se usó:** Detectar y completar el ranking y los puntajes globales de la tabla, y priorizar lo pendiente.

### 2026-10-17 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** Analiza los datos enviados primeramente y luego trabajamos en cada sección cuando me indiques que hayas finalizado. Solo responde "Listo" cuando ya lo tengas todo

+-- MENSAJES (ultimos 20) --------------------------------------------------------------------------------------+
| Entras a Sala 2.                                      | Recoges Coraza de cuero.                              |
| Recoges Llave de bronce.                              | Equipas Coraza de cuero.                              |
| Recoges Daga oxidada.                                 | Entras a Sala 4.                                      |
| Daga oxidada se equipa, no se usa.                    | Recoges Llave negra.                                  |
| Equipas Daga oxidada.                                 | Entras a Sala 5.                                      |
| Entras a Sala 3.                                      |                                                       |
+---------------------------------------------------------------------------------------------------------------+

Colocale un indice numerico tipo 1. 2. 3. y asi a los mensajes, además revisa esto

PS C:\Users\<usuario>\Cripta> py -m cripta --replay partida.log
[Error] Bitácora de partida inválida (partida.log): el archivo no existe

y ademas:

`ContadorSolicitudes.reiniciar()` (H-10). Sin él, el reporte de la segunda partida de una sesión suma las solicitudes de la primera.
Estructura y tests (H-11, H-12, H-13). Faltan tests de heap, lista doble, vector ordenado, ordenamientos, controlador y vista. Además, el rastreador usa búsqueda binaria por vecino (O(log n)) y el §4.7 pide costo proporcional a las salidas. Hay que cambiarlo o justificarlo con medición.
Haz esos 2, Repositorio (H-14, H-22, H-25). Falta excluir `datos/` en `.gitignore` y sacarlo del índice, mover o borrar `prueba_api.py`, y guardar un log de ejemplo real, porque `*.log` está ignorado.

**Prompt (resumido):** Se pidió numerar los mensajes de la bitácora en pantalla
(1., 2., 3.), revisar el error "[Error] Bitácora de partida inválida (partida.log):
el archivo no existe" de --replay, y resolver H-10 (ContadorSolicitudes.reiniciar()),
H-11/H-12/H-13 (tests de estructuras, controlador y vista, y el costo del rastreador
frente a §4.7) y H-14/H-22/H-25 (excluir datos/ del repositorio, log de ejemplo y
mover prueba_api.py). Se entregaron fragmentos "buscar / cambiar por" y archivos de
test nuevos, verificados en una copia (203 tests verdes). Se midió la decisión del
rastreador con 25 a 90 000 salas, se detectó que merge_sort no es estable (pendiente
de autorización) y se confirmó que el error de --replay era la ruta (datos/partida.log).

**Para qué se usó:** Cerrar hallazgos de la auditoría 04 con evidencia: reinicio del
contador por partida (§5.1), cobertura de pruebas de estructuras/controlador/vista
(§7, §10.2), justificación medida del rastreador (§4.7), limpieza del repositorio y
un log de ejemplo reproducible para la defensa de --replay (§4.11, §9).

### 2026-10-17 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** "Te paso la revisión de código que hizo un compañero, revisa qué sigue abierto y prioricemos lo importante. Empecemos la documentación: las secciones 4.3, 4.4 y 4.2 del Documento de Decisiones con las mediciones del bench."

**Prompt (resumido):** Se pidió ayuda para contrastar la revisión de código del proyecto con su estado actual, priorizar lo pendiente y escribir las secciones 4.2, 4.3 y 4.4 del Documento de Decisiones con sus mediciones. Durante el trabajo se pidió arreglar un comando de PowerShell que fallaba por las comillas, que los términos técnicos (por ejemplo "en frío", O(p) o el índice del guardado) se expliquen en el documento sin tener que pedirlo, y se pegaron las salidas de las mediciones, incluida la prueba de espera de la precarga con 400 ms de latencia simulada.

**Para qué se usó:** Redactar las secciones de catálogo, caché y precarga con su evidencia.

### 2026-10-18 — Claude Opus 5.5 (app de escritorio de Claude)
**Prompt:** Quiero cerrar los pendientes finales: arreglos pequeños de código y comentarios (import duplicado del cliente HTTP, MAX_REINTENTOS_429 en constantes, encabezados sin nombres, datos/ fuera de git), mover el script de la primera prueba del API a scripts/ y quitar pytest de requirements.txt si no hace falta. Después, escribir las secciones 4.9, 4.10 y 4.11 del Documento de Decisiones y el README sobre la versión más reciente tras un merge. También explícame por qué faltaban los __init__.py de tests/vista y tests/controlador, y completemos la bitácora de trabajo del 6 al 17 de octubre, que no incluía la parte de red, disco y servicios.

**Prompt (resumido):** Se pidió ayuda para cerrar los pendientes finales: arreglos pequeños de código y comentarios, limpieza del repositorio (prueba_api.py y pytest), las secciones 4.9, 4.10 y 4.11 del Documento de Decisiones, el README, los __init__.py faltantes de las pruebas y la bitácora de trabajo de la parte de red, disco y servicios.

**Para qué se usó:** Arreglos pequeños y limpieza del repositorio, redactar las secciones de ordenamiento, guardado binario y bitácora con replay, escribir el README, agregar los __init__.py para que discover ejecute 33 tests más (213 en total) y completar la bitácora de trabajo.

### 2026-10-18 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** Te paso el contexto actual, el enunciado, el openapi y el zip del proyecto, más los últimos cambios (git pull y los arreglos que están haciendo mis compañeros). Revisa la parte de la documentación: que en la bitácora de prompts todos los prompts vengan completos junto con su resumen, que en la bitácora de trabajo la última anotación no tenga puntos pendientes, y que en las Decisiones de Diseño esté todo completo, sin las líneas de "pendiente revisar" y con sentido, porque algunas cosas se escribieron hace días y pueden estar desactualizadas. No leas el zip completo a profundidad, solo los archivos que necesites.

**Prompt (resumido):** Se pidió revisar la documentación del proyecto: completar y uniformar PROMPTS_LLM.md, cerrar la última entrada de la bitácora sin pendientes y comprobar que el Documento de Decisiones esté completo y actualizado respecto al código.

**Para qué se usó:** Detectar y corregir textos desactualizados o contradictorios en las Decisiones de Diseño (muerte de enemigos en 4.1, límites de 4.6, formato de 4.2, referencias a secciones del enunciado), unificar PROMPTS_LLM.md y cerrar la bitácora del 18/10 con lo realizado.

### 2026-11-09 — Antigravity CLI 1.5.3 (Gemini 3.8 Flash)
**Prompt:** "/speckit-constitution Establece la constitución del proyecto Cripta, segunda parte, completa y en español, con ocho principios y reglas verificables: estructuras de datos a mano (sin dict ni set como índice, heapq, bisect, collections ni sort), determinismo con random.Random(semilla), separación MVC y adaptadores, ningún dato de una cripta concreta en el código, presupuesto de red, rendimiento respaldado con --bench (con los límites de 20, 200, 50 y 5 ms), especificación antes que código y compatibilidad con la primera parte. Incluye restricciones del proyecto, flujo de trabajo (los agentes no hacen commit ni push) y gobernanza con versión 1.0.0." (El texto completo está en prompts/p2/01-constitution.md.)

**Prompt (resumido):** Se pidió generar la constitución de la segunda parte con los ocho principios acordados por el grupo, las restricciones, el flujo de trabajo y la gobernanza.

**Para qué se usó:** Generar el borrador de .specify/memory/constitution.md, que el grupo revisó y ajustó a mano antes de confirmarlo.



### 2026-11-09 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** "Te paso el contexto de la segunda parte, el mapa del código, el contrato del API y los enunciados. Si quiero empezar desde cero, dime en pasos simples y directos qué debo instalar y qué hacer antes de empezar con la constitución. Después ayúdame con el setup de spec-kit con Antigravity (init, AGENTS.md, ramas, Pull Request y borrado de ramas), revisa la constitución que generó el agente contra el enunciado, y dime los pasos siguientes ahora que la constitución está aprobada. Para mi capacidad (001 terreno y cazador) dame el prompt de /speckit-specify y dime si es suficiente o necesita cambios."

**Prompt (resumido):** Se pidió una guía de instalación y setup de spec-kit con Antigravity, la revisión de la constitución contra el enunciado, los pasos siguientes y el prompt de especificación de la capacidad 001 con su verificación.

**Para qué se usó:** Instalar y configurar spec-kit, crear AGENTS.md, ordenar el trabajo con ramas y Pull Requests, corregir la constitución (retroceso sin copias completas, migración explícita, errores HTTP con contexto) y preparar prompts/p2/02-specify-001.md, al que se agregó el contrato de /llaves.

### 2026-11-09 — Antigravity CLI 1.5.3 (Gemini 3.8 Flash)
**Prompt:** "/speckit-specify Capacidad: terreno y cazador de Cripta Parte II. Cada salida puede declarar un costo entero >= 1 (por defecto 100, igual en ambos sentidos) y moverse cuesta ese costo, con intervalo max(1, costo * 100 // velocidad). El cazador es un cuarto comportamiento con rango: ataca si comparte sala con el jugador, calcula el costo mínimo d por salidas abiertas, espera si no hay ruta o d > rango y si no se mueve un paso por una ruta de costo d, con desempate por menor id. Conoce el esqueleto completo, no le afecta la niebla, no abre puertas y su decisión equivale a calcular desde cero en cada turno. El servicio trae costo por salida, comportamiento cazador con rango y la ubicación de llaves. Rendimiento: ciclo de eventos < 20 ms con decenas de cazadores. Incluye los 7 casos del Apéndice B de terreno y cazador como escenarios de aceptación, con prefijo FR-TER-NNN y sin mencionar estructuras, clases ni módulos." (El texto completo está en prompts/p2/02-specify-001.md.)

**Prompt (resumido):** Se pidió generar la especificación de la capacidad de terreno y cazador con sus reglas, el contrato de datos y los escenarios del Apéndice B.

**Para qué se usó:** Generar specs/001-terreno-cazador/spec.md. Se revisó que no mencionara estructuras de datos, clases ni módulos, y no hizo falta quitar nada.


### 2026-11-09 — Antigravity CLI 1.5.3 (Gemini 3.8 Flash)
**Prompt:** "Traduce al español los títulos, etiquetas y palabras clave (Given/When/Then a Dado/Cuando/Entonces) de spec.md y de checklists/requirements.md, sin cambiar el contenido de las reglas. Modifica solo esos dos archivos."

**Prompt (resumido):** Se pidió traducir al español los títulos, etiquetas y palabras clave de la especificación de terreno y cazador y de su lista de verificación, sin alterar las reglas.

**Para qué se usó:** Cumplir la regla de documentación en español de la constitución. Se revisó con git diff que solo cambiaron títulos y etiquetas, y que los requisitos FR-TER-001 a FR-TER-020 y los escenarios del Apéndice B quedaron intactos.

### 2026-11-09 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** "Te paso lo que generó /speckit-specify para la capacidad 001 (spec.md, la lista de verificación y el resumen del agente), junto con el enunciado y el contrato del API. Revisa la especificación contra el enunciado y dime qué hay que corregir. Después, dime los cambios concretos que debo hacer a mano en spec.md y qué hacer con la suposición del rango nulo."

**Prompt (resumido):** Se pidió revisar la especificación de terreno y cazador contra el enunciado y el contrato del API, y se pidieron los cambios exactos para corregirla. Además se preparó el prompt de /speckit-clarify (prompts/p2/03-clarify.md), con una pregunta explícita sobre el rango nulo del cazador.

**Para qué se usó:** Detectar reglas que el agente había inventado y corregirlas a mano en spec.md: se quitó la regla del "rango ilimitado" y se dejó el caso del rango nulo como pendiente para /speckit-clarify, se reemplazaron "al menos 30 cazadores" y "entre 1 y 500" por "decenas de cazadores" y "cualquier velocidad positiva", y se quitó de FR-TER-019 la mención al formato de la primera parte, que corresponde a la capacidad de línea de tiempo.

### 2026-11-09 — Antigravity CLI 1.5.3 (Gemini 3.8 Flash)
**Prompt:** "/speckit-clarify Prioriza ambigüedades que cambiarían el resultado observable: desempates, orden de eventos simultáneos, qué se guarda en partida.log, mensajes de rechazo y los casos del Apéndice B de esta capacidad. Incluye qué debe hacer un cazador cuando su ficha trae el rango nulo o ausente. Las respuestas deben ser compatibles con el enunciado de las Partes I y II. Si la respuesta está en el enunciado, cítala. No inventes reglas." (El texto completo está en prompts/p2/03-clarify-001.md.)

**Prompt (resumido):** Se pidió a spec-kit formular preguntas de aclaración sobre la especificación de terreno y cazador. Las respuestas las decidió el grupo con base en el enunciado.

**Para qué se usó:** Resolver cinco ambigüedades de spec.md: cazador con rango nulo (ficha inválida), contenido de partida.log (solo acciones aceptadas del jugador), orden de eventos simultáneos (número de secuencia), movimientos rechazados (sin consumir tiempo) y llaves sin enemigo (en el suelo). Se agregaron los requisitos FR-TER-021 a FR-TER-023.


### 2026-11-09 — Antigravity CLI 1.5.3 (Gemini 3.8 Flash)
**Prompt:** "/speckit-plan Restricciones obligatorias (ver constitución): implementar a mano las estructuras, prohibido heapq, bisect, collections, networkx, set y dict como índice o caché, y list.sort()/sorted() donde aplica. Reutiliza estructuras de la Parte I y cita el archivo real. El plan debe incluir: problema y operaciones reales con su frecuencia, al menos dos alternativas por problema con la razón de descarte, decisión y complejidad, impacto archivo por archivo, mediciones --bench previstas (incluida la alternativa descartada), límites conocidos, revisión de decisiones de la Parte I que esta carga invalide (agenda, historial) y una tabla de trazabilidad FR, componente y medición. Para esta capacidad debe resolver: búsqueda de ruta de costo mínimo con estructuras propias, límite por rango, cálculo compartido frente a individual, qué eventos invalidan qué cálculo, desempate por menor id, escenarios de --bench con puertas estables e inestables y la alternativa de recalcular siempre, impacto en la agenda y el contrato de datos como bloque separable. No agregues reglas que no estén en spec.md y, si falta una, detente y pregunta." (El texto completo está en prompts/p2/04-plan-001.md.)

**Prompt (resumido):** Se pidió generar el plan técnico de la capacidad de terreno y cazador, con estructuras propias, alternativas descartadas, impacto en el código existente, mediciones previstas y trazabilidad a los requisitos.

**Para qué se usó:** Generar el borrador de plan.md, research.md, data-model.md, quickstart.md y contracts/ en specs/001-terreno-cazador/, que luego se revisó y corrigió contra la constitución y el código de la Parte I.

### 2026-11-09 — Antigravity CLI 1.5.3 (Gemini 3.8 Flash)
**Prompt:** "Corrige estos puntos solo en specs/001-terreno-cazador (plan.md, research.md, data-model.md, quickstart.md y contracts/). No toques spec.md ni otros archivos. 1. Traduce al español los títulos de plan.md. 2. Toda cifra de tiempo o memoria (25 ms, 60 ms, 45-80 ms, 2 ms, 1,3 ms, 50 KB, 50x) escríbela como hipótesis a confirmar con --bench, o quítala. 3. La complejidad con montículo binario es O((V+E) log V). Corrígela en todos los archivos. 4. En 'cálculo compartido vs individual', además de la equivalencia del resultado, explica bajo qué condiciones cambia cuál conviene en rendimiento (pocos cazadores, rangos muy distintos con R_max grande) y que se medirá con --bench. 5. Una ficha de cazador sin rango viene de datos externos: no uses ValueError. Usa la excepción existente CriptaDatosInvalidosError (o CriptaApiError según el origen) con el id de la ficha en el mensaje. ValueError solo para errores de programación. Actualiza la fila de cripta/excepciones.py. 6. Quita del plan los cambios en vista_consola.py y resultado_partida.py, porque ningún FR de spec.md los pide. 7. Agrega la regeneración de fixtures con costo, rango y llaves (scripts/generar_fixtures.py). 8. El comportamiento del catálogo es 'guardián' con tilde. 9. En contracts/contrato_servicio_llaves.json elimina 'additionalProperties': false y 'minimum': 1, y no inventes el texto 'rate_limited'. 10. Presenta lo de los closures y la capacidad de línea de tiempo como riesgo a medir, no como conclusión. 11. No cites archivos que no existan: verifica con Test-Path y márcalos como 'Nuevo' si faltan."

**Prompt (resumido):** Se pidió corregir once puntos del plan de terreno y cazador: idioma de los títulos, cifras de rendimiento sin medir, complejidad del montículo binario, análisis de cuándo conviene el cálculo compartido, excepción para fichas inválidas, cambios sin requisito, fixtures, ortografía del catálogo, contrato de llaves, riesgo sobre la línea de tiempo y archivos citados que no existían.

**Para qué se usó:** Ajustar el plan a la constitución y al código real de la Parte I. Se revisó con git diff que solo cambiaron archivos de specs/001-terreno-cazador/.

### 2026-11-09 — Claude (claude.ai)
**Prompt:** "Termina estas correcciones solo en specs/001-terreno-cazador (plan.md, research.md, data-model.md, quickstart.md y contracts/). No toques spec.md ni otros archivos. 1. En plan.md traduce "Complexity Tracking" al español. 2. Escribe como "hipótesis a confirmar con --bench", o quita, estas cifras: "superará previsiblemente los 35-50 ms", "> 50x más rápida", "30x más lento, viola límite de 20 ms", "~50 KB", "~1.3 ms", "hasta 10x", "Python 3.12.3" y "113 columnas". 3. En la revisión de decisiones de la Parte I (historial de retroceso), presenta lo de los closures y la capacidad 004 como riesgo a medir con --bench --solo historial, no como conclusión. 4. Agrega tests/modelo/test_reloj.py (Nuevo) y scripts/revisar_prohibidos.py (Nuevo) al árbol del plan, o reemplaza el Escenario 4 del quickstart por un Select-String de heapq, bisect, collections y networkx en cripta/modelo y cripta/estructuras. 5. En "Límites Conocidos", punto 2, elimina la frase que afirma que el cálculo compartido sigue siendo drásticamente menor con rangos heterogéneos. 6. En la matriz de invalidación agrega: activación de un cazador con rango mayor al R_max actual, y carga de una partida guardada. 7. Agrega como tarea los __init__.py de tests/dto y tests/aceptacion. 8. Anota como riesgo que regenerar fixtures cambia la versión de la cripta y puede volver incompatible el --replay de docs/ejemplos/partida_cripta-02.log."

**Prompt (resumido):** Se pidió terminar ocho correcciones pendientes del plan de terreno y cazador: título en español, cifras de rendimiento sin medir, riesgo del historial de retroceso frente a la capacidad 004, auditoría de prohibiciones, límite sobre rangos heterogéneos, matriz de invalidación, __init__.py de las carpetas de pruebas nuevas y riesgo de --replay al regenerar fixtures.

**Para qué se usó:** Completar las correcciones que quedaron a medias en specs/001-terreno-cazador/. El auditor de prohibiciones se resolvió con un Select-String en quickstart.md, sin crear scripts/revisar_prohibidos.py. Se revisó con git diff que solo cambiaron archivos de esa carpeta y PROMPTS_LLM.md.

### 2026-11-09 — Antigravity CLI 1.5.3 (Claude Sonnet 4.6)
**Prompt:** "/speckit-tasks Genera tasks.md en español, incluidos los títulos de las fases y secciones de la plantilla. Usa solo specs/001-terreno-cazador/spec.md, plan.md, data-model.md, research.md, quickstart.md y contracts/. No agregues reglas del juego ni decisiones de diseño que no estén en ellos. Si falta algo, detente y pregunta. Cada tarea cita los identificadores FR-TER-NNN que atiende y la ruta real del archivo que toca (marca Nuevo si no existe). Cada escenario de aceptación de spec.md, incluidos los siete casos del Apéndice B, tiene al menos una tarea de prueba automatizada que cita el requisito, y las pruebas van antes que el código. Las pruebas usan unittest, con un __init__.py en cada carpeta nueva (tests/dto y tests/aceptacion llevan una tarea explícita). Ninguna tarea usa heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted() donde aplica. Ninguna tarea contiene commits ni push. Organización: Fase A bloque de contrato de datos separable y fusionable primero en su propio Pull Request; Fase B terreno; Fase C cazador; Fase D mediciones --bench con la alternativa descartada; Fase E cierre con las 222 pruebas de la Parte I, auditoría de importaciones prohibidas, --replay y entrada en PROMPTS_LLM.md. Marca [P] solo las tareas independientes e indica el orden de dependencias y el punto de corte del primer Pull Request. Modifica solo specs/001-terreno-cazador/tasks.md." (El texto completo está en prompts/p2/05-tasks-001.md.)

**Prompt (resumido):** Se pidió generar la lista de tareas de la capacidad de terreno y cazador, organizada en cinco fases, con cada tarea citando sus requisitos FR-TER y la ruta real del archivo, pruebas antes del código y el contrato de datos como primer bloque fusionable.

**Para qué se usó:** Generar el borrador de tasks.md en specs/001-terreno-cazador/, que luego se revisó contra spec.md y plan.md (cobertura de FR-TER-001 a 023 y de los escenarios del Apéndice B).

### 2026-11-09 — Antigravity CLI 1.5.3 (Claude Sonnet 4.6)
**Prompt:** "Corrige solo specs/001-terreno-cazador/tasks.md (y, si hace falta, la tabla de impacto de plan.md). No toques spec.md ni otros archivos. 1. Agrega una tarea de prueba y, si corresponde, de código para FR-TER-023. Quita FR-TER-023 de T035. 2. En T006 elimina la prueba de rechazo de un archivo de la Parte I. 3. En T020 y T022 reutiliza calcular_tiempo_reprogramado de cripta/modelo/reloj.py en lugar de una fórmula nueva. 4. En T038 y T039 marca Nuevo o Modificado según Test-Path y agrega esos archivos a la tabla de impacto de plan.md. 5. En la estrategia indica que cada fase de código va en una rama nueva desde main. 6. En T036 agrega el caso de rangos heterogéneos, en T002 cambia id de ficha por id de sala y corrige la dependencia entre C y D."

**Prompt (resumido):** Se pidió corregir seis puntos de tasks.md: cobertura de FR-TER-023, una prueba fuera de alcance, una fórmula inventada, archivos no citados en el plan, estrategia de ramas y detalles menores.

**Para qué se usó:** Ajustar tasks.md al plan y a la especificación antes de /speckit-analyze.

### 2026-11-09 — Claude (claude.ai)
**Prompt:** "Corrige solo specs/001-terreno-cazador/tasks.md y la tabla de trazabilidad de plan.md. No toques
spec.md ni otros archivos.
1. En "Estrategia de Implementación" aclara que hay tres Pull Requests: (a) documentación (spec,
   plan, tasks), (b) Fase A en rama nueva desde main, (c) Fases B a E en otra rama nueva desde main
   después de fusionar la Fase A. Quita la frase que llama a la Fase A "PR de documentación".
2. Quita de la Fase B la nota "puede iniciarse en paralelo con Fase C" y de la Fase D la nota
   "puede iniciarse en paralelo con Fase E". El orden es secuencial A, B, C, D, E.
3. Elimina T043 de tasks.md. El registro de /speckit-tasks en PROMPTS_LLM.md se hace fuera de las
   tareas de implementación.
4. Mueve T035b a la Fase B, en B.1 antes de T021, y agrégale una tarea de código posterior que
   verifique o corrija cripta/modelo/partida.py (_despachar) para que el desplazamiento rechazado no
   consuma tiempo ni escriba en partida.log (FR-TER-023). Actualiza las dependencias.
5. En T007 cambia "id de ficha" por "id de la sala".
6. En la trazabilidad de plan.md, usa para FR-TER-007 y FR-TER-021 el archivo de prueba que cita
   cada tarea. En T028 cambia "Ampliar" por "Crear".
7. Usa en T021, T022 y T025 los nombres reales de cripta/modelo/reloj.py: calcular_intervalo, calcular_tiempo_reprogramado, EventoProgramado y RelojEventos."

**Prompt (resumido):** Ramas: quedaron tres Pull Requests: documentación, Fase A y Fases B a E, cada uno desde una rama nueva desde main.
Paralelismo: quité las notas contradictorias. El orden es A, B, C, D, E.
FR-TER-023: la prueba pasó a la Fase B, antes del código (T019b), y agregué la tarea de verificación posterior (T025b). La prueba ahora pide mensaje de rechazo, reloj sin avanzar, estado e historial intactos y sin línea en partida.log.
Detalles menores: T007 dice “id de la sala” y T028 dice “Crear

**Para qué se usó:** Ajustar tasks.md al plan y a la especificación antes de /speckit-analyze.

### 2026-11-09 — Antigravity CLI 1.5.3 (Claude Sonnet 4.6)
**Prompt:** "Corrige solo la tabla de impacto, el árbol de código fuente y la tabla de trazabilidad de specs/001-terreno-cazador/plan.md, y la tarea T043 de tasks.md. No toques spec.md ni otros archivos. 1. Agrega cripta/modelo/efectos.py como Modificado (EfectoCierrePuerta invalida el BuscadorRutas, T033; se verifica EfectoCambioVelocidad, T022), en la tabla de impacto y en el árbol. 2. Reemplaza la fila docs/DECISIONES.md por DECISIONES.md (raíz), Modificado, sección de la capacidad 001 (T043). En la fila de tests/controlador/test_controlador_errores.py cambia T035b por T019b. En tasks.md T043 cambia verificar con Test-Path y crearlo por ampliar DECISIONES.md. 3. En la trazabilidad, FR-TER-007: la prueba es tests.aceptacion.test_terreno_costos. 4. En la trazabilidad, FR-TER-005: componente reloj.py (calcular_tiempo_reprogramado, reprogramar) y efectos.py (EfectoCambioVelocidad)."

**Prompt (resumido):** Se pidió alinear plan.md con tasks.md: agregar efectos.py al impacto, actualizar la referencia de DECISIONES.md y de T019b, y corregir la prueba de FR-TER-007 y el componente de FR-TER-005 en la trazabilidad.

**Para qué se usó:** Eliminar inconsistencias entre el plan y las tareas antes de /speckit-analyze.

### 2026-11-10 — Antigravity CLI 1.5.3 (Claude Sonnet 4.6)
**Prompt:** "/speckit-analyze Analiza la consistencia entre specs/001-terreno-cazador/spec.md, plan.md, tasks.md y la constitución. Solo lectura: no modifiques ningún archivo. Verifica en particular: cada FR-TER-001 a 023 tiene al menos una tarea y una prueba que lo cita, y ninguna tarea cita un requisito inexistente; los siete casos del Apéndice B aparecen como escenarios con prueba; plan.md no agrega reglas que no estén en spec.md y spec.md no nombra estructuras, clases ni módulos; ninguna tarea ni decisión usa heapq, bisect, collections, networkx, set ni dict como índice o caché; cada afirmación de rendimiento cita un comando de --bench o está marcada como hipótesis; las rutas de archivo del plan y de las tareas coinciden (Nuevo / Modificado); las pruebas van antes que el código en cada fase y el orden de dependencias entre fases es coherente; el contrato de datos (Fase A) es separable y no depende de B, C, D ni E. Clasifica cada hallazgo por gravedad y señala el archivo y la línea." (El texto completo está en prompts/p2/06-analyze-001.md.)

**Prompt (resumido):** Se pidió un análisis de solo lectura de la consistencia entre la especificación, el plan, las tareas y la constitución de la capacidad de terreno y cazador, con cobertura de requisitos y del Apéndice B, prohibiciones, afirmaciones de rendimiento, rutas de archivo, orden de pruebas y separabilidad del contrato de datos.

**Para qué se usó:** Detectar inconsistencias entre spec.md, plan.md y tasks.md antes de abrir el Pull Request de documentación. Los hallazgos se revisan y se corrigen primero, en commits separados, antes de abrir el Pull Request.

### 2026-11-10 — Antigravity CLI 1.5.3 (Claude Sonnet 4.6)
**Prompt:** "Corrige solo specs/001-terreno-cazador/plan.md, tasks.md y data-model.md. No toques spec.md ni otros archivos. 1. En la tabla de impacto de plan.md agrega cripta/modelo/cripta_mapa.py como Sin cambios (la simetría del costo viene en los datos del servicio) y en la trazabilidad de FR-TER-002 cita la prueba tests.aceptacion.test_terreno_costos (T019). 2. Agrega tests/infraestructura/test_partida_log.py (Modificado) al árbol de código fuente de plan.md. 3. En tasks.md T035 amplía la prueba para que cubra movimiento, espera y ataque de cazadores, errantes y rastreadores: ninguno escribe líneas en partida.log (FR-TER-021). 4. En la trazabilidad de plan.md, FR-TER-016 cita también cripta/dto/salida_dto.py y FR-TER-017 cita también cripta/dto/enemigo_dto.py. 5. En data-model.md renombra los métodos de BuscadorRutas (tabla y diagrama de clases) a calcular_o_reutilizar, decidir_paso y distancia, igual que plan.md, contrato y T031."

**Prompt (resumido):** Se pidió corregir los hallazgos de /speckit-analyze: una fila faltante en la tabla de impacto, un archivo de prueba ausente del árbol, el alcance de la prueba de partida.log, la trazabilidad de FR-TER-016 y 017 y los nombres de métodos de BuscadorRutas en data-model.md.

**Para qué se usó:** Resolver los hallazgos de gravedad media y los nombres inconsistentes del análisis antes de abrir el Pull Request de documentación.

### 2026-11-10 — Claude (Sonnet 5.5, claude.ai)
**Prompt:** "Cuando el agente se quedó sin cuota, se pidió a Claude terminar las correcciones de plan.md y research.md de la capacidad 001. Después se subieron spec.md, plan.md, tasks.md y data-model.md con este pedido: Analiza la consistencia entre specs/001-terreno-cazador/spec.md, plan.md, tasks.md y la constitución. Solo lectura: no modifiques ningún archivo. Verifica en particular: que cada FR-TER-001 a 023 tenga al menos una tarea y una prueba que lo cite y que ninguna tarea cite un requisito inexistente, que los siete casos del Apéndice B aparezcan como escenarios con prueba, que plan.md no agregue reglas que no estén en spec.md y que spec.md no nombre estructuras, clases ni módulos, que ninguna tarea ni decisión use heapq, bisect, collections, networkx, set ni dict como índice o caché, que cada afirmación de rendimiento cite un comando de --bench o esté marcada como hipótesis, que las rutas de archivo del plan y de las tareas coincidan (Nuevo / Modificado), que las pruebas vayan antes que el código en cada fase y que el contrato de datos (Fase A) sea separable. Clasifica cada hallazgo por gravedad y señala el archivo y la línea. Después: aplica las correcciones propuestas en los archivos."

**Prompt (resumido):** Se pidió completar las correcciones de plan.md y research.md y hacer un análisis de consistencia de solo lectura entre la especificación, el plan, las tareas y la constitución, con hallazgos por gravedad, y luego aplicar las correcciones.

**Para qué se usó:** Como Antigravity se quedó sin cuota, se corrigieron plan.md y research.md (cifras de rendimiento como hipótesis, complejidad O((V+E) log V), eventos de invalidación, riesgo de fixtures) y se hizo el análisis que habría hecho /speckit-analyze. Se aplicaron cinco ajustes: el rechazo de un costo inválido en FR-TER-016, los nombres de los métodos de BuscadorRutas en data-model.md, las pruebas faltantes en el árbol de plan.md, el orden de T035 en tasks.md (prueba antes del código) y la verificación de FR-TER-020 en T039, además de la auditoría de T041.


### 2026-11-10 — Claude Opus 5.5 (app de Claude)
**Prompt:** Decidimos como grupo que yo iba a aplicar las correcciones de 001, guíame en el proceso.

**Prompt (resumido):** Guía para aplicar las correcciones de la capacidad 001.

**Para qué se usó:** Corregir los documentos de la capacidad 001 (spec, plan, tareas, research, modelo de datos, quickstart y contrato) y el enlace del README según la revisión del PR #3 y los dos análisis de /speckit-analyze. Incluye la decisión del grupo sobre el cazador sin rango, registrada como sesión de aclaraciones del 2026-11-10. Los cambios se revisaron con git diff antes de hacer los commits.

### 2026-11-10 — Claude Code (Sonnet 5.5)
**Prompt:** /speckit-analyze Sigue las instrucciones de prompts/p2/07-analyze-001-revision.md

**Prompt (resumido):** Análisis de solo lectura de la capacidad 001 después de la revisión del PR (primera ejecución).

**Para qué se usó:** Detectó 19 hallazgos, 3 de gravedad alta. Se corrigieron antes de hacer los commits.

### 2026-11-10 — Claude Code (Sonnet 5.5)
**Prompt:** /speckit-analyze Sigue las instrucciones de prompts/p2/07-analyze-001-revision.md

**Prompt (resumido):** Verificación de las correcciones de la primera ejecución (segunda ejecución).

**Para qué se usó:** Confirmó las correcciones anteriores y detectó 18 hallazgos nuevos, 2 de gravedad alta. Se corrigieron los altos, los medios y los bajos rápidos antes de hacer los commits.

### 2026-11-10 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo los bloques A.0 y A.1 de la Fase A: T001, T001b, T002, T003, T004, T005, T006 y T006b. Solo pruebas y el cliente falso de tests/, nada de código en cripta/. Las pruebas nuevas deben fallar porque el código aún no existe. Al terminar, corre py -m unittest completo, dime cuáles fallan y por qué, y marca las casillas de esas tareas en tasks.md. No sigas con A.2."

**Prompt (resumido):** Escritura de las pruebas del contrato de datos (Fase A) antes del código.

**Para qué se usó:** Crear las pruebas de T001 a T006b. Fallaron solo las nuevas, como se esperaba. Se pidió además que el error por costos contradictorios se exija en agregar_pagina, con las dos salas en páginas distintas.

### 2026-11-10 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo el bloque A.2 de la Fase A: T007 a T015 y T021b. El objetivo es que pasen las pruebas escritas en A.0 y A.1 sin modificarlas. Si una prueba te parece contradictoria con la spec, detente y explícamelo en vez de cambiarla. Al terminar, corre py -m unittest completo y marca las casillas en tasks.md. No sigas con A.3. Para editar archivos usa tu herramienta de edición, no sed -i, porque cambia los finales de línea CRLF."

**Prompt (resumido):** Implementación del contrato de datos (Fase A) contra las pruebas ya escritas.

**Para qué se usó:** Implementar costo, rango, LlaveUbicacionDTO, obtener_llaves en los clientes, la caché de llaves y la resolución de costos en CriptaMapa. Pasaron las 247 pruebas.

### 2026-11-10 — Claude Code (Sonnet 5.5)
**Prompt:** "Corrige solo documentos de specs/001-terreno-cazador/ (spec.md, plan.md, quickstart.md y tasks.md), sin tocar código ni fixtures. El grupo acordó lo siguiente tras revisar el servidor: - cripta-01 ya no existe en el servidor. Hay dos criptas nuevas: cripta-05 "Cripta sellada" (24 salas) y cripta-06 "Cripta de referencia" (300 salas). La versión del catálogo cambió de be68d322d2f5 a 4b9e75a42be5. - cripta-01 se mueve con el catálogo anterior y criptas.json a tests/datos/ como datos de prueba congelados. Las 4 pruebas que usan ClienteOffline("fixtures") (test_guardado_ida, test_guardado_vuelta, test_pergamino, test_servicio_partida) pasan a usar ClienteOffline("tests/datos"), y se actualiza su docstring. - fixtures/ queda igual al servidor actual: cripta-02 a cripta-06 con llaves.json, costo, rango y el catálogo nuevo. - Los tres ejemplos de docs/ejemplos/ ya no se reproducen porque guardan el catálogo anterior. Se reemplazan por ejemplos nuevos que muestren terreno y cazador, en la Fase E. - La cripta de referencia de FR-TER-020 y SC-001 es cripta-06. La carga sintética de 400 salas se mantiene para comparar alternativas, pero la verificación de FR-TER-020 se hace con cripta-06 desde fixtures/. Cambios concretos: 1. spec.md: actualiza el supuesto de la cripta de referencia y agrega una sesión de clarificaciones "Sesión 2026-11-10 (estado del servidor)" con estos hechos. 2. plan.md: actualiza la línea de mediciones de FR-TER-020 y el Límite Conocido 5. 3. quickstart.md: actualiza la medición de FR-TER-020 y el comando de replay de ejemplo. 4. tasks.md: reescribe T016 (el respaldo es el commit e6d52ac y se mueve cripta-01 a tests/datos/ con las 4 pruebas), T017 (regenera cripta-02 a cripta-06 con llaves.json y actualiza docs/FORMATO_OFFLINE.md y la sección de fixtures del README), T039 (mide con cripta-06) y T042 (graba ejemplos nuevos, reemplaza los de docs/ejemplos/ y actualiza la tabla del README). Conserva los ids y el formato de las tareas. No marques casillas. Respeta los finales de línea de cada archivo. No uses sed -i. Al terminar, dime qué cambiaste en cada archivo." Seguimiento, en la misma sesión: "Sí falta una tarea: cargas_bench.py solo tiene cargas sintéticas. Agrega en la Fase D una tarea T036b, antes de T039: modificar cripta/bench/cargas_bench.py para registrar la carga ciclo_referencia, que carga cripta-06 desde fixtures/ con ClienteOffline (sin red ni vista), arma la partida y mide el ciclo de eventos entre dos decisiones del jugador con decenas de cazadores activos. Si cripta-06 no trae suficientes cazadores, la carga activa más instancias de cazador con una semilla fija, y se documenta cuántas. Cita FR-TER-020. Haz que T038 también habilite ciclo_referencia en servicio_bench.py y que T039 use ciclo_referencia. Actualiza la sección de dependencias de tasks.md. Solo tasks.md, no marques casillas, no uses sed -i." (El texto completo está en prompts/p2/08-estado-servidor-001.md.)

**Prompt (resumido):** Ajuste de la spec, el plan, el quickstart y las tareas de 001 a los cambios del servidor (cripta-01 retirada, cripta-05 y cripta-06 nuevas, catálogo nuevo).

**Para qué se usó:** Actualizar T016, T017, T039 y T042, registrar los hechos como sesión de aclaraciones y agregar T036b para medir FR-TER-020 con cripta-06. Se hizo antes del código, en un commit aparte.

### 2026-11-10 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T016. Ya moví con git mv fixtures/cripta-01, fixtures/catalogo y fixtures/criptas.json a tests/datos/, así que no muevas ni copies archivos. Falta solo esto: en tests/modelo/test_guardado_ida.py, tests/modelo/test_guardado_vuelta.py, tests/modelo/test_pergamino.py y tests/servicios/test_servicio_partida.py cambia ClienteOffline("fixtures") por ClienteOffline("tests/datos"), y en la primera línea del docstring de esos 4 archivos y de tests/controlador/test_controlador_cripta.py cambia "la cripta real de fixtures/" por "la cripta congelada de tests/datos/". Usa tu herramienta de edición, no sed -i. Corre py -m unittest y marca T016 en tasks.md. No sigas con T017."

**Prompt (resumido):** Paso de las pruebas de la Parte I a los datos congelados de cripta-01.

**Para qué se usó:** Cambiar la ruta de ClienteOffline en cuatro pruebas y los docstrings de siete. Las 247 pruebas siguieron pasando.

### 2026-11-10 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T017, sin ejecutar el script ni usar la red. Cambios: 1. scripts/generar_fixtures.py: en descargar, guardar también GET /criptas/{id}/llaves como <cripta>/llaves.json tal como llega del API, igual que los demás archivos. En verificar, leer también las llaves con ClienteOffline.obtener_llaves y mostrar cuántas leyó. Que el script siga recibiendo una cripta por ejecución. 2. docs/FORMATO_OFFLINE.md: documentar llaves.json, el campo costo de las salidas (opcional) y el campo rango de las fichas de enemigo (opcional), y aclarar que tests/datos/ guarda cripta-01 con el catálogo anterior como datos de prueba congelados que no se regeneran. 3. README.md: actualizar solo la sección de fixtures y la línea del árbol de carpetas para que digan que fixtures/ tiene cripta-02 a cripta-06 del servidor actual y que tests/datos/ tiene cripta-01 congelada. No toques la sección de bitácoras de ejemplo, eso es de T042. Usa tu herramienta de edición, no sed -i, y respeta los finales de línea de cada archivo. No marques T017 todavía, falta correr el script."

**Prompt (resumido):** Descarga de las llaves en el script de fixtures y documentación del formato.

**Para qué se usó:** Agregar llaves.json al script y documentar los campos nuevos. El script se ejecutó a mano para cripta-02 a cripta-06.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "$speckit-specify Sigue las instrucciones de prompts/p2/02-specify-004.md. SPECIFY_FEATURE_DIRECTORY=specs/004-linea-de-tiempo. [...] Solo crea o modifica archivos dentro de specs/004-linea-de-tiempo/. No agregues reglas del juego que no estén en el prompt ni en docs/CONTEXTO_CRIPTA2.md."

**Prompt (resumido):** Generar la especificación de la línea de tiempo con puntos de control, con los escenarios del Apéndice B y la coordinación con niebla de guerra y formato binario.

**Para qué se usó:** Obtener el borrador de specs/004-linea-de-tiempo/spec.md.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "$speckit-clarify Sigue las instrucciones de prompts/p2/03-clarify-004.md. [...] Modifica solo specs/004-linea-de-tiempo/spec.md. Las respuestas a cada pregunta las doy yo; no decidas reglas del juego."

**Prompt (resumido):** Aclarar ambigüedades de la línea de tiempo: numeración de «historia #k», pergamino, eventos simultáneos, rechazos, formato guardado y valor de K.

**Para qué se usó:** Generar las aclaraciones de spec.md que se mantuvieron ambiguas.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo specs/004-linea-de-tiempo/spec.md y checklists/requirements.md: agrega el escenario de historia tras un pergamino, la precisión de que la consulta no va a partida.log, una historia de guardar y cargar con el caso del archivo de la Parte I y un criterio de éxito de persistencia; no fijes K ni resuelvas el marcador de FR-LIN-012."

**Prompt (resumido):** Completar la cobertura de los escenarios del Apéndice B y de la persistencia en la especificación de la línea de tiempo.

**Para qué se usó:** Cerrar dos escenarios del Apéndice B que solo estaban como casos límite y añadir historia y criterio para guardar y cargar.

### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "$speckit-clarify Sigue las instrucciones de prompts/p2/03-clarify-004.md. [...] Modifica solo specs/004-linea-de-tiempo/spec.md. Las respuestas a cada pregunta las doy yo; no decidas reglas del juego."

**Prompt (resumido):** Aclarar ambigüedades de la línea de tiempo: numeración de «historia #k», acciones que cuentan, instante coincidente con una decisión, pergamino y archivo de la Parte I.

**Para qué se usó:** Obtener cinco aclaraciones registradas en la Sesión 2026-11-16 de spec.md; la última resolvió FR-LIN-012 (incompatibilidad por versión, sin migración).

### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo specs/004-linea-de-tiempo/spec.md y checklists/requirements.md: traduce los encabezados de aclaraciones, restaura los campos de las historias 2 y 4, divide el escenario de la historia 2 en cuatro y actualiza el checklist sin cambiar ninguna regla."

**Prompt (resumido):** Corrección de forma de la especificación tras el clarify: idioma, campos cruzados entre historias y escenarios.

**Para qué se usó:** Dejar spec.md coherente con el formato de las demás capacidades y el checklist en 18/18.

### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo specs/004-linea-de-tiempo/spec.md: registra en la sesión de aclaraciones dos decisiones del grupo (valores inválidos de --checkpoint-cada K y rechazo de consultas de historia sin efecto), agrega FR-LIN-022, FR-LIN-023 y SC-LIN-007 con sus escenarios, redacta los escenarios 2 a 4 de la historia 2 en formato dado/cuando/entonces y agrega las decisiones pendientes de confirmar al apartado de supuestos. No hagas preguntas ni agregues otras reglas."

**Prompt (resumido):** Cierre de las aclaraciones de la línea de tiempo con respuestas ya decididas, sin una nueva ronda interactiva de /speckit-clarify.

**Para qué se usó:** Dejar en la especificación el tratamiento de valores inválidos de K y de consultas rechazadas, y la lista de decisiones del grupo pendientes de confirmar con el profesor.

### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "$speckit-plan Sigue las instrucciones de prompts/p2/04-plan-004.md. SPECIFY_FEATURE_DIRECTORY=specs/004-linea-de-tiempo. [...] Solo crea o modifica archivos dentro de specs/004-linea-de-tiempo/. Puedes LEER (sin modificar) el código, specs/001-terreno-cazador/ y specs/002-niebla-ir-a/plan.md vía git show."

**Prompt (resumido):** Generar el plan de la línea de tiempo con puntos de control: alternativas de reconstrucción, búsqueda del punto de control, recorte por pergamino, memoria frente a K, formato binario y trazabilidad.

**Para qué se usó:** Obtener plan.md, research.md, data-model.md, contracts/ y quickstart.md de specs/004-linea-de-tiempo/.

### 2026-11-11 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo los bloques B.0 y B.1 de la Fase B: T018, T019, T019b y T020. Solo pruebas, nada de código en cripta/. Las pruebas que dependan de código aún no implementado deben fallar; si alguna pasa desde el inicio porque el comportamiento ya existe (por ejemplo T020 sobre reloj.py), dímelo. Al terminar, corre py -m unittest completo, dime cuáles fallan y por qué, y marca las casillas de esas tareas en tasks.md. No sigas con B.2. Para editar archivos usa tu herramienta de edición, no sed -i, porque cambia los finales de línea CRLF."

**Prompt (resumido):** Pruebas de la Fase B (bloques B.0 y B.1) del terreno: T018, T019, T019b y T020.

**Para qué se usó:** Escribir solo las pruebas de los costos de las salidas y del reloj, antes del código, y marcar sus casillas. Las que dependían de código aún inexistente debían fallar.

### 2026-11-11 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo el bloque B.2 de la Fase B: T021 a T025b. El objetivo es que pasen las pruebas de B.0 y B.1 sin modificarlas. T022, T024, T025 y T025b son de verificación: si sus pruebas ya pasan, no cambies código, solo márcalas. Si una prueba te parece contradictoria con la spec, detente y explícamelo en vez de cambiarla. Usa CriptaMapa.costo_de_conexion para obtener el costo de la salida. Al terminar, corre py -m unittest completo y marca las casillas en tasks.md. No sigas con la Fase C. Para editar archivos usa tu herramienta de edición, no sed -i. En los comentarios nunca uses ";"."

**Prompt (resumido):** Implementación del bloque B.2 de la Fase B (T021 a T025b) para que pasen las pruebas de B.0 y B.1.

**Para qué se usó:** Hacer pasar las pruebas del terreno sin modificarlas, usando CriptaMapa.costo_de_conexion para el costo de cada salida. Las tareas de verificación solo se marcaron si sus pruebas ya pasaban.

### 2026-11-12 — Claude Code (Sonnet 5.5)
**Prompt:** "Corrige solo documentos de specs/001-terreno-cazador/ (spec.md, plan.md, research.md, contracts/contrato_datos_p2.md y tasks.md), sin tocar código. El grupo decidió: 1. Llaves con enemigo vacío: en la respuesta de /llaves, un campo enemigo con texto vacío ("") es un dato inválido. LlaveUbicacionDTO.desde_json lanza ValueError con el dato afectado, igual que con un id vacío, y el cliente lo convierte como siempre. Solo null o ausente significa llave en el suelo. - spec.md: agrégalo a FR-TER-018 y añade la pregunta y respuesta a la sesión "Sesión 2026-11-10 (estado del servidor)" o en una sesión nueva "Sesión 2026-11-12 (decisiones previas a la Fase C)". - research.md y contracts/contrato_datos_p2.md: actualiza la regla de enemigo. - tasks.md: agrega T004b justo después de T004 (ampliar tests/dto/test_llave_ubicacion_dto.py con el caso enemigo="" que lanza ValueError, FR-TER-018) y T009b justo después de T009 (ajustar LlaveUbicacionDTO.desde_json para rechazar enemigo vacío, FR-TER-018). Sin marcar. En la sección de dependencias indica que T004b y T009b se hacen antes de la Fase C. 2. Rangos reales: los datos del servidor traen cazadores con rango 600 (ent_sabueso_oseo) y 2400 (ent_espectro_acechador), y costos de salida entre 20 y 490. cripta-06 tiene 25 sabuesos y 11 espectros. - plan.md: cambia la escala de rangos a "hasta 2 400 unidades de costo (valores reales del servidor: 600 y 2 400)". En la carga ruta_cazador, los costos de la cripta sintética pasan a 20-490, los rangos a R=600 y R=2400, y el caso heterogéneo usa la proporción de cripta-06 (25 de rango 600 y 11 de rango 2400, escalada a H). - tasks.md: actualiza T036 con esos mismos valores. 3. Costo de costo_de_conexion en la búsqueda: se mantiene la consulta actual (O(log n) por arista) y se mide. La carga ruta_cazador reporta aparte el tiempo dedicado a consultar costos. La alternativa de precalcular los costos en una tabla plana al construir el mapa (O(1) por consulta) queda como alternativa a evaluar si la medición muestra que pesa, y se documenta en DECISIONES.md (T043). - plan.md: agrégalo a las métricas de ruta_cazador y como límite conocido. - tasks.md: agrégalo a T036 y a T043. Conserva ids, formato y finales de línea de cada archivo. No marques casillas. No uses sed -i. En comentarios y textos nuevos no uses ";". Al terminar, dime qué cambiaste en cada archivo." (El texto completo está en prompts/p2/09-docs-enemigo-vacio-rangos-001.md.)

**Prompt (seguimiento):** "Actualiza solo la descripción de enemigo en contracts/contrato_servicio_llaves.json para que diga que una cadena vacía es un dato inválido que se rechaza (FR-TER-018). No agregues minLength. La fila de plan.md déjala como está."

**Prompt (seguimiento):** "Fue un error mío al rechazar. Vuelve a ejecutar exactamente ese mismo comando (editar2.py con el Límite 6 de plan.md y los cambios de tasks.md)."

**Prompt (resumido):** Decisiones del grupo antes de la Fase C: enemigo vacío como dato inválido, rangos reales del servidor y medición del costo de consulta.

**Para qué se usó:** Actualizar spec, plan, research, contrato y tareas (FR-TER-018, T004b, T009b, T036 y T043). Los seguimientos ajustaron la descripción de enemigo en el contrato JSON sin agregar minLength y repitieron un comando de edición de documentos que se había rechazado por error.

### 2026-11-12 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T004b. Amplía tests/dto/test_llave_ubicacion_dto.py según la tarea. La prueba de enemigo vacío debe fallar porque el código aún no lo rechaza. Corre py -m unittest, dime qué falla y marca T004b en tasks.md. No sigas con T009b. Usa tu herramienta de edición, no sed -i, y en comentarios no uses ";"."

**Prompt (resumido):** Prueba de T004b sobre LlaveUbicacionDTO con el enemigo vacío.

**Para qué se usó:** Ampliar tests/dto/test_llave_ubicacion_dto.py con el caso enemigo vacío, que debía fallar porque el código aún no lo rechazaba (FR-TER-018).

### 2026-11-12 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T009b. Ajusta LlaveUbicacionDTO.desde_json en cripta/dto/llave_ubicacion_dto.py para que pase la prueba de T004b sin modificarla. Corre py -m unittest completo y marca T009b en tasks.md. No sigas con la Fase C. Usa tu herramienta de edición, no sed -i, y en comentarios no uses ";"."

**Prompt (resumido):** Ajuste de LlaveUbicacionDTO.desde_json para T009b.

**Para qué se usó:** Hacer que desde_json rechace el enemigo vacío para que pase la prueba de T004b sin modificarla (FR-TER-018).

### 2026-11-12 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo el bloque C.1 de la Fase C: T026, T026b, T027, T028, T028b y T035. Solo pruebas, nada de código en cripta/. Usa grafos y criptas sintéticas armadas dentro de las pruebas, no fixtures/. Para los rangos de los cazadores usa los valores reales del plan (600 y 2400) donde la prueba necesite valores concretos. Las pruebas que dependan de BuscadorRutas, de HeapMinimo.esta_vacio o de __len__ deben fallar porque ese código aún no existe. Si alguna pasa desde el inicio, dímelo. Al terminar, corre py -m unittest completo, dime cuáles fallan y por qué, y marca las casillas de esas tareas en tasks.md. No sigas con C.2. Usa tu herramienta de edición, no sed -i, y en comentarios no uses ";"."

**Prompt (resumido):** Pruebas del bloque C.1 de la Fase C: T026, T026b, T027, T028, T028b y T035.

**Para qué se usó:** Escribir las pruebas de la búsqueda de ruta del cazador con grafos sintéticos armados en las pruebas. Las que dependían de BuscadorRutas o del montículo debían fallar.

### 2026-11-13 — Claude Code (Sonnet 5.5)
**Prompt:** "Corrige solo documentos de specs/001-terreno-cazador/ (contracts/contrato_datos_p2.md y tasks.md), sin tocar código ni pruebas. 1. En contracts/contrato_datos_p2.md, en el docstring de BuscadorRutas.decidir_paso, aclara que llama internamente a calcular_o_reutilizar(mapa, sala_jugador_id, cazador.rango), así que no hace falta calcular antes, y que la tabla se reutiliza si sigue válida y el rango del cazador no supera el rango con que se calculó. 2. En tasks.md agrega T028c justo después de T028, sin marcar: ampliar tests/aceptacion/test_cazador_persecucion.py con escenarios que comprueben, a través de Partida, que la tabla del cazador se invalida en cada evento de T033 que hoy no tiene prueba propia: el jugador abre una puerta con llave que acorta la ruta, el jugador usa el pergamino de retroceso y vuelve a una sala anterior, se activa un cazador con un rango mayor que el calculado, y se carga una partida guardada. En cada caso la decisión del cazador debe ser la misma que calcular desde cero (FR-TER-015). Actualiza las dependencias para que T028c vaya antes de C.4. Conserva ids, formato y finales de línea. No marques casillas. No uses sed -i. En textos nuevos no uses ";". Al terminar, dime qué cambiaste." (El texto completo está en prompts/p2/10-docs-decidir-paso-t028c-001.md.)

**Prompt (resumido):** Ajuste del contrato de BuscadorRutas.decidir_paso y nueva tarea T028c.

**Para qué se usó:** Aclarar en el contrato que decidir_paso llama a calcular_o_reutilizar y agregar T028c a tasks.md para probar la invalidación de la tabla en los eventos que no tenían prueba propia (FR-TER-015).

### 2026-11-13 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T028c. Amplía tests/aceptacion/test_cazador_persecucion.py con los cuatro escenarios de la tarea, reutilizando los ayudantes de tests/modelo/test_cazador_decisiones.py y criptas sintéticas armadas dentro de la prueba, sin fixtures/. En cada escenario arma la situación de modo que una tabla vieja daría una decisión distinta a la de calcular desde cero, para que la prueba detecte si falta la invalidación. Para la llave y el pergamino usa los mecanismos del juego de la Parte I (recoger, abrir y usar). Para cargar la partida usa el guardado y la carga del servicio de la Parte I. Corre py -m unittest, dime cuáles pasan y cuáles fallan y por qué, y marca T028c en tasks.md. No sigas con C.2. Usa tu herramienta de edición, no sed -i, y en comentarios no uses ";"."

**Prompt (seguimiento):** "El escenario de rango mayor está mal armado. Lo simulé: el jugador entra a la sala 4 por la salida de costo 1000 en t=110, su siguiente decisión es en t=210 y el primer turno del espectro también es en t=210, y el espectro actúa antes, con el jugador todavía en la sala 4, así que ataca. Cuando el jugador vuelve a la 3, ese turno ya pasó, y con la implementación correcta la prueba fallaría por error de la prueba. Rehazlo para que el jugador entre y salga de la sala del espectro por salidas baratas antes del primer turno del espectro, y termine en una sala a la que el espectro llegue con distancia entre 601 y 2400. Por ejemplo, la sala del espectro unida por costo 10 a una sala intermedia, y esa unida por costo 990 a la sala donde termina el jugador, de modo que el espectro dé su primer paso por la salida barata. Calcula a mano los tiempos y deja en comentarios el instante de cada evento. Además, en tests/modelo/test_cazador_decisiones.py renombra _id_ficha y _ficha_cazador a id_ficha y ficha_cazador, porque ahora se importan desde otro archivo, y actualiza sus usos. No toques los otros tres escenarios. No uses sed -i y en comentarios no uses ";"."

**Prompt (resumido):** Pruebas de aceptación T028c con cuatro escenarios de invalidación de la tabla del cazador.

**Para qué se usó:** Ampliar tests/aceptacion/test_cazador_persecucion.py con los escenarios de puerta con llave, pergamino, cazador con rango mayor y carga de partida. El seguimiento rehízo el escenario de rango mayor, que estaba mal armado por el orden de los turnos, y renombró dos ayudantes de tests/modelo/test_cazador_decisiones.py.

### 2026-11-13 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo el bloque C.2 de la Fase C: T029 y T030. Que pasen las pruebas del heap sin modificarlas. Para T030, expón rango en Enemigo tomándolo de su ficha. Corre py -m unittest completo, dime qué cambió en fallos y errores, y marca T029 y T030 en tasks.md. No sigas con C.3. Usa tu herramienta de edición, no sed -i, y en comentarios no uses ";"."

**Prompt (resumido):** Bloque C.2 de la Fase C: T029 y T030.

**Para qué se usó:** Hacer pasar las pruebas del montículo y exponer el rango en Enemigo tomándolo de su ficha.

### 2026-11-13 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo el bloque C.3 de la Fase C: T031. Crea cripta/modelo/buscador_rutas.py según la tarea, el plan, data-model.md y el contrato (contracts/contrato_datos_p2.md), incluido que decidir_paso llama internamente a calcular_o_reutilizar con el rango del cazador. La búsqueda va desde la sala del jugador, usa HeapMinimo, una tabla plana (lista) indexada por id de sala, solo salidas abiertas (puerta_transitable) y los costos con CriptaMapa.costo_de_conexion. Nada de heapq, bisect, collections, dict ni set. El objetivo es que pasen test_buscador_rutas y test_equivalencia_rutas sin modificarlas. Si una prueba te parece contradictoria con la spec, detente y explícamelo. No conectes nada en partida.py ni comportamiento_enemigo.py, eso es C.4. Corre py -m unittest completo, dime qué cambió y marca T031 en tasks.md. Usa tu herramienta de edición, no sed -i, y en comentarios no uses ";". La cabecera del archivo debe tener máximo 5 líneas y cada método 1 o 2 líneas de comentario."

**Prompt (resumido):** Bloque C.3 de la Fase C: T031.

**Para qué se usó:** Crear cripta/modelo/buscador_rutas.py con la búsqueda de ruta de costo mínimo según la tarea, el plan, el modelo de datos y el contrato.

### 2026-11-13 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo el bloque C.4 de la Fase C: T032, T033 y T034. Conecta el cazador al motor según las tareas. Un cazador con rango None nunca llama a BuscadorRutas: ataca si comparte sala y si no espera con costo 100, y el aviso a la bitácora de mensajes va al activarlo. La decisión del cazador devuelve también el costo, sin cambiar lo que devuelven errantes y rastreadores. Invalida la tabla en todos los eventos de T033 aunque parezca redundante, incluido el pergamino. El objetivo es que pasen todas las pruebas sin modificarlas. Si una prueba te parece contradictoria con la spec, detente y explícamelo. Corre py -m unittest completo y marca T032, T033 y T034 en tasks.md. No sigas con la Fase D. Usa tu herramienta de edición, no sed -i, y en comentarios no uses ";"."

**Prompt (resumido):** Bloque C.4 de la Fase C: T032, T033 y T034.

**Para qué se usó:** Conectar el cazador al motor de la partida, incluido el cazador sin rango, el costo de su decisión y el aviso a la bitácora al activarlo.

### 2026-11-13 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo el bloque D.1 de la Fase D: T036, T036b, T037 y T038. Sigue las tareas y la sección de mediciones del plan con los valores actuales: rangos 600 y 2400, costos de 20 a 490, la mezcla de cripta-06 escalada a H, H=1, 10 y 30, y el tiempo de consulta de costos (costo_de_conexion) reportado aparte. Las alternativas descartadas (cálculo individual desde cada cazador y recalcular siempre) se implementan dentro de cargas_bench.py, sin cambiar BuscadorRutas, CriptaMapa ni partida.py, y respetan las mismas prohibiciones que el código evaluado: HeapMinimo y tablas planas, sin heapq, bisect, collections, dict ni set. Para medir el tiempo de consulta de costos, envuelve la llamada en la carga, sin modificar el código del juego. Usa una constante con nombre para la semilla 42 de la tarea y no cambies SEMILLA_BENCH. ciclo_referencia carga cripta-06 desde fixtures/ con ClienteOffline y no escribe ningún dato de la cripta en el código. Si cripta-06 ya trae suficientes cazadores, no agregues más, y reporta cuántos había activos al medir. No corras las mediciones largas todavía, solo comprueba que cada carga arranca con py -m cripta --bench --solo <carga> a escala pequeña si existe esa opción, y que py -m unittest sigue en OK. Marca T036, T036b, T037 y T038 en tasks.md. No sigas con T039. Usa tu herramienta de edición, no sed -i, y en comentarios no uses ";"."

**Prompt (resumido):** Bloque D.1 de la Fase D: T036, T036b, T037 y T038.

**Para qué se usó:** Implementar en cargas_bench.py las cargas ruta_cazador, invalidacion y ciclo_referencia con sus alternativas descartadas, con los rangos 600 y 2400 y los costos de 20 a 490.

### 2026-11-13 — Claude Code (Sonnet 5.5)
**Prompt:** "Contexto: en la rama 001-terreno-cazador-fases-b-e ya están implementadas las cargas de la Fase D (T036, T036b, T037 y T038) en cripta/bench/cargas_bench.py y cripta/servicios/servicio_bench.py. Antes de correr las mediciones (T039) hay que hacer cuatro ajustes, sin cambiar BuscadorRutas, CriptaMapa ni partida.py: 1. ciclo_referencia: hoy despierta solo 1 cazador real de cripta-06 y agrega 29 copias. cripta-06 trae 36 cazadores reales. Cambia la carga para que no agregue copias y despierte a todos los cazadores reales con la activación del propio juego (cargando el contenido de sus salas como lo hace el juego), sin escribir datos de la cripta en el código. Reporta cuántos quedaron activos. Si quedan menos de 30, detente y dímelo antes de agregar nada. 2. Mueve los ayudantes compartidos de tests/modelo/test_cazador_decisiones.py (grafo, construir_mapa, armar_partida, id_ficha, ficha_cazador, recorrer, avanzar_hasta, cazador_de, tiempo y las constantes RANGO_SABUESO y RANGO_ESPECTRO) a un módulo de ayuda nuevo, tests/cripta_cazadores.py, como tests/cripta_artificial.py. Actualiza los imports de todas las pruebas que los usan y de cargas_bench.py, sin cambiar ninguna aserción. 3. En el resultado de la razón individual/compartido de ruta_cazador, no la muestres como un tiempo en ms. Que quede claro que es una razón. 4. Aclara en las notas de ruta_cazador e invalidacion que el número de búsquedas y decisiones es el total de la corrida, no por ciclo. Usa tu herramienta de edición, no sed -i. Los archivos nuevos van en CRLF con una conversión que primero pase todo a \n y luego a \r\n. En comentarios no uses ";". Al terminar, corre py -m unittest y las tres cargas (ruta_cazador, invalidacion y ciclo_referencia) a escala 0.1, y dime el resultado y cuántos cazadores reales quedaron activos en ciclo_referencia. No marques ni desmarques casillas y no sigas con T039." (El texto completo está en prompts/p2/11-ajustes-cargas-fase-d-001.md.)

**Prompt (resumido):** Cuatro ajustes a las cargas de la Fase D antes de correr T039.

**Para qué se usó:** Hacer que ciclo_referencia despierte a todos los cazadores reales de cripta-06 sin copias, mover los ayudantes compartidos a tests/cripta_cazadores.py, mostrar como razón y no como ms el resultado individual contra compartido, y aclarar que las búsquedas y decisiones son totales de la corrida.

### 2026-11-13 — Claude Code (Sonnet 5.5)
**Prompt:** "Corrige solo documentos de specs/001-terreno-cazador/ (spec.md, plan.md, quickstart.md y tasks.md), sin tocar código. Motivo: el enunciado P2 §6.1 fija el límite de 20 ms para la "Cripta de referencia con decenas de cazadores activos", y FR-TER-020 y SC-001 dicen "en persecución simultánea", que es más de lo que pide. Con los datos de cripta-06, que tiene 36 cazadores, como máximo 8 tienen al jugador dentro de su rango a la vez desde cualquier sala, así que esa redacción no se puede cumplir con la cripta de referencia. 1. spec.md: en FR-TER-020, SC-001 y el resumen del inicio, cambia la condición a la de §6.1: cripta de referencia con decenas de cazadores activos. Agrega a la sesión "Sesión 2026-11-12 (decisiones previas a la Fase C)", o a una nueva "Sesión 2026-11-13 (medición de FR-TER-020)", una pregunta y respuesta que lo explique, con el dato de los 36 activos y el máximo de 8 en rango, y que el caso de decenas persiguiendo a la vez al mismo jugador (P2 §5.1) se mide con la carga sintética ruta_cazador. 2. plan.md y quickstart.md: donde hablen de FR-TER-020 con cazadores "en persecución simultánea", ajusta la redacción igual, y deja claro que ciclo_referencia verifica §6.1 y ruta_cazador con H=30 compara cálculo compartido contra individual (§5.1). 3. tasks.md: ajusta T036b y T039 para que digan "activos" en vez de "persiguiendo", y que T039 reporte de ciclo_referencia los cazadores activos y el promedio en persecución por ciclo. Conserva ids y formato, no marques casillas. Respeta los finales de línea de cada archivo, no uses sed -i y en textos nuevos no uses ";". Al terminar, dime qué cambiaste en cada archivo." (El texto completo está en prompts/p2/12-docs-fr-ter-020-activos-001.md.)

**Prompt (seguimiento):** "T036b todavía describe que se agregan copias de cazadores si faltan. Actualízala para que diga que ciclo_referencia despierta a todos los cazadores reales de cripta-06 con la activación del juego, sin agregar copias, y reporta los cazadores activos y el promedio en persecución por ciclo. Solo esa tarea, sin marcar casillas, sin sed -i y sin ";" en el texto nuevo."

**Prompt (resumido):** Corrección de FR-TER-020 y SC-001 para que digan cazadores activos y no en persecución simultánea.

**Para qué se usó:** Alinear spec, plan, quickstart y tasks con el apartado 6.1 del enunciado, tomando en cuenta que cripta-06 tiene 36 cazadores y como máximo 8 con el jugador en su rango. El seguimiento actualizó el texto de T036b para que no agregue copias de cazadores.

### 2026-11-14 — Claude Code (Sonnet 5.5)
**Prompt:** "En cripta/bench/cargas_bench.py, en las cargas ruta_cazador, invalidacion y ciclo_referencia, llama a gc.collect() justo antes de empezar cada corrida medida (después de armar la partida y antes del primer ciclo cronometrado), dejando el recolector encendido durante la medición. No apagues el recolector. Motivo, para un comentario corto: así cada escenario no paga la basura acumulada por los anteriores. Una medición con el recolector apagado mostró que los picos de unos 130 ms y de unos 20 ms venían de pausas del recolector. Usa tu herramienta de edición, sin sed -i y sin ";" en comentarios. Corre py -m unittest y las tres cargas a escala 0.1, y dime qué cambiaste."

**Prompt (resumido):** Llamada a gc.collect() antes de cada corrida medida de las cargas del cazador.

**Para qué se usó:** Reducir el ruido de las mediciones en ruta_cazador, invalidacion y ciclo_referencia sin apagar el recolector de memoria.

### 2026-11-14 — Claude Code (Sonnet 5.5)
**Prompt:** "Corrige solo documentos de specs/001-terreno-cazador/ (plan.md y tasks.md), sin tocar código. Es una revisión de una decisión de la Parte I (P2 §5.6) descubierta al medir la Fase D. Hechos medidos: - El peor caso de la carga partida de la Parte I supera 20 ms con 400 salas (29.5, 43.8 y 48.2 ms en Windows con Python 3.14), y la Parte I lo había documentado con la causa sin aislar. - La causa son las pausas del recolector de memoria de Python. Con el recolector apagado el peor caso baja a unos 15 ms y la mediana no cambia. En una partida de 400 salas con 1287 acciones, una limpieza completa encuentra 0 objetos de basura cíclica y la memoria es igual con o sin limpiezas (8.5 MB), así que esas pausas recorren objetos vivos, sobre todo el historial de retroceso, sin recuperar nada. - Llamar a gc.freeze() al terminar cada acción del jugador deja el peor caso en 11.1, 15.7 y 17.4 ms en Windows con Python 3.14 (en Linux con Python 3.10 baja de 55-66 ms a 14-15.6 ms), con la mediana igual y un costo de unos 0.01 ms por llamada. - Alternativas evaluadas: apagar el recolector (descartada porque deja de recoger basura cíclica nueva), limpiar con gc.collect() en el tiempo ocioso tras cada acción (descartada porque cada limpieza cuesta 35 a 72 ms con 400 salas), subir el umbral de la generación 2 (descartada porque el recolector de Python 3.14 trabaja distinto y no es portable). - Riesgo: la basura cíclica entre objetos congelados no se recoge. Se midió 0, y se documenta como límite conocido. 1. plan.md: en la sección "Revisión de Decisiones de la Parte I que esta Carga pueda Invalidar", agrega esta revisión con problema, evidencia, alternativas, decisión (gc.freeze() al final de Partida.ejecutar_accion, que cubre el juego, --replay y el bench, porque las cargas del cazador llaman a Partida directamente sin pasar por ServicioPartida) y riesgo. 2. tasks.md: en la Fase D agrega, sin marcar: - T039b: prueba en tests/modelo/ que, después de Partida.ejecutar_accion, gc.get_freeze_count() es mayor que 0, con limpieza (gc.unfreeze) al final de la prueba, y luego el cambio en cripta/modelo/partida.py que llama a gc.freeze() al terminar ejecutar_accion (P2 §5.6, FR-TER-020). - T039c: prueba en tests/bench/ (con __init__.py) que ejecuta cada carga registrada en CARGAS a una escala mínima y comprueba que devuelve resultados sin lanzar excepciones (Principio VIII). Motivo: un cambio de la Fase C rompió la carga ciclo sin que ninguna prueba lo detectara. - Ajusta T039 para que las mediciones definitivas se tomen después de T039b, y que T043 documente el antes y el después de esta revisión. Actualiza las dependencias de la Fase D. Respeta los finales de línea de cada archivo, no uses sed -i y en textos nuevos no uses ";". Al terminar, dime qué cambiaste." (El texto completo está en prompts/p2/13-docs-revision-gc-freeze-001.md.)

**Prompt (seguimiento):** "tasks.md está en LF, no en CRLF. En el script usa '\r\n' solo para plan.md y '\n' para tasks.md. Lo demás está bien, vuelve a correrlo con ese cambio."

**Prompt (resumido):** Revisión de una decisión de la Parte I (P2 5.6) descubierta al medir la Fase D, con gc.freeze.

**Para qué se usó:** Agregar al plan la revisión con problema, evidencia, alternativas, decisión y riesgo, y crear T039b y T039c en tasks.md. El seguimiento corrigió el script para respetar que tasks.md usa LF y plan.md usa CRLF.

### 2026-11-16 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo la primera parte de T039b: la prueba. Crea en tests/modelo/ un archivo de prueba que arme una partida pequeña con los ayudantes existentes (por ejemplo tests/cripta_cazadores.py), ejecute una acción con Partida.ejecutar_accion y compruebe que gc.get_freeze_count() es mayor que 0. Llama a gc.unfreeze() con addCleanup para que se limpie aunque la prueba falle, y empieza la prueba con gc.unfreeze() para partir de cero. Cita P2 §5.6 y FR-TER-020. La prueba debe fallar porque el código aún no llama a gc.freeze(). No toques cripta/ ni marques T039b todavía. El archivo nuevo va en CRLF con la conversión segura, sin sed -i y sin ";" en comentarios. Corre py -m unittest y dime qué falla."

**Prompt (seguimiento):** "Renombra la clase PruebaCongelarMemoria a TestCongelarMemoria en tests/modelo/test_congelar_memoria.py, para seguir la convención de las demás pruebas. Solo eso, con tu herramienta de edición. Luego corre py -m unittest tests.modelo.test_congelar_memoria y confirma que sigue fallando por la misma razón."

**Prompt (seguimiento):** "Ahora la segunda parte de T039b: en cripta/modelo/partida.py, al final de Partida.ejecutar_accion, llama a gc.freeze() justo antes de devolver el resultado, en todos los caminos de salida del método (aceptada y rechazada). Agrega import gc y un comentario de una línea sin ";" que explique que congela los objetos vivos para que el recolector no vuelva a recorrerlos (P2 §5.6). No modifiques la prueba. Corre py -m unittest completo y marca T039b en tasks.md. Usa tu herramienta de edición, sin sed -i."

**Prompt (resumido):** T039b en dos partes: la prueba de gc.freeze y el cambio en Partida.ejecutar_accion.

**Para qué se usó:** Escribir la prueba que exige gc.get_freeze_count() mayor que 0, renombrar su clase a TestCongelarMemoria y llamar a gc.freeze() al final de ejecutar_accion.

### 2026-11-16 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo la tarea T039c de specs/001-terreno-cazador/tasks.md. Crea tests/bench/__init__.py y una prueba en tests/bench/ con clase de prefijo Test que recorre CARGAS de cripta/bench/cargas_bench.py y ejecuta cada carga con la escala mínima que acepte (revisa en cada función qué escala o parámetros usa para que la prueba sea rápida, sin cambiar las cargas) y comprueba que devuelve una lista no vacía de resultados sin lanzar excepciones. Si una carga tarda demasiado aun con escala mínima, dime cuál y cuánto antes de buscar otra solución. Usa finales de línea CRLF como el resto de los .py, no uses sed -i y no pongas ";" en comentarios. Corre la suite completa, marca T039c como [X] en tasks.md respetando que ese archivo usa LF y dime qué hiciste."

**Prompt (seguimiento):** "Repite lo mismo pero escribe el archivo con encoding="utf-8" además de newline="", porque en Windows la codificación por defecto no es UTF-8 y el texto tiene tildes. Quita el print de los tiempos de la prueba y en su lugar dime en tu respuesta cuánto tardó cada carga."

**Prompt (resumido):** T039c: prueba que ejecuta cada carga registrada en CARGAS a escala mínima.

**Para qué se usó:** Crear tests/bench/ con una prueba que detecta si una carga se rompe, y ajustar la escritura del archivo con UTF-8 y sin print de tiempos.

### 2026-11-16 — Claude Code (Sonnet 5.5)
**Prompt:** "Corrige solo documentos de specs/001-terreno-cazador/ (spec.md, plan.md y tasks.md), sin tocar código. El enunciado P2 §7.3 exige: "La vista debe mostrar los costos de las salidas de la sala actual y distinguir a los cazadores de los demás enemigos." Ningún requisito ni tarea de 001 lo cubre, y hoy la vista muestra las salidas sin costo (por ejemplo "E->2") y los enemigos sin indicar si son cazadores. 1. spec.md: agrega FR-TER-024 con esa exigencia, sin nombrar clases ni módulos, y un escenario de aceptación en la historia de usuario que corresponda (por ejemplo: dado un jugador en una sala con una salida de costo 250 y un cazador, cuando se muestra la sala, entonces se ve el costo 250 de esa salida y el cazador aparece distinguido de los demás enemigos). Agrega una pregunta y respuesta en una nueva sesión de clarificaciones "Sesión 2026-11-16 (vista)", después de la sesión 2026-11-13. 2. plan.md: agrega a la tabla de archivos y al árbol los cambios en cripta/modelo/resultado_partida.py (SalidaVista con el costo resuelto de la salida, EnemigoVista con un indicador de cazador), cripta/modelo/partida.py (al armar la vista, usar CriptaMapa.costo_de_conexion y el comportamiento del enemigo) y cripta/vista/vista_consola.py (mostrar el costo junto a cada salida y una marca para los cazadores), y la trazabilidad de FR-TER-024. 3. tasks.md: agrega un bloque "C.5 — Vista" en la Fase C, después de C.4, con dos tareas sin marcar: T034b, la prueba (en tests/vista/test_vista_consola.py y, para los datos de la vista, en tests/modelo/) que comprueba que la vista de la partida trae el costo de cada salida y la marca de cazador y que la vista de consola los muestra (FR-TER-024), y T034c, la implementación (FR-TER-024). Actualiza las dependencias dentro de la Fase C. Respeta los finales de línea de cada archivo (spec.md y plan.md usan CRLF, tasks.md usa LF), no uses sed -i y en textos nuevos no uses ";". Al terminar, dime qué cambiaste." (El texto completo está en prompts/p2/14-docs-vista-fr-ter-024-001.md.)

**Prompt (resumido):** Nuevo requisito FR-TER-024 para mostrar los costos de las salidas y distinguir a los cazadores en la vista (P2 7.3).

**Para qué se usó:** Actualizar spec, plan y tasks con el requisito, un escenario de aceptación, una sesión de aclaraciones de la vista y las tareas T034b y T034c.

### 2026-11-16 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo la tarea T034b de specs/001-terreno-cazador/tasks.md (FR-TER-024), sin tocar código de cripta/. Antes de escribir, lee cripta/modelo/resultado_partida.py (SalidaVista, EnemigoVista, VistaPartida), el método de Partida que arma la vista y cripta/vista/vista_consola.py (_paneles_izquierdos), y revisa cómo están armadas las pruebas existentes en tests/vista/test_vista_consola.py y los helpers de tests/cripta_cazadores.py para reutilizarlos. 1. tests/modelo/test_vista_partida.py (Nuevo, clase con prefijo Test): con una partida armada con los helpers, el jugador en una sala con una salida de costo 250 y otra sin costo declarado, y en esa sala un cazador y un enemigo que no es cazador. Comprueba que la vista de la partida trae costo 250 y 100 en esas salidas y que el indicador de cazador es verdadero solo para el cazador. Agrega un caso con un cazador sin rango válido, que también debe marcarse como cazador porque su comportamiento lo es. 2. tests/vista/test_vista_consola.py (Modificado): con una vista armada a mano, comprueba que la salida de la vista de consola muestra el costo junto a cada salida y una marca que distingue al cazador. No fijes el formato exacto del texto más allá de que aparezca el número del costo en la línea de esa salida y que la línea del cazador se distinga de la del otro enemigo. Usa los nombres de campo costo en SalidaVista y es_cazador en EnemigoVista. Las pruebas deben fallar ahora porque esos campos no existen: córrelas, muéstrame que fallan por esa razón y no por otra. CRLF en los .py, no uses sed -i, no pongas ";" en comentarios y no marques T034b todavía. Dime qué hiciste."

**Prompt (resumido):** T034b: pruebas de la vista con costos y cazadores (FR-TER-024).

**Para qué se usó:** Crear tests/modelo/test_vista_partida.py y ampliar tests/vista/test_vista_consola.py. Las pruebas debían fallar porque los campos costo y es_cazador aún no existían.

### 2026-11-16 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo la tarea T034c de specs/001-terreno-cazador/tasks.md (FR-TER-024). Las pruebas de T034b ya existen y fallan: tests/modelo/test_vista_partida.py y la clase TestTerrenoEnLaVista de tests/vista/test_vista_consola.py. No las modifiques. 1. cripta/modelo/resultado_partida.py: agrega costo: int al final de SalidaVista y es_cazador: bool al final de EnemigoVista, con un comentario corto cada uno. 2. cripta/modelo/partida.py, en el método que arma la vista (donde se crean SalidaVista y EnemigoVista): el costo de cada salida se obtiene con CriptaMapa.costo_de_conexion, el mismo que usa _mover, y es_cazador según el comportamiento del enemigo, usando la constante o el valor que ya use comportamiento_enemigo.py para identificar al cazador. Un cazador sin rango válido también es cazador. 3. cripta/vista/vista_consola.py, en _paneles_izquierdos: muestra el costo junto a cada salida (por ejemplo "E->2 (250)", conservando " [CERRADA]") y una marca visible para los cazadores en la línea del enemigo (por ejemplo "[CAZADOR]"). Revisa que las líneas no pasen del ancho del panel izquierdo (_ANCHO_IZQ) con costos de 3 dígitos y cuatro salidas cerradas. Si se pasan, dime cómo lo resolviste. 4. docs/CONTRATO_PARTIDA.md, línea de VistaPartida (sección 5): agrega el costo de cada salida y si el enemigo es cazador, conservando el estilo y los finales de línea CRLF. CRLF en los .py, no uses sed -i, no pongas ";" en comentarios. Corre la suite completa, marca T034c como [X] en tasks.md (LF) y dime qué hiciste."

**Prompt (seguimiento):** "Corre exactamente lo mismo pero sin la parte "sed -i.x 's/x/x/;q' /dev/null 2>/dev/null;", que no hace nada y no se debe usar sed -i. Deja el resto igual."

**Prompt (resumido):** T034c: implementación de la vista con costos y cazadores (FR-TER-024).

**Para qué se usó:** Agregar costo a SalidaVista y es_cazador a EnemigoVista, armarlos en Partida, mostrarlos en vista_consola.py y actualizar docs/CONTRATO_PARTIDA.md. El seguimiento repitió un comando sin una parte que usaba sed -i.

### 2026-11-17 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo la tarea T043 de specs/001-terreno-cazador/tasks.md. Edita únicamente DECISIONES.md (CRLF, no uses sed -i, no uses ";" en el texto nuevo) y marca T043 como [X] en tasks.md (LF). No toques código. Antes de escribir, lee: DECISIONES.md completo (para seguir su estilo y su sección "Cómo leer este documento"), el enunciado P2 §5.1, §5.2, §5.6, §6.1 y §7.1 (en docs/CONTEXTO_CRIPTA2.md o donde esté), specs/001-terreno-cazador/spec.md, plan.md y research.md, cripta/modelo/buscador_rutas.py y los resultados en docs/bench/resultados_001_a.md, _b.md, _c.md y resultados_001_antes_gc_freeze.md. Todas las cifras deben salir de esos archivos o de los datos de este prompt. No inventes ni redondees de más, y cuando uses las tres corridas reporta la mediana. Agrega al final tres secciones con la estructura de la Parte I (Problema, Alternativas consideradas, Decisión, Análisis de complejidad, Evidencia empírica, Límites conocidos). Cada una debe enlazar a specs/001-terreno-cazador/spec.md y plan.md y decir si la decisión final coincide con la del plan.md original y, si no, qué medición motivó el cambio (P2 §7.1). 1. "5.1 La ruta más barata del cazador": Dijkstra con HeapMinimo y tabla plana por id, calculado una sola vez desde la sala del jugador y compartido por todos los cazadores, con poda por el rango máximo. Alternativas: cálculo individual por cazador, búsqueda lineal del mínimo, A* y todas las parejas, con su razón de descarte según research.md. Evidencia de la carga ruta_cazador: tabla con R=600 y R=2400 y H=1, 10 y 30, más el escenario mixto, con el ciclo compartido, el individual y la razón de tiempo y de búsquedas. Explica bajo qué condiciones cambia la respuesta: con H=1 da casi igual (razón cerca de 1, porque el jugador se mueve y casi cada decisión necesita una búsqueda nueva), y la ventaja crece con H. Responde con datos la pregunta de cuántas búsquedas hacen falta (58 búsquedas para 1800 decisiones con H=30). Incluye que costo_de_conexion se lleva casi la mitad del tiempo de una búsqueda (compara "consultas de costo_de_conexion" con "búsqueda sola" en R=2400 H=1), que se mantuvo así porque el ciclo cumple, y menciona como alternativa no implementada precalcular los costos en una tabla plana al construir el mapa (O(1) frente a O(log n)). El desempate por menor id es exacto porque la tabla se calcula desde la sala del jugador. 2. "5.2 Rutas que dejan de ser válidas": invalidación selectiva por eventos (movimiento del jugador, abrir puerta, cierre automático, pergamino, carga de partida y activación de un cazador), y reutilización solo si la tabla es de la misma sala del jugador y el rango pedido no supera el calculado. Explica que la invalidación al activar cualquier cazador es conservadora, porque la activación ocurre al entrar el jugador a una sala, que ya invalida, y que el caso de rango mayor lo resuelve la comparación de rango. Evidencia de la carga invalidacion con puertas estables y con puertas que cambian, frente a recalcular siempre. 3. "5.6 Revisión de decisiones de la Parte I": la decisión que cambió fue agregar gc.freeze() al terminar cada acción del jugador (Partida.ejecutar_accion). Antes y después con docs/bench (partida 400 salas: 129.77 ms NO CUMPLE en resultados_001_antes_gc_freeze.md, frente a la mediana de las tres corridas nuevas, y el código de salida de --bench completo, que antes era 1 y ahora es 0). Causa según plan.md (Revisión de Decisiones, punto 3). Agrega estos datos medidos en el mismo equipo, con el código actual y desactivando gc.freeze solo para esa corrida, en las mismas condiciones y con otras aplicaciones abiertas: con gc.freeze la carga partida de 400 salas dio peores de cada corrida 14.91, 19.29 y 24.52 ms (mediana 19.29, CUMPLE), y sin gc.freeze 32.20, 42.79 y 51.89 ms (mediana 42.79, NO CUMPLE). Con 100 salas, sin gc.freeze apareció un pico de 33.00 ms frente a 2.58 ms con gc.freeze. El tiempo típico de una acción fue parecido en ambos casos (6.06 frente a 5.20 ms), así que el arreglo quita los picos y no cambia el trabajo. Además, un diagnóstico que registró el recolector durante el --bench completo encontró que, en la acción más lenta de cada repetición de 400 salas, el recolector usó menos de 3 ms y solo en la generación 0. Los picos aislados que quedan (por ejemplo 23.33 y 43.16 ms en una de tres repeticiones) no vienen del recolector, y su causa no se aisló. Por eso decide la mediana de los peores casos. Incluye también ciclo_referencia (cripta-06, 36 cazadores activos) como verificación de FR-TER-020 y de la agenda con la carga nueva, y las cargas agenda e historial de la Parte I repetidas. Di con honestidad que la carga historial es la misma carga sintética de la Parte I y no tiene cazadores. Límite conocido: la basura cíclica entre objetos congelados no se recupera. Además actualiza en "Cómo leer este documento" la lista de cargas (agrega ruta_cazador, invalidacion, ciclo_referencia) y en la tabla de equipos agrega estas secciones al Equipo B. En los Límites conocidos de 4.1, reemplaza el párrafo que dice que con 400 salas el peor caso no cumple por una frase que remita a la sección 5.6 nueva. Al terminar, dime qué cambiaste." (El texto completo está en prompts/p2/15-decisiones-001.md.)

**Prompt (seguimiento):** "Corrige tres cosas en DECISIONES.md, sección 5.6 y 5.1. Son errores de los datos que te pasé, no tuyos. 1. En la comparación controlada de 5.6 el tiempo típico está al revés: con gc.freeze fue 6.06 ms y sin gc.freeze fue 5.20 ms. Corrige la frase y mantén la conclusión de que el trabajo típico es parecido y el arreglo solo quita los picos. 2. En la misma comparación, el dato de 100 salas mezcla corridas. Reemplázalo por los valores de esa misma corrida controlada: con gc.freeze los peores de cada repetición fueron 2.51, 1.74 y 1.80 ms (mediana 1.80, CUMPLE) y sin gc.freeze 8.62, 2.54 y 33.00 ms (mediana 8.62, CUMPLE, con un pico de 33.00 ms en una repetición). Quita el 2.58 ms. 3. En 5.1, en el punto "Cuántas búsquedas hacen falta", presenta como interpretación y no como hecho medido que las 58 búsquedas corresponden a los ciclos en que el jugador cambió de sala, por ejemplo con "lo que es consistente con". Edita con Edit, conserva CRLF y no uses ";". Dime qué cambiaste."

**Prompt (resumido):** T043: secciones 5.1, 5.2 y 5.6 de DECISIONES.md para la ruta del cazador, la invalidación y la revisión de la Parte I.

**Para qué se usó:** Documentar las decisiones con la estructura de la Parte I y las cifras de docs/bench. El seguimiento corrigió tres datos de la comparación con y sin gc.freeze y la redacción sobre las 58 búsquedas.

### 2026-11-13 a 2026-11-17 — Claude Opus 5.5 (app de Claude)
**Prompt (resumido):** Le pedí ayuda a Claude, en varias conversaciones, para revisar contra el enunciado cada cambio de la capacidad 001 antes de cada commit y para hacer directamente en los archivos las correcciones que encontrara. No hay un único prompt textual, porque fueron muchos mensajes cortos de revisión y corrección.

**Para qué se usó:**
- Corregir los comentarios de tiempos en tests/aceptacion/test_cazador_persecucion.py (escenarios de T028c).
- Reemplazar en cripta/modelo/buscador_rutas.py una constante duplicada por COSTO_ESPERAR de cripta/constantes.py.
- Corregir el encabezado de cripta/modelo/comportamiento_enemigo.py y el aviso del cazador sin rango válido en cripta/modelo/partida.py.
- En cripta/bench/cargas_bench.py, agregar a ciclo_referencia la métrica de cazadores en persecución con un buscador aparte, y agregar "rango": None a la ficha falsa de bench_ciclo_eventos, que hacía fallar la carga ciclo.
- Reorganizar Partida.ejecutar_accion para que gc.freeze() se llame en un solo punto (T039b).
- Diagnosticar los picos de la carga partida con un script temporal que registró el recolector durante el --bench completo (no se incluyó en el repositorio) y la comparación con y sin gc.freeze que se cita en DECISIONES.md, sección 5.6.
- Renombrar docs/bench/resultados_001.md a resultados_001_antes_gc_freeze.md para conservar el antes de T039b.
- Agregar a la tarea T034c y al plan la actualización de docs/CONTRATO_PARTIDA.md.
- Actualizar el README (ejemplos de --replay, lista de cargas de --solo y nota del código de salida de --bench) y marcar en tasks.md T034b, T039, T039b, T040, T041 y T042.
- Quitar varios ";" de comentarios y docstrings y corregir referencias a requisitos e imports en archivos de prueba.
 

### 2026-11-14 — Codex CLI 0.167.2 (GPT-6-Luna)
**Prompt:**
```text
$speckit-specify
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Contexto: ya estoy en la rama 002-niebla-ir-a. No crees ni cambies de rama y no hagas commit ni push. Redacta todo en español, incluidas las etiquetas de la plantilla (Dado, Cuando, Entonces). Solo crea o modifica archivos dentro de specs/002-niebla-ir-a/ y .specify/feature.json. No ejecutes clarify ni plan. Puedes LEER (sin modificar) .specify/memory/constitution.md, docs/MAPA_CODIGO.md, specs/001-terreno-cazador/spec.md y docs/enunciados/Parte2.md (§3.3, §3.4, §5.3 y Apéndice B) para mantener coherencia con los costos de salida y con la bitácora de partida. Ante cualquier duda gana el enunciado. No inventes reglas, cifras ni límites que no estén en el enunciado: si falta una regla, anótala en Supuestos como decisión del grupo o detente y pregunta.

Capacidad: niebla de guerra y viaje automático "ir a".

Para el jugador cada sala está en uno de tres estados: EXPLORADA (entró al menos una vez; la inicial lo está desde t=0; conoce nombre, salidas, costo de cada salida y estado de sus puertas según la última observación), AVISTADA (no explorada pero destino de una salida de una sala explorada; solo sabe que existe una sala detrás), DESCONOCIDA (nada).
Memoria de puertas: el jugador observa una puerta cuando está en cualquiera de las dos salas que conecta; el mapa recuerda el estado de su última observación aunque haya cambiado después.
Antorcha: mientras esté encendida, al entrar a una sala quedan exploradas también todas sus vecinas por cualquier salida, abierta o cerrada; se revela nombre y salidas, no contenido; no se activan sus enemigos ni trampas.
Todo lo que la vista muestra y lo que usa "ir a" se deriva solo del conocimiento del jugador. El conocimiento es estado del juego: se guarda, se revierte con el pergamino y entra en la línea de tiempo. La interfaz ofrece un comando para ver el mapa conocido (explorada, salidas, avistadas).

"ir a <sala>": lleva al jugador a una sala EXPLORADA mediante movimientos ordinarios. Ruta con el conocimiento del jugador (solo salas exploradas, solo salidas recordadas abiertas), mínimo costo, desempate por primer paso hacia la vecina de menor id. Cada paso es una acción completa del jugador que consume tiempo (costos P2 §3.1) y deja correr los eventos. La ruta se recalcula antes de cada paso. Se detiene si: llega; entra a sala con enemigos (activos o dormidos); recibe daño; o deja de haber ruta conocida. No abre puertas aunque tenga la llave. En partida.log cada paso se registra como movimiento individual y la orden se registra además como comentario. El pergamino revierte solo el último paso.
El usuario debe poder ver por qué se detuvo el viaje.
Rendimiento: un paso de "ir a" < 5 ms con el mapa conocido completo de la cripta de referencia.

Escenarios del Apéndice B (cada uno debe ser un escenario de aceptación):
- ir a sala no explorada: se rechaza, no consume tiempo
- el mapa recuerda abierta una puerta realmente cerrada: al observarla se actualiza y se recalcula; si no hay ruta, el viaje se detiene sin consumir tiempo adicional
- ir a entra a sala con enemigos dormidos: se activan (P1 §2.4) y el viaje se detiene
- con antorcha encendida, entrar explora vecinas sin activar enemigos ni trampas
- un pergamino revierte una entrada con antorcha: las salas exploradas por la antorcha vuelven al estado anterior
- un pergamino durante un viaje: revierte solo el último paso y el viaje no continúa

Prefijo de requisitos: FR-NIE-NNN. spec.md dice qué y por qué: sin estructuras de datos, clases, módulos ni archivos de código.
```

**Prompt (resumido):** Se pidió generar la especificación de la capacidad de niebla de guerra e «ir a»: tres estados de sala (explorada, avistada, desconocida), memoria de puertas, efecto de la antorcha, conocimiento como estado del juego (se guarda, se revierte con el pergamino y entra en la línea de tiempo), comando para ver el mapa conocido, viaje automático con sus condiciones de parada y registro en partida.log, y los seis escenarios del Apéndice B como escenarios de aceptación, con prefijo FR-NIE-NNN y sin estructuras, clases ni módulos.

**Para qué se usó:** Generar spec.md y sus artefactos asociados de la capacidad 002 en la rama 002-niebla-ir-a, para revisarlos contra el enunciado antes de ejecutar clarify.


### 2026-11-14 — Claude (Sonnet 5.5, claude.ai)
**Prompt:**
```text
Revisa la especificación generada con spec-kit para la capacidad 002 (niebla de guerra e «ir a») y su lista de calidad (se adjuntaron spec.md y checklists/requirements.md). Contrástalas con el enunciado de la Parte II (§3.3, §3.4, §5.3, §6.1 y Apéndice B) y con la constitución, indica si necesitan cambios antes de ejecutar clarify y redacta el prompt de clarify.
```

**Prompt (resumido):** Se pidió revisar la especificación de niebla de guerra e «ir a» contra el enunciado y la constitución, decidir si requería correcciones antes de la aclaración y preparar el prompt de clarify.

**Para qué se usó:** Comprobar que la especificación cubriera los seis casos del Apéndice B sin reglas inventadas. Se concluyó que no requiere correcciones y se identificaron seis ambigüedades para resolver en clarify.

### 2026-11-14 — Codex CLI 0.169.0 (GPT-6-Luna)
**Prompt:**
```text
$speckit-clarify
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Contexto: ya estoy en la rama 002-niebla-ir-a. No crees ni cambies de rama y no hagas commit ni push. Redacta todo en español. Solo modifica specs/002-niebla-ir-a/spec.md. No modifiques checklists/requirements.md y no ejecutes plan. Puedes LEER (sin modificar) docs/enunciados/Parte2.md (§3.3, §3.4, §5.3, §6.1 y Apéndice B), .specify/memory/constitution.md y specs/001-terreno-cazador/spec.md (solo FR-TER-021 y FR-TER-023, por coherencia con el registro de partida.log). Si la respuesta a una duda ya está en el enunciado, no la preguntes: cítala y aplícala. No inventes reglas: lo que no esté en el enunciado queda como decisión del grupo, escrita en Supuestos.

PASO 1. No hay correcciones directas a spec.md.

PASO 2. Formula como máximo estas 5 preguntas, de una en una, cada una con tu recomendación, y actualiza spec.md con cada respuesta en la sección "Aclaraciones", subsección "Sesión 2026-11-14", con el formato "- P: ... → R: ...". Propaga cada respuesta a los requisitos, escenarios y casos límite afectados. Conserva los identificadores existentes; los requisitos y criterios nuevos van al final de su lista con la numeración siguiente, sin renumerar. No nombres estructuras, clases ni módulos.
a) Salas exploradas solo por la antorcha: se revelan nombre y salidas, pero las puertas que no conectan con la sala donde entró el jugador nunca se han observado. ¿Qué recuerda el mapa de esas puertas y puede «ir a» cruzarlas? (FR-NIE-005, FR-NIE-010)
b) Motivos de detención: si coinciden varios en un mismo paso (por ejemplo, llegar al destino con enemigos o recibir daño al entrar), ¿se informa uno con orden de prioridad o todos? ¿Un enemigo muerto cuenta como enemigo en la sala? ¿Cuándo se evalúa el daño? El escenario 6 de la historia 3 dice "cuando termina de resolverse ese paso y sus eventos", pero el enunciado solo dice "recibe daño".
c) Órdenes degeneradas: destino igual a la sala actual, destino que no existe en la cripta y viaje que se inicia estando ya en una sala con enemigos. ¿Se rechazan o se ejecutan, y consumen tiempo?
d) Tiempo y registro: ¿el comando de ver el mapa conocido consume tiempo, se registra en partida.log o altera el historial de retroceso? Una orden «ir a» rechazada o que no llega a dar ningún paso, ¿deja su comentario en partida.log? Debe ser coherente con la regla de la 001 de que las acciones rechazadas no se registran.
e) Antorcha: si el jugador la enciende estando ya dentro de una sala, ¿explora las vecinas en ese momento o solo en la siguiente entrada? Si se apaga, ¿lo ya explorado se conserva? Al revertir con pergamino una entrada con antorcha, ¿se revierten también las observaciones de puertas hechas en esa entrada?

Al terminar, muestra un resumen breve de lo cambiado.
```

**Prompt (resumido):** Se pidió resolver, con un máximo de cinco preguntas de una en una y cada una con recomendación, las ambigüedades de la especificación de niebla de guerra e «ir a»: puertas de salas exploradas solo con antorcha, motivos de detención simultáneos, órdenes degeneradas, registro y consumo de tiempo del mapa y de la orden, y comportamiento de la antorcha y del pergamino.

**Para qué se usó:** Dejar la especificación sin ambigüedades en las reglas observables antes de pasar al plan.

### 2026-11-14 — Claude (Sonnet 5.5, claude.ai)
**Prompt:**
```text
Revisa la especificación de la capacidad 002 tras la sesión de aclaración (se adjuntaron la transcripción de la sesión y el spec.md actualizado) y dime si necesita correcciones antes del commit. Después redacta el prompt de plan.
```

**Prompt (resumido):** Se pidió revisar la especificación aclarada de niebla de guerra e «ir a» contra el enunciado, decidir si requería correcciones y preparar el prompt del plan.

**Para qué se usó:** Detectar dos viñetas de casos límite con negaciones incompletas que invertían el sentido, registrar en Supuestos las decisiones del grupo derivadas de la aclaración y añadir el aviso de motivo en los rechazos.

### 2026-11-14 — Codex CLI 0.169.0 (GPT-6-Luna)
**Prompt:**
```text
$speckit-plan
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Contexto: ya estoy en la rama 002-niebla-ir-a. No crees ni cambies de rama y no hagas commit ni push. Redacta todo en español. Solo crea o modifica archivos dentro de specs/002-niebla-ir-a/. No modifiques spec.md ni checklists/requirements.md y no ejecutes tasks. Puedes LEER (sin modificar) docs/MAPA_CODIGO.md, specs/001-terreno-cazador/ (plan.md, spec.md y contracts/), docs/enunciados/Parte2.md (§3.3, §3.4, §5.3, §5.5 y §6.1) y el código de cripta/ para citar rutas reales. Cita solo archivos que existan en esta rama y verifícalo. Lo que la capacidad 001 prevé pero aún no está en esta rama (por ejemplo su búsqueda de rutas del cazador) se cita desde specs/001-terreno-cazador/plan.md como "previsto por la 001", nunca como código existente. Si falta una regla, detente y pregunta.

Restricciones obligatorias (constitución): implementar a mano las estructuras; PROHIBIDO heapq, bisect, collections, networkx, set y dict como índice, caché o tabla de búsqueda, y list.sort()/sorted() donde aplique. Permitido list como almacenamiento contiguo indexado por posición entera. Reutiliza estructuras de la Parte I cuando sean adecuadas y cita el archivo. Clases, métodos y atributos nuevos en español. Errores de programación heredan de IndexError o ValueError; CriptaError solo para fallos externos. El modelo no importa red ni archivos; --replay y --bench no instancian la vista. Ningún dato de una cripta concreta en el código.

El plan debe incluir:
1. Problema y operaciones reales con su frecuencia esperada.
2. Al menos DOS alternativas por problema y la razón concreta de descarte de cada una.
3. Decisión (estructura y estrategia) y complejidad de las operaciones más frecuentes.
4. Impacto en código existente: archivo por archivo (ruta real) marcado como Nuevo, Modificado o Sin cambios.
5. Mediciones --bench previstas, incluida la de la alternativa descartada, con el comando exacto para reproducirlas. Toda cifra es hipótesis hasta medirla.
6. Límites conocidos de la decisión.
7. Revisión de decisiones de la Parte I que esta carga pueda invalidar.
8. Trazabilidad: tabla FR-NIE -> componente -> medición/prueba. Incluye FR-NIE-001 a FR-NIE-024, SC-NIE-001 a SC-NIE-005 y los casos del Apéndice B.
No agregues reglas del juego que no estén en spec.md.

Aspectos que el plan debe resolver:
- Representación del conocimiento del jugador: estado por sala (explorada, avistada, desconocida) y estado recordado por puerta (abierta, cerrada, no observada), con consultas baratas por sala y por puerta, sin dict, set ni bisect.
- Costo de explorar proporcional a las salas reveladas y no al tamaño del mapa conocido (P2 §5.3), incluida la exploración por antorcha.
- Cómo registrar e invertir los cambios del conocimiento con el pergamino sin copiar el mapa completo por acción, reutilizando el historial reversible de la Parte I (cita los archivos reales).
- Declarar explícitamente qué estado nuevo debe guardarse en la partida. La capacidad 004 es dueña del formato binario: este plan no define el formato.
- Ruta de «ir a» sobre el subgrafo conocido: justificar con mediciones si comparte implementación con la búsqueda del cazador prevista por la 001 o si conviene separarla (P2 §5.3). Recálculo antes de cada paso y desempate por menor identificador.
- Dónde vive el bucle del viaje respetando MVC: el modelo no conoce la interfaz, y la vista solo muestra el motivo de detención. Registro en partida.log: comentario una sola vez antes del primer movimiento, y coherencia con la regla de la 001 de que los turnos de enemigos no se registran.
- Cuándo se actualiza la observación de puertas, incluidos los cierres automáticos mientras el jugador está en una sala vecina.
- Medición de la cota de 5 ms por paso con el mapa conocido completo de la cripta de referencia, y alternativa descartada implementada y medida con una carga sintética determinista por semilla.
- Compatibilidad con las pruebas de la Parte I.

Al terminar, muestra un resumen breve de los archivos creados.
```

**Prompt (resumido):** Se pidió generar el plan técnico de la capacidad de niebla de guerra e «ir a», con problema, al menos dos alternativas por decisión, complejidad, impacto archivo por archivo, mediciones con --bench y trazabilidad, citando solo código existente en la rama y declarando el estado nuevo a guardar.

**Para qué se usó:** Generar plan.md y sus artefactos asociados de la capacidad 002, para revisarlos antes de pasar a las tareas.

### 2026-11-15 — Claude (Sonnet 5.5, claude.ai)
**Prompt:**
```text
Revisa el plan generado con spec-kit para la capacidad 002 (se adjuntaron la transcripción de la sesión, plan.md, research.md, data-model.md, quickstart.md y el contrato) y dime si necesita cambios antes de las tareas. Después redacta el prompt de tasks.
```

**Prompt (resumido):** Se pidió revisar el plan de niebla de guerra e «ir a» contra el código existente y la constitución, indicar las correcciones necesarias y preparar el prompt de tareas.

**Para qué se usó:** Verificar rutas y símbolos citados en el plan, detectar que la búsqueda de rutas de la 001 no es reutilizable sin modificarla, que el formato del comentario del registro y el mecanismo del pergamino durante el viaje no estaban definidos, y que la verificación de guardado depende de una capacidad sin especificar.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6-Luna)
**Prompt:**
```text
$speckit-tasks
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Contexto: ya estoy en la rama 002-niebla-ir-a. No crees ni cambies de rama y no hagas commit ni push. Redacta todo en español, incluidos los títulos de las fases y secciones de la plantilla. Solo crea o modifica specs/002-niebla-ir-a/tasks.md. Usa solo spec.md, plan.md, research.md, data-model.md, quickstart.md y contracts/ de esa carpeta, y puedes LEER (sin modificar) el código de cripta/ y tests/ para citar rutas reales. No agregues reglas del juego ni decisiones de diseño que no estén en esos documentos. Si falta algo, detente y pregunta.

Reglas de la constitución que las tareas deben cumplir:
- Cada tarea cita los identificadores FR-NIE-NNN que atiende, la ruta real del archivo que toca (marca "Nuevo" o "Modificado" según exista en esta rama, comprobándolo), el comando de prueba que la valida y su criterio de "hecho". Máximo unos 90 minutos por tarea y ninguna tarea sin requisito.
- Cada escenario de aceptación de spec.md, incluidos los seis casos del Apéndice B, y cada SC-NIE-001 a SC-NIE-005 tiene al menos una tarea de prueba automatizada con unittest que cita el requisito. Las pruebas van antes que el código que las hace pasar. Las carpetas de pruebas nuevas, como tests/aceptacion, llevan su __init__.py en una tarea explícita.
- Ninguna tarea usa heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Se reutilizan las estructuras propias citadas en plan.md y list solo como almacenamiento contiguo indexado por entero.
- Los errores de programación heredan de IndexError o ValueError; CriptaError solo para fallos externos.
- El modelo no importa red, archivos ni vista. --replay y --bench no instancian la vista.
- Ninguna tarea contiene commits ni push, ni códigos de tarea ni nombres de personas en mensajes de commit.
- Ninguna tarea escribe cifras de rendimiento antes de medirlas. La cripta de referencia se elige por el mayor total de salas del listado de fixtures, sin fijar su id en el código.
- Las tareas que necesitan código que aún no está en esta rama llevan la etiqueta "Depende de 001" (costo de salida en el movimiento de partida.py y los métodos esta_vacio y __len__ de HeapMinimo) o "Depende de 004" (codificación binaria del guardado) y no se redactan como si ese código ya existiera.

Organización obligatoria:
1. Fase A, dominio puro del conocimiento: pruebas primero y luego cripta/modelo/conocimiento_jugador.py (estados de sala, observaciones de puerta, revelación, antorcha, inversas por celda).
2. Fase B, integración con la partida: entradas a salas, antorcha, observación de cierres automáticos desde una sala vecina, retroceso con pergamino y proyección lógica del conocimiento en EstadoPartida, sin codificación binaria.
3. Fase C, ruta y viaje: cripta/modelo/ruta_conocida.py (búsqueda propia con HeapMinimo, desempate por menor id), bucle del viaje en el controlador, motivos de detención en orden fijo y cancelación del viaje por cualquier otra acción entre pasos.
4. Fase D, registro y vista: comentario con # en partida.log (registro, lector y replay), comando de mapa conocido y motivo de detención en la vista.
5. Fase E, mediciones --bench: carga niebla_rutas con la alternativa de selección lineal y las mediciones de revelación y reversión, cada tarea con el comando exacto.
6. Fase F, cierre: pruebas de la Parte I en OK, auditoría de importaciones prohibidas, verificación del guardado marcada como bloqueada por la decisión sobre la 004, y una tarea final "Sección de DECISIONES.md".

Marca [P] solo las tareas que tocan archivos distintos y no dependen entre sí. Indica el orden de dependencias entre fases y el punto de corte del Pull Request, que no puede fusionarse antes del de la 001. El registro de este comando en PROMPTS_LLM.md se hace fuera de las tareas.
```

**Prompt (resumido):** Se pidió generar la lista de tareas de la capacidad de niebla de guerra e «ir a», con pruebas antes que el código, cada tarea ligada a sus requisitos, las dependencias externas de las capacidades 001 y 004 marcadas, y el punto de corte del Pull Request.

**Para qué se usó:** Generar tasks.md para revisarlo antes de ejecutar analyze.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6-Luna)
**Prompt:** Corrige solo specs/002-niebla-ir-a/tasks.md. No toques ningún otro archivo, no crees ni cambies de rama y no hagas commit ni push. Respeta los finales de línea del archivo y no uses sed -i. Conserva el formato de las tareas; renumera solo lo necesario y actualiza las dependencias y la sección "Cobertura independiente". Comprueba con Test-Path (solo lectura) cada ruta que cites.

1. T028: la ruta es DECISIONES.md en la raíz (Modificado), no docs/DECISIONES.md. Agrega la sección de esta capacidad.
2. Agrega tareas de prueba (antes del código) y de código para:
   a. cripta/modelo/efectos.py (Modificado): avisar al conocimiento los cierres automáticos observables desde una sala vecina (FR-NIE-004, FR-NIE-015; B-NIE-002).
   b. cripta/modelo/resultado_partida.py (Modificado): proyección inmutable del mapa y resultado y motivos del viaje (FR-NIE-007, FR-NIE-008, FR-NIE-013).
   c. cripta/vista/vista_base.py (Modificado): contrato de presentación del mapa conocido y de la detención, antes de T020.
   d. cripta/infraestructura/estado_guardado.py (Modificado, coordinar con 004) para el campo lógico del conocimiento y cripta/modelo/persistencia_modelo.py (Modificado) para proyectarlo y restaurarlo, sin codificación binaria. Corrige T008: EstadoPartida está en estado_guardado.py.
3. Pon T011 antes de T008 y valida T008 con tests.servicios.test_servicio_partida_guardado.
4. Pon T016 antes de T015.
5. Valida T022 con tests.servicios.test_servicio_bench; el comando de --bench queda en T023. Divide T022 en tres tareas: selección lineal, revelación y reversión, cada una con su criterio de hecho.
6. T024: quita tasks.md como ruta de evidencia; no modifica archivos y sus resultados se llevan a la sección de DECISIONES.md.
7. En T002, T003, T004 y T006 la ruta tests/modelo/test_conocimiento_jugador.py pasa a "Modificado"; solo T001 es "Nuevo".
8. Divide T010: B-NIE-004 y B-NIE-005 quedan en la Fase B; B-NIE-001, B-NIE-002, B-NIE-003 y B-NIE-006 pasan a la Fase C, antes del bucle del controlador. tests/aceptacion/test_niebla_ir_a.py es Nuevo en la primera y Modificado en la segunda.
9. T001 cita también los escenarios 1.3 y 1.4. T014 agrega el caso en que el daño mata al jugador (FR-NIE-013: se aplican las reglas de fin de partida y no se informa viaje) y las aserciones de cero tiempo, sin línea en partida.log y sin cambio en el historial para destino no explorado, destino igual a la sala actual y falta de ruta inicial (escenarios 3.1, 3.12, 3.14; FR-NIE-009, 019, 021). T019 agrega o remite a una prueba de que consultar el mapa no consume tiempo ni se registra (FR-NIE-007).
10. Agrega la etiqueta "Depende de 001" (costo de salida en el movimiento de partida.py) a T014 y T015.
11. Corrige la nota de paralelismo para que coincida con las tareas marcadas [P].
12. T026: agrega un comando de solo lectura que verifique que cripta/modelo no importa red, archivos ni vista, y otro que verifique que servicio_replay.py y servicio_bench.py no instancian la vista. Aclara que la búsqueda de set/dict puede traer falsos positivos en comentarios y que se revisan a mano.
13. En los criterios de T005 y T013 agrega que los errores de programación heredan de IndexError o ValueError.
Al terminar, dime qué cambiaste por punto y cuántas tareas quedaron.

**Prompt (resumido):** Se pidió corregir tasks.md de la capacidad 002: rutas, archivos del plan sin tarea, orden de pruebas y código, tareas demasiado grandes y cobertura de escenarios.

**Para qué se usó:** Ajustar la lista de tareas al plan, a la especificación y al estado real del repositorio antes de /speckit-analyze.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo specs/002-niebla-ir-a/tasks.md: coloca la proyección de resultado_partida.py antes del bucle del controlador; agrega la tarea de código de vista_base.py, las pruebas de revelación y reversión del benchmark y el comando de consulta del mapa en el controlador; explicita el punto de corte del Pull Request; reubica T015 y T023 bajo su objetivo; quita las marcas [P] que comparten archivo; fusiona las pruebas duplicadas; corrige T021 a Modificado; deja la medición sin escribir archivos y la sección de DECISIONES.md solo en la tarea final; divide la prueba del ciclo de viaje y ordena el formato."

**Prompt (resumido):** Se pidió una segunda corrección de tasks.md de la capacidad 002: orden de pruebas y código, tarea faltante de vista_base.py, pruebas del benchmark, comando de mapa, punto de corte del Pull Request y formato.

**Para qué se usó:** Dejar tasks.md consistente con el plan y con la regla de pruebas antes del código antes de /speckit-analyze.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo specs/002-niebla-ir-a/tasks.md: renumera las tareas de forma consecutiva, corrige qué prueba del harness es Nueva y cuál Modificada en tests/servicios/test_servicio_bench.py y agrega las líneas en blanco entre encabezados y objetivos."

**Prompt (resumido):** Se pidió una tercera corrección mecánica de tasks.md de la capacidad 002: numeración, estado de una ruta de pruebas y formato.

**Para qué se usó:** Dejar tasks.md consecutivo y consistente con el estado real del repositorio antes de /speckit-analyze.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "/speckit-analyze Sigue las instrucciones de prompts/p2/06-analyze-002.md. Analiza la consistencia entre spec.md, plan.md, research.md, data-model.md, quickstart.md, contracts/, tasks.md y la constitución, en solo lectura: cobertura de FR-NIE-001 a 024, de los escenarios, de los seis casos del Apéndice B y de SC-NIE-001 a 005; estructuras prohibidas; afirmaciones de rendimiento; rutas Nuevo y Modificado; orden de pruebas y código; etiquetas de dependencia con 001 y 004; contradicciones entre plan, quickstart, contrato y modelo de datos. Clasifica los hallazgos por gravedad con archivo y línea."

**Prompt (resumido):** Análisis de solo lectura de la consistencia de la capacidad de niebla de guerra e «ir a» entre especificación, plan, tareas y constitución.

**Para qué se usó:** Correciones al plan y tasks entregadas desde speckit.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "$speckit-analyze Sigue las instrucciones de prompts/p2/06-analyze-002.md. Solo lectura: no modifiques ningún archivo. Responde en español, con una tabla de hallazgos por gravedad con archivo y línea, y una lista de requisitos y escenarios sin cobertura."

**Prompt (resumido):** Análisis de solo lectura de la consistencia de la capacidad de niebla de guerra e «ir a» entre especificación, plan, tareas y constitución.

**Para qué se usó:** Detectó que SC-NIE-001, SC-NIE-003 y SC-NIE-005 no estaban citados por tareas de prueba, el nombre ambiguo de la prueba de equivalencia y la falta de salvedad de estimaciones en el plan. Su hallazgo sobre una prueba automatizada del umbral de 5 ms no se adoptó, porque el rendimiento se respalda con --bench.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo plan.md y tasks.md de la capacidad 002: agrega tests/vista/test_vista_consola.py y tests/servicios/test_servicio_bench.py a la tabla de impacto, el árbol y la trazabilidad del plan; marca las complejidades y el objetivo de 5 ms como estimaciones; redacta la cancelación del viaje como cancelación por pergamino; en las tareas, cita SC-NIE-001, 002, 003 y 005 en las pruebas, aclara que T034 valida FR-NIE-018 con --bench y renombra la prueba de equivalencia."

**Prompt (resumido):** Se pidió corregir los hallazgos de /speckit-analyze y dos incoherencias detectadas en la revisión: archivos de pruebas ausentes del plan y una regla de cancelación que la especificación no fija.

**Para qué se usó:** Alinear plan.md y tasks.md con la especificación antes del Pull Request de documentación.

### 2026-11-15 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "/speckit-analyze Sigue las instrucciones de prompts/p2/06-analyze-002.md. Solo lectura: no modifiques ningún archivo. Responde en español, con una tabla de hallazgos por gravedad con archivo y línea, y una lista de requisitos y escenarios sin cobertura."

**Prompt (resumido):** Segunda ejecución del análisis de solo lectura de la capacidad de niebla de guerra e «ir a» después de las correcciones del primer análisis.

**Para qué se usó:** Confirmó que los 24 requisitos, los escenarios y los seis casos del Apéndice B tienen tarea de prueba. Señaló la falta de claridad sobre cómo se usa el pergamino durante el viaje, que se resolvió con una aclaración del plan sin cambiar la especificación, y dos observaciones menores de etiquetas. La pendiente de guardado binario sigue bloqueada por la 004.

### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo archivos dentro de specs/002-niebla-ir-a/: FR-NIE-002 (explorada incluye la antorcha), una salida sin puerta cerrable se conoce abierta al revelarse, la 004 es dueña del formato binario y de su versión (tarea de guardado como «Depende de 004»), costos de salida en listas propias, cita del Apéndice B, coordinación con las vistas de la 001 y renumeración de tareas."

**Prompt (resumido):** Aplicar la revisión del Pull Request de la capacidad 002 a la especificación, el plan y las tareas.

**Para qué se usó:** Incorporar las correcciones de la revisión del PR antes de fusionar el PR de documentación.


### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo tasks.md y plan.md de la capacidad 002: referencia de la tarea que depende de 004, citar el escenario 3.18 en lugar de B-NIE-007, criterio de hecho de la implementación de vistas, etiqueta de dependencia con 001 y ubicar la comparación de costos guardados en la prueba y la carga del harness."

**Prompt (resumido):** Segunda corrección de tasks.md de la 002 tras la revisión del Pull Request: referencias, etiquetas y ubicación de la comparación de costos.

**Para qué se usó:** Dejar las tareas consistentes con la spec y el plan antes de fusionar el PR de documentación.

### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo archivos dentro de specs/004-linea-de-tiempo/: el uso del pergamino no es una acción numerada (spec primero); relación entre la línea vigente y partida.log; fuente del contenido de salas en la reconstrucción aislada; problema de pasar t al número de acción; registro de retroceso pausado; proyección compartida entre historia y replay; borde del recorte; tratamiento de lo no reversible; coordinación de archivos compartidos; --hasta solo con --replay; un solo cambio de versión del formato por esta capacidad con el conocimiento de la 002 en los checkpoints, incluidos los costos de salida; vistas de la 001. [...]"

**Prompt (resumido):** Corregir huecos de diseño del plan de la línea de tiempo y una aclaración de la especificación sobre el pergamino, con la coordinación de las capacidades 001 y 002.

**Para qué se usó:** Dejar el plan y sus artefactos consistentes con partida.log, el pergamino y la versión final de la 002.

### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo archivos dentro de specs/004-linea-de-tiempo/: numeración tras el pergamino (el número de una acción revertida se reutiliza), mecanismo de ajuste de inventario por el pergamino, replay completo con pergamino, fuente del contenido al reconstruir sin precarga, definición del punto de control, búsqueda binaria de t a número de acción y corrección de una fila del pergamino. [...]"

**Prompt (resumido):** Segunda corrección de la especificación y el plan de la línea de tiempo tras la revisión: numeración, estado vivo tras el pergamino, replay y reconstrucción sin E/S por consulta.

**Para qué se usó:** Cerrar las contradicciones de numeración y los huecos de diseño detectados antes de generar las tareas.


### 2026-11-10 — Antigravity CLI 1.5.4 (Gemini 3.8 Flash)
**Prompt:**
```text
/speckit-specify
SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad
Contexto: ya estoy en la rama 003-resolubilidad. No crees ni cambies de rama y no hagas commit. Redacta todo en español. Solo crea o modifica archivos dentro de specs/003-resolubilidad/ y .specify/feature.json. No ejecutes clarify.

Capacidad: verificación de resolubilidad de una cripta antes de jugar.

Supuestos: el jugador atraviesa cualquier salida abierta y cualquier cerrada cuya llave ya obtuvo;
las llaves no se consumen; todo enemigo puede derrotarse; una llave que suelta un enemigo se
considera obtenible en la sala donde ese enemigo inicia (incluye enemigos errantes); trampas y
cierres automáticos no bloquean.
Resoluble: partiendo de la sala inicial, el jugador puede obtener la llave de salida y llegar a la
sala de salida a través de una puerta que la requiere.
Resultado si es resoluble: un orden de obtención de llaves donde cada llave aparece después de
todas las necesarias para alcanzarla; determinista (dos ejecuciones, mismo orden).
Resultado si no lo es: llaves que no pueden obtenerse; puertas de la frontera bloqueada (cerradas,
adyacentes a la región alcanzable) con la llave que exige cada una; dónde está cada una de esas
llaves; y, si una llave está tras puertas que solo ella abre (directamente o por cadena), el ciclo
concreto de dependencia.
Sin --forzar, una cripta no resoluble no inicia y se muestra el reporte. --verificar <cripta> ejecuta
solo la verificación, sin vista. El reporte se muestra al iniciar una partida.
Usa los datos del esqueleto y la ubicación de llaves del servicio (nueva consulta que cuenta
dentro del presupuesto de solicitudes y puede persistirse con la versión de la cripta).
Rendimiento: < 200 ms en la cripta publicada más grande; costo total aproximadamente lineal en
salas, salidas y llaves; el reporte sale del mismo recorrido (sin recorridos adicionales por llave).

Escenarios del Apéndice B:
- llave de salida tras la única puerta que ella misma abre: no resoluble; el reporte señala el ciclo
- llave en el campo suelta de un enemigo errante: se ubica en la sala inicial del enemigo
- varios órdenes válidos: dos ejecuciones producen el mismo orden
- cripta no resoluble sin --forzar: la partida no inicia y se muestra el reporte

Prefijo: FR-RES-NNN. Sin estructuras, clases ni módulos.
```

**Prompt (resumido):** Se pidió generar la especificación de la capacidad de resolubilidad con sus supuestos, resultados esperados, banderas, rendimiento y los cuatro escenarios del enunciado, sin detalles de implementación.

**Para qué se usó:** Generar el borrador de specs/003-resolubilidad/spec.md y su lista de control, que luego se revisa y se corrige en la fase de aclaraciones.

### 2026-11-10 — Antigravity CLI 1.5.4 (Gemini 3.8 Flash)
**Prompt:**
```text
/speckit-clarify
SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad
Contexto: ya estoy en la rama 003-resolubilidad. No crees ni cambies de rama y no hagas commit. Redacta todo en español. Solo modifica archivos dentro de specs/003-resolubilidad/. No leas otros archivos del repositorio, no modifiques checklists/requirements.md y no ejecutes plan.

PASO 1. Antes de hacer preguntas, aplica estas correcciones directas a spec.md sin preguntar. Conserva los identificadores existentes; los requisitos y criterios nuevos van al final de su lista con la numeración siguiente, sin renumerar.
1. Idioma: traduce al español todos los encabezados y etiquetas de la plantilla (Rama de la funcionalidad, Creado, Estado, Entrada, Escenarios de usuario y pruebas, Historia de usuario, Prioridad, Por qué esta prioridad, Prueba independiente, Escenarios de aceptación, Dado/Cuando/Entonces, Casos límite, Requisitos funcionales, Entidades clave, Criterios de éxito, Resultados medibles, Supuestos). Conserva FR-RES-NNN y SC-NNN.
2. En FR-RES-005 y en la historia de usuario 5, sustituye "estáticos" por "cualquier enemigo" (los tipos reales son errantes, rastreadores y cazadores).
3. FR-RES-017: no definas la consulta de llaves, su DTO ni su caché por versión; di que la 003 usa el contrato de datos de la capacidad 001 (specs/001-terreno-cazador/contracts/contrato_datos_p2.md), sin escribir la ruta del endpoint. En SC-006, sustituye "como máximo una unidad del presupuesto" por "una solicitud, más los reintentos por 429 si los hay".
4. En la entidad Salida/Puerta elimina la mención a salidas unidireccionales: en este proyecto toda salida conecta dos salas.
5. Puertas declaradas en un solo lado: una conexión está cerrada si cualquiera de sus dos lados lo declara, y la llave exigida es la declarada en cualquiera de los dos lados. Añádelo como requisito.
6. En FR-RES-010 sustituye "región actualmente alcanzable" por "región alcanzable final" (después de usar todas las llaves obtenibles).
7. Determinismo: añade que el ciclo reportado, el orden de las llaves, el de las puertas de la frontera y el de los ciclos son deterministas (misma cripta, mismo reporte), con desempate por menor identificador en orden ascendente.
8. Añade un requisito y un criterio de éxito: --bench compara el recorrido incremental contra la alternativa ingenua de repetir el recorrido por cada llave, con criptas sintéticas de muchas llaves encadenadas, deterministas por semilla. Sin decir cómo se implementa.
9. Añade un caso límite con escenario: llegar a la sala de salida por una puerta abierta no cuenta; hay que entrar por una puerta que exige llave_salida.
10. Añade un requisito: si el esqueleto trae costos contradictorios en una misma conexión, --verificar informa el error de datos inválidos y termina, sin reporte de resolubilidad.

PASO 2. Después formula como máximo estas 4 preguntas, de una en una, cada una con tu recomendación, y actualiza spec.md con cada respuesta:
a) ¿El orden de obtención incluye todas las llaves obtenibles o solo las necesarias para llegar a llave_salida?
b) Cuando hay varios ciclos de dependencia, ¿el reporte muestra uno o todos? (reconcilia FR-RES-012 con el caso límite de varios ciclos).
c) Datos incoherentes: una puerta cerrada sin llave, ¿es infranqueable o dato inválido? Una llave exigida por una puerta que no aparece en la consulta de llaves, ¿se reporta como "llave sin ubicación"?
d) Presupuesto de solicitudes: --verificar necesita datos generales, páginas del esqueleto y llaves, y todo cuenta. ¿Se aplica el presupuesto igual que en una partida y qué hace el sistema si se agota (con o sin datos de llaves persistidos)?

Al terminar, muestra un resumen breve de lo cambiado.
```

**Prompt (resumido):** Se pidió corregir la redacción de la especificación según la revisión hecha con apoyo de Claude y resolver las ambigüedades restantes con un máximo de cuatro preguntas, cada una con una recomendación.

**Para qué se usó:** Dejar la especificación en español, coherente con el contrato de datos de la capacidad de terreno y cazador y sin ambigüedades antes de pasar al plan.


### 2026-11-11 — Antigravity CLI 1.5.4 (Gemini 3.8 Flash)
**Prompt:**
```text
/speckit-plan
SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad
Contexto: ya estoy en la rama 003-resolubilidad. No crees ni cambies de rama y no hagas commit. Redacta todo en español. Solo crea o modifica archivos dentro de specs/003-resolubilidad/. No modifiques spec.md ni checklists/requirements.md y no ejecutes tasks. Puedes LEER (sin modificar) docs/MAPA_CODIGO.md, specs/001-terreno-cazador/ (plan.md, tasks.md y contracts/contrato_datos_p2.md) y el código de cripta/ para citar rutas reales.

Restricciones obligatorias (constitución): implementar a mano las estructuras; PROHIBIDO heapq, bisect, collections, networkx, set y dict como índice, caché o tabla de búsqueda, y list.sort()/sorted() donde aplique. Permitido list como almacenamiento contiguo indexado por posición entera. Reutiliza estructuras de la Parte I cuando sean adecuadas y cita el archivo. Clases, métodos y atributos nuevos en español. Errores de programación heredan de IndexError o ValueError; CriptaError solo para fallos externos. El modelo no importa red ni archivos; --verificar, --replay y --bench no instancian la vista.

El plan debe incluir:
1. Problema y operaciones reales con su frecuencia esperada.
2. Al menos DOS alternativas por problema y la razón concreta de descarte de cada una.
3. Decisión (estructura y estrategia) y complejidad de las operaciones más frecuentes.
4. Impacto en código existente: archivo por archivo (ruta real) o "sin cambios".
5. Mediciones --bench previstas, incluida la de la alternativa descartada, con el comando exacto para reproducirlas.
6. Límites conocidos de la decisión.
7. Revisión de decisiones de la Parte I que esta carga pueda invalidar.
8. Trazabilidad: tabla FR-RES -> componente -> medición/prueba. Incluye los SC-001 a SC-008 y los casos del Apéndice B.
No agregues reglas del juego que no estén en spec.md. Si falta una regla, detente y pregunta.

Aspectos que el plan debe resolver para resolubilidad:
- Recorrido incremental único: obtener una llave desbloquea regiones sin reiniciar el recorrido. La frontera bloqueada, las llaves no obtenibles y las dependencias salen de ese mismo recorrido, sin recorridos adicionales por llave.
- Cómo asociar puertas cerradas pendientes con su llave y cómo identificar llaves (ids de texto) sin dict ni set ni bisect.
- Cómo garantizar el desempate por menor identificador en el orden de llaves, en las puertas de la frontera y en los ciclos.
- Detección determinista de un ciclo concreto por grupo de llaves, con costo aproximadamente lineal.
- Alternativa ingenua (repetir el recorrido por llave) implementada y medida con --bench sobre criptas sintéticas de muchas llaves encadenadas, deterministas por semilla.
- Reutilizar lo ya definido por la capacidad 001: obtener_llaves, LlaveUbicacionDTO, la caché de llaves por versión, el cliente falso (tests/cliente_falso.py) y CriptaMapa para resolver puertas declaradas en un solo lado y costos contradictorios (CriptaDatosInvalidosError). No redefinirlos.
- Flujo de --verificar y de inicio de partida (--forzar), adaptadores y presupuesto de solicitudes, sin que el modelo conozca red ni disco.
- Dónde se muestra el reporte (vista) sin que --verificar ni --bench la instancien.
- Medición de la cota de 200 ms en la cripta publicada más grande.

Al terminar, muestra un resumen breve de los archivos creados.
```

**Prompt (resumido):** Se pidió generar el plan técnico de la capacidad de resolubilidad con problema, al menos dos alternativas por decisión, complejidad, impacto en el código existente, mediciones con --bench y trazabilidad, respetando las restricciones de la constitución y reutilizando el contrato de datos de la capacidad de terreno y cazador.

**Para qué se usó:** Generar plan.md y sus artefactos asociados para la capacidad de resolubilidad, a revisar antes de pasar a las tareas.

### 2026-11-11 — Antigravity CLI 1.5.4 (Claude Sonnet 4.6 Thinking)
**Prompt:**
```text
/speckit-tasks
SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad
Contexto: ya estoy en la rama 003-resolubilidad. No crees ni cambies de rama y no hagas commit. Redacta todo en español, incluidos los títulos de las fases y secciones de la plantilla. Solo crea o modifica specs/003-resolubilidad/tasks.md. Usa solo spec.md, plan.md, research.md, data-model.md, quickstart.md y contracts/ de esa carpeta, y puedes LEER (sin modificar) el código de cripta/ y tests/ para citar rutas reales. No agregues reglas del juego ni decisiones de diseño que no estén en esos documentos. Si falta algo, detente y pregunta.

Reglas de la constitución que las tareas deben cumplir:
- Cada tarea cita los identificadores FR-RES-NNN que atiende, la ruta real del archivo que toca (marca "Nuevo" o "Modificado" según exista, comprobándolo en el repositorio), el comando de prueba que la valida y su criterio de "hecho". Máximo unos 90 minutos por tarea y ninguna tarea sin requisito.
- Cada escenario de aceptación de spec.md, incluidos los cuatro casos del Apéndice B, y cada SC-001 a SC-008 tiene al menos una tarea de prueba automatizada con unittest que cita el requisito. Las pruebas van antes que el código que las hace pasar. Las carpetas de pruebas nuevas llevan su __init__.py.
- Ninguna tarea usa heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Se reutilizan las estructuras propias de la Parte I citadas en plan.md (Cola, HeapMinimo, ordenamientos) y list solo como almacenamiento contiguo indexado por entero.
- Los errores de programación heredan de IndexError o ValueError; CriptaError solo para fallos externos. Se reutilizan CriptaDatosInvalidosError y CriptaLimiteError sin redefinirlos.
- El modelo no importa red ni archivos. --verificar y --bench no instancian la vista.
- Ninguna tarea contiene commits ni push, ni códigos de tarea ni nombres de personas en mensajes de commit.
- Ninguna tarea escribe cifras de rendimiento antes de medirlas. La cota de 200 ms se mide sobre la cripta publicada más grande, elegida por el mayor total de salas del listado y sin fijar su id en el código.

Organización obligatoria:
1. Fase A, dominio puro: pruebas primero y luego cripta/modelo/resolubilidad.py (catálogo de llaves ordenado con búsqueda binaria manual, recorrido incremental con Cola y HeapMinimo, condición de entrada a la sala de salida por una puerta que exige llave_salida, frontera bloqueada, ubicaciones, ciclos por DFS tricolor y alternativa ingenua verificar_ingenuo_reiniciado).
2. Fase B, servicio: ServicioResolubilidad con ClienteCripta, CacheDisco y presupuesto de solicitudes, costos contradictorios y presupuesto agotado sin reporte parcial.
3. Fase C, CLI y vista: --verificar sin vista, --forzar, compuerta al iniciar partida en el controlador y mostrar_reporte_resolubilidad en la vista.
4. Fase D, mediciones --bench: carga resolubilidad (incremental frente a la alternativa ingenua, criptas sintéticas encadenadas por semilla) y carga resolubilidad_cota, cada tarea con el comando exacto.
5. Fase E, cierre: las 222 pruebas de la Parte I en OK, auditoría de importaciones prohibidas con el Select-String del quickstart de la 001 y una tarea final "Sección de DECISIONES.md".

Marca [P] solo las tareas que tocan archivos distintos y no dependen entre sí. Indica el orden de dependencias entre fases y el punto de corte de cada Pull Request. El registro de este comando en PROMPTS_LLM.md se hace fuera de las tareas.
```

**Prompt (resumido):** Se pidió generar la lista de tareas de la capacidad de resolubilidad en cinco fases (dominio, servicio, CLI y vista, mediciones --bench, cierre), con cada tarea citando sus requisitos FR-RES, la ruta real del archivo y su prueba, y con las pruebas antes del código.

**Para qué se usó:** Generar tasks.md en specs/003-resolubilidad/, a revisar contra spec.md y plan.md antes de /speckit-analyze.


### 2026-11-17 — Antigravity CLI 1.5.4 (Claude Sonnet 4.6 Thinking)
**Prompt:**
```text
/speckit-analyze
SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad
Contexto: ya estoy en la rama 003-resolubilidad. No crees ni cambies de rama y no hagas commit. Es un análisis de SOLO LECTURA: no crees ni modifiques ningún archivo; entrega el informe únicamente en el chat. Redacta todo en español. Analiza la consistencia entre specs/003-resolubilidad/spec.md, plan.md, research.md, data-model.md, quickstart.md, contracts/, tasks.md y la constitución. Puedes leer cripta/ y tests/ solo para verificar rutas y nombres; no releas el repositorio completo.

Verifica en particular:
1. Cada FR-RES-001 a 023 y cada SC-001 a 008 tiene al menos una tarea y una prueba que lo cita; ninguna tarea cita un requisito inexistente.
2. Los cuatro casos del Apéndice B y cada escenario de aceptación de spec.md tienen una prueba prevista antes del código que los hace pasar.
3. spec.md no nombra estructuras, clases, módulos ni rutas de endpoint, y plan.md no agrega reglas del juego que no estén en spec.md.
4. Ningún documento propone heapq, bisect, collections, networkx, set, dict como índice o caché, ni list.sort() o sorted().
5. Cada cifra de rendimiento cita un comando de --bench o está marcada como hipótesis.
6. Las rutas de archivo y las marcas Nuevo/Modificado coinciden entre plan.md y tasks.md, y existen en el repositorio cuando dicen Modificado.
7. El orden de dependencias entre fases, las marcas [P] y los puntos de corte de los Pull Requests son coherentes.
8. Puntos a vigilar: los códigos de salida 0/1/2 de --verificar son decisión del plan y no vienen de la spec; la herencia de CriptaDatosInvalidosError; la semántica de las aristas del grafo de dependencias; quickstart.md no cita fixtures inexistentes ni exige datos offline sin explicarlo; la carga resolubilidad_cota está registrada en CARGAS; la prueba de --verificar (T012) vive en __main__.py, que se implementa en otra tarea; y cualquier cifra fija del número total de pruebas.

Informe: tabla con ID, gravedad (CRÍTICA, ALTA, MEDIA, BAJA), archivo y línea, problema y corrección sugerida. Máximo 25 hallazgos, los más graves primero, y cierra con una lista de requisitos sin tarea y tareas sin requisito (o "ninguno").
```

**Prompt (resumido):** Se pidió un análisis de solo lectura de la consistencia entre spec.md, plan.md, tasks.md, los anexos y la constitución de la capacidad de resolubilidad, con informe en el chat clasificado por gravedad.

**Para qué se usó:** Detectar requisitos sin tarea, reglas nuevas en el plan, estructuras prohibidas y rutas incoherentes antes de /speckit-implement.
 

### 2026-11-17 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-tasks
SPECIFY_FEATURE_DIRECTORY=specs/004-linea-de-tiempo
Contexto: ya estoy en la rama 004-linea-de-tiempo. No crees ni cambies de rama y no hagas commit ni push. Redacta todo en español, incluidos los títulos de las fases y secciones de la plantilla. Solo crea o modifica specs/004-linea-de-tiempo/tasks.md. Usa solo spec.md, plan.md, research.md, data-model.md, quickstart.md y contracts/ de esa carpeta, y puedes LEER (sin modificar) el código de cripta/ y tests/ para citar rutas reales. No agregues reglas del juego ni decisiones de diseño que no estén en esos documentos. Si falta algo, detente y pregunta.

Reglas de la constitución que las tareas deben cumplir:
- Cada tarea cita los identificadores FR-LIN-NNN que atiende, la ruta real del archivo que toca (marca "Nuevo" o "Modificado" según exista en esta rama, comprobándolo), el comando de prueba que la valida y su criterio de "hecho". Máximo unos 90 minutos por tarea y ninguna tarea sin requisito.
- Cada escenario de aceptación de spec.md, los seis casos B-LIN-001 a B-LIN-006 y cada SC-LIN-001 a SC-LIN-007 tienen al menos una tarea de prueba automatizada con unittest que cita el requisito. Las pruebas van antes que el código que las hace pasar. Las carpetas de pruebas nuevas llevan su __init__.py en una tarea explícita; tests/aceptacion/__init__.py y tests/servicios/test_servicio_bench.py se marcan «Nuevo si no existe tras fusionar la 002».
- Ninguna tarea usa heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Las búsquedas binarias se implementan a mano y list solo como almacenamiento contiguo indexado por entero.
- Los errores de programación heredan de IndexError o ValueError; CriptaError solo para fallos externos.
- El modelo no importa red, archivos ni vista. --replay y --bench no instancian la vista.
- Ninguna tarea contiene commits ni push, ni códigos de tarea ni nombres de personas en mensajes de commit.
- Ninguna tarea escribe cifras de rendimiento ni el valor por defecto de K antes de medir. La cripta de referencia se elige por el mayor total de salas del listado de fixtures, sin fijar su id; el criterio frente a la constante CRIPTA_REFERENCIA de la 001 queda como pendiente del grupo, sin decidir.
- Etiquetas de dependencia: «Depende de 001» para lo que use SalidaVista, EnemigoVista, Partida.vista() o el costo de salida en el movimiento; «Depende de 002» solo para lo que use el código del conocimiento del jugador (su proyección y sus costos de salida), que aún no está implementado; la línea de tiempo, los checkpoints y el formato binario propios de esta capacidad no llevan etiqueta. Ningún código previsto se redacta como si ya existiera.

Decisiones de diseño que las tareas deben reflejar tal como están en plan.md, data-model.md y research.md:
- El pergamino no es una acción numerada: la numeración de «historia #k» continúa desde la última acción vigente, el número de una acción revertida se reutiliza y k se rechaza si es cero o mayor que la cantidad de acciones vigentes. partida.log conserva las líneas revertidas y la del pergamino.
- Al aceptar un pergamino se anexa a la línea una entrada de ajuste de inventario sin número ni cuenta para K, acumulada en el nuevo final si un pergamino posterior trunca por detrás; el cursor del inventario no forma parte del resumen histórico.
- El punto de control se captura en el punto de decisión posterior a la acción múltiplo de K; al recortar se descartan los checkpoints con más acciones que la longitud vigente.
- La reconstrucción es aislada, con el registro de retroceso pausado, sin bitácora ni mensajes, y toma el contenido estático de las salas ya materializadas con una vía de restauración que no llama a precarga.preparar_sala.
- La búsqueda de t a número de acción y la de checkpoint son binarias manuales; las lineales solo existen en el benchmark.
- «historia» y «--replay --hasta» usan el mismo componente de proyección; el replay reproduce la bitácora completa, construye la línea vigente y consulta como historia. --hasta solo se acepta junto con --replay. La prueba de equivalencia usa docs/ejemplos/partida_cripta-03.log, que contiene un pergamino.
- Esta capacidad hace el único cambio de versión del formato binario y guarda en los checkpoints el conocimiento de la 002 con sus costos de salida.

Organización obligatoria:
1. Fase A, estructura pura de la línea de tiempo: pruebas primero y luego cripta/modelo/linea_tiempo.py (acciones vigentes con su instante, checkpoints, búsqueda binaria por número de acción y por instante, truncamiento desde el final, ajuste de inventario). No depende de otras capacidades.
2. Fase B, reconstrucción y consulta: contexto aislado, re-simulación desde el checkpoint con el estado de random.Random restaurado, estados en el instante t y en #k, resumen con los siete grupos mínimos, rechazos con motivo y sin efectos.
3. Fase C, persistencia: campos nuevos en EstadoPartida y persistencia_modelo.py, formato binario con versión nueva en guardado_binario.py, rechazo explícito y no destructivo de un archivo de la Parte I, y round-trip de la línea completa. Las tareas que guardan el conocimiento del jugador llevan «Depende de 002».
4. Fase D, interfaz y replay: comando historia en controlador y vista, --checkpoint-cada con validación, y --replay --hasta con la equivalencia descrita. El resumen de enemigos y salidas lleva «Depende de 001».
5. Fase E, mediciones --bench: carga linea_tiempo con K=100, 500, 1000 y sin checkpoints; inversión de cambios, búsqueda lineal de checkpoint y de acción, recorte por escaneo, y restauración con y sin precarga; cada tarea con el comando exacto. La elección del K por defecto es una tarea posterior a las mediciones.
6. Fase F, cierre: pruebas de la Parte I y II en OK, auditoría de importaciones prohibidas, repetición de las mediciones de agenda e historial de retroceso (Parte II §5.6) y una tarea final «Sección de DECISIONES.md».

Marca [P] solo las tareas que tocan archivos distintos y no dependen entre sí. Indica el orden de dependencias entre fases y el punto de corte del Pull Request, que no puede fusionarse antes de los de la 001 y la 002 y que incorpora main con merge. El registro de este comando en PROMPTS_LLM.md se hace fuera de las tareas.
```

**Prompt (resumido):** Generar la lista de tareas de la capacidad de línea de tiempo con pruebas antes que el código, requisitos citados, dependencias de 001 y 002 etiquetadas, las decisiones sobre el pergamino, la reconstrucción y el replay reflejadas, y el punto de corte del Pull Request.

**Para qué se usó:** Generar tasks.md para revisarlo antes de ejecutar analyze.

Corrige solo archivos dentro de specs/003-resolubilidad/ (spec.md, plan.md y tasks.md). No toques otras carpetas, no crees ni cambies de rama y no hagas commit ni push. SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad. Redacta en español. No cambies reglas del juego salvo lo pedido aquí; si algo cambia el resultado observable y no está decidido, detente y pregunta.

Spec primero:
1. spec.md: agrega al final de Supuestos las decisiones del grupo pendientes de confirmar con el profesor porque el enunciado no las fija: el orden incluye todas las llaves obtenibles, se informa un ciclo representativo por grupo, y una puerta cerrada sin llave es infranqueable. Agrega también los códigos de salida de --verificar (0 si la verificación termina, sea resoluble o no; 1 por datos inválidos; 2 por error externo) como requisito FR-RES-024 con su escenario, tomando el texto de contracts/contrato_resolubilidad.md §1.1 sin cambiarlo.

Plan y tareas (después de la spec):
2. tasks.md T013 y T014: fusiónalas en una sola tarea (método abstracto en vista_base.py, vistas falsas de las pruebas e implementación en vista_consola.py) para que la suite completa no se rompa entre ambas.
3. Unifica el ancho del reporte entre plan.md §4 y la tarea de la vista, tomando el valor de contracts/contrato_resolubilidad.md §3.
4. Agrega, antes de las tareas de bench, una tarea de prueba (tests/servicios/test_servicio_bench.py, Nuevo o Modificado según exista en esta rama, comprobándolo) para FR-RES-020 y SC-007: el generador sintético y las cargas producen la misma salida con la misma semilla; usa el nombre test_bench_resolubilidad_reproducible del plan.
5. Agrega una tarea que ejecute py -m cripta --bench --solo resolubilidad y py -m cripta --bench --solo resolubilidad_cota, y guarde los resultados en docs/bench/. La tarea de DECISIONES.md pasa a la sección «5.4 Resolubilidad», con alternativas, complejidad, evidencia medida y límites conocidos, y depende de esa tarea.
6. plan.md §3.2 y §7: declara el factor O(E log V) de CriptaMapa.obtener o indica que el verificador copia las salas a listas planas en una pasada, y ajusta la complejidad total. §5.1: alinea K = 40 y V = 800 con las tres escalas crecientes que pide la tarea de la carga. Agrega el «#» a la primera línea del plan.
7. Renumera las tareas y actualiza dependencias y trazabilidad.
Al terminar, dime qué cambiaste por punto y verifica con git diff que solo cambiaron archivos de specs/003-resolubilidad/.
```

**Prompt (resumido):** Aplicar la revisión del Pull Request de la capacidad de resolubilidad a la especificación, el plan y las tareas: supuestos del grupo, códigos de salida de --verificar, fusión de tareas de la vista, ancho del reporte, prueba de reproducibilidad del bench, tarea de mediciones, complejidad declarada y formato del plan.

**Para qué se usó:** Atender los seis puntos bloqueantes y las sugerencias de la revisión antes de fusionar el PR de documentación.

### 2026-11-17 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo plan.md y tasks.md dentro de specs/003-resolubilidad/. No toques otras carpetas, no crees ni cambies de rama y no hagas commit ni push. SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad. Redacta en español. No cambies reglas del juego; si algo cambia el resultado observable y no está decidido, detente y pregunta.
1. [Solo si ls-files imprimió la ruta] tests/servicios/test_servicio_bench.py ya existe en esta rama: marca T017 y la fila del plan §4 como Modificado, agregando test_bench_resolubilidad_reproducible sin alterar las pruebas existentes.
2. tasks.md: corrige el diagrama de dependencias entre fases, porque la Fase C va de T012 a T016, y cualquier otro rango desplazado.
3. tasks.md T012: agrega FR-RES-024 a Requisitos, porque prueba los códigos de salida de --verificar.
4. tasks.md T020 y plan.md §5.2: la carga resolubilidad_cota no usa red. Lee el listado de criptas desde fixtures/ con ClienteOffline, como hace ciclo_referencia de la 001, y elige la de mayor total de salas sin fijar su id. Agrega que T019 y T020 deben ejecutarse a escala mínima, porque la prueba de tests/bench/ recorre todas las cargas de CARGAS.
5. [Solo si los comandos lo detectaron] Elimina de plan.md el texto suelto «[2 coincidencias]» y el BOM del inicio.
Al terminar, dime qué cambiaste por punto y verifica con git diff que solo cambiaron archivos de specs/003-resolubilidad/.
```

**Prompt (resumido):** Ajustes finales de la 003 tras la revisión: rangos de fases, requisito de T012, origen de datos offline de la carga de cota y limpieza del plan.

**Para qué se usó:** Cerrar inconsistencias detectadas al revisar los cambios aplicados al PR de la 003 antes de aprobarlo.

### 2026-11-17 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo plan.md y tasks.md dentro de specs/003-resolubilidad/. No toques otras carpetas, no crees ni cambies de rama y no hagas commit ni push. SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad. Redacta en español. No cambies reglas del juego; si algo cambia el resultado observable y no está decidido, detente y pregunta.
1. tasks.md: corrige el diagrama de dependencias entre fases, porque la Fase C va de T012 a T016, y cualquier otro rango desplazado por la numeración actual.
2. tasks.md T012: agrega FR-RES-024 a Requisitos, porque prueba los códigos de salida de --verificar.
3. tasks.md T020 y plan.md §5.2: la carga resolubilidad_cota no usa red. Lee el listado de criptas desde fixtures/ con ClienteOffline, como hace ciclo_referencia de la capacidad 001 (verifícalo en cripta/bench/cargas_bench.py), y elige la de mayor total de salas sin fijar su id en el código. Agrega que T019 y T020 deben ejecutarse a escala mínima y sin red, porque tests/bench/test_cargas_bench.py recorre todas las cargas de CARGAS.
4. plan.md: elimina el texto suelto «[2 coincidencias]» de §5.1 y §5.2.
Al terminar, dime qué cambiaste por punto y verifica con git diff que solo cambiaron archivos de specs/003-resolubilidad/.
```

**Prompt (resumido):** Ajustes finales de la 003 tras la revisión: rangos de fases, requisito de T012, origen de datos offline de la carga de cota y limpieza del plan.

**Para qué se usó:** Cerrar inconsistencias detectadas al revisar los cambios aplicados al PR de la 003 antes de aprobarlo.

### 2026-11-17 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/07-implement-002.md. Solo T001 a T005, solo pruebas. No sigas con T006.
```
(El texto completo está en prompts/p2/07-implement-002.md.)

**Prompt (resumido):** Escritura de las pruebas del dominio del conocimiento del jugador de la capacidad de niebla de guerra e «ir a» (Fase A, T001 a T005), antes del código.

**Para qué se usó:** Crear tests/modelo/test_conocimiento_jugador.py con las pruebas de estados de sala, memoria de puertas, antorcha, inversas puntuales y salida sin puerta cerrable. Debían fallar porque cripta/modelo/conocimiento_jugador.py aún no existe.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/08-implement-002.md. Solo T006 a T009. No sigas con T010.
```
(El texto completo está en prompts/p2/08-implement-002.md.)

**Prompt (resumido):** Implementación del conocimiento del jugador (T006), pruebas de entrada y cierres observables (T007), integración en la partida (T008) y avisos de cierres automáticos (T009).

**Para qué se usó:** Crear cripta/modelo/conocimiento_jugador.py para que pasen las pruebas de T001 a T005 sin modificarlas, e integrarlo con las entradas, la antorcha, el pergamino y los cierres automáticos de la partida.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Estoy en la rama 002-niebla-ir-a-fases-a-b: no crees ni cambies de rama y no hagas commit ni push. Corrige solo cripta/modelo/conocimiento_jugador.py, cripta/modelo/partida.py, cripta/modelo/efectos.py y tests/modelo/test_conocimiento_jugador.py. No toques tasks.md ni PROMPTS_LLM.md ni las pruebas de T001 a T005. Mismas reglas de estilo de prompts/p2/08-implement-002.md (CRLF, sin sed -i, sin ";" en comentarios nuevos, sin estructuras prohibidas).
1. Regresión de T009. Hoy EfectoCierrePuerta._cerrar solo llama a al_cerrar si es_observable() es verdadero. Eso evita que un cierre fuera de las salas del jugador invalide el BuscadorRutas y emita "Una puerta se cierra sola.", que es el comportamiento de la 001 y de la Parte I. Restáuralo: al_cerrar se llama siempre, como antes. El aviso al conocimiento va por un segundo callback opcional que solo se llama cuando es_observable() es verdadero (ajusta el nombre del parámetro si hace falta y anótalo).
2. Deja _avisar_cierre_de_puerta(self) sin parámetros, como estaba, y mueve la lógica de observar la puerta a un método aparte que reciba sala_id y direccion. Con esto test_cazador_persecucion.py:97 funciona sin cambios.
3. Reemplaza la prueba test_cierre_automatico_solo_actualiza_si_jugador_esta_en_un_extremo por una que use el flujo real: abre una puerta con cierre automático, avanza el reloj con acciones reales y comprueba (a) que con el jugador en un extremo el conocimiento pasa a "cerrada" y (b) que con el jugador lejos el conocimiento no cambia pero el mensaje "Una puerta se cierra sola." sí sale y el BuscadorRutas queda invalidado.
4. En ConocimientoJugador.al_entrar quita la llamada redundante observar_puerta(destino, ...) y la variable sala sin uso de _explorar.
5. En partida.py no cambies el final de archivo y no uses "dir" como nombre en las lambdas.
No agregues reglas fuera de lo pedido. Si algo cambia lo que el jugador observa, detente y pregunta. Al terminar corre py -m unittest discover -s tests -t . y dime qué cambiaste por punto y verifica con git diff que solo cambiaron los cuatro archivos permitidos.
```

**Prompt (resumido):** Corrección de la integración del conocimiento con los cierres automáticos de puertas: restaurar el aviso y la invalidación de rutas en todo cierre, separar el aviso al conocimiento observable, probar el flujo real y limpiar código redundante.

**Para qué se usó:** Corregir una regresión de T009 detectada en la revisión: los cierres fuera de las salas del jugador dejaban de invalidar el buscador de rutas de los cazadores y de emitir su mensaje.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Estoy en la rama 002-niebla-ir-a-fases-a-b: no crees ni cambies de rama y no hagas commit ni push. Corrige solo cripta/modelo/partida.py, cripta/modelo/efectos.py y tests/modelo/test_conocimiento_jugador.py. No toques tasks.md, PROMPTS_LLM.md ni las pruebas de T001 a T005. Mismas reglas de estilo de prompts/p2/08-implement-002.md (CRLF, sin sed -i, sin ";" en comentarios nuevos, sin estructuras prohibidas).
1. La prueba test_cierre_automatico_actualiza_solo_si_jugador_esta_en_un_extremo no detecta un aviso faltante en el caso observable: la puerta nace cerrada, el jugador la observa cerrada al entrar y al final también se espera "cerrada", así que pasaría aunque nunca se avisara al conocimiento. Divídela en dos pruebas sin bucle ni ramas, una observable y otra lejana. En la observable, el jugador abre la puerta, la cruza y comprueba con una aserción que el conocimiento la recuerda "abierta", el cierre ocurre mientras el jugador sigue en uno de sus extremos y entonces el conocimiento pasa a "cerrada". La lejana conserva sus tres comprobaciones (memoria sin cambio, mensaje "Una puerta se cierra sola.", buscador invalidado).
2. En efectos.py restaura en el docstring de EfectoCierrePuerta la línea que cita §2.1 y deja la nota del segundo callback en una línea aparte.
3. Tras abrir una puerta con la acción abrir, el conocimiento sigue recordándola cerrada aunque el jugador está en uno de sus extremos. spec.md, sección Supuestos, dice que la observación ocurre al entrar o permanecer en las salas. Haz que tras abrir con éxito se observe esa puerta (observar_puerta con la sala actual y la dirección), antes de avanzar el tiempo de la acción, y agrega una prueba con la acción real. Si esto cambia lo que el jugador observa o contradice una regla de spec.md, detente y pregunta.
No agregues reglas fuera de lo pedido. Al terminar corre py -m unittest discover -s tests -t . y dime qué cambiaste por punto y verifica con git diff que solo cambiaron los tres archivos permitidos.
```

**Prompt (resumido):** Segunda corrección de la integración del conocimiento con los cierres automáticos: prueba del cierre observable que detecte el aviso faltante, docstring de `EfectoCierrePuerta` y observación de la puerta tras abrirla.

**Para qué se usó:** Cerrar tres hallazgos de la revisión: una prueba que pasaba sin verificar el aviso al conocimiento, una referencia a la especificación borrada de un docstring y la memoria de una puerta recién abierta por el jugador.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/09-implement-002.md. Solo T010 a T013. No sigas con T014.
```
(El texto completo está en prompts/p2/09-implement-002.md.)

**Prompt (resumido):** Proyección lógica del conocimiento en el estado guardado (T010 y T011), comprobación del paquete de aceptación (T012) y casos B-NIE-004 y B-NIE-005 (T013).

**Para qué se usó:** Incluir el conocimiento en el estado lógico de la partida sin tocar el formato binario, que corresponde a la 004, y verificar con casos de aceptación la antorcha y su reversión.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Estoy en la rama 002-niebla-ir-a-fases-a-b: no crees ni cambies de rama y no hagas commit ni push. Corrige solo cripta/infraestructura/estado_guardado.py, cripta/modelo/persistencia_modelo.py, cripta/modelo/partida.py (solo para conectar la proyección y la restauración del conocimiento), tests/servicios/test_servicio_partida_guardado.py, tests/aceptacion/test_niebla_ir_a.py y la casilla de T011 en tasks.md. No toques guardado_binario.py, cargas_bench.py, test_guardado_ida.py, test_guardado_vuelta.py ni las pruebas de T001 a T007. Mismas reglas de estilo de prompts/p2/09-implement-002.md (CRLF, sin sed -i, sin ";" en comentarios nuevos, sin estructuras prohibidas).
1. Prueba de T010. La mitad de restauración arma otra partida nueva con armar() e iniciar(), así que compara conocimiento inicial contra conocimiento inicial y no prueba nada. Reescríbela sin fijar atributos privados de ConocimientoJugador: partida con acciones reales (encender una antorcha con la acción usar y mover a una sala vecina, de modo que haya salas exploradas, vecinas reveladas y una puerta observada), proyecta el estado con a_estado_guardado, comprueba que estado.conocimiento no es None, restaura por el mismo camino que usan las pruebas existentes (desde_estado_guardado) sin pasar por bytes, y comprueba que proyectar() de la partida restaurada es igual al de la original. Luego, ya restaurada, ejecuta una acción nueva que cambie el conocimiento y usa el pergamino: el conocimiento debe volver al estado restaurado, lo que prueba que las inversas quedaron conectadas al retroceso. Muestra que falla antes de implementar T011 y por qué.
2. T011. Agrega a EstadoPartida un campo conocimiento AL FINAL, con valor por defecto None y excluido de la igualdad: conocimiento: tuple | None = field(default=None, compare=False). Así guardado_binario.py y cargas_bench.py, que lo construyen por posición, siguen funcionando, y test_guardado_ida y test_guardado_vuelta no cambian porque el codificador binario aún no conoce el campo. Proyéctalo en Partida.a_estado_guardado y restáuralo en la restauración, con la lógica de forma en persistencia_modelo.py. Al restaurar, el conocimiento restaurado reemplaza al creado en el constructor y queda conectado al retroceso. Si el estado no trae conocimiento (None, por ejemplo al cargar de archivo), la partida usa el ConocimientoJugador recién creado desde la sala actual. Es el comportamiento aceptado hasta que la 004 codifique el campo, no lo amplíes. Anota en un comentario de una línea sobre el campo que la 004 debe codificarlo y quitar compare=False. Marca T011 en [X] solo si pasan T010 y toda la suite.
3. T013, B-NIE-004. La sala 3 no tiene enemigos ni trampas, así que la aserción de listas vacías es verdadera por construcción. Pon en la sala 3 un enemigo dormido y una trampa, y comprueba tras entrar a la sala 2 con la antorcha encendida que la sala 3 está explorada, que su contenido no se cargó, que el enemigo no está activo ni tiene eventos en la agenda, que la trampa no se disparó y que la vida del jugador no cambió. Si el ayudante crear_partida_sintetica no permite colocar enemigos o trampas sin modificar tests/modelo/test_conocimiento_jugador.py, detente y explícalo.
4. T013, ambos casos. No asignes _antorcha_encendida. Enciende la antorcha con la acción real usar sobre un objeto de clase antorcha con duración, puesto en el inventario. En B-NIE-005 toma el estado previo después de encender la antorcha y antes de mover.
No agregues reglas fuera de lo pedido. Si algo cambia lo que el jugador observa o contradice spec.md, detente y pregunta. Al terminar corre py -m unittest discover -s tests -t . y dime qué cambiaste por punto y verifica con git diff que solo cambiaron los archivos permitidos y que guardado_binario.py, cargas_bench.py, test_guardado_ida.py y test_guardado_vuelta.py no cambiaron.
```

**Prompt (resumido):** Corrección de T010, T011 y T013: campo lógico del conocimiento en el estado guardado sin tocar el formato binario, prueba de restauración real y casos de aceptación con antorcha real y contenido que no se activa.

**Para qué se usó:** Cerrar T011, que se había detenido porque el campo rompía dos pruebas de ida y vuelta binaria de la Parte I, y reforzar dos pruebas que pasaban sin comprobar lo pedido.


### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/10-implement-002.md. Solo T015, T016, T019, T020 y T021. No sigas con T014, T017, T018 ni T022.
```
(El texto completo está en prompts/p2/10-implement-002.md.)

**Prompt (resumido):** Pruebas y búsqueda de costo mínimo sobre el conocimiento del jugador (T015 y T016), proyección inmutable del mapa y del resultado del viaje (T019 y T020) y su entrega desde la partida (T021).

**Para qué se usó:** Implementar en el modelo la ruta de «ir a» y las proyecciones que consumen el controlador y la vista, sin abrir puertas y usando solo el conocimiento del jugador.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/11-implement-002.md. Solo T014, T017, T018 y T022. No sigas con T023.
```
(El texto completo está en prompts/p2/11-implement-002.md.)

**Prompt (resumido):** Casos de aceptación del viaje (T014), pruebas del controlador (T017 y T018) y el bucle del viaje con la consulta del mapa (T022).

**Para qué se usó:** Implementar en el controlador la orden «ir a» como acciones ordinarias con recálculo por paso, motivos de detención y cancelación por pergamino, y la consulta del mapa conocido.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Estoy en una rama de trabajo: no crees ni cambies de rama y no hagas commit ni push. Corrige solo tests/modelo/test_ir_a.py, cripta/modelo/ruta_conocida.py (solo si hace falta), cripta/modelo/partida.py, cripta/modelo/resultado_partida.py, cripta/modelo/conocimiento_jugador.py y tests/modelo/test_conocimiento_jugador.py (solo agregar una prueba nueva, sin modificar las de T001 a T005). No toques tasks.md ni PROMPTS_LLM.md. Mismas reglas de estilo de prompts/p2/10-implement-002.md (CRLF, sin sed -i, sin ";" en comentarios nuevos, sin estructuras prohibidas, nombres nuevos mínimos y anotados).
1. Dos pruebas de TestRutaConocida no discriminan: esperan "N", que es la primera dirección en el orden N, S, E, O, así que una implementación que tomara la primera salida abierta también pasaría. Reescríbelas. (a) Desempate: dos vecinas con costo total idéntico hacia el destino, donde la de menor id quede en una dirección POSTERIOR a la de mayor id (por ejemplo la de menor id al E y la de mayor id al N). (b) Costo: la primera arista más barata no es la ruta más barata, y la ruta correcta sale por una dirección posterior (E u O). Agrega una aserción de control en cada una. Comprueba de forma temporal, sin dejarlo en el repositorio, que una versión que elige la primera salida abierta haría fallar ambas, y cuéntamelo.
2. Partida.motivos_despues_de_paso solo se prueba con llegada_destino, y la prueba de orden construye un ResultadoViaje a mano, así que no prueba la lógica. Agrega pruebas con Partida y un mapa sintético, colocando enemigos como en tests/aceptacion/test_niebla_ir_a.py: llegada más enemigo dormido más daño en el orden fijo de FR-NIE-013 (para el daño pasa como vida_anterior un valor mayor que la vida actual), un enemigo activo cuenta, un enemigo muerto no cuenta, sin llegada no aparece llegada_destino y con el jugador muerto el resultado es vacío.
3. ResultadoViaje.motivos nunca lo llena Partida: quita el campo motivos y su __post_init__, deja en el docstring que motivo es la razón por la que no hay paso, y ajusta las pruebas de T019 para que comprueben los motivos reales de Partida.motivos_despues_de_paso.
4. Partida.siguiente_paso: un id fuera del mapa (por ejemplo 99) da hoy destino_no_explorado y uno negativo da destino_inexistente. Haz que cualquier id que no exista en el mapa dé destino_inexistente. Agrega pruebas de ambos casos. Agrega también una prueba de sin_ruta con una puerta cerrada y el jugador con la llave en el inventario: el resultado es sin_ruta, la puerta sigue cerrada, y tiempo, mensajes y retrocesos_posibles no cambian (FR-NIE-014).
5. FR-NIE-025: sala_conocida marca como abierta toda salida sin llave ni cierre automático, incluso si su puerta empieza cerrada (SalidaDTO.cerrada, que puede venir marcada en un solo lado de la conexión). FR-NIE-025 habla de una salida sin puerta que pueda cerrarse, y una puerta que empieza cerrada es una puerta. Haz que esa excepción aplique solo si ninguno de los dos lados trae cerrada. Agrega una prueba nueva en tests/modelo/test_conocimiento_jugador.py: una puerta cerrada sin llave ni cierre no figura abierta antes de observarla y figura cerrada tras observarla, y una salida sin llave, sin cierre y sin cerrada sigue abierta sin observación. Muestra que la prueba falla antes del cambio. Si el cambio altera algo observable fuera de esto, detente y pregunta.
6. Confirma con conteo de bytes que cripta/modelo/ruta_conocida.py y tests/modelo/test_ir_a.py, y todo .py editado, quedan en CRLF, con la misma cantidad de CR y LF.
No agregues reglas fuera de lo pedido. Si algo cambia lo que el jugador observa o contradice spec.md, detente y pregunta. Al terminar corre py -m unittest discover -s tests -t . y dime qué cambiaste por punto, los nombres nuevos, y verifica con git diff que solo cambiaron los archivos permitidos.
```

**Prompt (resumido):** Corrección de la ruta conocida y sus pruebas: casos que distingan el desempate y el costo de elegir la primera salida, pruebas reales de los motivos de detención, limpieza del resultado del viaje, rechazo coherente de destinos inexistentes y puertas que empiezan cerradas sin llave ni cierre.

**Para qué se usó:** Cerrar los hallazgos de la revisión de T015 a T021 y un comentario de la revisión del PR de las fases A y B sobre FR-NIE-025.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/11-implement-002.md. Solo T014, T017, T018 y T022. No sigas con T023.
```
(El texto completo está en prompts/p2/11-implement-002.md.)

**Prompt (resumido):** Pruebas de aceptación y del controlador, y implementación de la consulta del mapa conocido y del bucle del viaje «ir a» en el controlador (T014, T017, T018 y T022).

**Para qué se usó:** Agregar las órdenes del mapa e «ir a» al controlador con recálculo de ruta por paso y motivos de detención, y los casos B-NIE-001, B-NIE-002, B-NIE-003 y B-NIE-006, sin tocar la vista, los servicios ni el modelo.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo cripta/controlador/controlador_cripta.py, tests/controlador/test_controlador_cripta.py y tests/aceptacion/test_niebla_ir_a.py.
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Estoy en la rama 002-niebla-ir-a-fases-c-d: no crees ni cambies de rama y no hagas commit ni push. No toques tasks.md: T014, T017, T018 y T022 siguen en [X]. Redacta en español.
Reglas: sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios, docstrings y textos nuevos no uses ";". No agregues reglas del juego. Si algo cambia lo que el jugador observa o contradice FR-NIE-013, detente y pregunta en vez de ajustar la prueba a lo observado.

1. Paso rechazado. Hoy _ejecutar_accion devuelve False tanto si el movimiento se rechaza como si se acepta y la partida sigue, así que un paso rechazado haría repetir el mismo paso sin fin. Primero escribe una prueba con un servicio falso que rechaza el movimiento y que lanza AssertionError si lo llaman más de 3 veces, para que falle sin colgar la suite. Debe verificar que el viaje se detiene, que no se piden más pasos, que se muestra el motivo de rechazo una sola vez y que no se llama a mostrar_motivos_viaje. Muéstrame que falla. Después corrige el controlador con el cambio mínimo, sin alterar el comportamiento de _ejecutar_accion para las demás órdenes, y anota el nombre nuevo si lo hay.
2. B-NIE-006. Usa una ruta de al menos 3 pasos, ejecuta 2 pasos con _ejecutar_paso_viaje y comprueba que el jugador está en la tercera sala. Registra el tiempo tras el primer paso. Lanza el pergamino con Orden("pergamino") por el controlador, no con partida.ejecutar_accion. Comprueba que el jugador queda en la sala del primer paso con ese tiempo, que revirtió solo un paso y que no se movió ni se llamó a mostrar_motivos_viaje después.
3. B-NIE-003. El enemigo dormido va en una sala intermedia y el destino es una sala posterior, no la sala del enemigo. Ejecuta el viaje por el controlador. Espera primero lo que dice FR-NIE-013 y comprueba que el jugador queda en la sala del enemigo, que el enemigo está activo y que los motivos incluyen enemigos_vivos y no incluyen llegada_destino. Agrega el control positivo: el mismo mapa sin enemigo llega al destino.
4. B-NIE-002. Agrega el control positivo (antes de observar el cierre, siguiente_paso devuelve dirección) y quita la asignación directa de partida._jugador.sala_actual: usa acciones reales de mover para entrar y volver. La única manipulación directa permitida es cambiar el estado real de la puerta en el mapa para simular el cierre no observado. Si no se puede sin tocar archivos no permitidos, detente y explícalo.
5. Quita el ";" del docstring de _ejecutar_paso_viaje y revisa con git diff que ninguna línea agregada en cripta/ ni tests/ tenga ";" en comentarios o docstrings.
Al terminar corre py -m unittest tests.aceptacion.test_niebla_ir_a tests.controlador.test_controlador_cripta y luego py -m unittest discover -s tests -t . y reporta cuántas pasan. Dime qué cambiaste por punto, los nombres nuevos y verifica con git diff que solo cambiaron esos tres archivos.
```

**Prompt (resumido):** Corrección del viaje «ir a» tras la revisión: detener el viaje si un paso es rechazado y reforzar los casos B-NIE-002, B-NIE-003 y B-NIE-006 con controles positivos y rutas de varios pasos.

**Para qué se usó:** Evitar un posible bucle sin fin cuando un movimiento es rechazado (nuevo `_ejecutar_accion_viaje`) y hacer que los casos de aceptación comprueben lo que describen. Esta corrección no tiene archivo en prompts/p2/.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo cripta/controlador/controlador_cripta.py y tests/controlador/test_controlador_cripta.py.
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Estoy en la rama 002-niebla-ir-a-fases-c-d: no crees ni cambies de rama y no hagas commit ni push. No toques tasks.md. Redacta en español.
Reglas: sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios, docstrings y textos nuevos no uses ";". No agregues reglas del juego. Si algo cambia lo que el jugador observa, detente y pregunta.

1. Defecto: _ejecutar_accion_viaje devuelve True cuando el desenlace no es "en_curso" pero no llama a self._finalizar(resultado.desenlace), como sí hace _ejecutar_accion. Si el jugador muere o gana durante un viaje, la partida vuelve al menú sin pedir nombre, sin registrar el puntaje y sin las pantallas de resultado y final. Primero escribe en tests/controlador/test_controlador_cripta.py una prueba que lo demuestre: un viaje cuyo paso termina la partida debe dejar en la vista exactamente un mostrar_resultado y un mostrar_final, y ningún mostrar_motivos_viaje. Hazla con el servicio real (preparar_controlador) y, si no es viable, con un servicio falso cuyo ejecutar devuelva un desenlace distinto de en_curso. Muéstrame que falla porque no se finaliza.
2. Corrige con el cambio mínimo: la rama de fin de partida de _ejecutar_accion_viaje llama a self._finalizar(resultado.desenlace) antes de devolver True. No dupliques lógica y no cambies _ejecutar_accion.
3. La prueba actual de muerte reemplaza _ejecutar_accion_viaje por un lambda y no cubre la finalización. Aclara en su docstring que solo comprueba que _ejecutar_paso_viaje no consulta motivos cuando el paso termina la partida, y que la finalización la cubre la prueba nueva.
Al terminar corre py -m unittest tests.aceptacion.test_niebla_ir_a tests.controlador.test_controlador_cripta y luego py -m unittest discover -s tests -t . y reporta cuántas pasan. Dime qué cambiaste por punto, los nombres nuevos y verifica con git diff que en este paso solo cambiaron esos dos archivos.
```

**Prompt (resumido):** Corrección del viaje «ir a»: finalizar la partida cuando un paso del viaje termina con muerte o victoria, con su prueba.

**Para qué se usó:** Evitar que un viaje que termina la partida vuelva al menú sin registrar el puntaje ni mostrar las pantallas de resultado y final.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/12-implement-002.md. Solo T023 y T024. No sigas con T025.
```
(El texto completo está en prompts/p2/12-implement-002.md.)

**Prompt (resumido):** Pruebas de la vista con datos del conocimiento (T023) y cambio de Partida.vista() para que las salidas de la sala actual salgan del conocimiento del jugador (T024).

**Para qué se usó:** Que las salidas, costos y puertas que muestra la vista sean las que el jugador conoce y no las del mapa real, sin filtrar nombres de salas avistadas o desconocidas.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo cripta/modelo/persistencia_modelo.py, tests/modelo/test_guardado_vuelta.py, tests/vista/test_vista_consola.py y specs/002-niebla-ir-a/tasks.md. Si el arreglo exige tocar otro archivo de cripta/modelo/, úsalo solo si es el cambio mínimo y anótalo.
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Estoy en la rama 002-niebla-ir-a-fases-c-d: no crees ni cambies de rama y no hagas commit ni push. No toques PROMPTS_LLM.md. Redacta en español.
Reglas: sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios, docstrings y textos nuevos no uses ";". No agregues reglas del juego. No modifiques pruebas existentes, solo agrega. Si algo cambia lo que el jugador observa más allá de lo descrito, detente y pregunta.

Contexto: tras T024, Partida.vista() toma las salidas del conocimiento. test_por_el_archivo_binario falla porque el archivo binario aún no guarda el conocimiento (el formato es de la capacidad 004). La partida cargada reconstruye un conocimiento sin observación de las puertas y su vista no coincide con la original. Dijiste que corregirlo queda fuera de lo autorizado, pero no es así: persistencia_modelo.py está en cripta/modelo/ y sí está autorizado. Lo prohibido sigue siendo guardado_binario.py, estado_guardado.py y toda codificación de bytes.

1. Cuando el estado restaurado no trae conocimiento (el caso del archivo binario), reconstruye una base coherente: la sala actual explorada con sus puertas observadas desde el mapa real, igual que en una entrada ordinaria, reutilizando el método existente del conocimiento. No cambies la forma de EstadoPartida ni escribas bytes. Cuando el estado sí trae conocimiento (la ruta en memoria), no cambies nada.
2. Primero escribe en tests/modelo/test_guardado_vuelta.py una prueba nueva, sin tocar las existentes: una partida jugada hasta una sala con una salida cerrada con llave, cargada desde un estado sin conocimiento (el mismo camino del archivo binario, o el estado con el campo del conocimiento en su valor por defecto), debe mostrar en vista() las mismas salidas, costos y cerradas que la original, con su control positivo (la salida con llave sale cerrada). Muéstrame que falla por la razón actual y no por un error de la prueba.
3. Con el arreglo, test_por_el_archivo_binario debe pasar sin modificarlo, igual que toda la suite.
4. En la prueba de T023 de tests/vista/test_vista_consola.py quitaste las aserciones de salidas_antes, que eran el control positivo previo al cambio de la puerta real. Restáuralas si siguen siendo válidas, o explica por qué no.
5. Dime cómo mapea Partida.vista() una puerta no_observada a SalidaVista.cerrada y si ese caso puede darse en la sala actual. No lo cambies, solo repórtalo.
6. Marca T024 como [X] en tasks.md solo si la suite completa pasa.
Al terminar corre py -m unittest tests.modelo.test_guardado_vuelta tests.vista.test_vista_consola y luego py -m unittest discover -s tests -t . (si py no puede ejecutarse usa .venv/Scripts/python.exe -m unittest) y reporta cuántas pasan. Dime qué cambiaste por punto, los nombres nuevos y verifica con git diff que en este paso solo cambiaron los archivos autorizados.
```

**Prompt (resumido):** Corrección de la carga desde archivo binario: reconstruir el conocimiento de la sala actual con sus puertas observadas cuando el estado no lo trae, para que la vista cargada coincida con la original.

**Para qué se usó:** Mantener en verde la prueba de guardado y carga por archivo binario tras hacer que la vista salga del conocimiento, hasta que la 004 codifique el conocimiento completo en el formato binario.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo plan.md y tasks.md dentro de specs/002-niebla-ir-a/. No toques otras carpetas, no crees ni cambies de rama y no hagas commit ni push. SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a. Redacta en español. No agregues reglas del juego. No marques ni desmarques ninguna casilla. Respeta los finales de línea CRLF. Si algo falta o cambia el resultado observable, detente y pregunta.
1. tasks.md T025 y T027: el contrato de presentación debe nombrar los dos métodos que el controlador ya pide a la vista: mostrar_mapa_conocido(proyeccion) y mostrar_motivos_viaje(motivos). Indica que motivos es una tupla de códigos y que la vista debe presentar llegada_destino, enemigos_vivos, daño_recibido y también sin_ruta, porque el controlador entrega sin_ruta por ese método cuando la ruta desaparece a mitad del viaje.
2. tasks.md T029 y T030: la vista de consola debe interpretar el comando mapa y el comando «ir a <sala>» (la sala es un identificador entero) y devolver las órdenes ya definidas en el controlador, Orden("mapa") y Orden("ir_a", id). Un argumento ausente o no entero no produce orden. Los controles visibles de la pantalla deben listar ambos comandos. Hoy ninguna tarea cubre este punto aunque FR-NIE-007 y FR-NIE-009 lo exigen.
3. tasks.md T026 y T028 y plan.md: hoy nadie llama al registro del comentario. ServicioPartida.ejecutar(Accion("mover")) no sabe que un movimiento pertenece a un viaje, así que el comentario único de FR-NIE-016 exige un método nuevo en ServicioPartida (el nombre lo propone la implementación) y que ControladorCripta lo llame una sola vez antes del primer paso, solo si la ruta tiene al menos un paso. Agrega a T028 la ruta cripta/controlador/controlador_cripta.py (Modificado) y la mención de ese método. Agrega a T026 la prueba del controlador en tests/controlador/test_controlador_cripta.py (Modificado) que verifica una sola llamada antes del primer paso y ninguna cuando la orden se rechaza. Revisa si [P] sigue siendo correcto en T026. En la tabla de impacto de plan.md ajusta las filas de servicio_partida.py y controlador_cripta.py para reflejarlo.
4. Comprueba con Test-Path que todas las rutas que citas existen y que su estado Nuevo o Modificado es correcto. Revisa que research.md, contracts/ y quickstart.md no contradigan estos cambios. Si alguno los contradice, no lo edites: dímelo.
Al terminar, dime qué cambiaste por punto y verifica con git diff que solo cambiaron archivos de specs/002-niebla-ir-a/ y que ninguna casilla cambió de estado.
```

**Prompt (resumido):** Ajuste del plan y las tareas de la Fase D de niebla de guerra e «ir a»: nombres de los métodos de presentación, interpretación de los comandos mapa e «ir a» en la vista de consola, y llamada del controlador al registro del comentario del viaje.

**Para qué se usó:** Cerrar dos huecos detectados antes de implementar la Fase D: ninguna tarea cubría la interpretación de los comandos en la vista ni la llamada que escribe el comentario de viaje en partida.log.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/13-implement-002.md. Solo T025, T027, T029 y T030. No sigas con T026 ni T028.

# Implementación 002, paso 7: contrato y presentación de la vista (T025, T027, T029 y T030)

Solo T025, T027, T029 y T030 de specs/002-niebla-ir-a/tasks.md. No sigas con T026 ni T028.

Reglas generales:
1. Lee spec.md (FR-NIE-007, FR-NIE-008, FR-NIE-009 y FR-NIE-013), plan.md, data-model.md, research.md, quickstart.md y contracts/ antes de escribir. Lee cripta/vista/vista_base.py, cripta/vista/vista_consola.py, tests/vista/test_vista_consola.py, el tipo de la proyección del mapa en cripta/modelo/resultado_partida.py y Partida.mapa_conocido() en cripta/modelo/partida.py. La vista solo lee esos datos y nunca toca el modelo, el servicio ni el mapa real.
2. Si necesitas un nombre nuevo que los documentos no definan, propón el mínimo siguiendo los patrones del código existente, en español, y anótalo en tu resumen con archivo y motivo. Solo detente y pregunta si algo cambia lo que el jugador observa o una regla de spec.md.
3. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Errores de programación heredan de IndexError o ValueError.
4. No modifiques pruebas existentes, solo agrega. No toques cripta/controlador/, cripta/modelo/, cripta/servicios/, cripta/infraestructura/ ni cripta/bench/. Si un defecto de esas capas lo exige, detente y explícalo. No crees ni cambies de rama y no hagas commit ni push. No toques PROMPTS_LLM.md. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios, docstrings y textos nuevos no uses ";". Comentarios cortos: cabecera de máximo 5 líneas y 1 o 2 líneas por método.
5. Pruebas con valor: cada caso comprueba valores concretos, incluye un control positivo cuando afirma una ausencia, no asigna atributos privados si existe una acción real, y cita en su docstring el FR-NIE y el escenario que cubre.
6. Marca cada casilla [X] en tasks.md cuando su tarea esté terminada y verificada.

Contexto de diseño, ya decidido en plan.md y tasks.md:
- El controlador ya llama a mostrar_mapa_conocido(proyeccion) y mostrar_motivos_viaje(motivos). motivos es una tupla de códigos (llegada_destino, enemigos_vivos, daño_recibido y sin_ruta) que la vista traduce a texto en español, conservando el orden recibido.
- VistaBase es una clase abstracta. Los dos métodos nuevos se declaran como abstractos, así que VistaConsola no se podrá instanciar hasta implementarlos. Por eso T027 y T030 se hacen juntas y no debes correr la suite completa entre ambas. Actualiza en VistaBase el texto que dice cuántos métodos tiene la vista.
- Los avisos y paneles de la consola salen por self._pendientes, justo encima de la entrada, como mostrar_inventario_ordenado. Presenta el mapa y los motivos con ese mismo patrón y con las cajas existentes (_caja y ANCHO).
- El mapa conocido muestra solo lo que trae la proyección: salas exploradas con su nombre, salidas, costos y estado recordado de las puertas, y salas avistadas solo como existencia. Nunca muestra el nombre de una sala avistada o desconocida.
- Comandos de consola: mapa devuelve Orden("mapa") e ir a <sala> devuelve Orden("ir_a", id) solo si el argumento es un entero. Ausente o no entero no produce orden y se informa como comando no reconocido. Solo se acepta la forma de tres palabras ir a <sala>. Los controles visibles de la pantalla deben listar ambos comandos sin romper la disposición actual de las celdas.

Puntos de control:
- T025: agrega a tests/vista/test_vista_consola.py la prueba del contrato: una subclase de VistaBase que implementa los métodos actuales pero no los dos nuevos no se puede instanciar, y con los dos sí. Debe fallar porque VistaBase aún no los declara. Muestra la razón.
- T029: agrega a tests/vista/test_vista_consola.py las pruebas de presentación del mapa (explorada con nombre, salidas, costos y puertas, avistada solo como existencia, ningún nombre oculto, con control positivo), de los motivos (cada código con su texto, orden conservado, sin_ruta incluido), de interpretación de comandos (mapa, ir a 3, ir a, ir a x, ir a -3, ir 3) y de los controles visibles. Deben fallar por lo que aún no existe, no por errores de sintaxis ni nombres mal escritos. Muestra las razones.
- T027 y T030, juntas: declara los dos métodos abstractos en cripta/vista/vista_base.py e impleméntalos en cripta/vista/vista_consola.py junto con la interpretación de comandos y los controles. Deben pasar T025 y T029. Corre py -m unittest tests.vista.test_vista_consola y luego py -m unittest discover -s tests -t . y confirma que todo pasa.
Al terminar, reporta cuántas pruebas pasan, qué hiciste por tarea, los nombres nuevos y confirma que no cambió ningún archivo fuera de cripta/vista/, tests/vista/ y tasks.md.
```

**Prompt (resumido):** Contrato de presentación de la vista (T025 y T027), pruebas de presentación del mapa conocido, de los motivos de detención y de los comandos mapa e «ir a» (T029), e implementación en la vista de consola (T030).

**Para qué se usó:** Que el jugador pueda consultar el mapa conocido y lanzar «ir a <sala>» desde la consola, y ver por qué se detuvo el viaje, sin que la vista acceda al mapa real ni muestre nombres de salas no exploradas. Codex no pudo mostrar las pruebas en rojo antes de implementar porque el sandbox bloqueó py.exe en la primera ejecución.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo tests/vista/test_vista_consola.py. No toques otros archivos, no crees ni cambies de rama y no hagas commit ni push. SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a. Redacta en español. Ajusta solo las pruebas que agregó la corrida anterior (TestContratoNiebla y TestPresentacionNiebla) y no modifiques las pruebas existentes. No marques ni desmarques ninguna casilla. Los .py van en CRLF. En comentarios, docstrings y textos nuevos no uses ";". Si algo cambia el resultado observable o exige tocar otro archivo, detente y pregunta.
1. test_mapa_muestra_datos_explorados_y_solo_existencia_avistada: hoy comprueba caracteres sueltos ("E", "N", "2", "3") que aparecen en cualquier texto, y assertNotIn("Secreto", texto) no prueba nada porque la proyección de la prueba no contiene ese nombre. Reemplaza esas aserciones por comprobaciones de las líneas completas que produce mostrar_mapa_conocido: la sala explorada con su nombre, cada salida con dirección, sala destino, costo y estado de la puerta, y la sala avistada como existente y sin explorar. Agrega la ausencia real con control positivo: arma una proyección con una sala avistada que traiga un nombre ("Secreto") si SalaConocida lo permite, comprueba que la vista no lo imprime y que el nombre de la sala explorada sí se imprime. Si SalaConocida rechaza un nombre en una sala avistada, elimina la aserción vacía, anota en el docstring que la proyección ya lo garantiza y dímelo.
2. test_controles_visibles_listan_mapa_e_ir_a_sin_salirse_de_celda: el límite 4 * 29 + 1 es un número suelto. Derívalo de la constante o del cálculo que usa VistaConsola._controles() para armar las celdas, o comprueba la disposición real (filas y celdas por fila) sin números mágicos. Dime además cuántas filas tenía la cuadrícula de controles antes de la corrida anterior y cuántas tiene ahora, y si el cambio altera la altura de la pantalla.
3. Corre py -m unittest tests.vista.test_vista_consola y luego py -m unittest discover -s tests -t . y confirma que todo pasa.
Al terminar, dime qué cambiaste por punto y confirma que en esta corrección no editaste ningún archivo salvo tests/vista/test_vista_consola.py.
```

**Prompt (resumido):** Corrección de las pruebas de presentación del mapa conocido y de los controles visibles de la vista de consola: aserciones sobre líneas completas, ausencia de nombres ocultos con control positivo y disposición de controles sin números mágicos.

**Para qué se usó:** Reforzar dos pruebas de la corrida 13 que no comprobaban lo que declaraban: la ausencia de nombres de salas no exploradas y la disposición de los controles.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/14-implement-002.md. Solo T026 y T028. No sigas con T031.

# Implementación 002, paso 8: comentario de viaje en partida.log (T026 y T028)

Solo T026 y T028 de specs/002-niebla-ir-a/tasks.md. No sigas con T031.

Reglas generales:
1. Lee spec.md (FR-NIE-011, FR-NIE-016 y FR-NIE-017), plan.md (filas de servicio_partida.py, controlador_cripta.py, partida_log.py y servicio_replay.py de la tabla de impacto), research.md, data-model.md, quickstart.md y contracts/ antes de escribir. Lee cripta/servicios/servicio_partida.py, cripta/controlador/controlador_cripta.py (el bucle del viaje), cripta/infraestructura/partida_log.py, cripta/servicios/servicio_replay.py, tests/infraestructura/test_partida_log.py, tests/controlador/test_controlador_cripta.py y tests/servicios/test_servicio_replay.py. Comprueba con Test-Path que cada ruta existe y que su estado Nuevo o Modificado es correcto antes de editarla.
2. Si necesitas un nombre nuevo que los documentos no definan, propón el mínimo siguiendo los patrones del código existente, en español, y anótalo en tu resumen con archivo y motivo. Solo detente y pregunta si algo cambia lo que el jugador observa o una regla de spec.md.
3. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). Errores de programación heredan de IndexError o ValueError. CriptaError es solo para errores externos de disco o archivos.
4. No modifiques pruebas existentes, solo agrega. No toques cripta/modelo/, cripta/vista/ ni cripta/bench/. Si un defecto de esas capas lo exige, detente y explícalo. No crees ni cambies de rama y no hagas commit ni push. No toques PROMPTS_LLM.md. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios, docstrings y textos nuevos no uses ";". Comentarios cortos: cabecera de máximo 5 líneas y 1 o 2 líneas por método.
5. Pruebas con valor: cada caso comprueba valores concretos, incluye un control positivo cuando afirma una ausencia, no asigna atributos privados si existe una acción real, y cita en su docstring el FR-NIE y el escenario que cubre.
6. Marca cada casilla [X] en tasks.md cuando su tarea esté terminada y verificada.

Contexto de diseño, ya decidido en plan.md y tasks.md:
- Una orden ir_a válida ejecuta cada paso como una acción ordinaria mover mediante ServicioPartida.ejecutar(Accion("mover")). Cada paso aceptado ya deja su línea de movimiento en partida.log, y los turnos de los enemigos no producen líneas.
- FR-NIE-016: antes del primer paso se escribe un único comentario que empieza con # y registra la orden. El comentario no es una acción: el lector de partida.log lo trata como metadato y el replay lo omite y reproduce solo las acciones.
- ServicioPartida recibe un método nuevo que escribe ese comentario (el nombre lo propone la implementación). ControladorCripta lo llama una sola vez, antes del primer paso, y solo si la ruta tiene al menos un paso. Una orden rechazada o sin efecto (destino no explorado, destino actual o sin ruta) no escribe nada. Una acción individual del jugador nunca lleva comentario.
- Si spec.md o contracts/ definen el texto del comentario, úsalo exacto. Si no lo definen, propón el mínimo que identifique la sala destino y repórtalo.
- La lectura de archivos partida.log de la Parte I no debe romperse.

Puntos de control:
- T026: agrega primero las pruebas. En tests/infraestructura/test_partida_log.py: el comentario se escribe antes del primer movimiento y una sola vez, una acción individual no lo lleva, no se escribe comentario si no hay pasos, y el replay de un archivo con comentario reproduce solo acciones y llega al mismo estado. En tests/controlador/test_controlador_cripta.py: con un servicio que registra sus llamadas, una sola llamada al método nuevo antes del primer paso y ninguna cuando la orden se rechaza. Antes de implementar, corre py -m unittest tests.infraestructura.test_partida_log tests.controlador.test_controlador_cripta y muestra por qué fallan, que debe ser por lo que aún no existe y no por errores de sintaxis ni nombres mal escritos. Si el sandbox bloquea py.exe, pide aprobación para correr ese comando antes de continuar y no implementes hasta mostrar el rojo.
- T028: implementa el método nuevo en cripta/servicios/servicio_partida.py, su llamada en cripta/controlador/controlador_cripta.py, y el tratamiento del comentario como metadato no accionable en cripta/infraestructura/partida_log.py y cripta/servicios/servicio_replay.py, sin instanciar la vista. Deben pasar las pruebas de T026. Corre py -m unittest tests.infraestructura.test_partida_log tests.servicios.test_servicio_replay tests.controlador.test_controlador_cripta y luego py -m unittest discover -s tests -t . y confirma que todo pasa.
Al terminar, reporta cuántas pruebas pasan, qué hiciste por tarea, los nombres nuevos, el texto exacto del comentario y de dónde salió, y confirma que no cambió ningún archivo fuera de cripta/servicios/, cripta/controlador/, cripta/infraestructura/partida_log.py, tests/ y tasks.md.
```

**Prompt (resumido):** Pruebas y implementación del comentario único de viaje en partida.log (T026 y T028): método nuevo en el servicio de partida, una sola llamada del controlador antes del primer paso, y tratamiento del comentario como metadato por el lector y el replay.

**Para qué se usó:** Que una orden «ir a» deje en partida.log un solo comentario antes del primer movimiento, sin registrar nada cuando la orden se rechaza, y que el replay reproduzca solo las acciones.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo tests/controlador/test_controlador_cripta.py, tests/infraestructura/test_partida_log.py y tests/servicios/test_servicio_replay.py. Solo si el punto 5 demuestra un defecto, puedes tocar también cripta/servicios/servicio_replay.py o cripta/infraestructura/partida_log.py con el cambio mínimo. No toques otros archivos, no crees ni cambies de rama y no hagas commit ni push. SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a. Redacta en español. Ajusta solo las pruebas que agregó la corrida anterior (TestComentarioViaje, TestComentarioViajeControlador y test_comentario_de_viaje_no_altera_replay) y no modifiques las pruebas existentes. No marques ni desmarques ninguna casilla. Los .py van en CRLF. En comentarios, docstrings y textos nuevos no uses ";". Si algo cambia el resultado observable o exige tocar otro archivo, detente y pregunta.
1. tests/controlador/test_controlador_cripta.py, test_comentario_se_registra_una_vez_antes_del_primer_paso: la ruta tiene un solo paso, así que no distingue una llamada por viaje de una llamada por paso. Agrega un caso con una ruta de al menos 3 pasos y comprueba que el orden es una llamada al comentario, el primer paso y los pasos siguientes sin más comentarios, por ejemplo [("comentario", destino), ("paso", ...), ("paso", ...), ("paso", ...)]. Prepara la partida con acciones reales cuando existan y no asignes atributos privados del modelo salvo que no haya otra forma, en cuyo caso dilo.
2. Agrega en tests/controlador/test_controlador_cripta.py una prueba de integración con el servicio real y su bitácora real, sin sustituir registrar_comentario_viaje: tras una orden ir_a con al menos 2 pasos, partida.log tiene el encabezado, luego una única línea "# ir a N" y después exactamente una línea de movimiento por paso, sin líneas de turnos de enemigos. Tras una orden rechazada (destino inexistente) y tras una orden al destino actual, el archivo contiene solo el encabezado. Si montar el servicio con bitácora exige tocar otro archivo, detente y dímelo.
3. tests/infraestructura/test_partida_log.py, test_sin_pasos_no_escribe_comentario: no ejecuta nada y ya pasaba antes de implementar, así que no prueba lo que declara, y compara contra un JSON escrito a mano que depende del orden de las claves. Elimínala, porque la cubre la prueba del punto 2. Las otras dos pruebas de TestComentarioViaje se quedan.
4. tests/servicios/test_servicio_replay.py, test_comentario_de_viaje_no_altera_replay: la última aserción compara la sala de una partida consigo misma. Reemplázala por comparar el estado final del replay del log con comentario contra el del replay del log sin comentario, con los datos que ResultadoReplay ya expone.
5. Números de línea: ServicioReplay numera las acciones con enumerate(..., start=2) suponiendo una línea del log por acción, pero ahora el log puede traer comentarios. Primero agrega en tests/servicios/test_servicio_replay.py una prueba con un log que tenga "# ir a 2" y después una acción inválida y comprueba que el número de línea reportado es la línea real del archivo. Corre solo esa prueba y muestra si falla y por qué. Si falla, corrígelo con el cambio mínimo en los archivos permitidos sin cambiar la firma ni el resultado de LectorBitacoraPartida.leer() que usan las pruebas existentes. Si no falla, dilo y deja la prueba como control. Si el arreglo exige cambiar esa firma, detente y pregúntame.
6. Corre py -m unittest tests.infraestructura.test_partida_log tests.servicios.test_servicio_replay tests.controlador.test_controlador_cripta y luego py -m unittest discover -s tests -t . y confirma que todo pasa.
Al terminar, dime qué cambiaste por punto y confirma qué archivos editaste en esta corrección y que ningún otro cambió.
```

**Prompt (resumido):** Corrección de las pruebas del comentario de viaje: ruta de varios pasos, integración con el servicio y la bitácora reales, eliminación de una prueba vacía, comparación real del replay y verificación de los números de línea con comentarios.

**Para qué se usó:** Reforzar las pruebas de T026 que no demostraban que el comentario se escribe una sola vez por viaje ni su efecto en partida.log, y comprobar que el replay informa la línea correcta cuando el log trae comentarios.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/15-implement-002.md. Solo T031 a T036. No sigas con T037.

# Implementación 002, paso 9: cargas de medición niebla_rutas (T031 a T036)

Solo T031 a T036 de specs/002-niebla-ir-a/tasks.md. No sigas con T037 ni con la Fase F.

Reglas generales:
1. Lee spec.md (FR-NIE-018, SC-NIE-002 y SC-NIE-004), plan.md (sección de mediciones --bench y la tabla de impacto), research.md, quickstart.md, data-model.md y contracts/ antes de escribir. Lee cripta/bench/cargas_bench.py (sus ayudantes _medir y _comparar, el registro CARGAS y las cargas de ruta_cazador, invalidacion y ciclo_referencia como patrón), cripta/servicios/servicio_bench.py, tests/bench/test_cargas_bench.py, cripta/modelo/conocimiento_jugador.py y cripta/modelo/ruta_conocida.py. Comprueba con Test-Path si tests/servicios/test_servicio_bench.py existe. Si existe, trátalo como Modificado y repórtalo. Si no existe, créalo como Nuevo.
2. Si necesitas un nombre nuevo que los documentos no definan, propón el mínimo siguiendo los patrones del código existente, en español, y anótalo en tu resumen con archivo y motivo. Solo detente y pregunta si algo cambia lo que el jugador observa o una regla de spec.md.
3. Sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted(). La selección lineal, la pasada completa y la copia completa son alternativas de medición del harness en cripta/bench/, nunca de implementación en cripta/modelo/. Errores de programación heredan de IndexError o ValueError.
4. No modifiques pruebas existentes, solo agrega. Edita únicamente cripta/bench/cargas_bench.py, cripta/servicios/servicio_bench.py, tests/servicios/test_servicio_bench.py, tests/bench/ si hace falta y tasks.md. No toques cripta/modelo/, cripta/vista/, cripta/controlador/ ni cripta/infraestructura/. Si un defecto de esas capas lo exige, detente y explícalo. No crees ni cambies de rama y no hagas commit ni push. No toques PROMPTS_LLM.md. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios, docstrings y textos nuevos no uses ";". Comentarios cortos: cabecera de máximo 5 líneas y 1 o 2 líneas por método.
5. Pruebas con valor: cada caso comprueba valores concretos, incluye un control positivo cuando afirma una ausencia, no asigna atributos privados si existe una acción real, y cita en su docstring el FR-NIE y el escenario o SC que cubre.
6. Marca cada casilla [X] en tasks.md cuando su tarea esté terminada y verificada. No marques T037.
7. Ninguna cifra de rendimiento se escribe antes de medir: no pongas resultados de medición en código, docstrings, tasks.md ni documentos. Las cargas solo miden y reportan cuando se ejecutan.

Contexto de diseño, ya decidido en plan.md y tasks.md:
- La carga niebla_rutas se selecciona con py -m cripta --bench --solo niebla_rutas --escala 1, se ejecuta sin red y sin instanciar la vista, y usa random.Random(semilla) propio. El reloj de pared se usa solo para medir y nunca decide nada del juego.
- Referencia: mapa conocido completo de la cripta de referencia. La cripta de referencia es la de mayor total de salas entre los fixtures de fixtures/, elegida dinámicamente leyendo los datos, sin fijar su id en el código. No reutilices ni modifiques la constante CRIPTA_REFERENCIA de las cargas de la 001. La carga comprueba existencia, integridad y versión del fixture antes de medir. Informa salas y salidas leídas del fixture, mediana y máximo del cálculo del primer paso de «ir a» y si cumple 5 ms.
- Alternativas de ruta: la búsqueda real con HeapMinimo de cripta/modelo/ruta_conocida.py frente a una selección lineal manual escrita en el harness, sobre el mismo grafo y las mismas consultas, y deben dar el mismo primer paso. También se compara, sobre consultas idénticas, la ruta con los costos guardados en el conocimiento frente a la consulta a CriptaMapa.costo_de_conexion. La selección lineal se reporta aunque resulte más rápida en esta escala.
- Revelación: varios R de salas nuevas sobre mapas de tamaños distintos, midiendo solo la actualización, con la revelación incremental frente a una pasada ingenua por todo el mapa escrita solo en el harness.
- Reversión: registra y revierte cambios de antorcha y compara el tiempo y el número de inversas contra una copia completa del conocimiento como alternativa de medición.
- tests/bench/test_cargas_bench.py recorre todas las cargas de CARGAS a escala mínima y sin red. niebla_rutas debe poder correr así.
- Cada carga reporta unidades, entorno, semilla o configuración, salas y salidas, mediana y máximo.

Puntos de control:
- T031 y T032: agrega primero las pruebas en tests/servicios/test_servicio_bench.py. T031: las parejas de revelación (incremental frente a pasada ingenua) y de reversión (inversas frente a copia completa) producen estados equivalentes en consultas deterministas. T032: la ruta con heap y la selección lineal dan el mismo primer paso, incluida la elección dinámica del fixture de mayor total de salas sin fijar su id, y la ruta con costos guardados y la que consulta CriptaMapa.costo_de_conexion dan el mismo resultado sobre consultas idénticas. Antes de implementar corre py -m unittest tests.servicios.test_servicio_bench y muestra por qué fallan, que debe ser por lo que aún no existe y no por errores de sintaxis ni nombres mal escritos. Si el sandbox bloquea py.exe, pide aprobación para correr ese comando antes de continuar y no implementes hasta mostrar el rojo.
- T033, T034, T035 y T036: implementa en cripta/bench/cargas_bench.py la selección lineal y la comparación de rutas con costos guardados frente a costo_de_conexion, la revelación incremental frente a la pasada completa y la reversión frente a la copia completa, y registra niebla_rutas en cripta/servicios/servicio_bench.py sin instanciar la vista. Deben pasar las pruebas de T031 y T032. Corre py -m unittest tests.servicios.test_servicio_bench tests.bench.test_cargas_bench y luego py -m unittest discover -s tests -t . y confirma que todo pasa.
- Al final corre una sola vez py -m cripta --bench --solo niebla_rutas --escala 1 solo para comprobar que termina sin error y sin instanciar la vista. Pega la salida en tu respuesta y no copies ninguna cifra en ningún archivo, porque la medición oficial es T037.
Al terminar, reporta cuántas pruebas pasan, qué hiciste por tarea, los nombres nuevos, cuál fixture eligió la carga y por qué criterio, si test_servicio_bench.py era Nuevo o Modificado, y confirma que no cambió ningún archivo fuera de cripta/bench/cargas_bench.py, cripta/servicios/servicio_bench.py, tests/ y tasks.md.
```

**Prompt (resumido):** Pruebas del harness y cargas de medición niebla_rutas (T031 a T036): selección lineal frente a heap, costos guardados frente a consulta del mapa, revelación incremental frente a pasada completa, reversión frente a copia completa, y registro de la carga sin vista.

**Para qué se usó:** Dejar listas y verificadas las alternativas de medición de la capacidad de niebla de guerra e «ir a» antes de la medición oficial con --bench.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo cripta/bench/cargas_bench.py y tests/servicios/test_servicio_bench.py. No toques otros archivos, no crees ni cambies de rama y no hagas commit ni push. SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a. Redacta en español. Ajusta solo lo que agregó la corrida anterior (bench_niebla_rutas y sus ayudantes, y las pruebas de test_servicio_bench.py). No marques ni desmarques ninguna casilla. Los .py van en CRLF. En comentarios, docstrings y textos nuevos no uses ";". No escribas cifras de medición en ningún archivo. Si algo cambia el resultado observable o exige tocar otro archivo, detente y pregunta.
1. Ruta con heap: hoy se mide el lote de las 12 consultas y se informa su total como mediana y máximo. Mide cada consulta por separado con varias repeticiones, informa mediana y máximo por cálculo de un primer paso, cuántas de las consultas tienen ruta, y una línea que diga si cumple o no el límite de 5 ms tomando el máximo por cálculo, con una constante LIMITE_PASO_MS como LIMITE_CICLO_MS. Mide solo las consultas que tienen ruta. Si ninguna la tiene, lanza ValueError.
2. Revelación y reversión: _comparar_revelacion y _comparar_reversion llaman a _elegir_fixture_referencia() dentro de lo que se mide, así que el tiempo incluye leer el fixture y armar el mapa. Haz que reciban la referencia ya armada una sola vez y mide solo la actualización de la revelación y solo registrar y revertir en la reversión.
3. Revelación: informa por separado, para cada R, la mediana y el máximo de la revelación incremental y los de la pasada ingenua, junto con la equivalencia. La alternativa descartada se reporta aunque resulte más rápida.
4. Reversión: informa por separado la mediana y el máximo de registrar y revertir por inversas y los de copiar y restaurar la copia completa, a partir de varias repeticiones y no de una sola corrida, junto con el número de inversas y la equivalencia. Se reporta aunque la copia resulte más rápida.
5. La fila «costos guardados frente a costo_de_conexion» informa 0.000 ms y solo comprueba equivalencia. Reemplázala por una comparación de tiempos de la misma búsqueda con costos guardados y con consulta a CriptaMapa.costo_de_conexion, sobre las mismas consultas, con mediana y máximo de cada una, y conserva la comprobación de equivalencia con la ruta real.
6. Selección lineal justa: hoy _seleccion_lineal y _siguiente_paso_costos_mapa recorren todas las salas y todas sus salidas por cada nodo extraído, lo que da O(V por E) y no el O(V al cuadrado más E) que declara plan.md, y llaman a conocimiento.proyectar() dentro de cada consulta. Reescríbelas para que difieran de la búsqueda real en cripta/modelo/ruta_conocida.py solo en cómo eligen el siguiente nodo (escaneo lineal de las distancias) y relajen únicamente las aristas del nodo extraído con el mismo criterio de puertas, desempate y costos que usa ruta_conocida.py. Saca proyectar() del tiempo medido o aplícalo igual en ambas alternativas. Explica qué cambiaste y por qué.
7. _elegir_fixture_referencia toma candidatos[0] y eso depende del orden de iterdir() cuando hay empate de salas_total. Desempata de forma explícita por el menor identificador, sin sorted ni list.sort, y que el resultado no dependa del orden de lectura del directorio.
8. Quita el segundo if repetido dentro de la pasada ingenua y sustituye los ";" que hay dentro de los textos de salida nuevos por otro separador.
9. Primero ajusta tests/servicios/test_servicio_bench.py a las nuevas firmas y agrega lo necesario, y corre py -m unittest tests.servicios.test_servicio_bench para mostrar el rojo por lo que aún no existe. Después implementa. Corre py -m unittest tests.servicios.test_servicio_bench tests.bench.test_cargas_bench, luego py -m unittest discover -s tests -t . y una sola vez py -m cripta --bench --solo niebla_rutas --escala 1 solo para comprobar que termina, y pega su salida sin copiar cifras en ningún archivo.
Al terminar, dime qué cambiaste por punto, si servicio_bench.py necesitó algún cambio y confirma qué archivos editaste en esta corrección y que ningún otro cambió.
```

**Prompt (resumido):** Corrección de la carga niebla_rutas: medición por cálculo con veredicto de 5 ms, fixture fuera del tiempo medido, alternativas descartadas reportadas por separado, selección lineal justa y desempate determinista del fixture.

**Para qué se usó:** Hacer que las mediciones de la Fase E midan lo que declaran y que las alternativas descartadas se comparen en igualdad de condiciones, antes de la medición oficial de T037.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
Corrige solo cripta/bench/cargas_bench.py y tests/servicios/test_servicio_bench.py. No toques otros archivos, no crees ni cambies de rama y no hagas commit ni push. SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a. Redacta en español. Ajusta solo lo de niebla_rutas. No marques ni desmarques ninguna casilla. Los .py van en CRLF. En comentarios, docstrings y textos nuevos no uses ";". No escribas cifras de medición en ningún archivo. Si algo cambia el resultado observable o exige tocar cripta/modelo/, detente y pregunta. Sé conciso.
1. Consultas representativas: hoy las consultas son pares de salas vecinas y el mapa conocido tiene puertas cerradas que lo parten en regiones pequeñas, así que la búsqueda explora muy poco y el veredicto de 5 ms no representa el peor caso de FR-NIE-018. En _elegir_fixture_referencia, antes de marcar las salas como exploradas, abre todas las puertas de la instancia de CriptaMapa que arma el harness (solo esa instancia, nunca el fixture en disco) para tener el peor caso conectado, usando la API pública del mapa. Elige hasta 12 consultas distintas con pares de origen y destino al azar con random.Random(SEMILLA_NIEBLA), con un número máximo de intentos, quedándote solo con los que tienen ruta, de forma determinista. Informa en las notas cuántas puertas se abrieron y cuántos pares se probaron y cuántos tenían ruta. Si no existe una API pública para abrir todas las puertas, detente y dímelo.
2. Comparación de costos justa: hoy el lado «costos guardados» usa siguiente_paso de producción y el lado «consulta al mapa» usa una búsqueda con heap del harness, así que no comparan lo mismo. Agrega en el harness una variante de _siguiente_paso_costos_mapa con la misma estructura y que use salida.costo, y compara solo esas dos para el origen del costo, con mediana y máximo por cálculo de cada una y equivalencia con la ruta real. Informa aparte, en su propia fila, la función de producción siguiente_paso con su mediana y máximo por cálculo y el veredicto de 5 ms. Lee cripta/modelo/ruta_conocida.py y explícame en tu respuesta qué trabajo hace la función de producción que no hacen las variantes del harness, y por qué mide más que la selección lineal. No modifiques cripta/modelo/.
3. Etiquetas: hoy las filas de ruta y de revelación pasan a Resultado una mediana por cálculo con el número de consultas como operaciones, y por eso el resumen de la primera línea muestra «totales» y «µs/op» incorrectos. Haz que cada fila por cálculo use una sola operación, de modo que la primera línea y la de la flecha digan lo mismo.
4. Copia completa: en el camino de copiar y restaurar de _comparar_reversion, deja el registrador del conocimiento sin asignar mientras se mide la alternativa, de modo que no registre cambios en el historial. La medición de inversas conserva su registrador.
5. tests/servicios/test_servicio_bench.py: en la prueba de rutas, recorre todas las consultas de la referencia y no solo la primera, y comprueba que la lista no está vacía, que cada consulta tiene ruta con siguiente_paso, y que dos llamadas a _elegir_fixture_referencia dan las mismas consultas. Agrega también la prueba de la variante con costo guardado frente a la de consulta al mapa sobre todas las consultas. Muestra primero en rojo lo que cambia y por qué.
6. Corre py -m unittest tests.servicios.test_servicio_bench tests.bench.test_cargas_bench, luego py -m unittest discover -s tests -t . y una sola vez py -m cripta --bench --solo niebla_rutas --escala 1 solo para comprobar que termina, y pega su salida sin copiar cifras en ningún archivo.
Al terminar, dime qué cambiaste por punto, la explicación del punto 2 y confirma qué archivos editaste en esta corrección y que ningún otro cambió.
```

**Prompt (resumido):** Segunda corrección de la carga niebla_rutas: consultas con ruta sobre el mapa conectado, comparación de costos que solo cambia el origen del costo, filas por cálculo con una operación, copia completa sin registrador y pruebas sobre todas las consultas.

**Para qué se usó:** Que la medición de FR-NIE-018 represente el peor caso de un mapa conectado y que las alternativas descartadas se comparen en igualdad de condiciones antes de la medición oficial.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Sigue las instrucciones de prompts/p2/16-implement-002.md. Solo T037, T038, T039 y T041. No marques T040.

# Implementación 002, paso 10: cierre de la capacidad (T037, T038, T039 y T041)

Solo T037, T038, T039 y T041 de specs/002-niebla-ir-a/tasks.md. No marques T040, que depende de la 004.

Reglas generales:
1. Lee spec.md (FR-NIE-018, SC-NIE-002, SC-NIE-004 y los supuestos de decisión del grupo), plan.md, research.md, quickstart.md y las tareas T037 a T041. Lee DECISIONES.md completo para seguir su estilo y su sección «Cómo leer este documento», con las secciones 5.1, 5.2 y 5.6 de la capacidad 001 como modelo, y los tres archivos docs/bench/resultados_002_a.md, _b.md y _c.md. Comprueba con Test-Path que existen.
2. Solo editas DECISIONES.md (CRLF), specs/002-niebla-ir-a/tasks.md (LF) y, para el punto 6, specs/002-niebla-ir-a/plan.md (CRLF). No toques código ni pruebas. No crees ni cambies de rama y no hagas commit ni push. No toques PROMPTS_LLM.md. Edita con tu herramienta de edición, no con sed -i. En el texto nuevo no uses ";".
3. Todas las cifras salen de los tres archivos de resultados o de los datos de este prompt. No inventes ni redondees de más. Usa la mediana de las tres corridas y cita las tres.
4. Si algo cambia lo que dicen spec.md o plan.md, o falta información, detente y pregunta.

Tareas:
- T037: la medición la hizo el grupo y su salida está en los tres archivos de resultados. Comprueba que las tres dicen CUMPLE el límite de 5 ms y marca T037 como [X].
- T038: corre py -m unittest discover -s tests -t . y reporta cuántas pruebas pasan. Marca T038 como [X] solo si todas pasan.
- T039: ejecuta los tres comandos de auditoría de T039 y analiza cada coincidencia por su contexto para descartar falsos positivos. Si hay un uso prohibido real, detente y repórtalo sin corregir. Marca T039 como [X] solo si no hay usos prohibidos reales ni vista instanciada en replay o bench.
- T041: añade a DECISIONES.md solo la sección «5.3 Niebla de guerra e «ir a»», entre la 5.2 y la 5.6, con la estructura de la Parte I (Problema, Alternativas consideradas, Decisión, Análisis de complejidad, Evidencia empírica, Límites conocidos). Enlaza a specs/002-niebla-ir-a/spec.md y plan.md y di si la decisión final coincide con la del plan.md original y, si no, qué medición lo motivó. Marca T041 como [X].
- Punto 6: servicio_bench.py no cambió porque ServicioBench ya ejecuta las cargas registradas en CARGAS de cargas_bench.py. Ajusta el texto de T036 en tasks.md (sin cambiar su casilla) y la fila de servicio_bench.py de la tabla de impacto de plan.md para que digan Sin cambios y por qué.
- En «Cómo leer este documento» agrega niebla_rutas a la lista de cargas y la sección 5.3 a la fila del Equipo B de la tabla de equipos, y añade una frase que diga que las cifras de la sección 5.3 se midieron con Python 3.14.7, sin cambiar la versión que ya figura para las otras secciones.

Datos para la sección 5.3 (Equipo B, Intel Core Ultra 7, 16 GB, Windows, Python 3.14.7):
- Comando: py -m cripta --bench --solo niebla_rutas --escala 1, tres corridas guardadas en docs/bench/resultados_002_a.md, _b.md y _c.md. Cripta de referencia: cripta-06, elegida por el mayor total de salas sin fijar su id en el código, con 300 salas y 760 salidas. El harness abre las 28 puertas cerradas de su propia instancia del mapa para tener el peor caso conectado y usa 12 consultas con ruta, elegidas al azar con semilla 20261118. Cada consulta se mide tres veces por alternativa. Las cifras son por cálculo del primer paso de «ir a».
- Ruta de producción (heap con costos guardados): medianas por cálculo de las tres corridas 3.100, 3.038 y 3.095 ms, mediana 3.095 ms. Máximos por cálculo 4.834, 3.799 y 4.599 ms, mediana 4.599 ms. El peor máximo fue 4.834 ms, a 0.166 ms del límite. CUMPLE 5 ms en las tres corridas.
- Selección lineal manual: medianas 5.013, 4.799 y 4.758 ms, mediana 4.799 ms, 1.55 veces más lenta que producción. Máximos 7.142, 6.122 y 5.284 ms, mediana 6.122 ms.
- Heap del harness con costos guardados: medianas 3.205, 3.069 y 3.062 ms, mediana 3.069 ms. Máximos 4.503, 3.709 y 3.398 ms, mediana 3.709 ms.
- Heap del harness con consulta a CriptaMapa.costo_de_conexion: medianas 4.287, 4.217 y 4.194 ms, mediana 4.217 ms, 1.37 veces más lento que con costos guardados. Máximos 5.398, 4.906 y 7.101 ms, mediana 5.398 ms, con un máximo que supera 5 ms. Las tres variantes dan el mismo primer paso que la ruta de producción.
- Revelación por entrada, mediana de las tres corridas. R=10: incremental 0.032 ms (máximo 0.053) y pasada ingenua 0.360 ms (máximo 0.417), 11.3 veces más lenta. R=50: incremental 0.028 ms (máximo 0.052) y pasada ingenua 0.362 ms (máximo 0.563), 12.9 veces. R=200: incremental 0.016 ms (máximo 0.068) y pasada ingenua 0.366 ms (máximo 0.577), 22.9 veces. Estados equivalentes en todas.
- Reversión con 20 entradas y 409 inversas: registrar y revertir por inversas 0.800 ms (máximo 0.878) y copiar y restaurar la copia completa 1.185 ms (máximo 1.197), 1.48 veces más lenta. Estados equivalentes.

Contenido de la sección 5.3, sin reglas nuevas:
- Problema: operaciones reales con su frecuencia. Cada entrada a una sala observa sus puertas y revela vecinas si hay antorcha. Cada paso de «ir a» calcula un primer paso con solo el conocimiento del jugador. El pergamino revierte la entrada y sus cambios de conocimiento.
- Alternativas, al menos dos por subproblema: representación del conocimiento (listas contiguas por id, elegida, frente a recalcular desde el mapa real en cada consulta); revelación (incremental, elegida, frente a pasada completa); reversión (inversas puntuales por celda, elegida, frente a copia completa del conocimiento); ruta (búsqueda propia con HeapMinimo desde el destino, elegida, frente a selección lineal y frente a reutilizar BuscadorRutas de la 001, descartada porque calcula sobre el mapa real, poda por rango de cazadores y guarda una caché pensada para sus eventos); costo de la salida (guardado en el conocimiento, elegido, frente a CriptaMapa.costo_de_conexion).
- Decisión y complejidad según plan.md: revelación O(R), búsqueda con heap O((V+E) log V), selección lineal O(V al cuadrado más E). Di que la decisión final coincide con la de plan.md y que la hipótesis de research.md de que la selección lineal podría ganar en mapas pequeños no se cumplió con las 300 salas conectadas de cripta-06.
- Evidencia: las tablas con las medianas de las tres corridas, con enlace a los tres archivos de resultados. Cuenta con honestidad que una primera versión de la carga usaba pares de salas vecinas con las puertas cerradas, que partían el mapa en regiones diminutas, y que se corrigió abriendo las puertas del harness y eligiendo pares al azar con ruta, para medir el peor caso.
- Límites conocidos: el margen del límite de 5 ms es estrecho, con 4.834 ms en la peor corrida. La función de producción proyecta el conocimiento y reconstruye las aristas entrantes en cada llamada, y que esa preparación domine el tiempo es una hipótesis sin medir. En la revelación, R es la cantidad de entradas al azar con reemplazo y no R salas nuevas, y solo se mide un tamaño de mapa. Se mide el cálculo del paso y no un viaje completo en una partida real. El guardado binario del conocimiento depende de la 004 y T040 sigue pendiente, así que hasta entonces cargar una partida de archivo no conserva el mapa explorado. Partida.vista() muestra como cerrada una puerta no observada, algo que no debería darse en la sala actual. La salida sin puerta cerrable se considera abierta al revelarse la sala, decisión del grupo pendiente de confirmar con el profesor. Los costos de salida del conocimiento ocupan memoria proporcional a las salidas.

Al terminar, dime qué cambiaste por punto, cuántas pruebas pasan, el resultado de la auditoría con sus falsos positivos descartados, y confirma con git diff que solo cambiaron DECISIONES.md, tasks.md y plan.md, y que en tasks.md solo cambiaron las casillas de T037, T038, T039 y T041 y el texto de T036.
```

**Prompt (resumido):** Cierre de la capacidad de niebla de guerra e «ir a»: marca de la medición oficial, suite completa, auditoría de usos prohibidos y sección 5.3 de DECISIONES.md con las cifras medidas, más el ajuste del texto sobre servicio_bench.py.

**Para qué se usó:** Dejar documentadas las decisiones, las alternativas descartadas y los resultados medidos de la capacidad, y cerrar las tareas de la Fase F que no dependen de la 004.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Retoma la corrida 16 de la capacidad 002, que se detuvo en T039 sin cambiar ningún archivo. Este mensaje reemplaza lo que prompts/p2/16-implement-002.md diga distinto y no necesitas releer ese prompt. Solo T037, T038, T039 y T041 de specs/002-niebla-ir-a/tasks.md. No marques T040, que depende de la 004.

Reglas generales:
1. Lee spec.md (FR-NIE-018, SC-NIE-002, SC-NIE-004 y los supuestos de decisión del grupo), plan.md, research.md, quickstart.md y las tareas T037 a T041. Lee DECISIONES.md completo para seguir su estilo y su sección «Cómo leer este documento», con las secciones 5.1, 5.2 y 5.6 de la capacidad 001 como modelo, y los tres archivos docs/bench/resultados_002_a.md, resultados_002_b.md y resultados_002_c.md. Comprueba con Test-Path que existen. Para describir el método de la medición puedes leer cripta/bench/cargas_bench.py, sin editarlo.
2. Solo editas DECISIONES.md, specs/002-niebla-ir-a/tasks.md y specs/002-niebla-ir-a/plan.md, respetando los finales de línea de cada archivo. No toques código, pruebas, PROMPTS_LLM.md ni la carpeta prompts. No crees ni cambies de rama y no hagas commit ni push. Edita con tu herramienta de edición, no con sed -i. En el texto nuevo no uses ";".
3. Todas las cifras salen exclusivamente de los tres archivos de resultados. Calcula tú la mediana de las tres corridas de cada cifra y cita las tres. No uses cifras de memoria ni redondees de más. Al final entrega una tabla con cada cifra que usaste en la sección 5.3 (alternativa, valor de cada corrida y mediana de las tres) para que el grupo la revise.
4. Si algo cambia lo que dicen spec.md o plan.md, o falta información, detente y pregunta.
5. Si py.exe devuelve acceso denegado, solicita autorización para ejecutarlo fuera del sandbox, como en las corridas anteriores. No des por pasada ninguna prueba que no hayas corrido.

Tareas:
- T037: la medición la hizo el grupo y su salida está en los tres archivos de resultados. Comprueba que las tres dicen CUMPLE el límite de 5 ms y marca T037 como [X].
- T038: corre py -m unittest discover -s tests -t . y reporta cuántas pruebas pasan. El grupo ya la corrió y dio 385 en OK. Marca T038 como [X] solo si todas pasan.
- T039: ejecuta los tres comandos de auditoría de T039 y analiza cada coincidencia por su contexto. Decisión del grupo sobre cripta/servicios/servicio_bench.py: es código de la 001 ya aprobado y fusionado, esta rama no lo modifica y no se corrige aquí. La constitución prohíbe dict, set y sorted en los problemas evaluados, y ese archivo los usa para validar nombres de subsistemas de la línea de comandos, ordenar un mensaje de error y devolver el contenedor del reporte, que no son un índice, una caché ni un ordenamiento de un problema evaluado. Lista cada coincidencia de ese archivo con su línea y la razón por la que no aplica, y no la corrijas. Si aparece una coincidencia real en conocimiento_jugador.py, ruta_conocida.py o cargas_bench.py, o una vista instanciada en replay o bench, detente y repórtalo sin corregir. Marca T039 como [X] solo si no hay usos prohibidos reales en los archivos de la 002 ni vista instanciada en replay o bench.
- T041: añade a DECISIONES.md solo la sección «5.3 Niebla de guerra e «ir a»», entre la 5.2 y la 5.6, con la estructura de la Parte I (Problema, Alternativas consideradas, Decisión, Análisis de complejidad, Evidencia empírica, Límites conocidos). Enlaza a specs/002-niebla-ir-a/spec.md y plan.md y di si la decisión final coincide con la del plan.md original y, si no, qué medición lo motivó. Marca T041 como [X].
- Punto 6: servicio_bench.py no cambió porque ServicioBench ya ejecuta las cargas registradas en CARGAS de cargas_bench.py. Ajusta el texto de T036 en tasks.md, sin cambiar su casilla, y la fila de servicio_bench.py de la tabla de impacto de plan.md para que digan Sin cambios y por qué.
- En «Cómo leer este documento»: agrega niebla_rutas a la lista de cargas. En la tabla de equipos agrega 5.3 a la columna «Se usó en» de la fila del Equipo A y no cambies su columna de Python. Añade una frase que diga que las cifras de la sección 5.3 se midieron en el Equipo A con Python 3.14.7, a diferencia de la versión que figura en su fila.

Datos verificados para la sección 5.3 (Equipo A: Ryzen 5 5600GT, 32 GB, Windows, Python 3.14.7):
- Comando: py -m cripta --bench --solo niebla_rutas --escala 1, tres corridas guardadas en docs/bench/resultados_002_a.md, resultados_002_b.md y resultados_002_c.md.
- Cripta de referencia: cripta-06, elegida por el mayor total de salas sin fijar su id en el código, con 300 salas y 760 salidas. El harness abre las 28 puertas cerradas de su propia instancia del mapa para tener el peor caso conectado, prueba 12 pares y los 12 tienen ruta, elegidos al azar con semilla 20261118. Cuántas veces se mide cada consulta por alternativa lo tomas de cargas_bench.py y solo lo escribes si el código lo confirma.
- Las cifras de ruta son por cálculo del primer paso de «ir a». Todas las cifras que cite la sección salen de los tres archivos de resultados y se reportan como mediana de las tres corridas, con su máximo.
- La ruta de producción es un heap con costos guardados. El peor máximo por cálculo de producción entre las tres corridas fue 4.834 ms, a 0.166 ms del límite de 5 ms, y cumple en las tres.

Contenido de la sección 5.3, sin reglas nuevas:
- Problema: operaciones reales con su frecuencia. Cada entrada a una sala observa sus puertas y revela vecinas si hay antorcha. Cada paso de «ir a» calcula un primer paso con solo el conocimiento del jugador. El pergamino revierte la entrada y sus cambios de conocimiento.
- Alternativas, al menos dos por subproblema: representación del conocimiento (listas contiguas por id, elegida, frente a recalcular desde el mapa real en cada consulta). Revelación (incremental, elegida, frente a pasada completa). Reversión (inversas puntuales por celda, elegida, frente a copia completa del conocimiento). Ruta (búsqueda propia con HeapMinimo desde el destino, elegida, frente a selección lineal y frente a reutilizar BuscadorRutas de la 001, descartada porque calcula sobre el mapa real, poda por rango de cazadores y guarda una caché pensada para sus eventos). Costo de la salida (guardado en el conocimiento, elegido, frente a CriptaMapa.costo_de_conexion).
- Decisión y complejidad según plan.md: revelación O(R), búsqueda con heap O((V+E) log V), selección lineal O(V al cuadrado más E). Di si la decisión final coincide con la de plan.md y si la hipótesis de research.md de que la selección lineal podría ganar en mapas pequeños se cumplió o no con las 300 salas conectadas de cripta-06, según las cifras de los archivos.
- Evidencia: tablas con las medianas y los máximos de las tres corridas para la ruta de producción, la selección lineal, el heap del harness con costos guardados, el heap del harness con consulta a CriptaMapa.costo_de_conexion, la revelación incremental frente a la pasada ingenua en cada tamaño R que midan los archivos y la reversión por inversas frente a la copia completa, con las razones calculadas desde las medianas y enlaces a los tres archivos de resultados. Si algún máximo supera 5 ms, dilo. Cuenta con honestidad que una primera versión de la carga usaba pares de salas vecinas con las puertas cerradas, que partían el mapa en regiones diminutas, y que se corrigió abriendo las puertas del harness y eligiendo pares al azar con ruta, para medir el peor caso.
- Límites conocidos: el margen del límite de 5 ms es estrecho. La función de producción proyecta el conocimiento y reconstruye las aristas entrantes en cada llamada, y que esa preparación domine el tiempo es una hipótesis sin medir. En la revelación, R es la cantidad de entradas al azar con reemplazo y no R salas nuevas, y solo se mide un tamaño de mapa. Se mide el cálculo del paso y no un viaje completo en una partida real. El guardado binario del conocimiento depende de la 004 y T040 sigue pendiente, así que hasta entonces cargar una partida de archivo no conserva el mapa explorado. Partida.vista() muestra como cerrada una puerta no observada, algo que no debería darse en la sala actual. La salida sin puerta cerrable se considera abierta al revelarse la sala, decisión del grupo pendiente de confirmar con el profesor. Los costos de salida del conocimiento ocupan memoria proporcional a las salidas. Comprueba cada uno de estos límites contra el código y los documentos actuales, y si alguno ya no es cierto, ajústalo o quítalo y dilo en tu resumen.

Al terminar, dime qué cambiaste por punto, cuántas pruebas pasan, el resultado de la auditoría con cada coincidencia de servicio_bench.py y su razón, la tabla de cifras de la regla 3, y confirma con git diff que solo cambiaron DECISIONES.md, tasks.md y plan.md, y que en tasks.md solo cambiaron las casillas de T037, T038, T039 y T041 y el texto de T036.
```

**Prompt (resumido):** Reanudación de la corrida 16 con cifras tomadas solo de los archivos de resultados, atribución al Equipo A con Python 3.14.7, tratamiento de los hallazgos de servicio_bench.py como código de la 001 ya aprobado y solicitud de autorización para ejecutar py fuera del sandbox.

**Para qué se usó:** Completar el cierre de la capacidad (T037, T038, T039 y T041) después de que la primera ejecución se detuviera en T039 sin cambios, corrigiendo el equipo de medición y evitando cifras copiadas de un resumen.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:**
```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/002-niebla-ir-a
Ajuste final de la sección 5.3 de DECISIONES.md de la capacidad 002. Solo editas DECISIONES.md, respetando sus finales de línea CRLF. No toques otros archivos, no marques ni desmarques casillas de tasks.md, no cambies de rama y no hagas commit ni push. No uses ";" en el texto nuevo. No corras la suite, es solo documentación.
1. En «Análisis de complejidad» elimina la última oración, la que dice que las consultas observadas y los valores de V y E se describen con la evidencia y no son nuevas reglas.
2. En «Límites conocidos» reescribe con redacción clara el punto sobre Partida.vista(), después de comprobar en cripta/modelo/partida.py y cripta/modelo/resultado_partida.py cómo se presenta hoy una puerta no observada en la sala actual. Si en la sala actual todas las puertas ya se observan al entrar y ese caso no ocurre, quita el punto o redáctalo como el límite real que exista. Separa en un punto propio la decisión del grupo sobre la salida sin puerta cerrable, que se considera abierta al explorar su sala y está pendiente de confirmar con el profesor.
3. Comprueba en cripta/bench/cargas_bench.py cuántos cálculos se miden por consulta y por alternativa. Corrige el texto de la sección 5.3 solo si el código dice otra cosa.
Al terminar, dime qué cambiaste por punto y confirma con git diff que solo cambió DECISIONES.md.
```

**Prompt (resumido):** Ajuste final de la sección 5.3 de DECISIONES.md: quitar una frase residual, aclarar el límite sobre Partida.vista() y separar la decisión del grupo sobre la salida sin puerta cerrable, y comprobar el número de cálculos por consulta contra el código.

**Para qué se usó:** Corregir tres defectos de redacción y de precisión detectados en la revisión de la sección 5.3 antes de cerrar la capacidad.
### 2026-11-18 — Codex CLI 0.169.0 (GPT-6.2 Sol)
**Prompt:**
```text
$speckit-implement Trabaja solo en el benchmark de la 004, como preparación de T033. Actualiza primero los artefactos de la fase E para dejar trazado el nuevo escenario. Añade K=50 con puntos reales cada 50 acciones y conserva K=100, 500, 1000 y sin puntos periódicos. Para medir registro y ciclo usa corridas propias con la misma semilla y carga. Para consulta usa las mismas posiciones en todos los escenarios e incluye casos justo antes de un punto de control. Verifica la cadencia y ejecuta py -m cripta --bench --solo linea_tiempo --escala 1. Reporta por escenario cantidad de puntos, memoria, mediana y máximo observado de consulta y peor ciclo. Conserva la captura completa para obtener la línea base. No cambies el K predeterminado, no cierres T033 y no toques T034–T036. Respeta CRLF, cita los FR en las pruebas y no hagas commits ni push.
```

(El texto completo está en prompts/p2/22-implement-004-benchmark-linea-base.md.)

**Continuación:** «Implement the plan.»

**Prompt (resumido):** Benchmark de la 004 con K=50 y puntos reales cada 50 acciones junto a K=100, 500, 1000 y sin puntos, con los artefactos de la fase E actualizados primero y la captura completa conservada como línea base.

**Para qué se usó:** Preparar y registrar la línea base del benchmark de la 004 antes de T033.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6.2 Sol)
**Prompt:**
```text
$speckit-implement Trabaja solo en la optimización de los puntos de control periódicos de la 004. Antes de tocar código, actualiza el plan y añade una tarea en tasks.md vinculada a los FR correspondientes. Omite una sala del punto periódico solo si nunca se preparó y su estado se puede reconstruir desde el esqueleto: puertas en estado inicial, sin rastro y sin enemigos activos. Conserva la captura completa del estado inicial y del estado actual del guardado. Verifica que el formato v2 siga leyendo los puntos completos anteriores y los nuevos puntos reducidos, y que historia, replay y guardado/carga den los mismos resultados. Ejecuta la suite completa y repite py -m cripta --bench --solo linea_tiempo --escala 1 con la misma carga. Guarda los resultados por separado y compara memoria, mediana y máximo de consulta y peor ciclo con docs/bench/resultados_004_linea_base.md. Deja K=100 provisional y T033 abierta para revisar los datos. Registra el prompt en PROMPTS_LLM.md, conserva CRLF y no hagas commits ni push.
```

(El texto completo está en prompts/p2/23-implement-004-puntos-reducidos.md.)

**Prompt (resumido):** Reducir los puntos de control periódicos omitiendo las salas nunca preparadas que se pueden reconstruir desde el esqueleto, con el plan y una tarea actualizados antes del código y la medición repetida contra la línea base.

**Para qué se usó:** Reducir la captura periódica, comprobar la compatibilidad v2 y medir el cambio frente a la línea base de la 004.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6.2 Sol)
**Prompt:**
```text
$speckit-implement Ejecuta solo T033 de specs/004-linea-de-tiempo/tasks.md. Contrasta las mediciones de docs/bench/resultados_004_linea_base.md y docs/bench/resultados_004_puntos_reducidos.md. Registra en tasks.md el comando, las condiciones de la carga y la justificación para proponer K=50 frente a los otros escenarios, con el máximo observado de consulta y el costo de memoria. Si falta alguna medición del grupo requerida por T033, indícala y deja la tarea abierta. Registra el prompt en PROMPTS_LLM.md. Conserva CRLF y no hagas commits ni push.
```

(El texto completo está en prompts/p2/24-implement-004-t033.md.)

**Prompt (resumido):** T033: contrastar la línea base con la medición de puntos reducidos y registrar el comando, las condiciones y la justificación de proponer K=50.

**Para qué se usó:** Comparar las mediciones de la 004, sustentar la propuesta de K=50 y registrar el insumo de rendimiento pendiente para cerrar T033.

### 2026-11-18 — Codex CLI 0.169.0 (GPT-6.2 Sol)
**Prompt:**
```text
$speckit-implement Completa la elección de K para la 004. Confirmo K=50 como valor predeterminado con base en las mediciones de T041 y T042. Corrige en T033 la nota que trata la medición de retroceso con muchos cazadores como un bloqueo para elegir K y deja esa medición pendiente en T039. Registra en tasks.md el cambio de cripta/constantes.py antes de editar el código. Ajusta el valor predeterminado a 50 y verifica con una prueba que una partida iniciada sin --checkpoint-cada usa 50 y que un K explícito sigue funcionando. Ejecuta la suite completa, cita la medición a escala 1 que respalda K=50 y marca T033 al completar la validación. Registra el prompt en PROMPTS_LLM.md. Respeta CRLF y no hagas commits ni push.
```

(El texto completo está en prompts/p2/25-implement-004-k-predeterminado.md.)

**Prompt (resumido):** Confirmar K=50 como valor predeterminado, corregir la nota de T033 sobre la medición con cazadores y probar el valor al iniciar con y sin --checkpoint-cada.

**Para qué se usó:** Fijar K=50, comprobar la configuración al iniciar una partida y dejar el benchmark de retroceso con cazadores en T039.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo las pruebas de la Fase A de specs/004-linea-de-tiempo/tasks.md: T001 y T004. Antes lee spec.md, plan.md y data-model.md de specs/004-linea-de-tiempo/. Crea tests/modelo/test_linea_tiempo.py con clases de prefijo Test que citen los FR en comentarios. No crees ni modifiques nada en cripta/. Las pruebas deben fallar porque cripta/modelo/linea_tiempo.py aún no existe: córrelas y muéstrame que fallan por eso y no por otra razón. CRLF en el .py, sin ";" en comentarios, y no marques las tareas todavía. Dime qué casos cubriste."

**Prompt (resumido):** T001 y T004: pruebas de la clase LineaTiempo (límites temporales, numeración #k, puntos de control, recorte y consulta) antes del código.

**Para qué se usó:** Crear tests/modelo/test_linea_tiempo.py con clases Test y FR citados. Debían fallar porque cripta/modelo/linea_tiempo.py aún no existía.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T002, T003 y T005 de specs/004-linea-de-tiempo/tasks.md. Crea cripta/modelo/linea_tiempo.py con la clase LineaTiempo y la API exacta que fijan las pruebas de tests/modelo/test_linea_tiempo.py, sin modificar las pruebas. Usa listas contiguas y búsquedas binarias escritas a mano, sin bisect, heapq, collections, dict ni set como índice, y sin sorted ni .sort. Un docstring al inicio del módulo y un comentario corto por método, sin ";". CRLF. Corre py -m unittest tests.modelo.test_linea_tiempo y después la suite completa con py -m unittest discover -s tests -t . Marca T001, T002, T003, T004 y T005 como [X] en specs/004-linea-de-tiempo/tasks.md (LF). Dime el resultado de las dos corridas."

**Prompt (resumido):** T002, T003 y T005: implementación de LineaTiempo con listas contiguas y búsquedas binarias escritas a mano.

**Para qué se usó:** Crear cripta/modelo/linea_tiempo.py para que pasen las pruebas de la Fase A sin modificarlas y marcar T001 a T005.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo las pruebas de la Fase B de specs/004-linea-de-tiempo/tasks.md: T006, T007, T008 y T009. Antes lee la Fase B de tasks.md y las secciones «Registro de historia y reconstrucción» de plan.md, y revisa cómo arman partidas las pruebas existentes (tests/cripta_cazadores.py, tests/modelo/test_conocimiento_jugador.py y las de tests/servicios/ que usan ClienteOffline) para reutilizar esos ayudantes. Crea tests/modelo/test_partida_linea_tiempo.py con clases de prefijo Test que citen los FR y los casos B-LIN. Antes de escribir, fija y dime la API pública que usarán las pruebas en Partida para consultar la historia (por ejemplo consultar_instante(t) y consultar_accion(k) que devuelven una proyección de solo lectura), porque la implementación tendrá que respetarla. No modifiques nada en cripta/. Las pruebas deben fallar porque esa API aún no existe: córrelas y muéstrame que fallan por eso. CRLF, sin ";" en comentarios, no marques tareas. Dime qué casos cubriste y la API elegida."

**Prompt (resumido):** T006 a T009: pruebas de la consulta histórica de Partida (instantes, orden de eventos, pergamino, consulta sin efectos y resumen) y definición de su API pública.

**Para qué se usó:** Crear tests/modelo/test_partida_linea_tiempo.py. Debían fallar porque consultar_instante, consultar_accion y linea_tiempo aún no existían.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T010, T011, T012, T013 y T014 de specs/004-linea-de-tiempo/tasks.md, para que pasen las pruebas de tests/modelo/test_partida_linea_tiempo.py sin modificarlas. Sigue el diseño de plan.md: el checkpoint se toma en el punto de decisión del jugador que sigue a cada acción múltiplo de K, como estado completo en datos planos (reutiliza la proyección que ya arma crear_estado en persistencia_modelo.py, con el estado del random.Random), y la consulta reconstruye en una Partida aislada desde el checkpoint más cercano, re-simulando como máximo K acciones dentro de HistorialRetroceso.sin_registrar(), sin red ni precarga (reutiliza el contenido estático de las salas ya cargadas, T011), sin escribir en la bitácora de mensajes ni en partida.log, y sin tocar la partida viva. Al aceptar un pergamino, trunca la línea y registra el ajuste de inventario como dice el plan. Usa como valor por defecto de checkpoint_cada una constante provisional en cripta/constantes.py (por ejemplo 100), que se justificará con el bench en T033. Sin bisect, heapq, collections, sorted, .sort, ni dict o set como índice. CRLF, sin ";" en comentarios. Si alguna prueba te parece contradictoria con spec.md o plan.md, detente y explícamelo en vez de cambiarla. Corre el archivo de pruebas y luego la suite completa, marca T006 a T014 como [X] en tasks.md y dime el resultado y qué archivos tocaste." (El texto completo está en prompts/p2/16-implement-004-registro-y-reconstruccion.md.)

**Prompt (resumido):** T010 a T014: integración de la línea de tiempo en Partida con puntos de control, consulta por reconstrucción aislada, recorte por pergamino y valor provisional de K.

**Para qué se usó:** Hacer pasar test_partida_linea_tiempo.py sin modificarlo: registrar acciones, crear puntos de control, re-simular en una partida aislada y recortar la línea al usar un pergamino.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "En tests/modelo/test_partida_linea_tiempo.py, el ayudante _hacer usa resultado.motivo, pero el campo real de ResultadoAccion es motivo_rechazo. Corrígelo con Edit (solo eso) y corre el archivo de pruebas."

**Prompt (resumido):** Corrección de una línea de una prueba: resultado.motivo por motivo_rechazo.

**Para qué se usó:** El ayudante _hacer de test_partida_linea_tiempo.py usaba un campo que no existe en ResultadoAccion.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo las pruebas de la Fase C de specs/004-linea-de-tiempo/tasks.md: T015 y T016. Lee la Fase C de tasks.md y plan.md, y revisa tests/infraestructura/test_guardado_binario.py y cripta/infraestructura/guardado_binario.py para seguir su estilo. Las pruebas deben cubrir el ida y vuelta de la línea de tiempo (acciones, ajustes, checkpoints con el estado de random) y del conocimiento de la 002 (EstadoPartida.conocimiento, que hoy tiene compare=False y no se codifica), y que un archivo con la versión de la Parte I se rechace con un error claro sin modificarlo. No modifiques nada en cripta/. Las pruebas nuevas deben fallar ahora por la razón esperada: córrelas y muéstrame por qué fallan. CRLF, sin ";" en comentarios, no marques tareas. Dime qué casos cubriste."

**Prompt (resumido):** T015 y T016: pruebas del guardado binario de la línea de tiempo y del conocimiento, y del rechazo de la versión de la Parte I.

**Para qué se usó:** Ampliar tests/infraestructura/test_guardado_binario.py. Debían fallar porque el formato aún no guardaba la línea ni el conocimiento.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T017, T018 y T019 de specs/004-linea-de-tiempo/tasks.md, para que pasen las pruebas nuevas de tests/infraestructura/test_guardado_binario.py sin modificarlas. Respeta la API que fijaron esas pruebas en estado_guardado.py (AccionGuardada, AjusteGuardado, PuntoControlGuardado, LineaGuardada, EstadoPartida.linea y conocimiento con compare=True). En guardado_binario.py sube FORMATO_VERSION una sola vez y codifica la línea y el conocimiento de la 002, y rechaza la versión de la Parte I con CriptaFormatoIncompatibleError sin modificar el archivo. En persistencia_modelo.py y partida.py, guarda y restaura la línea vigente completa, de modo que una partida cargada pueda consultar instantes anteriores a la carga (hoy da ValueError). Sin dict ni set como índice, sin sorted, bisect ni collections. CRLF, sin ";" en comentarios. Si una prueba te parece contradictoria con spec.md o plan.md, detente y explícamelo. Corre el archivo de pruebas, tests/modelo/test_partida_linea_tiempo.py y la suite completa, marca T015 a T019 como [X] en tasks.md y dime el resultado y qué archivos tocaste." (El texto completo está en prompts/p2/17-implement-004-guardado-binario.md.)

**Prompt (resumido):** T017 a T019: formato binario nuevo que guarda y restaura la línea y el conocimiento, y rechaza los archivos de la Parte I.

**Para qué se usó:** Subir FORMATO_VERSION, codificar la línea y el conocimiento y hacer que una partida cargada conserve la línea y pueda consultar instantes anteriores a la carga.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "Sí, corrige test_el_resto_del_estado_no_cambia_por_llevar_linea comparando las salas por id, solo eso en la prueba. Además, como el formato ya pasó a la versión 2, agrega a EstadoPartida el contador de instancias (siguiente_instancia) y codifícalo en guardado_binario.py, para que una partida cargada numere los objetos igual que la original y los checkpoints creados después de cargar coincidan. Agrega una prueba de ida y vuelta para ese campo en tests/infraestructura/test_guardado_binario.py y una que compruebe que la partida cargada y la original asignan el mismo id al siguiente objeto recogido. Corre la suite completa, marca T015 y dime el resultado."

**Prompt (resumido):** Corrección de una prueba del guardado y contador de instancias en el estado guardado.

**Para qué se usó:** Comparar las salas por id en test_el_resto_del_estado_no_cambia_por_llevar_linea y guardar siguiente_instancia para que una partida cargada numere los objetos igual que la original.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo las pruebas de la Fase D de specs/004-linea-de-tiempo/tasks.md: T020, T021, T023 y T025. Lee la Fase D de tasks.md, el contrato specs/004-linea-de-tiempo/contracts/cli.md y spec.md (formato de historia <t>, historia #k, --checkpoint-cada K y --replay --hasta t). Revisa cómo están armadas las pruebas existentes del controlador, de la vista de consola, del servicio de partida y del replay, y amplíalas en sus archivos, con clases de prefijo Test y FR citados. No modifiques nada en cripta/. Las pruebas nuevas deben fallar ahora por la razón esperada: córrelas y muéstrame por qué fallan. CRLF, sin ";" en comentarios, no marques tareas. Dime qué casos cubriste y qué formato de salida fijan las pruebas." (El texto completo está en prompts/p2/18-implement-004-pruebas-fase-d.md.)

**Prompt (resumido):** T020, T021, T023 y T025: pruebas de historia en controlador y vista, de --checkpoint-cada en el servicio y de --replay --hasta, antes del código.

**Para qué se usó:** Ampliar las pruebas existentes del controlador, la vista, el servicio de partida y el replay, y fijar el formato de salida. Debían fallar porque nada de eso existía.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "En specs/004-linea-de-tiempo/ (plan.md, research.md, data-model.md, quickstart.md y tasks.md), reemplaza toda referencia a docs/ejemplos/partida_cripta-03.log por docs/ejemplos/partida_cripta-02.log, que es el ejemplo vigente con pergamino (el de cripta-03 se retiró al cambiar los ejemplos en la 001). Ajusta la descripción si menciona detalles del contenido del archivo viejo. Usa Edit, conserva los finales de línea y no toques nada fuera de esa carpeta."

**Prompt (resumido):** Cambiar las referencias al log de ejemplo retirado por el vigente en los documentos de la 004.

**Para qué se usó:** Que plan, research, data-model, quickstart y tasks citen docs/ejemplos/partida_cripta-02.log, el ejemplo con pergamino, y no el de cripta-03 que se retiró en la 001.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T022, T024 y T026 de specs/004-linea-de-tiempo/tasks.md, para que pasen las pruebas de la Fase D sin modificarlas, respetando el formato y la API que fijan. En VistaBase, mostrar_historia debe ser un método concreto (no abstracto) para no romper las vistas falsas que heredan de ella. El replay con --hasta no debe instanciar la vista ni el controlador. Sin dict ni set como índice, sin sorted, bisect ni collections. CRLF, sin ";" en comentarios. Si una prueba te parece contradictoria con spec.md o el contrato cli.md, detente y explícamelo. Corre la suite completa, marca T020 a T026 como [X] en tasks.md y dime el resultado y qué archivos tocaste." (El texto completo está en prompts/p2/19-implement-004-controlador-vista-cli.md.)

**Prompt (resumido):** T022, T024 y T026: comando historia en controlador y vista, --checkpoint-cada en servicio y línea de comandos, y --replay --hasta sin vista.

**Para qué se usó:** Hacer pasar las pruebas de la Fase D sin modificarlas y marcar T020 a T026.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T027 de specs/004-linea-de-tiempo/tasks.md: la prueba de la carga linea_tiempo. Revisa primero tests/bench/test_cargas_bench.py (la prueba de humo que ya recorre todas las cargas de CARGAS a escala mínima) y tests/servicios/, y no dupliques lo que ya cubre. La prueba debe comprobar que linea_tiempo está registrada en CARGAS, que corre sin instanciar la vista, que es determinista por semilla (dos corridas dan los mismos conteos) y que reporta K=100, 500, 1000 y sin checkpoints. No modifiques nada en cripta/. Debe fallar ahora porque la carga no existe: muéstrame por qué falla. CRLF, sin ";" en comentarios, no marques la tarea."

**Prompt (resumido):** T027: prueba de la carga linea_tiempo del benchmark.

**Para qué se usó:** Comprobar que está registrada en CARGAS, que corre sin vista, que es determinista por semilla y que reporta los escenarios de K. Debía fallar porque la carga no existía.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T028, T029, T030, T031 y T032 de specs/004-linea-de-tiempo/tasks.md, para que pasen las pruebas de tests/servicios/test_servicio_bench.py sin modificarlas. Implementa la carga linea_tiempo en cripta/bench/cargas_bench.py y regístrala en CARGAS y en servicio_bench.py. Indicaciones: 1. La partida de medición usa la cripta de referencia de fixtures/ (la misma constante CRIPTA_REFERENCIA que usa ciclo_referencia) con una semilla fija y un random.Random propio para elegir los pasos. Para que el jugador sobreviva miles de acciones, súbele la vida máxima en los datos generales ANTES de iniciar la partida (por ejemplo cargando los datos de la cripta en un cliente falso con la vida modificada), nunca después, porque la reconstrucción parte del estado inicial y daría otra partida. 2. A escala 1 son al menos 5 000 acciones del jugador. Con escalas menores la cantidad baja proporcionalmente, con un mínimo pequeño para que la prueba de humo sea rápida. 3. Para K=100, 500, 1000 y sin checkpoints, reporta la memoria de la línea (acciones, ajustes y checkpoints), la mediana y el máximo del tiempo de consulta sobre consultas en posiciones elegidas con la semilla, y si cumple el límite de 50 ms (P2 §6.1). Reporta también el peor tiempo de una acción que crea un checkpoint, comparado con el límite de 20 ms por ciclo. 4. Compara las alternativas descartadas que piden las tareas: re-simular frente a reconstruir hacia atrás (T030), búsqueda binaria frente a lineal del checkpoint y del límite temporal (T031), y recorte desde el final frente a escaneo y filtrado (T032). Para la memoria usa una estimación honesta y di en la nota cómo se calcula. 5. Llama a gc.collect() antes de cada corrida medida, como las demás cargas. Sin dict ni set como índice, sin sorted, bisect ni collections. CRLF, sin ";" en comentarios. Corre la prueba de la carga, la de humo de tests/bench y la suite completa. Después corre py -m cripta --bench --solo linea_tiempo una vez y pégame la salida completa. No elijas todavía el K por defecto (eso es T033). Marca T027 a T032 como [X] en tasks.md." (El texto completo está en prompts/p2/20-implement-004-carga-bench.md.)

**Prompt (resumido):** T028 a T032: carga linea_tiempo del benchmark con K=100, 500, 1000 y sin puntos, y comparación con las alternativas descartadas.

**Para qué se usó:** Implementar la carga en cargas_bench.py y registrarla en servicio_bench.py para que pasen sus pruebas, y correr el bench sin elegir todavía el K predeterminado.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "Optimización acotada, solo cripta/modelo/cripta_mapa.py y sus pruebas. Un perfil de consultar_accion muestra que el 40 % del tiempo es CriptaMapa.obtener (búsqueda binaria en VectorOrdenado, unas 238 000 llamadas en 10 consultas), llamado sobre todo desde BuscadorRutas, costo_de_conexion, puerta_transitable y vecinos. 1. Primero agrega en las pruebas de CriptaMapa (busca el archivo existente en tests/modelo/) casos que fijen el comportamiento de obtener: una sala existente, una inexistente, ids fuera de rango y salas agregadas en varias páginas en desorden. Deben pasar ya con el código actual. 2. Luego agrega en CriptaMapa un índice plano por id de sala (una lista indexada por id que se amplía al agregar páginas, sin dict ni set) para que obtener sea O(1). Mantén la interfaz pública igual y no cambies nada fuera de cripta_mapa.py. Corre la suite completa y después py -m cripta --bench --solo ciclo_referencia linea_tiempo, y pégame las dos salidas. CRLF, sin ";" en comentarios, sin sorted, bisect ni collections. No marques tareas." (El texto completo está en prompts/p2/21-optimizacion-cripta-mapa-004.md.)

**Prompt (resumido):** Índice plano por id de sala en CriptaMapa.obtener, con pruebas previas del comportamiento.

**Para qué se usó:** Reducir el costo de consultar_accion, donde un perfil mostró que obtener ocupaba el 40 % del tiempo, y medir el efecto con ciclo_referencia y linea_tiempo.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T034, T035 y T036 de specs/004-linea-de-tiempo/tasks.md: las pruebas de aceptación en tests/aceptacion/test_linea_tiempo.py (tests/aceptacion/__init__.py ya existe). Cubre los escenarios de aceptación de las historias de spec.md y los casos B-LIN del Apéndice B que no estén ya cubiertos en tests/modelo/test_partida_linea_tiempo.py, sin duplicarlos. Clases con prefijo Test y FR citados. No modifiques nada en cripta/. Deben pasar con el código actual: córrelas y dime el resultado. CRLF, sin ";" en comentarios. Marca T034 a T036 como [X]."

**Prompt (resumido):** T034 a T036: pruebas de aceptación de la línea de tiempo.

**Para qué se usó:** Crear tests/aceptacion/test_linea_tiempo.py con las historias de la especificación y los casos B-LIN no cubiertos por las pruebas del modelo, y que pasen con el código actual.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T037, T038 y T039 de specs/004-linea-de-tiempo/tasks.md. T037: corre py -m unittest discover -s tests -t . y anota el resultado en tasks.md. T038: audita importaciones y estructuras prohibidas (heapq, bisect, collections, networkx, sorted, .sort, dict o set como índice) en los archivos de cripta/ modificados o creados por la 004 y por el índice de cripta_mapa.py, y anota el resultado. T039: corre py -m cripta --bench --solo agenda historial ciclo partida ciclo_referencia y anota los resultados en tasks.md comparándolos con docs/bench/resultados_001_a.md. Di honestamente que la carga historial es sintética y no incluye cazadores. No cambies código salvo que encuentres una regresión real (en ese caso detente y dímelo). Marca T037 a T039 como [X] y pégame las salidas."

**Prompt (resumido):** T037 a T039: suite completa, auditoría de estructuras prohibidas y mediciones de la Parte I repetidas.

**Para qué se usó:** Anotar en tasks.md el resultado de la suite, la auditoría de los archivos de la 004 y la comparación del bench con resultados_001_a.md, dejando claro que la carga historial es sintética y no incluye cazadores.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "/speckit-implement Solo T040 de specs/004-linea-de-tiempo/tasks.md. Edita solo DECISIONES.md (CRLF, sin ";" en el texto nuevo) y marca T040. Lee antes DECISIONES.md completo (estilo y secciones 5.1 y 5.6), specs/004-linea-de-tiempo/spec.md, plan.md, research.md, tasks.md (T033, T039, T041 y T042) y docs/bench/resultados_004_linea_base.md y resultados_004_puntos_reducidos.md. Las cifras deben salir de esos archivos o de este prompt, sin inventar. 1. Agrega una sección "5.5 La línea de tiempo" con la estructura de la Parte I (Problema, Alternativas, Decisión, Complejidad, Evidencia, Límites), enlaces a spec.md y plan.md de la 004 y si la decisión coincide con el plan original y qué medición motivó cada cambio. Incluye: re-simular desde el checkpoint frente a reconstruir hacia atrás, búsqueda binaria frente a lineal, recorte desde el final frente a filtrado, restauración materializada frente a preparar salas, la tabla de K=50, 100, 500, 1000 y sin checkpoints, y por qué K=50. 2. Cambios motivados por mediciones (no estaban en el plan): a. Índice plano por id en CriptaMapa.obtener (O(1) en lugar de búsqueda binaria). Un perfil mostró que el 83 % de una consulta era re-simular y el 40 % del total era obtener. Antes del índice, en el mismo equipo, el bench de linea_tiempo dio con K=100 mediana 66 ms y máximo 118 ms, K=500 263 y 523 ms, K=1000 512 y 1110 ms, sin checkpoints 2083 y 5318 ms. Después del índice, K=100 dio mediana 31.8 ms y máximo 54.6 ms. ciclo_referencia pasó de 3.144 ms (resultados_001_a.md) a 2.541 ms. b. Puntos de control reducidos (T042), con su ahorro de memoria. 3. Mide el tamaño del archivo de guardado con K=50 para 1 000 y 5 000 acciones, jugando la partida con el ayudante _jugar_linea de cargas_bench.py y guardando con ServicioPartida.guardar, y anota el comando o script usado. Aclara que la memoria del bench es una cota superior (suma objetos compartidos) y el archivo es el tamaño real en disco. 4. Límites conocidos: el estado cambiado a mano fuera de las acciones no se puede reconstruir; si una ficha fue desalojada de la caché, la reconstrucción puede leer disco o red; una partida cargada conserva el K con que se guardó; PuntoControlGuardado.siguiente_instancia repite el valor de su estado; el costo del historial con cazadores sigue sin medirse; el criterio de la cripta de referencia (constante frente a la de más salas) queda pendiente del grupo. 5. En la sección 5.6 agrega un párrafo con la revisión de la Parte I hecha en T039 (agenda, historial, ciclo, partida y ciclo_referencia) y el índice de CriptaMapa como cambio de una decisión de la Parte I. En 5.1, en "Alternativa no implementada", agrega una frase que remita a 5.5: la consulta de salas por id ya es O(1). Dime qué cambiaste." (El texto completo está en prompts/p2/26-decisiones-004.md.)

**Prompt (resumido):** T040: sección 5.5 de DECISIONES.md con la línea de tiempo, más un párrafo en 5.6 y una frase en 5.1.

**Para qué se usó:** Documentar las decisiones con la estructura de la Parte I, las cifras de docs/bench, el índice de CriptaMapa, los puntos reducidos y el tamaño del archivo de guardado.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "Tres ajustes en DECISIONES.md, sección 5.5: 1. Ahora existe docs/bench/resultados_004_antes_indice.md, medido en el commit anterior al índice de CriptaMapa en el mismo equipo. Reemplaza las cifras de «antes del índice» por las de ese archivo, citándolo, y quita el límite que dice que esas cifras no tienen archivo. Ese bench es la versión vieja de la carga (sin K=50 y con 16 consultas en vez de 21), así que compara solo los escenarios que existen en los dos archivos y aclara esa diferencia. 2. El equipo es el mismo Equipo B de la tabla del inicio: agrega 5.5 a su fila y ajusta la frase de la sección. 3. Verifica la descripción de «Decisión» leyendo cripta/modelo/linea_tiempo.py y los métodos de la línea de tiempo en cripta/modelo/partida.py, y corrígela para que describa lo que hace el código. Usa Edit, CRLF y sin ";". Dime qué cambiaste." (El texto completo está en prompts/p2/27-decisiones-004-ajustes.md.)

**Prompt (resumido):** Tres ajustes de la sección 5.5: cifras de antes del índice, equipo y descripción de la decisión.

**Para qué se usó:** Usar el archivo medido antes del índice en lugar de cifras del prompt, ubicar la medición en el Equipo B y corregir la descripción para que coincida con el código.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "Actualiza solo README.md para la capacidad 004, sin tocar otros archivos: agrega los comandos historia <t> e historia #k a la sección de controles o del juego, las banderas --checkpoint-cada K (valor por defecto 50, entero mayor o igual a 1) y --replay ... --hasta t a la tabla de banderas y a la sección de replay, con un ejemplo usando docs/ejemplos/partida_cripta-02.log, y la carga linea_tiempo a la lista de --solo. Agrega también una frase de que el guardado usa ahora la versión 2 del formato y que un archivo de la Parte I se rechaza con un error claro sin modificarlo. Usa Edit, CRLF y sin ";". Dime qué cambiaste."

**Prompt (resumido):** README de la 004: comandos historia, banderas --checkpoint-cada y --hasta, carga linea_tiempo y formato v2.

**Para qué se usó:** Documentar el uso de la línea de tiempo y que un archivo guardado de la Parte I se rechaza con un error claro sin modificarlo.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "Dos cambios, con pruebas antes del código, y documentos al final. 1. Cripta de referencia: en cripta/bench/cargas_bench.py, ciclo_referencia usa la constante CRIPTA_REFERENCIA = "cripta-06", mientras linea_tiempo elige la cripta con más salas del listado. La constitución prohíbe datos de una cripta concreta en el código. Extrae a una función común la elección de linea_tiempo (la de más salas, desempate por id) y úsala en las dos cargas. Elimina la constante. Ajusta la prueba existente si alguna depende de ella. 2. Retroceso con cazadores (P2 §5.6): agrega una carga historial_cazadores en cargas_bench.py y regístrala en CARGAS. Sobre la cripta de referencia, con los cazadores activos como en ciclo_referencia, mide por cada acción del jugador cuántas operaciones inversas registra su intervalo y cuánto tarda revertir el último intervalo como lo hace el pergamino, con mediana y máximo, y compáralo con la carga historial sintética de la Parte I. Agrega su prueba en tests/servicios/test_servicio_bench.py antes del código. Corre la suite completa y py -m cripta --bench --solo ciclo_referencia historial historial_cazadores, y pégame la salida. Después agrega el resultado a DECISIONES.md, en el párrafo de la sección 5.6 que dice que el retroceso con cazadores no se midió, y quita esa nota pendiente de 5.5 y de tasks.md (T039). Sin dict ni set como índice, sin sorted, bisect ni collections. CRLF, sin ";" en comentarios ni en el texto nuevo." (El texto completo está en prompts/p2/28-implement-004-cripta-referencia-historial-cazadores.md.)

**Prompt (resumido):** Elegir la cripta de referencia con una función común en las cargas con partida real y eliminar la constante, y agregar la carga historial_cazadores que mide el retroceso con cazadores, con pruebas antes del código y los resultados en DECISIONES.md y tasks.md.

**Para qué se usó:** Quitar de cargas_bench.py el id de una cripta concreta, que la constitución prohíbe, medir cuántas inversas registra una acción con cazadores activos y cuánto tarda revertirla como el pergamino, y comparar con la carga sintética de la Parte I.

### 2026-11-18 — Claude Code (Sonnet 5.5)
**Prompt:** "Sí, actualiza esas dos cosas: la línea 15 de tasks.md y T040 para que digan que la cripta de referencia ya se elige con la función común, y agrega historial_cazadores a la lista de --solo del README y a la de «Cómo se reproduce» de DECISIONES.md (revisa que linea_tiempo también esté en las dos). Edit, CRLF y sin ";"."

**Prompt (resumido):** Actualizar la línea 15 de tasks.md y T040 con la elección común de la cripta de referencia, y agregar historial_cazadores y linea_tiempo a las listas de --solo del README y de DECISIONES.md.

**Para qué se usó:** Que la documentación dejara de decir que el criterio de la cripta de referencia estaba pendiente y que las listas de cargas coincidieran con las registradas en CARGAS.


### 2026-11-18 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Estoy en la rama 002-niebla-ir-a-fases-c-d con un git merge origin/main en curso que quedó con conflictos. No crees ni cambies de rama, no abortes el merge, no hagas commit ni push y no uses git add. Resuelve solo estos archivos: DECISIONES.md, cripta/bench/cargas_bench.py, cripta/controlador/controlador_cripta.py, cripta/servicios/servicio_replay.py, cripta/vista/vista_base.py, cripta/vista/vista_consola.py, tests/controlador/test_controlador_cripta.py, tests/servicios/test_servicio_bench.py y tests/vista/test_vista_consola.py. No toques PROMPTS_LLM.md, que ya resolví a mano. Contexto: el lado HEAD trae la capacidad 002 (niebla de guerra, mapa conocido, ir a, carga niebla_rutas, comentario de viaje en partida.log) y origin/main trae la capacidad 004 (comandos historia, --checkpoint-cada, --replay --hasta, cargas linea_tiempo e historial_cazadores, guardado binario versión 2). Se conserva todo de ambos lados, sin perder código de ninguno. 1. En cada bloque conserva lo de los dos lados y une imports, parámetros, métodos abstractos, comandos y pruebas, sin duplicados. 2. DECISIONES.md: en el primer bloque (lista de cargas de «Cómo se reproduce») deja una sola lista con todas las cargas registradas en CARGAS de cargas_bench.py. En el segundo bloque deja la sección 5.3 de la 002 y después la 5.5 de la 004, sin cambiar su texto. 3. cargas_bench.py: la tupla CARGAS conserva niebla_rutas, historial_cazadores y linea_tiempo. No reintroduzcas la constante CRIPTA_REFERENCIA y conserva elegir_cripta_de_referencia y cripta_de_referencia. 4. tests/servicios/test_servicio_bench.py es un conflicto add/add: conserva las clases de pruebas de los dos lados con un solo bloque de imports. 5. servicio_replay.py: conserva --hasta de la 004 y el comentario de viaje de la 002, y que los números de línea del replay sigan contando igual. 6. Sin heapq, bisect, collections, networkx, set ni dict como índice, y sin sorted ni list.sort() en lo que escribas. En comentarios y textos nuevos no uses ';'. Conserva los finales de línea CRLF de cada archivo. No uses sed -i. 7. No agregues reglas del juego. Si una resolución no es obvia o cambia el resultado observable, detente y pregunta. Al terminar verifica: git diff --name-only --diff-filter=U sin resultados, ninguna marca <<<<<<<, ======= ni >>>>>>> en esos archivos (git grep -n -e '^<<<<<<<' -e '^=======' -e '^>>>>>>>' -- cripta tests DECISIONES.md), y corre py -m unittest discover -s tests -t . completo. Dime cuántas pruebas pasan y, si falla alguna, en qué archivo y por qué, sin corregirla fuera de los conflictos. Dime qué decidiste por archivo."

**Prompt (resumido):** Resolver los conflictos del merge de origin/main (capacidad 004) en la rama de la 002, conservando el código de ambos lados, y correr la suite completa.

**Para qué se usó:** Fusionar la línea de tiempo con la niebla de guerra y el viaje ir a en los comandos, la vista, el replay, las cargas del bench, DECISIONES.md y las pruebas, sin perder lo de ninguna de las dos capacidades.


### 2026-11-18 — Antigravity CLI (Gemini)
**Prompt:** "/speckit-implement Sigue las instrucciones de prompts/p2/18-implement-002.md. Solo T040. No hagas commit ni push. Solo T040 de specs/002-niebla-ir-a/tasks.md. Estoy en la rama 002-niebla-ir-a-fases-c-d con el merge de main ya resuelto y commiteado. No crees ni cambies de rama y no hagas commit ni push. Lee solo los archivos que se nombran aquí y no corras scripts de verificación amplios. 1. Lee la tarea T040, FR-NIE-006 y SC-NIE-005 de specs/002-niebla-ir-a/spec.md, cripta/infraestructura/guardado_binario.py, cripta/infraestructura/estado_guardado.py, cripta/modelo/persistencia_modelo.py, tests/servicios/test_servicio_partida_guardado.py y tests/infraestructura/test_guardado_binario.py. La 004 ya subió el formato binario a la versión 2 y guarda el conocimiento del jugador y la línea de tiempo. No cambies el formato ni la versión y no definas bytes. 2. Primero la prueba. En tests/servicios/test_servicio_partida_guardado.py (Modificado) agrega, solo si no existe ya una equivalente, una prueba que juegue una partida con niebla (salas exploradas y avistadas, una puerta observada y recordada, la antorcha encendida en algún momento), la guarde con ServicioPartida en el archivo binario, la cargue en un servicio nuevo y compruebe que el conocimiento (estado de cada sala, observaciones de puertas y costos de salida) coincide con el de la partida original, que ir a calcula la misma ruta y que historia de un instante anterior muestra el mismo mapa conocido que antes de guardar. Cita FR-NIE-006 y SC-NIE-005 en el comentario de la prueba. 3. Si ya existen pruebas que cubren parte de eso (revisa test_proyecta_y_restaura_conocimiento_y_permite_retroceso_nuevo, test_conocimiento_completo_de_puertas_se_conserva_al_restaurar y las de la 004), no las dupliques: dime cuáles cubren qué y agrega solo lo que falte. 4. Si la prueba nueva falla porque el código no restaura algo, detente y dime qué falta, sin corregir código fuera de lo pedido. 5. Corre py -m unittest tests.servicios.test_servicio_partida_guardado y después py -m unittest discover -s tests -t . completo, y dime los resultados. 6. Marca T040 en tasks.md y cambia «Depende de 004» por un texto que diga que la 004 ya está fusionada, sin tocar otras tareas. Revisa si DECISIONES.md 5.3 o plan.md dicen que el guardado binario del conocimiento está pendiente de la 004 y, si lo dicen, corrígelo con una frase. 7. Sin heapq, bisect, collections, networkx, set ni dict como índice, y sin sorted ni list.sort(). En comentarios y textos nuevos no uses ';'. Conserva CRLF. No uses sed -i. 8. No agregues reglas del juego. Si falta algo o cambia el resultado observable, detente y pregunta. Al terminar dime qué cambiaste por punto y verifica con git diff que solo cambiaron tests/servicios/test_servicio_partida_guardado.py, specs/002-niebla-ir-a/tasks.md y, si hizo falta, DECISIONES.md o specs/002-niebla-ir-a/plan.md."

**Prompt (resumido):** T040 de la 002: prueba binaria de guardar y cargar el conocimiento del jugador sobre el formato versión 2 de la 004, y marcar la tarea.

**Para qué se usó:** Confirmar que el conocimiento, la ruta de ir a y la historia de la 004 se restauran tras guardar y cargar, y cerrar T040 de la 002. Se pasó a Antigravity porque la cuota de Codex se agotó.


### 2026-11-18 — Antigravity CLI (Gemini)
**Prompt:** "Corrige solo estos archivos: cripta/controlador/controlador_cripta.py, cripta/bench/cargas_bench.py y tests/servicios/test_servicio_partida_guardado.py. No toques otros archivos. Estoy en la rama 002-niebla-ir-a-fases-c-d. No crees ni cambies de rama y no hagas commit ni push. Lee solo esos tres archivos y tests/servicios/test_servicio_bench.py. No corras scripts de verificación amplios. Es la revisión del PR de la capacidad 002. 1. dict como tabla de búsqueda en el controlador. En cripta/controlador/controlador_cripta.py el método _avisar_motivo_viaje arma mensajes = {...} y lo consulta con mensajes.get(motivo, ...). La constitución prohíbe el dict como tabla de búsqueda. Reemplázalo por una cadena de if o por una tupla de pares (motivo, mensaje) recorrida a mano con un for. Deja exactamente los mismos cuatro mensajes (destino_inexistente, destino_no_explorado, sala_actual, sin_ruta) y el mismo mensaje por defecto «No se puede iniciar el viaje.», sin cambiar lo que ve el jugador. Si no existe una prueba que cubra los cuatro motivos y el motivo desconocido, agrégala primero en tests/controlador/test_controlador_cripta.py, solo para eso, y comprueba que pasa antes y después del cambio. 2. Elección de la cripta en niebla_rutas. En cripta/bench/cargas_bench.py la carga niebla_rutas elige la cripta con su propia función _elegir_fixture_referencia, mientras la 004 agregó la función común elegir_cripta_de_referencia (y cripta_de_referencia). El criterio es el mismo (la de más salas, desempate por menor id), así que quita el código duplicado: que niebla_rutas obtenga el id con cripta_de_referencia() y use lo demás sin cambios. Si tests/servicios/test_servicio_bench.py importa _elegir_fixture_referencia, ajusta esa prueba para que use la función común, o deja _elegir_fixture_referencia como un envoltorio de una línea que llame a la común. Si el cambio altera lo que mide o devuelve niebla_rutas, o el resultado de alguna prueba de equivalencia, detente y pregunta. 3. Punto y coma en un comentario. En tests/servicios/test_servicio_partida_guardado.py hay un comentario nuevo con ';' («vecinas avistadas; puerta observada»). Reescríbelo con coma o dos frases. Busca también cualquier otro ';' en los comentarios que agregué en este archivo y quítalo. Reglas: sin heapq, bisect, collections, networkx, set ni dict como índice, y sin sorted ni list.sort(). En comentarios y textos nuevos no uses ';'. Conserva los finales de línea CRLF de cada archivo. No uses sed -i. No agregues reglas del juego. Si falta algo o cambia el resultado observable, detente y pregunta. Al terminar corre py -m unittest discover -s tests -t . completo y dime cuántas pasan. Comprueba con Select-String que no queda un dict como tabla de búsqueda en controlador_cripta.py. Dime qué cambiaste por punto y verifica con git diff que solo cambiaron los archivos indicados."

**Prompt (resumido):** Corregir los puntos de la revisión del PR de la 002: quitar el dict como tabla de búsqueda del aviso de viaje, reutilizar la función común de cripta de referencia en niebla_rutas y quitar un ";" de un comentario.

**Para qué se usó:** Cumplir la regla de la constitución sobre el dict en el controlador, eliminar código duplicado en el bench y corregir el comentario.


### 2026-11-18 — Antigravity CLI (Gemini)
**Prompt:** "/speckit-implement Sigue las instrucciones de prompts/p2/01-cierre.md. No hagas commit ni push. Estoy en la rama cierre. No crees ni cambies de rama y no hagas commit ni push. Lee solo los archivos que se nombran aquí y no corras scripts de verificación amplios. 1. Primero la prueba. Crea tests/scripts/test_revisar_prohibidos.py (Nuevo), con tests/scripts/__init__.py si no existe. Cada caso escribe un archivo .py temporal con unittest y tempfile y comprueba los errores, los avisos y el código de salida: importación prohibida, sorted, .sort, id de cripta concreto, dict literal, ';' en un comentario y código limpio. Debe fallar antes de crear el script. 2. Crea scripts/revisar_prohibidos.py (Nuevo), sin dependencias fuera de la biblioteca estándar (ast y tokenize), con nombres de funciones y variables en español. Se ejecuta con py -m scripts.revisar_prohibidos y recorre los .py de cripta/. Reporta como ERROR, con ruta y línea: a) importaciones de heapq, bisect, collections y networkx (import y from ... import), b) llamadas a sorted(...) y a .sort(...), c) ids de cripta o de entidad concretos escritos como cadenas (cripta-NN y ent_...). Reporta como AVISO, para revisión manual: d) literales de dict y set y llamadas a dict(...) y set(...) dentro de cripta/modelo, cripta/estructuras, cripta/servicios y cripta/controlador (el dict que devuelve json y lo de infraestructura, dto y vista quedan fuera), e) ';' dentro de comentarios, leídos con tokenize y sin contar docstrings ni cadenas. Al final imprime el conteo de errores y de avisos. El código de salida es 1 si hay errores y 0 si solo hay avisos. Cabecera de máximo 5 líneas y 1 o 2 comentarios por método. 3. En cripta/servicios/servicio_bench.py, SubsistemaDesconocidoError usa sorted(pedidos) y ServicioBench.ejecutar usa un set de nombres válidos, set(subsistemas) y el operador in sobre subsistemas. Reemplázalo por listas y recorridos a mano, sin set, dict ni sorted. Si una prueba espera los nombres desconocidos en orden alfabético, ordénalos con la función de ordenamiento propia del proyecto en cripta/estructuras/ordenamiento_selector.py y no con sorted. No cambies el mensaje del error ni el orden de ejecución de las cargas. 4. Corre py -m unittest tests.scripts.test_revisar_prohibidos, py -m unittest tests.servicios.test_servicio_bench, py -m unittest discover -s tests -t . completo y py -m scripts.revisar_prohibidos. Dime los resultados y los avisos que salgan, sin corregir los avisos. Reglas: en comentarios y textos nuevos no uses ';'. Conserva CRLF. No uses sed -i. No agregues reglas del juego. Si falta algo o cambia el resultado observable, detente y pregunta. Al terminar dime qué cambiaste por punto y verifica con git diff que solo cambiaron scripts/revisar_prohibidos.py, tests/scripts/test_revisar_prohibidos.py, sus __init__.py y cripta/servicios/servicio_bench.py."

**Prompt (resumido):** Crear el script de auditoría de estructuras prohibidas con su prueba y quitar el set y el sorted de servicio_bench.

**Para qué se usó:** Tener una comprobación repetible de la constitución para la defensa y dejar servicio_bench sin estructuras prohibidas.


### 2026-11-18 — Antigravity CLI (Gemini)
**Prompt:** "/speckit-implement Sigue las instrucciones de prompts/p2/02-cierre.md. No hagas commit ni push. Estoy en la rama cierre. No crees ni cambies de rama y no hagas commit ni push. No escribas fuera del repo ni crees py.cmd. Usa .\.venv\Scripts\python.exe en lugar de py para correr los comandos. Lee solo los archivos que se nombran aquí y no corras scripts de verificación amplios. 1. Ids sintéticos en cripta/bench/cargas_bench.py. El script scripts/revisar_prohibidos.py marca como ERROR 'ent_rata_gigante' (línea 427) y 'ent_rata' (línea 470). Son ids inventados de datos sintéticos de la carga. Cámbialos por ids neutros que no empiecen con ent_ ni con cripta-, por ejemplo enemigo-sintetico-a y enemigo-sintetico-b, de forma consistente en toda la carga. Si una prueba en tests/ depende de esos ids, ajusta solo esa prueba. No cambies lo que mide la carga. 2. Punto y coma en comentarios. Reemplaza el ';' por una coma, un punto o dos frases en estos comentarios de cripta/, conservando el significado y sin tocar código, cadenas ni docstrings: cripta/__main__.py:53, cripta/bench/cargas_bench.py:489, 522 y 597, cripta/constantes.py:49, cripta/controlador/controlador_cripta.py:50, 80, 238, 250, 293, 329, 345, 353 y 407, cripta/infraestructura/estado_guardado.py:16, 17, 18, 21 y 67, cripta/infraestructura/guardado_binario.py:90, cripta/modelo/partida.py:496 y 548, cripta/modelo/persistencia_modelo.py:134, cripta/modelo/reloj.py:27, cripta/modelo/reversible.py:10, cripta/modelo/sala.py:58, 80 y 98, cripta/servicios/servicio_catalogo.py:139, cripta/vista/vista_consola.py:32, 56, 189, 299 y 344. Los números de línea pueden haberse movido por el punto 1: guíate por el texto del comentario. En comentarios estilo tabla, como los de estado_guardado.py, usa coma o barra en lugar de ';'. 3. No toques los avisos de dict de accion.py, servicio_bench.py y servicio_partida.py, que son falsos positivos (JSON del log, encabezados de bitácora y resultados del reporte). 4. Corre .\.venv\Scripts\python.exe -m scripts.revisar_prohibidos y confirma 0 errores y ningún aviso de punto y coma. Solo deben quedar los 5 avisos de dict. Corre después .\.venv\Scripts\python.exe -m unittest discover -s tests -t . completo y dime los resultados. Reglas: en comentarios y textos nuevos no uses ';'. Conserva CRLF. No uses sed -i. No cambies comportamiento ni agregues reglas del juego. Si falta algo o cambia el resultado observable, detente y pregunta. Al terminar dime qué cambiaste por punto y verifica con git diff que solo cambiaron comentarios y los ids sintéticos en archivos de cripta/ y, si hizo falta, tests/."

**Prompt (resumido):** Cambiar los ids sintéticos del bench por ids neutros y quitar el punto y coma de los comentarios de cripta/ para que la auditoría quede sin errores.

**Para qué se usó:** Dejar scripts/revisar_prohibidos.py con 0 errores y sin avisos de punto y coma, cumpliendo la regla de comentarios de la constitución.
