// ==========================================================================
// SWIGGY SEARCH SECTION JAVASCRIPT LOGIC
// ==========================================================================

let currentSearchTab = 'restaurants';

function handleSearch(query) {
  const clearBtn = document.getElementById('clearBtn');
  const magnifier = document.getElementById('searchMagnifier');
  const defaultState = document.getElementById('defaultState');
  const resultsSection = document.getElementById('searchResults');
  const searchInput = document.getElementById('searchInput');

  const q = (query || '').trim().toLowerCase();

  if (q === '') {
    if (clearBtn) clearBtn.style.display = 'none';
    if (magnifier) magnifier.style.display = 'flex';
    if (defaultState) defaultState.style.display = 'block';
    if (resultsSection) resultsSection.style.display = 'none';
    return;
  }

  if (clearBtn) clearBtn.style.display = 'flex';
  if (magnifier) magnifier.style.display = 'none';
  if (defaultState) defaultState.style.display = 'none';
  if (resultsSection) resultsSection.style.display = 'block';

  renderSearchResults(q);
}

function switchSearchTab(tab) {
  currentSearchTab = tab;
  document.getElementById('tabRestaurants').classList.toggle('active', tab === 'restaurants');
  document.getElementById('tabDishes').classList.toggle('active', tab === 'dishes');
  const query = document.getElementById('searchInput').value;
  renderSearchResults(query.trim().toLowerCase());
}

function renderSearchResults(q) {
  const grid = document.getElementById('resultsGrid');
  if (!grid) return;

  const matches = (typeof restaurants !== 'undefined' ? restaurants : []).filter(r =>
    r.name.toLowerCase().includes(q) ||
    r.cuisine.toLowerCase().includes(q) ||
    r.area.toLowerCase().includes(q)
  );

  if (matches.length === 0) {
    grid.innerHTML = `
      <div class="no-results-box">
        <div class="no-results-title">No matching ${currentSearchTab} found</div>
        <div class="no-results-sub">Try searching for "Pizza", "Biryani", "Burger", or "Cake"</div>
      </div>
    `;
    return;
  }

  if (currentSearchTab === 'restaurants') {
    grid.innerHTML = matches.map(r => `
      <a href="restaurant.html" class="search-rest-card">
        <div class="search-card-img-wrap">
          <img src="${r.img}" alt="${r.name}" class="search-card-img" onerror="this.src='assets/food-categories.jpg'">
        </div>
        <div class="search-card-info">
          <h4 class="search-card-name">${r.name}</h4>
          <div class="search-card-meta">
            <span class="search-star-badge">★ ${r.rating}</span>
            <span>•</span>
            <span>${r.time}</span>
            <span>•</span>
            <span>${r.price}</span>
          </div>
          <div class="search-card-cuisines">${r.cuisine}</div>
          <div class="search-card-area">${r.area}</div>
        </div>
      </a>
    `).join('');
  } else {
    // Dishes tab view
    grid.innerHTML = matches.map(r => `
      <a href="restaurant.html" class="search-rest-card">
        <div class="search-card-img-wrap">
          <img src="${r.img}" alt="${r.name}" class="search-card-img" onerror="this.src='assets/food-categories.jpg'">
        </div>
        <div class="search-card-info">
          <h4 class="search-card-name">${r.name} Special Dish</h4>
          <div class="search-card-meta">
            <span>By ${r.name}</span>
            <span>•</span>
            <span>${r.price}</span>
          </div>
          <div class="search-card-cuisines">${r.cuisine}</div>
          <div class="search-card-area">${r.area}</div>
        </div>
      </a>
    `).join('');
  }
}

function searchCuisine(cuisine) {
  const input = document.getElementById('searchInput');
  if (input) {
    input.value = cuisine;
    handleSearch(cuisine);
    input.focus();
  }
}

function clearSearch() {
  const input = document.getElementById('searchInput');
  if (input) {
    input.value = '';
    handleSearch('');
    input.focus();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (typeof updateCartBadge === 'function') updateCartBadge();
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });

  const params = new URLSearchParams(window.location.search);
  const q = params.get('q');
  if (q) {
    const input = document.getElementById('searchInput');
    if (input) {
      input.value = q;
      handleSearch(q);
    }
  }
});
