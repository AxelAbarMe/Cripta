# Guía rápida de validación: línea de tiempo

Esta guía describe validaciones para la fase de implementación. Ejecutarlas con la versión integrada de 001 y 002 y sin red cuando la prueba use fixtures.

## Requisitos previos

- Python 3.11 o superior y dependencias del proyecto instaladas.
- Rama `004-linea-de-tiempo` con las capacidades necesarias integradas.
- Fixtures de la Parte II disponibles para el benchmark de referencia.

## Validaciones automatizadas

Desde la raíz del repositorio:

```powershell
py -m unittest tests.modelo.test_linea_tiempo tests.modelo.test_partida_linea_tiempo
py -m unittest tests.infraestructura.test_guardado_binario tests.servicios.test_servicio_replay
py -m unittest tests.aceptacion.test_linea_tiempo
```

Esperado: todas las pruebas pasan e identifican en su docstring o nombre de prueba los requisitos FR que cubren. Deben ejercitar los seis casos B-LIN-001 a B-LIN-006 y los criterios SC-LIN-001 a SC-LIN-007. Los detalles lógicos están en [data-model.md](data-model.md) y los comandos de usuario en [contracts/cli.md](contracts/cli.md).

## Revisión manual de comandos

1. Iniciar una partida con `py -m cripta --offline --checkpoint-cada 100` y ejecutar acciones aceptadas.
2. Consultar `historia 0` y `historia #1` cuando corresponda. Confirmar que se presentan los siete grupos mínimos y que reloj, estado, log e historial no cambian.
3. Consultar un tiempo posterior al reloj y un `#k` inválido. Confirmar rechazo con motivo y sin efecto.
4. Guardar, cargar y repetir una consulta válida. Comparar el resumen antes y después de cargar.
5. Intentar cargar un guardado P1 de prueba. Confirmar incompatibilidad por versión y verificar que sus bytes siguen intactos; no debe ofrecerse migración.
6. Reproducir una bitácora con `--replay partida.log --hasta t`. Comparar su resumen con `historia t`. Si el log finaliza antes, debe indicar final anticipado.

## Medición requerida

```powershell
py -m cripta --bench --solo linea_tiempo --escala 1
```

Esperado: ejecución determinista con semilla declarada, al menos 5 000 acciones sintéticas, cripta de referencia elegida por mayor cantidad de salas, y reporte de memoria/consulta para K=100, 500, 1000 y sin checkpoints. Debe incluir la alternativa de reconstrucción por inversión y búsqueda lineal de checkpoint. No se presupone resultado ni valor predeterminado. El grupo selecciona K después de medir y verifica consulta <50 ms.

## Compatibilidad de la suite

Tras las validaciones específicas, ejecutar la suite completa prescrita por el proyecto:

```powershell
py -m unittest discover -s tests -t .
```

Esperado: suite completa de Parte I y II satisfactoria; las pruebas afectadas deben citar FR. Esta planificación no ejecuta pruebas.

