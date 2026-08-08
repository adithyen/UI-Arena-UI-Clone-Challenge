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
    <div style="display:flex;align-items:center;gap:14px;padding-bottom:14px;border-bottom:2px solid #02060c;margin-bottom:16px;">
      <img src="assets/restaurants/pizza-hut.svg" alt="Pizza Hut" style="width:50px;height:50px;border-radius:4px;object-fit:cover;">
      <div>
        <h4 style="font-size:17px;font-weight:600;color:#02060c;">Pizza Hut</h4>
        <p style="font-size:13px;color:rgba(2,6,12,0.6);margin-top:2px;">Palayam</p>
      </div>
    </div>
  `;
}

function renderItems(cart) {
  const el = document.getElementById('orderItems');
  if (!el) return;
  el.innerHTML = cart.map(item => `
    <div id="ci-${item.id}" style="display:flex;align-items:center;justify-content:space-between;padding:10px 0;font-size:14px;color:#02060c;">
      <div style="display:flex;align-items:center;gap:8px;flex:1;">
        <span style="width:12px;height:12px;border:1px solid #1ba672;display:flex;align-items:center;justify-content:center;border-radius:2px;"><span style="width:6px;height:6px;background:#1ba672;border-radius:50%;"></span></span>
        <span style="font-size:13px;font-weight:500;">${item.name}</span>
      </div>
      <div style="display:flex;align-items:center;border:1px solid #bebfc5;padding:3px 8px;font-size:13px;font-weight:600;gap:12px;margin:0 14px;">
        <button onclick="changeQty('${item.id}', -1)" style="border:none;background:none;color:#686b78;cursor:pointer;font-weight:700;font-size:14px;">−</button>
        <span id="qty-${item.id}" style="color:#60b246;font-weight:700;">${item.qty}</span>
        <button onclick="changeQty('${item.id}', 1)" style="border:none;background:none;color:#60b246;cursor:pointer;font-weight:700;font-size:14px;">+</button>
      </div>
      <span class="ci-price" style="font-weight:600;font-size:14px;min-width:50px;text-align:right;">₹${item.price * item.qty}</span>
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
    const row = document.getElementById('ci-' + itemId);
    if (row) row.remove();
  } else {
    const qtyEl = document.getElementById('qty-' + itemId);
    if (qtyEl) qtyEl.textContent = cart[idx].qty;
    const row = document.getElementById('ci-' + itemId);
    if (row) {
      row.querySelector('.ci-price').textContent = '₹' + cart[idx].price * cart[idx].qty;
    }
  }
  saveCart(cart);
  renderBill(cart);
  if (cart.length === 0) renderCart();
}

// Execute renderCart immediately so there is zero delay/flash/collapse
renderCart();

document.addEventListener('DOMContentLoaded', () => {
  renderCart();
  updateCartBadge();
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
});
