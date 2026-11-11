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