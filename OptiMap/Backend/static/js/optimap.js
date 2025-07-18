let rutaPersonalizadaActiva = false;

function mostrarAlert(mensaje, tipo = 'error') {
    const alertContainer = document.getElementById('alertContainer');
    const alertClass = tipo === 'error' ? 'alert-error' : 'alert-success';
    alertContainer.innerHTML = `<div class="alert ${alertClass}">${mensaje}</div>`;
    setTimeout(() => { alertContainer.innerHTML = ''; }, 4000);
}

function mostrarLoading() {
    document.getElementById("loading").style.display = "block";
    document.getElementById("resultados").style.display = "none";
}

function ocultarLoading() {
    document.getElementById("loading").style.display = "none";
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

function toggleRutaPersonalizada() {
    const destinosGroup = document.getElementById('destinosGroup');
    const btnCalcular = document.getElementById('btnCalcularPersonalizada');
    rutaPersonalizadaActiva = !rutaPersonalizadaActiva;
    if (rutaPersonalizadaActiva) {
        destinosGroup.style.display = 'block';
        btnCalcular.style.display = 'block';
        document.querySelectorAll('#destinosGroup input[type="checkbox"]').forEach(cb => { cb.checked = false; });
    } else {
        destinosGroup.style.display = 'none';
        btnCalcular.style.display = 'none';
        limpiarRutas();
    }
}

function validarRutaPersonalizada() {
    const origen = document.getElementById("origen").value;
    const destinos = Array.from(document.querySelectorAll('#destinosGroup input[type="checkbox"]:checked')).map(cb => cb.value);
    if (!origen) {
        mostrarAlert("⚠️ Selecciona una ciudad de origen");
        return false;
    }
    if (destinos.length === 0) {
        mostrarAlert("⚠️ Selecciona al menos un destino");
        return false;
    }
    const ciudadesUnicas = new Set([origen, ...destinos]);
    if (ciudadesUnicas.size < 2) {
        mostrarAlert("⚠️ Necesitas al menos 2 ciudades diferentes para crear una ruta");
        return false;
    }
    return true;
}

function calcularTSP() {
    const origen = document.getElementById("origen").value;
    if (!origen) {
        mostrarAlert("⚠️ Selecciona una ciudad de origen");
        return;
    }
    limpiarRutas();
    mostrarLoading();
    const startTime = performance.now();
    fetch("/api/tsp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ origen: origen })
    })
    .then(res => res.json())
    .then(data => {
        const endTime = performance.now();
        const tiempoCalculo = Math.round(endTime - startTime);
        if (data.error) {
            mostrarAlert(`❌ Error: ${data.error}`);
            ocultarLoading();
            return;
        }
        actualizarResultados(
            "Ruta Óptima (TSP)", 
            `<strong>Ruta:</strong> ${data.ruta.join(' → ')}<br><strong>Distancia:</strong> ${data.distancia} km`, 
            data.distancia, 
            tiempoCalculo, 
            data.ruta.length - 1, 
            "TSP Backtracking", 
            "🚗"
        );
        resaltarRuta(data.ruta, "tsp");
        ocultarLoading();
        mostrarAlert("✅ Ruta óptima calculada exitosamente", "success");
    })
    .catch(err => { 
        console.error(err); 
        mostrarAlert("❌ Error al calcular la ruta"); 
        ocultarLoading(); 
    });
}

function calcularMST() {
    limpiarRutas();
    mostrarLoading();
    const startTime = performance.now();
    fetch("/api/mst")
    .then(res => res.json())
    .then(data => {
        const endTime = performance.now();
        const tiempoCalculo = Math.round(endTime - startTime);
        if (data.error) {
            mostrarAlert(`❌ Error: ${data.error}`);
            ocultarLoading();
            return;
        }
        let conexiones = "<strong>Conexiones:</strong><br>";
        data.aristas.forEach(a => {
            conexiones += `${a.origen} ↔ ${a.destino} (${a.peso} km)<br>`;
        });
        actualizarResultados(
            "Conexión Mínima (MST)", 
            conexiones, 
            data.costo_total, 
            tiempoCalculo, 
            data.aristas.length, 
            "Prim (Greedy)", 
            "🌐"
        );
        // Resaltar aristas del MST
        data.aristas.forEach(a => {
            const edge1 = document.getElementById(`edge-${a.origen}-${a.destino}`);
            const edge2 = document.getElementById(`edge-${a.destino}-${a.origen}`);
            if (edge1) edge1.classList.add("highlighted", "mst");
            if (edge2) edge2.classList.add("highlighted", "mst");
        });
        ocultarLoading();
        mostrarAlert("✅ Árbol de expansión mínima calculado exitosamente", "success");
    })
    .catch(err => { 
        console.error(err); 
        mostrarAlert("❌ Error al calcular el MST"); 
        ocultarLoading(); 
    });
}

function calcularRutaPersonalizada() {
    if (!validarRutaPersonalizada()) {
        return;
    }
    const origen = document.getElementById("origen").value;
    const destinos = Array.from(document.querySelectorAll('#destinosGroup input[type="checkbox"]:checked')).map(cb => cb.value);
    const subconjunto = Array.from(new Set([origen, ...destinos])); // Eliminar duplicados
    limpiarRutas();
    mostrarLoading();
    const startTime = performance.now();
    fetch("/api/tsp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ origen: origen, subconjunto: subconjunto })
    })
    .then(res => res.json())
    .then(data => {
        const endTime = performance.now();
        const tiempoCalculo = Math.round(endTime - startTime);
        if (data.error) {
            mostrarAlert(`❌ Error: ${data.error}`);
            ocultarLoading();
            return;
        }
        actualizarResultados(
            "Ruta Personalizada",
            `<strong>Ruta:</strong> ${data.ruta.join(' → ')}<br><strong>Distancia:</strong> ${data.distancia} km`, 
            data.distancia, 
            tiempoCalculo, 
            subconjunto.length, 
            "TSP Personalizado", 
            "⚙️"
        );
        resaltarRuta(data.ruta, "custom");
        ocultarLoading();
        mostrarAlert("✅ Ruta personalizada calculada exitosamente", "success");
    })
    .catch(err => { 
        console.error(err); 
        mostrarAlert("❌ Error al calcular la ruta personalizada"); 
        ocultarLoading(); 
    });
}
