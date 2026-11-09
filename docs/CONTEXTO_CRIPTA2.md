# CRIPTA 2 — Guía maestra de contexto, instalación y proceso SDD

> **Proyecto:** Cripta, Parte II · Estructuras de Datos, II ciclo 2026
> **Entrega:** miércoles **18 de noviembre de 2026** · **Equipo:** 3 personas · **Peso:** 15 % de la nota del curso
> **Metodología:** Spec-Driven Development (SDD) con GitHub **spec-kit**
> **Agentes del equipo:** 1 × Claude Code (Claude Pro) + 2 × Antigravity CLI (Gemini)

---

## Cómo usar este archivo

| Si eres... | Lee... |
|---|---|
| Un **agente de IA** (Claude, Gemini, otro) | **PARTE D completa primero**, luego la parte que te toque |
| Un integrante que **instala herramientas** | PARTE A |
| Un integrante que **empieza una feature** | PARTE B y luego PARTE C |
| Quien **integra / revisa** | PARTE B §B.8 y PARTE C §C.9 |

Guárdalo en el repo como `docs/CONTEXTO_CRIPTA2.md`. El `AGENTS.md` de la raíz (plantilla en §B.2) lo referencia para que todo agente lo lea al empezar.

### Índice

- **PARTE 0** — Respuestas a las tres aclaraciones previas
- **PARTE A** — Instalación completa (Git, Python, uv, Claude Code, Antigravity CLI, spec-kit)
- **PARTE B** — Cómo aplicar SDD en equipo: comandos, Git, ramas, los 7 pasos, división del trabajo
- **PARTE C** — Guía completa de Cripta 2: qué cambiar, quién, en qué orden, con qué prompts
- **PARTE D** — Contexto completo del proyecto (Parte I + Parte II) para agentes y compañeros

---

# PARTE 0 — Aclaraciones previas

## 0.1 ¿Hace falta otro repositorio de GitHub para Cripta 2?

**No. Usen el mismo repositorio de la Parte I.** El enunciado lo dice textualmente: *«Base de código: se continúa sobre el repositorio de la primera parte»* y *«specify init --here»* se ejecuta sobre el repositorio existente. Además la evaluación revisa el **historial de Git** (especificación antes que código) y la trazabilidad contra el código ya existente; un repo nuevo lo rompería.

Lo que sí deben hacer antes de tocar nada:

```bash
git switch main
git pull
git tag parte-1-entrega            # punto de retorno seguro
git push origin parte-1-entrega
```

La Parte I queda congelada en ese tag; la Parte II vive en ramas nuevas y vuelve a `main` por Pull Request.

## 0.2 Notas extra para orientar el proyecto

1. **El tiempo es muy corto.** Del 8 al 18 de noviembre son ~10 días. Todo el plan de §C.2 está pensado para eso: las especificaciones se escriben **en paralelo** y el código arranca el día 4.
2. **El historial de Git es parte de la nota.** Debe mostrar `spec.md` confirmado **antes** que el código que lo implementa. Si el código revela un error en la especificación: primero commit de la spec corregida, después commit del código.
3. **Los agentes no saben las prohibiciones del curso** (`heapq`, `bisect`, `collections`, `networkx`, `set`, `dict` como índice/caché). Hay que ponerlas en la **constitución**, en `AGENTS.md` y verificar cada `plan.md` a mano. La constitución se la lee el agente en cada fase.
4. **`spec.md` no lleva estructuras de datos, clases ni módulos.** Eso va en `plan.md`. Es el error más común.
5. **Trazabilidad:** cada requisito `FR-…` ↔ escenario de aceptación ↔ tarea ↔ código ↔ prueba (que cita el id). En la defensa sacan un requisito al azar.
6. **Todos deben poder explicar todo.** Lo que genere un agente es responsabilidad del grupo. Cada persona debe leer los `plan.md` de las otras tres capacidades.
7. **`PROMPTS_LLM.md`** debe registrar cada invocación de `/speckit.*` con texto propio, no solo los chats sueltos.
8. **Contrato del API (OpenAPI v1.1.0 = contrato de la Parte II).** Ya incluye `costo` en las salidas, `comportamiento: cazador` y `rango` en el catálogo, y `GET /criptas/{id}/llaves`. Guárdenlo en `docs/api/openapi-v1.1.0.json`. Ojo: los DTO actuales (`SalidaDTO`, `EnemigoDTO`) ignoran los campos que no conocen, así que `costo` y `rango` no rompen la lectura, pero **se pierden** hasta que se agreguen al DTO, a la serialización de la caché y al cliente offline (ver `MAPA_CODIGO.md` §9.5). `costo` y `rango` son **nulos/opcionales** (ausente = costo 100; un cazador sin `rango` es un caso a aclarar en `/speckit.clarify`) y `KeyLocation` sin `enemigo` significa llave en el suelo de esa sala. Verifiquen siempre en `/docs` en vivo por si hay nuevas versiones.
9. **Documento de decisiones:** el README actual lo ubica en `docs/DecisionesDiseño.md`, pero la Parte II pide `DECISIONES.md` **en la raíz**. Mover/renombrar (con `git mv`) en una tarea explícita.
10. **Presupuesto de red:** la consulta `/llaves` cuenta como solicitud. Hay que pensar en la precarga y la caché para que no rompa `presupuesto_solicitudes`.

## 0.3 ¿Se puede trabajar multiagente con herramientas distintas? ¿Se permite?

- **El grupo asume que se permite.** El enunciado dice que el agente es decisión del grupo («Claude Code, GitHub Copilot, Gemini CLI u otro compatible») y que se indique en el README. Lo escribe en singular («el agente»), sin prohibir ni permitir explícitamente varios: es una interpretación del grupo. En el README se declaran **todos** los agentes usados y qué hizo cada uno.
- **Viabilidad técnica: por verificar.** Esta guía supone que spec-kit v1.2.3 admite varios agentes en el mismo repo (`specify integration install`, `--integration agy`, `--integration none`) y que Claude Code y Antigravity CLI comparten `.agents/skills/`. Antes de depender de eso, comprueben con `specify --help`, `specify init --help` y `specify integration --help` que esos comandos y claves existen en la versión fijada (ver §B.1).
- **Lo que no debe pasar:** que dos agentes editen la misma capacidad a la vez, o que alguien edite a mano los comandos generados por spec-kit.
- La verdad de fondo: **spec-kit son archivos Markdown en Git**. El agente es intercambiable; la fuente de verdad es el repo.

---

# PARTE A — Instalación completa (Windows 10/11)

> Todo está en versión Windows (el lab del curso es Windows). Para macOS/Linux al final de cada paso hay equivalentes.
> ⚠️ **Después de cada instalación cierren y reabran la terminal**: Windows solo recarga el `PATH` en terminales nuevas. «Command not found» justo después de instalar casi siempre es eso.

## A.1 Requisitos previos: Git, Python, uv

```powershell
winget install --id Git.Git -e
winget install --id Python.Python.3.12 -e
winget install --id astral-sh.uv -e
```

Reabrir terminal y verificar:

```powershell
git --version
python --version      # 3.11+ (proyecto probado con 3.12)
uv --version
```

Configurar identidad de Git (cada integrante, con su propio nombre):

```powershell
git config --global user.name  "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
git config --global core.autocrlf true
```

> `core.autocrlf true` evita que los saltos de línea de Windows ensucien los diffs de los `.md`.

macOS/Linux: `brew install git python@3.12 uv` o el gestor de paquetes de la distro; `uv` también con `curl -LsSf https://astral.sh/uv/install.sh | sh`.

## A.2 Permitir scripts de PowerShell (una sola vez)

Los scripts auxiliares de spec-kit en Windows son `.ps1`:

```powershell
powershell -Command "Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"
```

## A.3 Instalar spec-kit (`specify`) — **misma versión para los tres**

Se fija **v1.2.3**, la versión que ya se instaló para los laboratorios del curso. **Anótenla en el README** y no la cambien a mitad del proyecto:

```powershell
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.3
uv tool update-shell
```

> Si ya había una versión instalada, `uv tool install` repetido **no la actualiza**: usen `uv tool install --force specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.3` y verifiquen con `specify version`.
> En la serie 1.2 los comandos de agentes basados en *skills* se invocan como `/speckit-specify` (con guion). Los prompts de esta guía escriben `/speckit.specify`: usen el que muestre su agente al teclear `/`.

Reabrir terminal y verificar:

```powershell
specify version
specify check
specify --help
```

> ⚠️ **No** usar `pip install specify-cli` de PyPI: ese paquete **no** es el oficial.
> ⚠️ Si GitHub responde `403 rate limit` durante `specify init`, esperen unos minutos o definan un token de GitHub (`GH_TOKEN`) en el entorno, **sin pegarlo nunca en archivos ni commits**.
> ✅ Ejecuten `specify --help` y `specify integration --help`: confirmen que existe el subcomando `integration` en la versión fijada. Si no existe, vean la nota de contingencia en §B.1.

## A.4 Instalar Claude Code (la persona con Claude Pro)

Opción recomendada (instalador nativo, no requiere Node.js):

```powershell
irm https://claude.ai/install.ps1 | iex
```

Alternativa con Node.js 20+:

```powershell
winget install --id OpenJS.NodeJS.LTS -e
npm install -g @anthropic-ai/claude-code
```

Reabrir terminal, verificar y autenticar:

```powershell
claude --version
cd C:\ruta\a\tu\repo
claude                 # primera vez: elegir login con cuenta Claude (Pro) y autorizar en el navegador
```

Notas para Claude Pro (el cupo es por ventanas de uso y se agota más rápido con código):

- Dentro de Claude Code, `/clear` entre fases del flujo, `/compact` si la conversación crece y `/status` o `/usage` para ver el consumo (los nombres exactos pueden variar; escribe `/` para ver la lista).
- **No** usen modo de aprobación automática. Lean cada edición/comando antes de aceptar.
- Reserven los tokens de Claude para lo más delicado (§C.3).

> Verifiquen siempre contra la documentación oficial de Claude Code por si el comando de instalación cambió: <https://docs.claude.com>.

## A.5 Instalar Antigravity CLI (`agy`) (las dos personas con Gemini)

Es un binario único (no requiere Node.js). **PowerShell**:

```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```

**CMD:**

```cmd
curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
```

macOS/Linux: `curl -fsSL https://antigravity.google/cli/install.sh | bash` (instala en `~/.local/bin/agy`).

Reabrir terminal y verificar:

```powershell
agy --version
agy update          # actualiza en sitio cuando haya versión nueva
```

**Autenticación** (primera vez):

```powershell
agy
```

1. Se abre el navegador: iniciar sesión con la cuenta de Google y autorizar.
2. Alternativa con API key de Gemini (de <https://aistudio.google.com/apikey>):
   - Crear `~/.gemini/antigravity-cli/settings.json` con `{ "modelProvider": "gemini" }`
   - Definir la clave como variable de usuario **sin escribirla en ningún archivo del repo**: `setx GEMINI_API_KEY "tu-clave"` y reabrir terminal.
   - Comprobar sin imprimirla entera: `$env:GEMINI_API_KEY.Substring(0,6) + "..."`
3. Diagnóstico: `agy inspect` muestra el contexto que el agente descubrió (útil para verificar que lee `AGENTS.md` y `.agents/skills/`).

> 🔐 **La clave API es una contraseña.** Nunca en código, prompts, capturas ni commits. Si se filtra, se borra en AI Studio y se crea otra.
>
> ⚠️ **Conflicto del comando `agy`** con la app de escritorio de Antigravity: si `agy --version` abre la aplicación gráfica en vez de imprimir la versión, la guía de instalación de la herramienta documenta cómo resolverlo (alias o enlace simbólico al binario de la CLI). Revisen `where agy`.
>
> 🔁 **Plan B del lab del curso:** si Antigravity CLI da problemas, `npm install -g @google/gemini-cli` y `--integration gemini` (los comandos quedan en `.gemini/commands/`). Es la herramienta con la que el profesor ya probó el lab.

## A.6 Clonar el repositorio y comprobar el entorno

```powershell
mkdir C:\dev ; cd C:\dev
git clone https://github.com/<organizacion-o-usuario>/<repo-cripta>.git
cd <repo-cripta>
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m unittest discover -s tests -t .       # debe terminar en OK
py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log   # código de salida 0
```

Si las pruebas de la Parte I pasan en las tres máquinas, la base está sana.

## A.7 Lista de verificación final (cada integrante)

| Check | Comando | Esperado |
|---|---|---|
| Git | `git --version` | versión |
| Python | `python --version` | 3.11+ |
| uv | `uv --version` | versión |
| spec-kit | `specify version` | **la misma versión en los tres** |
| Agente | `claude --version` o `agy --version` | versión |
| Repo | `py -m unittest discover -s tests -t .` | `OK` |
| Secretos | `git status` | ningún `.env` ni clave en cambios |

---

# PARTE B — Cómo aplicar SDD en equipo

## B.1 Dónde ejecutar `specify init` y qué crea

**Se ejecuta UNA vez, en la raíz del repo de Cripta** (la carpeta que contiene `cripta/`, `tests/`, `docs/`, `requirements.txt`). Lo ejecuta **una sola persona** (el *integrador*) en una rama propia; los demás hacen `git pull`.

```powershell
git switch main ; git pull
git switch -c setup/spec-kit
specify init --here --script ps --integration <clave>
```

Claves de integración relevantes (según la documentación de spec-kit):

| Agente | Clave | Qué genera |
|---|---|---|
| Claude Code | `claude` | comandos/skills para Claude y `.agents/skills/` |
| Antigravity CLI | `agy` | skills en `.agents/skills/` |
| Gemini CLI (plan B) | `gemini` | `.gemini/commands/` |
| Ninguno (neutro) | `none` | solo `.specify/`, sin carpetas de agente |

> En versiones antiguas la bandera era `--ai`; en la actual es `--integration` (el lab del curso ya usa esta). Si `specify init --here` pregunta por directorio no vacío, confirmar; **revisar luego el `git diff`** (puede tocar `.gitignore`).

### Estrategia recomendada para el equipo mixto (1 Claude + 2 Antigravity)

> ⚠️ **Por verificar antes de usar esta sección:** los comandos `specify integration …` y las claves `agy` y `none` no se comprobaron en la v1.2.3. Corran `specify init --help` y `specify integration --help` y ajusten esta sección a lo que muestre la ayuda.

El enunciado exige que los archivos generados (`.specify/` y los comandos del agente) estén versionados. La documentación de spec-kit para equipos mixtos describe otro camino (inicializar neutro y que cada quien active su agente en local). Elijan **una** de estas dos opciones y documéntenla en el README:

**Opción 1 (recomendada, cumple «se versionan»): instalar ambos agentes y subir todo.**

```powershell
specify init --here --script ps --integration claude
specify integration install agy
specify integration status        # verifica que ambos figuran instalados
git add -A
git commit -m "Inicializa spec-kit para Claude Code y Antigravity"
```

Como ambos escriben a `.agents/skills/`, los tres usan **las mismas habilidades** sin editar nada. `specify integration install <clave>` no cambia el agente por defecto; `specify integration use <clave>` sí.

**Opción 2 (flujo oficial de equipos mixtos): repo neutro, agente local.**

```powershell
specify init --here --script ps --integration none      # integrador, una vez; se commitea
specify integration switch agy                          # cada integrante, en su checkout local
...
specify integration switch none                         # ANTES de hacer git add/commit
specify integration status                              # verificar
```

Ventaja: nadie sube carpetas de agente. Desventaja: si el profesor quiere verlas en el repo, hay que justificarlo en el README. **Pregunten al profesor cuál prefiere si hay duda.**

Reglas para ambas opciones:

- **No editar a mano** los comandos/skills generados por spec-kit. Las personalizaciones van en la constitución, en `AGENTS.md` o en *presets* revisados.
- Mismo `--script ps` para todos (si alguien usa macOS/Linux, todos deben usar `bash`; el tipo de script se fija al inicializar).
- *Contingencia:* si en la versión fijada no existe `specify integration …`, ejecuten `specify init --here --script ps --integration claude` y `--integration agy` (o `--ai agy`) uno tras otro y comiten el resultado revisando el diff.

> **Convención de invocación:** en agentes basados en comandos se escribe `/speckit.specify`; en los basados en *skills* puede aparecer como `/speckit-specify` o `$speckit-specify`. Escriban `/` en el agente y miren la lista. Los comandos se ejecutan **dentro del agente, no en la terminal**.

## B.2 Estructura del repositorio resultante

```
cripta/                      ← código de la Parte I (modelo, controlador, vista, servicios, infraestructura, estructuras, dto, bench)
tests/                       ← pruebas unittest por capa (+ tests/aceptacion/ para P2)
docs/
  CONTEXTO_CRIPTA2.md        ← este archivo
  MAPA_CODIGO.md             ← mapa del código existente (§C.1)
  ejemplos/                  ← partida_*.log de ejemplo
fixtures/                    ← respuestas del API para --offline
scripts/
  generar_fixtures.py
  revisar_prohibidos.py        ← auditor de dependencias prohibidas (§B.9)
.specify/
  memory/constitution.md     ← constitución (PROTEGIDA)
  templates/ scripts/        ← de spec-kit
.agents/skills/              ← skills de spec-kit (claude/agy)
specs/
  001-terreno-cazador/       (spec.md plan.md tasks.md research.md data-model.md contracts/ ...)
  002-niebla-ir-a/
  003-resolubilidad/
  004-linea-de-tiempo/
prompts/p2/                  ← prompts de entrada por fase y feature (los "7 segmentos")
AGENTS.md                    ← instrucciones para cualquier agente
CLAUDE.md                    ← contiene solo:  @AGENTS.md
DECISIONES.md                ← Documento de Decisiones (raíz, exigido por P2 §7.2)
PROMPTS_LLM.md               ← bitácora de prompts (raíz)
README.md                    ← actualizado con versión spec-kit, agente, comandos nuevos
```

### Material de referencia en la carpeta del proyecto (los agentes leen archivos, no tu chat)

El repositorio es **público**, así que los enunciados del profesor **no se suben**. Se guardan en una carpeta ignorada por Git, que cada integrante llena en su propia copia; el agente los lee igual porque están en la carpeta del proyecto.

```
docs/enunciados/Parte1.pdf            ← enunciado P1 (fuente de verdad)            [solo local]
docs/enunciados/Parte2.pdf            ← enunciado P2 (fuente de verdad)            [solo local]
docs/enunciados/Parte1.md, Parte2.md  ← conversión a Markdown (revisar a mano)      [solo local]
docs/api/openapi-v1.1.0.json          ← contrato del API (P2)                      [en el repo]
docs/CONTEXTO_CRIPTA2.md              ← este archivo (resumen operativo)           [en el repo]
```

En `.gitignore` se agrega:

```
docs/enunciados/
```

- Nada del programa ni de las pruebas puede depender de `docs/enunciados/`: un clon limpio (como el del profesor) no la tiene.
- Usen la versión corregida de `Parte1.md` (tabla de acceso al API y URL de §3.3 rehechas contra el PDF). Si alguna URL no coincide, la correcta es la de `cripta/infraestructura/cliente_http.py`.

Regla en `AGENTS.md`: *«Este contexto es un resumen; ante cualquier duda de una regla, consulta docs/enunciados/ y gana el enunciado.»*

### Plantilla de `AGENTS.md` (raíz)

```markdown
# Instrucciones para agentes — Cripta 2
1. Lee primero docs/CONTEXTO_CRIPTA2.md (PARTE D) y .specify/memory/constitution.md.
2. Antes de planificar, lee docs/MAPA_CODIGO.md. No inventes módulos que no existan.
3. PROHIBIDO en los problemas evaluados: heapq, bisect, collections (deque, OrderedDict,
   defaultdict, Counter), networkx, bibliotecas de grafos/rutas, list.sort()/sorted() donde el
   enunciado lo prohíbe, dict o set como índice/caché/tabla de búsqueda. Implementa a mano.
4. spec.md = QUÉ y POR QUÉ (sin estructuras, clases ni módulos). plan.md = CÓMO.
5. Determinismo: random.Random(semilla) propia; nunca hora del sistema ni orden de red.
6. MVC: modelo sin red/archivos/UI; --replay y --bench no instancian la vista.
7. Ningún dato de una cripta concreta en el código.
8. Cada tarea cita su requisito (FR-XXX-NNN); cada prueba cita el requisito que cubre.
9. Si falta información, pregunta; no asumas. Si la spec está mal, corrige la spec PRIMERO.
10. No hagas commits ni push. Los hace el humano. Registra el trabajo en tasks.md (casillas).
11. Si te quedas sin contexto/tokens: deja tasks.md actualizado y escribe docs/HANDOFF.md.
12. Convenciones de la Parte I (siguen vigentes):
    - Clases, métodos y atributos nuevos en español. Los métodos especiales (__len__...) quedan igual.
    - Comentarios: cabecera de máximo 5 líneas por archivo y 1-2 líneas por método. Nunca ";"
      dentro de un comentario. Las justificaciones van a docs/ o DECISIONES.md, no al código.
    - Sin nombres de personas en código, comentarios, commits ni documentos para el profesor.
    - Un error de programación hereda de IndexError o ValueError en su propio módulo. CriptaError
      (excepciones.py) es solo para errores externos (red, disco, archivos).
    - Pruebas con unittest en tests/, misma estructura que cripta/, y cada carpeta con su
      __init__.py (si falta, discover no la ve).
    - Respeta los finales de línea CRLF de los archivos existentes.
    - No crees ni modifiques un .py que la tarea no pida sin preguntar antes.
```

`CLAUDE.md`:

```markdown
@AGENTS.md
```

## B.3 Qué es cada uno de los 7 «segmentos» y cómo se relacionan con spec-kit

El lab del curso usa una carpeta `prompts/` con `01-constitution.md` … `07-implement.md`. Son **los textos de entrada (prompts) que se pegan en cada comando**; **no** son las salidas. Las salidas las genera spec-kit en otras rutas:

| # | Comando en el agente | Archivo de prompt (entrada, lo escriben ustedes) | Salida generada (se revisa y se commitea) |
|---|---|---|---|
| 1 | `/speckit.constitution` | `prompts/p2/01-constitution.md` | `.specify/memory/constitution.md` |
| 2 | `/speckit.specify` | `prompts/p2/02-specify-<feature>.md` | `specs/NNN-…/spec.md` (+ rama nueva) |
| 3 | `/speckit.clarify` | `prompts/p2/03-clarify.md` | `spec.md` (sección *Clarifications*) |
| 4 | `/speckit.plan` | `prompts/p2/04-plan-<feature>.md` | `plan.md`, `research.md`, `data-model.md`, `contracts/` |
| 5 | `/speckit.tasks` | `prompts/p2/05-tasks.md` | `tasks.md` |
| 6 | `/speckit.analyze` | `prompts/p2/06-analyze.md` | informe (no cambia archivos) |
| 7 | `/speckit.implement` | `prompts/p2/07-implement.md` | código + pruebas |

Cada uno se **copia textualmente** a `PROMPTS_LLM.md` (fecha, modelo, prompt, propósito) al ejecutarlo.

> El paso 1 se hace **una vez para todo el proyecto**. Los pasos 2–7 se repiten **por cada feature** (4 veces).

## B.4 Flujo Git (ramas, commits, push, PR)

### Ramas

```
main                         ← siempre verde (pruebas OK); código P1 + lo integrado
├─ setup/spec-kit            ← init (integrador)
├─ setup/constitution        ← constitución (los 3, una sola vez)
├─ 001-terreno-cazador       ← una rama por feature (spec-kit nombra así la rama de /speckit.specify)
├─ 002-niebla-ir-a
├─ 003-resolubilidad
├─ 004-linea-de-tiempo
└─ docs/decisiones           ← (opcional) para ir armando DECISIONES.md
```

### Dos PRs por feature (clave para cumplir «spec antes que código»)

1. **PR-docs**: `spec.md` + clarificaciones + `plan.md` + `tasks.md` (+ informe de `analyze` si se guarda). Se **fusiona a `main` primero**. Así los demás ven las interfaces antes de planificar sus propias features.
2. **PR-código**: implementación + pruebas + mediciones `--bench`. Se abre desde la **misma rama**, después del PR-docs.

Regla: **ningún commit de código antes de que el PR-docs de esa feature esté fusionado.**

### Cuándo hacer commit y push

Convención de la Parte I: mensajes **en español**, un tema por commit, **sin códigos de tarea ni nombres de personas**, siempre con `-m "..."`. La trazabilidad (FR → tarea → prueba) vive en `tasks.md` y en las pruebas, no en el mensaje del commit.

| Momento | Mensaje sugerido |
|---|---|
| Tras `/speckit.specify` | `Especificación de terreno y cazador` |
| Tras `/speckit.clarify` | `Aclaraciones en la especificación de terreno y cazador` |
| Tras `/speckit.plan` | `Plan de terreno y cazador: estructuras y mediciones previstas` |
| Tras `/speckit.tasks` | `Tareas de terreno y cazador` |
| Tras cada tarea (o grupo pequeño) | `Búsqueda de ruta de costo mínimo del cazador` |
| Corrección de especificación | `Corrige en la especificación el costo de espera del cazador` — **commit separado, antes del código** |

- **Commit** al terminar cada fase o tarea. **Push** al menos al final de cada sesión de trabajo y **siempre antes de cambiar de agente o cuando se acaben los tokens** (así el siguiente agente lee el estado real).
- Al empezar cada sesión y antes de abrir PR: `git fetch` y `git merge origin/main` (como en la Parte I). En PyCharm, cada conflicto se resuelve con sus flechas; nunca «Accept Left/Right» en bloque.
- **Los agentes no hacen commits ni push** (lo dice `AGENTS.md`): revisen `git diff` antes de aceptar.

### Archivos compartidos que provocan conflictos (y cómo evitarlos)

| Archivo | Riesgo | Regla |
|---|---|---|
| `PROMPTS_LLM.md` | los 3 escriben al final | cada quien añade sus entradas al final con el formato de la Parte I (`### AAAA-MM-DD — modelo (herramienta)`, prompt, prompt resumido, para qué se usó), **sin nombres de personas**; al conflicto se conservan **ambos** bloques |
| `.specify/memory/constitution.md` | cambia las reglas de todos | solo se modifica por PR con aprobación de los 3 (*enmienda*) |
| `README.md`, `DECISIONES.md` | secciones de todos | cada feature escribe **solo su sección**; el integrador unifica |
| Formato binario de guardado | lo tocan niebla (002) y línea de tiempo (004) | **004 es dueña** de la versión del formato; 002 declara en su plan qué estado nuevo debe persistirse |
| Esqueleto/DTO (`costo`, `rango`, `/llaves`) | lo necesitan 002, 003, 004 | lo implementa **001 primero** (tareas de contrato), PR corto fusionado el día 4 |
| Agenda de eventos | 001, 004 | cambios se anuncian en el chat del grupo |

## B.5 Cómo darle el contexto correcto al agente en cada fase

1. **Siempre** al abrir una sesión nueva: «Lee `AGENTS.md`, `docs/CONTEXTO_CRIPTA2.md` (Parte D) y `docs/MAPA_CODIGO.md`».
2. En `/speckit.specify` pega el contenido del prompt de la feature (§C.5) y **adjunta/menciona** la sección del PDF correspondiente (§3.x y Apéndice B).
3. En `/speckit.plan` pega las restricciones (§C.6) **y** el nombre del módulo existente a reutilizar.
4. En `/speckit.implement` limita el alcance: «ejecuta solo las tareas T001–T005, deténte y reporta».
5. Una sesión de agente por fase: `/clear` o sesión nueva entre fases evita contexto contaminado.

## B.6 Qué va en cada archivo (para no rehacer el código ya escrito)

| Archivo | Sí | No |
|---|---|---|
| `spec.md` | reglas del juego, historias de usuario, escenarios de aceptación (Dado/Cuando/Entonces), `FR-` numerados, requisitos de rendimiento | clases, módulos, estructuras de datos, librerías |
| `plan.md` | estructuras elegidas, alternativas (≥2), complejidad, módulos afectados (con rutas reales), mediciones planificadas, riesgos | reglas del juego nuevas que no estén en spec.md |
| `tasks.md` | tareas pequeñas verificables, dependencias, **requisito que atienden**, ruta del archivo a tocar | tareas sin requisito |
| código | solo lo que alguna spec describe | funcionalidades sin spec |

**Truco para minimizar refactorización:** en cada `/speckit.plan` se exige una sección **«Impacto en código existente»** que liste, por archivo de `cripta/`, qué cambia y por qué; si no hay necesidad, «sin cambios». El `MAPA_CODIGO.md` es la base.

## B.7 Manejo de errores del agente

| Situación | Qué hacer |
|---|---|
| **Se acaba el cupo/tokens a mitad** | 1) pedir que deje `tasks.md` al día (casillas) y escribir `docs/HANDOFF.md` (qué hizo, qué falta, archivos tocados); 2) commit del avance con un mensaje que lo diga (por ejemplo `Avance parcial de la búsqueda de ruta del cazador`); 3) push; 4) otra persona o agente abre sesión: «Lee AGENTS.md, tasks.md y docs/HANDOFF.md y continúa en la primera tarea sin marcar». |
| **No entiende una tarea** | no insistir con el mismo texto. Releer la tarea: ¿tiene archivo, requisito y criterio de «hecho»? Si no, **reescribir la tarea** en `tasks.md` (commit) y repetir. Si el problema es la spec, `/speckit.clarify` o corregir spec primero. |
| **Propone `heapq`, `set`, `dict`, `collections`…** | rechazar de inmediato, citar la cláusula de la constitución y pedir reescribir el plan. Si pasó a código: correr `scripts/revisar_prohibidos.py` y revertir. |
| **Se sale del alcance** (toca archivos de otra feature) | `git restore` de esos archivos; repetir con «solo modifica: <lista de archivos>». |
| **Inventa módulos/funciones** | exigir que cite archivo y línea que existen (`MAPA_CODIGO.md`). |
| **Alucina el contrato del API** | contrastar contra `/docs` en vivo y las respuestas en `fixtures/`. |
| **Rompe pruebas de la Parte I** | detener; `py -m unittest discover -s tests -t .`; arreglar antes de seguir. La P1 debe seguir pasando. |
| **Pierde el hilo en sesiones largas** | `/clear`, volver a darle `AGENTS.md` + la spec/plan/tasks de esa feature. |
| **Dos agentes dieron resultados distintos** | la spec manda. Si ambas lecturas son válidas, la spec era ambigua: `/speckit.clarify`. |

Límites prácticos para que el agente cumpla lo pedido:

- Tareas **pequeñas** (≈ 1 archivo, ≈ 1 requisito, ≈ 30–90 min).
- Siempre darle el **criterio de aceptación** y el **comando de prueba** que lo valida.
- Pedirle que **explique** antes de implementar tareas complejas (modo plan) y revisar.
- **No** modo de aprobación automática.

## B.8 Cómo revisar e integrar

Checklist del revisor (otra persona, no el autor) antes de fusionar un PR:

- [ ] `py -m unittest discover -s tests -t .` → `OK`
- [ ] `py -m scripts.revisar_prohibidos` → sin hallazgos
- [ ] La spec no menciona estructuras/clases/módulos
- [ ] Cada `FR-` tiene escenario, tarea, prueba (la prueba cita el id)
- [ ] Cada caso del Apéndice B asignado a la feature tiene escenario y prueba
- [ ] `plan.md` justifica ≥ 2 alternativas y planifica la medición de la descartada
- [ ] El historial muestra spec antes que código
- [ ] `PROMPTS_LLM.md` tiene las entradas de las fases ejecutadas
- [ ] Sin claves/secretos; `datos/` no versionado
- [ ] `py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log` sigue en código 0

## B.9 Automatización mínima útil

**Auditor de dependencias prohibidas** — `scripts/revisar_prohibidos.py` (propuesta: es un `.py` nuevo, así que el grupo decide antes si se crea):

```python
# Revisa cripta/ en busca de importaciones prohibidas por P2 §6.2 (error)
# y de usos de set, dict, sort o sorted que hay que revisar a mano (aviso).
# Solo se exime dto/, donde los dict de respuesta.json() sirven para leer JSON.
import os
import re
import sys

IMPORTACION_PROHIBIDA = re.compile(r"^\s*(?:from|import)\s+(heapq|bisect|collections|networkx)\b")
USO_A_REVISAR = re.compile(r"((?<![.\w])set\s*\(|(?<![.\w])dict\s*\(|\.sort\s*\(|\bsorted\s*\()")
CARPETAS_EXENTAS_DE_AVISO = ("dto",)


def revisar(raiz="cripta"):
    errores, avisos = [], []
    for base, _, archivos in os.walk(raiz):
        for nombre in archivos:
            if not nombre.endswith(".py"):
                continue
            ruta = os.path.join(base, nombre)
            exenta = any(carpeta in ruta.split(os.sep) for carpeta in CARPETAS_EXENTAS_DE_AVISO)
            with open(ruta, encoding="utf-8") as archivo:
                for numero, linea in enumerate(archivo, 1):
                    if IMPORTACION_PROHIBIDA.match(linea):
                        errores.append(f"{ruta}:{numero}: importación prohibida -> {linea.strip()}")
                    elif USO_A_REVISAR.search(linea) and not exenta:
                        avisos.append(f"{ruta}:{numero}: revisar -> {linea.strip()}")
    for aviso in avisos:
        print("AVISO", aviso)
    for error in errores:
        print("ERROR", error)
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(revisar())
```

Se ejecuta con `py -m scripts.revisar_prohibidos` desde la raíz. Código de salida 1 si hay importaciones prohibidas.

> Es una **red de seguridad heurística**: no detecta un `dict` usado como caché con otro nombre. La revisión humana del `plan.md` sigue siendo obligatoria. `infraestructura/` **sí** se revisa, porque ahí vive la caché.

**Hook opcional** (`.git/hooks/pre-commit`, o con la herramienta que prefieran): ejecutar el auditor y las pruebas antes de cada commit de código.

## B.10 Comandos de spec-kit, resumen

| Comando | Cuándo | Resultado |
|---|---|---|
| `/speckit.constitution` | una vez | principios del proyecto |
| `/speckit.specify <texto>` | por feature | `spec.md` + rama |
| `/speckit.clarify` | tras specify; repetible | preguntas/respuestas dentro de `spec.md` |
| `/speckit.plan <texto>` | tras clarify | `plan.md` + artefactos |
| `/speckit.tasks` | tras plan | `tasks.md` |
| `/speckit.analyze` | tras tasks, **antes** de implementar | informe de consistencia |
| `/speckit.implement` | tras analyze | código |
| `specify integration status` | antes de cada commit | verifica agentes instalados |
| `specify check` | diagnóstico | herramientas disponibles |

---

# PARTE C — Guía completa de Cripta 2

## C.1 Orientación previa (día 1, antes de especificar nada)

Ninguno de los agentes conoce el código. Primero que **lo lean y lo describan**:

Prompt (a un agente, sin tocar archivos salvo el nuevo):

```text
Lee el repositorio (carpeta cripta/, tests/, docs/, README.md). NO modifiques nada salvo crear
docs/MAPA_CODIGO.md con: (1) árbol de módulos y responsabilidad de cada uno; (2) las estructuras
de datos propias que existen y dónde están (agenda, caché, listas enlazadas, pila, cola circular,
vector ordenado, ordenamientos); (3) cómo se modela salida/puerta/sala, enemigo, comportamiento,
catálogo, caché de contenido, mapa/rastro; (4) cómo se guardan historial de retroceso, partida
(.sav) y bitácora (.log); (5) puntos de extensión naturales para: costo de salida, comportamiento
cazador, conocimiento del jugador, línea de tiempo; (6) riesgos de acoplamiento. Cita archivo y
clase para cada afirmación. Si algo no existe, dilo.
```

Revisar `docs/MAPA_CODIGO.md` entre los tres (30 min). Es la base de todos los `plan.md`.

## C.2 Cronograma (8–18 noviembre)

| Día | Fecha | Qué |
|---|---|---|
| 1 | Dom 8 | **PARTE A** (instalación). Tag `parte-1-entrega`. `init`. `MAPA_CODIGO.md`. Prompts de la constitución |
| 2 | Lun 9 | Constitución (los 3 juntos, reunión corta). Merge `setup/*`. Reparto de features |
| 2–3 | Lun 9–Mar 10 | Cada quien: `specify` → `clarify` de su feature (en paralelo). PR-docs temprano de **001** (contrato) |
| 3–4 | Mar 10–Mié 11 | `plan` → `tasks` → `analyze` → PR-docs de las 4. **Revisión cruzada de todos los plan.md** (prohibiciones, interfaces) |
| 4 | Mié 11 | **Fusión del PR-código de contrato** (costo, rango, `/llaves`, versión) |
| 5–8 | Jue 12–Dom 15 | `implement` por feature; pruebas de aceptación; `--bench` de cada una |
| 9 | Lun 16 | Integración, formato binario, replay, repetir mediciones P1 (§5.6) |
| 9–10 | Lun 16–Mar 17 | `DECISIONES.md`, README, `PROMPTS_LLM.md`, verificación de trazabilidad |
| 10 | Mar 17 | Ensayo de defensa: cada uno explica specs ajenas; ejercicio «cambio de regla» (spec primero) |
| 11 | **Mié 18** | **Entrega** |

> Si algo se atrasa, recorten **alcance de optimización**, no **especificación ni trazabilidad** (20 % del proyecto).

## C.3 División del trabajo (sugerencia)

| Persona | Agente | Responsabilidades |
|---|---|---|
| **A** | Claude Code (Pro) | **Integrador y revisor.** Constitución. `004-linea-de-tiempo` (la más delicada: interacciona con retroceso, formato binario y agenda). Revisión de §5.6 y `DECISIONES.md`. Corre `analyze` cruzado |
| **B** | Antigravity | `001-terreno-cazador` (incluye contrato de datos, costo variable, cazador, invalidación de rutas) |
| **C** | Antigravity | `003-resolubilidad` (independiente, arranca ya) y luego `002-niebla-ir-a` (depende de la búsqueda de rutas de 001) |

Dependencias reales:

```
001 (costo en esqueleto, rango, búsqueda de rutas) ──► 002 (ir a reutiliza o separa la búsqueda)
001 (contrato) ──► 003 (necesita /llaves y esqueleto con costo)
002 (conocimiento del jugador) ──► 004 (la línea de tiempo lo reconstruye)
001 + 002 + 004 ──► formato binario de guardado
```

**Todos hacen:** pruebas de aceptación de su feature, sección de `DECISIONES.md` de su feature, entradas en `PROMPTS_LLM.md`, y **revisión cruzada** de al menos una spec ajena.

Con el cupo limitado de Claude Pro: A usa Claude para `plan`/`analyze`/revisión de diseño y para las tareas difíciles (retroceso/línea de tiempo); la implementación repetitiva puede hacerse a mano o con cualquiera de los agentes.

## C.4 Constitución (paso 1, una vez) — `prompts/p2/01-constitution.md`

```text
Establece la constitución del proyecto Cripta (Parte II). Redáctala en español, en palabras del
grupo, con estos principios, cada uno con regla verificable:

1. Estructuras a mano. Las estructuras de datos de los problemas evaluados las implementa el
   grupo. Prohibido: dict como índice, caché, tabla de búsqueda o estructura propia; set en las
   mismas condiciones que dict; heapq, bisect, collections (deque, OrderedDict, defaultdict,
   Counter), networkx y cualquier biblioteca de grafos o búsqueda de rutas; list.sort()/sorted()
   en los ordenamientos evaluados. Permitido: list como almacenamiento contiguo, struct, json,
   requests, bibliotecas de interfaz, y los dict que devuelve respuesta.json() solo para leer JSON.
2. Determinismo. Misma cripta + misma semilla + mismas acciones = misma partida. Toda
   aleatoriedad usa una instancia propia random.Random(semilla). Nunca la hora del sistema ni el
   orden de llegada de respuestas HTTP.
3. MVC y adaptadores. Modelo sin red, archivos ni interfaz. --replay y --bench no instancian la vista.
   --offline sustituye la fuente de datos por una interfaz, sin if dispersos.
4. Sin datos de cripta concreta en el código: ni números de sala, ni ids de entidades, ni
   presupuestos, ni estadísticas.
5. Respeto de presupuesto_solicitudes. Toda solicitud HTTP cuenta, incluidos reintentos tras 429.
6. Rendimiento con evidencia. Toda afirmación de rendimiento se respalda con --bench; las cargas
   sintéticas son deterministas por semilla.
7. Especificación antes que código. spec.md no menciona estructuras, clases ni módulos; el plan
   no introduce reglas nuevas; toda tarea cita un requisito FR-XXX-NNN; toda prueba cita el
   requisito que ejerce. Si la spec está mal, se corrige primero en un commit separado.
8. Compatibilidad. Las pruebas de la Parte I siguen pasando. El formato binario nuevo detecta
   archivos incompatibles. Lo persistido se invalida por versión de cripta/catálogo.
9. Proceso. Los agentes no hacen commit ni push. Las enmiendas a la constitución requieren
   acuerdo de los tres. Toda invocación de spec-kit con texto propio se registra en PROMPTS_LLM.md.
10. Idioma y estilo: documentación en español; nombres de código en español, coherentes con la
    Parte I.

Incluye una sección «Gobernanza» con el procedimiento de enmienda.
```

**Después:** leer, ajustar a mano si falta algo, commit `Constitución del proyecto`, PR a `main` (aprobación de los tres).

## C.5 Prompts de `/speckit.specify` por feature

> Los prompts describen **comportamiento**. Si el agente propone clases o estructuras, se las quitan. Prefijos de requisitos sugeridos: `FR-TER-`, `FR-NIE-`, `FR-RES-`, `FR-LIN-`.
> Antes de ejecutar, crear la rama (ver nota) y verificar que el número/nombre del directorio es el esperado.

> **Numeración paralela:** spec-kit calcula el siguiente número viendo ramas/directorios existentes; si dos personas ejecutan a la vez ambas obtendrían `001`. Para evitarlo: `git switch -c 002-niebla-ir-a` **antes** de `/speckit.specify`, y comprueben que el agente usa esa rama/directorio; si crea otro, renombren (`git branch -m`, `git mv`) y commiteen.

### 02-specify-001 — Terreno y cazador

```text
/speckit.specify
Capacidad: terreno y cazador de Cripta Parte II.

Terreno: cada salida puede declarar un costo entero >= 1; si no lo declara vale 100; es igual
en ambos sentidos. Moverse a través de una salida cuesta el costo de esa salida; el intervalo
sigue siendo max(1, costo_salida * 100 // velocidad). Aplica a todos los actores. Atacar, esperar
y demás acciones no cambian. Errantes y rastreadores conservan su comportamiento.

Cazador: cuarto comportamiento de enemigo; su ficha incluye "rango" (entero en unidades de costo).
En su turno: (1) si comparte sala con el jugador, ataca; (2) si no, considera el costo mínimo d de
llegar a la sala actual del jugador sumando costos de salidas recorridas y usando solo salidas
abiertas en ese instante; (3) si no hay ruta o d > rango, espera con costo 100; (4) si hay, se
mueve un paso por una ruta de costo d, y el costo de esa acción es el de la salida que cruza.
Desempate: entre las vecinas v con costo(u,v)+dist(v,jugador)=d va a la de menor id. El cazador
conoce el esqueleto completo y el estado actual de todas las puertas; no le afecta la niebla; no
abre puertas; su decisión nunca depende de si el contenido de una sala se descargó.
Equivalencia observable: la decisión de cada turno debe ser idéntica a calcular desde cero en ese
instante, aunque cambien puertas, el jugador se mueva o mueran actores.

Servicio: el esqueleto trae "costo" por salida; el catálogo trae "comportamiento: cazador" y
"rango". Los datos persistidos de la Parte I deben invalidarse por versión, no borrando archivos.

Rendimiento: ciclo de eventos < 20 ms con decenas de cazadores activos que persiguen al mismo
objetivo (cripta de referencia, sin red ni renderizado).

Incluye como escenarios de aceptación todos estos casos del Apéndice B:
- cazador sin ruta abierta: espera con costo 100
- ruta más barata mayor que el rango: espera con costo 100
- ruta de menos salas pero mayor costo vs más salas y menor costo: sigue la de menor costo
- dos vecinas con rutas de costo mínimo: va a la de menor id
- una puerta de la ruta se cierra entre dos turnos: decide como desde cero
- actor de velocidad alta cruza salida de costo 1: intervalo >= 1
- cambia la velocidad de un actor que cruza una salida costosa: tiempo restante escalado (P1 §2.3)

Prefijo de requisitos: FR-TER-NNN. No menciones estructuras de datos, clases ni módulos.
```

### 02-specify-002 — Niebla de guerra e «ir a»

```text
/speckit.specify
Capacidad: niebla de guerra y viaje automático "ir a".

Para el jugador cada sala está en uno de tres estados: EXPLORADA (entró al menos una vez; la
inicial lo está desde t=0; conoce nombre, salidas, costo de cada salida y estado de sus puertas
según la última observación), AVISTADA (no explorada pero destino de una salida de una sala
explorada; solo sabe que existe una sala detrás), DESCONOCIDA (nada).
Memoria de puertas: el jugador observa una puerta cuando está en cualquiera de las dos salas que
conecta; el mapa recuerda el estado de su última observación aunque haya cambiado después.
Antorcha: mientras esté encendida, al entrar a una sala quedan exploradas también todas sus
vecinas por cualquier salida, abierta o cerrada; se revela nombre y salidas, no contenido; no se
activan sus enemigos ni trampas.
Todo lo que la vista muestra y lo que usa "ir a" se deriva solo del conocimiento del jugador. El
conocimiento es estado del juego: se guarda, se revierte con el pergamino y entra en la línea de
tiempo. La interfaz ofrece un comando para ver el mapa conocido (explorada, salidas, avistadas).

"ir a <sala>": lleva al jugador a una sala EXPLORADA mediante movimientos ordinarios. Ruta con el
conocimiento del jugador (solo salas exploradas, solo salidas recordadas abiertas), mínimo costo,
desempate por primer paso hacia la vecina de menor id. Cada paso es una acción completa del
jugador que consume tiempo (costos P2 §3.1) y deja correr los eventos. La ruta se recalcula antes
de cada paso. Se detiene si: llega; entra a sala con enemigos (activos o dormidos); recibe daño;
o deja de haber ruta conocida. No abre puertas aunque tenga la llave. En partida.log cada paso se
registra como movimiento individual y la orden se registra además como comentario. El pergamino
revierte solo el último paso.
El usuario debe poder ver por qué se detuvo el viaje.
Rendimiento: un paso de "ir a" < 5 ms con el mapa conocido completo de la cripta de referencia.

Escenarios del Apéndice B:
- ir a sala no explorada: se rechaza, no consume tiempo
- el mapa recuerda abierta una puerta realmente cerrada: al observarla se actualiza y se recalcula;
  si no hay ruta, el viaje se detiene sin consumir tiempo adicional
- ir a entra a sala con enemigos dormidos: se activan (P1 §2.4) y el viaje se detiene
- con antorcha encendida, entrar explora vecinas sin activar enemigos ni trampas
- un pergamino revierte una entrada con antorcha: las salas exploradas por la antorcha vuelven al
  estado anterior
- un pergamino durante un viaje: revierte solo el último paso y el viaje no continúa

Prefijo: FR-NIE-NNN. Sin estructuras, clases ni módulos.
```

### 02-specify-003 — Resolubilidad

```text
/speckit.specify
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
```

### 02-specify-004 — Línea de tiempo

```text
/speckit.specify
Capacidad: línea de tiempo (consulta del pasado de la partida) con puntos de control.

Estado en el instante t: el estado después de ejecutar todos los eventos con tiempo <= t; si a t le
corresponde una decisión del jugador, es el estado justo antes de tomarla.
"historia <t>" o "historia #k" (estado justo antes de la acción k del jugador) muestra como mínimo:
reloj, sala del jugador, vida y estadísticas, inventario, efectos activos, enemigos de esa sala con
su vida y el mapa conocido en ese momento. No consume tiempo, no se registra como acción, no
altera estado del juego ni del historial de retroceso.
"--replay partida.log --hasta <t>" reproduce hasta t e imprime el mismo resumen sin vista.
Los pergaminos recortan la línea: las acciones revertidas dejan de existir. Consultar un instante
posterior al reloj actual se rechaza.
Memoria: se permiten copias completas del estado (puntos de control) pero no más de una cada K
acciones del jugador; K se configura con --checkpoint-cada K (el valor por defecto lo justifica el
grupo con mediciones). Una consulta nunca requiere aplicar o deshacer cambios de más de K acciones.
Fuera de los puntos de control solo se guarda la información necesaria para reconstruir cambios; la
memoria crece con los cambios ocurridos más un punto de control cada K, nunca con acciones×tamaño
del estado. Si se reconstruye re-simulando, el punto de control incluye el estado del generador
aleatorio.
Persistencia: guardar y cargar conserva la línea completa; el formato binario cambia y un archivo
de la Parte I se detecta como incompatible (o se migra explícitamente), nunca se carga en silencio.
Rendimiento: consulta < 50 ms en partida de >= 5 000 acciones con K por defecto.

Escenarios del Apéndice B:
- historia <t> con t mayor que el reloj actual: se rechaza
- historia tras un pergamino: no muestra las acciones revertidas
- varios eventos en el mismo t: muestra el estado después de todos
- historia no consume tiempo, no va a partida.log, no modifica el historial de retroceso
- --replay --hasta t posterior al final: muestra el estado final e indica que terminó antes
- carga de archivo de la Parte I: incompatibilidad reportada o migración explícita

Prefijo: FR-LIN-NNN. Sin estructuras, clases ni módulos.
```

## C.6 Prompts de `/speckit.clarify`, `plan`, `tasks`, `analyze`, `implement`

### 03-clarify.md (igual para todas)

```text
/speckit.clarify
Prioriza ambigüedades que cambiarían el resultado observable: desempates, qué cuenta como
"recibir daño" o "entrar a sala con enemigos", interacción con pergaminos, orden de eventos
simultáneos, qué se guarda en partida.log, mensajes de rechazo, y todos los casos del Apéndice B
de la Parte II. Las respuestas deben ser compatibles con el enunciado de las Partes I y II (están
en docs/CONTEXTO_CRIPTA2.md). Si la respuesta está en el enunciado, cítala; no inventes reglas.
```

> En cada pregunta de `clarify`, **respondan ustedes (humanos)** con base en el PDF; no dejen que el agente decida reglas del juego.

### 04-plan.md (plantilla; añadir el bloque de la feature)

```text
/speckit.plan
Restricciones obligatorias (ver constitución): implementar a mano las estructuras; PROHIBIDO
heapq, bisect, collections, networkx, set y dict como índice/caché, list.sort()/sorted() donde
aplica. Reutiliza estructuras de la Parte I cuando sean adecuadas (cita el archivo).
El plan debe incluir:
 1. Problema y operaciones reales con su frecuencia esperada.
 2. Al menos DOS alternativas por problema y la razón concreta de descarte de cada una.
 3. Decisión (estructura y estrategia) y complejidad de las operaciones más frecuentes.
 4. Impacto en código existente: archivo por archivo (ruta real) o "sin cambios".
 5. Mediciones --bench previstas, incluida la de la alternativa descartada.
 6. Límites conocidos de la decisión.
 7. Revisión de decisiones de la Parte I que esta carga pueda invalidar (agenda, historial).
 8. Trazabilidad: tabla FR -> componente -> medición.
No agregues reglas del juego que no estén en spec.md. Si falta una regla, detente y pregunta.
```

Bloques por feature (añadir al final del prompt anterior):

| Feature | Aspectos que el plan debe resolver |
|---|---|
| 001 | Búsqueda de ruta de costo mínimo con selección del siguiente nodo y registro de distancias (propias); límite por rango para no recorrer toda la cripta; **cálculo compartido vs individual** (objetivo común) y cuándo cambia; qué eventos invalidan qué (puertas, jugador, muerte, velocidad); desempate por menor id garantizado con muchas rutas iguales; escenarios `--bench` con puertas estables e inestables y alternativa «recalcular siempre»; impacto en agenda (costos variables, reprogramación) |
| 002 | Representación del conocimiento (tres estados + memoria de puertas) con consulta barata; exploración que cueste lo proporcional a salas reveladas; registrar/invertir cambios para pergamino y línea; «ir a» sobre subgrafo conocido: ¿compartir implementación con 001 o separar? Justificar con medición |
| 003 | Recorrido incremental único (la obtención de una llave desbloquea regiones sin reiniciar), frontera bloqueada y dependencias salen del mismo recorrido; detección determinista de ciclos reportando el ciclo; orden determinista de llaves; alternativa ingenua (repetir por llave) y `--bench` con criptas sintéticas de muchas llaves encadenadas; persistencia de `/llaves` y presupuesto de red |
| 004 | Punto de control cada K; búsqueda del punto de control más cercano a t; reconstrucción adelante (re-simular, estado del random en el punto) vs atrás (invertir cambios), con evidencia; recorte por pergamino sin recorrer la historia; memoria vs K con ≥3 valores de K y alternativa sin puntos de control; formato binario nuevo + versión; consultas sin alterar estado |

### 05-tasks.md

```text
/speckit.tasks
Cada tarea debe: afectar ≈ 1 archivo existente o nuevo (ruta exacta), citar el/los requisitos FR-XXX-NNN
que atiende, declarar dependencias, indicar el comando de prueba que la valida y su criterio de
"hecho". Orden: (a) contrato de datos/DTO, (b) estructuras, (c) modelo, (d) servicios/controlador/vista,
(e) pruebas de aceptación (una por escenario, citando el requisito), (f) bench, (g) docs.
Ninguna tarea sin requisito. Marca con [P] las que pueden hacerse en paralelo. Máximo ~90 minutos por tarea.
Añade una tarea final «Sección de DECISIONES.md» y otra «Entradas de PROMPTS_LLM.md».
```

### 06-analyze.md

```text
/speckit.analyze
Revisa consistencia entre spec.md, plan.md y tasks.md de esta feature y contra la constitución y
docs/CONTEXTO_CRIPTA2.md. Reporta: (1) requisitos sin tarea; (2) tareas sin requisito; (3) escenarios
del Apéndice B sin prueba prevista; (4) estructuras o librerías prohibidas en el plan; (5)
estructuras/clases/módulos dentro de spec.md; (6) reglas nuevas en el plan que no están en la spec;
(7) conflictos con las otras features (formato binario, agenda, DTO). No modifiques archivos.
```

**Cada autor corrige los hallazgos (en commits separados) y otro integrante revisa el informe.**

### 07-implement.md

```text
/speckit.implement
Ejecuta SOLO las tareas T00X–T00Y de specs/NNN-.../tasks.md, en orden. Para cada tarea: implementa,
ejecuta su prueba, marca la casilla, y detente al terminar el bloque para que el humano revise el diff.
Reglas: sin heapq/bisect/collections/networkx/set/dict-como-índice; random.Random(semilla); MVC;
sin datos de cripta concreta; pruebas con unittest citando el requisito; no hagas commit ni push; no
toques archivos fuera de los listados en cada tarea. Si descubres que la spec es incorrecta,
DETENTE y repórtalo en lugar de seguir.
```

## C.7 Cómo cada feature toca el código existente (guía de dónde mirar)

> Rutas según el README de la Parte I; verifíquenlas en `MAPA_CODIGO.md`.

| Capa / carpeta | Cambios esperados de la Parte II |
|---|---|
| `cripta/dto/` | aceptar `costo` en salidas, `rango` y `cazador` en fichas, nuevo DTO de `/llaves`; toleran campos extra |
| `cripta/infraestructura/` | cliente HTTP y offline: método para `/llaves`; caché/persistencia: guardar llaves; invalidar por versión |
| `cripta/modelo/` | costo de salida y movimiento con costo variable; comportamiento cazador; conocimiento del jugador; efecto de antorcha; integración con retroceso |
| `cripta/estructuras/` | estructuras auxiliares para rutas, mapa conocido, resolubilidad y puntos de control (a mano); reutilizar las existentes si convienen |
| `cripta/servicios/` | partida, precarga (no puede depender de la niebla), replay con `--hasta`, verificación, línea de tiempo |
| `cripta/controlador/` | comandos `ir a`, `mapa`, `historia <t>`/`historia #k` |
| `cripta/vista/` | mostrar costos de salidas, cazadores distinguibles, mapa conocido, motivo de parada del viaje, reporte de resolubilidad |
| `cripta/__main__.py` | banderas `--verificar`, `--forzar`, `--checkpoint-cada`, `--replay … --hasta` |
| `cripta/bench/` | nuevas cargas (§C.8) |
| `tests/` | `tests/aceptacion/` con una prueba por escenario, citando `FR-…` |
| `fixtures/` | regenerar con las criptas de la P2 (nuevas versiones); `py -m scripts.generar_fixtures <id>` |
| `README.md`, `DECISIONES.md`, `PROMPTS_LLM.md` | actualizar |

## C.8 Benchmarks que la Parte II exige (`--bench`)

| Carga nueva | Qué compara |
|---|---|
| `ruta_cazador` | 1 vs muchos cazadores; rango pequeño vs grande; **cálculo compartido vs individual** |
| `invalidacion` | reutilizar vs recalcular siempre; puertas estables vs inestables |
| `mapa_conocido` | consultas al mapa, exploración, antorcha, `ir a` |
| `resolubilidad` | recorrido incremental vs repetido por llave; criptas sintéticas de muchas llaves encadenadas |
| `linea_tiempo` | memoria y tiempo para ≥ 3 valores de K + alternativa **sin** puntos de control |
| Repeticiones de P1 | agenda, historial de retroceso (y las demás) con la **carga nueva** (§5.6) |

- Las criptas sintéticas son **deterministas por semilla**.
- Límites: ciclo 20 ms (decenas de cazadores), resolubilidad 200 ms (la cripta mayor), `historia` 50 ms (≥5 000 acciones, K por defecto), paso de `ir a` 5 ms. Pueden ajustarse por enmienda cuando se publique la cripta de referencia.
- Aviso heredado de la P1: la carga `partida` con 400 salas supera 20 ms y hace que `--bench` completo termine en código 1; está documentado. **Con cazadores activos revísenlo y, si cambia, documenten antes y después.**

## C.9 Cierre: documentación, defensa y verificación

1. **`DECISIONES.md` (raíz):** mover/enlazar `docs/DecisionesDiseño.md`; añadir una sección por problema (5.1–5.6) con: problema, alternativas, decisión, complejidad, evidencia `--bench`, límites; **enlace a su `spec.md` y `plan.md`**; si la decisión final difiere del `plan.md` original, qué medición lo motivó; en §5.6 el **antes y después** de lo que cambie de la P1.
2. **README:** versión de spec-kit, agente(s), comandos nuevos (`--verificar`, `--forzar`, `--checkpoint-cada`, `--replay … --hasta`), cómo ejecutar las pruebas de aceptación.
3. **Trazabilidad:** hoja `docs/TRAZABILIDAD.md` con tabla `FR → escenario → tarea → archivo → prueba`. Elijan 3 requisitos al azar y recórranlos.
4. **Ejercicio de «cambio de regla»:** cambien (p.ej.) el costo por defecto de 100 a 120 o el radio de frescura del rastro: primero la spec (commit), luego el código (commit). Practíquenlo.
5. **Verificaciones finales:**
   ```powershell
   py -m unittest discover -s tests -t .
   py -m scripts.revisar_prohibidos
   py -m cripta --bench
   py -m cripta --offline --replay docs/ejemplos/partida_cripta-02.log
   py -m cripta --verificar <cripta>
   git log --oneline --graph --all      # spec antes que código, por feature
   ```
6. **Defensa:** requisito al azar → escenario, tarea, código, prueba. Cambio pequeño de regla (spec primero). Cada integrante explica **cualquier** spec. `--replay` y `--bench` en vivo contra una **cripta nueva, no resoluble posiblemente**.

## C.10 Lo que NO debe pasar (resumen)

- ❌ Código sin spec o spec desactualizada respecto al programa.
- ❌ `heapq`, `bisect`, `collections`, `networkx`, `set`/`dict` como índice o caché.
- ❌ Datos de una cripta concreta en el código.
- ❌ Usar la niebla del jugador para la decisión del cazador, o el esqueleto completo para la vista/`ir a`.
- ❌ Hora del sistema u orden de llegada de HTTP influyendo en la simulación.
- ❌ Copias completas del estado en cada acción (línea de tiempo y retroceso).
- ❌ Claves o secretos en el repo.

---

# PARTE D — Contexto completo del proyecto (para agentes y compañeros)

> **Para los agentes:** esta parte resume los enunciados de la Parte I (P1) y la Parte II (P2) de Cripta. Úsenla como fuente al explicar el proyecto, redactar especificaciones o revisar planes. Si hay discrepancia con el PDF original, **gana el PDF**. No se analizó el código del repositorio al escribir esta guía; para eso usar `docs/MAPA_CODIGO.md`.

## D.1 Qué es el proyecto y por qué existe

- Curso **Estructuras de Datos**, II ciclo 2026. Proyecto «Cripta»: juego de mazmorra por turnos en **Python 3.11+**, jugado por consola.
- **No se trata de programar un juego**, sino de **tomar decisiones de estructuras de datos bajo restricciones reales**, implementarlas a mano y **defenderlas con mediciones propias** (`--bench`).
- Regla editorial: *las reglas del juego están especificadas; las decisiones de estructuras de datos no.*
- Un programa que funciona pero no justifica sus decisiones con mediciones **no cumple**; una buena explicación sin implementación correcta tampoco.
- La mazmorra («cripta») **no viene en el programa**: se descarga de un **API REST** de solo lectura con un presupuesto de solicitudes. En la revisión se usa una **cripta nunca vista**.
- Grupos de hasta 4 (aquí 3). P1 vale 15 % de la nota del curso; P2 vale otro 15 %.
- Se permite el uso de LLM con **bitácora obligatoria** (`PROMPTS_LLM.md`: fecha, modelo, prompt textual, propósito). El código generado es responsabilidad del grupo y **cada integrante debe poder explicarlo y modificarlo**.

## D.2 Estado actual del repositorio (Parte I, ya implementada)

Según el README del repo:

- Estructuras propias: **montículo** para la agenda de eventos, **listas enlazadas**, **pila**, **cola circular**, **vector ordenado**; ordenamientos propios; caché del catálogo con tope `--cache-size` (25 por defecto).
- Arquitectura **MVC**: `cripta/{modelo, controlador, vista, servicios, infraestructura, estructuras, dto, bench}`, más `constantes.py`, `excepciones.py`, `__main__.py`.
- Banderas: `--offline`, `--cache-size N`, `--replay <log>`, `--bench [--solo ...] [--escala X] [--markdown f]`, `--help`.
- Archivos en `datos/` (no versionado): `cache/`, `puntajes/`, `partida.sav`, `partida.sav.log`, `partida.log`.
- Fixtures offline de 4 criptas: `cripta-01` (6 salas), `cripta-02` (20), `cripta-03` (40), `cripta-04` (50).
- Pruebas con `unittest` (`py -m unittest discover -s tests -t .`), sin red (clientes falsos y criptas artificiales).
- Bitácoras de ejemplo en `docs/ejemplos/` para `--replay`.
- Documento de decisiones actual: `docs/DecisionesDiseño.md`. Límite conocido: la carga `partida` con 400 salas supera 20 ms (§4.1 del documento).
- Consola de ≥ 113 columnas. Comandos de juego: `n/s/e/o`, `abrir`, `atacar #`, `esperar`, `recoger #`, `sig/ant`, `usar/equipar/soltar`, `ordenar peso|valor|nombre`, `pergamino [1-5]`, `guardar`, `cargar`, `salir`.

## D.3 Reglas de la Parte I (siguen vigentes salvo que la P2 las modifique)

### Cripta y actores
- Salas conectadas por salidas **N, S, E, O**; cada salida conecta exactamente dos salas y puede no existir, estar abierta o cerrada con llave. No hay cuadrícula: todos los actores de una sala son adyacentes.
- La cripta declara sala inicial, sala de salida, `llave_salida`, estadísticas iniciales del jugador, `inventario_max` y `presupuesto_solicitudes`.
- Actor = jugador o instancia de enemigo (dos ratas del mismo tipo comparten ficha pero son actores distintos con vida, sala, id de instancia y `tiempo_siguiente` propios).
- Atributos: `vida/vida_max`, `ataque`, `defensa`, `velocidad` (referencia 100), `tiempo_siguiente`, `comportamiento` (solo enemigos).

### Reloj virtual y eventos
- Reloj entero que **no depende de la hora real**. Bucle: tomar el evento con menor `tiempo_siguiente`, avanzar el reloj, ejecutar, reprogramar si corresponde.
- **Empate:** menor número de secuencia (creciente al programar). Todo reprogramación asigna secuencia nueva. Orden total determinista.
- Costos base: moverse 100, atacar 100, esperar 100, usar 50, equipar 50, recoger 25, soltar 25, abrir puerta con llave 50.
- Tras una acción de costo `c`:  
  $$\text{intervalo} = \max(1,\ c \cdot 100 \,//\, \text{velocidad}),\qquad t_{sig} = t_{reloj} + \text{intervalo}$$  
  (velocidad 150 y costo 100 → 66).
- **Cambio de velocidad** con acción programada, en el instante `t`:  
  $$\text{restante\_nuevo}=\max\!\big(1,\ (t_{sig}-t)\cdot v_{ant} \,//\, v_{nueva}\big),\qquad t_{sig}=t+\text{restante\_nuevo}$$

### Inicio y activación
- Reloj 0; el jugador en la sala inicial con primera acción en t=0. El contenido de la sala inicial se carga antes de aceptar la primera acción.
- Cargar contenido **no activa** enemigos: se activan cuando el jugador **entra** a la sala (los de la sala inicial, en t=0). Un enemigo activo que se mueve sigue activo. Primera acción de un recién activado: costo base 100 desde el reloj actual; si hay varios a la vez, se programan en orden ascendente de id de instancia.
- **Determinismo de red:** la latencia real no puede cambiar la simulación; esperar red nunca avanza el reloj virtual; una acción hacia una sala sin contenido no se confirma hasta tenerlo.

### Movimiento, puertas, combate
- Moverse requiere salida existente y puerta abierta; sin ataques gratuitos ni de oportunidad.
- Abrir y atravesar son acciones distintas; la llave no se consume; una puerta abierta sigue abierta salvo `cierre_automatico` (evento de cierre tras el intervalo). Enemigos no tienen inventario ni abren puertas.
- **Daño** $=\max(1,\ \text{ataque} + \texttt{azar.randint(0,4)} - \text{defensa})$ con `azar = random.Random(semilla)` propio. Al morir, deja de ejecutar eventos y suelta objetos de su campo `suelta` en el suelo.
- Misma versión de cripta + semilla + acciones ⇒ misma partida (incluida la secuencia de llamadas al generador).

### Inventario y objetos
- Capacidad `inventario_max`, un hueco por objeto sin importar peso; lleno ⇒ no se puede recoger. Equipar mueve al frente del orden real (máx. un arma y una armadura; la anterior queda en el inventario).
- Clases: arma (`ataque_bonus`), armadura (`defensa_bonus`), poción (`cura` o `modificador_velocidad` + `duracion`), antídoto (cancela veneno), llave (`abre`), antorcha (`duracion`), pergamino de retroceso.

### Enemigos (P1)
- En su turno: si comparte sala con el jugador **ataca**; si no, según comportamiento: **guardián** espera; **errante** elige al azar una salida abierta (si no hay, espera); **rastreador** examina solo vecinas accesibles y sigue el rastro más fresco (< 400 unidades; empate → menor id; si no hay, espera). Todas son acciones de costo 100.
- **Rastro:** cada sala guarda el último instante de presencia del jugador; la inicial en 0; al completar un movimiento, la destino recibe el reloj actual; se refresca por cada acción del jugador.

### Efectos
- **Veneno:** daño cada 80 durante 400 (el antídoto lo cancela). **Cambio de velocidad** (poción). **Antorcha:** se apaga tras `duracion`. **Regeneración:** cada 200, sin superar `vida_max`. **Trampa:** se activa al entrar, queda desarmada, se rearma a los 300 (u otro valor de la ficha). **Cierre de puerta** automático. Cancelar efectos o morir no debe obligar a recorrer todos los eventos pendientes.

### Pergamino de retroceso
- Deshace la última acción del jugador **y todo lo ocurrido hasta su siguiente acción** (enemigos, efectos, reloj, eventos, rastro, vida, inventario, suelo, puertas, trampas). **No consume tiempo ni se registra** como acción. Máximo 5 acciones atrás y tantos como pergaminos se tengan.
- Excepción: los pergaminos quedan **fuera** de la reversión (ni se restauran ni se devuelven los recogidos/soltados en el intervalo). La **caché no** es estado del juego.
- **Prohibido guardar copias completas del estado**: solo la información necesaria para invertir cambios.

### Victoria, derrota y puntaje
- Derrota: vida 0. Victoria: entrar a la sala de salida tras abrir con la llave correspondiente su puerta. La tabla de puntajes guarda: nombre, id y versión de cripta, acciones del jugador, enemigos derrotados, tiempo final.
- «Acción del jugador» = acción que consume tiempo virtual (no hay «turnos»).

## D.4 El servicio web

- Base: `https://cripta-api.kad06a0zhgs84.us-east-2.cs.amazonlightsail.com/v1` · Swagger: `.../docs`.
- **Cabecera obligatoria `X-Cripta-Client-Id`** (UUID generado **una vez por ejecución** y reutilizado en todas las solicitudes, incluidos reintentos).
- Cada solicitud tarda ~400 ms (igual para 1 que para 10 elementos). **HTTP 429**: cuerpo `{"error": ..., "reintentar_en": n}`; esperar y reintentar sin caerse; la espera real no mueve el reloj virtual; el reintento cuenta contra el presupuesto. Otros códigos: mensaje con la operación que falló. `requests` con `timeout` explícito.

| Endpoint | Para qué |
|---|---|
| `GET /criptas` | listar criptas (id, nombre, salas, dificultad) |
| `GET /criptas/{id}` | datos generales: versión, salas, páginas, sala inicial/salida, `llave_salida`, `presupuesto_solicitudes`, `inventario_max`, jugador |
| `GET /criptas/{id}/version` | verificación liviana de versión |
| `GET /criptas/{id}/salas?pagina=n` | **esqueleto** (≤ 50 salas por página) |
| `GET /criptas/{id}/contenido?salas=a,b,c` | contenido (enemigos, objetos, trampas) de ≤ 10 salas |
| `GET /catalogo?ids=...` | fichas de catálogo, ≤ 10 ids (el catálogo se comparte entre criptas) |
| `GET /catalogo/{id}` | una ficha (cuesta como un lote: normalmente desperdicia presupuesto) |
| `GET /catalogo/version` | versión global del catálogo |
| **(P2)** `GET /criptas/{id}/llaves` | ubicación de llaves: `{id, sala, enemigo?}` |

- **Presupuesto:** `presupuesto_solicitudes` lo define cada cripta (no se calcula ni se quema en el código). **Toda** solicitud cuenta (lista, generales, páginas, contenido, catálogo, versiones, reintentos 429). Lecturas de disco o `--offline` no cuentan. Al terminar se reporta: solicitudes vs presupuesto, aciertos y fallos de caché.
- **Modo `--offline`:** el programa lee respuestas guardadas por el **mismo contrato lógico** que el cliente de red; el modelo no sabe si vienen de HTTP o de disco.
- **Contrato P2 (OpenAPI v1.1.0):** agrega `costo` (≥ 1, opcional) en salidas, `comportamiento: cazador` + `rango` (≥ 1, opcional) en el catálogo y `/llaves`. Respuesta de `/llaves`: `{llaves: [{id, sala, enemigo?}]}`.

## D.5 Problemas de estructuras de datos de la Parte I (§4)

| § | Problema | Propiedades clave |
|---|---|---|
| 4.1 | Qué ocurre a continuación (agenda) | obtener el menor sin examinar todos; cientos de eventos; decenas de miles de operaciones; muerte y cancelación sin recorrer todo; reprogramación; orden determinista |
| 4.2 | Traer contenido antes de que haga falta (precarga) | nunca ubicar al jugador en sala sin contenido; lotes de hasta 10; no repetir solicitudes vigentes; respuestas pendientes en orden determinista |
| 4.3 | Resolución de referencias del catálogo | resolver ids a fichas por lotes; ids repetidos y en orden no controlado |
| 4.4 | Caché persistente | tope configurable; desalojo con justificación; **fichas en uso no se liberan**; recuperar de disco no cuenta como red; validar por versión; sobrevive al cierre; búsqueda en caché muy frecuente |
| 4.5 | Inventario | recorrer adelante/atrás; soltar en cualquier posición sin costo dependiente de la posición; equipar al frente; vista ordenada sin alterar el orden real |
| 4.6 | Historial reversible | ≤ 5 acciones; sin copias completas; pergaminos excluidos |
| 4.7 | Rastro | costo proporcional a salidas de la sala; caducidad (400); varios rastreadores en tiempo lineal |
| 4.8 | Bitácora en pantalla | últimos 20 mensajes; memoria constante; sin desplazar físicamente |
| 4.9 | Ordenamiento | ≥ 2 algoritmos distintos; elección automática por propiedades medibles; sin `list.sort()`/`sorted()` |
| 4.10 | Guardado binario | formato propio; recuperar una sala sin leer todo; detectar versión incompatible; comparar con JSON |
| 4.11 | Bitácora de partida y `--replay` | log append-only con cripta, versión de cripta, versión de catálogo y semilla; reproducción fiel o reporte de incompatibilidad |

**Rendimiento P1:** ciclo completo de eventos entre dos decisiones del jugador **< 20 ms**; `--bench` mide agenda, caché, disco, inventario, historial, ordenamientos, guardado.

## D.6 Arquitectura y restricciones (P1 §6–7, P2 §6.2)

- **MVC + adaptadores.** Modelo (reglas y estructuras) sin HTTP/archivos/interfaz. Vista (consola o gráfica; sin bonificación por gráfica). Controlador traduce acciones. Adaptadores de red y disco detrás de interfaces. `--replay` y `--bench` **no** instancian la vista.
- **Prohibido:** `dict` como índice/caché/tabla de búsqueda/estructura propia (se permiten los dict de `respuesta.json()` solo para leer JSON); equivalentes de bibliotecas.
- **Permitido:** `list` como almacenamiento contiguo, `struct`, `json`, `requests`, bibliotecas de interfaz.
- **P2 añade (para los problemas evaluados de §5):** prohibidos `heapq`, `bisect`, `collections` (`deque`, `OrderedDict`, `defaultdict`, `Counter`), `networkx` y cualquier biblioteca de grafos o rutas; `set` queda prohibido en las mismas condiciones que `dict`.
- spec-kit y el agente son **herramientas de proceso**: no pueden introducir dependencias prohibidas en el código entregado. **Revisar cada plan generado.**

## D.7 La Parte II: qué cambia (resumen de capacidades)

1. **Terreno y cazadores** — las salidas tienen costo; aparece un enemigo que calcula la ruta más barata hacia el jugador.
2. **Niebla de guerra** — el jugador solo conoce lo explorado; puede viajar automáticamente («ir a»).
3. **Resolubilidad** — antes de jugar, determinar si la cripta puede ganarse y explicar por qué si no.
4. **Línea de tiempo** — consultar el estado en cualquier instante pasado sin copiar el estado completo en cada acción.

*«Las decisiones de la Parte I pueden dejar de ser adecuadas con las reglas nuevas. Detectarlo, medirlo y documentar el cambio es parte esperada del trabajo.»*

### D.7.1 Terreno y costo de salidas (P2 §3.1)
- Campo `costo` (entero ≥ 1) en cada salida; si falta, **100**; igual en ambos sentidos.
- Moverse cuesta el costo de la salida (en vez de 100). Intervalo: $\max(1,\ \text{costo\_salida}\cdot 100 // \text{velocidad})$. Aplica a todos los actores. El resto de acciones no cambia.

### D.7.2 Cazador (P2 §3.2)
- Cuarto comportamiento; la ficha trae `rango` (unidades de costo). En su turno: (1) ataca si comparte sala; (2) calcula el costo mínimo `d` hasta la sala **actual** del jugador usando solo salidas **abiertas ahora**; (3) si no hay ruta o `d > rango`, espera (100); (4) si no, se mueve un paso por una ruta de costo `d`; el costo de la acción es el de la salida.
- **Desempate:** entre vecinas `v` con `costo(u,v) + dist(v,jugador) = d`, va a la de **menor id**.
- Conoce el **esqueleto completo** y el estado actual de las puertas; **no** le afecta la niebla ni si el contenido se descargó. No abre puertas.
- **Equivalencia observable:** la decisión de cada turno es idéntica a recalcular desde cero. Se puede reutilizar cálculo solo si no cambia la respuesta.

### D.7.3 Niebla de guerra (P2 §3.3)
- Estados por sala: **explorada** (nombre, salidas, costos, puertas según última observación; la inicial lo está desde t=0), **avistada** (destino de una salida de una explorada; solo se sabe que existe), **desconocida**.
- **Memoria de puertas:** se observa una puerta al estar en cualquiera de sus dos salas; se recuerda el último estado visto aunque haya cambiado.
- **Antorcha encendida:** al entrar a una sala quedan exploradas también todas sus vecinas (cualquier salida, abierta o cerrada); se revela nombre y salidas, **no** contenido; **no** se activan enemigos ni trampas.
- El programa sigue descargando todo el esqueleto y la precarga puede usarlo (infraestructura), pero **la vista y «ir a» solo usan el conocimiento del jugador**.
- El conocimiento es **estado del juego**: se guarda, se revierte con el pergamino y entra en la línea de tiempo. Hay comando para ver el mapa conocido.

### D.7.4 Viaje automático «ir a» (P2 §3.4)
- `ir a <sala>` hacia una sala **explorada**; ruta sobre el subgrafo conocido (solo salas exploradas y salidas recordadas abiertas), mínimo costo, desempate igual que el cazador.
- Cada paso es una acción completa del jugador (consume tiempo; corren los eventos); ruta **recalculada antes de cada paso**. Se detiene al: llegar; entrar a sala con enemigos (activos o dormidos); recibir daño; perder ruta conocida. **No abre puertas** aunque haya llave.
- `partida.log`: cada paso como movimiento individual + la orden como comentario. El pergamino revierte solo el último paso.

### D.7.5 Resolubilidad (P2 §3.5)
- Supuestos: se atraviesan salidas abiertas y cerradas con llave ya obtenida; llaves no se consumen; todo enemigo es derrotable; la llave de un enemigo está en la sala donde ese enemigo **inicia**; trampas y cierres automáticos no bloquean.
- **Resoluble:** desde la sala inicial se puede obtener `llave_salida` y llegar a `sala_salida` por una puerta que la requiere.
- Si es resoluble: **orden determinista** de obtención de llaves (cada llave después de las necesarias para alcanzarla).
- Si no: llaves no obtenibles; puertas de la **frontera bloqueada** con la llave que exigen; dónde está cada una; y el **ciclo concreto** si una llave está tras puertas que solo ella (directa o indirectamente) abre.
- Sin `--forzar`, una cripta no resoluble no inicia. `--verificar <cripta>` solo verifica, sin vista.

### D.7.6 Línea de tiempo (P2 §3.6)
- Estado en `t` = tras ejecutar todos los eventos con tiempo ≤ t (si a `t` toca decisión del jugador, justo antes de tomarla).
- `historia <t>` / `historia #k`: reloj, sala, vida y estadísticas, inventario, efectos activos, enemigos de la sala con vida, mapa conocido de ese momento. No consume tiempo, no se registra, no altera el estado ni el historial de retroceso.
- `--replay partida.log --hasta <t>` imprime el mismo resumen sin vista. Las acciones revertidas con pergamino dejan de existir en la línea. Consultar un instante posterior al reloj actual se rechaza.
- **Memoria:** puntos de control (copias completas) como máximo uno cada **K** acciones (`--checkpoint-cada K`, por defecto justificado con mediciones); una consulta aplica/deshace como máximo K acciones. Reconstrucción hacia adelante (re-simulando; el punto guarda el estado de `random.Random`) o hacia atrás (invirtiendo cambios).
- Guardar/cargar conserva la línea completa; el formato binario cambia y un archivo de la P1 se detecta como incompatible o se migra explícitamente.

## D.8 Problemas de estructuras de la Parte II (§5)

| § | Problema | Exigencias principales |
|---|---|---|
| 5.1 | Ruta más barata del cazador | costos no uniformes; costo proporcional a la región dentro del rango (no al tamaño de la cripta); decenas de cazadores al mismo objetivo: medir **cálculo compartido vs individual**; estructuras auxiliares propias; desempate siempre |
| 5.2 | Rutas que dejan de ser válidas | eventos que invalidan (puertas, jugador, cambios de sala, velocidad); decisión = cálculo desde cero; demostrar cuándo es válido reutilizar; `--bench` con puertas estables vs inestables y alternativa de recalcular siempre |
| 5.3 | Mapa conocido | consultas frecuentes (cada vista, cada paso de «ir a», cada antorcha); exploración proporcional a salas reveladas; barato de registrar/invertir; justificar si «ir a» comparte implementación con el cazador |
| 5.4 | Resolubilidad | recorrido incremental (costo ~ lineal en salas, salidas, llaves); frontera y dependencias salen del mismo recorrido; ciclo determinista y concreto; `--bench` contra la alternativa ingenua con muchas llaves encadenadas |
| 5.5 | Línea de tiempo y puntos de control | ≤ K acciones por consulta; memoria ~ cambios + 1 punto cada K; ubicar el punto de control más cercano (búsqueda frecuente); recorte al usar pergamino sin recorrer la historia; mediciones con ≥ 3 valores de K y justificar el valor por defecto; adelante vs atrás con evidencia |
| 5.6 | Revisión de decisiones de la P1 | repetir mediciones con la carga nueva (en especial agenda de eventos e historial de retroceso); si alguna decisión deja de ser adecuada: cambiarla y documentar antes y después |

## D.9 Límites de rendimiento (P2 §6.1; pueden ajustarse por enmienda)

| Operación | Límite | Condición |
|---|---|---|
| Ciclo de eventos entre dos decisiones del jugador | **20 ms** | cripta de referencia con decenas de cazadores activos |
| Verificación de resolubilidad | **200 ms** | la cripta publicada más grande |
| Consulta `historia` | **50 ms** | partida ≥ 5 000 acciones, K por defecto |
| Paso de «ir a» | **5 ms** | mapa conocido completo de la cripta de referencia |

Todos medidos en el equipo local, sin red ni renderizado. Las criptas sintéticas de `--bench` son deterministas por semilla.

## D.10 spec-kit: reglas del curso (P2 §2)

- Instalación con `uv`, versión fijada (`@vX.Y.Z`), registrada en el README; el agente (Claude Code, Copilot, Gemini CLI…) lo decide el grupo y se indica en el README; los archivos generados se versionan.
- Flujo por capacidad: **constitution (una vez) → specify → clarify → plan → tasks → analyze → implement**.
- **Mínimo una especificación por capacidad**: terreno y cazador; niebla de guerra (incluido «ir a»); resolubilidad; línea de tiempo.
- **Constitución** con (en palabras del grupo): estructuras a mano y prohibiciones; determinismo; MVC con `--replay`/`--bench` sin vista; sin datos de cripta concreta; respeto del presupuesto; afirmaciones de rendimiento respaldadas con `--bench`; especificación antes que implementación.
- **Qué va en cada artefacto:** `spec.md` (reglas, historias, escenarios, requisitos numerados; **sin** estructuras/clases/módulos); `plan.md` (estructuras, alternativas, complejidad, módulos, mediciones; **sin** reglas nuevas); `tasks.md` (tareas pequeñas con requisito asociado; **sin** tareas huérfanas). El `plan.md` es borrador de la sección del Documento de Decisiones.
- **Trazabilidad:** `FR-…` estable ↔ escenario de aceptación (cada caso del Apéndice B) ↔ tarea ↔ prueba o `partida.log` que cita el id.
- **Historial:** la spec de cada capacidad se confirma **antes** que el código; si la spec estaba mal, se corrige primero y en commit separado. Una spec desactualizada respecto del programa se **penaliza**.
- Cada invocación de `/speckit.*` con texto propio es un prompt y se registra en `PROMPTS_LLM.md`.

## D.11 Entregables, estructura mínima y evaluación (P2 §7)

Repositorio con: `.specify/memory/constitution.md`, `specs/<NNN-capacidad>/{spec,plan,tasks}.md`, `DECISIONES.md`, `PROMPTS_LLM.md`, `README.md` (con versión de spec-kit, agente, comandos nuevos `--verificar`, `--forzar`, `--checkpoint-cada`, `--replay … --hasta`, y cómo correr las pruebas de aceptación).

**Interfaz mínima adicional:** ver mapa conocido; `ir a <sala>` y ver por qué se detuvo; `historia <t>` e `historia #k`; reporte de resolubilidad al iniciar; mostrar costos de salidas de la sala actual y distinguir a los cazadores.

| Rubro | Peso dentro del proyecto |
|---|---|
| Especificaciones, constitución y proceso spec-kit (calidad, trazabilidad, historial) | 20 % |
| Terreno, cazador e invalidación de rutas | 20 % |
| Niebla de guerra e «ir a» | 10 % |
| Verificación de resolubilidad | 15 % |
| Línea de tiempo y puntos de control | 15 % |
| Documento de Decisiones de Diseño | 10 % |
| Rendimiento | 10 % |

**Documento de Decisiones** (por problema): problema (operaciones reales y frecuencias medidas) · alternativas (≥ 2, con razón concreta de descarte) · decisión · complejidad (operaciones más frecuentes) · evidencia con `--bench` (al menos una mide la alternativa descartada) · límites conocidos. Cada sección nueva enlaza a su spec y plan, indica si la decisión final coincide con el `plan.md` original y, si no, qué medición la cambió.

**Defensa:** cripta nunca vista (más grande, posiblemente no resoluble); `--replay` y `--bench` en vivo; requisito al azar con su cadena (escenario → tarea → código → prueba); **cambio pequeño de regla**: primero la spec, luego el código; cualquier integrante explica **cualquier** especificación.

## D.12 Casos del Apéndice B (cada uno debe ser un escenario de aceptación)

**Parte I (siguen vigentes):**
- Recoger con inventario lleno: no se ejecuta ni consume tiempo.
- Abrir sin la llave correcta: se rechaza, sin tiempo.
- Errante sin salidas abiertas: espera con costo 100.
- El rastro de la sala actual se refresca en cada acción del jugador.
- Rastreador con dos vecinos igual de frescos: menor id.
- Enemigo muerto con eventos futuros: no producen acciones.
- Antídoto cancela veneno antes del siguiente pulso: los pulsos cancelados no hacen daño.
- Puerta se cierra automáticamente con un actor ya del otro lado: permanece; solo se impide atravesar de nuevo hasta abrir.
- Regeneración y pociones nunca superan `vida_max`.
- Movimiento hacia contenido pendiente: espera la información; la espera real no mueve el reloj.
- Replay con versión incompatible: reporta la incompatibilidad.
- Pergamino cuando el intervalo incluía recoger otro pergamino: la reversión no lo devuelve al suelo; la cantidad refleja solo el consumo.
- Dos pergaminos seguidos: el segundo retrocede la acción anterior a la ya revertida.

**Parte II — terreno y cazador:** sin ruta abierta → espera 100 · ruta > rango → espera 100 · menos salas pero mayor costo vs más salas y menor costo → menor costo · dos vecinas con rutas mínimas → menor id · puerta de la ruta se cierra entre turnos → decide desde cero · velocidad alta con salida de costo 1 → intervalo ≥ 1 · cambio de velocidad en salida costosa → escala según P1 §2.3.

**Parte II — niebla e «ir a»:** `ir a` sala no explorada → rechazo sin tiempo · mapa recuerda abierta una puerta cerrada → se actualiza, se recalcula; sin ruta, se detiene sin tiempo adicional · sala con enemigos dormidos → se activan y se detiene · antorcha: explora vecinas sin activar enemigos ni trampas · pergamino revierte entrada con antorcha → salas vuelven al estado anterior · pergamino durante un viaje → revierte solo el último paso y el viaje no continúa.

**Parte II — resolubilidad:** `llave_salida` tras la única puerta que ella abre → no resoluble, señala el ciclo · llave en `suelta` de un errante → sala inicial del enemigo · varios órdenes válidos → mismo orden en dos ejecuciones · no resoluble sin `--forzar` → no inicia y muestra el reporte.

**Parte II — línea de tiempo:** `historia <t>` con `t` > reloj → rechazo · `historia` tras pergamino → no muestra acciones revertidas · varios eventos en el mismo `t` → estado tras todos · `historia` no consume tiempo, no va a `partida.log`, no toca el historial de retroceso · `--replay --hasta t` posterior al final → estado final e indica que terminó antes · archivo de la P1 → incompatibilidad reportada o migración explícita.

## D.13 Glosario rápido

| Término | Significado |
|---|---|
| **Reloj virtual** | contador entero propio del juego; no depende de la hora real |
| **Agenda de eventos** | colección de eventos programados con `tiempo_siguiente` y secuencia |
| **Esqueleto** | salas y conexiones (liviano, se descarga completo por páginas) |
| **Contenido** | enemigos, objetos y trampas por sala (por lotes) |
| **Catálogo** | fichas técnicas reutilizables (enemigos, objetos, trampas) |
| **Instancia vs ficha** | la ficha se comparte; la instancia es un actor/objeto concreto |
| **Rastro** | último instante en que el jugador estuvo en una sala |
| **Niebla de guerra** | el jugador solo conoce lo explorado |
| **Frontera bloqueada** | puertas cerradas adyacentes a la región alcanzable, con su llave |
| **Punto de control** | copia completa del estado, como máximo cada K acciones |
| **SDD** | Spec-Driven Development: especificar → planificar → tareas → implementar |
| **Constitución** | reglas del proyecto que todo agente lee en cada fase |
| **Deriva de especificación** | spec desactualizada respecto del programa (penalizada) |
| **Replay / bitácora** | reproducir una partida desde `partida.log` con semilla y acciones |

## D.14 Preguntas para arrancar (del enunciado; sirven para discutir, no se responden por escrito)

- Treinta cazadores persiguen al mismo jugador: ¿cuántas búsquedas de ruta hacen falta realmente por ciclo?
- Una puerta con cierre automático se cierra lejos de todos los cazadores: ¿qué rutas siguen siendo válidas y cómo lo saben sin recalcular?
- ¿Qué diferencia hay entre «encontró una ruta» y «encontró la ruta que exige el desempate»?
- ¿Qué información mínima hay que registrar para revertir la exploración de cinco salas con una antorcha encendida?
- Una llave abre una región con otras tres llaves: ¿qué hace la verificación con las puertas que encontró cerradas antes de tener esa llave?
- Con K = 1 la consulta es instantánea y con K infinito no hay copias: ¿dónde está el punto razonable y cómo lo miden?
- ¿Qué cosas escribirían en `spec.md` que un agente no podría deducir del enunciado? ¿Cuáles no deberían escribir allí?
- Si el agente propone `heapq` en `plan.md`: ¿en qué fase debería detectarse y por quién? *(Respuesta del equipo: en `/speckit.analyze` y en la revisión humana del plan antes de fusionar el PR-docs; lo detecta cualquiera de los tres, y `scripts/revisar_prohibidos.py` es la red de seguridad.)*

---

*Fin del documento. Mantenerlo actualizado: si cambia una regla por enmienda del profesor, primero se edita aquí y en la spec correspondiente, luego el código.*
