// Espera a que el documento HTML esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
    // Obtiene el input de búsqueda y el contenedor de resultados del DOM
    const input = document.getElementById("search-input");
    const results = document.getElementById("search-results");

    // Agrega un evento cuando el usuario escribe en el input
    input.addEventListener("input", async () => {
        const query = input.value.trim(); // Elimina espacios en blanco al inicio y final

        // Si no hay texto, oculta y limpia los resultados
        if (query.length === 0) {
            results.style.display = "none";
            results.innerHTML = "";
            return;
        }

        // Realiza una petición al servidor con la búsqueda
        const response = await fetch(`/search/?q=${encodeURIComponent(query)}`);
        const data = await response.json(); // Convierte la respuesta en JSON

        // Si se encontraron resultados, los muestra en el contenedor
        if (data.length > 0) {
            results.innerHTML = data.map(p => `
                <a class="search-item" href="/pokemon_detail/${p.pokedex_id}/">
                    <img src="${p.sprite}" alt="${p.name}">
                    <span>${p.name} (#${p.pokedex_id})</span>
                </a>
            `).join("");
            results.style.display = "block"; // Muestra el contenedor de resultados
        } else {
            // Si no hay resultados, muestra un mensaje
            results.innerHTML = `<div class="search-item">No se encontraron resultados</div>`;
            results.style.display = "block";
        }
    });

    // Oculta los resultados si se hace clic fuera del input o de los resultados
    document.addEventListener("click", e => {
        if (!results.contains(e.target) && e.target !== input) {
            results.style.display = "none";
        }
    });
});
