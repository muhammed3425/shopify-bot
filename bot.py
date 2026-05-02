from flask import Flask, jsonify
import requests
import threading
import time
import os

app = Flask(__name__)

# --- AYARLAR (Abdurrahman gelince buraları dolduracak) ---
SHOP_URL = "https://MAGAZA-ADIN.myshopify.com"
TOKEN = "SHPAT_ANAHTARIN"
YASAKLI_KELIMELER = ["çakma", "replika", "silah", "illegal", "kumar"]

status = {"bot": "çalışıyor", "eklenen_urun": 0}

# --- GÜVENLİK FİLTRESİ ---
def guvenli_mi(urun_adi):
    for kelime in YASAKLI_KELIMELER:
        if kelime in urun_adi.lower():
            return False
    return True

# --- PAZAR TARAMASI FONKSİYONU ---
def pazar_taramasi():
    # Bu fonksiyon arka planda keşif yapar
    bulunan_urunler = [
        {"ad": "Mini Taşınabilir Yazıcı", "trend": "Yüksek", "kar_marji": "%40"},
        {"ad": "Akıllı Temizleme Fırçası", "trend": "Orta-Yüksek", "kar_marji": "%35"}
    ]
    return bulunan_urunler

# --- BOTUN ANA DÖNGÜSÜ ---
def bot_loop():
    while True:
        # Bot her 60 saniyede bir dükkanı ve piyasayı kontrol eder
        pazar_taramasi()
        time.sleep(60)

# --- PANELİN YENİ PREMİUM TASARIMI ---
@app.route("/")
def home():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Luvrenzo AI Control Panel</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #1a1a1a; /* Koyu Gri / Siyah Arka Plan */
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }}
            .panel-container {{
                border: 1px solid #444;
                padding: 60px;
                background-color: #262626; /* Panel Grisi */
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.7);
            }}
            h1 {{
                font-size: 3.5em;
                margin-bottom: 20px;
                letter-spacing: 8px;
                text-transform: uppercase;
                background: linear-gradient(to bottom, #ffffff, #888888);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .status-box {{
                font-size: 1.2em;
                margin-top: 20px;
                color: #aaa;
            }}
            .status-badge {{
                background-color: #28a745;
                color: white;
                padding: 6px 18px;
                border-radius: 50px;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.9em;
                box-shadow: 0 0 15px rgba(40, 167, 69, 0.4);
            }}
            .footer-text {{
                margin-top: 40px;
                font-style: italic;
                color: #666;
                letter-spacing: 2px;
            }}
        </style>
    </head>
    <body>
        <div class="panel-container">
            <h1>LUVRENZO AI</h1>
            <div class="status-box">
                SİSTEM DURUMU: <span class="status-badge">{status['bot']}</span>
            </div>
            <p style="margin-top: 15px; color: #888;">Mağaza Bağlantısı Bekleniyor...</p>
            <div class="footer-text">EBEDİ MANZARANIN KORUYUCUSU</div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    # Botu daemon olarak başlatıyoruz ki sistem kapanmasın
    threading.Thread(target=bot_loop, daemon=True).start()
    # Render'ın istediği portu otomatik ayarla
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
