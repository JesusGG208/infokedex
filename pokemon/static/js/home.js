document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-input");
    const results = document.getElementById("search-results");

    input.addEventListener("input", async () => {
        const query = input.value.trim();

        if (query.length === 0) {
            results.style.display = "none";
            results.innerHTML = "";
            return;
        }

        const response = await fetch(`/search/?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.length > 0) {
            results.innerHTML = data.map(p => `
                <a class="search-item" href="/pokemon_detail/${p.pokedex_id}/">
                    <img src="${p.sprite}" alt="${p.name}">
                    <span>${p.name} (#${p.pokedex_id})</span>
                </a>
            `).join("");
            results.style.display = "block";
        } else {
            results.innerHTML = `<div class="search-item">No se encontraron resultados</div>`;
            results.style.display = "block";
        }
    });

    document.addEventListener("click", e => {
        if (!results.contains(e.target) && e.target !== input) {
            results.style.display = "none";
        }
    });
});