from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QListWidgetItem, QGroupBox,
    QSizePolicy, QScrollArea, QAbstractItemView
)
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import networkx as nx

from algoritmos.tsp_backtracking import tsp_backtracking
from algoritmos.prim_greedy import mst_prim
from grafo import GrafoCiudades


class OptiMapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OptiMap – Planificador de Rutas RD")
        self.setGeometry(100, 100, 1100, 800)

        self.grafo_modelo = GrafoCiudades("utils/mapa_ciudades.json")
        self.grafo_modelo.cargar_datos()
        self.G = self.grafo_modelo.obtener_grafo()
        self.ciudades = self.grafo_modelo.obtener_ciudades()

        self.pos = nx.spring_layout(self.G, seed=42)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        controles_box = QGroupBox("Configuración de Ruta")
        controles_layout = QVBoxLayout()
        controles_box.setLayout(controles_layout)

        self.label_origen = QLabel("Ciudad de Origen:")
        self.combo_origen = QComboBox()
        self.combo_origen.addItems(self.ciudades)
        controles_layout.addWidget(self.label_origen)
        controles_layout.addWidget(self.combo_origen)

        self.label_destinos = QLabel("Selecciona los destinos:")

        self.lista_destinos = QListWidget()
        self.lista_destinos.setSelectionMode(QAbstractItemView.NoSelection)
        for ciudad in self.ciudades:
            item = QListWidgetItem(ciudad)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.lista_destinos.addItem(item)

        self.scroll_destinos = QScrollArea()
        self.scroll_destinos.setWidgetResizable(True)
        self.scroll_destinos.setFixedHeight(120)
        self.scroll_destinos.setWidget(self.lista_destinos)

        self.label_destinos.hide()
        self.scroll_destinos.hide()

        controles_layout.addWidget(self.label_destinos)
        controles_layout.addWidget(self.scroll_destinos)

        botones_layout = QHBoxLayout()
        self.btn_tsp = QPushButton("Ruta Óptima (TSP)")
        self.btn_mst = QPushButton("Conexión Mínima (Prim)")
        self.btn_personalizada = QPushButton("Ruta Personalizada")
        botones_layout.addWidget(self.btn_tsp)
        botones_layout.addWidget(self.btn_mst)
        botones_layout.addWidget(self.btn_personalizada)
        controles_layout.addLayout(botones_layout)

        main_layout.addWidget(controles_box)

        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.canvas)

        self.resultado_label = QLabel("")
        self.resultado_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.resultado_label)

        self.btn_tsp.clicked.connect(self.calcular_ruta)
        self.btn_mst.clicked.connect(self.calcular_mst)
        self.btn_personalizada.clicked.connect(self.calcular_ruta_personalizada)

        self.dibujar_grafo_base()

    def obtener_destinos_seleccionados(self):
        destinos = []
        for index in range(self.lista_destinos.count()):
            item = self.lista_destinos.item(index)
            if item.checkState() == Qt.Checked:
                destinos.append(item.text())
        return destinos

    def dibujar_grafo_base(self):
        self.ax.clear()
        self.ax.axis('off')
        nx.draw_networkx_nodes(self.G, self.pos, node_color='lightgray', node_size=800, ax=self.ax)

        offset_ciudades = {
            "Santo Domingo": (0, 0.07),
            "Santiago": (-0.07, 0),
            "La Romana": (0, -0.07),
            "Puerto Plata": (0.07, 0),
            "San Cristóbal": (-0.05, 0.05),
            "San Pedro de Macorís": (0.05, -0.05)
        }
        offset_pos = {c: (self.pos[c][0] + dx, self.pos[c][1] + dy) for c, (dx, dy) in offset_ciudades.items()}
        nx.draw_networkx_labels(self.G, offset_pos, ax=self.ax)

        nx.draw_networkx_edges(self.G, self.pos, edge_color='gray', alpha=0.4, ax=self.ax)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)
        self.canvas.draw()

    def calcular_ruta(self):
        self.mostrar_origen()
        self.ocultar_lista_destinos()
        self.dibujar_grafo_base()
        origen = self.combo_origen.currentText()
        ruta, costo = tsp_backtracking(self.G, self.ciudades, origen)
        self.mostrar_ruta(ruta, costo, color='red', titulo="Ruta Óptima (TSP)")

    def calcular_mst(self):
        self.ocultar_lista_destinos()
        self.ocultar_origen()
        self.dibujar_grafo_base()
        aristas, costo = mst_prim(self.G)
        edges = [(u, v) for u, v, _ in aristas]
        nx.draw_networkx_edges(self.G, self.pos, edgelist=edges, edge_color='green', width=3, ax=self.ax)
        edge_labels = {(u, v): self.G[u][v]['weight'] for u, v, _ in aristas}
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)
        self.canvas.draw()

        texto = "<br>".join([f"{u} ↔ {v} ({w} km)" for u, v, w in aristas])
        self.resultado_label.setText(f"<b>Conexión mínima (Prim):</b><br>{texto}<br><b>Costo total:</b> {costo} km")

    def calcular_ruta_personalizada(self):
        self.mostrar_origen()
        self.mostrar_lista_destinos()
        self.dibujar_grafo_base()
        origen = self.combo_origen.currentText()
        destinos = self.obtener_destinos_seleccionados()
        if not destinos:
            self.resultado_label.setText("Selecciona al menos un destino.")
            return
        subconjunto = [origen] + [d for d in destinos if d != origen]
        ruta, costo = tsp_backtracking(self.G, subconjunto, origen)
        self.mostrar_ruta(ruta, costo, color='orange', titulo="Ruta Personalizada")

    def mostrar_ruta(self, ruta, costo, color, titulo):
        orden_labels = {ciudad: f"{i+1}" for i, ciudad in enumerate(ruta[:-1])}
        nx.draw_networkx_nodes(self.G, self.pos, node_color='skyblue', node_size=800, ax=self.ax)
        nx.draw_networkx_labels(self.G, self.pos, labels=orden_labels, font_size=12, font_color='black', ax=self.ax)

        offset_ciudades = {
            "Santo Domingo": (0, 0.07),
            "Santiago": (-0.07, 0),
            "La Romana": (0, -0.07),
            "Puerto Plata": (0.07, 0),
            "San Cristóbal": (-0.05, 0.05),
            "San Pedro de Macorís": (0.05, -0.05)
        }
        offset_pos = {c: (self.pos[c][0] + dx, self.pos[c][1] + dy) for c, (dx, dy) in offset_ciudades.items()}
        nx.draw_networkx_labels(self.G, offset_pos, ax=self.ax)

        nx.draw_networkx_edges(self.G, self.pos, edge_color='gray', alpha=0.3, ax=self.ax)
        edges = [(ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1)]
        nx.draw_networkx_edges(self.G, self.pos, edgelist=edges, edge_color=color, width=3, ax=self.ax, arrows=True, arrowstyle='-|>', arrowsize=20)
        edge_labels = {(u, v): self.G[u][v]['weight'] for u, v in edges}
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)
        self.canvas.draw()

        ruta_str = " → ".join(ruta)
        self.resultado_label.setText(f"<b>{titulo}:</b><br>{ruta_str}<br><b>Distancia total:</b> {costo} km")

    def ocultar_lista_destinos(self):
        self.label_destinos.hide()
        self.scroll_destinos.hide()

    def mostrar_lista_destinos(self):
        self.label_destinos.show()
        self.scroll_destinos.show()

    def ocultar_origen(self):
        self.label_origen.hide()
        self.combo_origen.hide()

    def mostrar_origen(self):
        self.label_origen.show()
        self.combo_origen.show()
