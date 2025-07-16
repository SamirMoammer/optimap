// js/optimap.js completo

function mostrarLoading() {
    document.getElementById("loading").classList.add("active");
    document.getElementById("resultados").style.display = "none";
}

function ocultarLoading() {
    document.getElementById("loading").classList.remove("active");
    document.getElementById("resultados").style.display = "block";
}

function actualizarResultados(titulo, contenido, distancia, tiempo, ciudades, algoritmo, icono) {
    document.getElementById("resultTitle").textContent = titulo;
    document.getElementById("resultContent").innerHTML = contenido;
    document.getElementById("distanciaTotal").textContent = distancia;
    document.getElementById("tiempoCalculo").textContent = tiempo;
    document.getElementById("ciudadesVisitadas").textContent = ciudades;
    document.getElementById("algoritmUsado").textContent = algoritmo;
    document.getElementById("resultIcon").textContent = icono;
}

function limpiarRutas() {
    document.querySelectorAll('.edge').forEach(edge => {
        edge.classList.remove("highlighted", "tsp", "mst", "custom");
    });
}

function resaltarRuta(ruta, tipo) {
    limpiarRutas();
    for (let i = 0; i < ruta.length - 1; i++) {
        const origen = ruta[i];
        const destino = ruta[i + 1];
        const edge1 = document.getElementById(`edge-${origen}-${destino}`);
        const edge2 = document.getElementById(`edge-${destino}-${origen}`);
        if (edge1) edge1.classList.add("highlighted", tipo);
        if (edge2) edge2.classList.add("highlighted", tipo);
    }
}

function calcularTSP() {
    const origen = document.getElementById("origen").value;
    if (!origen) {
        alert("Selecciona una ciudad de origen");
        return;
    }
    mostrarLoading();
    fetch("/api/tsp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ origen: origen })
    })
    .then(res => res.json())
    .then(data => {
        actualizarResultados("Ruta Óptima (TSP)", `<strong>Ruta:</strong> ${data.ruta.join(' → ')}<br><strong>Distancia:</strong> ${data.distancia} km`, data.distancia, "45", data.ruta.length, "TSP Backtracking", "🚗");
        resaltarRuta(data.ruta, "tsp");
        ocultarLoading();
    })
    .catch(err => { console.error(err); ocultarLoading(); });
}

function calcularMST() {
    mostrarLoading();
    fetch("/api/mst")
    .then(res => res.json())
    .then(data => {
        let conexiones = "<strong>Conexiones:</strong><br>";
        data.aristas.forEach(a => {
            conexiones += `${a.origen} ↔ ${a.destino} (${a.peso} km)<br>`;
        });
        actualizarResultados("Conexión Mínima (MST)", conexiones, data.costo_total, "12", data.aristas.length, "Prim (Greedy)", "🌐");
        limpiarRutas();
        data.aristas.forEach(a => {
            const edge1 = document.getElementById(`edge-${a.origen}-${a.destino}`);
            const edge2 = document.getElementById(`edge-${a.destino}-${a.origen}`);
            if (edge1) edge1.classList.add("highlighted", "mst");
            if (edge2) edge2.classList.add("highlighted", "mst");
        });
        ocultarLoading();
    })
    .catch(err => { console.error(err); ocultarLoading(); });
}

function rutaPersonalizada() {
    const origen = document.getElementById("origen").value;
    const destinos = Array.from(document.querySelectorAll("#destinosGroup input:checked")).map(cb => cb.value);
    if (!origen) {
        alert("Selecciona ciudad de origen");
        return;
    }
    if (destinos.length === 0) {
        alert("Selecciona al menos un destino");
        return;
    }
    const subconjunto = [origen, ...destinos];
    mostrarLoading();
    fetch("/api/tsp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ origen: origen, subconjunto: subconjunto })
    })
    .then(res => res.json())
    .then(data => {
        actualizarResultados("Ruta Personalizada", `<strong>Ruta:</strong> ${data.ruta.join(' → ')}<br><strong>Distancia:</strong> ${data.distancia} km`, data.distancia, "28", data.ruta.length, "TSP Personalizado", "⚙️");
        resaltarRuta(data.ruta, "custom");
        ocultarLoading();
    })
    .catch(err => { console.error(err); ocultarLoading(); });
}
