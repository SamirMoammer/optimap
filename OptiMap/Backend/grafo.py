import json
import networkx as nx

class GrafoCiudades:
    def __init__(self, archivo_json):
        self.archivo_json = archivo_json
        self.grafo = nx.Graph()
        self.ciudades = []

    def cargar_datos(self):
        with open(self.archivo_json, 'r') as f:
            datos = json.load(f)

        self.ciudades = datos["ciudades"]
        distancias = datos["distancias"]

        # Crear nodos
        for ciudad in self.ciudades:
            self.grafo.add_node(ciudad)

        # Crear aristas con pesos
        for origen, destinos in distancias.items():
            for destino, peso in destinos.items():
                self.grafo.add_edge(origen, destino, weight=peso)

    def obtener_grafo(self):
        return self.grafo

    def obtener_ciudades(self):
        return self.ciudades
    