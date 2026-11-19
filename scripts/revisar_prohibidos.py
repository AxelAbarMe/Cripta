"""Auditor estático de estructuras y patrones vetados para Cripta 2.
Analiza importaciones, llamadas y literales prohibidos con ast y tokenize.
"""
import ast
import io
import os
import re
import sys
import tokenize

MODULOS_PROHIBIDOS = ("heapq", "bisect", "collections", "networkx")
PATRON_CRIPTA = re.compile(r"\bcripta-\d+\b", re.IGNORECASE)
PATRON_ENTIDAD = re.compile(r"\bent_[a-zA-Z0-9_]+", re.IGNORECASE)
CARPETAS_AVISO_ESTRUCTURAS = ("modelo", "estructuras", "servicios", "controlador")
CARPETAS_EXCLUIDAS_AVISO = ("infraestructura", "dto", "vista")


def corresponde_aviso_estructuras(ruta: str) -> bool:
    # Determina si el archivo pertenece a las carpetas auditadas para avisos
    partes = [p.lower() for p in os.path.normpath(ruta).split(os.sep)]
    for excluida in CARPETAS_EXCLUIDAS_AVISO:
        if excluida in partes:
            return False
    for carpeta in CARPETAS_AVISO_ESTRUCTURAS:
        if carpeta in partes:
            return True
    return False


def ordenar_elementos(elementos):
    # Ordena pares linea y mensaje sin usar funciones vetadas
    lista = list(elementos)
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and lista[j][0] > actual[0]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista


def ordenar_rutas(rutas):
    # Ordena rutas lexicograficamente mediante insercion
    lista = list(rutas)
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and str(lista[j]) > str(actual):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista


class VisitanteAuditoria(ast.NodeVisitor):
    # Recorre el arbol sintactico para detectar patrones prohibidos

    def __init__(self, ruta: str, evaluar_estructuras: bool):
        self.ruta = ruta
        self.evaluar_estructuras = evaluar_estructuras
        self.errores = []
        self.avisos = []

    def visit_Import(self, node):
        # Detecta importaciones directas de modulos vetados
        for alias in node.names:
            modulo = alias.name.split(".")[0]
            if modulo in MODULOS_PROHIBIDOS:
                self.errores.append((node.lineno, f"importación prohibida de '{alias.name}'"))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Detecta clausulas from import desde modulos vetados
        if node.module:
            modulo = node.module.split(".")[0]
            if modulo in MODULOS_PROHIBIDOS:
                self.errores.append((node.lineno, f"importación prohibida desde '{node.module}'"))
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detecta llamadas a funciones y metodos vetados o a revisar
        if isinstance(node.func, ast.Name):
            if node.func.id == "sorted":
                self.errores.append((node.lineno, "llamada prohibida a 'sorted(...)'"))
            elif self.evaluar_estructuras and node.func.id in ("dict", "set"):
                self.avisos.append((node.lineno, f"llamada a '{node.func.id}(...)' a revisar"))
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr == "sort":
                self.errores.append((node.lineno, "llamada prohibida al método '.sort(...)'"))
        self.generic_visit(node)

    def visit_Dict(self, node):
        # Reporta literales de diccionario en modulos sensibles
        if self.evaluar_estructuras:
            self.avisos.append((node.lineno, "literal de dict a revisar"))
        self.generic_visit(node)

    def visit_Set(self, node):
        # Reporta literales de conjunto en modulos sensibles
        if self.evaluar_estructuras:
            self.avisos.append((node.lineno, "literal de set a revisar"))
        self.generic_visit(node)

    def visit_DictComp(self, node):
        # Reporta comprensiones de diccionario en modulos sensibles
        if self.evaluar_estructuras:
            self.avisos.append((node.lineno, "comprensión de dict a revisar"))
        self.generic_visit(node)

    def visit_SetComp(self, node):
        # Reporta comprensiones de conjunto en modulos sensibles
        if self.evaluar_estructuras:
            self.avisos.append((node.lineno, "comprensión de set a revisar"))
        self.generic_visit(node)

    def visit_Constant(self, node):
        # Detecta cadenas con identificadores fijos de cripta o entidad
        if isinstance(node.value, str):
            if PATRON_CRIPTA.search(node.value):
                self.errores.append((node.lineno, f"id de cripta concreto en cadena -> '{node.value}'"))
            elif PATRON_ENTIDAD.search(node.value):
                self.errores.append((node.lineno, f"id de entidad concreto en cadena -> '{node.value}'"))
        self.generic_visit(node)


def revisar_comentarios(ruta: str) -> list:
    # Busca punto y coma en comentarios usando el modulo tokenize
    avisos = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        contenido_bytes = contenido.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        tokens = tokenize.tokenize(io.BytesIO(contenido_bytes).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT and ";" in token.string:
                avisos.append((token.start[0], f"punto y coma dentro de comentario -> {token.string.strip()}"))
    except (tokenize.TokenError, IndentationError, SyntaxError, UnicodeDecodeError):
        pass
    return avisos


def revisar_archivo(ruta: str) -> tuple:
    # Audita un archivo de Python individual y retorna errores y avisos
    evaluar_estructuras = corresponde_aviso_estructuras(ruta)
    errores = []
    avisos = []

    with open(ruta, "r", encoding="utf-8") as archivo:
        try:
            arbol = ast.parse(archivo.read(), filename=ruta)
            visitante = VisitanteAuditoria(ruta, evaluar_estructuras)
            visitante.visit(arbol)
            for lineno, mensaje in visitante.errores:
                errores.append((lineno, mensaje))
            for lineno, mensaje in visitante.avisos:
                avisos.append((lineno, mensaje))
        except SyntaxError as error_sintaxis:
            errores.append((error_sintaxis.lineno or 1, f"error de sintaxis -> {error_sintaxis.msg}"))

    for lineno, mensaje in revisar_comentarios(ruta):
        avisos.append((lineno, mensaje))

    errores_ordenados = ordenar_elementos(errores)
    avisos_ordenados = ordenar_elementos(avisos)

    resultado_errores = [f"{ruta}:{lineno}: {msg}" for lineno, msg in errores_ordenados]
    resultado_avisos = [f"{ruta}:{lineno}: {msg}" for lineno, msg in avisos_ordenados]
    return resultado_errores, resultado_avisos


def recopilar_archivos(objetivos) -> list:
    # Reune todos los archivos con extension py en los objetivos dados
    archivos = []
    for objetivo in objetivos:
        if os.path.isfile(objetivo):
            if objetivo.endswith(".py"):
                archivos.append(objetivo)
        elif os.path.isdir(objetivo):
            for raiz, _, nombres in os.walk(objetivo):
                for nombre in nombres:
                    if nombre.endswith(".py"):
                        archivos.append(os.path.join(raiz, nombre))
    return ordenar_rutas(archivos)


def ejecutar(argumentos=None) -> int:
    # Corre la auditoria sobre los objetivos y reporta el conteo final
    if argumentos is None:
        argumentos = sys.argv[1:]
    if not argumentos:
        argumentos = ["cripta"]

    archivos = recopilar_archivos(argumentos)
    todos_errores = []
    todos_avisos = []

    for archivo in archivos:
        errores, avisos = revisar_archivo(archivo)
        for error in errores:
            todos_errores.append(error)
            print(f"ERROR: {error}")
        for aviso in avisos:
            todos_avisos.append(aviso)
            print(f"AVISO: {aviso}")

    total_errores = len(todos_errores)
    total_avisos = len(todos_avisos)
    print(f"\nAuditoría finalizada: {total_errores} error(es), {total_avisos} aviso(s).")

    return 1 if total_errores > 0 else 0


if __name__ == "__main__":
    sys.exit(ejecutar())
