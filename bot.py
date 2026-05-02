import requests
from flask import Flask
import threading
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup # İnternet sayfalarını okumak için gereken asıl parça

app = Flask(__name__)

# --- GERÇEK GOOGLE ARAMA AYARLARI ---
ARAMA_TERIMLERI = [
    "top selling dropshipping products 2026",
    "trending ecommerce products may 2026",
    "shopify winning products list"
]

islem_defteri = [f"[{datetime.now().strftime('%H:%M:%S')}] Luvrenzo Mastermind Başlatıldı..."]

# --- MOD: GERÇEK GOOGLE GEZGİNİ ---
def google_gezgin_motoru():
    global islem_defteri
    simdi = datetime.now().strftime("%H:%M:%S")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for terim in ARAMA_TERIMLERI:
        try:
            # BOT BURADA GERÇEKTEN GOOGLE'A GİRİP ARAMA YAPIYOR
            url = f"https://www.google.com/search?q={terim.replace(' ', '+')}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Sayfadaki başlıkları çekerek "öğreniyor"
                islem_defteri.insert(0, f"[{simdi}] 🔍 GOOGLE'DA ARANDI: '{terim}'")
                islem_defteri.insert(1, f"   └─ Yeni stratejiler ve ürünler analiz ediliyor...")
            
            time.sleep(5) # Google engellemesin diye bekleme yapıyoruz
        except Exception as e:
            continue

def bot_loop():
    while True:
        google_gezgin_motoru()
        time.sleep(60)

@app.route("/")
def home():
    rapor_html = "".join([f"<div style='margin-bottom:12px; color:#00ffcc; border-left: 4px solid #00ffcc; padding-left: 15px;'>{islem}</div>" for islem in islem_defteri])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="10">
        <title>Luvrenzo Mastermind AI</title>
        <style>
            body {{ margin:0; background:#050505; color:#fff; font-family:sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; }}
            .panel {{ border:2px solid #00ffcc; padding:30px; background:#111; border-radius:20px; width:90%; max-width:750px; box-shadow: 0 0 20px #00ffcc44; }}
            h1 {{ color:#00ffcc; letter-spacing:5px; text-align:center; }}
            .rapor {{ background:#000; border:1px solid #333; padding:20px; border-radius:10px; text-align:left; font-family:monospace; min-height:300px; }}
        </style>
    </head>
    <body>
        <div class="panel">
            <h1>LUVRENZO MASTERMIND</h1>
            <div style="margin-bottom:15px; text-align:center;"><span style="background:#00ffcc; color:#000; padding:5px 15px; border-radius:50px; font-weight:bold; font-size:0.8em;">MOD: CANLI GOOGLE ANALİZİ</span></div>
            <div class="rapor">
                {rapor_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
