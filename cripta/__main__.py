'''Arranque de Cripta: arma infraestructura, servicio, vista y controlador (la vista solo en la rama interactiva).
Banderas: --offline (lee fixtures/), --cache-size N (fichas del catálogo en memoria) y --bench (mediciones sin vista).
Con --bench se aceptan además --escala, --solo y --markdown; --replay RUTA reproduce un log sin vista.
Archivos generados en datos/: cache/, puntajes/, partida.sav y partida.log.
Uso: py -m cripta [--offline] [--cache-size N]  |  py -m cripta --bench [--escala X]  |  py -m cripta --replay partida.log
'''
import argparse
import sys
from pathlib import Path

from cripta.constantes import CACHE_TAMANO_DEFAULT
from cripta.controlador.controlador_cripta import ControladorCripta
from cripta.excepciones import CriptaError
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cache import CacheDisco
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.cliente_http import ClienteHttp
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.puntajes_disco import RepositorioPuntajes
from cripta.servicios.servicio_partida import ServicioPartida
from cripta.servicios.servicio_replay import ServicioReplay
from cripta.vista.vista_consola import VistaConsola

DIRECTORIO_DATOS = Path("datos")
DIRECTORIO_FIXTURES = "fixtures"


def _entero_positivo(texto: str) -> int:
    # Valida --cache-size: el tope de la caché en memoria debe ser un entero mayor o igual a 1
    try:
        valor = int(texto)
    except ValueError:
        valor = 0
    if valor < 1:
        raise argparse.ArgumentTypeError("debe ser un entero mayor o igual a 1")
    return valor


def _reproducir(servicio, ruta: str) -> int:
    # --replay: sin vista ni interacción (§6). Código 0 solo si la reproducción fue fiel; 2 si falla algo externo
    try:
        resultado = ServicioReplay(servicio).reproducir(ruta)
    except CriptaError as error:
        print(f"[Error] {error}", file=sys.stderr)
        return 2
    print(resultado.informe())
    return 0 if resultado.fiel else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="cripta", description="Cripta: juego de mazmorra por eventos.")
    parser.add_argument("--offline", action="store_true", help="usa las respuestas guardadas en fixtures/ en vez de la red")
    parser.add_argument("--cache-size", type=_entero_positivo, default=CACHE_TAMANO_DEFAULT, metavar="N",
                        help=f"tope de fichas del catálogo en memoria (por defecto {CACHE_TAMANO_DEFAULT})")
    parser.add_argument("--replay", metavar="PARTIDA.LOG", help="reproduce una partida desde su bitácora, sin vista")
    parser.add_argument("--bench", action="store_true",
                        help="ejecuta las cargas sintéticas sin vista; admite --escala, --solo y --markdown")
    argumentos, resto = parser.parse_known_args(argv)

    if argumentos.bench:
        # Los argumentos que no son del juego (--escala, --solo, --markdown) los interpreta el propio bench
        from cripta.servicios.servicio_bench import ejecutar_bench_cli
        return ejecutar_bench_cli(resto)
    if resto:
        parser.error(f"argumentos no reconocidos: {' '.join(resto)}")

    contador = ContadorSolicitudes()
    cliente = ClienteOffline(DIRECTORIO_FIXTURES) if argumentos.offline else ClienteHttp(contador)
    repositorio_puntajes = RepositorioPuntajes(AlmacenDiscoArchivos(DIRECTORIO_DATOS / "puntajes"))
    servicio = ServicioPartida(
        ClienteGeneral(cliente), contador,
        cache_disco=CacheDisco(AlmacenDiscoArchivos(DIRECTORIO_DATOS / "cache")),
        tamano_cache=argumentos.cache_size,
        repositorio_puntajes=repositorio_puntajes,
    )
    if argumentos.replay is not None:
        return _reproducir(servicio, argumentos.replay)
    ControladorCripta(
        servicio, VistaConsola(),
        ruta_guardado=str(DIRECTORIO_DATOS / "partida.sav"),
        ruta_bitacora=str(DIRECTORIO_DATOS / "partida.log"),
        leer_puntajes=servicio.puntajes_globales,
    ).ejecutar()
    print("\n" + servicio.reporte_final())
    return 0


if __name__ == "__main__":
    sys.exit(main())