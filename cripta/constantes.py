"""Constantes. No incluye nada específico de una cripta, 
solo valores de referencia para el motor de juego y la vista, y funciones auxiliares.
"""

# Costos base de las acciones, en unidades de tiempo virtual (2.3)
COSTO_MOVER = 100
COSTO_ATACAR = 100
COSTO_ESPERAR = 100
COSTO_USAR_OBJETO = 50
COSTO_EQUIPAR_OBJETO = 50
COSTO_RECOGER_OBJETO = 25
COSTO_SOLTAR_OBJETO = 25
COSTO_ABRIR_PUERTA = 50

# Velocidad usada en intervalo = max(1, costo * 100 // velocidad) (2.3)
VELOCIDAD_INTERVALO = 100

# Combate: daño = max(1, ataque + azar.randint(RAND_MIN, RAND_MAX) - defensa) (2.6)
RAND_MIN = 0
RAND_MAX = 4
DANO_MIN = 1

# Veneno: pulso de daño cada VENENO_INTERVALO, durante VENENO_DURACION (2.10)
VENENO_INTERVALO = 80
VENENO_DURACION = 400

# Regeneración de enemigos: cada REGENERACION_ENEMIGO, sin superar vida_max (2.10)
REGENERACION_ENEMIGO = 200

# Trampas: intervalo de rearme si la ficha de catálogo no trae uno propio (2.10)
TRAMPA_REARME_DEFAULT = 300

# Rastro del jugador: un rastro con esta antigüedad o más ya no sirve (2.9)
RASTRO_ANTIGUEDAD_MAX = 400

# Pergaminos de retroceso: como mucho se puede deshacer esta cantidad de acciones (2.11)
RETROCESO_MAX_ACCIONES = 5

# Bitácora en pantalla: solo se muestran los últimos N mensajes (4.8)
BITACORA_MAX_MENSAJES = 20

# === RED / DISCO / BENCH (Saul) ===
# Caché de catálogo en memoria: tope por defecto, configurable con --cache-size (4.4)
CACHE_TAMANO_DEFAULT = 25

# Tope de elementos por solicitud en /contenido y /catalogo (3.4)
MAX_ELEMENTOS_POR_LOTE = 10

DIRECCIONES = ("N", "S", "E", "O")


def direccion_opuesta(direccion: str) -> str:
    """La dirección por la que se vería la misma puerta desde la sala del otro lado."""
    if direccion == "N":
        return "S"
    if direccion == "S":
        return "N"
    if direccion == "E":
        return "O"
    if direccion == "O":
        return "E"
    raise ValueError(f"Dirección inválida: {direccion}")

# === MODELO (Isaac) ===