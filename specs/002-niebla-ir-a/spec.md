# Especificación de Funcionalidad: Niebla de Guerra e «Ir a»

**Rama de la funcionalidad**: `002-niebla-ir-a`

**Creado**: 2026-11-14

**Estado**: Borrador

**Entrada**: Descripción del usuario: capacidad de niebla de guerra, mapa conocido, antorcha y viaje automático «ir a», conforme a Parte II §3.3, §3.4, §5.3 y Apéndice B.

## Aclaraciones

### Sesión 2026-11-14

- P: Cuando la antorcha explora una sala vecina, ¿qué debe recordar el mapa sobre las puertas de esa sala que no conectan con la sala donde está el jugador, y puede «ir a» cruzarlas? → R: La puerta entre la sala del jugador y la vecina explorada por antorcha se observa en ese momento. Las demás puertas de la vecina quedan no observadas hasta que el jugador entre a esa sala o a la sala del otro lado; «ir a» no puede cruzarlas mientras sigan no observadas.
- P: Si al completar un paso coinciden varios motivos de detención, ¿cuáles se informan, cuentan como enemigos solo los que siguen vivos y cuándo se evalúa el daño? → R: Se informan todos los motivos coincidentes en orden fijo y determinista: llegada al destino, enemigos vivos en la sala, daño recibido. El daño se evalúa al terminar de resolverse el paso y sus eventos. Si el daño mata al jugador, se aplican las reglas de fin de partida de la Parte I y no se informa un viaje.
- P: ¿Qué ocurre si el destino de «ir a» es la sala actual o si el viaje empieza en una sala con enemigos vivos? → R: Si el destino es la sala actual, se informa que el jugador ya está allí, sin efecto, tiempo, pasos ni registro en `partida.log`. Si el viaje empieza en una sala con enemigos vivos, se permite; la detención por enemigos solo se aplica al entrar a una sala. El primer paso se ejecuta con normalidad y el viaje se detiene por las reglas habituales.
- P: ¿Consultar el mapa conocido consume tiempo, se registra o altera el historial de retroceso, y qué registro deja una orden «ir a» rechazada o sin pasos? → R: Consultar el mapa no consume tiempo, no se registra ni altera el historial de retroceso. Las órdenes «ir a» rechazadas —incluidos destino no explorado, inexistente o igual a la sala actual— y las que no tienen ruta conocida desde el inicio no consumen tiempo, no se registran ni alteran el historial. Para un viaje que ejecuta pasos, el comentario se escribe una sola vez por orden, inmediatamente antes de la línea del primer movimiento, y permanece aunque el viaje se detenga después.
- P: Al apagar la antorcha, ¿se conserva lo que ya exploró mientras estuvo encendida? → R: Sí, se conserva. Según Parte II §3.3, la antorcha explora vecinas al entrar a una sala, por lo que encenderla dentro de una sala no explora en ese momento; el conocimiento generado por una entrada, incluidas sus observaciones de puertas, se revierte junto con esa entrada mediante el pergamino.

## Escenarios de Usuario y Pruebas *(obligatorio)*

### Historia de Usuario 1: Consultar lo conocido del laberinto (Prioridad: P1)

Como jugador, quiero distinguir las salas exploradas, avistadas y desconocidas, y consultar el mapa que conozco, para decidir por dónde avanzar sin recibir información que todavía no he descubierto.

**Por qué esta prioridad**: El mapa conocido determina la información disponible durante toda la partida y es la base del viaje automático.

**Prueba independiente**: Iniciar una partida y comprobar el estado inicial, las salidas visibles y cómo cambia el conocimiento al entrar a salas y al observar puertas.

**Escenarios de aceptación**:

1. **Dado** que comienza una partida, **Cuando** el jugador consulta el mapa conocido, **Entonces** la sala inicial figura como explorada y las salas que son destino de sus salidas figuran como avistadas.
2. **Dado** que una sala está explorada, **Cuando** el jugador consulta sus datos conocidos, **Entonces** ve su nombre, sus salidas, el costo de cada salida y el estado recordado de sus puertas según la última observación; la consulta no consume tiempo, no se registra ni altera el historial de retroceso.
3. **Dado** que una sala no explorada es destino de una salida de una sala explorada, **Cuando** el jugador consulta el mapa conocido, **Entonces** esa sala figura como avistada y solo se indica que existe una sala detrás de la salida.
4. **Dado** que una sala no explorada no es destino de una salida de una sala explorada, **Cuando** el jugador consulta el mapa conocido, **Entonces** no se revela información de esa sala y permanece desconocida.
5. **Dado** que una puerta conecta dos salas, **Cuando** el jugador está en cualquiera de ellas, **Entonces** observa su estado y el mapa conserva ese último estado observado aunque posteriormente cambie en la realidad.

### Historia de Usuario 2: Explorar con la antorcha encendida (Prioridad: P1)

Como jugador, quiero que la antorcha revele las salas vecinas al entrar a una sala, para ampliar mi conocimiento del mapa sin activar amenazas en esas vecinas.

**Por qué esta prioridad**: La antorcha altera el alcance de la exploración y afecta las decisiones del jugador, por lo que debe integrarse con las reglas de descubrimiento y retroceso.

**Prueba independiente**: Entrar a una sala con la antorcha encendida y comparar el conocimiento antes y después, así como el estado de enemigos y trampas de sus vecinas.

**Escenarios de aceptación**:

1. **Dado** que la antorcha está encendida y el jugador entra a una sala, **Cuando** se actualiza el mapa conocido, **Entonces** también quedan exploradas todas las salas vecinas mediante cualquier salida, abierta o cerrada, con nombre y salidas revelados, sin revelar su contenido ni activar sus enemigos o trampas; se observa la puerta entre la sala del jugador y cada vecina, pero las demás puertas de esas vecinas quedan no observadas.
2. **Dado** que una entrada con antorcha encendida exploró salas vecinas que antes no estaban exploradas, **Cuando** el jugador usa un pergamino para revertir esa entrada, **Entonces** esas salas vuelven exactamente al estado de conocimiento previo a la entrada.

### Historia de Usuario 3: Viajar automáticamente a una sala conocida (Prioridad: P1)

Como jugador, quiero ordenar «ir a» una sala explorada y que el personaje avance por una ruta económica conocida mientras el mundo sigue funcionando, para reducir movimientos manuales sin perder el control ante peligros o cambios del camino.

**Por qué esta prioridad**: Permite desplazarse entre destinos ya conocidos y conserva las reglas ordinarias de movimiento, tiempo y eventos.

**Prueba independiente**: Emitir una orden de viaje en un mapa conocido con rutas alternativas y observar cada paso, su costo, los eventos y la condición de detención.

**Escenarios de aceptación**:

1. **Dado** que el destino solicitado no está explorado o no existe, **Cuando** el jugador emite «ir a <sala>», **Entonces** la orden se rechaza, no se ejecuta ningún movimiento, no se consume tiempo, no se registra y no altera el historial de retroceso.
2. **Dado** que hay varias rutas conocidas hasta el destino, **Cuando** el jugador inicia el viaje, **Entonces** se elige una ruta que minimiza la suma de costos, usando solo salas exploradas y salidas que el mapa recuerda abiertas, y en empate el primer paso se dirige a la vecina de menor identificador.
3. **Dado** que el viaje tiene un siguiente paso disponible, **Cuando** el personaje lo ejecuta, **Entonces** ese paso es una acción ordinaria de movimiento, consume el tiempo que corresponda al costo de salida según Parte II §3.1 y deja ejecutarse normalmente los eventos entre decisiones.
4. **Dado** que el jugador recuerda abierta una puerta que en realidad está cerrada, **Cuando** observa esa puerta al estar en una de las salas que conecta, **Entonces** el recuerdo se actualiza y la ruta se recalcula; si ya no existe ruta conocida, el viaje se detiene sin consumir tiempo adicional.
5. **Dado** que el viaje entra a una sala con enemigos dormidos, **Cuando** se activa el comportamiento normal de entrada a sala, **Entonces** los enemigos se activan según Parte I §2.4 y el viaje se detiene.
6. **Dado** que el jugador recibe daño durante un paso del viaje y sobrevive, **Cuando** termina de resolverse ese paso y sus eventos, **Entonces** el viaje se detiene y comunica el daño junto con cualquier otro motivo coincidente, en el orden fijo: llegada al destino, enemigos vivos en la sala, daño recibido.
7. **Dado** que el jugador llega al destino y sobrevive, **Cuando** se completa el último paso, **Entonces** el viaje se detiene indicando que llegó y comunica también cualquier otro motivo coincidente, en el orden fijo: llegada al destino, enemigos vivos en la sala, daño recibido.
8. **Dado** que el viaje no tiene ruta conocida disponible antes del siguiente movimiento, **Cuando** se evalúa el paso siguiente, **Entonces** se detiene sin consumir tiempo adicional e informa que no queda ruta conocida.
9. **Dado** que el jugador tiene una llave para una puerta cerrada, **Cuando** la ruta de viaje requeriría abrir esa puerta, **Entonces** «ir a» no abre la puerta y solo puede continuar si existe una ruta conocida por salidas recordadas abiertas.
10. **Dado** que el viaje ejecuta uno o más pasos, **Cuando** se registra la partida, **Entonces** cada paso aparece como movimiento individual y se escribe una sola vez el comentario de la orden inmediatamente antes de la línea del primer movimiento; ese comentario permanece aunque el viaje se detenga después.
11. **Dado** que el jugador usa un pergamino durante un viaje, **Cuando** se revierte la acción, **Entonces** se deshace solo el último paso y el viaje no continúa automáticamente.
12. **Dado** que el destino de «ir a» es la sala actual, **Cuando** se emite la orden, **Entonces** se informa que el jugador ya está allí y no se produce efecto, consumo de tiempo, paso, registro en `partida.log` ni cambio del historial de retroceso.
13. **Dado** que el jugador inicia «ir a» en una sala con enemigos vivos, **Cuando** comienza el viaje, **Entonces** se permite ejecutar el primer paso con normalidad; la presencia inicial de enemigos no detiene el viaje, que se detiene por sus reglas habituales.
14. **Dado** que no existe una ruta conocida al destino antes del primer movimiento, **Cuando** se emite «ir a», **Entonces** la orden se detiene sin pasos, consumo de tiempo, registro en `partida.log` ni cambio del historial de retroceso.
15. **Dado** que la antorcha exploró salas vecinas y luego se apaga, **Cuando** el jugador consulta el mapa conocido, **Entonces** esas salas y observaciones se conservan.
16. **Dado** que el jugador enciende la antorcha dentro de una sala, **Cuando** permanece en ella, **Entonces** no se exploran vecinas por ese encendido; la exploración ocurre al entrar a una sala mientras la antorcha está encendida.
17. **Dado** que al entrar con la antorcha encendida se observan puertas y se exploran vecinas, **Cuando** el pergamino revierte esa entrada, **Entonces** esas observaciones y exploraciones vuelven al estado de conocimiento previo a la entrada.

### Casos Límite

- El estado observado de una puerta puede diferir del estado real hasta que el jugador esté en una de las dos salas que conecta.
- Una sala explorada por la antorcha revela nombre y salidas, pero no su contenido ni activa enemigos o trampas. Solo se observa la puerta entre la sala del jugador y esa vecina; las demás puertas de la vecina quedan no observadas hasta que el jugador entre en una de las salas que conectan.
- Una actualización de conocimiento causada por la antorcha debe revertirse junto con la entrada que la causó.
- El destino de «ir a» debe ser explorado; que esté avistado no basta.
- Un viaje puede perder su ruta conocida cuando se actualiza la observación de una puerta; esa detención no añade un paso ni tiempo.
- La parada por enemigos dormidos ocurre después de que se active su comportamiento normal de entrada a sala.
- Si coinciden motivos de detención en un paso, se comunican todos en el orden fijo: llegada al destino, enemigos vivos en la sala, daño recibido. Si el daño mata al jugador, se aplican las reglas de fin de partida de la Parte I y no se informa un viaje.
- Una orden «ir a» cuyo destino sea la sala actual informa que el jugador ya está allí, y no produce efecto, no consume tiempo, no ejecuta pasos y no se registra en `partida.log`.
- Consultar el mapa conocido no consume tiempo, no se registra y no altera el historial de retroceso. Una orden «ir a» rechazada o sin ruta desde el inicio tampoco consume tiempo, ni se registra, ni altera ese historial.
- El comentario de «ir a» se registra una sola vez, justo antes del primer movimiento de un viaje con pasos, y permanece aunque el viaje se detenga posteriormente.
- Iniciar «ir a» en una sala con enemigos vivos no detiene el viaje: la condición de detención por enemigos se evalúa al entrar a una sala.
- Apagar la antorcha no elimina las salas ni las observaciones ya conocidas. Encenderla dentro de una sala no explora vecinas hasta una entrada posterior con la antorcha encendida.
- Al revertir con pergamino una entrada que produjo exploraciones u observaciones por antorcha, se revierten también esos cambios del conocimiento.
- Si el pergamino revierte un paso durante un viaje, el sistema no ejecuta otro paso como continuación de la misma orden.

## Requisitos *(obligatorio)*

### Requisitos Funcionales

- **FR-NIE-001**: El sistema debe asignar a cada sala del punto de vista del jugador uno de tres estados: explorada, avistada o desconocida. La sala inicial empieza explorada en el instante cero.
- **FR-NIE-002**: Una sala explorada es aquella a la que el jugador entró al menos una vez. El jugador conoce su nombre, salidas, costos y estado de las puertas según la última observación.
- **FR-NIE-003**: Una sala no explorada que es destino de una salida de una sala explorada debe figurar como avistada, y el jugador solo debe saber que existe una sala tras esa salida. Las demás salas no exploradas permanecen desconocidas.
- **FR-NIE-004**: El jugador observa una puerta cuando está en cualquiera de las dos salas que conecta. El mapa conocido debe recordar el estado de su última observación aunque el estado real cambie después.
- **FR-NIE-005**: Mientras la antorcha esté encendida, al entrar a una sala deben quedar exploradas también todas sus vecinas por cualquier salida, abierta o cerrada. Se revela el nombre y las salidas de esas vecinas, pero no su contenido ni se activan sus enemigos o trampas. Se observa la puerta entre la sala del jugador y cada vecina; las demás puertas de esas vecinas quedan no observadas hasta que el jugador entre en una de las salas que conectan. Encender la antorcha dentro de una sala no explora vecinas hasta una entrada posterior. Apagarla no elimina el conocimiento ya adquirido.
- **FR-NIE-006**: El conocimiento del jugador forma parte del estado de la partida, se conserva al guardar y cargar, se revierte con el pergamino y se incluye en los estados consultables de la línea de tiempo.
- **FR-NIE-007**: La interfaz debe ofrecer un comando para consultar el mapa conocido, mostrando las salas exploradas, sus salidas y las salas avistadas, sin revelar información que no forme parte del conocimiento del jugador. La consulta no consume tiempo, no se registra ni altera el historial de retroceso.
- **FR-NIE-008**: La vista y el comando «ir a» deben derivar toda información del mapa exclusivamente del conocimiento del jugador.
- **FR-NIE-009**: El comando «ir a <sala>» debe aceptar como destino únicamente una sala explorada. Una orden cuyo destino no esté explorado o no exista se rechaza sin movimiento, consumo de tiempo, registro en `partida.log` ni cambio del historial de retroceso, e informa al jugador el motivo del rechazo.
- **FR-NIE-010**: «Ir a» debe calcular la ruta usando solo salas exploradas y salidas cuyas puertas el mapa conocido recuerde abiertas, minimizando la suma de costos. Una puerta no observada no se considera abierta ni puede cruzarse. En caso de empate, el primer paso debe dirigirse a la vecina con menor identificador.
- **FR-NIE-011**: Cada paso de «ir a» debe ser una acción completa ordinaria del jugador: consume tiempo según Parte II §3.1 y permite que los eventos ocurran normalmente entre pasos.
- **FR-NIE-012**: La ruta de «ir a» debe recalcularse antes de cada paso según el conocimiento vigente del jugador.
- **FR-NIE-013**: El viaje debe detenerse al llegar al destino, al entrar a una sala con enemigos vivos activos o dormidos, al recibir daño o al dejar de existir una ruta conocida. Debe comunicar todos los motivos coincidentes en un orden fijo y determinista: llegada al destino, enemigos vivos en la sala, daño recibido. El daño se evalúa al terminar de resolverse el paso y sus eventos. Si el daño mata al jugador, se aplican las reglas de fin de partida de la Parte I y no se informa un viaje.
- **FR-NIE-014**: «Ir a» no debe abrir puertas, incluso si el jugador posee la llave correspondiente.
- **FR-NIE-015**: Si el estado real de una puerta difiere del estado recordado, al observarla el conocimiento debe actualizarse y la ruta debe recalcularse. Si no queda ruta conocida, el viaje se detiene sin consumir tiempo adicional.
- **FR-NIE-016**: En `partida.log`, cada paso de viaje debe quedar registrado como movimiento individual. Si la orden ejecuta uno o más pasos, su comentario debe registrarse una sola vez, inmediatamente antes de la línea del primer movimiento, y permanece aunque el viaje se detenga después. Las órdenes rechazadas o sin pasos no se registran.
- **FR-NIE-017**: Usar un pergamino durante un viaje debe revertir solamente el último paso y evitar que el viaje continúe automáticamente.
- **FR-NIE-018**: Con el mapa conocido completo de la cripta de referencia, el cálculo de un paso de «ir a» debe tardar menos de 5 ms en las condiciones de medición del enunciado.
- **FR-NIE-019**: Si el destino de «ir a» es la sala actual del jugador, el sistema debe informar que el jugador ya está allí, sin producir efecto, consumir tiempo, ejecutar pasos, registrar la orden en `partida.log` ni alterar el historial de retroceso.
- **FR-NIE-020**: Si «ir a» se inicia en una sala con enemigos vivos, el viaje debe poder ejecutar su primer paso con normalidad. La detención por enemigos se evalúa al entrar a una sala, y el viaje se detiene por las reglas habituales.
- **FR-NIE-021**: Si «ir a» no tiene ruta conocida desde el inicio, la orden debe terminar sin pasos, consumo de tiempo, registro en `partida.log` ni alteración del historial de retroceso, e informar al jugador que no hay ruta conocida.
- **FR-NIE-022**: Apagar la antorcha no debe eliminar las salas ni observaciones ya conocidas por su efecto.
- **FR-NIE-023**: Encender la antorcha mientras el jugador permanece en una sala no debe explorar sus vecinas en ese momento; esa exploración ocurre al entrar a una sala mientras la antorcha está encendida.
- **FR-NIE-024**: Al revertir con pergamino una entrada que produjo exploraciones u observaciones por antorcha, el conocimiento de esas salas y puertas debe volver al estado previo a la entrada.

### Entidades Clave

- **Sala conocida**: Sala del laberinto y estado de conocimiento que el jugador tiene sobre ella, con la información revelada que corresponda.
- **Observación de puerta**: Último estado de una puerta observado por el jugador desde cualquiera de las salas que conecta.
- **Viaje automático**: Orden del jugador para alcanzar una sala explorada mediante movimientos ordinarios, con recalculación de ruta y motivos de detención observables.
- **Estado de partida**: Incluye el conocimiento del jugador para persistencia, retroceso y consulta histórica.

## Criterios de Éxito *(obligatorio)*

### Resultados Medibles

- **SC-NIE-001**: En todos los casos de aceptación, la información mostrada distingue correctamente salas exploradas, avistadas y desconocidas, sin revelar contenido desconocido.
- **SC-NIE-002**: Cada viaje válido elige en cada paso una ruta mínima conforme al conocimiento vigente y al desempate por menor identificador; cada viaje inválido por destino no explorado consume cero tiempo.
- **SC-NIE-003**: Los viajes se detienen en todas las condiciones especificadas e informan el motivo correspondiente.
- **SC-NIE-004**: Con mapa conocido completo de la cripta de referencia, el cálculo de cada paso de «ir a» queda por debajo de 5 ms.
- **SC-NIE-005**: Guardar, cargar, revertir con pergamino y consultar la línea de tiempo conservan o reconstruyen el conocimiento del jugador conforme a los cambios realizados.

## Supuestos

- La sala inicial se considera explorada desde el instante cero, según Parte II §3.3.
- Se adopta como decisión del grupo que la observación de las puertas de la sala ocurre cuando el jugador está en cualquiera de las dos salas que conectan, incluyendo al entrar o permanecer en ellas. El enunciado define cuándo se observa, pero no detalla el instante exacto de actualización.
- El costo de salida usado por la vista y por el viaje corresponde al costo del terreno definido en Parte II §3.1.
- Los eventos y activaciones que suceden al entrar a una sala conservan las reglas de Parte I; esta funcionalidad añade la parada del viaje cuando hay enemigos, sin redefinir el combate ni las trampas.
- Decisiones del grupo tomadas en la aclaración, pendientes de confirmar con el profesor porque el enunciado no las fija expresamente:
  - Una puerta no observada no se considera abierta y «ir a» no puede cruzarla.
  - Si coinciden varios motivos de detención se comunican todos, en el orden fijo: llegada al destino, enemigos vivos en la sala, daño recibido. Solo cuentan los enemigos vivos y el daño se evalúa al terminar el paso y sus eventos.
  - «Ir a» hacia la sala actual no tiene efecto, y iniciar un viaje en una sala con enemigos vivos está permitido.
  - Consultar el mapa conocido y las órdenes «ir a» rechazadas o sin pasos no consumen tiempo, no se registran y no alteran el historial de retroceso. El comentario de una orden con pasos se escribe una sola vez, antes del primer movimiento.
  - Apagar la antorcha conserva lo explorado, y encenderla dentro de una sala no explora vecinas hasta una entrada posterior.
- El formato de guardado y la línea de tiempo pertenecen a la capacidad 004. Esta especificación solo exige que el conocimiento del jugador forme parte de ese estado.
