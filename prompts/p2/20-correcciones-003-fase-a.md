# Correcciones de la Fase A de la 003, de la revisión del Pull Request

Corrige solo cripta/modelo/resolubilidad.py y tests/modelo/test_resolubilidad.py. No toques tasks.md ni ningún otro archivo.

Reglas generales: sin heapq, bisect, collections, networkx, set ni dict como índice o caché, ni list.sort() o sorted() en cripta/modelo/resolubilidad.py. Los .py van en CRLF. Edita con tu herramienta de edición, no con sed -i. En comentarios y textos nuevos no uses ";". No crees ni cambies de rama y no hagas commit ni push. Si algo contradice spec.md, detente y explícalo.

Punto 1. verificar() y verificar_ingenuo_reiniciado() no coinciden. En verificar(), entro_por_llave_salida solo se activa dentro de if not visitada[destino], tanto en el recorrido principal como en la función interna _activar_llave. Si la sala de salida ya fue alcanzada por una ruta abierta, una puerta con llave_salida que sí se puede cruzar no cuenta. Arreglo: mover la comprobación fuera del if not visitada.
En el recorrido, cuando la llave de la puerta ya está obtenida:
    if destino == sala_salida and idx_k == idx_llave_salida:
        entro_por_llave_salida = True
    if not visitada[destino]:
        visitada[destino] = True
        cola.enqueue(destino)
En _activar_llave, agrega nonlocal entro_por_llave_salida al inicio de la función y usa el mismo patrón dentro del for sobre puertas_pendientes[idx_k]. Usa los nombres reales que ya existen en el archivo, adapta si difieren.

Punto 2. El caso del Apéndice B no reporta el ciclo. Con la llave de salida dentro de la sala de salida, tras la puerta que ella misma abre, ciclos_dependencia sale vacío y debe dar itm_llave_salida -> itm_llave_salida (quickstart, escenario 6). La causa es una línea if ub.sala == sala_salida and k_nombre == llave_salida: continue dentro de _detectar_ciclos, que no tiene respaldo en la spec. Quítala y comprueba que el caso queda correcto.

Punto 3. En tests/modelo/test_resolubilidad.py, el ayudante armar_mapa_conexiones pisa en silencio las direcciones repetidas, y por eso test_cadena_doble_ciclos_independientes pasa con un fixture mal armado. Haz que el ayudante lance ValueError ante direcciones repetidas: antes de construir, para cada conexión revisa las claves (origen, direccion) y (destino, direccion_opuesta(direccion)) y lanza ValueError con el mensaje "Dirección repetida en el fixture: <clave>" si alguna ya fue vista. Usa una lista para llevar las claves vistas, no set ni dict.
Reemplaza el fixture de test_cadena_doble_ciclos_independientes por este, con nombre test_doble_ciclo_con_fixture_consistente:
    mapa = armar_mapa_conexiones([
        (1, "N", 2, True, "itm_c1_b"), (1, "S", 3, True, "itm_c1_a"), (1, "E", 7),
        (7, "N", 4, True, "itm_c2_y"), (7, "S", 5, True, "itm_c2_x"), (7, "E", 6, True, "itm_llave_salida")])
    llaves = (LlaveUbicacionDTO(id="itm_c1_a", sala=2, enemigo=None), LlaveUbicacionDTO(id="itm_c1_b", sala=3, enemigo=None),
              LlaveUbicacionDTO(id="itm_c2_x", sala=4, enemigo=None), LlaveUbicacionDTO(id="itm_c2_y", sala=5, enemigo=None))
    r = VerificadorResolubilidad(mapa, 1, 6, "itm_llave_salida", llaves).verificar()
    ciclos esperados: ["itm_c1_a -> itm_c1_b -> itm_c1_a", "itm_c2_x -> itm_c2_y -> itm_c2_x"], comparando [c.formato() for c in r.ciclos_dependencia]
Si otras pruebas existentes repiten direcciones y ahora lanzan ValueError, corrige esos fixtures y dime cuáles.

Pruebas nuevas en tests/modelo/test_resolubilidad.py:
a) test_dos_rutas_a_la_salida_cuenta_la_puerta_con_llave_salida: mapa = armar_mapa_conexiones([(1, "E", 3), (3, "E", 2), (1, "N", 2, True, "itm_llave_salida")]), llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=1, enemigo=None),), sala inicial 1, salida 2. Tanto verificar() como verificar_ingenuo_reiniciado() deben dar es_resoluble True. Debe fallar antes del punto 1.
b) test_llave_salida_dentro_de_la_sala_de_salida_ApendiceB: mapa = armar_mapa_conexiones([(1, "E", 2, True, "itm_llave_salida")]), llaves = (LlaveUbicacionDTO(id="itm_llave_salida", sala=2, enemigo=None),), sala inicial 1, salida 2. es_resoluble False y [c.formato() for c in ciclos_dependencia] == ["itm_llave_salida -> itm_llave_salida"]. Debe fallar antes del punto 2.
c) test_orden_de_entrada_no_cambia_el_resultado: con fixture_cripta_con_varios_ordenes_validos(), el resultado de verificar() es igual con las llaves en el orden original y con tuple(reversed(llaves)).
d) Haz que test_equivalencia_verificar_e_ingenuo_reiniciado recorra varias criptas, incluidas no resolubles (las de los fixtures y las de los casos de los puntos anteriores), no solo la lineal.

Antes de corregir, corre las pruebas a) y b) y muestra que fallan. Después de corregir, corre py -m unittest tests.modelo.test_resolubilidad y py -m unittest discover -s tests -t . y reporta cuántas pasan. Corre Select-String -Path cripta\modelo\resolubilidad.py -Pattern "heapq|bisect|collections|networkx|sorted\(|\.sort\(|dict|set\(" y muestra la salida. Confirma que solo cambiaron los dos archivos permitidos.