from flask import Flask, jsonify
import time
import threading

app = Flask(__name__)

status = {
    "bot": "çalışıyor",
    "eklenen_urun": 0
}

def bot_loop():
    while True:
        print("BOT ÇALIŞIYOR")
        status["eklenen_urun"] += 1
        time.sleep(60)

@app.route("/")
def home():
    return f"""
    <h1>🤖 BOT PANEL</h1>
    <p>Durum: {status['bot']}</p>
    <p>Eklenen ürün: {status['eklenen_urun']}</p>
    """

@app.route("/status")
def get_status():
    return jsonify(status)

threading.Thread(target=bot_loop).start()

app.run(host="0.0.0.0", port=10000)
sales = count_sales()

def should_add(product_name):
    if product_name in sales:
        if sales[product_name] >= 3:
            return True
        else:
            return False
    return True  # yeni ürünse dene
    product = choose_product()

if should_add(product["title"]):
    upload_to_shopify(product["title"], price(product["price"]))
    GET /admin/api/2023-10/orders.json
    import requests

SHOP_URL = "https://YOUR_STORE.myshopify.com"
TOKEN = "YOUR_TOKEN"

def get_orders():
    url = f"{SHOP_URL}/admin/api/2023-10/orders.json"

    headers = {
        "X-Shopify-Access-Token": TOKEN
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data["orders"]
def count_sales():
    orders = get_orders()
    
    product_sales = {}

    for order in orders:
        for item in order["line_items"]:
            name = item["title"]

            if name not in product_sales:
                product_sales[name] = 0

            product_sales[name] += item["quantity"]

    return product_sales
    {
 "LED Light Strip": 5,
 "Mini Fan": 2
    }
    prompt = f"""
Bu ürün {sales} adet satıldı.
Neden satmış olabilir?
"""
