"""Pruebas de la estructura pura de la línea de tiempo: acciones, instantes, checkpoints, truncamiento y ajustes.
Se ejecuta con:  py -m unittest tests.modelo.test_linea_tiempo -v
"""
import random
import unittest


def _nueva(k=100):
    # Importa dentro de la función para que cada caso falle por separado mientras el módulo no exista
    from cripta.modelo.linea_tiempo import LineaTiempo
    return LineaTiempo(k)


def _con_acciones(cantidad, k=100, paso=10):
    # Registra acciones con instante paso por número de acción y devuelve la línea
    linea = _nueva(k)
    for numero in range(1, cantidad + 1):
        linea.registrar_accion(("mover", numero), numero * paso)
    return linea


def _con_checkpoints(cantidad, k):
    # Registra acciones y crea un checkpoint cada vez que la línea lo pide
    linea = _nueva(k)
    for numero in range(1, cantidad + 1):
        linea.registrar_accion(("mover", numero), numero * 10)
        if linea.debe_crear_checkpoint():
            linea.registrar_checkpoint(("estado", numero))
    return linea


def _numeros_de_checkpoints(linea, cantidad_maxima):
    # Lista los números de acción de los checkpoints consultando de la última acción hacia atrás
    numeros = []
    k = cantidad_maxima
    while k >= 0:
        punto = linea.buscar_checkpoint(k)
        if punto is None:
            break
        numeros.append(punto.numero_acciones)
        k = punto.numero_acciones - 1
    return numeros


class TestRegistroDeAcciones(unittest.TestCase):
    def test_las_acciones_se_numeran_desde_1(self):  # FR-LIN-003
        linea = _nueva()
        self.assertEqual(linea.registrar_accion(("mover", "N"), 10), 1)
        self.assertEqual(linea.registrar_accion(("mover", "E"), 20), 2)
        self.assertEqual(linea.registrar_accion(("esperar",), 30), 3)
        self.assertEqual(len(linea), 3)

    def test_la_accion_k_devuelve_los_datos_registrados_en_orden(self):  # FR-LIN-003
        linea = _con_acciones(5)
        for numero in range(1, 6):
            self.assertEqual(linea.accion(numero), ("mover", numero))

    def test_k_cero_se_rechaza(self):  # FR-LIN-003, FR-LIN-023
        linea = _con_acciones(3)
        with self.assertRaises(IndexError):
            linea.accion(0)

    def test_k_negativo_se_rechaza(self):  # FR-LIN-003, FR-LIN-023
        linea = _con_acciones(3)
        with self.assertRaises(IndexError):
            linea.accion(-1)

    def test_k_mayor_que_las_acciones_vigentes_se_rechaza(self):  # FR-LIN-003, FR-LIN-023
        linea = _con_acciones(3)
        with self.assertRaises(IndexError):
            linea.accion(4)
        with self.assertRaises(IndexError):
            linea.accion(99)

    def test_linea_vacia_rechaza_cualquier_k(self):  # FR-LIN-003
        linea = _nueva()
        with self.assertRaises(IndexError):
            linea.accion(1)

    def test_cada_accion_conserva_su_instante(self):  # FR-LIN-006
        linea = _con_acciones(4, paso=7)
        for numero in range(1, 5):
            self.assertEqual(linea.tiempo_de(numero), numero * 7)

    def test_tiempo_de_rechaza_numeros_sin_accion(self):  # FR-LIN-003
        linea = _con_acciones(2)
        with self.assertRaises(IndexError):
            linea.tiempo_de(0)
        with self.assertRaises(IndexError):
            linea.tiempo_de(3)

    def test_instantes_iguales_son_validos(self):  # FR-LIN-006
        linea = _nueva()
        linea.registrar_accion(("a",), 50)
        linea.registrar_accion(("b",), 50)
        self.assertEqual(len(linea), 2)

    def test_un_instante_menor_que_el_ultimo_se_rechaza_sin_efecto(self):  # FR-LIN-006
        linea = _con_acciones(3)
        with self.assertRaises(ValueError):
            linea.registrar_accion(("tarde",), 5)
        self.assertEqual(len(linea), 3)
        self.assertEqual(linea.tiempo_de(3), 30)


class TestFrecuenciaK(unittest.TestCase):
    def test_k_valido_se_acepta(self):  # FR-LIN-013
        self.assertEqual(_nueva(1).frecuencia, 1)
        self.assertEqual(_nueva(250).frecuencia, 250)

    def test_k_cero_se_rechaza(self):  # FR-LIN-013
        with self.assertRaises(ValueError):
            _nueva(0)

    def test_k_negativo_se_rechaza(self):  # FR-LIN-013
        with self.assertRaises(ValueError):
            _nueva(-5)

    def test_k_no_entero_se_rechaza(self):  # FR-LIN-013
        with self.assertRaises(ValueError):
            _nueva("abc")
        with self.assertRaises(ValueError):
            _nueva(2.5)


class TestBusquedaPorInstante(unittest.TestCase):
    def test_linea_vacia_cuenta_cero(self):  # FR-LIN-001, FR-LIN-006
        linea = _nueva()
        self.assertEqual(linea.contar_hasta_instante(100, True), 0)
        self.assertEqual(linea.contar_hasta_instante(100, False), 0)

    def test_instante_anterior_a_la_primera_accion(self):  # FR-LIN-001
        linea = _con_acciones(5)
        self.assertEqual(linea.contar_hasta_instante(9, True), 0)
        self.assertEqual(linea.contar_hasta_instante(9, False), 0)

    def test_instante_entre_acciones(self):  # FR-LIN-001
        linea = _con_acciones(5)
        self.assertEqual(linea.contar_hasta_instante(25, True), 2)
        self.assertEqual(linea.contar_hasta_instante(25, False), 2)

    def test_instante_igual_al_de_una_accion_distingue_inclusivo_y_exclusivo(self):  # FR-LIN-001, FR-LIN-002
        linea = _con_acciones(5)
        self.assertEqual(linea.contar_hasta_instante(30, True), 3)
        self.assertEqual(linea.contar_hasta_instante(30, False), 2)

    def test_instantes_repetidos_se_cuentan_todos(self):  # FR-LIN-001, FR-LIN-002
        linea = _nueva()
        for tiempo in (10, 20, 20, 20, 30):
            linea.registrar_accion(("a",), tiempo)
        self.assertEqual(linea.contar_hasta_instante(20, True), 4)
        self.assertEqual(linea.contar_hasta_instante(20, False), 1)

    def test_instante_posterior_a_la_ultima_accion_cuenta_todas(self):  # FR-LIN-006
        linea = _con_acciones(5)
        self.assertEqual(linea.contar_hasta_instante(10 ** 6, True), 5)
        self.assertEqual(linea.contar_hasta_instante(10 ** 6, False), 5)

    def test_coincide_con_un_conteo_lineal_de_referencia(self):  # FR-LIN-001, FR-LIN-002, FR-LIN-006
        azar = random.Random(20260116)
        linea = _nueva()
        tiempos = []
        tiempo = 0
        for _ in range(300):
            tiempo += azar.randint(0, 3)
            tiempos.append(tiempo)
            linea.registrar_accion(("a",), tiempo)
        for consulta in range(-1, tiempo + 3):
            inclusivo = 0
            exclusivo = 0
            for existente in tiempos:
                if existente <= consulta:
                    inclusivo += 1
                if existente < consulta:
                    exclusivo += 1
            self.assertEqual(linea.contar_hasta_instante(consulta, True), inclusivo)
            self.assertEqual(linea.contar_hasta_instante(consulta, False), exclusivo)

    def test_la_busqueda_es_binaria(self):  # FR-LIN-006, FR-LIN-015
        linea = _con_acciones(1024)
        linea.contar_hasta_instante(5000, True)
        self.assertLessEqual(linea.inspecciones_ultima_busqueda, 12)
        self.assertGreater(linea.inspecciones_ultima_busqueda, 0)


class TestCheckpoints(unittest.TestCase):
    def test_no_se_pide_checkpoint_antes_del_primer_multiplo(self):  # FR-LIN-013
        linea = _nueva(5)
        self.assertFalse(linea.debe_crear_checkpoint())
        for numero in range(1, 5):
            linea.registrar_accion(("a",), numero)
            self.assertFalse(linea.debe_crear_checkpoint())

    def test_se_pide_checkpoint_en_cada_multiplo_de_k(self):  # FR-LIN-013
        linea = _nueva(5)
        for numero in range(1, 6):
            linea.registrar_accion(("a",), numero)
        self.assertTrue(linea.debe_crear_checkpoint())

    def test_con_k_1_se_pide_checkpoint_tras_cada_accion(self):  # FR-LIN-013
        linea = _nueva(1)
        for numero in range(1, 6):
            linea.registrar_accion(("a",), numero)
            self.assertTrue(linea.debe_crear_checkpoint())
            linea.registrar_checkpoint(("estado", numero))
            self.assertFalse(linea.debe_crear_checkpoint())
        self.assertEqual(linea.cantidad_checkpoints(), 5)

    def test_con_k_mayor_que_las_acciones_nunca_se_pide(self):  # FR-LIN-013
        linea = _nueva(1000)
        for numero in range(1, 51):
            linea.registrar_accion(("a",), numero)
            self.assertFalse(linea.debe_crear_checkpoint())
        self.assertEqual(linea.cantidad_checkpoints(), 0)

    def test_no_hay_mas_de_un_checkpoint_por_cada_k_acciones(self):  # FR-LIN-013
        linea = _con_checkpoints(25, 5)
        self.assertEqual(linea.cantidad_checkpoints(), 5)

    def test_registrar_fuera_de_un_multiplo_se_rechaza(self):  # FR-LIN-013
        linea = _con_acciones(3, k=5)
        with self.assertRaises(ValueError):
            linea.registrar_checkpoint(("estado",))
        self.assertEqual(linea.cantidad_checkpoints(), 0)

    def test_registrar_sin_acciones_se_rechaza(self):  # FR-LIN-013
        linea = _nueva(5)
        with self.assertRaises(ValueError):
            linea.registrar_checkpoint(("estado",))

    def test_no_se_admite_un_segundo_checkpoint_en_la_misma_posicion(self):  # FR-LIN-013
        linea = _con_checkpoints(5, 5)
        with self.assertRaises(ValueError):
            linea.registrar_checkpoint(("otro",))
        self.assertEqual(linea.cantidad_checkpoints(), 1)

    def test_buscar_sin_checkpoints_devuelve_none(self):  # FR-LIN-015
        linea = _con_acciones(4, k=100)
        self.assertIsNone(linea.buscar_checkpoint(4))

    def test_buscar_antes_del_primer_checkpoint_devuelve_none(self):  # FR-LIN-015
        linea = _con_checkpoints(10, 5)
        self.assertIsNone(linea.buscar_checkpoint(4))

    def test_buscar_devuelve_el_checkpoint_mas_cercano_anterior_o_igual(self):  # FR-LIN-015
        linea = _con_checkpoints(20, 5)
        self.assertEqual(linea.buscar_checkpoint(5).numero_acciones, 5)
        self.assertEqual(linea.buscar_checkpoint(9).numero_acciones, 5)
        self.assertEqual(linea.buscar_checkpoint(10).numero_acciones, 10)
        self.assertEqual(linea.buscar_checkpoint(20).numero_acciones, 20)

    def test_el_checkpoint_conserva_el_estado_entregado(self):  # FR-LIN-016, FR-LIN-017
        linea = _nueva(2)
        linea.registrar_accion(("a",), 1)
        linea.registrar_accion(("b",), 2)
        estado = {"rng": (3, (1, 2, 3), None), "sala": 7}
        linea.registrar_checkpoint(estado)
        self.assertIs(linea.buscar_checkpoint(2).estado, estado)

    def test_ninguna_consulta_re_simula_mas_de_k_acciones(self):  # FR-LIN-015
        k = 7
        linea = _con_checkpoints(100, k)
        for numero in range(1, 101):
            punto = linea.buscar_checkpoint(numero)
            base = 0 if punto is None else punto.numero_acciones
            self.assertLessEqual(numero - base, k)

    def test_la_busqueda_de_checkpoint_es_binaria(self):  # FR-LIN-015
        linea = _con_checkpoints(1024, 1)
        linea.buscar_checkpoint(700)
        self.assertLessEqual(linea.inspecciones_ultima_busqueda, 12)
        self.assertGreater(linea.inspecciones_ultima_busqueda, 0)


class TestTruncamiento(unittest.TestCase):
    def test_truncar_deja_solo_las_acciones_vigentes(self):  # FR-LIN-007
        linea = _con_acciones(5)
        linea.truncar(3)
        self.assertEqual(len(linea), 3)
        self.assertEqual(linea.accion(3), ("mover", 3))

    def test_las_acciones_revertidas_ya_no_se_consultan(self):  # FR-LIN-007
        linea = _con_acciones(5)
        linea.truncar(3)
        with self.assertRaises(IndexError):
            linea.accion(4)
        with self.assertRaises(IndexError):
            linea.tiempo_de(5)

    def test_la_numeracion_se_reutiliza_desde_la_ultima_vigente(self):  # FR-LIN-003, FR-LIN-007, FR-LIN-020
        linea = _con_acciones(5)
        linea.truncar(3)
        self.assertEqual(linea.registrar_accion(("nueva",), 35), 4)
        self.assertEqual(linea.accion(4), ("nueva",))

    def test_las_busquedas_por_instante_excluyen_lo_revertido(self):  # FR-LIN-006, FR-LIN-007
        linea = _con_acciones(5)
        linea.truncar(3)
        self.assertEqual(linea.contar_hasta_instante(10 ** 6, True), 3)
        self.assertEqual(linea.contar_hasta_instante(40, True), 3)

    def test_tras_truncar_un_instante_menor_que_lo_revertido_es_valido(self):  # FR-LIN-006, FR-LIN-007
        linea = _con_acciones(5)
        linea.truncar(2)
        linea.registrar_accion(("nueva",), 25)
        self.assertEqual(linea.tiempo_de(3), 25)

    def test_tras_truncar_no_se_admite_un_instante_menor_que_la_ultima_vigente(self):  # FR-LIN-006
        linea = _con_acciones(5)
        linea.truncar(3)
        with self.assertRaises(ValueError):
            linea.registrar_accion(("nueva",), 29)

    def test_truncar_a_la_longitud_actual_no_cambia_nada(self):  # FR-LIN-007
        linea = _con_checkpoints(10, 5)
        linea.truncar(10)
        self.assertEqual(len(linea), 10)
        self.assertEqual(linea.cantidad_checkpoints(), 2)

    def test_truncar_a_cero_vacia_la_linea(self):  # FR-LIN-007
        linea = _con_checkpoints(10, 5)
        linea.truncar(0)
        self.assertEqual(len(linea), 0)
        self.assertEqual(linea.cantidad_checkpoints(), 0)
        self.assertEqual(linea.registrar_accion(("a",), 1), 1)

    def test_truncar_mas_alla_de_la_longitud_se_rechaza_sin_efecto(self):  # FR-LIN-007
        linea = _con_acciones(3)
        with self.assertRaises(ValueError):
            linea.truncar(4)
        self.assertEqual(len(linea), 3)

    def test_truncar_a_un_negativo_se_rechaza_sin_efecto(self):  # FR-LIN-007
        linea = _con_acciones(3)
        with self.assertRaises(ValueError):
            linea.truncar(-1)
        self.assertEqual(len(linea), 3)

    def test_se_quitan_los_checkpoints_posteriores_al_limite(self):  # FR-LIN-007
        linea = _con_checkpoints(6, 2)
        linea.truncar(3)
        self.assertEqual(linea.cantidad_checkpoints(), 1)
        self.assertEqual(linea.buscar_checkpoint(6).numero_acciones, 2)

    def test_el_checkpoint_del_borde_se_conserva(self):  # FR-LIN-007
        linea = _con_checkpoints(6, 2)
        linea.truncar(4)
        self.assertEqual(linea.cantidad_checkpoints(), 2)
        self.assertEqual(linea.buscar_checkpoint(6).numero_acciones, 4)
        self.assertEqual(_numeros_de_checkpoints(linea, 6), [4, 2])

    def test_tras_truncar_se_vuelve_a_pedir_el_checkpoint_descartado(self):  # FR-LIN-007, FR-LIN-013
        linea = _con_checkpoints(6, 2)
        linea.truncar(3)
        linea.registrar_accion(("nueva",), 35)
        self.assertTrue(linea.debe_crear_checkpoint())
        linea.registrar_checkpoint(("estado nuevo",))
        self.assertEqual(linea.buscar_checkpoint(4).estado, ("estado nuevo",))

    def test_truncamientos_sucesivos(self):  # FR-LIN-007
        linea = _con_checkpoints(10, 2)
        linea.truncar(7)
        linea.truncar(5)
        self.assertEqual(len(linea), 5)
        self.assertEqual(_numeros_de_checkpoints(linea, 5), [4, 2])


class TestAjustesDeInventario(unittest.TestCase):
    def test_el_ajuste_no_recibe_numero_de_accion(self):  # FR-LIN-005, FR-LIN-007
        linea = _con_acciones(3)
        linea.registrar_ajuste(["pergamino-1"])
        self.assertEqual(len(linea), 3)
        with self.assertRaises(IndexError):
            linea.accion(4)
        self.assertEqual(linea.registrar_accion(("a",), 40), 4)

    def test_el_ajuste_no_cuenta_para_k(self):  # FR-LIN-005, FR-LIN-013
        linea = _nueva(2)
        linea.registrar_accion(("a",), 1)
        linea.registrar_ajuste(["pergamino-1"])
        self.assertFalse(linea.debe_crear_checkpoint())
        linea.registrar_accion(("b",), 2)
        self.assertTrue(linea.debe_crear_checkpoint())

    def test_el_ajuste_queda_en_la_posicion_donde_se_anexo(self):  # FR-LIN-005
        linea = _con_acciones(3)
        linea.registrar_ajuste(["pergamino-1"])
        self.assertEqual(linea.ajustes_en(3), ["pergamino-1"])
        self.assertEqual(linea.ajustes_en(2), [])
        self.assertEqual(linea.ajustes_en(0), [])

    def test_el_ajuste_conserva_las_instancias_afectadas_en_orden(self):  # FR-LIN-005
        linea = _con_acciones(2)
        linea.registrar_ajuste(["consumido", "recogido"])
        self.assertEqual(linea.ajustes_en(2), ["consumido", "recogido"])

    def test_un_ajuste_puede_anexarse_antes_de_toda_accion(self):  # FR-LIN-005
        linea = _nueva()
        linea.registrar_ajuste(["pergamino-1"])
        self.assertEqual(linea.ajustes_en(0), ["pergamino-1"])

    def test_el_ajuste_sigue_antes_de_las_acciones_posteriores(self):  # FR-LIN-005, FR-LIN-007
        linea = _con_acciones(3)
        linea.registrar_ajuste(["pergamino-1"])
        linea.registrar_accion(("a",), 40)
        self.assertEqual(linea.ajustes_en(3), ["pergamino-1"])
        self.assertEqual(linea.ajustes_en(4), [])

    def test_la_consulta_de_ajustes_devuelve_una_copia(self):  # FR-LIN-005
        linea = _con_acciones(2)
        linea.registrar_ajuste(["pergamino-1"])
        linea.ajustes_en(2).append("intruso")
        self.assertEqual(linea.ajustes_en(2), ["pergamino-1"])

    def test_el_pergamino_trunca_y_luego_anexa_su_ajuste(self):  # FR-LIN-005, FR-LIN-007
        linea = _con_acciones(5)
        linea.truncar(3)
        linea.registrar_ajuste(["pergamino-1"])
        self.assertEqual(len(linea), 3)
        self.assertEqual(linea.ajustes_en(3), ["pergamino-1"])
        self.assertEqual(linea.registrar_accion(("a",), 35), 4)

    def test_truncar_por_detras_acumula_los_ajustes_en_el_nuevo_final(self):  # FR-LIN-007
        linea = _con_acciones(5)
        linea.truncar(3)
        linea.registrar_ajuste(["p1"])
        linea.registrar_accion(("a",), 35)
        linea.registrar_accion(("b",), 36)
        linea.registrar_ajuste(["p2"])
        linea.truncar(1)
        self.assertEqual(linea.ajustes_en(1), ["p1", "p2"])
        self.assertEqual(linea.ajustes_en(3), [])
        self.assertEqual(linea.ajustes_en(5), [])

    def test_los_ajustes_ya_presentes_en_el_nuevo_final_van_primero(self):  # FR-LIN-007
        linea = _con_acciones(4)
        linea.truncar(2)
        linea.registrar_ajuste(["p1"])
        linea.registrar_accion(("a",), 25)
        linea.registrar_ajuste(["p2"])
        linea.truncar(2)
        self.assertEqual(linea.ajustes_en(2), ["p1", "p2"])
        self.assertEqual(linea.ajustes_en(3), [])

    def test_truncar_en_la_posicion_del_ajuste_lo_conserva(self):  # FR-LIN-007
        linea = _con_acciones(5)
        linea.truncar(3)
        linea.registrar_ajuste(["p1"])
        linea.registrar_accion(("a",), 35)
        linea.truncar(3)
        self.assertEqual(linea.ajustes_en(3), ["p1"])

    def test_truncar_por_delante_de_un_ajuste_no_lo_toca(self):  # FR-LIN-007
        linea = _con_acciones(5)
        linea.truncar(2)
        linea.registrar_ajuste(["p1"])
        linea.registrar_accion(("a",), 25)
        linea.registrar_accion(("b",), 26)
        linea.truncar(3)
        self.assertEqual(linea.ajustes_en(2), ["p1"])
        self.assertEqual(linea.ajustes_en(3), [])

    def test_truncamientos_sucesivos_acumulan_todos_los_ajustes(self):  # FR-LIN-007
        linea = _con_acciones(6)
        linea.truncar(5)
        linea.registrar_ajuste(["p1"])
        linea.registrar_accion(("a",), 55)
        linea.truncar(4)
        linea.registrar_ajuste(["p2"])
        linea.registrar_accion(("b",), 45)
        linea.truncar(3)
        linea.registrar_ajuste(["p3"])
        self.assertEqual(linea.ajustes_en(3), ["p1", "p2", "p3"])
        linea.truncar(1)
        self.assertEqual(linea.ajustes_en(1), ["p1", "p2", "p3"])
        self.assertEqual(linea.ajustes_en(3), [])
        self.assertEqual(linea.ajustes_en(4), [])
        self.assertEqual(linea.ajustes_en(5), [])

    def test_truncar_a_cero_acumula_en_la_posicion_cero(self):  # FR-LIN-007
        linea = _con_acciones(3)
        linea.registrar_ajuste(["p1"])
        linea.truncar(0)
        self.assertEqual(linea.ajustes_en(0), ["p1"])

    def test_los_ajustes_no_alteran_los_checkpoints(self):  # FR-LIN-005, FR-LIN-007
        linea = _con_checkpoints(4, 2)
        linea.registrar_ajuste(["p1"])
        linea.truncar(3)
        self.assertEqual(linea.cantidad_checkpoints(), 1)
        self.assertEqual(linea.ajustes_en(3), ["p1"])

    def test_el_cursor_del_inventario_no_forma_parte_de_la_linea(self):  # FR-LIN-005
        linea = _con_acciones(2)
        linea.registrar_ajuste(["pergamino-1"])
        self.assertFalse(hasattr(linea, "cursor"))
        self.assertFalse(hasattr(linea, "cursor_inventario"))
        self.assertEqual(linea.ajustes_en(2), ["pergamino-1"])


if __name__ == "__main__":
    unittest.main()
