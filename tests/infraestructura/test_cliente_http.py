'''Pruebas de ClienteHttp ante HTTP 429, errores de red y presupuesto (3.1 y 5.1), sin red real.
Se reemplazan requests.get y time.sleep: la espera real no se ejecuta, solo se comprueba cuánto se pidió.
Ejecutar: python -m unittest tests.infraestructura.test_cliente_http
'''
import unittest
from unittest.mock import patch

import requests

from cripta.constantes import MAX_REINTENTOS_429
from cripta.excepciones import CriptaApiError, CriptaLimiteError
from cripta.infraestructura.cliente_http import ClienteHttp
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes

CRIPTAS_JSON = {"criptas": [{"id": "cripta-01", "nombre": "Osario menor", "salas": 6, "dificultad": 1}]}


class RespuestaFalsa:
    # Imita lo mínimo de requests.Response que usa el cliente.
    def __init__(self, codigo: int, cuerpo=None):
        self.status_code = codigo
        self._cuerpo = cuerpo
        self.text = "" if cuerpo is None else str(cuerpo)

    def json(self):
        if self._cuerpo is None:
            raise ValueError("sin cuerpo")
        return self._cuerpo


def limite(segundos=3):
    return RespuestaFalsa(429, {"error": "demasiadas solicitudes", "reintentar_en": segundos})


class TestCliente429(unittest.TestCase):
    def setUp(self):
        self.contador = ContadorSolicitudes()
        self.cliente = ClienteHttp(self.contador)

    def _listar(self, respuestas):
        with patch("cripta.infraestructura.cliente_http.requests.get", side_effect=respuestas) as get, \
                patch("cripta.infraestructura.cliente_http.time.sleep") as dormir:
            return self.cliente.listar_criptas(), get, dormir

    def test_un_429_espera_lo_indicado_y_reintenta(self):
        criptas, get, dormir = self._listar([limite(3), RespuestaFalsa(200, CRIPTAS_JSON)])
        self.assertEqual(criptas[0].id, "cripta-01")
        dormir.assert_called_once_with(3)
        self.assertEqual(get.call_count, 2)

    def test_el_reintento_cuenta_en_el_presupuesto(self):
        self._listar([limite(), RespuestaFalsa(200, CRIPTAS_JSON)])
        self.assertEqual(self.contador.realizadas, 2)

    def test_el_mismo_client_id_en_todos_los_reintentos(self):
        _, get, _ = self._listar([limite(), limite(), RespuestaFalsa(200, CRIPTAS_JSON)])
        ids = {llamada.kwargs["headers"]["X-Cripta-Client-Id"] for llamada in get.call_args_list}
        self.assertEqual(ids, {self.cliente.client_id})

    def test_429_sin_reintentar_en_espera_un_segundo(self):
        _, _, dormir = self._listar([RespuestaFalsa(429, {"error": "x"}), RespuestaFalsa(200, CRIPTAS_JSON)])
        dormir.assert_called_once_with(1)

    def test_429_persistente_termina_con_error_con_contexto(self):
        with self.assertRaises(CriptaApiError) as contexto:
            self._listar([limite() for _ in range(MAX_REINTENTOS_429 + 1)])
        self.assertEqual(contexto.exception.codigo, 429)
        self.assertIn("listar criptas", str(contexto.exception))
        self.assertEqual(self.contador.realizadas, MAX_REINTENTOS_429 + 1)

    def test_429_con_presupuesto_agotado_lanza_limite(self):
        self.contador.fijar_presupuesto_maximo(2)
        with self.assertRaises(CriptaLimiteError):
            self._listar([limite() for _ in range(10)])
        self.assertEqual(self.contador.realizadas, 2)     # nunca se supera el presupuesto

    def test_error_de_red_se_reporta_con_la_operacion(self):
        with self.assertRaises(CriptaApiError) as contexto:
            self._listar(requests.ConnectionError("sin red"))
        self.assertIsNone(contexto.exception.codigo)
        self.assertIn("listar criptas", str(contexto.exception))

    def test_otro_codigo_no_reintenta(self):
        with self.assertRaises(CriptaApiError) as contexto:
            self._listar([RespuestaFalsa(500, {"error": "falla"})])
        self.assertEqual(contexto.exception.codigo, 500)
        self.assertEqual(self.contador.realizadas, 1)


if __name__ == "__main__":
    unittest.main()