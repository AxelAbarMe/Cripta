"""ServicioBench: orquesta las cargas sintéticas de bench/cargas_bench.py para la
bandera --bench (§5.3). Corre SIN vista (§6: "--bench debe ejecutarse sin instanciar
la vista interactiva") — solo produce texto plano y, opcionalmente, una tabla en
Markdown lista para pegar en docs/DecisionesDiseño.md (§8.5: evidencia empírica).

No mide nada por sí mismo: cada función de bench/cargas_bench.py ya sabe medir SU
subsistema (incluida la alternativa descartada cuando el PDF lo exige). Este
servicio solo decide CUÁLES correr, con qué escala, y cómo mostrar el resultado.
"""
import platform
import sys
import time

from cripta.bench.cargas_bench import CARGAS
from cripta.estructuras.ordenamiento_selector import ordenar_auto


class SubsistemaDesconocidoError(ValueError):
    def __init__(self, pedidos, validos):
        self.pedidos = pedidos
        pedidos_ordenados = list(pedidos)
        ordenar_auto(pedidos_ordenados)
        super().__init__(
            f"Subsistema(s) desconocido(s): {', '.join(pedidos_ordenados)}. "
            f"Válidos: {', '.join(n for n, _ in validos)}"
        )


class ServicioBench:
    def __init__(self, escala: float = 1.0):
        if escala <= 0:
            raise ValueError("escala debe ser positiva")
        self.escala = escala

    def ejecutar(self, subsistemas=None) -> dict:
        """subsistemas: nombres a correr (None = todos, en el orden de CARGAS).
        Devuelve {nombre: (segundos_totales, [Resultado, ...])}."""
        if subsistemas is not None:
            nombres_validos = []
            for par in CARGAS:
                nombres_validos.append(par[0])

            faltantes = []
            for pedido in subsistemas:
                es_valido = False
                for valido in nombres_validos:
                    if pedido == valido:
                        es_valido = True
                        break
                if not es_valido:
                    ya_agregado = False
                    for f in faltantes:
                        if f == pedido:
                            ya_agregado = True
                            break
                    if not ya_agregado:
                        faltantes.append(pedido)

            if faltantes:
                raise SubsistemaDesconocidoError(faltantes, CARGAS)

            elegidos = []
            for par in CARGAS:
                for pedido in subsistemas:
                    if par[0] == pedido:
                        elegidos.append(par)
                        break
        else:
            elegidos = CARGAS

        salida = {}
        for nombre, funcion in elegidos:
            t0 = time.perf_counter()
            resultados = funcion(self.escala)
            salida[nombre] = (time.perf_counter() - t0, resultados)
        return salida

    # ------------------------------------------------------------- reportes
    def reporte_texto(self, salida: dict) -> str:
        lineas = [f"--bench  (Python {platform.python_version()}, escala={self.escala})"]
        total = 0.0
        for nombre, (duracion, resultados) in salida.items():
            total += duracion
            lineas.append(f"\n=== {nombre.upper()}  ({duracion:.2f} s) ===")
            for r in resultados:
                base = f"  {r.caso}: razón" if r.es_razon else f"  {r.caso}: {r.segundos * 1000:.3f} ms"
                if r.operaciones > 1 and not r.es_razon:
                    base += f" totales, {r.micros_por_operacion:.2f} µs/op ({r.operaciones} ops)"
                if r.nota:
                    base += f"\n      -> {r.nota}"
                lineas.append(base)
        lineas.append(f"\nTotal: {total:.2f} s")
        return "\n".join(lineas)

    def reporte_markdown(self, salida: dict) -> str:
        """Tabla lista para pegar en la sección 'Evidencia empírica' de cada
        problema en docs/DecisionesDiseño.md (§8.5)."""
        lineas = ["| Subsistema | Caso | Tiempo | Nota |", "|---|---|---:|---|"]
        for nombre, (_duracion, resultados) in salida.items():
            for r in resultados:
                if r.es_razon:
                    tiempo = "razón"
                else:
                    tiempo = (f"{r.micros_por_operacion:.2f} µs/op" if r.operaciones > 1
                              else f"{r.segundos * 1000:.3f} ms")
                lineas.append(f"| {nombre} | {r.caso} | {tiempo} | {r.nota} |")
        return "\n".join(lineas)

    def verificar_limite_ciclo(self, salida: dict, limite_ms: float = 20.0) -> bool:
        """True si TODOS los casos de 'ciclo', 'partida' y 'ciclo_referencia' cumplieron el límite de §5.2."""
        for nombre in ("ciclo", "partida", "ciclo_referencia"):
            if nombre in salida and any("NO CUMPLE" in (r.nota or "") for r in salida[nombre][1]):
                return False
        return True


def ejecutar_bench_cli(argv=None) -> int:
    """Punto de entrada para --bench desde __main__.py. No importa nada de vista/
    controlador: cumple la regla de correr sin interfaz interactiva (§6)."""
    import argparse

    parser = argparse.ArgumentParser(prog="cripta --bench", add_help=True)
    parser.add_argument("--escala", type=float, default=1.0)
    parser.add_argument("--solo", nargs="+", default=None, metavar="SUBSISTEMA",
                        help=f"uno o más de: {', '.join(n for n, _ in CARGAS)}")
    parser.add_argument("--markdown", metavar="ARCHIVO",
                        help="además, escribe la tabla de evidencia en este archivo")
    args = parser.parse_args(argv)

    servicio = ServicioBench(escala=args.escala)
    try:
        salida = servicio.ejecutar(args.solo)
    except SubsistemaDesconocidoError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print(servicio.reporte_texto(salida))
    if args.markdown:
        with open(args.markdown, "w", encoding="utf-8") as archivo:
            archivo.write(servicio.reporte_markdown(salida))
        print(f"\nTabla Markdown escrita en {args.markdown}")

    return 0 if servicio.verificar_limite_ciclo(salida) else 1