from grafo import GrafoCiudades
from algoritmos.prim_greedy import mst_prim

grafo = GrafoCiudades("utils/mapa_ciudades.json")
grafo.cargar_datos()
G = grafo.obtener_grafo()

aristas, costo = mst_prim(G)

print("Conexión mínima (Prim):")
for u, v, peso in aristas:
    print(f"{u} ↔ {v} ({peso} km)")
print("Costo total:", costo, "km")
