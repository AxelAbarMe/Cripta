"""Pruebas de VistaConsola con entrada y salida simuladas.


Se ejecuta desde la raíz del proyecto con:  python -m unittest tests.vista.test_vista_consola -v
"""
import unittest
from types import SimpleNamespace


from cripta.controlador.controlador_cripta import Orden
from cripta.modelo.enemigo import Enemigo


from cripta.modelo.conocimiento_jugador import SalaConocida, SalidaConocida
from cripta.modelo.linea_tiempo import ObjetoHistorico, ResumenHistorico
from cripta.modelo.resultado_partida import EnemigoVista, SalidaVista, VistaPartida
from cripta.modelo.resultado_partida import MapaConocido
from cripta.vista.vista_base import VistaBase
from cripta.vista.vista_consola import ANCHO, VistaConsola, _caja_mensajes
from tests.modelo.test_conocimiento_jugador import crear_partida_sintetica, salida


def crear(*respuestas):
    """Devuelve (vista, salida): `respuestas` se entregan una por una; al acabarse simula Ctrl+D."""
    pendientes, salida = list(respuestas), []


    def entrada(_indicador):
        if not pendientes:
            raise EOFError
        return pendientes.pop(0)
    return VistaConsola(entrada, salida.append), salida


class TestComandos(unittest.TestCase):
    def interpretar(self, texto):
        vista, _ = crear(texto)
        return vista.pedir_orden(None)


    def test_direcciones_en_una_letra_o_con_mover(self):
        self.assertEqual(self.interpretar("n"), Orden("mover", "N"))
        self.assertEqual(self.interpretar("MOVER o"), Orden("mover", "O"))


    def test_abrir_lleva_la_direccion(self):
        self.assertEqual(self.interpretar("abrir e"), Orden("abrir", "E"))


    def test_las_posiciones_se_muestran_desde_1_y_se_envian_desde_0(self):
        self.assertEqual(self.interpretar("atacar 1"), Orden("atacar", 0))
        self.assertEqual(self.interpretar("recoger 3"), Orden("recoger", 2))


    def test_ordenar_solo_acepta_los_criterios_validos(self):
        self.assertEqual(self.interpretar("ordenar valor"), Orden("ordenar", "valor"))
        vista, salida = crear("ordenar color", "esperar")
        self.assertEqual(vista.pedir_orden(None), Orden("esperar"))
        self.assertTrue(any("no reconocido" in linea for linea in salida))


    def test_comandos_sin_argumento_y_cursor_del_inventario(self):
        for texto in ("esperar", "usar", "equipar", "soltar", "guardar", "cargar", "salir"):
            self.assertEqual(self.interpretar(texto), Orden(texto))
        self.assertEqual(self.interpretar("sig"), Orden("siguiente"))
        self.assertEqual(self.interpretar("ant"), Orden("anterior"))


    def test_pergamino_admite_de_1_a_5(self):
        self.assertEqual(self.interpretar("pergamino"), Orden("pergamino", 1))
        self.assertEqual(self.interpretar("pergamino 5"), Orden("pergamino", 5))
        vista, _ = crear("pergamino 6", "pergamino 0", "esperar")
        self.assertEqual(vista.pedir_orden(None), Orden("esperar"))


    def test_comando_invalido_se_repite_hasta_recibir_uno_valido(self):
        vista, salida = crear("", "xyz", "atacar", "atacar x", "s")
        self.assertEqual(vista.pedir_orden(None), Orden("mover", "S"))
        self.assertEqual(sum("no reconocido" in linea for linea in salida), 4)


    def test_fin_de_entrada_equivale_a_salir(self):
        vista, _ = crear()
        self.assertEqual(vista.pedir_orden(None), Orden("salir"))


    def test_confirmar_acepta_s_si_y_rechaza_lo_demas(self):
        for texto, esperado in (("s", True), ("SI", True), ("sí", True), ("n", False), ("", False)):
            vista, _ = crear(texto)
            self.assertEqual(vista.confirmar("¿Seguro?"), esperado, texto)
        vista, _ = crear()
        self.assertFalse(vista.confirmar("¿Seguro?"))


class TestMenuYCripta(unittest.TestCase):
    def test_elegir_cripta_devuelve_el_id_o_none(self):
        from types import SimpleNamespace as N
        criptas = (N(id="c-1", nombre="Uno", salas=20, dificultad=1), N(id="c-2", nombre="Dos", salas=60, dificultad=2))
        vista, _ = crear("2")
        self.assertEqual(vista.elegir_cripta(criptas), "c-2")
        vista, _ = crear("9", "abc", "1")
        self.assertEqual(vista.elegir_cripta(criptas), "c-1")
        vista, _ = crear("0")
        self.assertIsNone(vista.elegir_cripta(criptas))
        vista, _ = crear()
        self.assertIsNone(vista.elegir_cripta(criptas))


class TestCajaDeMensajes(unittest.TestCase):
    MENSAJES = ("Entras a Sala 2.", "Recoges Llave de bronce.", "Equipas Daga oxidada.")


    def test_cada_mensaje_lleva_su_indice_desde_1(self):
        texto = "\n".join(_caja_mensajes(self.MENSAJES))
        for numero, mensaje in enumerate(self.MENSAJES, start=1):
            self.assertIn(f"{numero}. {mensaje}", texto)


    def test_con_20_mensajes_van_del_1_al_20_en_orden(self):
        mensajes = tuple(f"Mensaje {k}" for k in range(1, 21))
        texto = "\n".join(_caja_mensajes(mensajes))
        for k in range(1, 21):
            self.assertIn(f"{k}. Mensaje {k}", texto)


    def test_la_caja_conserva_el_ancho_fijo(self):
        mensajes = tuple("texto largo " * 12 for _ in range(20))
        for linea in _caja_mensajes(mensajes):
            self.assertEqual(len(linea), ANCHO)


    def test_un_mensaje_largo_se_ajusta_con_sangria_del_tamano_de_su_indice(self):
        lineas = _caja_mensajes(("palabra " * 20,))
        self.assertTrue(any(l.startswith("|    palabra") for l in lineas))     # sangría de 3 ("1. ")


    def test_sin_mensajes(self):
        self.assertIn("(sin mensajes)", "\n".join(_caja_mensajes(())))


def vista_armada(salidas, enemigos):
    """VistaPartida mínima armada a mano, con la sala 1 como sala actual."""
    return VistaPartida(
        sala_id=1, sala_nombre="Sala 1", salidas=tuple(salidas), enemigos=tuple(enemigos), objetos_suelo=(),
        trampas=(), vida=50, vida_max=100, ataque=6, defensa=2, velocidad=100, efectos_activos=(),
        objeto_actual=None, objeto_actual_indice=None, inventario_cantidad=0, inventario_capacidad=10,
        pergaminos=0, retrocesos_posibles=0, arma_equipada=None, armadura_equipada=None, tiempo=0,
        desenlace="en_curso")


def pantalla(vista_partida):
    vista, salida = crear()
    vista.mostrar_estado(vista_partida, ())
    return [linea for bloque in salida for linea in bloque.splitlines()]


class TestTerrenoEnLaVista(unittest.TestCase):
    def test_cada_salida_muestra_su_costo(self):  # FR-TER-024
        for costo in (250, 100):
            lineas = pantalla(vista_armada([SalidaVista("E", 2, False, costo)], []))
            linea = next(l for l in lineas if "Salidas" in l)
            self.assertIn(str(costo), linea)


    def test_el_cazador_se_distingue_de_los_demas_enemigos(self):  # FR-TER-024
        cazador = EnemigoVista("Sabueso [e-1]", "e-1", 40, 40, True)
        otro = EnemigoVista("Rata [e-2]", "e-2", 40, 40, False)
        lineas = pantalla(vista_armada([], [cazador, otro]))
        resto = []
        for numero, enemigo in ((1, cazador), (2, otro)):
            linea = next(l for l in lineas if enemigo.etiqueta in l)
            resto.append(" ".join(linea.replace(enemigo.etiqueta, "").replace(f"{numero}.", "").split()))
        self.assertNotEqual(resto[0], resto[1])


class TestVistaConNiebla(unittest.TestCase):
    """T023: FR-NIE-007 y FR-NIE-008, escenarios 1.2, 1.4 y 1.5."""


    def test_partida_proyecta_costos_y_puertas_recordados_sin_filtrar_datos(self):
        partida = crear_partida_sintetica((
            {"id": 1, "nombre": "Vestibulo visible", "salidas": {
                "E": salida(2, 37, llave="llave"), "N": salida(3, 211),
            }},
            {"id": 2, "nombre": "Sala avistada secreta", "salidas": {"O": salida(1, 37, llave="llave")}},
            {"id": 3, "nombre": "Sala desconocida secreta", "salidas": {"S": salida(1, 211)}},
        ))
        ficha = SimpleNamespace(
            id="ent_cazador", nombre="Acechador", vida_max=12, ataque=2,
            defensa=0, velocidad=100, comportamiento="cazador", suelta=(), rango=3,
        )
        partida._mapa.obtener(1).enemigos_activos.append(Enemigo("e-prueba", ficha, 1))


        vista_antes = partida.vista()
        salida_este = next(s for s in vista_antes.salidas if s.direccion == "E")
        salida_norte = next(s for s in vista_antes.salidas if s.direccion == "N")
        self.assertEqual((salida_este.costo, salida_norte.costo), (37, 211))
        self.assertFalse(salida_este.cerrada)
        self.assertFalse(salida_norte.cerrada)
        self.assertTrue(vista_antes.enemigos[0].es_cazador)
        panel_antes = "\n".join(VistaConsola()._paneles_izquierdos(vista_antes))
        self.assertIn("[CAZADOR]", panel_antes)
        self.assertIn("E->2 (37)", panel_antes)


        partida._mapa.cerrar_puerta(1, "E")
        vista = partida.vista()
        salida_este = next(s for s in vista.salidas if s.direccion == "E")
        self.assertFalse(salida_este.cerrada)
        panel = "\n".join(VistaConsola()._paneles_izquierdos(vista))
        self.assertIn("E->2 (37)", panel)
        self.assertNotIn("[CERRADA]", panel)
        for nombre_oculto in ("Sala avistada secreta", "Sala desconocida secreta"):
            self.assertNotIn(nombre_oculto, repr(vista))
            self.assertNotIn(nombre_oculto, panel)
        self.assertIn("Sala avistada secreta", repr(partida._mapa.obtener(2).esqueleto.nombre))


class TestContratoNiebla(unittest.TestCase):
    def test_vista_base_exige_presentacion_del_mapa_y_motivos(self):
        """FR-NIE-007/008/013, escenario 1.2 y viaje detenido con motivos."""
        metodos = VistaBase.__abstractmethods__
        self.assertIn("mostrar_mapa_conocido", metodos)
        self.assertIn("mostrar_motivos_viaje", metodos)


        implementaciones = {nombre: (lambda self, *args: None) for nombre in metodos
                            if nombre not in ("mostrar_mapa_conocido", "mostrar_motivos_viaje")}
        vista_incompleta = type("VistaIncompleta", (VistaBase,), implementaciones)
        with self.assertRaises(TypeError):
            vista_incompleta()
        implementaciones["mostrar_mapa_conocido"] = lambda self, proyeccion: None
        implementaciones["mostrar_motivos_viaje"] = lambda self, motivos: None
        vista_completa = type("VistaCompleta", (VistaBase,), implementaciones)
        self.assertIsInstance(vista_completa(), VistaBase)


class TestPresentacionNiebla(unittest.TestCase):
    """FR-NIE-007/008/009/013, escenarios 1.2, 1.3 y viaje detenido."""


    def test_mapa_muestra_datos_explorados_y_solo_existencia_avistada(self):
        """La proyeccion garantiza que solo hay nombre en la sala explorada."""
        proyeccion = MapaConocido((
            SalaConocida(1, "explorada", "Vestibulo", (
                SalidaConocida("E", 2, 37, "abierta"),
                SalidaConocida("N", 3, 211, "cerrada"),
            )),
            SalaConocida(2, "avistada", "Secreto", ()),
        ))
        vista, salida = crear()
        vista.mostrar_mapa_conocido(proyeccion)
        lineas = salida + vista._pendientes


        def linea_de_caja(contenido):
            return f"| {contenido.ljust(ANCHO - 4)} |"


        for contenido in (
            "Sala 1: Vestibulo (explorada)",
            "  E -> sala 2, costo 37, puerta abierta",
            "  N -> sala 3, costo 211, puerta cerrada",
            "Sala 2: existe, sin explorar",
        ):
            self.assertIn(linea_de_caja(contenido), lineas)
        texto = "\n".join(lineas)
        self.assertIn("Vestibulo", texto)
        self.assertNotIn("Secreto", texto)


    def test_motivos_se_traducen_y_conservan_el_orden(self):
        vista, salida = crear()
        motivos = ("llegada_destino", "enemigos_vivos", "daño_recibido", "sin_ruta")
        vista.mostrar_motivos_viaje(motivos)
        texto = "\n".join(salida + vista._pendientes)
        textos = ("destino", "enemigos", "daño", "ruta")
        posiciones = [texto.lower().find(palabra) for palabra in textos]
        self.assertTrue(all(posicion >= 0 for posicion in posiciones), texto)
        self.assertTrue(posiciones[0] < posiciones[1] < posiciones[2] < posiciones[3])


    def test_interpreta_mapa_e_ir_a_con_identificador_entero(self):
        vista = VistaConsola()
        self.assertEqual(vista._interpretar(["mapa"]), Orden("mapa"))
        self.assertEqual(vista._interpretar(["ir", "a", "3"]), Orden("ir_a", 3))
        for partes in (["ir", "a"], ["ir", "a", "x"], ["ir", "a", "-3"], ["ir", "3"]):
            with self.subTest(partes=partes):
                self.assertIsNone(vista._interpretar(partes))


    def test_controles_visibles_listan_mapa_e_ir_a_sin_salirse_de_celda(self):
        lineas = VistaConsola._controles()
        texto = "\n".join(lineas).lower()
        self.assertIn("mapa", texto)
        self.assertIn("ir a <sala>", texto)


        bordes = lineas[:-1:2]
        filas = lineas[1:-1:2]
        self.assertEqual(len(bordes), len(filas))
        for borde, fila in zip(bordes, filas):
            self.assertEqual(len(fila), len(borde))
            separadores = [indice for indice, caracter in enumerate(borde) if caracter == "+"]
            self.assertTrue(all(fila[indice] == "|" for indice in separadores))
            anchos_celdas = [derecha - izquierda for izquierda, derecha in zip(separadores, separadores[1:])]
            self.assertTrue(all(ancho == anchos_celdas[0] for ancho in anchos_celdas))


class TestComandoHistoria(unittest.TestCase):
    def interpretar(self, texto):
        vista, _ = crear(texto)
        return vista.pedir_orden(None)


    def test_historia_con_un_instante(self):  # FR-LIN-003
        self.assertEqual(self.interpretar("historia 150"), Orden("historia", "150"))
        self.assertEqual(self.interpretar("HISTORIA 0"), Orden("historia", "0"))


    def test_historia_con_una_accion(self):  # FR-LIN-003
        self.assertEqual(self.interpretar("historia #3"), Orden("historia", "#3"))
        self.assertEqual(self.interpretar("  historia   #12 "), Orden("historia", "#12"))


    def test_el_argumento_mal_formado_se_entrega_tal_cual_para_que_se_informe_el_motivo(self):  # FR-LIN-023
        self.assertEqual(self.interpretar("historia abc"), Orden("historia", "abc"))
        self.assertEqual(self.interpretar("historia #"), Orden("historia", "#"))
        self.assertEqual(self.interpretar("historia -5"), Orden("historia", "-5"))
        self.assertEqual(self.interpretar("historia 1 2"), Orden("historia", "1 2"))


    def test_historia_sin_argumento_se_entrega_sin_argumento(self):  # FR-LIN-023
        self.assertEqual(self.interpretar("historia"), Orden("historia", None))


    def test_historia_no_se_confunde_con_otros_comandos(self):  # FR-LIN-003
        vista, salida = crear("historiax 3", "esperar")
        self.assertEqual(vista.pedir_orden(None), Orden("esperar"))
        self.assertTrue(any("no reconocido" in linea for linea in salida))


    def test_los_controles_muestran_el_comando(self):  # FR-LIN-003
        lineas = pantalla(vista_armada([], []))
        self.assertTrue(any("historia" in linea for linea in lineas))


def resumen_armado(**cambios):
    """ResumenHistorico mínimo con una sala explorada y una avistada, para presentarlo."""
    datos = dict(
        tiempo=150, sala_id=1, vida=40, vida_max=100, ataque=6, defensa=2, velocidad=100,
        inventario=(ObjetoHistorico("i-1", "itm_antorcha"),), efectos_activos=("Antorcha",),
        enemigos=(EnemigoVista("Rata gigante [e-201]", "e-201", 8, 12, False),),
        mapa_conocido=(SalaConocida(1, "explorada", "Sala uno", (SalidaConocida("E", 2, 100, "abierta"),)),
                       SalaConocida(2, "avistada", None, ())))
    datos.update(cambios)
    return ResumenHistorico(**datos)


def historia(resumen, referencia="t=150"):
    """(lo impreso justo tras mostrar_historia, las líneas del bloque de historia tras el siguiente mostrar_estado)."""
    vista, salida = crear()
    vista.mostrar_historia(resumen, referencia)
    inmediato = list(salida)
    vista.mostrar_estado(vista_armada([], []), ())
    lineas = [linea for bloque in salida for linea in bloque.splitlines()]
    inicio = next(i for i, linea in enumerate(lineas) if "HISTORIA" in linea and i > _fin_del_estado(lineas))
    return inmediato, lineas, lineas[inicio:]


def _fin_del_estado(lineas):
    # Índice de la caja de mensajes: lo que viene después ya no es la pantalla de juego
    return next(i for i, linea in enumerate(lineas) if "MENSAJES" in linea)


class TestPantallaDeHistoria(unittest.TestCase):
    def test_la_historia_espera_al_siguiente_estado_y_sale_debajo_de_el(self):  # FR-LIN-004
        inmediato, lineas, _ = historia(resumen_armado())
        self.assertEqual(inmediato, [])
        self.assertGreater(len(lineas), _fin_del_estado(lineas) + 1)
        self.assertTrue(any("HISTORIA" in linea for linea in lineas[_fin_del_estado(lineas):]))


    def test_una_historia_ya_mostrada_no_se_repite(self):  # FR-LIN-005
        vista, salida = crear()
        vista.mostrar_historia(resumen_armado(), "t=150")
        vista.mostrar_estado(vista_armada([], []), ())
        salida.clear()
        vista.mostrar_estado(vista_armada([], []), ())
        lineas = [linea for bloque in salida for linea in bloque.splitlines()]
        self.assertFalse(any("HISTORIA" in linea for linea in lineas[_fin_del_estado(lineas):]))


    def test_el_titulo_lleva_la_referencia_consultada(self):  # FR-LIN-003
        for referencia in ("t=150", "#3"):
            _, _, bloque = historia(resumen_armado(), referencia)
            self.assertIn(referencia, bloque[0])


    def test_muestra_el_reloj(self):  # FR-LIN-004, SC-LIN-001
        _, _, bloque = historia(resumen_armado(tiempo=150))
        self.assertTrue(any("Tiempo" in linea and "150" in linea for linea in bloque))


    def test_muestra_la_sala_del_jugador(self):  # FR-LIN-004, SC-LIN-001
        _, _, bloque = historia(resumen_armado(sala_id=7))
        self.assertTrue(any("Sala 7" in linea for linea in bloque))


    def test_muestra_vida_y_estadisticas(self):  # FR-LIN-004, SC-LIN-001
        _, _, bloque = historia(resumen_armado())
        texto = "\n".join(bloque)
        for esperado in ("Vida 40/100", "Ataque 6", "Defensa 2", "Velocidad 100"):
            self.assertIn(esperado, texto)


    def test_muestra_el_inventario(self):  # FR-LIN-004, SC-LIN-001
        _, _, bloque = historia(resumen_armado())
        self.assertTrue(any("INVENTARIO" in linea for linea in bloque))
        self.assertTrue(any("itm_antorcha" in linea and "i-1" in linea for linea in bloque))


    def test_inventario_vacio(self):  # FR-LIN-004
        _, _, bloque = historia(resumen_armado(inventario=()))
        self.assertIn("(vacio)", "\n".join(bloque))


    def test_muestra_los_efectos_activos(self):  # FR-LIN-004, SC-LIN-001
        _, _, bloque = historia(resumen_armado(efectos_activos=("Veneno", "Antorcha")))
        self.assertTrue(any("Efectos: Veneno, Antorcha" in linea for linea in bloque))
        _, _, sin = historia(resumen_armado(efectos_activos=()))
        self.assertTrue(any("Efectos: ninguno" in linea for linea in sin))


    def test_muestra_los_enemigos_de_la_sala_con_su_vida(self):  # FR-LIN-004, SC-LIN-001
        _, _, bloque = historia(resumen_armado())
        linea = next(l for l in bloque if "Rata gigante [e-201]" in l)
        self.assertIn("PV 8/12", linea)
        self.assertNotIn("CAZADOR", linea)


    def test_el_cazador_se_distingue_en_la_historia(self):  # FR-LIN-004
        cazador = EnemigoVista("Sabueso [e-1]", "e-1", 40, 40, True)
        _, _, bloque = historia(resumen_armado(enemigos=(cazador,)))
        self.assertIn("[CAZADOR]", next(l for l in bloque if "Sabueso [e-1]" in l))


    def test_sin_enemigos(self):  # FR-LIN-004
        _, _, bloque = historia(resumen_armado(enemigos=()))
        self.assertTrue(any("ENEMIGOS" in linea for linea in bloque))
        self.assertTrue(any("(ninguno)" in linea for linea in bloque))


    def test_muestra_el_mapa_conocido(self):  # FR-LIN-004, FR-LIN-019, SC-LIN-001
        _, _, bloque = historia(resumen_armado())
        self.assertTrue(any("MAPA CONOCIDO" in linea for linea in bloque))
        explorada = next(l for l in bloque if "Sala 1" in l and "explorada" in l)
        self.assertIn("Sala uno", explorada)
        self.assertTrue(any("E->2" in linea and "100" in linea and "abierta" in linea for linea in bloque))
        avistada = next(l for l in bloque if "Sala 2" in l and "avistada" in l)
        self.assertNotIn("explorada", avistada)


    def test_una_puerta_cerrada_se_marca(self):  # FR-LIN-019
        mapa = (SalaConocida(1, "explorada", "Sala uno", (SalidaConocida("N", 3, 50, "cerrada"),)),)
        _, _, bloque = historia(resumen_armado(mapa_conocido=mapa))
        self.assertTrue(any("N->3" in linea and "cerrada" in linea for linea in bloque))


    def test_ninguna_linea_pasa_del_ancho_de_la_pantalla(self):  # SC-LIN-001
        _, _, bloque = historia(resumen_armado())
        for linea in bloque:
            self.assertLessEqual(len(linea), ANCHO)


    def test_mostrar_historia_no_pide_entrada(self):  # FR-LIN-005
        def entrada(_indicador):
            raise AssertionError("mostrar_historia no debe leer del teclado")
        VistaConsola(entrada, lambda _linea: None).mostrar_historia(resumen_armado(), "t=150")


    def test_dos_consultas_seguidas_salen_en_orden(self):  # FR-LIN-005
        vista, salida = crear()
        vista.mostrar_historia(resumen_armado(), "t=150")
        vista.mostrar_historia(resumen_armado(), "#2")
        vista.mostrar_estado(vista_armada([], []), ())
        lineas = [l for bloque in salida for l in bloque.splitlines()]
        titulos = [l for l in lineas[_fin_del_estado(lineas):] if "HISTORIA" in l]
        self.assertEqual(len(titulos), 2)
        self.assertIn("t=150", titulos[0])
        self.assertIn("#2", titulos[1])


if __name__ == "__main__":
    unittest.main()
