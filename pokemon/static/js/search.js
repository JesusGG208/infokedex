// Función para buscar Pokémon
function search(query) {
    const searchResults = document.getElementById('search-results');

    if (query.length < 2) {
        searchResults.classList.remove('active');
        return;
    }

    fetch(`/api/pokemon/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                let html = '';
                data.forEach(pokemon => {
                    html += `
                        <div class="search-result-item" onclick="window.location.href='/pokemon/${pokemon.id}'">
                            <img src="${pokemon.sprite}" alt="${pokemon.name}">
                            <span>${pokemon.name}</span>
                            <span class="text-muted">#${pokemon.pokedex_id.toString().padStart(3, '0')}</span>
                        </div>
                    `;
                });
                searchResults.innerHTML = html;
                searchResults.classList.add('active');
            } else {
                searchResults.innerHTML = '<div class="search-result-item">No se encontraron resultados</div>';
                searchResults.classList.add('active');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            searchResults.classList.remove('active');
        });
}

// Cerrar resultados al hacer clic fuera
document.addEventListener('click', function(event) {
    const searchResults = document.getElementById('search-results');
    const searchInput = document.getElementById('search-input');

    if (event.target !== searchInput && !searchInput.contains(event.target)) {
        searchResults.classList.remove('active');
    }
});

// Manejar navegación con teclado en resultados
document.getElementById('search-input').addEventListener('keydown', function(e) {
    const searchResults = document.getElementById('search-results');
    const items = searchResults.querySelectorAll('.search-result-item');
    let currentFocus = -1;

    if (e.key === 'ArrowDown') {
        e.preventDefault();
        currentFocus++;
        if (currentFocus >= items.length) currentFocus = 0;
        setActive(items);
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        currentFocus--;
        if (currentFocus < 0) currentFocus = items.length - 1;
        setActive(items);
    } else if (e.key === 'Enter' && currentFocus > -1) {
        e.preventDefault();
        items[currentFocus].click();
    }
});

function setActive(items) {
    if (!items || items.length === 0) return;

    items.forEach(item => {
        item.classList.remove('active');
    });

    items[currentFocus].classList.add('active');
    items[currentFocus].scrollIntoView({
        block: 'nearest'
    });
}