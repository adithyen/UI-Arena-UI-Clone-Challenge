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

function addItemToCart(item) {
  addToCart(item);
  updateFloatingCart();
  // flash the add button
  event.target.textContent = '1';
  event.target.classList.add('added');
}

function updateFloatingCart() {
  const cart = getCart();
  const total = cart.reduce((sum, i) => sum + i.qty, 0);
  const amount = cart.reduce((sum, i) => sum + (i.price * i.qty), 0);
  const fc = document.getElementById('floatingCart');
  if (total > 0) {
    fc.style.display = 'block';
    document.getElementById('fcCount').textContent = total + (total === 1 ? ' item' : ' items');
    document.getElementById('fcTotal').textContent = '₹' + amount;
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
