import networkx as nx

def mst_prim(grafo):
    """
    Calcula el Árbol de Expansión Mínima usando el algoritmo de Prim.
    Devuelve:
    - Lista de aristas (origen, destino, peso)
    - Costo total del árbol
    """
    mst = nx.minimum_spanning_tree(grafo, algorithm="prim")
    aristas = list(mst.edges(data="weight"))
    costo_total = sum(peso for _, _, peso in aristas)
    return aristas, costo_total
