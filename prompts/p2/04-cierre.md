# Cierre, paso 3 (continuación): terminar el README

Estoy en la rama cierre. No crees ni cambies de rama y no hagas commit ni push. No escribas fuera del repo ni crees py.cmd. Usa .\.venv\Scripts\python.exe en lugar de py para correr los comandos. Lee solo los archivos que se nombran aquí y no corras scripts de verificación amplios.

Contexto: la corrida anterior de prompts/p2/03-cierre.md se interrumpió antes de terminar. Edita solo README.md (Modificado) y no rehagas lo que ya esté bien.

1. Lee prompts/p2/03-cierre.md y compáralo con git diff README.md. Para cada uno de sus puntos 1 a 5 decide si está aplicado, a medias o ausente, y dame esa lista. Completa solo lo que falte o esté a medias. Si hay secciones duplicadas, cortadas o texto a medias de la corrida anterior, corrígelo. Conserva la estructura de secciones 1 a 10 y el estilo del README, en español, sin nombres de personas (la URL del repositorio puede quedar) y sin cifras que no estén medidas en DECISIONES.md o docs/bench.
2. Agentes. Los agentes que declara el README deben coincidir con los encabezados de PROMPTS_LLM.md (las líneas que empiezan con ### y terminan con el nombre del agente). Si el README menciona un agente que no aparece ahí, quítalo y dímelo. Si PROMPTS_LLM.md tiene uno que el README no menciona, agrégalo.
3. Versión de Spec Kit. Búscala en .specify/ (archivos de configuración o de versión). Si no la encuentras, deja la que está en el README y dímelo.
4. Comandos. Cada comando, bandera y ejemplo del README debe existir de verdad. Compruébalo leyendo cripta/__main__.py y cripta/vista/vista_consola.py. Para los de la 003 (--verificar, --forzar y sus códigos de salida) toma el texto de specs/003-resolubilidad/contracts/contrato_resolubilidad.md y de specs/003-resolubilidad/quickstart.md aunque su código aún no esté en la rama. Dame una lista aparte de todo lo que describes y no se puede comprobar en el código.
5. --bench. La lista de --solo debe coincidir con los nombres registrados en CARGAS de cripta/bench/cargas_bench.py. Si resolubilidad y resolubilidad_cota no están, agrégalas a la lista igualmente y dime que lo hiciste.
6. Corre .\.venv\Scripts\python.exe -m unittest discover -s tests/aceptacion -t . y dime el resultado.

Reglas: en textos nuevos no uses ";". Conserva CRLF. No uses sed -i. No agregues reglas del juego. Si falta algo o dudas, detente y pregunta. Al terminar dime qué cambiaste por punto y verifica con git diff que solo cambió README.md.
