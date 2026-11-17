Corrige solo documentos de specs/001-terreno-cazador/ (spec.md, plan.md, research.md, contracts/contrato_datos_p2.md y tasks.md), sin tocar código. El grupo decidió:

1. Llaves con enemigo vacío: en la respuesta de /llaves, un campo enemigo con texto vacío ("") es un dato inválido. LlaveUbicacionDTO.desde_json lanza ValueError con el dato afectado, igual que con un id vacío, y el cliente lo convierte como siempre. Solo null o ausente significa llave en el suelo.
   - spec.md: agrégalo a FR-TER-018 y añade la pregunta y respuesta a la sesión "Sesión 2026-11-10 (estado del servidor)" o en una sesión nueva "Sesión 2026-11-12 (decisiones previas a la Fase C)".
   - research.md y contracts/contrato_datos_p2.md: actualiza la regla de enemigo.
   - tasks.md: agrega T004b justo después de T004 (ampliar tests/dto/test_llave_ubicacion_dto.py con el caso enemigo="" que lanza ValueError, FR-TER-018) y T009b justo después de T009 (ajustar LlaveUbicacionDTO.desde_json para rechazar enemigo vacío, FR-TER-018). Sin marcar. En la sección de dependencias indica que T004b y T009b se hacen antes de la Fase C.

2. Rangos reales: los datos del servidor traen cazadores con rango 600 (ent_sabueso_oseo) y 2400 (ent_espectro_acechador), y costos de salida entre 20 y 490. cripta-06 tiene 25 sabuesos y 11 espectros.
   - plan.md: cambia la escala de rangos a "hasta 2 400 unidades de costo (valores reales del servidor: 600 y 2 400)". En la carga ruta_cazador, los costos de la cripta sintética pasan a 20-490, los rangos a R=600 y R=2400, y el caso heterogéneo usa la proporción de cripta-06 (25 de rango 600 y 11 de rango 2400, escalada a H).
   - tasks.md: actualiza T036 con esos mismos valores.

3. Costo de costo_de_conexion en la búsqueda: se mantiene la consulta actual (O(log n) por arista) y se mide. La carga ruta_cazador reporta aparte el tiempo dedicado a consultar costos. La alternativa de precalcular los costos en una tabla plana al construir el mapa (O(1) por consulta) queda como alternativa a evaluar si la medición muestra que pesa, y se documenta en DECISIONES.md (T043).
   - plan.md: agrégalo a las métricas de ruta_cazador y como límite conocido.
   - tasks.md: agrégalo a T036 y a T043.

Conserva ids, formato y finales de línea de cada archivo. No marques casillas. No uses sed -i. En comentarios y textos nuevos no uses ";". Al terminar, dime qué cambiaste en cada archivo.
