from grafo import GrafoCiudades
from algoritmos.tsp_backtracking import tsp_backtracking

grafo = GrafoCiudades("utils/mapa_ciudades.json")
grafo.cargar_datos()
G = grafo.obtener_grafo()
ciudades = grafo.obtener_ciudades()

origen = "Santo Domingo"
ruta, costo = tsp_backtracking(G, ciudades, origen)

print("Ruta óptima (TSP):", " → ".join(ruta))
print("Distancia total:", costo, "km")