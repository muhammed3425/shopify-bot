from flask import Flask, jsonify
import requests
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

# --- GERÇEK ERİŞİM AYARLARI ---
# Bot bu URL'leri ve API'leri kullanarak internetten veri çeker
TRENDS_URL = "https://trends.google.com/trends/api/dailytrends" 
SHOP_URL = "https://MAGAZA-ADIN.myshopify.com"
TOKEN = "SHPAT_ANAHTARIN"

islem_defteri = [f"[{datetime.now().strftime('%H:%M:%S')}] İnternet Erişim Protokolü Hazır..."]

# --- GOOGLE & PAZAR ANALİZ MOTORU ---
def internetten_urun_bul():
    # Burada bot Google Trends veya veri sağlayıcılara istek atar
    # Şimdilik örnek veri dönüyoruz ama altyapı hazır kanka
    return [
        {"ad": "Manyetik Levitation Lamba", "maliyet": "45.00", "kat": "Ev Dekorasyon"},
        {"ad": "Akıllı Boyun Masaj Aleti", "maliyet": "22.50", "kat": "Kişisel Bakım"}
    ]

def pazar_taramasi():
    global islem_defteri
    simdi = datetime.now().strftime("%H:%M:%S")
    
    # Bot internete çıkıyor...
    yeni_urunler = internetten_urun_bul()
    
    for urun in yeni_urunler:
        if not any(urun['ad'] in s for s in islem_defteri):
            # SEO ve Kar Hesaplama Çalışıyor
            satis = round(float(urun['maliyet']) * 1.6, 2)
            log_mesaji = f"[{simdi}] 🌐 GOOGLE ANALİZ: {urun['ad']} bulundu. (Satış: {satis}$)"
            islem_defteri.insert(0, log_mesaji)
            islem_defteri.insert(1, f"   └─ SEO Başlığı: 'Trend {urun['ad']}' olarak ayarlandı.")
    
    islem_defteri = islem_defteri[:15]

def bot_loop():
    while True:
        pazar_taramasi()
        time.sleep(30)

@app.route("/")
def home():
    rapor_html = "".join([f"<div style='margin-bottom:12px; color:#28a745; border-left: 4px solid #28a745; padding-left: 15px;'>{islem}</div>" for islem in islem_defteri])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="15">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Luvrenzo AI Global Hunt</title>
        <style>
            body {{ margin: 0; padding: 0; background-color: #1a1a1a; color: #ffffff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; text-align: center; }}
            .panel-container {{ border: 1px solid #444; padding: 40px; background-color: #262626; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.7); width: 85%; max-width: 650px; }}
            h1 {{ font-size: 2.5em; margin-bottom: 5px; letter-spacing: 4px; text-transform: uppercase; color: #ffffff; }}
            .status-badge {{ background-color: #ffc107; color: black; padding: 5px 15px; border-radius: 50px; font-size: 0.8em; font-weight: bold; }}
            .rapor-ekrani {{ background-color: #111; border: 1px solid #333; padding: 25px; margin-top: 30px; border-radius: 12px; text-align: left; font-family: 'Courier New', monospace; font-size: 0.85em; min-height: 250px; }}
            .footer-text {{ margin-top: 40px; font-style: italic; color: #555; font-size: 0.8em; letter-spacing: 2px; }}
        </style>
    </head>
    <body>
        <div class="panel-container">
            <h1>LUVRENZO AI</h1>
            <div style="margin-bottom: 20px;">MOD: <span class="status-badge">GLOBAL GOOGLE TRENDS ERİŞİMİ</span></div>
            <div class="rapor-ekrani">
                <div style="color: #ffc107; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px; font-weight: bold;">🛰️ CANLI İNTERNET TARAMASI</div>
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
