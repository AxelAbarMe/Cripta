'''Arranque mínimo de Cripta para probar la vista de consola: arma infraestructura, servicio, vista y controlador.
Bandera: --offline (lee fixtures/ en lugar de la red). Faltan --cache-size, --replay y --bench.
Archivos generados en datos/: cache/, puntajes/, partida.sav y partida.log.
Uso: py -m cripta [--offline]   (en Linux o macOS: python -m cripta [--offline])
'''
import argparse
from pathlib import Path

from cripta.controlador.controlador_cripta import ControladorCripta
from cripta.infraestructura.almacen_disco import AlmacenDiscoArchivos
from cripta.infraestructura.cache import CacheDisco
from cripta.infraestructura.cliente_general import ClienteGeneral
from cripta.infraestructura.cliente_http import ClienteHttp
from cripta.infraestructura.cliente_offline import ClienteOffline
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes
from cripta.infraestructura.puntajes_disco import RepositorioPuntajes
from cripta.servicios.servicio_partida import ServicioPartida
from cripta.vista.vista_consola import VistaConsola

DIRECTORIO_DATOS = Path("datos")
DIRECTORIO_FIXTURES = "fixtures"


def main() -> None:
    parser = argparse.ArgumentParser(prog="cripta", description="Cripta: juego de mazmorra por eventos.")
    parser.add_argument("--offline", action="store_true", help="usa las respuestas guardadas en fixtures/ en vez de la red")
    argumentos = parser.parse_args()

    contador = ContadorSolicitudes()
    cliente = ClienteOffline(DIRECTORIO_FIXTURES) if argumentos.offline else ClienteHttp(contador)
    repositorio_puntajes = RepositorioPuntajes(AlmacenDiscoArchivos(DIRECTORIO_DATOS / "puntajes"))
    servicio = ServicioPartida(
        ClienteGeneral(cliente), contador,
        cache_disco=CacheDisco(AlmacenDiscoArchivos(DIRECTORIO_DATOS / "cache")),
        repositorio_puntajes=repositorio_puntajes,
    )
    ControladorCripta(
        servicio, VistaConsola(),
        ruta_guardado=str(DIRECTORIO_DATOS / "partida.sav"),
        ruta_bitacora=str(DIRECTORIO_DATOS / "partida.log"),
        leer_puntajes=lambda: repositorio_puntajes.cargar().ordenados_por_tiempo(),
    ).ejecutar()
    print("\n" + servicio.reporte_final())


if __name__ == "__main__":
    main()