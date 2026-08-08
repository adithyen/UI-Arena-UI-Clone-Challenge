import json
import re

# Restaurant metadata
restaurants = [
  { "id": 1, "name": "Pizza Hut", "rating": "4.4 (4.5K+ ratings)", "cost": "₹350 for two", "cuisines": "Pizzas", "time": "25–30 mins", "location": "Thiruvananthapuram", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/RX_THUMBNAIL/IMAGES/VENDOR/2026/6/15/4fc2475d-7187-41ee-b4b5-40c41fba3a94_448001.JPG" },
  { "id": 2, "name": "Hotel Chinnus", "rating": "4.6 (37K+ ratings)", "cost": "₹250 for two", "cuisines": "South Indian, Chinese", "time": "25–30 mins", "location": "Thiruvananthapuram", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/sfqa2q7svnybbjajui58" },
  { "id": 3, "name": "Zam Zam Dosa Hut", "rating": "4.7 (30K+ ratings)", "cost": "₹349 for two", "cuisines": "South Indian, Biryani", "time": "40-50 mins", "location": "YMR Jn", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/bwqvepdiw71hg3w49you" },
  { "id": 4, "name": "Mother's Veg Plaza", "rating": "4.5 (8K+ ratings)", "cost": "₹200 for two", "cuisines": "South Indian, Kerala", "time": "30–40 mins", "location": "Palayam", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/sfqa2q7svnybbjajui58" },
  { "id": 5, "name": "Birdie Bite", "rating": "4.0 (2K+ ratings)", "cost": "₹400 for two", "cuisines": "North Indian, Fast Food", "time": "30–35 mins", "location": "Palayam", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/bwqvepdiw71hg3w49you" },
  { "id": 6, "name": "The Cake Bros", "rating": "4.3 (1K+ ratings)", "cost": "₹300 for two", "cuisines": "Bakery, Desserts", "time": "25–30 mins", "location": "Eanchakkal", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/sfqa2q7svnybbjajui58" },
  { "id": 7, "name": "Cring Burger", "rating": "4.3 (5K+ ratings)", "cost": "₹350 for two", "cuisines": "Burgers, Fast Food", "time": "45–50 mins", "location": "Thiruvananthapuram", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/bwqvepdiw71hg3w49you" },
  { "id": 8, "name": "Chefette", "rating": "2.7 (4 ratings)", "cost": "₹299 for two", "cuisines": "American, Continental", "time": "45-55 mins", "location": "Medical College", "cover": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_1600,h_640,c_fill/sfqa2q7svnybbjajui58" }
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

mothers_veg_dishes = [
    {
        "name": "1 Butter Naan With Paneer Kadhai (combo)",
        "price": "165",
        "rating": "4.2",
        "rating_count": "(15)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Palak Paneer (combo)",
        "price": "155",
        "rating": "4.1",
        "rating_count": "(9)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Paneer Chilly (combo)",
        "price": "165",
        "rating": "5.0",
        "rating_count": "(3)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Paneer Masala (combo)",
        "price": "145",
        "rating": "4.7",
        "rating_count": "(9)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Veg Kurma (combo)",
        "price": "115",
        "rating": "5.0",
        "rating_count": "(4)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Aloo Gobi (combo)",
        "price": "125",
        "rating": "4.0",
        "rating_count": "(5)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Aloo Masala (combo)",
        "price": "105",
        "rating": "3.8",
        "rating_count": "(4)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Aloo Mutter (combo)",
        "price": "125",
        "rating": "4.5",
        "rating_count": "(6)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Dal Tadka (combo)",
        "price": "110",
        "rating": "3.5",
        "rating_count": "(3)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    },
    {
        "name": "1 Butter Naan With Mix Veg Curry (combo)",
        "price": "115",
        "rating": "4.3",
        "rating_count": "(7)",
        "desc": "Curry/Masala served on 250 ml container",
        "img": "",
        "veg": True
    }
]

birdie_bite_dishes = [
    {
        "name": "Oats Upma",
        "price": "249",
        "rating": "4.0",
        "rating_count": "(21)",
        "desc": "A wholesome and flavorful vegetarian twist on a classic Indian breakfast favorite, perfect for a satisfying and nutritious meal.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/26/ebef1250-0237-437f-a1c2-2961f612c7ed_87ffff00-250f-4730-88bb-5d6b8bb4ec41.JPG",
        "veg": True
    },
    {
        "name": "Dal Khichidi [450Ml]",
        "price": "249",
        "rating": "3.3",
        "rating_count": "(6)",
        "desc": "| Serve 1 | Medium spicy | This gently flavoured khichadi, tempered with a ghee tadka is a powerhouse of protein- served with papad and pickle |",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2025/4/1/72d2953b-2a6d-41ad-aa37-bf04db7a3096_8f9d4506-b9d5-438d-83a1-a303f148c9d7.jpg",
        "veg": True
    },
    {
        "name": "Garlic Khichdi",
        "price": "249",
        "rating": "4.9",
        "rating_count": "(3)",
        "desc": "| Serve 1 | Medium spicy | This popular Khichadi is the most delicious way in which you can reap the innumerable health benefits of garlic | Served with Papad |",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/18/23c6f24e-e362-4911-a7e4-0fe71dcd7128_b8ffbd99-15ce-453c-957b-835ece19d1e0.JPG",
        "veg": True
    },
    {
        "name": "Sunny Side Up",
        "price": "129",
        "rating": "2.1",
        "rating_count": "(3)",
        "desc": "A delightful classic featuring perfectly cooked eggs that are simply irresistible.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/b93936d8b9fc5ce6b8b06113dca783ad",
        "veg": False
    },
    {
        "name": "Cheese Omlet",
        "price": "139",
        "rating": "2.8",
        "rating_count": "(4)",
        "desc": "A delectable and savory delight with a rich and creamy filling, perfect for a quick and satisfying bite.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/29/ef1c1a74-64af-4ba3-8b42-84f7184e3976_bf9f0693-373e-42c0-a02f-25db43234d81.JPG",
        "veg": True
    },
    {
        "name": "Nuggets ( 8pcs)",
        "price": "147",
        "rating": "4.2",
        "rating_count": "(8)",
        "desc": "Crispy and flavorful bites that will surely satisfy your cravings.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/9/11/71059e9e-289d-41a0-b6ff-45f3a9b14b1b_b7b655a7-c364-4bed-918e-a50f6ce69f29.jpg",
        "veg": False
    },
    {
        "name": "Classic Paneer Maggi",
        "price": "147",
        "rating": "4.4",
        "rating_count": "(11)",
        "desc": "Indulge in a timeless favorite, loaded with delightful flavors, perfect for a quick and satisfying bite.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/18/f8267abc-d0bf-45c7-a2da-6e94ac316bb6_754ce4a5-c2e8-4c87-89b6-63eff5c7bcec.JPG",
        "veg": True
    },
    {
        "name": "Classic  Maggi",
        "price": "119",
        "rating": "3.3",
        "rating_count": "(5)",
        "desc": "A timeless favorite that delivers mouthwatering flavors in every bite, perfect for a quick, satisfying vegetarian treat.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/18/da41d996-9ffa-4277-8487-64afade5d708_0fe413d9-9a23-4cbf-9a1c-0a664438630f.JPG",
        "veg": True
    },
    {
        "name": "Egg Maggi",
        "price": "115",
        "rating": "3.4",
        "rating_count": "(8)",
        "desc": "Indulge in a comforting bowl of noodles, perfectly blended with scrambled egg for a delightful, savory experience.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/3/9d99a1e4-4ed0-4087-ac1d-090f8d77ea41_5eee281f-5dd0-4740-8337-d0f60d2698f0.jpg",
        "veg": False
    },
    {
        "name": "Chicken Massala Maggi",
        "price": "119",
        "rating": "3.8",
        "rating_count": "(32)",
        "desc": "A tantalizing blend of flavors that will satisfy any craving for a quick, savory non-Veg delight.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/3/6f0ac1f7-07ef-4cdc-9b14-17cf4b7dad4b_d1abb90f-c109-4ccd-a99a-77384fb0b8b2.jpg",
        "veg": False
    },
    {
        "name": "Classic Cheese Massala Maggi",
        "price": "149",
        "rating": "4.7",
        "rating_count": "(5)",
        "desc": "Deliciously cheesy and flavorful, this quick bite will satisfy your cravings with its classic taste.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/3/010a7d5f-6355-4102-a135-f13deb5ffe11_3ddc8bbb-2db4-451e-aaf5-7aded709b601.jpg",
        "veg": True
    }
]

cake_bros_dishes = [
    {
        "name": "Mayo",
        "price": "20",
        "rating": "4.0",
        "rating_count": "(10)",
        "desc": "Creamy and smooth, perfect as a dip or to add a rich touch to your snacks.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/2/6/a6f5fb4d-a9d8-4043-a9cb-66661a363f58_516778b7-9d46-406c-84d6-6625aee4ebf4.JPG",
        "veg": True
    },
    {
        "name": "Cheese",
        "price": "20",
        "rating": "4.1",
        "rating_count": "(12)",
        "desc": "A creamy and tasty option for cheese lovers, perfect for adding extra indulgence.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/18/7d84dc58-ccb1-47b9-bf1d-a0d4a1c83411_a94a21be-59e9-4181-a81e-6df68febd765.JPG",
        "veg": True
    },
    {
        "name": "Peri peri",
        "price": "20",
        "rating": "4.2",
        "rating_count": "(8)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/2/6/944e5703-f828-4a2c-ba5b-ce807ff8cc67_0f364877-994c-49ae-a8cb-621994c85fcc.JPG",
        "veg": True
    },
    {
        "name": "Schezwan",
        "price": "20",
        "rating": "4.3",
        "rating_count": "(7)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/19/aa3b8a48-631a-4d61-abe4-fa239996399d_01459c7d-48d3-4011-895f-b02e704ea4d2.JPG",
        "veg": True
    },
    {
        "name": "Strawberry shake",
        "price": "99",
        "rating": "4.5",
        "rating_count": "(20)",
        "desc": "A chilled and creamy strawberry shake thats perfect for a refreshing treat.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/2/6/ae40fe08-12ff-4930-b631-efdc2391d5a1_de15a82e-e856-490a-85a5-ecb76c51b268.JPG",
        "veg": True
    },
    {
        "name": "Mango shake",
        "price": "99",
        "rating": "4.6",
        "rating_count": "(18)",
        "desc": "A creamy and refreshing mango treat blended into a chilled shake, perfect for summers.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/17/5cf5cfa9-d252-4601-b944-b0734335fd86_a0fd62df-fb04-4d23-afe6-82555d46ff66.JPG",
        "veg": True
    },
    {
        "name": "Brownie Sundae",
        "price": "149",
        "rating": "4.8",
        "rating_count": "(3)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/1/27/99b7b818-0d2b-4e12-a88b-1ba51af7cb16_8b6a2d71-4a65-47f0-b62a-09d2a2923ef0.JPG",
        "veg": False
    },
    {
        "name": "Papaya juice",
        "price": "80",
        "rating": "4.0",
        "rating_count": "(5)",
        "desc": "",
        "img": "",
        "veg": True
    },
    {
        "name": "Butterscotch Pastrie",
        "price": "89",
        "rating": "4.2",
        "rating_count": "(15)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/3/24/9dcb97f6-9b84-4058-b741-c7826a840d9e_8d6ec268-dc98-4296-a0ee-333ec8bd1d93.jpg",
        "veg": False
    },
    {
        "name": "Vancho Pastrie",
        "price": "89",
        "rating": "4.0",
        "rating_count": "(9)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/3/24/d15d34a5-d311-442b-94ed-bad3040b8886_69a123bc-bffc-4b42-9fec-cab9135ce442.jpg",
        "veg": False
    },
    {
        "name": "Chocolate Pastrie",
        "price": "89",
        "rating": "4.4",
        "rating_count": "(13)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/3/24/a1d3f0fd-50c6-4c2e-9e38-e7755b34002c_1a1c977d-2617-4f09-b4fb-91d34f9a4b63.jpg",
        "veg": False
    },
    {
        "name": "Black Forest Pastrie",
        "price": "69",
        "rating": "4.1",
        "rating_count": "(8)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/71fff509a58eef55e2833089135d4dc7",
        "veg": False
    },
    {
        "name": "White Forest Pastrie",
        "price": "69",
        "rating": "4.0",
        "rating_count": "(10)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/3/24/e5eadbd4-a393-4e98-9d1c-add280111b3a_f93f6798-e21d-48e4-9187-2d5394a3f99b.jpg",
        "veg": False
    },
    {
        "name": "Brownie Pastrie",
        "price": "79",
        "rating": "3.2",
        "rating_count": "(12)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/3/24/cc67a09d-9f14-4525-bb03-5f4577db91bf_54491cf5-0d0e-4328-abf0-f442657bbc63.jpg",
        "veg": False
    },
    {
        "name": "Vanilla Cupcake (2 Pcs)",
        "price": "109",
        "rating": "4.2",
        "rating_count": "(11)",
        "desc": "",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/10/6/a2e9f140-7d2d-4eca-9870-b515000bf08c_bc2da332-1ade-4a7c-a692-6d9d6340a696.jpg",
        "veg": True
    }
]

cring_burger_dishes = [
    {
        "name": "Cring's Regular Veg Burger",
        "price": "169",
        "rating": "5.0",
        "rating_count": "(3)",
        "desc": "Veg patty, soft burger bun, lettuce, mayo, tomato ketchup, onion, tomato. Product Image is for illustrative purpose only",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/5/21/a4016816-aea2-4d99-814d-5afcd3b16030_2de92c32-1026-41b5-8256-81abb6e029d4.jpg",
        "veg": True
    },
    {
        "name": "Cring's Veg Cheese Burger",
        "price": "189",
        "rating": "",
        "rating_count": "",
        "desc": "Veg patty, soft burger bun, lettuce, cheese slice, mayo, tomato ketchup, onion, tomato. Product Image is for illustrative purpose only",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/5/21/5f9f34ec-3f96-45e8-ad41-f44ba12746c7_8b5bc2cd-bcbc-4d43-a866-8be2ef110740.jpg",
        "veg": True
    },
    {
        "name": "Cring's Regular Chicken Burger",
        "price": "179",
        "rating": "",
        "rating_count": "",
        "desc": "Chicken patty, soft burger bun, lettuce, mayo, tomato ketchup, onion, tomato.  Product Image is for illustrative purpose only",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/5/21/8f539bef-bd2d-4cfb-b1a6-9251c3c71727_51cac584-13fc-4773-83f0-4ef0b5b89e0d.jpg",
        "veg": False
    },
    {
        "name": "Cring's Chicken Cheese Burger",
        "price": "199",
        "rating": "4.5",
        "rating_count": "(17)",
        "desc": "Chicken patty, soft burger bun, lettuce, cheese slice, mayo, tomato ketchup, onion, tomato.  Product Image is for illustrative purpose only",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/5/21/6d08f5f5-b682-4193-a353-0c4cd318edc1_2ca2b8e1-f930-4c81-9099-993ec6cb29ac.jpg",
        "veg": False
    },
    {
        "name": "Cring's Regular Beef Burger",
        "price": "229",
        "rating": "",
        "rating_count": "",
        "desc": "Beef patty, soft burger bun, lettuce, mayo, tomato ketchup, onion, tomato.  Product Image is for illustrative purpose only",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/5/21/1d3a88b8-b0bb-496e-95a1-f5b9759cfff4_980aa1b8-632f-4aff-a8ef-cab2ff1a53ff.jpg",
        "veg": False
    },
    {
        "name": "Cring's Beef Cheese Burger",
        "price": "249",
        "rating": "4.2",
        "rating_count": "(14)",
        "desc": "Beef patty, soft burger bun, lettuce, cheese slice, mayo, tomato ketchup, onion, tomato.  Product Image is for illustrative purpose only",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/5/21/07616fbf-8d64-48d2-a8a0-870c9cc6b558_0bf44ed7-6c61-4585-94c2-27c49848d69c.jpg",
        "veg": False
    },
    {
        "name": "Chicken Creamy Pasta",
        "price": "349",
        "rating": "",
        "rating_count": "",
        "desc": "Ingredients:  boneless chicken, bell papers, zucchini, Italian herbs and white sauce.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/7/18/40089f55-0b4e-4183-9089-da9e230a6b50_eec6a06a-0152-4dc4-85a1-4a26c34380b1.jpg",
        "veg": False
    },
    {
        "name": "Veg Broccoli Creamy Pasta",
        "price": "319",
        "rating": "",
        "rating_count": "",
        "desc": "Ingredients: Bellpapers, zucchini, Italian herbs and white sauce, Cheese",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2024/7/18/92c1ba15-94c1-43c7-a126-203b4f0fd33e_53964292-1644-4bd8-bc48-cfea95f406ec.jpg",
        "veg": True
    },
    {
        "name": "Grilled Veg Cheese Burger",
        "price": "199",
        "rating": "",
        "rating_count": "",
        "desc": "Grilled vegetables, soft burger bun, Cheese slice,  lettuce, cheese slice, mayo, tomato ketchup, onion, tomato. *Disclaimer: Image for Illustration Purposes Only: Actual product may vary in appearance.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/5/21/8bdf0ac5-2e54-4ae6-81d4-ebb1eee39604_46857fbc-fafa-43e5-8112-5d0df642a490.jpg",
        "veg": True
    },
    {
        "name": "Shredded Beef Mushroom Burger",
        "price": "299",
        "rating": "4.9",
        "rating_count": "(3)",
        "desc": "Mushroom and shredded Beef deep fried and served with Herbed cheese seasoning Mustard sauce and Layered with Freshly Lettuce(Iceberg),Tomato, Onion, Jalapeno  on a  butter soft bun. *Disclaimer: Image for Illustration Purposes Only: Actual product may vary in appearance.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/5/21/974e9271-9afe-4038-8d21-4637cbd2a19b_bb500760-3415-455f-a12b-67643dde9721.jpg",
        "veg": False
    },
    {
        "name": "Thai Shredded Beef Burger",
        "price": "319",
        "rating": "",
        "rating_count": "",
        "desc": "Boneless Beef, soft burger bun, lettuce, Thai Sweet Chilli Sauce, mayo, tomato ketchup, onion, tomato. *Disclaimer: Image for Illustration Purposes Only: Actual product may vary in appearance.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2025/10/4/476caa61-d04a-4b17-aa68-055f80ba2a75_2c5c3c7f-3bef-456d-a92d-a9769e4ce6b7.jpg",
        "veg": False
    },
    {
        "name": "Thai Shredded Chicken Burger",
        "price": "299",
        "rating": "4.6",
        "rating_count": "(11)",
        "desc": "Grilled chicken, soft burger bun, lettuce, Thai Sweet Chilli Sauce, mayo, tomato ketchup, onion, tomato. *Disclaimer: Image for Illustration Purposes Only: Actual product may vary in appearance.",
        "img": "",
        "veg": False
    }
]

chefette_dishes = [
    {
        "name": "Double Egg Supreme Sandwich",
        "price": "139",
        "rating": "",
        "rating_count": "",
        "desc": "Double fluffy omelette, fresh lettuce, tomatoes, onions, creamy mayo, and butter-toasted grilled white bread for the ultimate protein-packed sandwich.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/f6f1ff2d-8f30-4a0e-876d-8fbda5e94a66_3841ebfc-3c53-41bf-8943-12cb14268edc.png_compressed",
        "veg": False
    },
    {
        "name": "Cheesy Broccoli Pepper Melt Sandwich",
        "price": "149",
        "rating": "",
        "rating_count": "",
        "desc": "A premium grilled sandwich loaded with tender broccoli, crunchy red peppers, and a generous layer of creamy mozzarella and cheddar cheese, seasoned with herbs and black pepper, then toasted between buttery white bread until perfectly golden. Crispy, cheesy, and bursting with flavor in every bite.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/78915df2-bb4b-44a7-8b32-d65e540275c2_c4a35917-ae84-46f1-a5f6-7193598d5470.png_compressed",
        "veg": True
    },
    {
        "name": "Classic Paneer Tikka Sandwich",
        "price": "149",
        "rating": "",
        "rating_count": "",
        "desc": "Soft, butter-toasted white bread grilled to golden perfection and loaded with smoky paneer tikka cubes tossed in indian spices, crunchy onions, tomatoes, capsicum, crisp lettuce, and creamy tandoori mayo.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/4fa42dce-2caa-450a-8548-97a89ad5b77d_2c1bb373-cbd8-4a28-8d08-b88316ac6191.png_compressed",
        "veg": True
    },
    {
        "name": "Tandoori Chicken Crunchy Sandwich (White / Wheat)",
        "price": "149",
        "rating": "4.0",
        "rating_count": "(2)",
        "desc": "A bold and flavour-packed sandwich made with juicy tandoori-spiced chicken, fresh onions, crisp lettuce and a creamy mint mayo blend. Served in 4” toasted bread slices — available in both white & wheat options. Perfectly grilled for a smoky, satisfying bite.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/303d44eb-36bf-443f-bec0-e2d70e3cd7b5_030be9a6-7a02-4991-85e0-00f2dc92de66.png_compressed",
        "veg": False
    },
    {
        "name": "Chicken Broccoli Protein Sandwich",
        "price": "169",
        "rating": "",
        "rating_count": "",
        "desc": "The sandwich has melted cheese, crisp iceberg lettuce, red onion, broccoli, and grilled chicken layered inside",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/204edabe-be27-4794-9aaf-0fec396628e9_097007d9-a1a5-41ef-9db8-7d90fa6c3d5e.png_compressed",
        "veg": False
    },
    {
        "name": "Paneer Egg Fusion Sandiwich",
        "price": "169",
        "rating": "",
        "rating_count": "",
        "desc": "The paneer egg fusion sandwich made with grilled bread, spiced paneer, fluffy egg, melted cheese, crisp lettuce, tomato, onion, and creamy sauce",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/67325273-fc3c-46bd-8009-c03401bf1903_8f1a9c2f-91a1-4382-8c90-175e3f547572.png_compressed",
        "veg": False
    },
    {
        "name": "Panjabi Tandoori Paneer Sandwich",
        "price": "169",
        "rating": "",
        "rating_count": "",
        "desc": "The punjabi tandoori paneer sandwich is featuring smoky tandoori paneer, crisp lettuce, onions, capsicum, creamy tandoori sauce, and perfectly grilled & stacked in white bread",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/496266ec-8b36-43b2-8e5e-41ca9c14fc5f_b023abd1-c240-43c4-896a-2b388bd4df6e.png_compressed",
        "veg": True
    },
    {
        "name": "Tandoori Chicken & Egg Club Sandwich",
        "price": "189",
        "rating": "",
        "rating_count": "",
        "desc": "Double-decker grilled sandwich layered with smoky tandoori chicken, fluffy egg, fresh veggies, and creamy tandoori mayo in butter-toasted white bread.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/ba86e643-fea4-441b-9e34-5d46fa7b9f30_74dd31d7-136e-4342-a3bc-0ce64619e05c.png_compressed",
        "veg": False
    },
    {
        "name": "High Protein Mixed Sandwich (Chicken+paneer+broccoli)",
        "price": "209",
        "rating": "",
        "rating_count": "",
        "desc": "Grilled chicken, tandoori paneer, fresh broccoli, crisp veggies, and creamy herb mayo layered in butter-toasted white bread for a delicious high-protein meal.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/29/39aa6adf-48a9-4123-8075-3e2bfb518fd1_a70f14ac-cb68-40d0-9bc2-9a8470a4c8e3.png_compressed",
        "veg": False
    },
    {
        "name": "Tandoori Chicken Sandwich",
        "price": "129",
        "rating": "",
        "rating_count": "",
        "desc": "Smoky, juicy tandoori chicken tossed in mint mayo, layered with crispy lettuce and onions, inside a perfectly toasted sandwich.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/13/6e29a426-8b08-4ba9-88b5-397b93e97ccf_fe4901bd-3c7b-41c5-96ad-f0eb8c82e14e.png_compressed",
        "veg": False
    },
    {
        "name": "Classic Chicken Sandwich [Three Layer ]",
        "price": "189",
        "rating": "",
        "rating_count": "",
        "desc": "Butter toasted 5\" bread slices, featuring grilled shredded chicken breasts mixed with iceberg lettuce, tomatoes, cucumber, onion, with tasty classic mayo sauce paired with ketchup",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/13/aa99b364-8706-4998-84d5-0af3c951b3b1_c0835c82-a914-4a34-98c9-29dac8aeec41.png_compressed",
        "veg": False
    },
    {
        "name": "Wheat Chicken Sandwich",
        "price": "199",
        "rating": "",
        "rating_count": "",
        "desc": "Butter-toasted whole wheat bread filled with grilled chicken breast, fresh lettuce, tomatoes, cucumber, onions, creamy mayo, and ketchup for a healthy, flavorful sandwich.",
        "img": "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_300,h_300,c_fit/FOOD_CATALOG/IMAGES/CMS/2026/7/13/b87d788a-383d-44a5-bf3e-f1623de447ae_188195cf-13e6-499e-957b-491c44125cbc.png_compressed",
        "veg": False
    },
    {
        "name": "Tuna Sandwich Box",
        "price": "229",
        "rating": "",
        "rating_count": "",
        "desc": "Creamy tuna salad with fresh lettuce, tomatoes, onions, and signature herb mayo in butter-toasted grilled white bread",
        "img": "",
        "veg": False
    }
]

def render_dish(dish, dish_id):
    if dish['veg']:
        icon_svg = '<svg viewBox="0 0 20 20" width="16" height="16" class="sc-eWVJoQ cxxFkr"><rect x="2" y="2" width="16" height="16" rx="3" fill="none" stroke="#0f8a65" stroke-width="2"/><circle cx="10" cy="10" r="4.5" fill="#0f8a65"/></svg>'
    else:
        icon_svg = '<svg viewBox="0 0 20 20" width="16" height="16" class="sc-eWVJoQ cxxFkr"><rect x="2" y="2" width="16" height="16" rx="3" fill="none" stroke="#e43b4f" stroke-width="2"/><polygon points="10,4.5 15.5,14.5 4.5,14.5" fill="#e43b4f"/></svg>'
        
    rating_html = ""
    if dish.get('rating'):
        try:
            color = '#116649' if float(dish['rating']) >= 4.0 else '#E6A408'
        except:
            color = '#116649'
        rating_html = f'''<div class="sc-jDWblu ciPLFu"><div class="sc-eeLFso bPRWxu"><svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" fillColor="{color}"><rect width="14" height="14" fill="transparent"></rect><path d="M5.67163 3.99166C6.22068 2.34179 6.49521 1.51686 7 1.51686C7.50479 1.51686 7.77932 2.34179 8.32837 3.99166L8.65248 4.96556H9.60668C11.4122 4.96556 12.315 4.96556 12.4703 5.45302C12.6256 5.94049 11.8893 6.4628 10.4167 7.50744L9.67376 8.03444L9.97544 8.94095C10.5325 10.615 10.8111 11.452 10.4033 11.754C9.99553 12.056 9.27604 11.5457 7.83705 10.5249L7 9.93112L6.16295 10.5249C4.72396 11.5457 4.00447 12.056 3.5967 11.754C3.18893 11.452 3.46747 10.615 4.02456 8.94095L4.04557 8.87783C4.18081 8.47145 4.24843 8.26825 4.18684 8.08006C4.12525 7.89187 3.94958 7.76725 3.59824 7.51802C2.11566 6.46633 1.37437 5.94049 1.52971 5.45302C1.68504 4.96556 2.5878 4.96556 4.39332 4.96556H5.34752L5.67163 3.99166Z" fill="{color}"></path></svg></div><div class="sc-dlfnOL fpLIrj sc-kYpsJR bzekZl">{dish['rating']}</div><div class="sc-dlfnOL pDfZF sc-kYpsJR lhLgBz">{dish['rating_count']}</div></div>'''

    veg_str = 'veg' if dish['veg'] else 'nonveg'
    desc_html = f'<div class="sc-fUfliA iGdIQY"><div aria-hidden="true" class="sc-dlfnOL ipuZJn sc-jSUnEA jaouuY">{dish["desc"]}</div></div>' if dish.get('desc') else ''
    
    img_html = ""
    if dish.get('img'):
        img_html = f"""<button aria-label="See more information" class="sc-iUeFge fxIkFp" style="background: rgb(246, 230, 233);">
      <img alt="{dish['name']}" class="_3XS7H" height="144" loading="lazy" width="156" src="{dish['img']}">
    </button>"""
    
    return f"""<div data-testid="normal-dish-item" class="sc-jiVjYv gRIQgR" data-id="dish-{dish_id}" data-name="{dish['name'].lower()}" data-type="{veg_str}" data-bestseller="true">
  <div class="sc-goLLcu jEJsYT">
    <div>
      <div aria-hidden="true" class="sc-eWmBjE bSWzBq">
        {icon_svg}
      </div>
      <h3 aria-hidden="true" class="sc-dlfnOL hJCbXn sc-bxIdbF hEeFlr">{dish['name']}</h3>
      <div class="sc-kYpOdn gRmCvj">
        <div aria-hidden="true" class="sc-jSgsbC ewmHof">
          <span class="sc-eCsseJ kiCBpN"><div class="sc-dlfnOL cWZrLo">₹{dish['price']}</div></span>
        </div>
      </div>
      {rating_html}
      {desc_html}
    </div>
  </div>
  <div aria-hidden="true" class="sc-jmAvkx bIQAsK">
    {img_html}
    <div class="sc-fXJWTj goDnKo">
      <div style="position: relative;">
        <div class="sc-cBNeAB hIFViE">
          <div class="sc-jcVbNL dfmBqs" id="dishAction-dish-{dish_id}">
            <button class="swiggy-main-add-btn" onclick="handleAddClick({{id:'dish-{dish_id}',name:'{dish['name'].replace(chr(39), chr(92)+chr(39))}',price:{dish['price']},type:'{veg_str}'}}, false)">ADD</button>
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
    html = html.replace('>Palayam<', f'>{r["location"]}<')
    
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
    elif r['id'] == 4:
        target_dishes = mothers_veg_dishes
    elif r['id'] == 5:
        target_dishes = birdie_bite_dishes
    elif r['id'] == 6:
        target_dishes = cake_bros_dishes
    elif r['id'] == 7:
        target_dishes = cring_burger_dishes
    elif r['id'] == 8:
        target_dishes = chefette_dishes

    if target_dishes:
        dishes_html = '\n'.join([render_dish(d, idx) for idx, d in enumerate(target_dishes)])
        
        marker1 = 'id="recItemsBlock">'
        marker2 = '<!-- Exact Swiggy Menu FAB'
        
        if marker1 in html and marker2 in html:
            idx1 = html.find(marker1) + len(marker1)
            idx2 = html.find(marker2)
            
            prefix = html[:idx1]
            suffix = html[idx2:]
            
            # Load the footer
            footer_path = r'C:\Users\ADITHYAN\.gemini\antigravity-ide\brain\ad67dd81-9167-4734-b024-b96466a9b7b0\scratch\footer.html'
            import os
            if os.path.exists(footer_path):
                with open(footer_path, 'r', encoding='utf-8') as ff:
                    footer_html = ff.read()
            else:
                footer_html = ""
            
            html = prefix + '\n' + dishes_html + '\n</div></div></div></div>\n' + footer_html + '\n\n  ' + suffix
            print(f"Successfully injected dishes for restaurant {r['id']} ({r['name']})")
        else:
            print(f"Could not find markers for restaurant {r['id']}")

    filename = f'restaurant{r["id"]}.html'
    with open(filename, 'w', encoding='utf-8') as out:
        out.write(html)
        
print("Regenerated restaurant HTML files successfully.")
