// Cargar lista inicial
actualizarListaPokemon();

// Eventos de entrada y cambio
document.getElementById('search_input').addEventListener('input', actualizarListaPokemon);
document.getElementById('filter_type').addEventListener('change', actualizarListaPokemon);
document.getElementById('filter_generation').addEventListener('change', actualizarListaPokemon);
document.getElementById('filter_evolution_stage').addEventListener('change', actualizarListaPokemon);

function actualizarListaPokemon() {
    const q = document.getElementById('search_input').value;
    const type = document.getElementById('filter_type').value;
    const generation = document.getElementById('filter_generation').value;
    const evoStage = document.getElementById('filter_evolution_stage').value;

    const params = new URLSearchParams();
    if (q) {
        params.append('q', q);
    }

    if (type) {
        params.append('type', type);
    }

    if (generation) {
        params.append('generation', generation);
    }

    if (evoStage) {
        params.append('evolution_stage', evoStage);
    }

    fetch(`/filter/?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById('pokemon_list');
            lista.innerHTML = '';

            if (data.length === 0) {
                lista.innerHTML = '<p>No se encontraron Pokémon.</p>';
                return;
            }

            data.forEach(p => {
                const card = document.createElement('div');
                card.className = 'pokemon-card';
                card.innerHTML = `
                    <img src="${p.sprite}" alt="${p.name}">
                    <p>#${p.pokedex_id} - ${p.name}</p>
                `;
                lista.appendChild(card);
            });
        });
}

