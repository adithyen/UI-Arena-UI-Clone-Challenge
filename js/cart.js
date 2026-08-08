// cart page - render items from localStorage and handle qty changes

const GST_RATE = 0.18;
const DELIVERY_FEE = 24;

function renderCart() {
  const cart = getCart();
  const wrap = document.getElementById('checkoutWrap');
  const empty = document.getElementById('emptyCart');

  if (cart.length === 0) {
    if (wrap) wrap.style.display = 'none';
    if (empty) empty.style.display = 'flex';
    return;
  }

  if (wrap) wrap.style.display = 'flex';
  if (empty) empty.style.display = 'none';

  renderRestaurant();
  renderItems(cart);
  renderBill(cart);
}

function renderRestaurant() {
  const el = document.getElementById('orderRestaurant');
  if (!el) return;
  el.innerHTML = `
    <div class="rest-row">
      <img src="assets/restaurants/pizza-hut.svg" alt="Pizza Hut" class="rest-thumb">
      <div class="rest-row-info">
        <h4>Pizza Hut</h4>
        <p>Palayam</p>
        <div class="rest-underline"></div>
      </div>
    </div>
  `;
}

function renderItems(cart) {
  const el = document.getElementById('orderItems');
  if (!el) return;
  el.innerHTML = cart.map(item => `
    <div class="cart-item" id="ci-${item.id}">
      <span class="ci-veg"></span>
      <span class="ci-name">${item.name}</span>
      <div class="qty-control">
        <button class="qty-btn" onclick="changeQty('${item.id}', -1)">−</button>
        <span class="qty-num" id="qty-${item.id}">${item.qty}</span>
        <button class="qty-btn" onclick="changeQty('${item.id}', 1)">+</button>
      </div>
      <span class="ci-price">₹${item.price * item.qty}</span>
    </div>
  `).join('');
}

function renderBill(cart) {
  const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const gst = Math.round(subtotal * GST_RATE * 100) / 100;
  const total = subtotal + DELIVERY_FEE + gst;

  const el = id => document.getElementById(id);
  if (el('billItemTotal')) el('billItemTotal').textContent = '₹' + subtotal;
  if (el('billGst')) el('billGst').textContent = '₹' + gst.toFixed(2);
  if (el('billTotal')) el('billTotal').textContent = '₹' + total.toFixed(0);
}

function changeQty(itemId, delta) {
  const cart = getCart();
  const idx = cart.findIndex(i => i.id === itemId);
  if (idx === -1) return;
  cart[idx].qty += delta;
  if (cart[idx].qty <= 0) {
    cart.splice(idx, 1);
    // remove row from DOM
    const row = document.getElementById('ci-' + itemId);
    if (row) row.remove();
  } else {
    const qtyEl = document.getElementById('qty-' + itemId);
    if (qtyEl) qtyEl.textContent = cart[idx].qty;
    // update price in row
    const row = document.getElementById('ci-' + itemId);
    if (row) {
      row.querySelector('.ci-price').textContent = '₹' + cart[idx].price * cart[idx].qty;
    }
  }
  saveCart(cart);
  renderBill(cart);
  // if cart is now empty, show empty state
  if (cart.length === 0) renderCart();
}

document.addEventListener('DOMContentLoaded', () => {
  renderCart();
  updateCartBadge();
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
});
