// Espera a que el documento HTML esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {
    // Obtiene referencias a los elementos del formulario de búsqueda y filtros
    const searchInput = document.getElementById("search-input");
    const typeFilter = document.getElementById("filter-type");
    const genFilter = document.getElementById("filter-generation");
    const evoFilter = document.getElementById("filter-evolution-stage");
    const pokemonList = document.getElementById("pokemon-list");

    // Función que realiza la búsqueda y actualiza la lista de Pokémon
    function fetchFilteredResults() {
        // Obtiene los valores actuales de los campos de filtro
        const q = searchInput.value;
        const type = typeFilter.value;
        const generation = genFilter.value;
        const evolution = evoFilter.value;

        // Crea los parámetros de la URL con los valores recogidos
        const params = new URLSearchParams({
            q,
            type,
            generation,
            evolution_stage: evolution, // Usa este nombre en la consulta al servidor
        });

        // Realiza una petición fetch con los parámetros
        fetch(`?${params.toString()}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest", // Indica que es una petición AJAX
            }
        })
        .then(response => response.text()) // Obtiene la respuesta como texto HTML
        .then(html => {
            // Parsea el HTML de respuesta para extraer solo la parte relevante
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const newList = doc.getElementById("pokemon-list");

            // Reemplaza el contenido actual de la lista si se encuentra el nuevo
            if (newList) {
                pokemonList.innerHTML = newList.innerHTML;
            }
        });
    }

    // Añade listeners a todos los filtros para que actualicen resultados en tiempo real
    [searchInput, typeFilter, genFilter, evoFilter].forEach(element => {
        element.addEventListener("input", fetchFilteredResults); // Al escribir
        element.addEventListener("change", fetchFilteredResults); // Al cambiar selección
    });
});
