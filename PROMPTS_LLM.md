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
**Prompt:** "Corrige solo documentos de specs/001-terreno-cazador/ según el estado actual del servidor. (El texto completo, con el seguimiento que agregó T036b, está en prompts/p2/08-estado-servidor-001.md.)"

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
