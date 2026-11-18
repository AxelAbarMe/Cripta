"""Línea de tiempo pura: acciones vigentes, checkpoints y ajustes de inventario en listas contiguas.
Las búsquedas por instante y por número de acción son binarias escritas a mano.
No usa red, archivos ni vista.
"""


class PuntoControl:
    # Estado completo guardado tras un número de acciones
    __slots__ = ("numero_acciones", "estado")

    def __init__(self, numero_acciones, estado):
        # Guarda el número de acciones incluidas y el estado entregado
        self.numero_acciones = numero_acciones
        self.estado = estado


class LineaTiempo:
    # Registro de la línea vigente con un checkpoint como máximo cada K acciones

    def __init__(self, frecuencia):
        # Valida K como entero mayor o igual que 1 y deja la línea vacía
        if isinstance(frecuencia, bool) or not isinstance(frecuencia, int) or frecuencia < 1:
            raise ValueError("La frecuencia de checkpoints debe ser un entero mayor o igual que 1")
        self.frecuencia = frecuencia
        self.inspecciones_ultima_busqueda = 0
        self._acciones = []
        self._tiempos = []
        self._puntos = []
        self._ajustes_posicion = []
        self._ajustes_instancias = []

    def __len__(self):
        # Cantidad de acciones vigentes
        return len(self._acciones)

    def registrar_accion(self, datos, tiempo):
        # Anexa una acción con instante no decreciente y devuelve su número desde 1
        if len(self._tiempos) > 0 and tiempo < self._tiempos[-1]:
            raise ValueError("El instante de la acción no puede ser menor que el de la anterior")
        self._acciones.append(datos)
        self._tiempos.append(tiempo)
        return len(self._acciones)

    def accion(self, k):
        # Devuelve los datos de la acción vigente número k
        self._validar_numero(k)
        return self._acciones[k - 1]

    def tiempo_de(self, k):
        # Devuelve el instante de la acción vigente número k
        self._validar_numero(k)
        return self._tiempos[k - 1]

    def contar_hasta_instante(self, t, inclusivo):
        # Búsqueda binaria de cuántas acciones tienen instante menor o igual (o solo menor) que t
        bajo = 0
        alto = len(self._tiempos)
        inspecciones = 0
        while bajo < alto:
            medio = (bajo + alto) // 2
            inspecciones += 1
            if self._tiempos[medio] < t or (inclusivo and self._tiempos[medio] == t):
                bajo = medio + 1
            else:
                alto = medio
        self.inspecciones_ultima_busqueda = inspecciones
        return bajo

    def debe_crear_checkpoint(self):
        # Indica si el número actual de acciones es múltiplo de K y aún no tiene checkpoint
        cantidad = len(self._acciones)
        if cantidad == 0 or cantidad % self.frecuencia != 0:
            return False
        return len(self._puntos) == 0 or self._puntos[-1].numero_acciones != cantidad

    def registrar_checkpoint(self, estado):
        # Guarda el estado como checkpoint de la acción actual si corresponde por K
        cantidad = len(self._acciones)
        if cantidad == 0 or cantidad % self.frecuencia != 0:
            raise ValueError("Solo se crea checkpoint en un múltiplo positivo de K acciones")
        if len(self._puntos) > 0 and self._puntos[-1].numero_acciones == cantidad:
            raise ValueError("Ya existe un checkpoint para este número de acciones")
        self._puntos.append(PuntoControl(cantidad, estado))

    def cantidad_checkpoints(self):
        # Cantidad de checkpoints vigentes
        return len(self._puntos)

    def buscar_checkpoint(self, k):
        # Búsqueda binaria del checkpoint con mayor número de acciones menor o igual que k
        bajo = 0
        alto = len(self._puntos)
        inspecciones = 0
        while bajo < alto:
            medio = (bajo + alto) // 2
            inspecciones += 1
            if self._puntos[medio].numero_acciones <= k:
                bajo = medio + 1
            else:
                alto = medio
        self.inspecciones_ultima_busqueda = inspecciones
        if bajo == 0:
            return None
        return self._puntos[bajo - 1]

    def truncar(self, n):
        # Deja solo las primeras n acciones, quita checkpoints posteriores y acumula ajustes en n
        if isinstance(n, bool) or not isinstance(n, int) or n < 0 or n > len(self._acciones):
            raise ValueError("El límite de truncamiento debe estar entre 0 y la cantidad de acciones")
        del self._acciones[n:]
        del self._tiempos[n:]
        while len(self._puntos) > 0 and self._puntos[-1].numero_acciones > n:
            self._puntos.pop()
        indice = len(self._ajustes_posicion) - 1
        while indice >= 0 and self._ajustes_posicion[indice] > n:
            self._ajustes_posicion[indice] = n
            indice -= 1

    def registrar_ajuste(self, instancias):
        # Anexa un ajuste de inventario en la posición actual sin numerarlo ni contarlo para K
        self._ajustes_posicion.append(len(self._acciones))
        self._ajustes_instancias.append(list(instancias))

    def ajustes_en(self, posicion):
        # Devuelve una copia con las instancias de los ajustes situados en la posición dada
        resultado = []
        for indice in range(len(self._ajustes_posicion)):
            if self._ajustes_posicion[indice] == posicion:
                for instancia in self._ajustes_instancias[indice]:
                    resultado.append(instancia)
        return resultado

    def _validar_numero(self, k):
        # Rechaza números de acción fuera de 1 hasta la cantidad vigente
        if k < 1 or k > len(self._acciones):
            raise IndexError("No hay una acción vigente con el número " + str(k))
