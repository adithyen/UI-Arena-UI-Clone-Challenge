// ==========================================================================
// SWIGGY RESTAURANT PAGE JAVASCRIPT LOGIC
// ==========================================================================

let isVegOnly = false;
let isNonVegOnly = false;
let isBestsellerOnly = false;
let searchQuery = '';

// Tab switching (Order Online vs Dineout)
function switchTab(btn, tab) {
  document.querySelectorAll('.rest-tab-item').forEach(t => t.classList.remove('active-tab'));
  btn.classList.add('active-tab');
}

// Deals carousel scroll
function scrollDeals(direction) {
  const container = document.getElementById('dealsScroll');
  if (container) {
    container.scrollBy({ left: direction * 240, behavior: 'smooth' });
  }
}

// Toggle Category Accordion
function toggleCategorySection(blockId, headerEl) {
  const block = document.getElementById(blockId);
  if (!block) return;
  const isHidden = block.classList.contains('hidden');
  if (isHidden) {
    block.classList.remove('hidden');
    headerEl.classList.remove('collapsed');
  } else {
    block.classList.add('hidden');
    headerEl.classList.add('collapsed');
  }
}

// Filter handlers
function handleVegFilter(checked) {
  isVegOnly = checked;
  if (checked) {
    // Uncheck non-veg if checked
    const nonVegCb = document.getElementById('NON_VEG');
    if (nonVegCb) nonVegCb.checked = false;
    isNonVegOnly = false;
  }
  applyFilters();
}

function handleNonVegFilter(checked) {
  isNonVegOnly = checked;
  if (checked) {
    // Uncheck veg if checked
    const vegCb = document.getElementById('VEG');
    if (vegCb) vegCb.checked = false;
    isVegOnly = false;
  }
  applyFilters();
}

function toggleBestsellerFilter() {
  isBestsellerOnly = !isBestsellerOnly;
  const btn = document.getElementById('bestsellerBtn');
  if (btn) {
    btn.classList.toggle('active', isBestsellerOnly);
  }
  applyFilters();
}

function filterDishes(val) {
  searchQuery = (val || '').toLowerCase().trim();
  applyFilters();
}

function applyFilters() {
  const dishRows = document.querySelectorAll('.dish-item-row');
  dishRows.forEach(row => {
    const type = row.dataset.type; // 'veg' | 'nonveg'
    const name = (row.dataset.name || '').toLowerCase();
    const isBestseller = row.dataset.bestseller === 'true';

    let match = true;

    if (isVegOnly && type !== 'veg') match = false;
    if (isNonVegOnly && type !== 'nonveg') match = false;
    if (isBestsellerOnly && !isBestseller) match = false;
    if (searchQuery && !name.includes(searchQuery)) match = false;

    row.classList.toggle('hidden-by-filter', !match);
  });
}

// ==========================================================================
// DISH ADD & QUANTITY CONTROLLER LOGIC
// ==========================================================================

// Customisation Modal State
let currentCustomiseItem = null;
let currentStep = 1;
let selectedCrust = 'Pan';
let selectedSize = 'Personal';
let extraCheese = false;

function handleAddClick(item, isCustomisable) {
  if (isCustomisable) {
    openCustomiseModal(item);
  } else {
    addItemDirectly(item);
  }
}

function openCustomiseModal(item) {
  currentCustomiseItem = item;
  currentStep = 1;
  selectedCrust = 'Pan';
  selectedSize = 'Personal';
  extraCheese = false;
  renderModalStep();
  const modal = document.getElementById('modalOverlay');
  if (modal) modal.classList.add('open');
}

function closeCustomiseModal() {
  const modal = document.getElementById('modalOverlay');
  if (modal) modal.classList.remove('open');
}

function renderModalStep() {
  const title = document.getElementById('modalItemTitle');
  const body = document.getElementById('modalBody');
  const stepInd = document.getElementById('modalStepIndicator');
  const actionBtn = document.getElementById('modalActionBtn');

  if (currentStep === 1) {
    title.textContent = `${currentCustomiseItem.name} · ₹${currentCustomiseItem.price}`;
    stepInd.textContent = 'Step 1/2';
    actionBtn.textContent = 'Continue';
    actionBtn.onclick = () => { currentStep = 2; renderModalStep(); };

    body.innerHTML = `
      <p class="option-group-title">Choose your Crust</p>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="crust" value="Pan" ${selectedCrust === 'Pan' ? 'checked' : ''} onchange="selectedCrust='Pan'">
          Pan
        </span>
      </label>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="crust" value="Ultimate Cheese" ${selectedCrust === 'Ultimate Cheese' ? 'checked' : ''} onchange="selectedCrust='Ultimate Cheese'">
          Ultimate Cheese
        </span>
      </label>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="crust" value="Stuffed Crust - Maxx" ${selectedCrust === 'Stuffed Crust - Maxx' ? 'checked' : ''} onchange="selectedCrust='Stuffed Crust - Maxx'">
          Stuffed Crust - Maxx
        </span>
      </label>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="crust" value="Thin n Crispy" ${selectedCrust === 'Thin n Crispy' ? 'checked' : ''} onchange="selectedCrust='Thin n Crispy'">
          Thin n Crispy
        </span>
      </label>
    `;
  } else {
    stepInd.textContent = 'Step 2/2';
    actionBtn.textContent = 'Add Item to cart';
    actionBtn.onclick = finishCustomisation;

    body.innerHTML = `
      <div style="background:#f9f9f9; padding:12px 16px; border-radius:8px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">
        <span>• ${selectedCrust}</span>
        <button style="border:none; background:none; color:#fc8019; font-weight:700; cursor:pointer;" onclick="currentStep=1; renderModalStep();">Change</button>
      </div>
      <p class="option-group-title">Choose Size</p>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="size" value="Personal" ${selectedSize === 'Personal' ? 'checked' : ''} onchange="selectedSize='Personal'">
          Personal
        </span>
        <span>₹${currentCustomiseItem.price}</span>
      </label>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="size" value="Medium" ${selectedSize === 'Medium' ? 'checked' : ''} onchange="selectedSize='Medium'">
          Medium
        </span>
        <span>₹${currentCustomiseItem.price + 200}</span>
      </label>

      <p class="option-group-title" style="margin-top:20px;">Extra Cheese Topping</p>
      <label class="option-row">
        <span class="option-left">
          <input type="checkbox" ${extraCheese ? 'checked' : ''} onchange="extraCheese=this.checked">
          Extra Mozzarella Cheese
        </span>
        <span>+ ₹65</span>
      </label>
    `;
  }
}

function finishCustomisation() {
  const itemToAdd = {
    id: currentCustomiseItem.id,
    name: `${currentCustomiseItem.name} (${selectedSize}, ${selectedCrust})`,
    price: currentCustomiseItem.price + (selectedSize === 'Medium' ? 200 : 0) + (extraCheese ? 65 : 0),
    type: currentCustomiseItem.type
  };
  addToCart(itemToAdd);
  closeCustomiseModal();
  updateDishActionButtons();
  updateFloatingCart();
}

function addItemDirectly(item) {
  addToCart(item);
  updateDishActionButtons();
  updateFloatingCart();
}

function changeDishQty(dishId, delta) {
  const cart = getCart();
  const idx = cart.findIndex(i => i.id === dishId || (i.id && i.id.startsWith(dishId)));
  if (idx === -1) {
    if (delta > 0) {
      // Find item details from DOM
      const row = document.querySelector(`.dish-item-row[data-id="${dishId}"]`);
      if (row) {
        const name = row.querySelector('.dish-title-text').textContent;
        const price = parseInt(row.querySelector('.dish-price-text').textContent.replace('₹', ''));
        const type = row.dataset.type;
        addToCart({ id: dishId, name, price, type });
      }
    }
  } else {
    cart[idx].qty += delta;
    if (cart[idx].qty <= 0) {
      cart.splice(idx, 1);
    }
    saveCart(cart);
  }
  updateDishActionButtons();
  updateFloatingCart();
}

// Update all dish ADD buttons / quantity selectors on page based on cart
function updateDishActionButtons() {
  const cart = getCart();
  const dishRows = document.querySelectorAll('.dish-item-row');

  dishRows.forEach(row => {
    const dishId = row.dataset.id;
    const container = document.getElementById(`dishAction-${dishId}`);
    if (!container) return;

    // Find quantity in cart
    const inCart = cart.filter(i => i.id === dishId || (i.id && i.id.startsWith(dishId)));
    const totalQty = inCart.reduce((sum, item) => sum + item.qty, 0);

    if (totalQty > 0) {
      // Render Swiggy interactive counter: [-] [ 1 ] [+]
      container.innerHTML = `
        <div class="sc-dOSQqJ eHMbdb">
          <button class="sc-bZSSRQ sc-jNMdgd eDwJae emzPLX" onclick="changeDishQty('${dishId}', -1)">
            <div class="sc-dlfnOL dIFmud">−</div>
          </button>
          <button direction="stable" class="sc-bZSSRQ sc-bBrNAk eDwJae AowEK">
            <div class="sc-dlfnOL dIFmud">${totalQty}</div>
          </button>
          <button class="sc-bZSSRQ sc-cOahfn eDwJae kyLLdF" onclick="changeDishQty('${dishId}', 1)">
            <div class="sc-dlfnOL dIFmud">+</div>
          </button>
        </div>
      `;
    } else {
      // Render standard Swiggy ADD button
      const name = row.querySelector('.dish-title-text').textContent;
      const price = parseInt(row.querySelector('.dish-price-text').textContent.replace('₹', ''));
      const type = row.dataset.type;

      container.innerHTML = `
        <button class="swiggy-add-btn" onclick="handleAddClick({id:'${dishId}',name:'${name}',price:${price},type:'${type}'}, true)">ADD</button>
      `;
    }
  });
}

// Floating View Cart Green Bar & Menu FAB positioning
function updateFloatingCart() {
  const cart = getCart();
  const total = cart.reduce((sum, i) => sum + i.qty, 0);
  const fc = document.getElementById('floatingCart');
  const countText = document.getElementById('fcCountText');
  const menuFabWrap = document.getElementById('menuFabWrap');

  if (total > 0) {
    if (fc) fc.style.display = 'block';
    if (menuFabWrap) menuFabWrap.classList.add('with-cart');
    if (countText) {
      countText.textContent = total + (total === 1 ? ' item added' : ' items added');
    }
  } else {
    if (fc) fc.style.display = 'none';
    if (menuFabWrap) menuFabWrap.classList.remove('with-cart');
  }

  // Update header cart count
  updateCartBadge();
}

// Browse Menu Modal Handlers
function toggleBrowseMenuModal() {
  const overlay = document.getElementById('browseMenuOverlay');
  if (overlay) {
    overlay.classList.toggle('open');
  }
}

function scrollToCategory(groupId) {
  const el = document.getElementById(groupId);
  if (el) {
    const offset = el.getBoundingClientRect().top + window.pageYOffset - 120;
    window.scrollTo({ top: offset, behavior: 'smooth' });
  }
  toggleBrowseMenuModal();
}

// Sticky top header scroll listener
window.addEventListener('scroll', () => {
  const stickyHeader = document.getElementById('stickyRestHeader');
  if (stickyHeader) {
    if (window.scrollY > 320) {
      stickyHeader.classList.add('visible');
    } else {
      stickyHeader.classList.remove('visible');
    }
  }
});

document.addEventListener('DOMContentLoaded', () => {
  updateDishActionButtons();
  updateFloatingCart();

  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
});

