# Formato de los datos para `--offline`

`ClienteOffline` lee de `fixtures/` las respuestas del API guardadas tal cual llegaron, y las
convierte con los mismos DTO que el modo en línea.

**Generar o actualizar** (con internet, desde la raíz):

```
python -m scripts.generar_fixtures [id_cripta]
```

Para actualizar, se borra `fixtures/` y se vuelve a correr.

## Estructura

```
fixtures/
├── criptas.json                  GET /criptas
├── <id_cripta>/
│   ├── general.json              GET /criptas/<id>
│   ├── version.json              GET /criptas/<id>/version
│   ├── salas/pagina_<N>.json     GET /criptas/<id>/salas?pagina=N
│   └── contenido/<id_sala>.json  un elemento de "contenido" de GET /criptas/<id>/contenido
└── catalogo/
    ├── version.json              GET /catalogo/version
    └── <id_ficha>.json           GET /catalogo/<id> (igual a un elemento de "entidades")
```

El contenido y el catálogo se guardan **un archivo por sala y uno por ficha**, aunque el API los
entregue por lotes, para poder armar cualquier lote que pida la partida.

## Origen de los datos

El profesor confirmó (08/10/2026) que para `--offline` se guardan en archivos los `.json` que
devuelve el API, y que la organización de esos archivos queda a criterio nuestro. Este formato
sigue las rutas del API, salvo el contenido (explicado arriba) y los datos generales
(`general.json`, porque `<id_cripta>` ya es la carpeta).