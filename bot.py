import requests
from flask import Flask
import threading
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

# --- GERÇEK GOOGLE ARAMA TERİMLERİ ---
ARAMA_LISTESI = [
    "best selling dropshipping products 2026",
    "trending shopify items may 2026",
    "most profitable dropshipping niches"
]

islem_defteri = [f"[{datetime.now().strftime('%H:%M:%S')}] Luvrenzo AI Gözlerini Açtı..."]

def google_gercek_arama():
    global islem_defteri
    simdi = datetime.now().strftime("%H:%M:%S")
    
    # GOOGLE'I KANDIRAN "İNSAN" KİMLİĞİ (Headers)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }

    for terim in ARAMA_LISTESI:
        try:
            # BOT BURADA GERÇEKTEN GOOGLE'A GİRİYOR
            search_url = f"https://www.google.com/search?q={terim.replace(' ', '+')}"
            response = requests.get(search_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Sayfanın içine girip başlıkları (h3 etiketlerini) okuyoruz
                soup = BeautifulSoup(response.text, 'html.parser')
                basliklar = soup.find_all('h3')
                
                log = f"[{simdi}] 🔍 GOOGLE'DA ARANDI: '{terim}'"
                islem_defteri.insert(0, log)
                
                # İlk 2 sonucu panele yazdır ki arama yaptığını gözünle gör kanka
                for i, b in enumerate(basliklar[:2]):
                    islem_defteri.insert(0, f"   └─ Bulunan Kaynak: {b.get_text()[:50]}...")
            
            time.sleep(10) # Google çakmasın diye 10 saniye mola veriyor
        except Exception as e:
            islem_defteri.insert(0, f"[{simdi}] ⚠️ Google Erişimi Zorlanıyor...")
            continue

def bot_loop():
    while True:
        google_gercek_arama()
        time.sleep(120) # 2 dakikada bir yeni arama

@app.route("/")
def home():
    rapor_html = "".join([f"<div style='margin-bottom:12px; color:#00ffcc; border-left: 4px solid #00ffcc; padding-left: 15px;'>{islem}</div>" for islem in islem_defteri])
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="10">
        <title>Luvrenzo AI Real Search</title>
        <style>
            body {{ margin:0; background:#050505; color:#fff; font-family:sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; }}
            .panel {{ border:2px solid #00ffcc; padding:30px; background:#111; border-radius:20px; width:90%; max-width:750px; box-shadow: 0 0 20px #00ffcc44; }}
            h1 {{ color:#00ffcc; text-align:center; }}
            .rapor {{ background:#000; border:1px solid #333; padding:20px; border-radius:10px; text-align:left; font-family:monospace; min-height:350px; font-size:0.85em; overflow:hidden; }}
        </style>
    </head>
    <body>
        <div class="panel">
            <h1>LUVRENZO MASTERMIND</h1>
            <div style="text-align:center; margin-bottom:10px; color:#00ffcc;">● GERÇEK ZAMANLI GOOGLE ANALİZİ AKTİF</div>
            <div class="rapor">{rapor_html}</div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
