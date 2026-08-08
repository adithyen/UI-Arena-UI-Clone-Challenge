import json
import re

# Restaurant metadata
restaurants = [
  { "id": 1, "name": "Pizza Hut", "rating": "4.4 (4.5K+ ratings)", "cost": "₹350 for two", "cuisines": "Pizzas", "time": "25–30 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/6/15/4fc2475d-7187-41ee-b4b5-40c41fba3a94_448001.JPG" },
  { "id": 2, "name": "Hotel Chinnus", "rating": "4.6 (37K+ ratings)", "cost": "₹250 for two", "cuisines": "South Indian, Chinese", "time": "25–30 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/sfqa2q7svnybbjajui58" },
  { "id": 3, "name": "Zam Zam Dosa Hut", "rating": "4.7 (30K+ ratings)", "cost": "₹349 for two", "cuisines": "South Indian, Biryani", "time": "40-50 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/bwqvepdiw71hg3w49you" },
  { "id": 4, "name": "Mother's Veg Plaza", "rating": "4.5 (8K+ ratings)", "cost": "₹200 for two", "cuisines": "South Indian, Kerala", "time": "30–40 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/5/14/abcde_12345.JPG" },
  { "id": 5, "name": "Birdie Bite", "rating": "4.0 (2K+ ratings)", "cost": "₹400 for two", "cuisines": "North Indian, Fast Food", "time": "30–35 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/2/1/birdie_123.jpg" },
  { "id": 6, "name": "The Cake Bros", "rating": "4.3 (1K+ ratings)", "cost": "₹300 for two", "cuisines": "Bakery, Desserts", "time": "25–30 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/3/3/cakebros.jpg" },
  { "id": 7, "name": "Cring Burger", "rating": "4.3 (5K+ ratings)", "cost": "₹350 for two", "cuisines": "Burgers, Fast Food", "time": "45–50 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/4/4/cringburger.jpg" },
  { "id": 8, "name": "Chefette", "rating": "3.8 (1K+ ratings)", "cost": "₹500 for two", "cuisines": "American, Punjabi", "time": "45–55 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/5/5/chefette.jpg" },
  { "id": 9, "name": "Naadan Bhakshanasala", "rating": "4.4 (3K+ ratings)", "cost": "₹250 for two", "cuisines": "Kerala, Indian", "time": "35–40 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/6/6/naadan.jpg" },
  { "id": 10, "name": "CFC Crispy Fried Chicken", "rating": "3.9 (4K+ ratings)", "cost": "₹450 for two", "cuisines": "Burgers, Cafe", "time": "50–60 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/7/7/cfc.jpg" },
  { "id": 11, "name": "Flavours by MMS", "rating": "4.6 (6K+ ratings)", "cost": "₹400 for two", "cuisines": "Chinese, South Indian", "time": "25–30 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/8/8/flavours.jpg" },
  { "id": 12, "name": "The Cozy Cup", "rating": "4.6 (2K+ ratings)", "cost": "₹200 for two", "cuisines": "Cafe, Beverages", "time": "35–40 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/9/9/cozycup.jpg" },
  { "id": 13, "name": "The Imperial Kitchen", "rating": "4.2 (5K+ ratings)", "cost": "₹800 for two", "cuisines": "North Indian, Biryani", "time": "40–50 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/10/10/imperial.jpg" },
  { "id": 14, "name": "Cake Bliss", "rating": "4.5 (3K+ ratings)", "cost": "₹300 for two", "cuisines": "Bakery, Desserts", "time": "30–35 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/11/11/cakebliss.jpg" },
  { "id": 15, "name": "Ambrosia", "rating": "4.1 (1K+ ratings)", "cost": "₹500 for two", "cuisines": "Continental", "time": "35–45 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/12/12/ambrosia.jpg" },
  { "id": 16, "name": "Murfies", "rating": "4.0 (2K+ ratings)", "cost": "₹400 for two", "cuisines": "Burgers, Fast Food", "time": "40–50 mins", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/1/1/murfies.jpg" }
]

chinnus_dishes = [
    {
        "name": "White Chily Chicken (500 Ml)",
        "price": "399",
        "rating": "4.4",
        "rating_count": "(34)",
        "desc": "No Artificial flavours / MSG (Ajinomotto) in any of our food products.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/8c469e5dd0f63240fb95d99923d923b0",
        "veg": False
    },
    {
        "name": "Avocado Shake (300ml)",
        "price": "189",
        "rating": "4.2",
        "rating_count": "(32)",
        "desc": "Avocado milkshake will give you a win-win situation, and it's always better than fizzy drinks.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/7/2/a67a53fe-0c29-4414-a061-24837095460e_6c16b6b4-9755-4679-a456-399ab5d7e69e.jpg",
        "veg": True
    },
    {
        "name": "Butter Beef",
        "price": "399",
        "rating": "3.2",
        "rating_count": "(3)",
        "desc": "Butter Beef is a rich and indulgent dish featuring tender pieces of beef cooked in a creamy, buttery sauce.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/8/23/7f334a75-5773-4146-b13e-7b0333954e80_fef10a16-0bd0-4924-bddf-c4dbc7a81dda.jpg",
        "veg": False
    },
    {
        "name": "Dragon Fried Rice[750ml]",
        "price": "299",
        "rating": "4.7",
        "rating_count": "(16)",
        "desc": "Dragon Fried Rice is a vibrant and flavorful dish that typically combines stir-fried rice with a mix of colorful vegetables.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/9/11/d7f1ae1c-c728-4a53-a26f-03e5f72cd3d3_e2e8bbf1-dd4e-4f9f-925b-c3188322de2b.jpg",
        "veg": False
    },
    {
        "name": "Hong Kong Chicken",
        "price": "399",
        "rating": "4.5",
        "rating_count": "(40)",
        "desc": "Hong Kong Chicken is a flavorful dish often featuring crispy, battered chicken pieces stir-fried.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/9/11/2b3c0a1b-1a17-4dbf-8d3e-4219ffaa09d1_09dfa317-71c9-4946-b22b-17b0c8ccad4e.jpg",
        "veg": False
    },
    {
        "name": "Nawabi Chicken",
        "price": "399",
        "rating": "4.9",
        "rating_count": "(11)",
        "desc": "Nawabi Chicken is a luxurious dish that features tender pieces of chicken cooked in a rich, creamy sauce.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/10/14/d59b64b2-17b8-49a9-9b71-bd7883b9491d_51d279f3-0fcb-46f7-9bda-1e44dd8ee887.jpeg",
        "veg": False
    }
]

zam_zam_dishes = [
    {
        "name": "Mandi Rice",
        "price": "149",
        "rating": "2.8",
        "rating_count": "(4)",
        "desc": "1 Person Mandhi Rice",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/d325b710a96749763294c828ada9641e",
        "veg": True
    },
    {
        "name": "BOILED EGG",
        "price": "25",
        "rating": "4.7",
        "rating_count": "(175)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/5/29/cb2d56ab-f204-4a15-a6ac-ae1bdc363a2d_e3e65e98-a639-4ff9-95f5-4ca1c39fba0f.png",
        "veg": False
    },
    {
        "name": "Cool Blue Crushers",
        "price": "140",
        "rating": "5.0",
        "rating_count": "(133)",
        "desc": "Serve with Bottle",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/xv3t9llqg5m3y3hyd803",
        "veg": True
    },
    {
        "name": "Mountain Crushers",
        "price": "170",
        "rating": "5.0",
        "rating_count": "(49)",
        "desc": "Serve with Bottle",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/drikdddfszvupqgszawx",
        "veg": True
    },
    {
        "name": "Plain Dosa",
        "price": "102",
        "rating": "4.7",
        "rating_count": "(2.0K+)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2025/3/28/ef1e5e25-04b9-44c3-8440-b29f9b6ed7ab_f4a28e1d-fa98-4e67-a1ff-7292922aedd4.jpg",
        "veg": True
    },
    {
        "name": "Ghee Roast Dosa",
        "price": "152",
        "rating": "4.7",
        "rating_count": "(2.5K+)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2025/3/28/ef1e5e25-04b9-44c3-8440-b29f9b6ed7ab_f4a28e1d-fa98-4e67-a1ff-7292922aedd4.jpg",
        "veg": True
    },
    {
        "name": "Masala Dosa",
        "price": "170",
        "rating": "4.7",
        "rating_count": "(3.5K+)",
        "desc": "[Serves 1]",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/72718c1cdb5db4de858344c9e82cbdc0",
        "veg": True
    },
    {
        "name": "Butter Dosa",
        "price": "206",
        "rating": "4.9",
        "rating_count": "(169)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2025/3/28/ce9188f0-b2e2-4db9-b4b4-0c2799c6133e_d904fde6-806a-4aee-b0b2-a10071ffe714.jpg",
        "veg": True
    },
    {
        "name": "Egg Dosa",
        "price": "163",
        "rating": "4.5",
        "rating_count": "(253)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2025/3/28/53501195-dfb2-4dec-b714-460c095b5e17_20022925-b866-4ab7-bb6e-f481cbea6b83.jpg",
        "veg": False
    },
    {
        "name": "Egg Masala Dosa",
        "price": "215",
        "rating": "4.7",
        "rating_count": "(211)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2025/3/28/90e8eddf-6989-4b79-b505-a688ba30816f_a7208a57-6cae-4e31-8b20-45df24d5afc3.jpg",
        "veg": False
    },
    {
        "name": "Cheese Dosa",
        "price": "198",
        "rating": "4.6",
        "rating_count": "(176)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2025/3/28/b9c9c936-8052-4575-8668-c609f1ddfd77_0c111668-b7f7-46a0-ae75-1a3a2462ea37.jpg",
        "veg": True
    }
]

def render_dish(dish, dish_id):
    veg_icon = 'vegVeg16' if dish['veg'] else 'nonvegNonVeg16'
    color = '#116649' if float(dish['rating']) >= 4.0 else '#E6A408'
    veg_str = 'veg' if dish['veg'] else 'nonveg'
    desc_html = f'<div class="sc-fUfliA iGdIQY"><div aria-hidden="true" class="sc-dlfnOL ipuZJn sc-jSUnEA jaouuY">{dish["desc"]}</div></div>' if dish['desc'] else ''
    
    return f"""<div data-testid="normal-dish-item" class="sc-jiVjYv gRIQgR" data-id="dish-{dish_id}" data-name="{dish['name'].lower()}" data-type="{veg_str}" data-bestseller="true">
  <div class="sc-goLLcu jEJsYT">
    <div>
      <div aria-hidden="true" class="sc-eWmBjE bSWzBq">
        <svg viewBox="0 0 20 20" width="16" height="16" class="sc-eWVJoQ cxxFkr">
          <use xlink:href="/food/sprite-0RhsIk92.svg#{veg_icon}"></use>
        </svg>
      </div>
      <h3 aria-hidden="true" class="sc-dlfnOL hJCbXn sc-bxIdbF hEeFlr">{dish['name']}</h3>
      <div class="sc-kYpOdn gRmCvj">
        <div aria-hidden="true" class="sc-jSgsbC ewmHof">
          <span class="sc-eCsseJ kiCBpN"><div class="sc-dlfnOL cWZrLo">₹{dish['price']}</div></span>
        </div>
      </div>
      <div class="sc-jDWblu ciPLFu">
        <div class="sc-eeLFso bPRWxu">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" role="img">
            <path d="M5.67163 3.99166C6.22068 2.34179 6.49521 1.51686 7 1.51686C7.50479 1.51686 7.77932 2.34179 8.32837 3.99166L8.65248 4.96556H9.60668C11.4122 4.96556 12.315 4.96556 12.4703 5.45302C12.6256 5.94049 11.8893 6.4628 10.4167 7.50744L9.67376 8.03444L9.97544 8.94095C10.5325 10.615 10.8111 11.452 10.4033 11.754C9.99553 12.056 9.27604 11.5457 7.83705 10.5249L7 9.93112L6.16295 10.5249C4.72396 11.5457 4.00447 12.056 3.5967 11.754C3.18893 11.452 3.46747 10.615 4.02456 8.94095L4.04557 8.87783C4.18081 8.47145 4.24843 8.26825 4.18684 8.08006C4.12525 7.89187 3.94958 7.76725 3.59824 7.51802C2.11566 6.46633 1.37437 5.94049 1.52971 5.45302C1.68504 4.96556 2.5878 4.96556 4.39332 4.96556H5.34752L5.67163 3.99166Z" fill="{color}"></path>
          </svg>
        </div>
        <div class="sc-dlfnOL fpLIrj sc-kYpsJR bzekZl">{dish['rating']}</div>
        <div class="sc-dlfnOL pDfZF sc-kYpsJR lhLgBz">{dish['rating_count']}</div>
      </div>
      {desc_html}
    </div>
    <div aria-hidden="true" class="sc-jmAvkx PgoaT">
      <button aria-label="See more information" class="sc-iUeFge fxIkFp" style="background: rgb(246, 230, 233);">
        <img alt="{dish['name']}" class="_3XS7H" height="144" loading="lazy" width="156" src="{dish['img']}">
      </button>
      <div class="sc-fXJWTj goDnKo">
        <div style="position: relative;">
          <div class="sc-cBNeAB hIFViE">
            <div class="sc-jcVbNL dfmBqs">
              <button class="swiggy-main-add-btn" onclick="openCustomiseModal(this, '{dish['name']}', '{dish['price']}')">ADD</button>
              <div class="swiggy-qty-counter" style="display: none;">
                <button class="sc-bZSSRQ sc-eggOvH eDwJae qty-btn" onclick="handleQtyChange(this, -1)">−</button>
                <div class="sc-dlfnOL qty-val">1</div>
                <button class="sc-bZSSRQ sc-cTkvqA eDwJae qty-btn" onclick="handleQtyChange(this, 1)">+</button>
              </div>
            </div>
            <div class="sc-dlfnOL kOObuW">Customisable</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>"""

with open('restaurant.html', 'r', encoding='utf-8') as f:
    template = f.read()

for r in restaurants:
    if r['id'] == 1:
        continue
    
    html = template
    html = html.replace('Pizza Hut', r['name'])
    html = html.replace('4.4 (4.5K+ ratings)', r['rating'])
    html = html.replace('₹350 for two', r['cost'])
    
    # replace the cuisines.
    new_cuisines = '&nbsp;'.join([f'<a href="#"><div class="sc-dlfnOL cgFCGx sc-bOSqUZ crkxAI">{c.strip()}</div></a>' for c in r['cuisines'].split(',')])
    html = re.sub(r'<a href="search\.html\?q=pizzas"><div class="sc-dlfnOL cgFCGx sc-bOSqUZ crkxAI">Pizzas</div></a>', new_cuisines, html)
    
    # replace cover image
    html = re.sub(r'https://media-assets\.swiggy\.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/6/15/4fc2475d-7187-41ee-b4b5-40c41fba3a94_448001\.JPG', r['cover'], html)
    
    # Target dishes container
    target_dishes = None
    if r['id'] == 2:
        target_dishes = chinnus_dishes
    elif r['id'] == 3:
        target_dishes = zam_zam_dishes

    if target_dishes:
        dishes_html = '\n'.join([render_dish(d, idx) for idx, d in enumerate(target_dishes)])
        
        # Replace recItemsBlock content
        marker1 = '<div class="category-dish-container" id="recItemsBlock">'
        marker2 = '<!-- Exact Swiggy Menu FAB'
        
        if marker1 in html and marker2 in html:
            idx1 = html.find(marker1) + len(marker1)
            idx2 = html.find(marker2)
            
            # Find the closing tags right before marker2
            prefix = html[:idx1]
            suffix = html[idx2:]
            
            html = prefix + '\n' + dishes_html + '\n</div></div></div></div>\n' + suffix
            print(f"Successfully injected dishes for restaurant {r['id']} ({r['name']})")
        else:
            print(f"Could not find markers for restaurant {r['id']}")

    filename = f'restaurant{r["id"]}.html'
    with open(filename, 'w', encoding='utf-8') as out:
        out.write(html)
        
print("Regenerated restaurant HTML files successfully.")
