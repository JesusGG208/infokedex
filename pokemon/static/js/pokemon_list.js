document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search_input");
    const typeFilter = document.getElementById("filter_type");
    const genFilter = document.getElementById("filter_generation");
    const evoFilter = document.getElementById("filter_evolution_stage");
    const pokemonList = document.getElementById("pokemon_list");

    function fetchFilteredResults() {
        const q = searchInput.value;
        const type = typeFilter.value;
        const generation = genFilter.value;
        const evolution = evoFilter.value;

        const params = new URLSearchParams({
            q,
            type,
            generation,
            evolution_stage: evolution,
        });

        fetch(`?${params.toString()}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            }
        })
        .then(response => response.text())
        .then(html => {
            // Extraer solo el contenido de #pokemon_list del HTML devuelto
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const newList = doc.getElementById("pokemon_list");
            if (newList) {
                pokemonList.innerHTML = newList.innerHTML;
            }
        });
    }

    // Escucha eventos
    [searchInput, typeFilter, genFilter, evoFilter].forEach(element => {
        element.addEventListener("input", fetchFilteredResults);
        element.addEventListener("change", fetchFilteredResults);
    });
})