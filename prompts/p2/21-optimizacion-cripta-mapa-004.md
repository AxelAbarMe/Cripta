Optimización acotada, solo cripta/modelo/cripta_mapa.py y sus pruebas. Un perfil de consultar_accion muestra que el 40 % del tiempo es CriptaMapa.obtener (búsqueda binaria en VectorOrdenado, unas 238 000 llamadas en 10 consultas), llamado sobre todo desde BuscadorRutas, costo_de_conexion, puerta_transitable y vecinos.

1. Primero agrega en las pruebas de CriptaMapa (busca el archivo existente en tests/modelo/) casos que fijen el comportamiento de obtener: una sala existente, una inexistente, ids fuera de rango y salas agregadas en varias páginas en desorden. Deben pasar ya con el código actual.
2. Luego agrega en CriptaMapa un índice plano por id de sala (una lista indexada por id que se amplía al agregar páginas, sin dict ni set) para que obtener sea O(1). Mantén la interfaz pública igual y no cambies nada fuera de cripta_mapa.py.

Corre la suite completa y después py -m cripta --bench --solo ciclo_referencia linea_tiempo, y pégame las dos salidas. CRLF, sin ";" en comentarios, sin sorted, bisect ni collections. No marques tareas.
