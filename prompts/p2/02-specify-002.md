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