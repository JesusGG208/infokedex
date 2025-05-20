document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("search-input");
  const list = document.getElementById("pokemon-list");

  input.addEventListener("input", () => {
    const query = input.value.trim();

    fetch(`/search/?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        list.innerHTML = "";

        data.forEach(pokemon => {
          const item = document.createElement("li");
          const img = document.createElement("img");
          img.src = pokemon.sprite;
          img.alt = pokemon.name;

          const label = document.createElement("strong");
          label.textContent = `${pokemon.pokedex_id} - ${pokemon.name}`;

          item.appendChild(img);
          item.appendChild(label);
          list.appendChild(item);
        });
      })
      .catch(err => {
        console.error("Error fetching Pokémon:", err);
      });
  });
});
