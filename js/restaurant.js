// restaurant page specific logic

function switchTab(btn, tab) {
  document.querySelectorAll('.rest-tab').forEach(t => t.classList.remove('active-tab'));
  btn.classList.add('active-tab');
}

function activateCat(link) {
  document.querySelectorAll('.menu-cat-link').forEach(l => l.classList.remove('active-cat'));
  link.classList.add('active-cat');
}

function toggleCategory(itemsId) {
  const items = document.getElementById(itemsId);
  const header = items.previousElementSibling;
  if (items.classList.contains('hidden')) {
    items.classList.remove('hidden');
    header.classList.remove('collapsed');
  } else {
    items.classList.add('hidden');
    header.classList.add('collapsed');
  }
}

function filterDishes(query) {
  const q = query.toLowerCase();
  document.querySelectorAll('.menu-item').forEach(item => {
    const name = item.dataset.name || '';
    item.classList.toggle('hidden', q.length > 0 && !name.includes(q));
  });
}

let vegOnly = false;
function toggleVeg() {
  vegOnly = !vegOnly;
  const btn = document.getElementById('vegToggle');
  btn.style.background = vegOnly ? 'var(--green)' : '#fff';
  document.querySelectorAll('.menu-item').forEach(item => {
    if (vegOnly) {
      item.classList.toggle('hidden', item.dataset.type !== 'veg');
    } else {
      item.classList.remove('hidden');
    }
  });
}

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
    addItemToCart(item);
  }
}

function openCustomiseModal(item) {
  currentCustomiseItem = item;
  currentStep = 1;
  selectedCrust = 'Pan';
  selectedSize = 'Personal';
  extraCheese = false;
  renderModalStep();
  document.getElementById('modalOverlay').classList.add('open');
}

function closeCustomiseModal() {
  document.getElementById('modalOverlay').classList.remove('open');
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
          <input type="radio" name="crust" class="custom-radio" value="Pan" ${selectedCrust === 'Pan' ? 'checked' : ''} onchange="selectedCrust='Pan'">
          Pan
        </span>
      </label>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="crust" class="custom-radio" value="Ultimate Cheese" ${selectedCrust === 'Ultimate Cheese' ? 'checked' : ''} onchange="selectedCrust='Ultimate Cheese'">
          Ultimate Cheese
        </span>
      </label>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="crust" class="custom-radio" value="Stuffed Crust - Maxx" ${selectedCrust === 'Stuffed Crust - Maxx' ? 'checked' : ''} onchange="selectedCrust='Stuffed Crust - Maxx'">
          Stuffed Crust - Maxx
        </span>
      </label>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="crust" class="custom-radio" value="Thin n Crispy" ${selectedCrust === 'Thin n Crispy' ? 'checked' : ''} onchange="selectedCrust='Thin n Crispy'">
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
          <input type="radio" name="size" class="custom-radio" value="Personal" ${selectedSize === 'Personal' ? 'checked' : ''} onchange="selectedSize='Personal'">
          Personal
        </span>
        <span>₹${currentCustomiseItem.price}</span>
      </label>
      <label class="option-row">
        <span class="option-left">
          <input type="radio" name="size" class="custom-radio" value="Medium" ${selectedSize === 'Medium' ? 'checked' : ''} onchange="selectedSize='Medium'">
          Medium
        </span>
        <span>₹${currentCustomiseItem.price + 200}</span>
      </label>

      <p class="option-group-title" style="margin-top:20px;">Extra Cheese Topping</p>
      <label class="option-row">
        <span class="option-left">
          <input type="checkbox" class="custom-checkbox" ${extraCheese ? 'checked' : ''} onchange="extraCheese=this.checked">
          Cheese
        </span>
        <span>+ ₹65</span>
      </label>
    `;
  }
}

function finishCustomisation() {
  const itemToAdd = {
    ...currentCustomiseItem,
    name: `${currentCustomiseItem.name} (${selectedSize}, ${selectedCrust})`,
    price: currentCustomiseItem.price + (selectedSize === 'Medium' ? 200 : 0) + (extraCheese ? 65 : 0)
  };
  addToCart(itemToAdd);
  closeCustomiseModal();
  updateFloatingCart();
}

function addItemToCart(item) {
  addToCart(item);
  updateFloatingCart();
}

function updateFloatingCart() {
  const cart = getCart();
  const total = cart.reduce((sum, i) => sum + i.qty, 0);
  const amount = cart.reduce((sum, i) => sum + (i.price * i.qty), 0);
  const fc = document.getElementById('floatingCart');
  if (total > 0) {
    fc.style.display = 'block';
    document.getElementById('fcCount').textContent = total + (total === 1 ? ' item added' : ' items added');
    document.getElementById('fcTotal').textContent = 'VIEW CART 🛍️';
  } else {
    fc.style.display = 'none';
  }
}

// highlight active category on scroll
window.addEventListener('scroll', () => {
  const sections = document.querySelectorAll('.menu-category-block');
  const links = document.querySelectorAll('.menu-cat-link');
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 120) current = s.id;
  });
  links.forEach(l => {
    l.classList.toggle('active-cat', l.getAttribute('href') === '#' + current);
  });
});

document.addEventListener('DOMContentLoaded', () => {
  updateFloatingCart();
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
});
