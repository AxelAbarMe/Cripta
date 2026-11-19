# Cierre, paso 7: matriz de trazabilidad

Estoy en la rama cierre. No crees ni cambies de rama y no hagas commit ni push. No escribas fuera del repo. Usa .\.venv\Scripts\python.exe en lugar de py para correr los comandos. Lee solo los archivos que se nombran aquí y no corras scripts de verificación amplios.

Crea solo docs/TRAZABILIDAD.md (Nuevo). Redáctalo en español, sin nombres de personas, y que cada dato salga de los archivos del repositorio y no de tu memoria.

1. Fuentes. Lista specs/ con Get-ChildItem y toma las carpetas de las cuatro capacidades (001 terreno y cazador, 002 niebla de guerra e ir a, 003 resolubilidad y 004 línea de tiempo). Si hay otra carpeta, ignórala y dímelo. De cada una lee spec.md (requisitos FR-XXX-NNN, escenarios de aceptación, casos del Apéndice B y criterios SC) y tasks.md (en cada tarea: los FR que atiende, las rutas con su estado Nuevo o Modificado y el comando de validación).
2. Estructura. Una sección por capacidad con su carpeta y su prefijo. Dentro, una tabla con una fila por requisito y las columnas: Requisito (su código), Escenario o caso (los escenarios y casos B que spec.md o las tareas citan junto a ese requisito), Tareas (códigos), Código (rutas bajo cripta/ de esas tareas) y Pruebas (rutas bajo tests/ de esas tareas). Agrega una segunda tabla por capacidad para los criterios SC con su caso, tareas y pruebas. Si un dato no está citado en spec.md o tasks.md, escribe un guion y no lo deduzcas.
3. Verificación de rutas. Comprueba con Test-Path cada ruta citada. Las cuatro capacidades ya están integradas en esta rama, así que se espera que todas existan. Si alguna no existe, márcala con '(prevista)' al lado y dime cuál es. No cambies ni inventes rutas.
4. Resumen al inicio. Una frase de cómo leer la matriz y, por capacidad, cuántos requisitos hay, cuántos tienen al menos una tarea y una prueba, y cuántas rutas no existen. Después de la matriz agrega una sección 'Requisitos sin tarea, sin prueba o sin escenario citado' con la lista de los que queden así, o la frase 'Ninguno' si no hay.
5. Si generas las tablas con un script auxiliar, no lo dejes en el repositorio. Verifica que todos los requisitos de cada spec.md aparezcan en la matriz.
6. Estado de las tareas. En tu respuesta, no en el archivo, dame por capacidad cuántas tareas de tasks.md están marcadas [X] y cuántas siguen en [ ], con los códigos de las que siguen sin marcar.
7. Al terminar corre .\.venv\Scripts\python.exe -m unittest discover -s tests -t . y dime el resultado.

Reglas: en textos nuevos no uses ";". Conserva CRLF. No uses sed -i. No agregues reglas del juego ni cambies ningún archivo salvo docs/TRAZABILIDAD.md. Si falta algo o dudas, detente y pregunta. Al terminar dime qué hiciste por punto y verifica con git diff que solo se agregó docs/TRAZABILIDAD.md.
