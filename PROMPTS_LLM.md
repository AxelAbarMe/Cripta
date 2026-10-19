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

