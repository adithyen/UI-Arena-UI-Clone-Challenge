// search page js

// reuse restaurant data from main.js
const bgColors = ['#ffb347','#87ceeb','#98fb98','#dda0dd','#f0e68c','#ffa07a','#20b2aa','#ff7f7f','#b0c4de','#8fbc8f','#d2b48c','#bc8f8f','#f4a460','#9370db','#3cb371','#cd853f'];

function handleSearch(query) {
  const clearBtn = document.getElementById('clearBtn');
  const defaultState = document.getElementById('defaultState');
  const resultsSection = document.getElementById('searchResults');

  if (query.trim() === '') {
    clearBtn.style.display = 'none';
    defaultState.style.display = 'block';
    resultsSection.style.display = 'none';
    return;
  }

  clearBtn.style.display = 'block';
  defaultState.style.display = 'none';
  resultsSection.style.display = 'block';

  const q = query.toLowerCase();
  const matches = restaurants.filter(r =>
    r.name.toLowerCase().includes(q) ||
    r.cuisine.toLowerCase().includes(q) ||
    r.area.toLowerCase().includes(q)
  );

  const grid = document.getElementById('resultsGrid');
  if (matches.length === 0) {
    grid.innerHTML = `<div class="no-results" style="grid-column:1/-1"><h3>No results for "${query}"</h3><p>Try searching for something else</p></div>`;
    return;
  }

  grid.innerHTML = matches.map((r, i) => buildRestaurantCard(r, i)).join('');
}

function searchCuisine(cuisine) {
  document.getElementById('searchInput').value = cuisine;
  handleSearch(cuisine);
}

function clearSearch() {
  document.getElementById('searchInput').value = '';
  handleSearch('');
}

// check url param
document.addEventListener('DOMContentLoaded', () => {
  updateCartBadge();
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
  // pre-fill from url param
  const params = new URLSearchParams(window.location.search);
  const q = params.get('q');
  if (q) {
    document.getElementById('searchInput').value = q;
    handleSearch(q);
  }
});
