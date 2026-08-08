// ==========================================================================
// SWIGGY RESTAURANT PAGE - AUTHENTIC 1:1 CONTROLLER LOGIC
// ==========================================================================

let isVegOnly = false;
let isNonVegOnly = false;
let isBestsellerOnly = false;
let searchQuery = '';

// Tab switching (Order Online vs Dineout)
function switchTab(btn, tab) {
  document.querySelectorAll('.sc-gaGBLo.gsSDZP').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
}

// Category Accordion Toggle
function toggleCategoryAccordion(btn) {
  btn.classList.toggle('collapsed');
  const container = btn.parentElement.querySelector('.category-dish-container');
  if (container) {
    container.classList.toggle('collapsed');
  }
}

// Search dishes in restaurant
function handleDishSearch(val) {
  searchQuery = (val || '').toLowerCase().trim();
  applyFilters();
}

// Veg Filter Handler
function handleVegFilter(checked) {
  isVegOnly = checked;
  if (checked) {
    const nonVegCb = document.getElementById('NON_VEG');
    if (nonVegCb) nonVegCb.checked = false;
    isNonVegOnly = false;
  }
  applyFilters();
}

// Non-Veg Filter Handler
function handleNonVegFilter(checked) {
  isNonVegOnly = checked;
  if (checked) {
    const vegCb = document.getElementById('VEG');
    if (vegCb) vegCb.checked = false;
    isVegOnly = false;
  }
  applyFilters();
}

// Bestseller Filter Handler
function toggleBestsellerFilter(btn) {
  isBestsellerOnly = !isBestsellerOnly;
  const chipBtn = btn || document.getElementById('bestsellerBtn');
  if (chipBtn) {
    chipBtn.classList.toggle('active', isBestsellerOnly);
  }
  applyFilters();
}

// Master Filter Function
function applyFilters() {
  const dishRows = document.querySelectorAll('.sc-jiVjYv.gRIQgR');
  dishRows.forEach(row => {
    const type = row.dataset.type; // 'veg' | 'nonveg'
    const name = (row.dataset.name || '').toLowerCase();
    const isBestseller = row.dataset.bestseller === 'true';

    let match = true;

    if (isVegOnly && type !== 'veg') match = false;
    if (isNonVegOnly && type !== 'nonveg') match = false;
    if (isBestsellerOnly && !isBestseller) match = false;
    if (searchQuery && !name.includes(searchQuery)) match = false;

    row.style.display = match ? 'flex' : 'none';
  });
}

// ==========================================================================
// DISH ADD & QUANTITY CONTROLLER LOGIC
// ==========================================================================

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
  if (modal) modal.style.display = 'flex';
}

function closeCustomiseModal() {
  const modal = document.getElementById('modalOverlay');
  if (modal) modal.style.display = 'none';
}

function renderModalStep() {
  const title = document.getElementById('modalItemTitle');
  const body = document.getElementById('modalBody');
  const stepInd = document.getElementById('modalStepIndicator');
  const actionBtn = document.getElementById('modalActionBtn');

  if (!title || !body || !stepInd || !actionBtn) return;

  if (currentStep === 1) {
    title.textContent = `${currentCustomiseItem.name} · ₹${currentCustomiseItem.price}`;
    stepInd.textContent = 'Step 1/2';
    actionBtn.textContent = 'Continue';
    actionBtn.onclick = () => { currentStep = 2; renderModalStep(); };

    body.innerHTML = `
      <p style="font-weight:700; margin-bottom:12px; font-size:14px;">Choose your Crust</p>
      <label style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f0f0f5; cursor:pointer;">
        <span><input type="radio" name="crust" value="Pan" ${selectedCrust === 'Pan' ? 'checked' : ''} onchange="selectedCrust='Pan'"> Pan Crust</span>
      </label>
      <label style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f0f0f5; cursor:pointer;">
        <span><input type="radio" name="crust" value="Ultimate Cheese" ${selectedCrust === 'Ultimate Cheese' ? 'checked' : ''} onchange="selectedCrust='Ultimate Cheese'"> Ultimate Cheese Crust</span>
      </label>
      <label style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f0f0f5; cursor:pointer;">
        <span><input type="radio" name="crust" value="Stuffed Crust" ${selectedCrust === 'Stuffed Crust' ? 'checked' : ''} onchange="selectedCrust='Stuffed Crust'"> Stuffed Crust - Maxx</span>
      </label>
      <label style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; cursor:pointer;">
        <span><input type="radio" name="crust" value="Thin n Crispy" ${selectedCrust === 'Thin n Crispy' ? 'checked' : ''} onchange="selectedCrust='Thin n Crispy'"> Thin n Crispy</span>
      </label>
    `;
  } else {
    stepInd.textContent = 'Step 2/2';
    actionBtn.textContent = 'Add Item to Cart';
    actionBtn.onclick = finishCustomisation;

    body.innerHTML = `
      <div style="background:#f0f0f5; padding:10px 14px; border-radius:8px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center; font-size:13px; font-weight:600;">
        <span>• Crust: ${selectedCrust}</span>
        <button style="border:none; background:none; color:#ff5200; font-weight:700; cursor:pointer;" onclick="currentStep=1; renderModalStep();">Change</button>
      </div>
      <p style="font-weight:700; margin-bottom:12px; font-size:14px;">Choose Size</p>
      <label style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f0f0f5; cursor:pointer;">
        <span><input type="radio" name="size" value="Personal" ${selectedSize === 'Personal' ? 'checked' : ''} onchange="selectedSize='Personal'"> Personal (Serves 1)</span>
        <span style="font-weight:600;">₹${currentCustomiseItem.price}</span>
      </label>
      <label style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f0f0f5; cursor:pointer;">
        <span><input type="radio" name="size" value="Medium" ${selectedSize === 'Medium' ? 'checked' : ''} onchange="selectedSize='Medium'"> Medium (Serves 2)</span>
        <span style="font-weight:600;">₹${currentCustomiseItem.price + 200}</span>
      </label>

      <p style="font-weight:700; margin:16px 0 12px; font-size:14px;">Extra Cheese Topping</p>
      <label style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; cursor:pointer;">
        <span><input type="checkbox" ${extraCheese ? 'checked' : ''} onchange="extraCheese=this.checked"> Extra Mozzarella Cheese</span>
        <span style="font-weight:600;">+ ₹65</span>
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
      const row = document.querySelector(`.sc-jiVjYv.gRIQgR[data-id="${dishId}"]`);
      if (row) {
        const name = row.querySelector('h3').textContent.trim();
        const priceText = row.querySelector('.sc-dlfnOL.cWZrLo').textContent.replace('₹', '').trim();
        const price = parseInt(priceText) || 149;
        const type = row.dataset.type || 'veg';
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

// Update all dish action buttons / counters
function updateDishActionButtons() {
  const cart = getCart();
  const dishRows = document.querySelectorAll('.sc-jiVjYv.gRIQgR');

  dishRows.forEach(row => {
    const dishId = row.dataset.id;
    const container = document.getElementById(`dishAction-${dishId}`);
    if (!container) return;

    const inCart = cart.filter(i => i.id === dishId || (i.id && i.id.startsWith(dishId)));
    const totalQty = inCart.reduce((sum, item) => sum + item.qty, 0);

    if (totalQty > 0) {
      container.innerHTML = `
        <div class="swiggy-qty-counter" style="display:flex; align-items:center; justify-content:space-between; width:100%; height:100%; padding:0 8px;">
          <button class="qty-btn" style="background:none; border:none; color:#1ba672; font-size:18px; font-weight:800; cursor:pointer;" onclick="changeDishQty('${dishId}', -1)">−</button>
          <div class="qty-val" style="font-size:14px; font-weight:800; color:#1ba672;">${totalQty}</div>
          <button class="qty-btn" style="background:none; border:none; color:#1ba672; font-size:18px; font-weight:800; cursor:pointer;" onclick="changeDishQty('${dishId}', 1)">+</button>
        </div>
      `;
    } else {
      const name = row.querySelector('h3').textContent.trim();
      const priceText = row.querySelector('.sc-dlfnOL.cWZrLo').textContent.replace('₹', '').trim();
      const price = parseInt(priceText) || 149;
      const type = row.dataset.type || 'veg';
      const isCustomisable = dishId.startsWith('pizza');

      container.innerHTML = `
        <button class="swiggy-main-add-btn" onclick="handleAddClick({id:'${dishId}',name:'${name}',price:${price},type:'${type}'}, ${isCustomisable})">ADD</button>
      `;
    }
  });
}

// Floating View Cart Green Bar
function updateFloatingCart() {
  const cart = getCart();
  const total = cart.reduce((sum, i) => sum + i.qty, 0);
  const fc = document.getElementById('floatingCart');
  const countText = document.getElementById('fcCountText');

  if (total > 0) {
    if (fc) fc.style.display = 'block';
    if (countText) {
      countText.textContent = total + (total === 1 ? ' item added' : ' items added');
    }
  } else {
    if (fc) fc.style.display = 'none';
  }

  updateCartBadge();
}

// Browse Menu Modal
function toggleBrowseMenuModal() {
  const overlay = document.getElementById('browseMenuOverlay');
  if (overlay) {
    const isVisible = overlay.style.display === 'flex';
    overlay.style.display = isVisible ? 'none' : 'flex';
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

// Sticky header scroll listener
window.addEventListener('scroll', () => {
  const stickyHeader = document.getElementById('stickyRestHeader');
  if (stickyHeader) {
    if (window.scrollY > 340) {
      stickyHeader.classList.add('visible');
    } else {
      stickyHeader.classList.remove('visible');
    }
  }
});

// Deals carousel scroll
function scrollDeals(dir) {
  const container = document.getElementById('dealsScroll');
  if (!container) return;
  const scrollAmount = 300;
  container.scrollBy({ left: dir * scrollAmount, behavior: 'smooth' });
  setTimeout(updateDealArrows, 250);
}

function updateDealArrows() {
  const container = document.getElementById('dealsScroll');
  const prevBtn = document.getElementById('dealPrev');
  const nextBtn = document.getElementById('dealNext');
  if (!container || !prevBtn || !nextBtn) return;

  const isStart = container.scrollLeft <= 5;
  const isEnd = container.scrollLeft + container.clientWidth >= container.scrollWidth - 5;

  if (isStart) {
    prevBtn.setAttribute('disabled', '');
    prevBtn.querySelector('.sc-emrHyn')?.classList.add('sc-kDDaHh', 'iLVdim');
  } else {
    prevBtn.removeAttribute('disabled');
    prevBtn.querySelector('.sc-emrHyn')?.classList.remove('sc-kDDaHh', 'iLVdim');
  }

  if (isEnd) {
    nextBtn.setAttribute('disabled', '');
    nextBtn.querySelector('.sc-emrHyn')?.classList.add('sc-kDDaHh', 'iLVdim');
  } else {
    nextBtn.removeAttribute('disabled');
    nextBtn.querySelector('.sc-emrHyn')?.classList.remove('sc-kDDaHh', 'iLVdim');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateDishActionButtons();
  updateFloatingCart();
  updateDealArrows();

  const dealsScroll = document.getElementById('dealsScroll');
  if (dealsScroll) {
    dealsScroll.addEventListener('scroll', updateDealArrows);
  }

  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
});
