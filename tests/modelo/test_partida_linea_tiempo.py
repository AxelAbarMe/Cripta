"""Pruebas de la consulta histórica de Partida: consultar_instante(t), consultar_accion(k) y linea_tiempo().
Cada estado histórico se compara con una fotografía tomada en vivo en el mismo punto de la partida.
Se ejecuta con:  py -m unittest tests.modelo.test_partida_linea_tiempo -v
"""
import unittest

from cripta.modelo.accion import Accion as A
from cripta.modelo.cripta_mapa import CriptaMapa
from cripta.modelo.inventario import ObjetoInventario
from cripta.modelo.partida import Partida
from cripta.servicios.servicio_catalogo import ServicioCatalogo
from cripta.servicios.servicio_precarga import ServicioPrecarga
from tests.cliente_falso import ClienteFalso
from tests.cripta_cazadores import ficha_cazador, grafo, id_ficha

FICHA_PERGAMINO = {"id": "itm_pergamino", "nombre": "Pergamino de retroceso", "clase": "pergamino_retroceso",
                   "peso": 1, "valor": 40}
FICHA_ANTORCHA = {"id": "itm_antorcha", "nombre": "Antorcha", "clase": "antorcha", "peso": 1, "valor": 5,
                  "duracion": 2000}


def _armar(cazadores=(), velocidad_cazador=100, velocidad_jugador=100, pergaminos=0, objetos_sala1=(),
           checkpoint_cada=None, semilla=3, puerta_cerrada=False):
    # Cripta sintética 1-2-3 en fila con costo 100 por salida, cazadores sin rango como lista (sala, instancia, None)
    salidas = grafo([(1, "E", 2, 100), (2, "E", 3, 100)])
    salas = [{"id": i, "nombre": f"Sala {i}", "salidas": s} for i, s in salidas.items()]
    contenido = [{"sala": i, "enemigos": [], "objetos": [], "trampas": []} for i in salidas]
    fichas = [dict(FICHA_PERGAMINO), dict(FICHA_ANTORCHA)]
    if puerta_cerrada:
        salidas[1]["E"].update(cerrada=True, llave="itm_llave")
        fichas.append({"id": "itm_llave", "nombre": "Llave", "clase": "llave", "peso": 1, "valor": 0})
    for sala, instancia, rango in cazadores:
        for entrada in contenido:
            if entrada["sala"] == sala:
                entrada["enemigos"].append({"instancia": instancia, "tipo": id_ficha(rango)})
        if id_ficha(rango) not in [f["id"] for f in fichas]:
            fichas.append(ficha_cazador(rango, velocidad_cazador))
    contenido[0]["objetos"].extend(objetos_sala1)
    general = {"id": "c1", "version": "v1", "salas_total": len(salas), "paginas": 1, "salas_por_pagina": 50,
               "sala_inicial": 1, "sala_salida": 3, "llave_salida": "itm_llave",
               "presupuesto_solicitudes": 9, "inventario_max": 10,
               "jugador": {"vida_max": 100000, "ataque": 6, "defensa": 2, "velocidad": velocidad_jugador}}
    cliente = ClienteFalso(fichas, contenido, [{"pagina": 1, "total_paginas": 1, "salas": salas}], general)
    datos = cliente.obtener_general("c1")
    mapa, catalogo = CriptaMapa(), ServicioCatalogo(cliente)
    precarga = ServicioPrecarga(cliente, "c1", mapa, servicio_catalogo=catalogo, asincrono=False)
    precarga.cargar_esqueleto(datos.paginas)
    if checkpoint_cada is None:
        partida = Partida(datos, mapa, catalogo, precarga, semilla)
    else:
        partida = Partida(datos, mapa, catalogo, precarga, semilla, checkpoint_cada=checkpoint_cada)
    for numero in range(pergaminos):
        partida._jugador.inventario.recoger(ObjetoInventario(f"p{numero}", catalogo.obtener("itm_pergamino")))
    if puerta_cerrada:
        partida._jugador.inventario.recoger(ObjetoInventario("llave", catalogo.obtener("itm_llave")))
    partida.iniciar()
    return partida


def _hacer(partida, tipo, argumento=None):
    # Ejecuta una acción que debe ser aceptada
    resultado = partida.ejecutar_accion(A(tipo, argumento))
    if not resultado.aceptada:
        raise AssertionError(f"La acción {tipo} fue rechazada: {resultado.motivo_rechazo}")
    return resultado


def _foto_viva(partida):
    # Fotografía del estado vivo con los siete grupos de la consulta histórica
    vista = partida.vista()
    inventario = tuple((o.instancia_id, o.ficha.id) for o in partida._jugador.inventario.objetos_en_orden())
    enemigos = tuple((e.instancia, e.vida, e.vida_max) for e in vista.enemigos)
    return (vista.tiempo, vista.sala_id, vista.vida, vista.vida_max, vista.ataque, vista.defensa, vista.velocidad,
            inventario, vista.efectos_activos, enemigos, partida._conocimiento.proyectar())


def _foto_resumen(resumen):
    # Misma fotografía construida desde la proyección histórica
    inventario = tuple((o.instancia_id, o.ficha_id) for o in resumen.inventario)
    enemigos = tuple((e.instancia, e.vida, e.vida_max) for e in resumen.enemigos)
    return (resumen.tiempo, resumen.sala_id, resumen.vida, resumen.vida_max, resumen.ataque, resumen.defensa,
            resumen.velocidad, inventario, resumen.efectos_activos, enemigos, resumen.mapa_conocido)


def _sin_tiempo(foto):
    # Quita el reloj de la fotografía para comparar instantes sin decisión del jugador
    return foto[1:]


def _observable(partida):
    # Todo lo que una consulta no debe cambiar: estado, reloj, mensajes, historial, línea y azar
    eventos = frozenset((e.tiempo, e.secuencia) for e in partida._reloj.eventos_vigentes())
    linea = partida.linea_tiempo()
    return (partida.vista(), partida.mensajes(), partida.puntaje(), partida.desenlace(), len(partida._historial),
            len(linea), linea.cantidad_checkpoints(), partida._reloj.tiempo_actual,
            partida._reloj.siguiente_secuencia, eventos, partida._azar.getstate(),
            partida._conocimiento.exportar_celdas())


def _con_esperas(cantidad, **opciones):
    # Partida con cazadores veloces en la sala 1 tras una cantidad de esperas, con una fotografía por decisión
    cazadores = [(1, "z1", None), (1, "z2", None)]
    partida = _armar(cazadores=cazadores, velocidad_cazador=200, **opciones)
    fotos = [_foto_viva(partida)]
    for _ in range(cantidad):
        _hacer(partida, "esperar")
        fotos.append(_foto_viva(partida))
    return partida, fotos


class TestInstantesYOrdenDeEventos(unittest.TestCase):
    # Escenario con dos cazadores de velocidad 200 y jugador de velocidad 100 con decisiones en 0, 100 y 200.
    # Los cazadores actúan en 50, 100, 150 y 200 y los de 100 y 200 quedan después de la decisión.

    def setUp(self):
        self.partida, self.fotos = _con_esperas(2)

    def test_el_escenario_tiene_las_decisiones_esperadas(self):  # B-LIN-003
        self.assertEqual([f[0] for f in self.fotos], [0, 100, 200])
        self.assertEqual(self.fotos[0][2], self.fotos[0][3])
        self.assertLess(self.fotos[1][2], self.fotos[0][2])
        self.assertLess(self.fotos[2][2], self.fotos[1][2])

    def test_t_mayor_que_el_reloj_se_rechaza_con_motivo(self):  # B-LIN-001, FR-LIN-006, FR-LIN-023
        for instante in (201, 250, 10 ** 6):
            with self.assertRaises(ValueError) as contexto:
                self.partida.consultar_instante(instante)
            self.assertNotEqual(str(contexto.exception).strip(), "")

    def test_t_mayor_que_el_reloj_no_cambia_nada(self):  # B-LIN-001, FR-LIN-005, FR-LIN-023
        antes = _observable(self.partida)
        with self.assertRaises(ValueError):
            self.partida.consultar_instante(201)
        self.assertEqual(_observable(self.partida), antes)

    def test_t_igual_al_reloj_se_acepta(self):  # B-LIN-001, FR-LIN-006
        resumen = self.partida.consultar_instante(200)
        self.assertEqual(_foto_resumen(resumen), self.fotos[2])

    def test_t_con_decision_muestra_el_estado_justo_antes_de_ella(self):  # B-LIN-003, FR-LIN-002
        # En t=100 hay decision y los eventos de los cazadores en 100 se ejecutan despues de ella
        self.assertEqual(_foto_resumen(self.partida.consultar_instante(100)), self.fotos[1])
        self.assertEqual(_foto_resumen(self.partida.consultar_instante(0)), self.fotos[0])

    def test_un_naive_hasta_t_inclusive_daria_otro_estado_en_100(self):  # B-LIN-003, FR-LIN-002
        # Los ataques de 100 existen pero el estado en 100 no los incluye y el de 150 sí
        en_100 = self.partida.consultar_instante(100)
        en_150 = self.partida.consultar_instante(150)
        self.assertLess(en_150.vida, en_100.vida)

    def test_t_sin_decision_incluye_todos_los_eventos_hasta_t(self):  # B-LIN-003, FR-LIN-001
        # En 150 no hay decision y los dos cazadores actúan en ese instante
        resumen = self.partida.consultar_instante(150)
        self.assertEqual(_sin_tiempo(_foto_resumen(resumen)), _sin_tiempo(self.fotos[2]))
        self.assertEqual(resumen.tiempo, 150)

    def test_instantes_de_un_mismo_tramo_dan_el_mismo_estado(self):  # B-LIN-003, FR-LIN-001
        base = _sin_tiempo(_foto_resumen(self.partida.consultar_instante(150)))
        self.assertEqual(_sin_tiempo(_foto_resumen(self.partida.consultar_instante(199))), base)
        base = _sin_tiempo(_foto_resumen(self.partida.consultar_instante(50)))
        self.assertEqual(_sin_tiempo(_foto_resumen(self.partida.consultar_instante(99))), base)
        self.assertEqual(base, _sin_tiempo(self.fotos[1]))

    def test_dos_eventos_en_el_mismo_t_se_aplican_ambos(self):  # B-LIN-003, FR-LIN-001, FR-LIN-002
        # En 50 actúan los dos cazadores y el daño mínimo de cada ataque es 1
        antes = self.partida.consultar_instante(49)
        en_50 = self.partida.consultar_instante(50)
        self.assertEqual(antes.vida, antes.vida_max)
        self.assertGreaterEqual(antes.vida - en_50.vida, 2)

    def test_el_instante_de_cada_accion_es_el_de_su_decision(self):  # FR-LIN-006
        linea = self.partida.linea_tiempo()
        self.assertEqual(len(linea), 2)
        self.assertEqual(linea.tiempo_de(1), 0)
        self.assertEqual(linea.tiempo_de(2), 100)

    def test_el_resumen_por_accion_coincide_con_el_de_su_instante(self):  # FR-LIN-003, FR-LIN-006
        for k, instante in ((1, 0), (2, 100)):
            por_accion = _foto_resumen(self.partida.consultar_accion(k))
            por_instante = _foto_resumen(self.partida.consultar_instante(instante))
            self.assertEqual(por_accion, por_instante)


class TestPergaminoYNumeracion(unittest.TestCase):
    def _tres_esperas_y_pergamino(self, pergaminos=1):
        partida = _armar(pergaminos=pergaminos)
        fotos = [_foto_viva(partida)]
        for _ in range(3):
            _hacer(partida, "esperar")
            fotos.append(_foto_viva(partida))
        _hacer(partida, "pergamino")
        return partida, fotos

    def test_las_acciones_aceptadas_se_registran_y_las_rechazadas_no(self):  # FR-LIN-003
        partida = _armar()
        _hacer(partida, "esperar")
        resultado = partida.ejecutar_accion(A("mover", "N"))
        self.assertFalse(resultado.aceptada)
        self.assertEqual(len(partida.linea_tiempo()), 1)

    def test_cada_paso_de_un_viaje_cuenta_como_una_accion(self):  # FR-LIN-003, FR-LIN-020
        partida = _armar()
        _hacer(partida, "mover", "E")
        _hacer(partida, "mover", "O")
        self.assertEqual(len(partida.linea_tiempo()), 2)

    def test_el_pergamino_no_se_numera_y_recorta_la_linea(self):  # B-LIN-002, FR-LIN-003, FR-LIN-007
        partida, _ = self._tres_esperas_y_pergamino()
        self.assertEqual(len(partida.linea_tiempo()), 2)

    def test_las_acciones_revertidas_no_se_pueden_consultar(self):  # B-LIN-002, FR-LIN-007
        partida, fotos = self._tres_esperas_y_pergamino()
        with self.assertRaises(IndexError):
            partida.consultar_accion(3)
        self.assertEqual(_foto_resumen(partida.consultar_accion(2)), fotos[1])
        self.assertEqual(_foto_resumen(partida.consultar_accion(1)), fotos[0])

    def test_la_numeracion_continua_desde_la_ultima_accion_vigente(self):  # B-LIN-002, FR-LIN-003, FR-LIN-007
        partida, _ = self._tres_esperas_y_pergamino()
        antes = _foto_viva(partida)
        _hacer(partida, "esperar")
        self.assertEqual(len(partida.linea_tiempo()), 3)
        self.assertEqual(partida.linea_tiempo().tiempo_de(3), 200)
        self.assertEqual(_foto_resumen(partida.consultar_accion(3)), antes)

    def test_un_instante_posterior_al_reloj_restaurado_se_rechaza(self):  # B-LIN-002, FR-LIN-006
        partida, fotos = self._tres_esperas_y_pergamino()
        self.assertEqual(partida.vista().tiempo, 200)
        with self.assertRaises(ValueError):
            partida.consultar_instante(300)
        with self.assertRaises(ValueError):
            partida.consultar_instante(201)

    def test_un_instante_menor_o_igual_se_acepta_sin_acciones_revertidas(self):  # B-LIN-002, FR-LIN-006, FR-LIN-007
        partida, fotos = self._tres_esperas_y_pergamino()
        self.assertEqual(_foto_resumen(partida.consultar_instante(100)), fotos[1])
        self.assertEqual(_foto_resumen(partida.consultar_instante(0)), fotos[0])

    def test_el_reloj_actual_coincide_con_el_estado_vivo_tras_el_pergamino(self):  # B-LIN-002, FR-LIN-005, FR-LIN-007
        partida, _ = self._tres_esperas_y_pergamino()
        vivo = _foto_viva(partida)
        self.assertEqual(_foto_resumen(partida.consultar_instante(200)), vivo)

    def test_el_ajuste_quita_el_pergamino_consumido_desde_su_posicion(self):  # B-LIN-002, FR-LIN-005, FR-LIN-007
        partida, fotos = self._tres_esperas_y_pergamino()
        antes = partida.consultar_accion(2)
        despues = partida.consultar_instante(200)
        self.assertEqual(len(antes.inventario), 1)
        self.assertEqual(len(despues.inventario), 0)
        self.assertNotEqual(_foto_resumen(despues), fotos[2])

    def test_el_ajuste_no_tiene_numero_ni_cuenta_como_accion(self):  # B-LIN-002, FR-LIN-005, FR-LIN-007
        partida, _ = self._tres_esperas_y_pergamino()
        linea = partida.linea_tiempo()
        self.assertGreaterEqual(len(linea.ajustes_en(2)), 1)
        self.assertEqual(linea.ajustes_en(3), [])
        self.assertEqual(len(linea), 2)

    def test_un_pergamino_recogido_en_lo_revertido_sigue_en_el_inventario(self):  # B-LIN-002, FR-LIN-005, FR-LIN-007
        partida = _armar(pergaminos=1, objetos_sala1=("itm_pergamino",))
        fotos = [_foto_viva(partida)]
        _hacer(partida, "esperar")
        fotos.append(_foto_viva(partida))
        _hacer(partida, "recoger", "itm_pergamino")
        _hacer(partida, "pergamino")
        vivo = _foto_viva(partida)
        self.assertEqual(len(partida.linea_tiempo()), 1)
        self.assertGreaterEqual(len(partida.linea_tiempo().ajustes_en(1)), 1)
        self.assertEqual(_foto_resumen(partida.consultar_instante(partida.vista().tiempo)), vivo)
        self.assertEqual(_foto_resumen(partida.consultar_accion(1)), fotos[0])
        with self.assertRaises(IndexError):
            partida.consultar_accion(2)

    def test_tras_el_pergamino_la_siguiente_accion_conserva_el_inventario_vivo(self):  # B-LIN-002, FR-LIN-005
        partida = _armar(pergaminos=1, objetos_sala1=("itm_pergamino",))
        _hacer(partida, "esperar")
        _hacer(partida, "recoger", "itm_pergamino")
        _hacer(partida, "pergamino")
        antes = _foto_viva(partida)
        _hacer(partida, "esperar")
        self.assertEqual(_foto_resumen(partida.consultar_accion(2)), antes)

    def test_dos_pergaminos_seguidos_acumulan_sus_ajustes(self):  # B-LIN-002, FR-LIN-005, FR-LIN-007
        partida, fotos = self._tres_esperas_y_pergamino(pergaminos=2)
        _hacer(partida, "pergamino")
        linea = partida.linea_tiempo()
        self.assertEqual(len(linea), 1)
        self.assertGreaterEqual(len(linea.ajustes_en(1)), 2)
        self.assertEqual(linea.ajustes_en(2), [])
        self.assertEqual(_foto_resumen(partida.consultar_instante(100)), _foto_viva(partida))
        self.assertEqual(_foto_resumen(partida.consultar_accion(1)), fotos[0])
        with self.assertRaises(ValueError):
            partida.consultar_instante(200)

    def test_el_cursor_del_inventario_no_se_refleja_en_el_resumen(self):  # B-LIN-002, FR-LIN-005
        partida = _armar(pergaminos=2)
        _hacer(partida, "esperar")
        antes = _foto_resumen(partida.consultar_instante(100))
        posicion = partida._jugador.inventario.posicion_actual()
        partida.inventario_siguiente()
        self.assertNotEqual(partida._jugador.inventario.posicion_actual(), posicion)
        self.assertEqual(_foto_resumen(partida.consultar_instante(100)), antes)
        resumen = partida.consultar_instante(100)
        for nombre in ("cursor", "objeto_actual", "objeto_actual_indice", "posicion_actual"):
            self.assertFalse(hasattr(resumen, nombre))


class TestConsultaSinEfectos(unittest.TestCase):
    def setUp(self):
        self.partida, self.fotos = _con_esperas(5, checkpoint_cada=2)

    def test_las_consultas_validas_no_cambian_el_estado_ni_el_historial(self):  # B-LIN-004, FR-LIN-005, SC-LIN-002
        antes = _observable(self.partida)
        for instante in (0, 49, 50, 100, 250, 400, 500):
            self.partida.consultar_instante(instante)
        for k in range(1, 6):
            self.partida.consultar_accion(k)
        self.assertEqual(_observable(self.partida), antes)

    def test_las_consultas_rechazadas_no_cambian_nada(self):  # B-LIN-004, FR-LIN-023
        antes = _observable(self.partida)
        with self.assertRaises(ValueError):
            self.partida.consultar_instante(501)
        with self.assertRaises(IndexError):
            self.partida.consultar_accion(0)
        with self.assertRaises(IndexError):
            self.partida.consultar_accion(6)
        self.assertEqual(_observable(self.partida), antes)

    def test_la_consulta_no_agrega_mensajes(self):  # B-LIN-004, FR-LIN-005
        antes = self.partida.mensajes()
        self.partida.consultar_instante(250)
        self.partida.consultar_accion(3)
        self.assertEqual(self.partida.mensajes(), antes)

    def test_la_consulta_no_prepara_salas_ni_precarga(self):  # B-LIN-004, FR-LIN-005
        partida = _armar(checkpoint_cada=1)
        _hacer(partida, "mover", "E")
        _hacer(partida, "mover", "O")
        llamadas = []
        original_preparar = partida._precarga.preparar_sala
        original_precargar = partida._precarga.precargar_desde
        partida._precarga.preparar_sala = lambda sala_id: llamadas.append("preparar") or original_preparar(sala_id)
        partida._precarga.precargar_desde = lambda sala_id: llamadas.append("precargar") or original_precargar(sala_id)
        for k in (1, 2):
            partida.consultar_accion(k)
        for instante in (0, 100, 200):
            partida.consultar_instante(instante)
        self.assertEqual(llamadas, [])

    def test_una_consulta_no_altera_lo_que_pasa_despues(self):  # B-LIN-004, FR-LIN-005, FR-LIN-017
        otra, _ = _con_esperas(5, checkpoint_cada=2)
        for k in range(1, 6):
            self.partida.consultar_accion(k)
            self.partida.consultar_instante(k * 50)
        for _ in range(4):
            _hacer(self.partida, "esperar")
            _hacer(otra, "esperar")
        self.assertEqual(_foto_viva(self.partida), _foto_viva(otra))
        self.assertEqual(self.partida.mensajes(), otra.mensajes())


class TestResumenMinimo(unittest.TestCase):
    def setUp(self):
        self.partida, self.fotos = _con_esperas(3)

    def test_el_resumen_tiene_los_siete_grupos(self):  # SC-LIN-001, FR-LIN-004
        for resumen in (self.partida.consultar_instante(100), self.partida.consultar_accion(2)):
            self.assertIsInstance(resumen.tiempo, int)
            self.assertIsInstance(resumen.sala_id, int)
            for nombre in ("vida", "vida_max", "ataque", "defensa", "velocidad"):
                self.assertIsInstance(getattr(resumen, nombre), int)
            self.assertIsInstance(resumen.inventario, tuple)
            self.assertIsInstance(resumen.efectos_activos, tuple)
            self.assertIsInstance(resumen.enemigos, tuple)
            self.assertIsInstance(resumen.mapa_conocido, tuple)
            self.assertGreaterEqual(len(resumen.mapa_conocido), 1)

    def test_el_resumen_por_accion_trae_el_reloj_de_esa_accion(self):  # FR-LIN-003, FR-LIN-004
        for k in (1, 2, 3):
            self.assertEqual(self.partida.consultar_accion(k).tiempo, self.partida.linea_tiempo().tiempo_de(k))

    def test_los_enemigos_de_la_sala_consultada_traen_su_vida(self):  # FR-LIN-004
        resumen = self.partida.consultar_instante(100)
        self.assertEqual([e.instancia for e in resumen.enemigos], ["z1", "z2"])
        for enemigo in resumen.enemigos:
            self.assertEqual((enemigo.vida, enemigo.vida_max), (1000, 1000))

    def test_el_resumen_es_de_solo_lectura(self):  # FR-LIN-005, SC-LIN-002
        resumen = self.partida.consultar_instante(100)
        with self.assertRaises(AttributeError):
            resumen.vida = 1
        with self.assertRaises(AttributeError):
            resumen.sala_id = 99

    def test_el_resumen_no_cambia_cuando_la_partida_sigue(self):  # FR-LIN-005
        resumen = self.partida.consultar_instante(100)
        foto = _foto_resumen(resumen)
        for _ in range(3):
            _hacer(self.partida, "esperar")
        self.assertEqual(_foto_resumen(resumen), foto)

    def test_cada_consulta_devuelve_el_mismo_estado(self):  # FR-LIN-005
        primero = _foto_resumen(self.partida.consultar_instante(150))
        segundo = _foto_resumen(self.partida.consultar_instante(150))
        self.assertEqual(primero, segundo)


class TestResumenAlRecorrerLaCripta(unittest.TestCase):
    def setUp(self):
        self.partida = _armar(cazadores=[(2, "z1", None)], objetos_sala1=("itm_antorcha",))
        self.fotos = [_foto_viva(self.partida)]
        for tipo, argumento in (("recoger", "itm_antorcha"), ("usar", 0), ("mover", "E"),
                                ("atacar", "z1"), ("atacar", "z1"), ("esperar", None)):
            _hacer(self.partida, tipo, argumento)
            self.fotos.append(_foto_viva(self.partida))

    def test_cada_estado_previo_a_una_accion_coincide_con_el_vivo(self):  # FR-LIN-003, FR-LIN-004
        for k in range(1, 7):
            self.assertEqual(_foto_resumen(self.partida.consultar_accion(k)), self.fotos[k - 1])

    def test_la_sala_y_los_enemigos_son_los_del_momento_consultado(self):  # FR-LIN-004
        antes = self.partida.consultar_accion(3)
        despues = self.partida.consultar_accion(4)
        self.assertEqual((antes.sala_id, len(antes.enemigos)), (1, 0))
        self.assertEqual((despues.sala_id, [e.instancia for e in despues.enemigos]), (2, ["z1"]))

    def test_la_vida_del_enemigo_baja_entre_consultas(self):  # FR-LIN-004
        tras_un_ataque = self.partida.consultar_accion(5).enemigos[0]
        tras_dos = self.partida.consultar_accion(6).enemigos[0]
        self.assertEqual(self.partida.consultar_accion(4).enemigos[0].vida, tras_un_ataque.vida_max)
        self.assertLess(tras_un_ataque.vida, tras_un_ataque.vida_max)
        self.assertLess(tras_dos.vida, tras_un_ataque.vida)

    def test_los_efectos_activos_son_los_del_momento_consultado(self):  # FR-LIN-004
        self.assertEqual(self.partida.consultar_accion(2).efectos_activos, ())
        self.assertIn("Antorcha", self.partida.consultar_accion(3).efectos_activos)

    def test_el_mapa_conocido_es_el_del_momento_y_no_el_real(self):  # FR-LIN-004, FR-LIN-019
        antes = self.partida.consultar_accion(3).mapa_conocido
        despues = self.partida.consultar_accion(4).mapa_conocido
        self.assertNotEqual(antes, despues)
        self.assertEqual(len(antes), 2)
        self.assertEqual(len(despues), 3)


class TestSalasDePuntosPeriodicos(unittest.TestCase):
    def test_omite_salas_con_puertas_iniciales_sincronizadas(self):  # FR-LIN-013, FR-LIN-016
        partida = _armar(checkpoint_cada=1, puerta_cerrada=True)
        _hacer(partida, "esperar")
        guardado = partida.a_estado_guardado("v1")
        self.assertEqual(tuple(s.sala_id for s in guardado.salas), (1, 2, 3))
        self.assertEqual(tuple(s.sala_id for s in guardado.linea.base.estado.salas), (1, 2, 3))
        self.assertEqual(tuple(s.sala_id for s in guardado.linea.checkpoints[0].estado.salas), (1,))
        self.assertFalse(partida._reconstruir(1)._mapa.puerta_transitable(2, "O"))

    def test_conserva_puerta_cambiada_en_el_extremo_no_preparado(self):  # FR-LIN-004, FR-LIN-015
        partida = _armar(checkpoint_cada=1, puerta_cerrada=True)
        _hacer(partida, "abrir", "E")
        punto = partida.linea_tiempo().buscar_checkpoint(1).estado[0]
        self.assertEqual(tuple(s.sala_id for s in punto.salas), (1, 2))
        self.assertFalse(punto.salas[1].contenido_cargado)
        self.assertTrue(partida._reconstruir(1)._mapa.puerta_transitable(2, "O"))
        _hacer(partida, "mover", "E")
        self.assertEqual(_foto_resumen(partida.consultar_accion(2))[1], 1)
        self.assertEqual(_foto_resumen(partida.consultar_instante(partida.vista().tiempo)), _foto_viva(partida))

    def test_conserva_rastro_sin_preparar_la_sala(self):  # FR-LIN-015, FR-LIN-016
        partida = _armar(checkpoint_cada=1)
        partida._mapa.obtener(2).marcar_visita(0)
        _hacer(partida, "esperar")
        reconstruida = partida._reconstruir(1)._mapa.obtener(2)
        self.assertEqual(reconstruida.rastro_ultima_visita, 0)
        self.assertFalse(reconstruida.contenido_cargado)

    def test_conserva_enemigo_activo_y_su_evento_en_sala_no_preparada(self):  # FR-LIN-015, FR-LIN-017
        partida = _armar(cazadores=[(1, "z1", None)], velocidad_cazador=10, checkpoint_cada=1)
        enemigo = partida._mapa.obtener(1).enemigos_activos[0]
        partida._mover_enemigo(enemigo, "E")
        _hacer(partida, "esperar")
        reconstruida = partida._reconstruir(1)
        sala = reconstruida._mapa.obtener(2)
        self.assertFalse(sala.contenido_cargado)
        self.assertEqual([e.instancia_id for e in sala.enemigos_activos], ["z1"])
        self.assertEqual(sala.enemigos_activos[0].evento_pendiente.tiempo, enemigo.evento_pendiente.tiempo)


class TestRestauracionYDeterminismo(unittest.TestCase):
    def test_el_resultado_no_depende_de_la_frecuencia_de_checkpoints(self):  # FR-LIN-015, FR-LIN-017
        resultados = []
        for frecuencia in (1, 2, 3, 5, 1000):
            partida, fotos = _con_esperas(8, checkpoint_cada=frecuencia)
            por_accion = [_foto_resumen(partida.consultar_accion(k)) for k in range(1, 9)]
            self.assertEqual(por_accion, fotos[:8])
            resultados.append(por_accion)
        for otro in resultados[1:]:
            self.assertEqual(otro, resultados[0])

    def test_los_instantes_con_decision_coinciden_con_el_vivo_desde_un_checkpoint(self):  # FR-LIN-001, FR-LIN-002, FR-LIN-017
        partida, fotos = _con_esperas(8, checkpoint_cada=3)
        for numero, foto in enumerate(fotos):
            self.assertEqual(_foto_resumen(partida.consultar_instante(numero * 100)), foto)

    def test_los_instantes_sin_decision_coinciden_entre_frecuencias(self):  # FR-LIN-001, FR-LIN-017
        referencia = None
        for frecuencia in (1, 4, 1000):
            partida, _ = _con_esperas(8, checkpoint_cada=frecuencia)
            fotos = [_foto_resumen(partida.consultar_instante(t)) for t in (25, 50, 150, 275, 399, 650)]
            if referencia is None:
                referencia = fotos
            self.assertEqual(fotos, referencia)

    def test_se_crea_un_checkpoint_cada_k_acciones(self):  # FR-LIN-013, FR-LIN-015
        partida, _ = _con_esperas(8, checkpoint_cada=3)
        linea = partida.linea_tiempo()
        self.assertEqual(linea.cantidad_checkpoints(), 2)
        self.assertEqual(linea.buscar_checkpoint(8).numero_acciones, 6)
        self.assertEqual(linea.buscar_checkpoint(5).numero_acciones, 3)
        self.assertIsNone(linea.buscar_checkpoint(2))

    def test_con_k_1_hay_un_checkpoint_por_accion(self):  # FR-LIN-013
        partida, _ = _con_esperas(6, checkpoint_cada=1)
        self.assertEqual(partida.linea_tiempo().cantidad_checkpoints(), 6)

    def test_con_k_mayor_que_las_acciones_no_hay_checkpoints(self):  # FR-LIN-013
        partida, _ = _con_esperas(6, checkpoint_cada=1000)
        self.assertEqual(partida.linea_tiempo().cantidad_checkpoints(), 0)

    def test_el_azar_vivo_no_se_toca_al_consultar(self):  # FR-LIN-005, FR-LIN-017
        consultada, _ = _con_esperas(4, checkpoint_cada=2)
        control, _ = _con_esperas(4, checkpoint_cada=2)
        for _ in range(4):
            consultada.consultar_accion(1)
            consultada.consultar_accion(4)
            consultada.consultar_instante(150)
            _hacer(consultada, "esperar")
            _hacer(control, "esperar")
        self.assertEqual(_foto_viva(consultada), _foto_viva(control))
        self.assertEqual(consultada._azar.getstate(), control._azar.getstate())

    def test_tras_el_pergamino_el_checkpoint_posterior_ya_no_se_usa(self):  # FR-LIN-007, FR-LIN-017
        partida = _armar(cazadores=[(1, "z1", None)], velocidad_cazador=200, pergaminos=1, checkpoint_cada=2)
        fotos = [_foto_viva(partida)]
        for _ in range(4):
            _hacer(partida, "esperar")
            fotos.append(_foto_viva(partida))
        self.assertEqual(partida.linea_tiempo().cantidad_checkpoints(), 2)
        _hacer(partida, "pergamino")
        self.assertEqual(len(partida.linea_tiempo()), 3)
        self.assertEqual(partida.linea_tiempo().cantidad_checkpoints(), 1)
        for k in range(1, 4):
            self.assertEqual(_foto_resumen(partida.consultar_accion(k)), fotos[k - 1])


class TestConsultasValidasYRechazadas(unittest.TestCase):
    def setUp(self):
        self.partida, self.fotos = _con_esperas(4, checkpoint_cada=2)

    def test_consulta_valida_por_accion_en_los_limites(self):  # FR-LIN-003
        self.assertEqual(_foto_resumen(self.partida.consultar_accion(1)), self.fotos[0])
        self.assertEqual(_foto_resumen(self.partida.consultar_accion(4)), self.fotos[3])

    def test_consulta_valida_por_instante_en_los_limites(self):  # FR-LIN-006
        self.assertEqual(_foto_resumen(self.partida.consultar_instante(0)), self.fotos[0])
        self.assertEqual(_foto_resumen(self.partida.consultar_instante(400)), self.fotos[4])

    def test_k_cero_se_rechaza_con_motivo(self):  # FR-LIN-003, FR-LIN-023
        with self.assertRaises(IndexError) as contexto:
            self.partida.consultar_accion(0)
        self.assertNotEqual(str(contexto.exception).strip(), "")

    def test_k_negativo_se_rechaza(self):  # FR-LIN-003, FR-LIN-023
        with self.assertRaises(IndexError):
            self.partida.consultar_accion(-1)

    def test_k_igual_a_la_ultima_accion_mas_uno_se_rechaza(self):  # FR-LIN-003, FR-LIN-023
        with self.assertRaises(IndexError) as contexto:
            self.partida.consultar_accion(5)
        self.assertNotEqual(str(contexto.exception).strip(), "")

    def test_k_mayor_que_las_acciones_vigentes_se_rechaza(self):  # FR-LIN-003, FR-LIN-023
        with self.assertRaises(IndexError):
            self.partida.consultar_accion(500)

    def test_argumento_de_accion_mal_formado_se_rechaza(self):  # FR-LIN-023
        for argumento in ("2", None, 1.5, True, [1]):
            with self.assertRaises(ValueError) as contexto:
                self.partida.consultar_accion(argumento)
            self.assertNotEqual(str(contexto.exception).strip(), "")

    def test_instante_mal_formado_o_negativo_se_rechaza(self):  # FR-LIN-006, FR-LIN-023
        for argumento in ("100", None, 1.5, True, -1, [1]):
            with self.assertRaises(ValueError) as contexto:
                self.partida.consultar_instante(argumento)
            self.assertNotEqual(str(contexto.exception).strip(), "")

    def test_instante_posterior_al_reloj_se_rechaza_con_motivo(self):  # FR-LIN-006, FR-LIN-023
        with self.assertRaises(ValueError) as contexto:
            self.partida.consultar_instante(401)
        self.assertNotEqual(str(contexto.exception).strip(), "")

    def test_ningun_rechazo_produce_efectos(self):  # FR-LIN-023, SC-LIN-007
        antes = _observable(self.partida)
        casos = ((self.partida.consultar_accion, (0, -1, 5, 99, "1", None, 2.5, True)),
                 (self.partida.consultar_instante, (401, 10 ** 9, -1, "abc", None, 2.5, True)))
        for consulta, argumentos in casos:
            for argumento in argumentos:
                with self.assertRaises((ValueError, IndexError)):
                    consulta(argumento)
        self.assertEqual(_observable(self.partida), antes)

    def test_tras_los_rechazos_la_partida_sigue_igual_que_una_de_control(self):  # FR-LIN-023, SC-LIN-007
        control, _ = _con_esperas(4, checkpoint_cada=2)
        for argumento in (0, 5, "x"):
            with self.assertRaises((ValueError, IndexError)):
                self.partida.consultar_accion(argumento)
        for _ in range(3):
            _hacer(self.partida, "esperar")
            _hacer(control, "esperar")
        self.assertEqual(_foto_viva(self.partida), _foto_viva(control))
        self.assertEqual(self.partida.mensajes(), control.mensajes())

    def test_el_rechazo_no_cuenta_como_accion_ni_toca_el_pergamino(self):  # FR-LIN-005, FR-LIN-023
        partida = _armar(pergaminos=1)
        _hacer(partida, "esperar")
        with self.assertRaises(ValueError):
            partida.consultar_instante(10 ** 6)
        self.assertEqual(len(partida.linea_tiempo()), 1)
        self.assertEqual(partida.vista().pergaminos, 1)
        self.assertEqual(partida.vista().retrocesos_posibles, 1)


if __name__ == "__main__":
    unittest.main()
