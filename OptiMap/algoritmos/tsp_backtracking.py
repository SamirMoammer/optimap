import itertools
import sys

def tsp_backtracking(grafo, ciudades, origen):
    """
    Calcula la ruta más corta visitando todas las ciudades exactamente una vez
    y regresando al origen, usando fuerza bruta con permutaciones (backtracking).
    """
    if origen not in ciudades:
        return None, sys.maxsize

    ciudades_sin_origen = [c for c in ciudades if c != origen]
    mejor_ruta = []
    mejor_costo = sys.maxsize

    for perm in itertools.permutations(ciudades_sin_origen):
        ruta = [origen] + list(perm) + [origen]
        costo = calcular_costo_ruta(grafo, ruta)

        if costo < mejor_costo:
            mejor_costo = costo
            mejor_ruta = ruta

    return mejor_ruta, mejor_costo

def calcular_costo_ruta(grafo, ruta):
    costo = 0
    for i in range(len(ruta) - 1):
        u, v = ruta[i], ruta[i + 1]
        if grafo.has_edge(u, v):
            costo += grafo[u][v]['weight']
        else:
            return sys.maxsize  # Penaliza rutas inválidas
    return costo
