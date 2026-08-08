// cart data - stored in localStorage
const CART_KEY = 'swiggy_cart';

function getCart() {
  try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; }
  catch { return []; }
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartBadge();
}

function addToCart(item) {
  const cart = getCart();
  const existing = cart.find(i => i.id === item.id);
  if (existing) {
    existing.qty++;
  } else {
    cart.push({ ...item, qty: 1 });
  }
  saveCart(cart);
}

function updateCartBadge() {
  const cart = getCart();
  const total = cart.reduce((sum, i) => sum + i.qty, 0);
  const badge = document.getElementById('cartCount');
  if (badge) badge.textContent = total;
}

// restaurant data
const restaurants = [
  { id: 1, name: 'Pizza Hut', img: 'assets/restaurants/pizza-hut.jpg', rating: 4.4, time: '25–30 mins', cuisine: 'Pizzas', area: 'Palayam', offer: '50% OFF' },
  { id: 2, name: 'Hotel Chinnus', img: 'assets/restaurants/hotel-chinnus.jpg', rating: 4.6, time: '25–30 mins', cuisine: 'South Indian, Chinese, Fast Food', area: 'Kesavadasapuram', offer: 'ITEMS AT ₹99' },
  { id: 3, name: 'Zam Zam Dosa Hut', img: 'assets/restaurants/zam-zam.jpg', rating: 4.7, time: '25–30 mins', cuisine: 'South Indian, Biryani, Chinese', area: 'YMR Jn', offer: '₹40 OFF ABOVE ₹499' },
  { id: 4, name: "Mother's Veg Plaza", img: 'assets/restaurants/mothers-veg.jpg', rating: 4.5, time: '30–40 mins', cuisine: 'South Indian, Kerala, Chinese', area: 'Palayam', offer: 'ITEMS AT ₹125' },
  { id: 5, name: 'Birdie Bite', img: 'assets/restaurants/birdie-bite.jpg', rating: 4.0, time: '30–35 mins', cuisine: 'North Indian, Chinese, Fast Food', area: 'Palayam', offer: 'ITEMS AT ₹105' },
  { id: 6, name: 'The Cake Bros', img: 'assets/restaurants/cake-bros.jpg', rating: 4.3, time: '25–30 mins', cuisine: 'Indian', area: 'Eanchakkal', offer: 'ITEMS AT ₹129' },
  { id: 7, name: 'Cring Burger', img: 'assets/restaurants/cring-burger.jpg', rating: 4.3, time: '45–50 mins', cuisine: 'Burgers, Cafe', area: 'Ulloor', offer: '70% OFF UPTO ₹130' },
  { id: 8, name: 'Chefette', img: 'assets/restaurants/chefette.jpg', rating: 2.7, time: '45–55 mins', cuisine: 'American, Continental, Punjabi', area: 'Medical College', offer: '50% OFF UPTO ₹100' },
  { id: 9, name: 'Naadan Bhakshanasala', img: 'assets/restaurants/naadan.jpg', rating: 4.4, time: '35–40 mins', cuisine: 'Kerala, Indian, Curry Point', area: 'Pappanamcode', offer: '60% OFF UPTO ₹120' },
  { id: 10, name: 'CFC Crispy Fried Chicken', img: 'assets/restaurants/cfc.jpg', rating: 3.7, time: '50–60 mins', cuisine: 'Juices, Pastas, Burgers, Cafe', area: 'Poojapura', offer: 'ITEMS AT ₹99' },
  { id: 11, name: 'Flavours by MMS', img: 'assets/restaurants/flavours.jpg', rating: 4.6, time: '25–30 mins', cuisine: 'Chinese, South Indian, North Indian', area: 'Pattoor', offer: '' },
  { id: 12, name: 'The Cozy Cup', img: 'assets/restaurants/cozy-cup.jpg', rating: 4.6, time: '35–40 mins', cuisine: 'Juices, Salads, Snacks, Home Food', area: 'Kamaleshwaram', offer: '20% OFF UPTO ₹125' },
  { id: 13, name: 'The Imperial Kitchen', img: 'assets/restaurants/imperial.jpg', rating: 4.2, time: '40–50 mins', cuisine: 'North Indian, Biryani, Kebabs', area: 'Pattom', offer: '₹40 OFF ABOVE ₹99' },
  { id: 14, name: 'Cake Bliss', img: 'assets/restaurants/cake-bliss.jpg', rating: 4.5, time: '30–35 mins', cuisine: 'Bakery, Desserts, Cakes', area: 'Kowdiar', offer: '' },
  { id: 15, name: 'Ambrosia', img: 'assets/restaurants/ambrosia.jpg', rating: 4.1, time: '35–45 mins', cuisine: 'Multi-cuisine, Continental', area: 'Sasthamangalam', offer: 'ITEMS AT ₹125' },
  { id: 16, name: 'Murfies', img: 'assets/restaurants/murfies.jpg', rating: 4.0, time: '40–50 mins', cuisine: 'Burgers, Sandwiches, Fast Food', area: 'Peroorkada', offer: '' },
];

// img color fallbacks
const colors = ['#ffb347','#87ceeb','#98fb98','#dda0dd','#f0e68c','#ffa07a','#20b2aa','#ff7f7f','#b0c4de','#8fbc8f','#d2b48c','#bc8f8f'];

function buildRestaurantCard(r, idx) {
  const bgColor = colors[idx % colors.length];
  return `
    <a href="restaurant.html" class="rest-card" id="rest-${r.id}">
      <div class="card-img-wrap" style="background:${bgColor}">
        <img src="${r.img}" alt="${r.name}" loading="lazy" onerror="this.style.display='none'">
        ${r.offer ? `<div class="card-offer-tag">${r.offer}</div>` : ''}
      </div>
      <p class="card-name">${r.name}</p>
      <p class="card-meta"><span class="rating-star">★</span> ${r.rating} · ${r.time}</p>
      <p class="card-sub">${r.cuisine}</p>
      <p class="card-loc">${r.area}</p>
    </a>
  `;
}

// category slider state
let catOffset = 0;
const CAT_STEP = 3; // items per scroll

function slideCat(dir) {
  const slider = document.getElementById('catSlider');
  if (!slider) return;
  const items = slider.querySelectorAll('.cat-item');
  const maxOffset = Math.max(0, items.length - 7);
  catOffset = Math.max(0, Math.min(maxOffset, catOffset + dir * CAT_STEP));
  const itemW = items[0].offsetWidth + 16;
  slider.style.transform = `translateX(-${catOffset * itemW}px)`;
  document.getElementById('catPrev').disabled = catOffset === 0;
  document.getElementById('catNext').disabled = catOffset >= maxOffset;
}

// chain slider state
let chainOffset = 0;
const CHAIN_STEP = 1;

function slideChain(dir) {
  const slider = document.getElementById('chainSlider');
  if (!slider) return;
  const cards = slider.querySelectorAll('.chain-card');
  const maxOffset = Math.max(0, cards.length - 4);
  chainOffset = Math.max(0, Math.min(maxOffset, chainOffset + dir * CHAIN_STEP));
  const cardW = cards[0].offsetWidth + 20;
  slider.style.transform = `translateX(-${chainOffset * cardW}px)`;
  document.getElementById('chainPrev').disabled = chainOffset === 0;
  document.getElementById('chainNext').disabled = chainOffset >= maxOffset;
}

// sign in drawer
function openSignIn() {
  document.getElementById('signinDrawer').classList.add('open');
  document.getElementById('drawerOverlay').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeSignIn() {
  document.getElementById('signinDrawer').classList.remove('open');
  document.getElementById('drawerOverlay').classList.remove('active');
  document.body.style.overflow = '';
}

function handleLogin() {
  const phone = document.getElementById('phoneInput').value;
  if (phone.length < 10) {
    alert('Enter a valid 10-digit phone number');
    return;
  }
  alert('OTP sent to ' + phone);
}

// init on load
document.addEventListener('DOMContentLoaded', () => {
  // render restaurant grid if on homepage
  const grid = document.getElementById('restaurantsGrid');
  if (grid) {
    grid.innerHTML = restaurants.map((r, i) => buildRestaurantCard(r, i)).join('');
  }
  // cart badge
  updateCartBadge();
  // sign in btn
  const signInBtn = document.getElementById('signInBtn');
  if (signInBtn) signInBtn.addEventListener('click', e => { e.preventDefault(); openSignIn(); });
  // init slider button states
  setTimeout(() => {
    slideCat(0); slideChain(0);
  }, 100);
});
