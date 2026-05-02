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
