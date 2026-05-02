from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

# --- AYARLAR (Abdurrahman gelince buraları dolduracak) ---
SHOP_URL = "https://MAGAZA-ADIN.myshopify.com"
TOKEN = "SHPAT_ANAHTARIN"
YASAKLI_KELIMELER = ["çakma", "replika", "silah", "illegal", "kumar"]

status = {"bot": "uyanıyor", "eklenen_urun": 0}

# --- GÜVENLİK FİLTRESİ ---
def guvenli_mi(urun_adi):
    for kelime in YASAKLI_KELIMELER:
        if kelime in urun_adi.lower():
            return False
    return True

# --- BOTUN ANA DÖNGÜSÜ ---
def bot_loop():
    while True:
        # Burada Abdurrahman'ın dükkanından siparişleri kontrol edecek
        # ve 3'ten fazla satanı analiz edip yeni ürün bulacak.
        print("Luvrenzo AI dükkanı gözlüyor...")
        time.sleep(60)

@app.route("/")
def home():
    return f"<h1>🤖 LUVRENZO AI PANEL</h1><p>Durum: {status['bot']}</p>"

if __name__ == "__main__":
    # Render için port ayarı
    threading.Thread(target=bot_loop).start()
    app.run(host="0.0.0.0", port=10000)
