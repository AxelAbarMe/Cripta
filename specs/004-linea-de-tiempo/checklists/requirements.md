# Lista de calidad de especificación: Línea de tiempo

**Propósito**: Validar la integridad y calidad de la especificación antes de continuar con la planificación
**Creada**: 2026-11-15
**Funcionalidad**: [spec.md](../spec.md)

## Calidad del contenido

- [x] Sin detalles de implementación (lenguajes, marcos de trabajo, API)
- [x] Enfocada en el valor para quien juega y sus necesidades
- [x] Redactada para partes interesadas no técnicas
- [x] Todas las secciones obligatorias están completas

## Integridad de requisitos

- [x] No quedan marcadores [NEEDS CLARIFICATION]
- [x] Los requisitos son verificables y no ambiguos
- [x] Los criterios de éxito son medibles
- [x] Los criterios de éxito no dependen de detalles de implementación
- [x] Todos los escenarios de aceptación están definidos para las reglas especificadas
- [x] Se identifican los casos límite indicados por el prompt
- [x] El alcance está delimitado a consultas históricas, reproducción, puntos de control y persistencia de la línea
- [x] Se identifican dependencias y supuestos

## Preparación de la funcionalidad

- [x] Cada requisito funcional tiene escenarios o criterios de aceptación claros
- [x] Los escenarios cubren consulta por instante, por acción, reproducción, acciones revertidas por pergamino y persistencia de la línea de tiempo
- [x] La consulta no se registra en `partida.log`
- [x] Los escenarios cubren el tratamiento explícito de archivos de la Parte I, con FR-LIN-012 resuelto en la sesión de aclaraciones 2026-11-16
- [x] La funcionalidad se vincula con resultados medibles
- [x] No se filtran detalles de implementación en la especificación

## Notas

- FR-LIN-012 quedó resuelto en la sesión de aclaraciones 2026-11-16: no se ofrece migración de archivos de la Parte I.
- El valor predeterminado de `K` sigue sin fijarse; el grupo debe justificarlo mediante mediciones.
- La sesión de aclaraciones 2026-11-16 también fija la validación de `K` (FR-LIN-022) y el rechazo sin efectos de las consultas de historia inválidas (FR-LIN-023); ambos tienen escenarios de aceptación.
