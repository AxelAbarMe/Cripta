import uuid
import json
import requests
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.cripta_general_dto import CriptaGeneralDTO
from cripta.dto.pagina_esqueleto_dto import PaginaEsqueletoDTO

BASE_URL = "https://cripta-api.kad06a0zhgs84.us-east-2.cs.amazonlightsail.com/v1"

# Un solo id por ejecución: se genera una vez y se reusa en todas las solicitudes
client_id = str(uuid.uuid4())
headers = {"X-Cripta-Client-Id": client_id}


def get(ruta, parametros=None):
    respuesta = requests.get(BASE_URL + ruta, headers=headers, params=parametros, timeout=10)
    print(f"\nGET {ruta} {parametros or ''} -> {respuesta.status_code}")
    datos = respuesta.json()
    print(json.dumps(datos, indent=2, ensure_ascii=False))
    return datos


criptas = get("/criptas")
id_cripta = criptas["criptas"][0]["id"]

general = get(f"/criptas/{id_cripta}")
esqueleto = get(f"/criptas/{id_cripta}/salas", {"pagina": 1})
contenido = get(f"/criptas/{id_cripta}/contenido", {"salas": "1,2,3"})
contenido_resto = get(f"/criptas/{id_cripta}/contenido", {"salas": "4,5,6"})
catalogo = get("/catalogo", {"ids": "ent_rata_gigante,itm_antorcha,itm_daga_oxidada,"
                                     "trp_dardos,itm_llave_bronce,itm_coraza_cuero"})
catalogo_resto = get("/catalogo", {"ids": "ent_guardian_oseo,itm_llave_negra,itm_pocion_menor,"
                                          "itm_pergamino_retroceso,itm_antidoto"})

dto = CriptaGeneralDTO.desde_json(general)
print(dto)
print("Vida del jugador:", dto.jugador.vida_max)
print("Presupuesto:", dto.presupuesto_solicitudes)

pagina = PaginaEsqueletoDTO.desde_json(esqueleto)
sala2 = pagina.salas[1]

print(sala2.nombre)
print("Norte:", sala2.salida("N"))
print("Oeste:", sala2.salida("O"))
print("Este:", sala2.este)
print("¿Este cerrada?", sala2.este.cerrada, "- llave:", sala2.este.llave)