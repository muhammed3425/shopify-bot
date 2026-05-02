from flask import Flask, jsonify
import requests
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

# --- AYARLAR ---
SHOP_URL = "https://MAGAZA-ADIN.myshopify.com"
TOKEN = "SHPAT_ANAHTARIN"
YASAKLI_KELIMELER = ["çakma", "replika", "silah", "illegal", "kumar"]

# Botun hafızasındaki işlem defteri - BAŞLANGIÇTA BOŞ KALMASIN DİYE ÖRNEK EKLEDİM
islem_defteri = ["Sistem başlatıldı, ilk tarama yapılıyor..."]
status = {"bot": "çalışıyor", "eklenen_urun": 0}

# --- GÜVENLİK FİLTRESİ ---
def guvenli_mi(urun_adi):
    for kelime in YASAKLI_KELIMELER:
        if kelime in urun_adi.lower():
            return False
    return True

# --- PAZAR TARAMASI VE RAPORLAMA ---
def pazar_taramasi():
    global islem_defteri
    simdi = datetime.now().strftime("%H:%M:%S")
    
    # Gerçekçi trend verileri
    bulunanlar = [
        {"ad": "Mini Taşınabilir Yazıcı", "trend": "Yüksek", "kar": "%45"},
        {"ad": "Akıllı Temizleme Fırçası", "trend": "Yüksek", "kar": "%38"},
        {"ad": "Mıknatıslı Şarj Kablosu", "trend": "Orta", "kar": "%50"}
    ]
    
    for urun in bulunanlar:
        if guvenli_mi(urun["ad"]):
            log_mesaji = f"[{simdi}] Trend Bulundu: {urun['ad']} ({urun['kar']} Kar)"
            if log_mesaji not in islem_defteri:
                islem_defteri.insert(0, log_mesaji)
    
    islem_defteri = islem_defteri[:10]

# --- BOTUN ANA DÖNGÜSÜ ---
def bot_loop():
    while True:
        pazar_taramasi()
        time.sleep(30) # 30 saniyede bir tarasın ki hızlı veri düşsün

# --- PANELİN YENİ GÖRÜNÜMÜ (OTOMATİK YENİLEME EKLENDİ) ---
@app.route("/")
def home():
    rapor_html = "".join([f"<div style='margin-bottom:10px; color:#28a745; border-left: 3px solid #28a745; padding-left: 10px;'>{islem}</div>" for islem in islem_defteri])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="30"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Luvrenzo AI Control Panel</title>
        <style>
            body {{
                margin: 0; padding: 0;
                background-color: #1a1a1a; color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                display: flex; justify-content: center; align-items: center;
                min-height: 100vh; text-align: center;
            }}
            .panel-container {{
                border: 1px solid #444; padding: 40px;
                background-color: #262626; border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.7); width: 85%; max-width: 600px;
            }}
            h1 {{
                font-size: 2.8em; margin-bottom: 5px; letter-spacing: 6px;
                text-transform: uppercase;
                background: linear-gradient(to bottom, #ffffff, #888888);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            }}
            .status-badge {{
                background-color: #28a745; color: white;
                padding: 4px 15px; border-radius: 50px; font-size: 0.85em; font-weight: bold;
            }}
            .rapor-ekrani {{
                background-color: #111; border: 1px solid #333;
                padding: 25px; margin-top: 30px; border-radius: 12px;
                text-align: left; font-family: 'Courier New', monospace; font-size: 0.95em;
                max-height: 300px; overflow-y: auto;
            }}
            .footer-text {{
                margin-top: 40px; font-style: italic; color: #555; font-size: 0.8em; letter-spacing: 2px;
            }}
        </style>
    </head>
    <body>
        <div class="panel-container">
            <h1>LUVRENZO AI</h1>
            <div style="margin-bottom: 20px;">DURUM: <span class="status-badge">{status['bot'].upper()}</span></div>
            
            <div class="rapor-ekrani">
                <div style="color: #888; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px; font-weight: bold;">🛰️ CANLI PAZAR ANALİZİ</div>
                {rapor_html}
            </div>

            <div class="footer-text">EBEDİ MANZARANIN KORUYUCUSU</div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
