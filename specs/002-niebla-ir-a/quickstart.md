# Guía de validación: niebla de guerra e «ir a»

Escenarios previstos para implementar con `unittest`; esta guía no ejecuta pruebas ni crea tareas.

## Preparación

- Python 3.11 o superior y fixtures completos.
- Tras implementar, ejecutar `py -m unittest discover -s tests -t .` y conservar las pruebas de Parte I.
- Medir sin red ni vista con `py -m cripta --bench --solo niebla_rutas --escala 1`.

## Escenarios

1. Iniciar y consultar mapa: inicial explorada, destinos avistados y otras desconocidas; la consulta no consume tiempo ni se registra.
2. Observar puertas al entrar. Cambiar una puerta fuera de sus extremos conserva la observación anterior. Activar cierre automático mientras el jugador está en la sala vecina actualiza la memoria; recalcular antes del movimiento siguiente.
3. Encender antorcha sin moverse no revela vecinas. Entrar con antorcha revela vecinas y la puerta de conexión sin preparar ni activar contenido. Apagarla conserva conocimiento.
4. Revertir con pergamino una entrada con antorcha: revertir el paso y las celdas cambiadas; terminar el bucle sin continuarlo.
5. «Ir a» entre varias rutas: verificar costo mínimo, puertas recordadas abiertas, desempate por menor id, recálculo por paso, acciones normales y detenciones en el orden especificado.
6. Destino no explorado/inexistente, sala actual y falta de ruta inicial: cero pasos, tiempo, comentario/log o cambio del retroceso; mostrar el motivo.
7. Revisar `partida.log`: comentario una vez justo antes del primer movimiento, movimientos individuales y ningún turno enemigo; replay omite comentario y reproduce acciones.
8. Guardar/cargar, consultar historia y revertir: conocimiento coincide con el momento correspondiente; validar integración con el formato de 004.

## Medición

Ejecutar exactamente `py -m cripta --bench --solo niebla_rutas --escala 1`. Reportar semilla/configuración, mapa completo de referencia `cripta-06`, latencias por cálculo y cumplimiento de <5 ms. Comparar búsqueda compartida, búsqueda separada, selección lineal manual, revelación incremental frente a pasada completa e inversas frente a copia completa. Toda cifra de este plan es hipótesis hasta medir.
