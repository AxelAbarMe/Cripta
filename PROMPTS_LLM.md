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
7. Usa en T021, T022 y T025 los nombres reales de cripta/modelo/reloj.py: <pega aquí el resultado
   de Select-String>."

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

**Para qué se usó:** Incorporar las correcciones de la revisión de saull04 antes de fusionar el PR de documentación.


### 2026-11-16 — Codex CLI 0.169.0 (GPT-6 Luna)
**Prompt:** "Corrige solo tasks.md y plan.md de la capacidad 002: referencia de la tarea que depende de 004, citar el escenario 3.18 en lugar de B-NIE-007, criterio de hecho de la implementación de vistas, etiqueta de dependencia con 001 y ubicar la comparación de costos guardados en la prueba y la carga del harness."

**Prompt (resumido):** Segunda corrección de tasks.md de la 002 tras la revisión del Pull Request: referencias, etiquetas y ubicación de la comparación de costos.

**Para qué se usó:** Dejar las tareas consistentes con la spec y el plan antes de fusionar el PR de documentación.


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


### 2026-11-18 — Antigravity CLI 1.5.6 (Gemini 3.8 Flash)
**Prompt:**
```text
/speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad
Sigue las instrucciones de prompts/p2/16-implement-003-fase-a-pruebas.md. Solo T001 a T004. No sigas con T005.
```
(El texto completo está en prompts/p2/16-implement-003-fase-a-pruebas.md.)

**Prompt (resumido):** Pruebas de dominio de la resolubilidad (T001 a T004): esqueleto con fixtures sintéticos, recorrido incremental, diagnóstico, determinismo, enemigos y comparación con la alternativa ingenua.

**Para qué se usó:** Escribir primero las pruebas que fijan la API del verificador, antes de implementar el módulo de dominio.

### 2026-11-18 — Antigravity CLI 1.5.10 (Claude Sonnet 4.6 Thinking)
**Prompt:**
```text
/speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/003-resolubilidad
Sigue las instrucciones de prompts/p2/17-implement-003-fase-a-nucleo.md. Solo T005 a T007. No sigas con T008.
```
(El texto completo está en prompts/p2/17-implement-003-fase-a-nucleo.md.)

**Prompt (resumido):** Núcleo del verificador de resolubilidad (T005 a T007): clases de datos inmutables, catálogo ordenado con búsqueda binaria propia y recorrido incremental con cola y montículo.

**Para qué se usó:** Implementar el dominio puro de la resolubilidad para que pasen las pruebas escritas en el paso anterior.