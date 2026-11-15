# Contrato interno: conocimiento y viaje

Este contrato describe límites entre capas, no añade reglas de juego.

## Modelo

- Acepta datos de la partida; no importa red, archivos, controlador ni vista.
- Consulta nivel de conocimiento por sala y observación por puerta.
- Devuelve una proyección sin contenido de salas desconocidas o avistadas.
- Revela y observa solo lo descrito en `spec.md`.
- Registra una inversa puntual por celda cambiada en el historial conectado.
- Calcula el siguiente paso con adyacencias conocidas; no abre puertas ni consulta rutas a través de conocimiento oculto.
- Devuelve resultado y motivos sin emitir texto de interfaz.

## Controlador

- Traduce órdenes de consulta y viaje.
- Para cada paso vuelve a solicitar una ruta y ejecuta una acción ordinaria por el servicio.
- Termina el bucle al recibir una condición de parada o al ejecutarse pergamino.
- Solicita a la vista presentar el mapa proyectado y el motivo. La vista no calcula ruta ni consulta estado real oculto.

## Servicio y bitácora

- Escribe un comentario único, como línea que empieza con `#`, inmediatamente antes del primer movimiento que sí se ejecutará.
- Registra cada movimiento mediante el mecanismo ordinario.
- Sin paso no hay comentario ni registro.
- El lector/replay reconoce el comentario como metadato, no acción; reproduce movimientos y acciones.
- Los turnos de enemigos no agregan registros.

## Persistencia

La proyección del conocimiento se entrega al estado lógico y se restaura al cargar. La capacidad 004 posee el formato binario y su compatibilidad; este contrato no define bytes, claves ni migraciones.
