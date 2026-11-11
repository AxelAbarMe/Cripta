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
│   ├── llaves.json               GET /criptas/<id>/llaves
│   ├── salas/pagina_<N>.json     GET /criptas/<id>/salas?pagina=N
│   └── contenido/<id_sala>.json  un elemento de "contenido" de GET /criptas/<id>/contenido
└── catalogo/
    ├── version.json              GET /catalogo/version
    └── <id_ficha>.json           GET /catalogo/<id> (igual a un elemento de "entidades")
```

El contenido y el catálogo se guardan **un archivo por sala y uno por ficha**, aunque el API los
entregue por lotes, para poder armar cualquier lote que pida la partida.

## Archivos y campos adicionales

- `llaves.json` guarda la respuesta de `GET /criptas/<id>/llaves` tal como llega (objeto con la
  lista `llaves`, dónde está cada llave). `ClienteOffline.obtener_llaves` la lee.
- `costo` en las salidas de `salas/pagina_<N>.json` es **opcional**: costo de terreno declarado en
  ese lado de la salida (entero mayor o igual a 1). Si falta o es nulo, no está declarado.
- `rango` en las fichas de enemigo del catálogo es **opcional**: rango de percepción de los
  enemigos cazadores (entero mayor o igual a 1). Si falta o es nulo, el cazador es pasivo.

## Datos de prueba congelados

`tests/datos/` guarda `cripta-01` con el catálogo anterior del servidor, como datos de prueba
congelados. **No se regeneran** con el script: `fixtures/` solo tiene las criptas del servidor actual.

## Origen de los datos

El profesor confirmó (08/10/2026) que para `--offline` se guardan en archivos los `.json` que
devuelve el API, y que la organización de esos archivos queda a criterio nuestro. Este formato
sigue las rutas del API, salvo el contenido (explicado arriba) y los datos generales
(`general.json`, porque `<id_cripta>` ya es la carpeta).