"""Pruebas del formato binario de guardado (§4.10): GuardadoBinario y la comparación con JSON.

Los tests de tests/modelo/test_guardado_*.py revisan que una partida real, guardada y cargada,
siga igual. Estos revisan el formato del archivo: que el índice quede ordenado, que se pueda
cargar una sola sala, que los valores que no caben den error y que un archivo dañado se rechace.
Usan el mismo estado de prueba que el bench.

Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.infraestructura.test_guardado_binario -v
"""
import struct
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from cripta.bench.cargas_bench import estado_sintetico
from cripta.excepciones import CriptaFormatoIncompatibleError
from cripta.infraestructura.guardado_binario import GuardadoBinario, cargar_json, guardar_json

N_SALAS = 50


class TestGuardadoBinario(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.carpeta = Path(carpeta.name)
        self.ruta = self.carpeta / "partida.sav"
        self.guardado = GuardadoBinario()
        self.estado = estado_sintetico(N_SALAS)   # las salas vienen desordenadas a propósito
        self.guardado.guardar(self.ruta, self.estado)

    def sala_original(self, sala_id):
        for sala in self.estado.salas:
            if sala.sala_id == sala_id:
                return sala
        return None

    def test_cargar_da_el_mismo_estado(self):
        cargado = self.guardado.cargar(self.ruta)
        # Todo lo que no es salas, igual
        self.assertEqual(replace(cargado, salas=()), replace(self.estado, salas=()))
        # Las salas: las mismas, cada una igual a la original
        self.assertEqual(len(cargado.salas), N_SALAS)
        for sala in cargado.salas:
            self.assertEqual(sala, self.sala_original(sala.sala_id))

    def test_las_salas_vuelven_ordenadas_por_id(self):
        # Se guardaron desordenadas; el índice las deja en orden (§4.9), y cargar() respeta ese orden
        cargado = self.guardado.cargar(self.ruta)
        self.assertEqual([s.sala_id for s in cargado.salas], list(range(1, N_SALAS + 1)))

    def test_cargar_una_sola_sala(self):
        for sala_id in (1, 25, N_SALAS):            # la primera, una del medio y la última del índice
            self.assertEqual(self.guardado.cargar_sala(self.ruta, sala_id), self.sala_original(sala_id))
        self.assertIsNone(self.guardado.cargar_sala(self.ruta, N_SALAS + 1))

    def test_leer_encabezado_sin_cargar_salas(self):
        e = self.estado
        self.assertEqual(self.guardado.leer_encabezado(self.ruta),
                         (e.cripta_id, e.cripta_version, e.catalogo_version, e.semilla, N_SALAS))

    def test_valores_que_no_caben_son_error_y_no_tocan_el_archivo_anterior(self):
        vida_enorme = replace(self.estado, jugador=replace(self.estado.jugador, vida=2**40))
        with self.assertRaises(ValueError):
            self.guardado.guardar(self.ruta, vida_enorme)
        with self.assertRaises(ValueError):
            self.guardado.guardar(self.ruta, replace(self.estado, mensajes=("x" * 70000,)))
        # El guardado que ya estaba sigue sano
        self.assertEqual(self.guardado.leer_encabezado(self.ruta)[4], N_SALAS)

    def danar(self, inicio, nuevos_bytes):
        # Reemplaza bytes del archivo a partir de `inicio`
        crudo = self.ruta.read_bytes()
        self.ruta.write_bytes(crudo[:inicio] + nuevos_bytes + crudo[inicio + len(nuevos_bytes):])

    def test_n_salas_absurdo_es_error(self):
        self.danar(8, struct.pack("<I", 10_000_000))     # bytes 8-11 del encabezado: n_salas
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar_sala(self.ruta, 25)

    def test_archivo_cortado_es_error(self):
        crudo = self.ruta.read_bytes()
        self.ruta.write_bytes(crudo[: len(crudo) // 2])
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)

    def test_archivo_que_no_es_de_cripta_o_de_otra_version_es_error(self):
        self.danar(0, b"XXXX")                           # bytes 0-3: el magic "CRPT"
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)
        self.guardado.guardar(self.ruta, self.estado)
        self.danar(4, struct.pack("<H", 99))             # bytes 4-5: versión del formato
        with self.assertRaises(CriptaFormatoIncompatibleError):
            self.guardado.cargar(self.ruta)

    def test_json_reconstruye_lo_mismo(self):
        # La comparación de tiempos del bench solo es justa si cargar_json arma el mismo estado
        ruta_json = self.carpeta / "partida.json"
        guardar_json(ruta_json, self.estado)
        self.assertEqual(cargar_json(ruta_json), self.estado)


if __name__ == "__main__":
    unittest.main()