/**
 * Busca Pokémon y muestra el cuadro de resultados si hay coincidencias.
 *
 * @param {string} query - Texto del input de búsqueda.
 */
async function search(query) {
    const resultsBox = document.getElementById("search-results");

    // Oculta el cuadro si el input está vacío
    if (query.length < 1) {
        resultsBox.style.display = "none";
        resultsBox.innerHTML = "";
        return;
    }

    const response = await fetch(`/search/?q=${query}`);
    const results = await response.json();

    if (results.length === 0) {
        resultsBox.style.display = "none";
        resultsBox.innerHTML = "";
        return;
    }

    // Inserta resultados y muestra el cuadro
    resultsBox.innerHTML = results
        .map(p => `<div onclick="location.href='/pokemon_detail/${p.id}/'">${p.name}</div>`)
        .join('');

    resultsBox.style.display = "block"; // Muestra el cuadro
}
