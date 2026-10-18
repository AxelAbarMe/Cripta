'''Prueba rápida del API con el cliente del proyecto: lista las criptas publicadas, pide los datos
generales de la primera y muestra cuántas solicitudes gastó. No es parte del juego ni de las pruebas
automáticas. Empezó como la primera prueba directa al servidor, para ver sus respuestas reales.
Uso, desde la raíz del proyecto:  py -m scripts.prueba_api
'''
from cripta.infraestructura.cliente_http import ClienteHttp
from cripta.infraestructura.contador_solicitudes import ContadorSolicitudes

# El presupuesto es alto a propósito, ya que aquí no se juega una partida, solo se prueban dos solicitudes
contador = ContadorSolicitudes(presupuesto_maximo=999)
cliente = ClienteHttp(contador)

criptas = cliente.listar_criptas()
print(criptas)
general = cliente.obtener_general(criptas[0].id)
print(general)
print(contador.reporte())