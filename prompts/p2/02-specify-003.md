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