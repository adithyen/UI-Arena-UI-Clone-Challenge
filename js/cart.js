// cart page - render items from localStorage and handle qty changes

const GST_RATE = 0.18;
const DELIVERY_FEE = 24;

function renderCart() {
  const cart = getCart();
  const wrap = document.getElementById('checkoutWrap');
  const empty = document.getElementById('emptyCart');

  if (!cart || cart.length === 0) {
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
    <div style="display:flex;align-items:center;gap:14px;padding-bottom:14px;margin-bottom:12px;">
      <img src="https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_660/RX_THUMBNAIL/IMAGES/VENDOR/2024/7/16/0e12d591-66a8-4dc8-a89e-99dd6c1c28c8_10575.jpg" alt="Pizza Hut" style="width:50px;height:50px;border-radius:6px;object-fit:cover;">
      <div>
        <h4 style="font-size:17px;font-weight:700;color:#02060c;margin:0;">Pizza Hut</h4>
        <p style="font-size:13px;color:rgba(2,6,12,0.6);margin-top:2px;margin:0;">Palayam</p>
        <div style="width:40px;height:2px;background:#02060c;margin-top:6px;"></div>
      </div>
    </div>
    <div style="border-left:3px solid #02060c;padding-left:10px;margin-bottom:16px;margin-top:14px;">
      <div style="font-size:12px;font-weight:700;color:#02060c;text-transform:uppercase;">FEASTMODE70 eligible items</div>
      <div style="font-size:12px;font-weight:600;color:#02060c;margin-top:2px;">You just saved <strong>₹129</strong> on these items!</div>
    </div>
  `;
}

function renderItems(cart) {
  const el = document.getElementById('orderItems');
  if (!el) return;
  el.innerHTML = cart.map(item => {
    const isVeg = item.type !== 'nonveg';
    const symbolColor = isVeg ? '#0f8a65' : '#e43b4f';
    const innerShape = isVeg 
      ? '<span style="width:6px;height:6px;background:#0f8a65;border-radius:50%;"></span>'
      : '<span style="width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-bottom:7px solid #e43b4f;"></span>';

    return `
      <div id="ci-${item.id}" style="display:flex;align-items:center;justify-content:space-between;padding:12px 0;border-bottom:1px solid #f1f1f6;">
        <div style="display:flex;align-items:center;gap:10px;flex:1;padding-right:10px;">
          <span style="width:14px;height:14px;border:1.5px solid ${symbolColor};display:inline-flex;align-items:center;justify-content:center;border-radius:3px;flex-shrink:0;">
            ${innerShape}
          </span>
          <span style="font-size:13px;font-weight:600;color:#02060c;line-height:1.3;">${item.name}</span>
        </div>
        <div style="display:flex;align-items:center;border:1px solid #bebfc5;padding:3px 8px;font-size:13px;font-weight:600;gap:10px;background:#fff;margin:0 12px;border-radius:4px;">
          <button onclick="changeQty('${item.id}', -1)" style="border:none;background:none;color:#686b78;cursor:pointer;font-weight:700;font-size:14px;padding:0 2px;">−</button>
          <span id="qty-${item.id}" style="color:#60b246;font-weight:700;">${item.qty}</span>
          <button onclick="changeQty('${item.id}', 1)" style="border:none;background:none;color:#60b246;cursor:pointer;font-weight:700;font-size:14px;padding:0 2px;">+</button>
        </div>
        <div style="text-align:right;min-width:65px;">
          <span style="font-size:11px;color:#686b78;text-decoration:line-through;display:block;">₹${Math.round(item.price * 1.35 * item.qty)}</span>
          <span class="ci-price" style="font-weight:700;font-size:14px;color:#02060c;">₹${item.price * item.qty}</span>
        </div>
      </div>
    `;
  }).join('');
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
  updateCartBadge();
  if (cart.length === 0) renderCart();
}

// Execute renderCart immediately
renderCart();

document.addEventListener('DOMContentLoaded', () => {
  renderCart();
  updateCartBadge();
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
});
