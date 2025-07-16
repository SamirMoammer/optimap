from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from grafo import GrafoCiudades
from algoritmos.tsp_backtracking import tsp_backtracking
from algoritmos.prim_greedy import mst_prim

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

grafo_modelo = GrafoCiudades("utils/mapa_ciudades.json")
grafo_modelo.cargar_datos()
G = grafo_modelo.obtener_grafo()
ciudades = grafo_modelo.obtener_ciudades()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/tsp", methods=["POST"])
def calcular_tsp():
    data = request.get_json()
    print("Datos recibidos:", data)

    origen = data.get("origen")
    subconjunto = data.get("subconjunto")
    print("Origen:", origen)
    print("Subconjunto:", subconjunto)

    try:
        if subconjunto:
            subgrafo = G.subgraph(subconjunto).copy()
        else:
            subgrafo = G

        ruta, distancia_total = tsp_backtracking(subgrafo, list(subgrafo.nodes), origen)
        print("Ruta calculada:", ruta)

        return jsonify({
            "ruta": ruta,
            "distancia": distancia_total
        })
    except Exception as e:
        print("Error en calcular_tsp:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/mst", methods=["GET"])
def calcular_mst():
    aristas, costo_total = mst_prim(G)
    resultado = [{"origen": u, "destino": v, "peso": p} for u, v, p in aristas]

    return jsonify({
        "aristas": resultado,
        "costo_total": costo_total
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
